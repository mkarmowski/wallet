from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class Wallet(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    wallet = models.ForeignKey(Wallet, null=True, blank=True)
    category = models.ForeignKey(Category,
                                 related_name='transactions',
                                 null=True,
                                 blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(max_length=250)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:transaction', args=[self.id, self.slug])
