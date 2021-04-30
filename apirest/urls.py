## Este archivo creo que no se está usando

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
