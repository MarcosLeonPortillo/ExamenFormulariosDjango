from django.urls import path

from ptpud03 import views

urlpatterns = [
    path('', views.index, name='index')
]
