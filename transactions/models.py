import django.utils.timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models

from budgets.models import Budget, Saving

TRANSACTION_CHOICES = (
    ('income', 'Income'),
    ('expense', 'Expense'),
)


class Wallet(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, related_name='wallets')
    description = models.TextField(blank=True, max_length=500)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:wallet_details', args=[self.id])


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    user = models.ForeignKey(User, related_name='categories')

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:category_details', args=[self.id])


class Transaction(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    type = models.CharField(choices=TRANSACTION_CHOICES, max_length=10)
    user = models.ForeignKey(User, related_name='transactions')
    wallet = models.ForeignKey(Wallet,
                               null=True,
                               blank=True,
                               related_name='transactions')
    category = models.ForeignKey(Category,
                                 related_name='transactions',
                                 null=True,
                                 blank=True)
    budget = models.ForeignKey(Budget,
                               blank=True,
                               null=True,
                               default=None)
    saving = models.ForeignKey(Saving,
                               blank=True,
                               null=True,
                               default=None)
    date = models.DateField(verbose_name='Date of transaction',
                            default=django.utils.timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=250, blank=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:transaction_details', args=[self.id])

    def wallet_balance_adjust(self, wallet, transaction):
        if transaction.type == 'expense':
            wallet.balance -= transaction.amount
            return wallet.save()
        else:
            wallet.balance += transaction.amount
            return wallet.save()
