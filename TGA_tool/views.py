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
from django.http import HttpResponse
from datetime import timedelta  
import json
from django.http import JsonResponse
from django.contrib import messages
from TGA_tool.utils import *
from django.db import models 
from django.core.exceptions import ObjectDoesNotExist
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.files import File

########################################################## Test ###################################################"
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound

def some_view(request):
    
    #f2 = ContentFile(b"these are bytes")
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Start writng the PDF here
    p.drawString(0, 100, 'A')
    # End writing

    p.showPage()
    p.save()
    pdf=open('./static/hell.pdf',"wb")
    pdf.write(buffer.getvalue())
    buffer.close()
    pdf.close()





    fs = FileSystemStorage()
    filename = './static/hell.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
####################################################### Nouveau : Parent Eleve Client Coach ##########################################################""

def nouveauParent(request):
    form = ParentForm(request.POST or None)
    if form.is_valid(): 
        parent = form.save(commit=False)
        if form.cleaned_data["email"]:
                user = User.objects.create_user(form.cleaned_data["email"] , form.cleaned_data["email"] , 'TGA123')

                
        else : 
            user = User.objects.create_user(form.cleaned_data["prenom"]  ,form.cleaned_data["prenom"],  'TGA123')
        parent.user=user
        #Création automatique de la famille 
        if len(Famille.objects.filter(nom=parent.nom))>0 and len(Famille.objects.filter(adresse=form.cleaned_data["adresse"]))>0 :
            nom=parent.nom+" "+str(len(Famille.objects.filter(nom=parent.nom))+1)
        famille=Famille.objects.create(nom=form.cleaned_data["nom"], adresse=form.cleaned_data["adresse"])
        id=famille.id
        parent.famille=famille
        parent.save()
        form.save_m2m()

        if 'end' in request.POST :#test if the user choosed "submit" 
            return redirect(nouveauEleve, id) #renvoyer vers le formulaire d'ajout d'élèves avec l'id famille en paramétre
        elif 'submit & add other' in request.POST :#or "submit && add" 
            form=ParentForm()#Vider le formulaire 
            return render(request,'TGA_tool/nouveau-parent.html', locals())

    return render(request, 'TGA_tool/nouveau-parent.html', locals())    

def newClient(request):
    
    form=ClientForm(request.POST or None)

    
    if form.is_valid():
        if form.cleaned_data["nom"] and form.cleaned_data["prenom"] and form.cleaned_data["telephone"]:
        #cette partie va chercher si il existe un parent qui a le meme nom-prenom-telephone que le nouveau client
            try :
                parent=Parent.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],telephone=form.cleaned_data["telephone"])
            
            
            except ObjectDoesNotExist:#Si on ne trouve aucun parent ce bouléan va définir la méthode dont laquelle va se créer le parent
                
                is_parent=False

            else : 
                
                is_parent=True

        
        if is_parent :#ramener le parent et le rataccher au client et ajouter les cours choisis 
            client=Client.objects.create(parent_ptr=parent,date_naissance=form.cleaned_data["date_naissance"])
            client.cours.set(form.cleaned_data["cours"])
            
            client.save()

        else :#Crer le user du nouveau client et créer le client 
            client=form.save()
            if form.cleaned_data["email"]:
                user = User.objects.create_user(form.cleaned_data["email"] , form.cleaned_data["email"] , 'TGA123')

                
            else : 
                user = User.objects.create_user(form.cleaned_data["prenom"]  ,form.cleaned_data["prenom"],  'TGA123')
            
            client.user=user
        
        #Le reste (ce qui vient en dessous) est commun pour les deux cas ( client parent ou pas )
        client.date_commencement=date.today()
        
        #essayer si ce client était déjà un client potentiel
        try:# Vérifier si ce client est un client potentiel déjà 
            ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
        except ObjectDoesNotExist:
            
            client.save()
            parent.save()
            
            if 'end' in request.POST :#test if the user choosed "submit" 
                return render(request,'TGA_tool/home.html')
            elif 'submit & add other' in request.POST :#or "submit && add" 
                form=ClientForm() #Vider le formulaire
        
        #Si c'est le cas prendre la liste de cours qu'il a demandé transférer les requetes de l'eleve poentiel au client et suprimer les requetes accomplies et l'eleve potentiel
        
        ###############*******
        client_potentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
        
        #Dans toutes les requetes changer de l'eleve au client pour transferer les requetes restantes 
        
        if client_potentiel.sessions:
            
            requetes=Requete.objects.filter(eleve=client_potentiel)
            for requete in requetes:
                requete.eleve= None
                requete.client=client
                requete.save()
        client.save()

        #Supprimer toutes les requetes qui contiennent les cours qui ont été choisit 

        for cours in form.cleaned_data["cours"] :
                
                if Requete.objects.filter(client=client).filter(session=cours.session):
                    requete=Requete.objects.filter(client=client).filter(session=cours.session)
                    requete.delete()
        
        #supprimer l'élève potentiel 

        client_potentiel.delete()
        ###############**********

    if 'end' in request.POST :#test if the user choosed "submit" 
                return render(request,'TGA_tool/home.html')
    elif 'submit & add other' in request.POST :#or "submit && add" 
                form=ClientForm() #Vider le formulaire
    return render(request, 'TGA_tool/newClient.html', locals())


def ajaxNewEleve(request):
    # Cette fonction n'est pas dans la fonction nouveauEleve par ce que je n'ai pas trrouvé comment envoyer un post a un url 
    # qui contient un id sans affecter l'id (j'avais toujours id=0)
    if 'langue_id' in list(request.POST.keys()):
        form = EleveForm(request.POST or None)
        id_2=int(request.POST['langue_id'])
        langue= Langue.objects.get(id=id_2)
        form.fields['cours'].queryset=Cours.objects.filter(langue=langue)
        data=[]
        data=form["cours"]
        
        return HttpResponse(str(data))


def ajax_requete(request):
    if 'langue_id' in list(request.POST.keys()):
        form=RequeteForm(request.POST or None)
        eleve_form=SelectEleveForm(request.POST or None)
        id=int(request.POST['langue_id'])
        langue= Langue.objects.get(id=id)
        form.fields['session'].queryset=Session.objects.filter(langue=langue)
        #eleve_form.fields['eleve'].queryset=Eleve.objects.filter(langue=langue)
        data=form['session']
        
        return HttpResponse(str(data))


def nouveauEleve(request, id=0):
    
    if id>0:
        
        form = EleveForm(request.POST or None)
        famille = True 
        
        if form.is_valid(): 
            
            eleve = form.save(commit=False)
            eleve.famille = Famille.objects.get(id=id)
            try:
                ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
            except ObjectDoesNotExist:
                eleve = form.save()
                form.save_m2m()
                #Si cet élève était un élève potentiel déja on le lie avec l'instance de l'élève potentiel
                #et on garde les autres requetes si il y'en a, on suprime la requete qui correspon a son cours si c'est elle 
            elevepotentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
            #Ici on gére le cas ou deux eleves ont le meme nom 
            #eleve=form.save(commit=False)
            eleve.elevepotentiel_ptr=elevepotentiel
            #Il se peut que les coordonés prises quand l'elève s'est présenté aient changés 
                
            eleve.elevepotentiel_ptr.email=form.cleaned_data["email"]
            eleve.elevepotentiel_ptr.num=form.cleaned_data["telephone"]
            #print(eleve)
            print(eleve.save())
            elevepotentiel.save()
            form.save_m2m()
            for cours in form.cleaned_data["cours"] :
                    
                if Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session):
                    requete=Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session)
                    requete.delete()
            if 'end' in request.POST :#test if the user choosed "submit" 
                return render(request,'TGA_tool/home.html')
            elif 'submit & add other' in request.POST :#or "submit && add" 
                form=EleveForm()#Vider le formulaire 
                return render(request,'TGA_tool/nouveau-eleve.html', locals())

            
    else:
        form = EleveForm2(request.POST or None)
        famille = False#Cet élève posséde déja une famille 
        
        
        if 'langue_id' in list(request.POST.keys()):
            
            id_2=int(request.POST['langue_id'])
            
            curr= Langue.objects.get(id=id_2)
            form.fields['cours'].queryset=Cours.objects.filter(langue=curr)
            
            return HttpResponse(str(form['cours']))
        #print(form.errors)
        if form.is_valid():
            try:
                ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"])
                #Si cet élève était un élève potentiel déja on le lie avec l'instance de l'élève potentiel
                #et on garde les autres requetes si il y'en a, on suprime la requete qui correspon a son cours si c'est elle 
            except ObjectDoesNotExist:
                eleve = form.save()
                

            elevepotentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"])
            #Ici on gére le cas ou deux eleves ont le meme nom 
            eleve=form.save(commit=False)
            eleve.elevepotentiel_ptr=elevepotentiel
            #Il se peut que les coordonés prises quand l'elève s'est présenté aient changés 
            eleve.elevepotentiel_ptr.email=form.cleaned_data["email"]
            eleve.elevepotentiel_ptr.num=form.cleaned_data["telephone"]
            eleve.save()
            elevepotentiel.save()
            form.save_m2m()
            for cours in form.cleaned_data["cours"] :
                    
                if Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session):
                    requete=Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session)
                    requete.delete()
    
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


################################################### Connexion/deconnexion #################################################################""

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

################################################ Nouveau cours ##################################################################


def nouveauCours(request):
    frequency_form=FrequenceForm(request.POST or None)
    cours_form=CoursForm(request.POST or None)
    
    if cours_form.is_valid() and frequency_form.is_valid():
        frequence=frequency_form.save()
        session=cours_form.cleaned_data['session']
        Cours.objects.create(langue=session.langue,session=session,coach=cours_form.cleaned_data['coach'],frequence=frequence)
        #Cette partie concerne le traitement du type de la réponse 
        if 'end' in request.POST:
            return redirect('home.html')
        elif 'submit & add other' in request.POST :
            frequency_form=FrequenceForm()
            cours_form=CoursForm()#Vider les formulaires
            return render(request, 'TGA_tool/nouveau-cours.html',locals())
    return render(request, 'TGA_tool/nouveau-cours.html',locals())






############################################## Cours du coach #####################################
#@login_required
def mesCours(request):
    listecours =[]
    if request.user.is_staff == 1:
        cours = Cours.objects.all()
        for cour in cours:
            listecours.append({'id': cour.id, 'langue': cour.session.langue.langue, 'session': cour.session.session, 'frequence': cour.frequence.frequence})

    elif request.user.is_staff == 0:
        id = request.user.id
        coach = Coach.objects.get(user = id)
        cours = Cours.objects.filter(coach = coach.id)  
        for cour in cours:
            listecours.append({'id': cour.id, 'langue': cour.session.langue.langue, 'session': cour.session.session, 'frequence': cour.frequence.frequence})
    
    return render(request,'TGA_tool/cours-du-coach.html', locals())


################################################################### Home Calendar mes séances ###################################################################
# Create your views here.
def home(request):
    return render(request, 'TGA_tool/home.html')

def calendar(request):
    return render(request,'TGA_tool/calendar.html')


def mesSeances(request):
 
    id = request.user.id
    listeseances =[]
    if request.user.is_staff == 0 :
        coach = Coach.objects.get(user = id)
        cours = Cours.objects.filter(coach = coach.id)
        coachings=Seance_Coaching.objects.filter(coach= coach.id)
        for seance in coachings:
            listeseances.append({'title': "Coaching " + seance.session.langue.langue + " - " + seance.session.session, 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "display-seance-coaching.html/" + str(seance.id)})
    elif request.user.is_staff == 1 : 
        cours=Cours.objects.all()
        coachings=Seance_Coaching.objects.all()
        print(coachings)
        if coachings :
            for seance in coachings:
                listeseances.append({'title': "Coaching " + seance.session.langue.langue  + " - " + seance.session.session + " - " + str(seance.coach) + " - " + str(seance.statut), 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "display-seance-coaching.html/" + str(seance.id)})
        
    
    for cour in cours:
        seances = Seance_Cours.objects.filter(cours = cour.id)
        for seance in seances:
             #listeseances.append({'id': seance.id, 'langue': seance.cours.session.langue.langue, 'session': seance.cours.session.session, 'date' : str(seance.date), 'start' : str(seance.creneau.debut)})       
            listeseances.append({'title': str(seance.cours.session) + " - "  + str(cour.coach) + " - " + str(seance.statut), 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "displayseance.html/" + str(seance.id)})
    
    #Cette partie va récupérer les seances de coaching 
    """coachings=Seance_Coaching.objects.filter(coach= coach.id)
    for seance in coachings:
        listeseances.append({'title': "Coaching " + seance.session.langue.langue + " - " + seance.session.session, 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "display-seance-coaching.html/" + str(seance.id)})"""

    data = listeseances

    return JsonResponse(data, safe=False)


################################################# Display Seance ########################################################

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
    langue = seance.cours.langue
    session = seance.cours.session.session
    #chapitre = seance.chapitre
    #notions = seance.notions
    eleves = Eleve.objects.filter(cours=seance.cours.id)
    statut = seance.statut
    displayMode = 1 # 1 : par défaut, 2 : modifier, 3 : déclarer


    return render(request, 'TGA_tool/display-seance.html', locals())

def displaySeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    langue = seance.session.langue
    session = seance.session.session
    #chapitre = seance.chapitre
    #notions = seance.notions
    eleves = seance.eleve.all()
 
    statut = seance.statut
    


    return render(request, 'TGA_tool/display-seance-coaching.html', locals())

#################################################################################### Annuler séance ###############################################################################

def annulerSeance(request,id):
    seance = Seance_Cours.objects.get(id = id)
    seance.statut = "Annulé"
    seance.save()
    messages.add_message(request, messages.SUCCESS, 'La séance a été annulée !')
    return redirect(displaySeance, id)


def annulerSeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id = id)
    seance.statut = "Annulé"
    seance.save()
    messages.add_message(request, messages.SUCCESS, 'La séance a été annulée !')
    return redirect(displaySeanceCoaching, id)


##################################################################################### Modifier seance #############################################################################

def modifierSeance(request,id):
    seance = Seance_Cours.objects.get(id=id)
    form = SeanceForm(request.POST or None, instance= seance)

    if form.is_valid():
        form.save()
        return redirect(displaySeance, id)
    return render(request, 'TGA_tool/edit-seance.html', locals()) 

def modifierSeanceCoaching(request,id):
    seance = Seance_Coaching.objects.get(id=id)
    form = Seance_CoachingForm(request.POST or None, instance= seance)

    if form.is_valid():
        form.save()
        return redirect(displaySeanceCoaching, id)
    return render(request, 'TGA_tool/edit-seance-coaching.html', locals()) 

#################################################################################### Déclaration des séances ###################################################################

def declarerSeance(request,id):
    seance = Seance_Cours.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    session = seance.cours.session.session
    #chapitre = seance.chapitre
    #notions = seance.notions.all()
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
    

def declarerSeanceCoaching(request,id):
    id_2=int(id)
    seance = Seance_Coaching.objects.get(id = id_2)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    session = seance.session.session
    #chapitre = seance.chapitre
    #notions = seance.notions
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


################################################################################# Création de séances cours/coaching ###############################################################


def nouvelleSeanceCoaching(request) :
    form = Seance_CoachingForm(request.POST or None)
    if request.POST:
        #print(form.errors.as_data())
        if 'langue_id' in list(request.POST.keys()):
            id=int(request.POST['langue_id'])
            langue= Langue.objects.get(id=id)
            form.fields['eleve'].queryset=Eleve.objects.filter(langue=langue)
            data=form['eleve'] 
            return HttpResponse(data)
        
        if 'eleves_id' in list(request.POST.keys()):
            if request.POST['eleves_id']:
                id_list=request.POST['eleves_id'].split(",")#On recoit une string contenant les ids séparés par ","
                ids=[]
                for id in id_list:#On va transformer cette liste de string en liste de int 
                    ids.append(int(id))
            
                matched_sessions=[]
                for id in ids:
                    sessions_eleve=Session.objects.none()
                    sessions_precedent=Session.objects.none()
                    eleve=Eleve.objects.get(id=id)
                    if id == ids[0]:#Tester si c'est la premiere itération
                        precedent=Eleve.objects.get(id=id)
                    for cours in eleve.cours.all():
                        sessions_eleve |=Session.objects.filter(cours__id=cours.id)
                
                    for cours in precedent.cours.all():
                        sessions_precedent |= Session.objects.filter(cours__id=cours.id)
                        #sessions_precedent
                    matched_sessions=sessions_eleve & sessions_precedent
                    precedent=Eleve.objects.get(id=id)
            
                form.fields['session'].queryset=matched_sessions
                return HttpResponse(form['session'])
            else :
                return HttpResponse("None")

        elif 'session_id' in list(request.POST.keys()):
            id=int(request.POST['session_id'])
            session= Session.objects.get(id=id)
            #form.fields['chapitre'].queryset=Chapitre.objects.filter(session=session)
            form.fields['coach'].queryset=Coach.objects.filter(sessions=session)
            data= [form['coach'],'iii',"form['chapitre']"]
            return HttpResponse(data)

            
        elif 'chapitre_id' in list(request.POST.keys()):
            id=int(request.POST['chapitre_id'])
            chapitre= Chapitre.objects.get(id=id)
            #form.fields['notions'].queryset=Notions.objects.filter(chapitre=chapitre)
            return HttpResponse(form['notions'])
    
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
    if request.POST:
        if 'langue_id' in list(request.POST.keys()):
            id=int(request.POST['langue_id'])
            langue= Langue.objects.get(id=id)
            form.fields['cours'].queryset=Cours.objects.filter(langue=langue)
            return HttpResponse(form['cours'])
        elif 'cours_id' in list(request.POST.keys()):
            id=int(request.POST['cours_id'])
            cours= Cours.objects.get(id=id)
            form.fields['chapitre'].queryset=Chapitre.objects.filter(session=cours.session)
            return HttpResponse(form['chapitre'])
        elif 'chapitre_id' in list(request.POST.keys()):
            id=int(request.POST['chapitre_id'])
            chapitre= Chapitre.objects.get(id=id)
            form.fields['notions'].queryset=Notions.objects.filter(chapitre=chapitre)
            return HttpResponse(form['notions'])
          
    #form.fields['eleves'].queryset=Eleve.objects.filter(session=seance.cours.session)
    if form.is_valid():
        form.save()
    #elif request.POST:
        #raise form.errors
    if 'end' in request.POST:
            return redirect('home.html')
    elif 'submit & add other' in request.POST :
        form=SeanceForm2()
        #Vider les formulaires
        return render(request, 'TGA_tool/seance-cours.html',locals())
    return render(request, 'TGA_tool/seance-cours.html', locals())


################################################ Session + chapitre + notions ##################################################################
def session(request):
    form = SessionForm(request.POST or None)
    if form.is_valid():
        session=form.cleaned_data['session']
        print(session.id)
        return redirect(chapitreNotions, session.id)#envoyer l'id en paramétre
       # return render(request, 'TGA_tool/nouveau-chapitre.html',{'session': mat} )
    return render(request, 'TGA_tool/nouvelle-session.html',locals())

def chapitreNotions(request, id): 
    form_chapitre=ChapitreForm(request.POST or None)
    NotionFormset = formset_factory(NotionForm, extra=4,max_num=4)
    form_notions=NotionFormset(request.POST or None)
    if form_notions.is_valid() and form_chapitre.is_valid() :
        chapitre=Chapitre.objects.create(chapitre=form_chapitre.cleaned_data['chapitre'],session=Session.objects.get(id= id))#créer le chapitre a partir de l'id session
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





############################################### Initial data #########################################################################


def init_data(request):
    
    if "Creneaux" in request.POST :
        if len(Creneau.objects.all())<20 :
            init_creneaux()
            done=True
        else:
            already=True

        return render(request,'TGA_tool/initial-data.html',locals())
    elif "Langue" in request.POST :
        if(len(Langue.objects.all()))==0:
            init_langues()#Cette fonction se trouve dans le fichier utils.py
            done=True
        else:
            already=True
        return render(request,'TGA_tool/initial-data.html',locals())

    elif "Session" in request.POST :
        if len(Session.objects.all())<200 :    
            init_sessions()
            done=True
        else:
            already=True
        return render(request,'TGA_tool/initial-data.html',locals())
    
    return render(request, 'TGA_tool/initial-data.html',locals())

#################################################################### Tableau de bord ###########################################################

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


##################################################################### Requete #####################################################

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
            for session in requete_form.cleaned_data['session']:
                if requete_form.cleaned_data['creneau']:#On doit vérifier l'existence d'un créneau pour utiliser la fonction .set
                
                    requete=Requete.objects.create(session=session,jour=requete_form.cleaned_data['jour'],eleve=eleve_potentiel)
                    requete.creneau.set(requete_form.cleaned_data['creneau'])

                else :
                    Requete.objects.create(session=session,jour=requete_form.cleaned_data['jour'],eleve=eleve_potentiel)
    
    elif type == "2":
        
        if eleve_form.is_valid() and requete_form.is_valid():
            for session in requete_form.cleaned_data['session']:
                if requete_form.cleaned_data['creneau']:#On doit vérifier l'existence d'un créneau( que l'utilisateur ait choisit un ou plusieurs) pour utiliser la fonction .set
                
                    requete=Requete.objects.create(session=session,jour=requete_form.cleaned_data['jour'],eleve=eleve_form.cleaned_data['eleve'])
                    requete.creneau.set(requete_form.cleaned_data['creneau'])

                else :
                    Requete.objects.create(session=session,jour=requete_form.cleaned_data['jour'],eleve=eleve_form.cleaned_data['eleve'])
            
    
    if 'end' in request.POST:
            return redirect('/TGA_tool/home.html')
    elif 'submit & add other' in request.POST :
        requete_form=RequeteForm()
        eleve_form=SelectEleveForm()
        eleve_potentiel_form=ElevePotentielForm()
        return render(request, 'TGA_tool/nouvelle-requete.html',locals())
    
    
    return render(request, 'TGA_tool/nouvelle-requete.html', locals())

##################################################################### Paiments ############################################################################
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


"""
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
"""


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