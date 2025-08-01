from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import TariffRuleForm
from .models import TariffRule
from decimal import Decimal
from .utils import calculate_fee
import json


def transaction_list(request):
    transactions = TariffRule.objects.all()
    return render(request, 'transactions/list.html', {'transactions': transactions})

def add_tariff_rule(request):
    if request.method == 'POST':
        form = TariffRuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TariffRuleForm()
    return render(request, 'transactions/add.html', {'form': form})

def edit_tariff_rule(request, id):
    rule = get_object_or_404(TariffRule, id=id)
    if request.method == 'POST':
        form = TariffRuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TariffRuleForm(instance=rule)
    return render(request, 'transactions/edit.html', {'form': form, 'rule': rule})

def delete_tariff_rule(request, id):
    rule = get_object_or_404(TariffRule, id=id)
    if request.method == 'POST':
        rule.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/delete.html', {'rule': rule})

@csrf_exempt
def calculate_fee_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = calculate_fee(data)
            amount = Decimal(data.get("amount", 0))
            fee = Decimal(result.get("fee", 0))
            total = amount + fee
            result["total_amount"] = str(round(total, 2))

            return JsonResponse(result, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
@csrf_exempt
def calculate_fees_batch_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transactions = data.get("transactions", [])
            results = []

            for tx in transactions:
                if 'amount' not in tx or 'transaction_type' not in tx:
                    results.append({
                        "error": "Missing required fields: 'amount' and 'transaction_type'",
                        "transaction": tx
                    })
                    continue

                result = calculate_fee(tx)
                amount = Decimal(str(tx.get('amount', '0')))
                fee = Decimal(str(result.get("fee", '0')))
                total = amount + fee
                result["total_amount"] = str(round(total, 2))
                result["original_amount"] = str(amount)
                results.append(result)

            return JsonResponse({"results": results}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
