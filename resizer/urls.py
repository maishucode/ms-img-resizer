from django.urls import path

from . import views

app_name = 'resizer'

urlpatterns = [
    path('', views.home, name='home'),
]