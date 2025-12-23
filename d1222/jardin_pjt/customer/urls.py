from django.urls import path, include
from . import views

app_name = 'customer'
urlpatterns = [
    path('notice/', views.notice, name='notice'),
]
