from .models import TariffRule
from decimal import Decimal
from django.db import models

def calculate_fee(transaction_data):
    amount = Decimal(transaction_data['amount'])
    transaction_type = transaction_data['transaction_type']
    client = transaction_data.get('client', {})
    credit_score = client.get('credit_score', 0)
    is_international = client.get('is_international', False)
    currency = transaction_data.get('currency')

    rules = TariffRule.objects.filter(
        transaction_type=transaction_type,
        is_active=True,
        min_amount__lte=amount,
        max_amount__gte=amount
    )
    rule = rules.first()

    fee = rule.fixed_fee + (amount * (rule.percentage_fee / 100))

    if rule.max_fee and fee > rule.max_fee:
        fee = rule.max_fee

    if rule.discount_for_credit_score_above and credit_score > rule.discount_for_credit_score_above:
        discount = fee * (rule.discount_percent / 100)
        fee -= discount

    return {
        'fee': str(round(fee, 2)),
        'applied_rule': rule.name,
        'note': f"Rule '{rule.name}' applied"
    }
