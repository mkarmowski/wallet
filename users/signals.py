from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.utils import DatabaseError, OperationalError
from django.dispatch import receiver

from transactions.models import Category, Wallet


@receiver(post_save, sender=User)
def basic_setup(sender, instance, **kwargs):
    """
    Creates default categories, and default Wallet
    after creating User account
    """
    names = ['Clothes', 'Food', 'Entertainment', 'Salary',
             'Savings', 'Transportation', 'Bills', 'Health', 'Others']
    try:
        if Wallet.objects.filter(user=instance).exists() is False:
            Wallet.objects.create(name='Default Wallet',
                                  user=instance,
                                  balance=0)
        for name in names:
            if Category.objects.filter(name=name, user=instance).exists() is False:
                Category.objects.create(name=name, user=instance)

    except (DatabaseError, OperationalError):
        pass
