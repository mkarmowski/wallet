from django import forms

from transactions.models import Category, Wallet

from .models import Budget, Saving


class BudgetCreateForm(forms.ModelForm):
    field_order = ['name', 'wallet', 'category', 'amount', 'date_from', 'date_to']

    class Meta:
        model = Budget
        fields = ['name', 'amount', 'wallet', 'category', 'date_from', 'date_to']

    def __init__(self, user, *args, **kwargs):
        super(BudgetCreateForm, self).__init__(*args, **kwargs)
        self.fields['wallet'] = forms.ModelChoiceField(queryset=Wallet.objects.filter(user=user))
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(user=user))


class SavingCreateForm(forms.ModelForm):
    field_order = ['name', 'goal', 'current_amount', 'date_from']

    class Meta:
        model = Saving
        fields = ['name', 'goal', 'current_amount', 'date_from']


class SavingDepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    wallet = forms.ModelChoiceField(Wallet)

    def __init__(self, user, *args, **kwargs):
        super(SavingDepositForm, self).__init__(*args, **kwargs)
        self.fields['wallet'] = forms.ModelChoiceField(queryset=Wallet.objects.filter(user=user))
