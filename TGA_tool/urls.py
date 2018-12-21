from django.urls import path
from . import views

urlpatterns = [
    path('home.html', views.home),
    path('calendar.html', views.calendar),
    path('nouveau-eleve.html', views.nouveauEleve, name="nouveau eleve"),
    path('nouveau-parent.html', views.nouveauParent, name="nouveau parent"),
    path('modifier-seance_cours.html', views.seance_cours, name='modifier seance cours'),
    path('nouveau-coach.html', views.nouveauCoach, name="nouveau coach"),

]