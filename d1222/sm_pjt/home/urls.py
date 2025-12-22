from django.urls import path, include
from . import views

app_name = ''
urlpatterns = [
    path('', views.index, name='index'),
    path('kakaomap/', views.kakaomap, name='kakaomap'),
    path('index2/', views.index2, name='index2'),
]
