from django.urls import path
from . import views

urlpatterns = [
    path('home.html', views.home),
    path('contact/', views.contact, name='contact'),
]