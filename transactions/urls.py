from django.urls import path
from .views import transaction_list, add_tariff_rule, edit_tariff_rule, delete_tariff_rule, calculate_fee_api, \
    calculate_fees_batch_api

urlpatterns = [
    path('', transaction_list, name='transaction_list'),
    path('add/', add_tariff_rule, name='add_tariff_rule'),
    path('edit/<int:id>/', edit_tariff_rule, name='edit_tariff_rule'),
    path('delete/<int:id>/', delete_tariff_rule, name='delete_tariff_rule'),
path('api/calculate-fee/', calculate_fee_api, name='calculate_fee_api'),
    path('api/calculate-fees-batch/', calculate_fees_batch_api, name='calculate_fees_batch'),

]
