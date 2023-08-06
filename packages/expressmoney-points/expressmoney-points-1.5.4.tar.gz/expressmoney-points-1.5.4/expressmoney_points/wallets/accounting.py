__all__ = ('WalletCommissionDebitPoint', 'WalletDebitPoint', 'WalletCreditPoint')

from expressmoney.api import *

SERVICE = 'wallets'
APP = 'accounting'


class WalletCommissionDebitReadContract(Contract):
    TO_WALLET_FROM_BANK_CARD = 'TO_WALLET_FROM_BANK_CARD'
    FROM_WALLTET_TO_BANK_CARD = 'FROM_WALLET_TO_BANK_CARD'
    FROM_WALLET_TO_CORRESPONDENT_ACCOUNT = 'FROM_WALLET_TO_CORRESPONDENT_ACCOUNT'
    TO_WALLTET_FROM_CORRESPONDENT_ACCOUNT = 'TO_WALLTET_FROM_CORRESPONDENT_ACCOUNT'
    COMMISSION = 'COMMISSION'
    NAME_CHOICES = (
        (TO_WALLET_FROM_BANK_CARD, TO_WALLET_FROM_BANK_CARD),
        (FROM_WALLTET_TO_BANK_CARD, FROM_WALLTET_TO_BANK_CARD),
        (FROM_WALLET_TO_CORRESPONDENT_ACCOUNT, FROM_WALLET_TO_CORRESPONDENT_ACCOUNT),
        (TO_WALLTET_FROM_CORRESPONDENT_ACCOUNT, TO_WALLTET_FROM_CORRESPONDENT_ACCOUNT),
        (COMMISSION, COMMISSION),
    )
    created = serializers.DateTimeField()
    operation_name = serializers.ChoiceField(choices=NAME_CHOICES)
    wallet = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    balance = serializers.DecimalField(max_digits=16, decimal_places=0)


class WalletDebitReadContract(WalletCommissionDebitReadContract):
    pass


class WalletCreditReadContract(WalletCommissionDebitReadContract):
    pass


class WalletCommissionDebitID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet_commission_debit'


class WalletDebitID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet_debit'


class WalletCreditID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet_credit'


class WalletCommissionDebitPoint(ListPointMixin, ContractPoint):
    _point_id = WalletCommissionDebitID()
    _read_contract = WalletCommissionDebitReadContract
    _sort_by = 'created'


class WalletDebitPoint(ListPointMixin, ContractPoint):
    _point_id = WalletDebitID()
    _read_contract = WalletDebitReadContract
    _sort_by = 'created'


class WalletCreditPoint(ListPointMixin, ContractPoint):
    _point_id = WalletCreditID()
    _read_contract = WalletCreditReadContract
    _sort_by = 'created'
