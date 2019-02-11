from django.shortcuts import render,redirect
from .forms import *
from django.views.generic import TemplateView
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import datetime
from datetime import timedelta  
import json
from django.http import JsonResponse
from django.contrib import messages
from TGA_tool.utils import *
from django.db import models 
# Create your views here.
def home(request):
    return render(request, 'TGA_tool/home.html')

def calendar(request):
    return render(request,'TGA_tool/calendar.html')

def nouvelleFamille(request):
    form = FamilleForm(request.POST or None)
    if form.is_valid():
        famille = form.save(commit=False)
        if len(Famille.objects.filter(nom=famille.nom))>0 and len(Famille.objects.filter(adresse=famille.adresse))>0 :
            famille.nom=famille.nom+" "+str(len(Famille.objects.filter(nom=famille.nom))+1)
        famille.save() 
        envoi = True
        return redirect(nouveauParent, famille.id)#envoyer l'id en paramétre
        
    return render(request, 'TGA_tool/nouvelle-famille.html',locals())

def nouveauParent(request, id):
    form = ParentForm(request.POST or None)
    if form.is_valid(): 
        parent = form.save(commit=False)
        parent.famille = Famille.objects.get(id=id)
        print(parent.famille.id)
        parent.save()
        form.save_m2m()

        if 'end' in request.POST :#test if the user choosed "submit" 
            return redirect(nouveauEleve, id) #renvoyer vers le formulaire d'ajout d'élèves avec l'id famille en paramétre
        elif 'submit & add other' in request.POST :#or "submit && add" 
            form=ParentForm()#Vider le formulaire 
            return render(request,'TGA_tool/nouveau-parent.html', locals())

    return render(request, 'TGA_tool/nouveau-parent.html', locals())    

def nouveauEleve(request, id=0):

    if id>0:
        form = EleveForm(request.POST or None)
        famille = True 
        if form.is_valid(): 
            eleve = form.save(commit=False)
            eleve.famille = Famille.objects.get(id=id)
            if ElevePotentiel.objects.get(nom=form.cleaned_data["nom"]):
                #Si cet élève était un élève potentiel déja on le lie avec l'instance de l'élève potentiel
                #et on garde les autres requetes si il y'en a, on suprime la requete qui correspon a son cours si c'est elle 
                elevepotentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"])
                #Ici on gére le cas ou deux eleves ont le meme nom 
                eleve=form.save(commit=False)
                eleve.elevepotentiel_ptr=elevepotentiel
                #Il se peut que les coordonés prises quand l'elève s'est présenté aient changés 
                
                eleve.elevepotentiel_ptr.email=form.cleaned_data["email"]
                eleve.elevepotentiel_ptr.num=form.cleaned_data["num"]
                eleve.save()
                form.save_m2m()
                for cours in form.cleaned_data["cours"] :
                    
                    if Requete.objects.filter(eleve=elevepotentiel).filter(matiere=cours.matiere):
                        requete=Requete.objects.filter(eleve=elevepotentiel).filter(matiere=cours.matiere)
                        requete.delete()

            else :
                eleve = form.save()
                form.save_m2m()
            
    else:
        form = EleveForm2(request.POST or None)
        famille = False
        if form.is_valid():
            if ElevePotentiel.objects.get(nom=form.cleaned_data["nom"]):
                #Si cet élève était un élève potentiel déja on le lie avec l'instance de l'élève potentiel
                #et on garde les autres requetes si il y'en a, on suprime la requete qui correspon a son cours si c'est elle 
                elevepotentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"])
                #Ici on gére le cas ou deux eleves ont le meme nom 
                eleve=form.save(commit=False)
                eleve.elevepotentiel_ptr=elevepotentiel
                #Il se peut que les coordonés prises quand l'elève s'est présenté aient changés 
                eleve.elevepotentiel_ptr.email=form.cleaned_data["email"]
                eleve.elevepotentiel_ptr.num=form.cleaned_data["num"]
                eleve.save()
                form.save_m2m()
                for cours in form.cleaned_data["cours"] :
                    
                    if Requete.objects.filter(eleve=elevepotentiel).filter(matiere=cours.matiere):
                        requete=Requete.objects.filter(eleve=elevepotentiel).filter(matiere=cours.matiere)
                        requete.delete()
                        

            else :
                eleve = form.save()
            return redirect('home.html')
    
    if 'end' in request.POST :#test if the user choosed "submit" 
            return render(request,'TGA_tool/home.html')
    elif 'submit & add other' in request.POST :#or "submit && add" 
            form=EleveForm()#Vider le formulaire 
            return render(request,'TGA_tool/nouveau-eleve.html', locals())
    return render(request,'TGA_tool/nouveau-eleve.html', locals())	

def nouveauCoach(request):
    form = CoachForm(request.POST or None)
    if form.is_valid(): 
        #Création de l'utilisateur 
        user = User.objects.create_user(form.cleaned_data["prenom"], form.cleaned_data["email"] , 'TGA123')

        #Extension du profile
        coach = form.save(commit=False)
        coach.user = user
        coach.save()    
        form.save_m2m()
        envoi = True

    if 'end' in request.POST :#test if the user choosed "submit" 
        return render(request,'TGA_tool/home.html')
    elif 'submit & add other' in request.POST :#or "submit && add" 
        form=CoachForm()#Vider le formulaire 
        return render(request,'TGA_tool/nouveau-coach.html', locals())
    
    return render(request, 'TGA_tool/nouveau-coach.html', locals())	

def connexion(request):
    error = False
    form = ConnexionForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
        if user is not None:  # Si l'objet renvoyé n'est pas None
            login(request, user)  # nous connectons l'utilisateur
            return redirect('home.html')
        else: # sinon une erreur sera affichée
            error = True
  
    return render(request, 'TGA_tool/login-coach.html', locals())

def deconnexion(request):
    logout(request)
    return redirect("connexion")

#@login_required
def mesCours(request):
    listecours =[]
    if request.GET['cours']=='all':
        cours = Cours.objects.all()
        for cour in cours:
            listecours.append({'id': cour.id, 'curriculum': cour.matiere.curriculum.niveau, 'matiere': cour.matiere.matiere, 'frequence': cour.frequence.frequence})

    else:
        id = request.user.id
        coach = Coach.objects.get(user = id)
        cours = Cours.objects.filter(coach = coach.id)  
        for cour in cours:
            listecours.append({'id': cour.id, 'curriculum': cour.matiere.curriculum.niveau, 'matiere': cour.matiere.matiere, 'frequence': cour.frequence.frequence})
    
    return render(request,'TGA_tool/cours-du-coach.html', locals())


def mesSeances(request):
 
    id = request.user.id
    coach = Coach.objects.get(user = id)
    cours = Cours.objects.filter(coach = coach.id)
    listeseances =[]
    for cour in cours:
        seances = Seance_Cours.objects.filter(cours = cour.id)
        for seance in seances:
             #listeseances.append({'id': seance.id, 'curriculum': seance.cours.matiere.curriculum.niveau, 'matiere': seance.cours.matiere.matiere, 'date' : str(seance.date), 'start' : str(seance.creneau.debut)})       
            listeseances.append({'title': seance.cours.matiere.curriculum.niveau + " - " + seance.cours.matiere.matiere, 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "displayseance.html/" + str(seance.id)})
    
    #Cette partie va récupérer les seances de coaching 
    coachings=Seance_Coaching.objects.filter(coach= coach.id)
    for seance in coachings:
        listeseances.append({'title': "Coaching " + seance.matiere.curriculum.niveau + " - " + seance.matiere.matiere, 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "display-seance-coaching.html/" + str(seance.id)})

    data = listeseances

    return JsonResponse(data, safe=False)

def displaySeance(request,id):
    #Cette vue permet d'afficher les détails d'une séance 
    # infos de la séances (date,heure, salle, chapitre, notions)
    # groupe d'élève de la séance
    # trois boutons : annuler, modifier,   déclarer
    seance = Seance_Cours.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    niveau = seance.cours.curriculum
    matiere = seance.cours.matiere.matiere
    chapitre = seance.chapitre
    notions = seance.notions
    eleves = Eleve.objects.filter(cours=seance.cours.id)
    statut = seance.statut
    displayMode = 1 # 1 : par défaut, 2 : modifier, 3 : déclarer


    return render(request, 'TGA_tool/display-seance.html', locals())

def annulerSeance(request,id):
    seance = Seance_Cours.objects.get(id = id)
    seance.statut = "Annulé"
    seance.save()
    messages.add_message(request, messages.SUCCESS, 'La séance a été annulée !')
    return redirect(displaySeance, id)

def modifierSeance(request,id):
    seance = Seance_Cours.objects.get(id=id)
    form = SeanceForm(request.POST or None, instance= seance)

    if form.is_valid():
        form.save()
        return redirect(displaySeance, id)
    return render(request, 'TGA_tool/edit-seance.html', locals()) 


def declarerSeance(request,id):
    seance = Seance_Cours.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    matiere = seance.cours.matiere.matiere
    chapitre = seance.chapitre
    notions = seance.notions.all()
    eleves = Eleve.objects.filter(cours=seance.cours.id)
    statut = seance.statut

    # Renseigner le chapitre et notions vues dans le cours

    # déclarer les élèves présents
        # recupérer les éleves cochés présents
    form = ReportSeanceForm(request.POST or None)
    form.fields['eleves'].queryset=Eleve.objects.filter(cours= seance.cours.id)
        
    if form.is_valid():
        
        seance.statut="Done"
        eleves=form.cleaned_data['eleves']
        seance.eleves.set(eleves)
        for eleve in eleves :
                parent=Parent.objects.filter(estResponsable=True).get(famille=eleve.famille)
                print(parent)
                parent.debit-=3000
                parent.solde-=3000
                parent.save()
        coach=seance.cours.coach        
        coach.salaire+=1000
        coach.save()
        seance.save()

        # les ajouter à la séance en question

    # Changer le status de la séance

    # Créer un avoir pour les parents des élèves en fonction du type de la séance

    # optionnel : envoi d'un email au parent

    return render(request, 'TGA_tool/report-seance.html', locals()) 
    

def displaySeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    niveau = seance.matiere.curriculum
    matiere = seance.matiere.matiere
    chapitre = seance.chapitre
    notions = seance.notions
    eleves = seance.eleve.all()
 
    statut = seance.statut
    


    return render(request, 'TGA_tool/display-seance-coaching.html', locals())


def annulerSeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id = id)
    seance.statut = "Annulé"
    seance.save()
    messages.add_message(request, messages.SUCCESS, 'La séance a été annulée !')
    return redirect(displaySeanceCoaching, id)

def modifierSeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id=id)
    form = Seance_CoachingForm(request.POST or None, instance= seance)

    if form.is_valid():
        form.save()
        return redirect(displaySeanceCoaching, id)
    return render(request, 'TGA_tool/edit-seance-coaching.html', locals()) 


def declarerSeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    matiere = seance.matiere.matiere
    chapitre = seance.chapitre
    notions = seance.notions
    eleves = seance.eleve.all()
    statut = seance.statut

    # Renseigner le chapitre et notions vues dans le cours

    # déclarer les élèves présents
        # recupérer les éleves cochés présents
    form = ReportSeanceCoachingForm(request.POST or None)
    form.fields['eleves'].queryset=eleves
    if form.is_valid():
        seance.statut="Done"
        eleves_presents=form.cleaned_data['eleves']
        seance.eleve.set(eleves_presents)
        for eleve in eleves_presents:
            parent=Parent.objects.filter(estResponsable=True).get(famille=eleve.famille)
            parent.solde-=5000
            parent.débit-=5000
            parent.save()
        coach=seance.coach
        coach.salaire+=1000
        coach.save()
        seance.save()
        return render(request, 'TGA_tool/home.html', locals())
        # les ajouter à la séance en question

    # Changer le status de la séance

    # Créer un avoir pour les parents des élèves en fonction du type de la séance

    # optionnel : envoi d'un email au parent

    return render(request, 'TGA_tool/report-seance-coaching.html', locals())

def makePayement(request):
    form = PayementForm(request.POST or None)
    if form.is_valid():
        payement = form.save()
        parent = form.cleaned_data['parent']
        montant= form.cleaned_data['montant']
        print(parent.solde)
        parent.credit+=montant
        parent.solde+=montant
        parent.save()
        if "did_paid" in request.POST:
            paid=True
        elif "will_pay" in request.POST :
            form=PayementForm()
            return render(request, 'TGA_tool/make-payement.html', locals())
        return render(request, 'TGA_tool/make-payement.html', locals())


    return render(request, 'TGA_tool/make-payement.html', locals())

def nouvelleSeanceCoaching(request) :
    form= Seance_CoachingForm(request.POST or None)
    if form.is_valid():
        form.save()
    if 'end' in request.POST:
            return redirect('home.html')
    elif 'submit & add other' in request.POST :
        form=Seance_CoachingForm()
        #Vider les formulaires
        return render(request, 'TGA_tool/seance-coaching.html',locals())
    return render(request, 'TGA_tool/seance-coaching.html', locals())

def nouvelleSeanceCours(request) :
    form= SeanceForm2(request.POST or None)
    #form.fields['eleves'].queryset=Eleve.objects.filter(matiere=seance.cours.matiere)
    if form.is_valid():
        form.save()
    if 'end' in request.POST:
            return redirect('home.html')
    elif 'submit & add other' in request.POST :
        form=Seance_CoachingForm()
        #Vider les formulaires
        return render(request, 'TGA_tool/seance-coaching.html',locals())
    return render(request, 'TGA_tool/seance-coaching.html', locals())




def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        #renvoi = form.cleaned_data['renvoi']
        form.fields['sujet'].help_text='Je peut aider'
        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
       
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'TGA_tool/contact.html', locals())

def seance_cours(request):
    form = Seance_CoursForm(request.POST or None)
    
    if form.is_valid() :
        seance=form.cleaned_data['seance']
        while not(form.cleaned_data['chapitre']) or not(form.cleaned_data['salle']) or not(form.cleaned_data['notion']) :
            form.fields['chapitre'].queryset=Chapitre.objects.filter(matiere=seance.cours.matiere)
            #chapitre=form.cleaned_data['chapitre']
            form.fields['notion'].queryset=Notions.objects.filter(chapitre=form.cleaned_data['chapitre'])
            #print(seance.pk)
            return render(request,'TGA_tool/modifier-seance_cours.html', locals())
            #print(notion)
            
        seance.salle=form.cleaned_data['salle']
        seance.chapitre=form.cleaned_data['chapitre']
        if form.cleaned_data['notion']:
            seance.save()
            seance.notions.set(form.cleaned_data['notion'])
        if seance.notions :
            seance.save()
            return render(request,'TGA_tool/home.html', locals())
            
    return render(request,'TGA_tool/modifier-seance_cours.html', locals())	

def matiere(request):
    form = MatiereForm(request.POST or None)
    if form.is_valid():
        matiere=form.cleaned_data['matiere']
        print(matiere.id)
        return redirect(chapitreNotions, matiere.id)#envoyer l'id en paramétre
       # return render(request, 'TGA_tool/nouveau-chapitre.html',{'matiere': mat} )
    return render(request, 'TGA_tool/nouvelle-matiere.html',locals())

def chapitreNotions(request, id): 
    form_chapitre=ChapitreForm(request.POST or None)
    NotionFormset = formset_factory(NotionForm, extra=4,max_num=4)
    form_notions=NotionFormset(request.POST or None)
    if form_notions.is_valid() and form_chapitre.is_valid() :
        chapitre=Chapitre.objects.create(chapitre=form_chapitre.cleaned_data['chapitre'],matiere=Matiere.objects.get(id= id))#créer le chapitre a partir de l'id matiere
        notions={}
        for form in form_notions.forms:#itérateur des formulaires
            if form.cleaned_data != {}:#éviter les formulaires vides
                notions[form.cleaned_data['notion']]= form.cleaned_data['details']#Créer un dictionnaire ou les "keys" sont les notions et les values sont les détails
        for notion_key in list(notions.keys()):#parcourir les clefs 
           Notions.objects.create(notion=notion_key,details=notions[notion_key],chapitre=chapitre)
        if 'end' in request.POST:#Partie réponse 
            return redirect('../home.html')
        elif 'submit & add other' in request.POST :
            form_chapitre=ChapitreForm()
            form_notions=NotionFormset()#Vider les formulaires
            return render(request, 'TGA_tool/nouveau-chapitre.html',locals())
    return render(request, 'TGA_tool/nouveau-chapitre.html',locals())

def nouveauCours(request):
    frequency_form=FrequenceForm(request.POST or None)
    cours_form=CoursForm(request.POST or None)
    if cours_form.is_valid() and frequency_form.is_valid():
        frequence=frequency_form.save()
        matiere=cours_form.cleaned_data['matiere']
        Cours.objects.create(curriculum=matiere.curriculum,matiere=matiere,coach=cours_form.cleaned_data['coach'],frequence=frequence)
        #Cette partie concerne le traitement du type de la réponse 
        if 'end' in request.POST:
            return redirect('home.html')
        elif 'submit & add other' in request.POST :
            frequency_form=FrequenceForm()
            cours_form=CoursForm()#Vider les formulaires
            return render(request, 'TGA_tool/nouveau-cours.html',locals())
    return render(request, 'TGA_tool/nouveau-cours.html',locals())

def init_data(request):
    
    if "Creneaux" in request.POST :
        if len(Creneau.objects.all())<20 :
            init_creneaux()
            done=True
        else:
            already=True

        return render(request,'TGA_tool/initial-data.html',locals())
    elif "Curricilum" in request.POST :
        if(len(Curriculum.objects.all()))==0:
            init_curriculums()#Cette fonction se trouve dans le fichier utils.py
            done=True
        else:
            already=True
        return render(request,'TGA_tool/initial-data.html',locals())

    elif "Matiere" in request.POST :
        if len(Matiere.objects.all())<200 :    
            init_matieres()
            done=True
        else:
            already=True
        return render(request,'TGA_tool/initial-data.html',locals())
    
    return render(request, 'TGA_tool/initial-data.html',locals())

"""
def eleveArrive(request):
    parents_titles=['Parent responsable','Parent contact']
    ParentFormset = modelformset_factory(Parent,form=ParentForm,extra=2,max_num=2)
    parent_form=ParentFormset(request.POST or None,initial=[{'estResponsable':'True',}])
    parents={}
    ind=0
    eleve_form=EleveForm(request.POST or None)
    for form in parent_form:
        parents[parents_titles[ind]]=form
        ind+=1    
    
    if parent_form.is_valid() and eleve_form.is_valid():
        eleve=eleve_form.save(commit=False)
        ind=0

        for parent in parent_form.save():              
            parents[parents_titles[ind]]=parent
            if ind==0:
                eleve.parent_resp=parent
            elif ind==1:
                eleve.parent_sec=parent
            ind+=1
        if ind==1:#si la boucle a éxécuté une seule itération uniquement(un parent)
                eleve.parent_sec=None
        eleve.save()
        eleve_form.save_m2m()
        if 'end' in request.POST:
            return redirect('home.html')
        elif 'submit & add other' in request.POST :
            
            parent_form=ParentFormset()
            eleve_form=EleveForm()#Vider les formulaires
            ids=[]
            ids.append(eleve.parent_resp.id)
            if eleve.parent_sec!=None:
                ids.append(eleve.parent_sec.id)
            else :
                ids.append(-1)
           
    return render(request, 'TGA_tool/eleve-arrive.html',locals())"""


def display(request,type):
    if type=="1":
        #Cette partie redirige vers une vue qui liste les membres de la famille 
        #avec des détails sur la consommation totale de la famille et avec les 
        #rapports pédagogiques
        familles=Famille.objects.all() 
    elif type=="2":
        parents=Parent.objects.filter(estResponsable=True)
        #Cette partie est utile si l'utilisateur veut contacter les parents
        #Si la personne responsable ne répond pas on va vers le parent contact qui va 
        #se trouver dans les détails de famille 
    elif type=="3":
        eleves=Eleve.objects.all()
    elif type=="4":
        paiements=Payement.objects.all()
    elif type=="5":
        coachs=Coach.objects.all()
        #Dirige vers une vue qui contient le salaire du coachs avec les
        #séances qu'il a enseigné
    elif type=="6":
        cours=Cours.objects.all()
    elif type=="7":
        salles=Salle.objects.all()#Cette partie redirige vers une page qui aura les details de 
                                  #la salle a savoir : capacité,calendrier,prise/libre ...
    elif type=="8":
        requetes=Requete.objects.all()
    
    return render(request,'TGA_tool/display.html', locals())

def details(request,type,id):
    if type=="5" :
        coach=Coach.objects.get(id=id)
        cours=Cours.objects.filter(coach=coach)
        listSeancesEnseigne=[]
        listSeancesRestant=[]
        for cour in cours:
            seances_done = Seance_Cours.objects.filter(cours = cour.id).filter(statut="Done")
            seances_planifie= Seance_Cours.objects.filter(cours = cour.id).filter(statut="Planifié")
            listSeancesEnseigne.append(seances_done)
            listSeancesRestant.append(seances_planifie)    
        listSeancesEnseigne.append(Seance_Coaching.objects.filter(coach = coach.id).filter(statut="Done"))
        listSeancesRestant.append(Seance_Coaching.objects.filter(coach = coach.id).filter(statut="Planifié"))
        print(listSeancesEnseigne)
        print(listSeancesRestant)
        sancesDone=len(listSeancesEnseigne)
        seancesRestant=len(listSeancesRestant)


    return render(request,'TGA_tool/details.html', locals())    

def requete(request,type):#1 pour une requete externe / 2 pour une requete interne 
    requete_form=RequeteForm(request.POST or None)
    eleve_form=SelectEleveForm(request.POST or None)
    eleve_potentiel_form=ElevePotentielForm(request.POST or None)
    if type == "1":        
        ind=True#Pour éviter la création de plusieurs instances de eleve potentiel
        if eleve_potentiel_form.is_valid() and requete_form.is_valid():
            if ind: 
                eleve_potentiel=eleve_potentiel_form.save()
                ind=False
            for matiere in requete_form.cleaned_data['matiere']:
                if requete_form.cleaned_data['creneau']:#On doit vérifier l'existence d'un créneau pour utiliser la fonction .set
                
                    requete=Requete.objects.create(matiere=matiere,jour=requete_form.cleaned_data['jour'],eleve=eleve_potentiel)
                    requete.creneau.set(requete_form.cleaned_data['creneau'])

                else :
                    Requete.objects.create(matiere=matiere,jour=requete_form.cleaned_data['jour'],eleve=eleve_potentiel)
    
    elif type == "2":
        
        if eleve_form.is_valid() and requete_form.is_valid():
            for matiere in requete_form.cleaned_data['matiere']:
                if requete_form.cleaned_data['creneau']:#On doit vérifier l'existence d'un créneau pour utiliser la fonction .set
                
                    requete=Requete.objects.create(matiere=matiere,jour=requete_form.cleaned_data['jour'],eleve=eleve_form.cleaned_data['eleve'])
                    requete.creneau.set(requete_form.cleaned_data['creneau'])

                else :
                    Requete.objects.create(matiere=matiere,jour=requete_form.cleaned_data['jour'],eleve=eleve_form.cleaned_data['eleve'])
            
    
    if 'end' in request.POST:
            return redirect('home.html')
    elif 'submit & add other' in request.POST :
        requete_form=RequeteForm()
        eleve_form=SelectEleveForm()
        eleve_potentiel_form=ElevePotentielForm()
        return render(request, 'TGA_tool/nouvelle-requete.html',locals())
    
    
    return render(request, 'TGA_tool/nouvelle-requete.html', locals())