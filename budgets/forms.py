from django import forms
from django.contrib.auth.models import User

from .models import Budget, Saving
from transactions.models import Category, Wallet


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

    # def __init__(self, user, *args, **kwargs):
    #     super(SavingCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.filter(user=user))
