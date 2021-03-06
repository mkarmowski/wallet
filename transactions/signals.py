from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from budgets.models import Budget

from .models import Transaction


@receiver(post_delete, sender=Transaction)
def delete_transaction(sender, instance, using, **kwargs):
    if instance.budget:
        budget = get_object_or_404(Budget, name=instance.budget)
        transactions = Transaction.objects.filter(
            Q(date__gte=budget.date_from)
            & Q(date__lte=budget.date_to)
            & Q(category=budget.category))

        completion = budget.budget_completion(transactions)
        budget.completion = completion
        if completion >= 100:
            budget.finished, budget.finishing = True, False
        elif completion >= 80:
            budget.finished, budget.finishing = False, True
        else:
            budget.finished, budget.finishing = False, False
        return budget.save()
