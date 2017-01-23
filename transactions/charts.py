from chartit import Chart
from chartit import DataPool

from budgets.models import Saving
from transactions.models import Wallet


def dashboard_chart(request):
    user = request.user
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
                    {'Saving amount': 'current_amount'}]}
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
