import django_filters

from transactions.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'category': ['exact'],
            'wallet': ['exact'],
            'date': ['month__gte', 'month__lte']
        }
