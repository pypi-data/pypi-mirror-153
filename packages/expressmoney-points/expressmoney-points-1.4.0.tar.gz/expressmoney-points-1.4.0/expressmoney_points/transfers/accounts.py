__all__ = ('CorrespondentAccountPoint', 'CorrespondentAccountObjectPoint')

from expressmoney.api import *

SERVICE = 'transfers'
APP = 'accounts'


class CorrespondentAccountDescriptionReadContract(Contract):
    RUB = 'RUB'
    USD = 'USD'
    CURRENCY_CODE_CHOICES = (
        (RUB, RUB),
        (USD, USD),
    )
    currency_code = serializers.ChoiceField(choices=CURRENCY_CODE_CHOICES)


class TrustLevelReadContract(Contract):
    LEVEL_0 = 'LEVEL_0'
    LEVEL_1 = 'LEVEL_1'
    LEVEL_2 = 'LEVEL_2'
    LEVEL_3 = 'LEVEL_3'
    LEVEL_4 = 'LEVEL_4'
    LEVEL_5 = 'LEVEL_5'
    NAME_CHOICES = (
        (LEVEL_0, LEVEL_0),
        (LEVEL_1, LEVEL_1),
        (LEVEL_2, LEVEL_2),
        (LEVEL_3, LEVEL_3),
        (LEVEL_4, LEVEL_4),
        (LEVEL_5, LEVEL_5),
    )
    name = serializers.ChoiceField(choices=NAME_CHOICES)
    currency_code = serializers.ChoiceField(choices=CorrespondentAccountDescriptionReadContract.CURRENCY_CODE_CHOICES)
    amount_min = serializers.DecimalField(max_digits=16, decimal_places=0)
    amount_max = serializers.DecimalField(max_digits=16, decimal_places=0)


class CorrespondentAccountReadContract(Contract):
    id = serializers.IntegerField(min_value=1)
    is_active = serializers.BooleanField()
    user_id = serializers.IntegerField(min_value=1)
    description = CorrespondentAccountDescriptionReadContract()
    trust_level = TrustLevelReadContract()
    balance = serializers.DecimalField(max_digits=16, decimal_places=0)


class CorrespondentAccountID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'correspondent_account'


class CorrespondentAccountPoint(ListPointMixin, ContractPoint):
    _point_id = CorrespondentAccountID()
    _read_contract = CorrespondentAccountReadContract


class CorrespondentAccountObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = CorrespondentAccountID()
    _read_contract = CorrespondentAccountReadContract
