from django.urls import path, include
from . import views

app_name = 'student'
urlpatterns = [
    path('write/', views.write, name='write'),
    path('list/', views.list, name='list'),
    path('<int:sno><str:name>/view/', views.view, name='view'),   # 앱방식, restful - <int:sno><str:name>를 /view/뒤에 붙여도 됨
    # path('view/', views.view, name='view'),
    path('delete/', views.delete, name='delete'),
]
