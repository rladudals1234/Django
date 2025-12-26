from django.urls import path, include
from . import views

app_name = 'comment'
urlpatterns = [
    path('colist/', views.colist, name='colist'),
    path('cowrite/', views.cowrite, name='cowrite'),
    path('codelete/', views.codelete, name='codelete'),
    path('coupdate/', views.coupdate, name='coupdate'),
]
