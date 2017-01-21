from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^budget/list/$', views.budgets_list, name='budgets_list'),
    url(r'^budget/details/(?P<id>\d+)/$', views.budget_details, name='budget_details'),
    url(r'^budget/create/$', views.budget_create, name='budget_create'),
    url(r'^budget/delete/(?P<pk>\d+)/$', views.BudgetDelete.as_view(), name='budget_delete'),
    url(r'^budget/update/(?P<pk>\d+)/$', views.BudgetUpdate.as_view(), name='budget_update'),
    url(r'^savings/list/$', views.savings_list, name='savings_list'),
    url(r'^savings/details/(?P<id>\d+)/$', views.saving_details, name='saving_details'),
    url(r'^savings/create/$', views.saving_create, name='saving_create'),
    url(r'^savings/delete/(?P<pk>\d+)/$', views.SavingDelete.as_view(), name='saving_delete'),
    url(r'^savings/update/(?P<pk>\d+)/$', views.SavingUpdate.as_view(), name='saving_update'),
    url(r'^savings/deposit/(?P<pk>\d+)/$', views.saving_deposit, name='saving_deposit'),
    url(r'^savings/withdraw/(?P<pk>\d+)/$', views.saving_withdraw, name='saving_withdraw'),
]
