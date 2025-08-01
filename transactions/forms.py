from django import forms
from .models import TariffRule

class TariffRuleForm(forms.ModelForm):
    class Meta:
        model = TariffRule
        fields = '__all__'
