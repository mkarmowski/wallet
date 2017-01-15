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
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_from', 'date_to', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('budgets:budget_details', args=[self.id])
