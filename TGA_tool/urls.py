from django.urls import path
from django.conf.urls import  url, include
from django.views.generic import TemplateView,ListView
from . import views
from .models import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('home.html', views.home), Basculer vers les vues génériques 
    path('calendar.html', views.calendar),
    url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
    #url(r'^connexion$', auth_views.LoginView.as_view()),
    path('nouveau-eleve.html/<int:id>', views.nouveauEleve, name="nouveau eleve"),
    path('nouveau-parent.html/<int:id>', views.nouveauParent, name="nouveau parent"),
    path('nouveau-coach.html', views.nouveauCoach, name="nouveau coach"),
    path('nouvelle-famille.html', views.nouvelleFamille, name="nouvelle famille"),
    
    path('modifier-seance_cours.html', views.seance_cours, name='modifier seance cours'),

    url(r'^home.html$',TemplateView.as_view(template_name="TGA_tool/home.html")),#Test des vues génériques
    path('nouvelle-matiere.html', views.matiere, name="nouvelle matiere"),
    path('nouveau-chapitre.html/<int:id>',views.chapitreNotions,name='chapitre notion'),
    path('nouveau-cours.html', views.nouveauCours, name="nouveau cours"),
    path('eleve-arrive.html', views.eleveArrive, name="eleve arrive"),

    # Les urls du profile du coach
    path('mes-cours.html',views.mesCours,name='mes cours'), # id du coach
    url(r'^mes-seances.html/$',views.mesSeances, name= 'mes seances'), #id du coach
    path('displayseance.html/<int:id>',views.displaySeance,name='display seance'),
    path('annulerseance.html/<int:id>',views.annulerSeance,name='annuler seance'),
    path('edit-seance.html/<int:id>',views.modifierSeance,name='edit seance'),
]