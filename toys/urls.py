from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.toy_list, name='toy_list'),
    path('toy/<slug:slug>/', views.toy_detail, name='toy_detail'),

    path('register/', views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('my-collection/', views.my_collection, name='my_collection'),
    path('toy/<slug:slug>/add/', views.add_to_collection, name='add_to_collection'),
    path('collection/remove/<int:item_id>/', views.remove_from_collection, name='remove_from_collection'),
]