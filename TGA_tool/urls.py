from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil,name='acceuil'),
    path('parent/', views.parent, name='parent'),
]