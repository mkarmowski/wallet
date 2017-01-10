import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

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
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:wallet_details', args=[self.id])


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:categories_list', args=[self.slug])


class Transaction(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    type = models.CharField(choices=TRANSACTION_CHOICES, max_length=10)
    user = models.ForeignKey(User, related_name='transactions')
    wallet = models.ForeignKey(Wallet, null=True, blank=True)
    category = models.ForeignKey(Category,
                                 related_name='transactions',
                                 null=True,
                                 blank=True)
    date = models.DateTimeField(verbose_name='Date of transaction',
                                default=datetime.datetime.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(max_length=250)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Transaction, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('wallet:transaction_details', args=[self.id])
