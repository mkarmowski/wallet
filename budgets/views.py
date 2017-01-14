from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from transactions.models import Transaction
from .models import Budget


@login_required
def budgets_list(request):
    current_user = request.user
    budgets = Budget.objects.filter(user=current_user)
    return render(request, 'budgets/list.html', {'budgets': budgets})


@login_required
def budget_details(request, id):
    # user = request.user
    budget = get_object_or_404(Budget, id=id)
    # transactions = Transaction.objects.filter(budget=budget)
    return render(request, 'budgets/details.html', {'budget': budget})
