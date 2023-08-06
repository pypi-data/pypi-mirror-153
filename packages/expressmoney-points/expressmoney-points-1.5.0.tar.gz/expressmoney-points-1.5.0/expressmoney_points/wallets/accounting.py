__all__ = ('CommissionDebitPoint', 'WalletDebitPoint', 'WalletCreditPoint')

from expressmoney.api import *

SERVICE = 'wallets'
APP = 'accounting'


class CommissionDebitReadContract(Contract):
    created = serializers.DateTimeField()
    wallet = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    balance = serializers.DecimalField(max_digits=16, decimal_places=0)


class WalletDebitReadContract(CommissionDebitReadContract):
    pass


class WalletCreditReadContract(CommissionDebitReadContract):
    pass


class CommissionDebitID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'commission_debit'


class WalletDebitID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet_debit'


class WalletCreditID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'wallet_credit'


class CommissionDebitPoint(ListPointMixin, ContractPoint):
    _point_id = CommissionDebitID()
    _read_contract = CommissionDebitReadContract
    _sort_by = 'created'


class WalletDebitPoint(ListPointMixin, ContractPoint):
    _point_id = WalletDebitID()
    _read_contract = WalletDebitReadContract
    _sort_by = 'created'


class WalletCreditPoint(ListPointMixin, ContractPoint):
    _point_id = WalletCreditID()
    _read_contract = WalletCreditReadContract
    _sort_by = 'created'
