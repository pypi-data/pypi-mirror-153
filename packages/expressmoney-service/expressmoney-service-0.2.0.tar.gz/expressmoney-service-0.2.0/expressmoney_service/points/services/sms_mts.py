__all__ = ('SmsMTSPoint',)

from ...api import *

_SERVICE = 'services'


class _SmsMTSCreateContract(Contract):
    message = serializers.CharField(max_length=60)


class _SmsMTSResponseContract(_SmsMTSCreateContract):
    pass


class _SmsMTSID(ID):
    _service = _SERVICE
    _app = 'sms_mts'
    _view_set = 'sms_mts'


class SmsMTSPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = _SmsMTSID()
    _create_contract = _SmsMTSCreateContract
    _response_contract = _SmsMTSResponseContract
