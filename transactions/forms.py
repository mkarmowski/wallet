from django import forms

from .models import Category, Transaction, Wallet


RECURRING_CHOICES = (
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
)


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
        self.fields['wallet'] = forms.ModelChoiceField(queryset=Wallet.objects.filter(user=user))
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(user=user))


class TransactionNextMonth(forms.Form):
    month = forms.IntegerField(widget=forms.HiddenInput)


class TransactionPrevMonth(forms.Form):
    month = forms.IntegerField(widget=forms.HiddenInput)


class RecurringTransactionForm(forms.Form):
    frequency = forms.ChoiceField(choices=RECURRING_CHOICES, required=True)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=False)
