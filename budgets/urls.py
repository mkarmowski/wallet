from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^budget/list/$', views.budgets_list, name='budgets_list'),
    url(r'^budget/details/(?P<id>\d+)/$', views.budget_details, name='budget_details'),
    url(r'^budget/create/$', views.budget_create, name='budget_create'),
    url(r'^budget/delete/(?P<pk>\d+)/$', views.BudgetDelete.as_view(), name='budget_delete'),
    url(r'^budget/update/(?P<pk>\d+)/$', views.BudgetUpdate.as_view(), name='budget_update'),
]
