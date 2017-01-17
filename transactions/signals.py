from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Transaction
from budgets.models import Budget


@receiver(post_delete, sender=Transaction)
def delete_transaction(sender, instance, using, **kwargs):
    budget = get_object_or_404(Budget, id=5)
    transactions = Transaction.objects.filter(
        Q(date__gte=budget.date_from)
        & Q(date__lte=budget.date_to)
        & Q(category=budget.category))
    if budget.budget_completion(transactions) >= 100:
        budget.finished, budget.finishing = True, False
        return budget.save()
    elif budget.budget_completion(transactions) >= 80:
        budget.finished, budget.finishing = False, True
        return budget.save()
    else:
        budget.finished, budget.finishing = False, False
        return budget.save()
