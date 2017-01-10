from django import forms
from .models import Wallet, Transaction


class WalletCreateForm(forms.ModelForm):
    field_order = ['name', 'balance', 'description']

    class Meta:
        model = Wallet
        fields = ('description', 'balance', 'name',)


class TransactionCreateForm(forms.ModelForm):
    field_order = ['name', 'type', 'wallet', 'category', 'date', 'amount', 'notes', ]

    class Meta:
        model = Transaction
        fields = ('name', 'type', 'wallet', 'category', 'date', 'amount', 'notes',)

    def __init__(self, user, *args, **kwargs):
        super(TransactionCreateForm, self).__init__(*args, **kwargs)
        self.fields['wallet'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in Wallet.objects.filter(user=user)])


