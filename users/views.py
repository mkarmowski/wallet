import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from budgets.models import Budget, Saving
from transactions.models import Transaction, Wallet
from .forms import LoginForm, UserRegistrationForm

from chartit import DataPool, Chart


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'users/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'users/register.html',
                  {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Account is not active')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def chart(request):
    user= request.user
    ds = DataPool(
            series=
            [{'options': {
                'source': Wallet.objects.filter(user=user)},
                'terms': [
                    'name',
                    {'Wallet balance': 'balance'}]},
            {'options': {
                'source': Saving.objects.filter(user=user, finished=False)},
                'terms': [
                    {'saving_name': 'name'},
                    {'Saving amount': 'current_amount'}]},
            ])

    cht = Chart(
        datasource=ds,
        series_options=
        [{'options': {
            'type': 'column',
            'stacking': False},
            'terms': {
                'name': [
                    'Wallet balance', ],
                'saving_name':[
                    'Saving amount'
                ]
            }}],
        chart_options={
            'chart':{
                'backgroundColor': "#f7f7f7"},
            'title':{
                'text': 'Wallet balance and savings amount'},
            'xAxis':{
                'title':{
                    'text': 'Name'}},
            'yAxis':{
                'title': {
                    'text': 'Amount'}}
        })
    return cht


@login_required
def main_view(request):
    current_user = request.user
    transactions = Transaction.objects.filter(user=current_user)
    budget_list = Budget.objects.filter(Q(user=current_user)
                                        & Q(date_to__gte=datetime.datetime.now())
                                        & Q(date_from__lte=datetime.datetime.now()))
    budgets_running = budget_list.filter(finished=False)
    budgets_finishing = budget_list.filter(finishing=True)
    budgets_finished = budget_list.filter(finished=True)
    savings_list = Saving.objects.filter(user=current_user, finished=False)

    walletchart = chart(request)

    return render(request, 'users/main.html', {'transactions': transactions,
                                               'budgets': budget_list,
                                               'budgets_running': budgets_running,
                                               'budgets_finishing': budgets_finishing,
                                               'budgets_finished': budgets_finished,
                                               'savings_list': savings_list,
                                               'chart': walletchart})
