from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.toy_list, name='toy_list'),
    path('toy/<slug:slug>/', views.toy_detail, name='toy_detail'),
]