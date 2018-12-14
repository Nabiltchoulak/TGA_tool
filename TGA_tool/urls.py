from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil,name='acceuil'),
    path('cours/', views.cours, name='cours'),
]