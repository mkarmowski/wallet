from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^transaction/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.transaction_detail, name='transaction_detail'),
]
