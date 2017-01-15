from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from budgets.forms import BudgetCreateForm
from .models import Budget


@login_required
def budgets_list(request):
    current_user = request.user
    budgets = Budget.objects.filter(user=current_user)
    return render(request, 'budgets/list.html', {'budgets': budgets})


@login_required
def budget_details(request, id):
    budget = get_object_or_404(Budget, id=id)
    # transactions = Transaction.objects.filter(budget=budget)
    return render(request, 'budgets/details.html', {'budget': budget})


@login_required
def budget_create(request):
    current_user = request.user
    if request.method == 'POST':
        budget_create_form = BudgetCreateForm(current_user, request.POST)
        if budget_create_form.is_valid():
            new_budget = budget_create_form.save(commit=False)
            new_budget.user = request.user
            new_budget.save()
            messages.success(request, 'Budget created')
            return render(request, 'budgets/done.html')
    else:

        budget_create_form = BudgetCreateForm(current_user)
    return render(request, 'budgets/create.html',
                  {'budget_form': budget_create_form})


class BudgetDelete(DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budgets:budgets_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BudgetDelete, self).dispatch(*args, **kwargs)


class BudgetUpdate(UpdateView):
    model = Budget
    fields = ['name', 'amount', 'wallet', 'category', 'date_from', 'date_to']
    template_name = 'budgets/update.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BudgetUpdate, self).dispatch(*args, **kwargs)
