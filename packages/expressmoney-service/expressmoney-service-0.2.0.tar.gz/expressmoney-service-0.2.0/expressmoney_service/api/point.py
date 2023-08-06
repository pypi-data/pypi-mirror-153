__all__ = (
           'Point', 'ContractPoint',
           'ResponseMixin', 'CreatePointMixin',
           'ID', 'Contract',
           )

from typing import OrderedDict

from expressmoney.api import PointNotFound404, PointThrottled, PointClientError, PointServerError
from expressmoney.api.point import PointError
from expressmoney.utils import status
from .contract import Contract
from .id import ID
from .client import Request


class Point:
    """Base endpoint handler"""
    _point_id: ID = None

    def __init__(self,
                 user,
                 timeout: tuple = (30, 30)
                 ):
        self._user = user
        self._response = None
        self._client = Request(service=self._point_id.service,
                               path=self._path,
                               user=user,
                               timeout=timeout,
                               )

    @property
    def _path(self):
        path = self._point_id.path
        return path

    def _post(self, payload: dict):
        self._response = self._client.post(payload=payload)
        self._handle_error(self._response)

    def _get(self, url=None) -> dict:
        self._response = self._client.get(url)
        self._handle_error(self._response)
        data = self._response.json()
        return data

    def _handle_error(self, response):

        if not status.is_success(response.status_code):
            if status.is_client_error(response.status_code):
                if status.is_not_found(response.status_code):
                    raise PointNotFound404(self._client.url)
                if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    raise PointThrottled(self._client.url, response.status_code, response.headers.get(
                        'Retry-After'))
                else:
                    raise PointClientError(self._client.url, response.status_code, response.json())
            else:
                raise PointServerError(self._client.url, response.status_code)


class ContractPoint(Point):
    """Endpoints with validated data by contract"""
    _read_contract = None
    _create_contract = None
    _sort_by = 'id'

    def __init__(self,
                 user,
                 timeout: tuple = (30, 30),
                 ):
        super().__init__(user=user, timeout=timeout)

    def _get_validated_data(self):
        data = self._get()
        contract = self._get_contract(data, True)
        validated_data = contract.validated_data
        return validated_data

    def _get_contract(self, data, is_read: bool) -> Contract:
        contract_class = self._get_contract_class(is_read)
        contract = contract_class(data=data, many=True if is_read else False)
        contract.is_valid(raise_exception=True)
        return contract

    def _get_contract_class(self, is_read: bool):
        return self._read_contract if is_read else self._create_contract


class CreatePointMixin:
    """For type ContractPoint"""

    def create(self, payload: dict):
        if self._create_contract is None:
            raise PointError(f'Set attr create_contract')
        contract = self._get_contract(data=payload, is_read=False)
        self._post(contract.data)


class ResponseMixin:
    """Only for create and update actions"""

    _response_contract = None

    @property
    def response(self) -> OrderedDict:
        if self._response_contract is None:
            raise PointError('Response contract not set')
        if self._response is None:
            raise PointError('First create or update data')
        if self._response.status_code != status.HTTP_201_CREATED:
            raise PointError(f'Response data only for 201 status, current {self._response.status_code}')
        contract = self._response_contract(data=self._response.json())
        contract.is_valid(raise_exception=True)
        return contract.validated_data
