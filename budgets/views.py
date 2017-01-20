from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from transactions.models import Transaction, Category, Wallet
from .forms import BudgetCreateForm, SavingCreateForm
from .models import Budget, Saving


@login_required
def budgets_list(request):
    current_user = request.user
    budgets = Budget.objects.filter(user=current_user)
    return render(request, 'budgets/list.html', {'budgets': budgets})


@login_required
def budget_details(request, id):
    budget = get_object_or_404(Budget, id=id)
    transactions = Transaction.objects.filter(
        Q(date__gte=budget.date_from) & Q(date__lte=budget.date_to) & Q(category=budget.category))
    budget_used = Budget.budget_completion(budget, transactions)
    return render(request, 'budgets/details.html', {'budget': budget,
                                                    'budget_used': budget_used,
                                                    'transactions': transactions})


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


@login_required
def savings_list(request):
    current_user = request.user
    savings = Saving.objects.filter(user=current_user)
    return render(request, 'savings/list.html', {'savings': savings})


@login_required
def saving_details(request, id):
    saving = get_object_or_404(Saving, id=id)
    transactions = Transaction.objects.filter(saving=saving)
    completion = saving.saving_completion()
    return render(request, 'savings/details.html', {'saving': saving,
                                                    'transactions': transactions,
                                                    'completion': completion})


@login_required
def saving_create(request):
    current_user = request.user
    if request.method == 'POST':
        saving_create_form = SavingCreateForm(request.POST)
        if saving_create_form.is_valid():
            new_saving = saving_create_form.save(commit=False)
            new_saving.user = request.user
            new_saving.save()
            messages.success(request, 'Saving created')
            return render(request, 'savings/done.html')
    else:

        saving_create_form = SavingCreateForm()
    return render(request, 'savings/create.html',
                  {'saving_form': saving_create_form})


class SavingDelete(DeleteView):
    model = Saving
    template_name = 'savings/saving_confirm_delete.html'
    success_url = reverse_lazy('budgets:savings_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SavingDelete, self).dispatch(*args, **kwargs)


class SavingUpdate(UpdateView):
    model = Saving
    fields = ['name', 'goal', 'date_from']
    template_name = 'savings/update.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SavingUpdate, self).dispatch(*args, **kwargs)
