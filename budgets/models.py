import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Budget(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # amount budget is set for
    user = models.ForeignKey(User, related_name='budgets')
    wallet = models.ForeignKey('transactions.Wallet', on_delete=models.DO_NOTHING)
    category = models.ForeignKey('transactions.Category', on_delete=models.DO_NOTHING)
    date_from = models.DateField(default=django.utils.timezone.now(),)
    date_to = models.DateField(default=django.utils.timezone.now())
    finishing = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    completion = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
            if transaction.type == 'expense':
                amount_used += transaction.amount
            else:
                amount_used -= transaction.amount
        budget_used = (amount_used / amount_set) * 100  # budget use in percent
        return budget_used


class Saving(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    goal = models.DecimalField(max_digits=10, decimal_places=2)  # saving amount
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, related_name='savings')
    date_from = models.DateField()
    finished = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('budgets:saving_details', args=[self.id])

    def saving_completion(self):
        completion = (self.current_amount / self.goal) * 100
        return completion
