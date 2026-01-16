from django.urls import path, include
from . import views

app_name = 'member'
urlpatterns = [
    path('userAll/', views.userAll, name='userAll'),
    path('userInsert/', views.userInsert, name='userInsert'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('step03/', views.step03, name='step03'),
    path('idCheck/', views.idCheck, name='idCheck'),
]
