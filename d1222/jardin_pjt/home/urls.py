from django.urls import path, include
from . import views

app_name = ''
urlpatterns = [
    path('', views.index, name='index'),
    path('chart1/', views.chart1, name='chart1'),
    path('chart2/', views.chart2, name='chart2'),
    path('chart_json/', views.chart_json, name='chart_json'),
    path('chart_json2/', views.chart_json2, name='chart_json2'),
]
