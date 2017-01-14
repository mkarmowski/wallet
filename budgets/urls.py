from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^budget/list/$', views.budgets_list, name='budgets_list'),
    url(r'^budget/details/(?P<id>\d+)/$', views.budget_details, name='budget_details'),
]
