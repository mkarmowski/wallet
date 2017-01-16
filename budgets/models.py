import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from transactions.models import Wallet, Category


class Budget(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, related_name='budgets')
    wallet = models.ForeignKey(Wallet)
    category = models.ForeignKey(Category)
    date_from = models.DateField(default=django.utils.timezone.now())
    date_to = models.DateField(default=django.utils.timezone.now())
    finishing = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date_from', 'date_to', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('budgets:budget_details', args=[self.id])

    def budget_completion(self, queryset):
        amount_set = self.amount
        amount_used = 0
        for transaction in queryset:
            amount_used += transaction.amount
        budget_used = (amount_used / amount_set) * 100  # budget use in percent
        return budget_used
