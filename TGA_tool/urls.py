from django.urls import path
from django.conf.urls import  url, include
from django.views.generic import TemplateView,ListView
from . import views
from .models import *

urlpatterns = [
    #path('home.html', views.home), Basculer vers les vues génériques 
    path('calendar.html', views.calendar),
    path('nouveau-eleve.html', views.nouveauEleve, name="nouveau eleve"),
    path('nouveau-parent.html', views.nouveauParent, name="nouveau parent"),
    path('modifier-seance_cours.html', views.seance_cours, name='modifier seance cours'),
    path('nouveau-coach.html', views.nouveauCoach, name="nouveau coach"),
    url(r'^home.html$',TemplateView.as_view(template_name="TGA_tool/home.html")),#Test des vues génériques
    path('nouvelle-matiere.html', views.matiere, name="nouvelle matiere"),
    path('nouveau-chapitre.html/<int:id>',views.chapitreNotions,name='chapitre notion')
]