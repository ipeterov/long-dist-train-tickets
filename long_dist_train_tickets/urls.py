"""long_dist_train_tickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from core.views import all_stations, list_tickets, create_ticket, confirm_purchase, confirm_boarding, confirm_arrival


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^all_stations', all_stations, name='all_stations'),
    url(r'^list_tickets', list_tickets, name='list_tickets'),
    url(r'^create_ticket', create_ticket, name='create_ticket'),
    url(r'^confirm_purchase', confirm_purchase, name='confirm_purchase'),
    url(r'^confirm_boarding', confirm_boarding, name='confirm_boarding'),
    url(r'^confirm_arrival', confirm_arrival, name='confirm_arrival'),
]
