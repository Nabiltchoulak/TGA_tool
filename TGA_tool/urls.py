from django.urls import path,re_path
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
    url(r'^nouveau-eleve\.html$', views.nouveauEleve, name="nouveau eleve"),
    path('nouveau_eleve-extra/<int:id>',views.choose_extra_courses, name = "extra courses"),
    path('nouveau-eleve.html/<int:id>', views.nouveauEleve, name="nouveau eleve"),
    path('eleve_already_in', views.ChooseEleve, name="choose eleve"),
    re_path(r'^ajax_new_student$',views.ajaxNewEleve, name="ajax NE"),
    re_path(r'^ajax_new_cours$',views.ajaxNewCours, name="ajax new cours"),
    re_path(r'^ajax_requete$',views.ajax_requete, name="ajax requete"),

    re_path(r'^presence_checker$',views.presence_checker, name="presence checker"),
    path('nouveau-parent.html', views.nouveauParent, name="nouveau parent"),
    path('nouveau-client', views.newClient, name="nouveau client"),
    path('nouveau-coach.html', views.nouveauCoach, name="nouveau coach"),
    path('seance-coaching.html', views.nouvelleSeanceCoaching, name="seance coaching"),
    path('seance-cours.html', views.nouvelleSeanceCours, name="seance cours"),
    #path('nouvelle-famille.html', views.nouvelleFamille, name="nouvelle famille"),
    #path('liste-famille',views.listeFamilles, name="liste famille"),
    path('initial-data.html', views.init_data, name="initial data"),
    path('test',views.some_view),

    url(r'^home.html$',TemplateView.as_view(template_name="TGA_tool/home.html")),#Test des vues génériques
    #path('nouvelle-matiere.html', views.matiere, name="nouvelle matiere"),
    path('nouveau-chapitre.html/<int:id>',views.chapitreNotions,name='chapitre notion'),
    path('nouveau-cours.html/<str:choice>', views.nouveauCours, name="nouveau cours"),
    path('nouvelle-requete.html/<str:type>', views.new_requete, name="nouvelle requete"),
    path('nouveau-prospect', views.new_prospect_cours, name="nouveau prospect"),
    url(r'^nouvelle-requete-3', views.choose_creneaux, name="choose creneaux"),
    
    path('nouvelle-requete-2/<int:id>/<str:demandeur>', views.choose_sessions, name="choose sessions"),
    #path('eleve-arrive.html', views.eleveArrive, name="eleve arrive"),
    path('display.html/<str:type>',views.display,name='display'),
    path('details.html/<str:type>/<int:id>',views.details,name='details'),
    # Les urls du profile du coach
    path('mes-cours.html',views.mesCours,name='mes cours'), # id du coach
    url(r'^mes-seances.html/$',views.mesSeances, name= 'mes seances'), #id du coach
    path('displayseance.html/<int:id>',views.displaySeance,name='display seance'),
    path('display-seance-coaching.html/<int:id>',views.displaySeanceCoaching,name='display seance coaching'),
    path('annulerseance.html/<int:id>',views.annulerSeance,name='annuler seance'),
    path('annuler-seance-coaching.html/<int:id>',views.annulerSeanceCoaching,name='annuler seance coaching'),
    path('edit-seance.html/<int:id>',views.modifierSeance,name='edit seance'),
    path('edit-seance-coaching.html/<int:id>',views.modifierSeanceCoaching,name='edit seance coaching'),
    path('report-seance.html/<int:id>',views.declarerSeance,name='report seance'),
    path('report-seance-coaching.html/<int:id>',views.declarerSeanceCoaching,name='report seance coaching'),
    # les urls du paiement
    path('make-payement/<int:id>',views.makePayement,name='make payement'),

    

]