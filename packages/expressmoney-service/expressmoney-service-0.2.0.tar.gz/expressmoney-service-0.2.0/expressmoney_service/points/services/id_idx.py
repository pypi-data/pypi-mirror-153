__all__ = ('IdIDXPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'


class _IdIDXCreateContract(Contract):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_date = serializers.DateField()
    passport_code = serializers.CharField(max_length=16)


class _IdIDXResponseContract(_IdIDXCreateContract):
    pass


class _IdIDXID(ID):
    _service = _SERVICE
    _app = 'id_idx'
    _view_set = 'id_idx'


class IdIDXPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = _IdIDXID()
    _create_contract = _IdIDXCreateContract
    _response_contract = _IdIDXResponseContract
