from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^transactions/', include('transactions.urls', namespace='wallet')),
    url(r'^budgets/', include('budgets.urls', namespace='budgets')),
    url(r'^users/', include('users.urls')),
    url(r'^$', TemplateView.as_view(template_name='users/index.html')),
]
