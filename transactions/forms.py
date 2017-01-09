from django import forms
from .models import Wallet, Transaction


class WalletCreateForm(forms.ModelForm):
    field_order = ['name', 'balance', 'description']

    class Meta:
        model = Wallet
        fields = ('description', 'balance', 'name',)
