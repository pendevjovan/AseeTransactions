from django.db import models

class TariffRule(models.Model):
    TRANSACTION_TYPES = [
        ('POS', 'POS'),
        ('ECOM', 'ECOM'),
        ('TRANSFER', 'TRANSFER'),
        ('CASHOUT', 'CASHOUT'),
        ('INTL', 'INTL'),
    ]

    name = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    fixed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percentage_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    max_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_for_credit_score_above = models.IntegerField(null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    currency = models.CharField(max_length=5, null=True, blank=True,)
    applies_to_international = models.BooleanField(default=False,)

    def __str__(self):
        return f"{self.name} ({self.transaction_type})"
