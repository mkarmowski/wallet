import django.utils.timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from transactions.models import Transaction, Category, Wallet
from .forms import BudgetCreateForm, SavingCreateForm, SavingDepositForm
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
            try:
                categories = Category.objects.get(name='Savings')
            except ObjectDoesNotExist:
                saving_category = Category(name='Savings', user=current_user)
                saving_category.save()
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


def saving_deposit(request, pk):
    current_user = request.user
    if request.method == 'POST':
        saving_deposit_form = SavingDepositForm(current_user, request.POST)
        if saving_deposit_form.is_valid():
            cd = saving_deposit_form.cleaned_data
            saving = get_object_or_404(Saving, id=pk)
            wallet = get_object_or_404(Wallet, name=cd['wallet'])
            category = get_object_or_404(Category, name='Savings')

            wallet.balance -= cd['amount']
            transaction = Transaction(name='Saving deposit to: {}'.format(saving),
                                      type='expense',
                                      user=current_user,
                                      wallet=wallet,
                                      category=category,
                                      budget=None,
                                      saving=saving,
                                      date=django.utils.timezone.now(),
                                      amount=cd['amount'])
            saving.current_amount += cd['amount']  # adjust saving amount
            saving.save(), wallet.save(), transaction.save()
            messages.success(request, 'Deposit done')
            return redirect(saving)
    else:
        saving_deposit_form = SavingDepositForm(current_user)
    return render(request, 'savings/deposit.html',
                  {'deposit_form': saving_deposit_form})


def saving_withdraw(request, pk):
    current_user = request.user
    if request.method == 'POST':
        saving_withdraw_form = SavingDepositForm(current_user, request.POST)
        if saving_withdraw_form.is_valid():
            cd = saving_withdraw_form.cleaned_data
            saving = get_object_or_404(Saving, id=pk)
            wallet = get_object_or_404(Wallet, name=cd['wallet'])
            category = get_object_or_404(Category, name='Savings')

            wallet.balance += cd['amount']
            transaction = Transaction(name='Saving withdraw from: {}'.format(saving),
                                      type='income',
                                      user=current_user,
                                      wallet=wallet,
                                      category=category,
                                      budget=None,
                                      saving=saving,
                                      date=django.utils.timezone.now(),
                                      amount=cd['amount'])
            saving.current_amount -= cd['amount']  # adjust saving amount
            saving.save(), wallet.save(), transaction.save()
            messages.success(request, 'Withdraw done')
            return redirect(saving)
    else:
        saving_deposit_form = SavingDepositForm(current_user)
    return render(request, 'savings/withdraw.html',
                  {'withdraw_form': saving_deposit_form})
