__all__ = ('TransferPoint',)

from expressmoney.api import *

SERVICE = 'transfers'
APP = 'operations'


class TransferCreateContract(Contract):
    RUB = 'RUB'
    USD = 'USD'
    AMOUNT_CURRENCY_CHOICES = (
        (RUB, RUB),
        (USD, USD),
    )
    withdraw_wallet_id = serializers.IntegerField(min_value=1)
    deposit_wallet_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    amount_currency = serializers.ChoiceField(choices=AMOUNT_CURRENCY_CHOICES)


class TransferReadContract(Contract):
    withdraw_wallet_id = serializers.IntegerField(min_value=1)
    deposit_wallet_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class TransferID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'transfer'


class TransferPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = TransferID()
    _create_contract = TransferCreateContract
    _read_contract = TransferReadContract
