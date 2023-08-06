__all__ = ('WalletPoint', 'WalletObjectPoint', 'WalletInfoRequestPoint', 'FindWalletPoint')

from expressmoney.api import *
from phonenumber_field.serializerfields import PhoneNumberField

SERVICE = 'wallets'
APP = 'wallets'


class WalletCreateContract(Contract):
    RUB = 'RUB'
    USD = 'USD'
    CURRENCY_CODE_CHOICES = (
        (RUB, RUB),
        (USD, USD),
    )
    currency_code = serializers.ChoiceField(choices=CURRENCY_CODE_CHOICES)


class WalletReadContract(WalletCreateContract):
    id = serializers.IntegerField(min_value=1)
    is_active = serializers.BooleanField()
    user_id = serializers.IntegerField(min_value=1)
    balance = serializers.DecimalField(max_digits=16, decimal_places=0)


class WalletInfoRequestCreateContract(Contract):
    wallet_id = serializers.IntegerField(min_value=1)


class WalletInfoResponseRetrieveContract(WalletInfoRequestCreateContract):
    wallet_is_active = serializers.BooleanField()
    wallet_user_id = serializers.IntegerField(min_value=1)
    wallet_currency_code = serializers.ChoiceField(choices=WalletCreateContract.CURRENCY_CODE_CHOICES)


class FindWalletCreateContract(Contract):
    username = PhoneNumberField()
    currency_code = serializers.ChoiceField(choices=WalletCreateContract.CURRENCY_CODE_CHOICES)


class FindWalletResponseContract(Contract):
    wallet_id = serializers.IntegerField(min_value=1)


class WalletID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet'


class WalletInfoRequestID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet_info_request'


class FindWalletID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'find_wallet'


class WalletPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = WalletID()
    _create_contract = WalletCreateContract
    _read_contract = WalletReadContract


class WalletObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = WalletID()
    _read_contract = WalletReadContract


class WalletInfoRequestPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = WalletInfoRequestID()
    _create_contract = WalletInfoRequestCreateContract
    _response_contract = WalletInfoResponseRetrieveContract


class FindWalletPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = FindWalletID()
    _create_contract = FindWalletCreateContract
    _response_contract = FindWalletResponseContract
