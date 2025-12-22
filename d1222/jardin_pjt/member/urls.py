from django.urls import path, include
from . import views

app_name = 'member'
urlpatterns = [
    path('step03/', views.step03, name='step03'),
    path('idCheck/', views.idCheck, name='idCheck'),
]
