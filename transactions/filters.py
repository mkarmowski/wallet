import django_filters

from transactions.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'category': ['exact'],
            'wallet': ['exact'],
            'type': ['exact'],
            'date': ['gte', 'lte'],
            'amount': ['gte', 'lte'],
        }

    # @property
    # def qs(self):
    #     parent = super(TransactionFilter, self).qs
    #     return parent.filter(user=request.user)
