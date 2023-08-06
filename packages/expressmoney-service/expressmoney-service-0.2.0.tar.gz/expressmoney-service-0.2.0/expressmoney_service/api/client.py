__all__ = ('Request',)

import abc

import requests
from django.contrib.auth import get_user_model
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken


class HttpClient(abc.ABC):
    """Abstract HTTP client"""

    _client = None
    _project = 'expressmoney-service'

    def __init__(self,
                 service: str = 'default',
                 path: str = '/',
                 access_token: str = None,
                 ):
        """
        Common params for all http clients
        Args:
            service: 'default'
            path: '/user'
            access_token: 'Bearer DFD4345345D'
        """
        self._service = service
        self._path = path
        self._access_token = access_token

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def post(self, payload: dict):
        pass

    @abc.abstractmethod
    def put(self, payload: dict):
        pass


class BaseRequest(HttpClient):
    """Base HTTP Client"""

    def __init__(self,
                 service: str = None,
                 path: str = '/',
                 access_token: str = None,
                 timeout: tuple = (30, 30)):
        super().__init__(service=service,
                         path=path,
                         access_token=access_token,
                         )
        self._timeout = timeout

    def get(self, url=None):
        response = requests.get(url if url else self.url, headers=self._headers, timeout=self._timeout)
        return response

    def post(self, payload: dict):
        response = requests.post(self.url, json=payload, headers=self._headers, timeout=self._timeout)
        return response

    def put(self, payload: dict = None):
        payload = {} if payload is None else payload
        response = requests.put(self.url, json=payload, headers=self._headers, timeout=self._timeout)
        return response

    @property
    def url(self):
        domain = f'https://{self._service}-dot-{self._project}.appspot.com'
        url = f'{domain}{self._path}'
        return url

    @property
    def _headers(self):
        headers = dict()
        headers.update(self._get_authorization())
        return headers

    def _get_authorization(self) -> dict:
        return {'X-Forwarded-Authorization': f'Bearer {self._access_token}'} if self._access_token else {}


class Request(BaseRequest):
    """HTTP Client for Django user"""
    IAP_CLIENT_ID = '829013617684-ti6smlt6nd38dc0sj6cq4khku4ims917.apps.googleusercontent.com'

    def __init__(self,
                 service: str = None,
                 path: str = '/',
                 user=None,
                 timeout: tuple = (30, 30),
                 ):
        user_class = get_user_model()
        if not isinstance(user, user_class):
            user = user_class.objects.get(pk=user)

        access_token = RefreshToken.for_user(user).access_token if user is not None else None
        super().__init__(service=service,
                         path=path,
                         access_token=access_token,
                         timeout=timeout
                         )

    def _get_authorization(self) -> dict:
        authorization = super()._get_authorization()
        open_id_connect_token = id_token.fetch_id_token(GoogleRequest(), self.IAP_CLIENT_ID)
        iap_token = {'Authorization': f'Bearer {open_id_connect_token}'}
        authorization.update(iap_token)
        return authorization
