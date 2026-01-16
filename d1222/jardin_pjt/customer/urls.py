from django.urls import path, include
from . import views

app_name = 'customer'
urlpatterns = [
    path('clist/', views.clist, name='clist'),
    # 리액트 - 게시판 리스트
    path('clistJson/', views.clistJson, name='clistJson'),
    path('cviewJson/', views.cviewJson, name='cviewJson'),
    path('cwriteJson/', views.cwriteJson, name='cwriteJson'),
    path('cdeleteJson/<int:bno>/', views.cdeleteJson, name='cdeleteJson'),
    path('cview/<int:bno>/', views.cview, name='cview'),
    path('cwrite/', views.cwrite, name='cwrite'),
    path('clikes/', views.clikes, name='clikes'),
]
