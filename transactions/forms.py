from django import forms
from django.contrib.auth.models import User

from .models import Wallet, Transaction, Category


class WalletCreateForm(forms.ModelForm):
    field_order = ['name', 'balance', 'description']

    class Meta:
        model = Wallet
        fields = ('description', 'balance', 'name',)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', )


class TransactionCreateForm(forms.ModelForm):
    field_order = ['name', 'type', 'wallet', 'category', 'date', 'amount', 'notes', ]

    class Meta:
        model = Transaction
        fields = ('name', 'type', 'wallet', 'category', 'date', 'amount', 'notes',)

    def __init__(self, user, *args, **kwargs):
        super(TransactionCreateForm, self).__init__(*args, **kwargs)
        self.fields['wallet'] = forms.ChoiceField(
            choices=[(wallet.id, str(wallet)) for wallet in Wallet.objects.filter(user=user)])



