from django.urls import path
from . import views

urlpatterns = [
    path('home.html', views.home),
    path('nouveau-eleve.html', views.nouveauEleve, name="nouveau eleve"),
    path('nouveau-parent.html', views.nouveauParent, name="nouveau parent"),
    path('nouveau-coach.html', views.nouveauCoach, name="nouveau coach"),
]