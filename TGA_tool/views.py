from datetime import datetime, date, time
import io
import json
from datetime import timedelta
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.http import (FileResponse, HttpResponse, HttpResponseNotFound,
                         JsonResponse)
from django.http.request import QueryDict
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from reportlab.pdfgen import canvas
from TGA_tool.utils import *
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *

########################################################## Test ###################################################"

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
####################################################### Nouveau : Parent Client ##########################################################""

def nouveauParent(request):
    form = ParentForm(request.POST or None)
    if form.is_valid(): 
        parent = form.save(commit=False)
        if form.cleaned_data["email"]:
                user = User.objects.create_user(form.cleaned_data["email"] , form.cleaned_data["email"] , 'TGA123')

                
        else : 
            user = User.objects.create_user(form.cleaned_data["prenom"]  ,form.cleaned_data["prenom"],  'TGA123')
        user.last_name = form.cleaned_data["nom"]
        clients_group = Group.objects.get(name='Parents') 
        clients_group.user_set.add(user)
        user.save
        parent.user=user
        #Création automatique de la famille 
        if len(Famille.objects.filter(nom=parent.nom))>0 and len(Famille.objects.filter(adresse=form.cleaned_data["adresse"]))>0 :
            nom=parent.nom+" "+str(len(Famille.objects.filter(nom=parent.nom))+1)
        famille=Famille.objects.create(nom=form.cleaned_data["nom"], adresse=form.cleaned_data["adresse"])
        id=famille.id
        parent.famille=famille
        parent.save()
        form.save_m2m()
        try:# Vérifier si ce parent est un eleve potentiel déjà 
            ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
        except ObjectDoesNotExist:
            
            if 'end' in request.POST :#test if the user choosed "submit" 
                return redirect(nouveauEleve, id) #renvoyer vers le formulaire d'ajout d'élèves avec l'id famille en paramétre
            elif 'submit & add other' in request.POST :#or "submit && add" 
                form=ParentForm()#Vider le formulaire 
            return render(request,'TGA_tool/nouveau-parent.html', locals())
        
        #Si c'est le cas prendre la liste de cours qu'il a demandé transférer les requetes de l'eleve poentiel au parent et suprimer les requetes accomplies et l'eleve potentiel
        
        ###############*******
        parent_potentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
        
        #Dans toutes les requetes changer de l'eleve au parent pour transferer les requetes restantes 
        
        if parent_potentiel.sessions:
            
            requetes=Requete.objects.filter(eleve=parent_potentiel)
            for requete in requetes:
                requete.eleve= None
                requete.parent=parent
                requete.save()
        parent.save()

        #Supprimer toutes les requetes qui contiennent les cours qui ont été choisit 

        for cours in form.cleaned_data["cours"] :
                
                if Requete.objects.filter(parent=parent).filter(session=cours.session):
                    requete=Requete.objects.filter(parent=parent).filter(session=cours.session)
                    requete.delete()
        
        #supprimer l'élève potentiel 

        parent_potentiel.delete()
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
            parent.save()

        else :#Crer le user du nouveau client et créer le client 
            client=form.save()
            if form.cleaned_data["email"]:
                user = User.objects.create_user(form.cleaned_data["email"] , form.cleaned_data["email"] , 'TGA123')

                
            else : 
                user = User.objects.create_user(form.cleaned_data["prenom"]  ,form.cleaned_data["prenom"],  'TGA123')
            user.last_name = form.cleaned_data["nom"]
            clients_group = Group.objects.get(name='Clients') 
            clients_group.user_set.add(user)
            user.save
            client.user=user
        
        #Le reste (ce qui vient en dessous) est commun pour les deux cas ( client parent ou pas )
        client.date_commencement=date.today()
        
        #essayer si ce client était déjà un client potentiel
        try:# Vérifier si ce client est un client potentiel déjà 
            ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["telephone"])
        except ObjectDoesNotExist:
            
            client.save()
            
            
            if 'end' in request.POST :#test if the user choosed "submit" 
                client.save()
                
                if form.cleaned_data["cours"]:
                    print(form.cleaned_data["cours"])
                    return redirect(makePayement,client.id)
                else :
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
                requete.parent=client.parent_ptr
                requete.save()
        client.save()

        #Supprimer toutes les requetes qui contiennent les cours qui ont été choisit 

        for cours in form.cleaned_data["cours"] :
                
                if Requete.objects.filter(parent=client.parent_ptr).filter(session=cours.session):
                    requete=Requete.objects.filter(parent=client.parent_ptr).filter(session=cours.session)
                    requete.delete()
        
        #supprimer l'élève potentiel 

        client_potentiel.delete()
        ###############**********

        if 'end' in request.POST :#test if the user choosed "submit" 
            client.save()
            if form.cleaned_data["cours"]:
                
                return redirect(makePayement,client.id)
            else :
                return render(request,'TGA_tool/home.html')
        elif 'submit & add other' in request.POST :#or "submit && add" 
            form=ClientForm() #Vider le formulaire
    return render(request, 'TGA_tool/newClient.html', locals())

############################################################### Eleve ############################################################################
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




def nouveauEleve(request, id=0):
    
    if id>0:
        
        form = EleveForm(request.POST or None)
        famille = True 
        
        if form.is_valid(): 
            
            eleve = form.save(commit=False)
            eleve.famille = Famille.objects.get(id=id)
            try:
                ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["num"])
            except ObjectDoesNotExist:
                eleve = form.save()
                form.save_m2m()
                #Si cet élève était un élève potentiel déja on le lie avec l'instance de l'élève potentiel
                #et on garde les autres requetes si il y'en a, on suprime la requete qui correspon a son cours si c'est elle 
            elevepotentiel=ElevePotentiel.objects.get(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"],num=form.cleaned_data["num"])
            #Ici on gére le cas ou deux eleves ont le meme nom 
            #eleve=form.save(commit=False)
            eleve.elevepotentiel_ptr=elevepotentiel
            #Il se peut que les coordonés prises quand l'elève s'est présenté aient changés 
                
            eleve.elevepotentiel_ptr.email=form.cleaned_data["email"]
            eleve.elevepotentiel_ptr.num=form.cleaned_data["num"]
            #print(eleve)
            eleve.save()
            elevepotentiel.save()
            form.save_m2m()
            for cours in form.cleaned_data["cours"] :
                    
                if Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session):
                    requete=Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session)
                    requete.delete()
            for ptr in eleve.famille.parent_set.filter(estResponsable=True) :
                parent=ptr.id
            if 'end' in request.POST :#test if the user choosed "submit" 
                if form.cleaned_data["cours"]:
                    return redirect(makePayement,parent)
                else :
                    return render(request,'TGA_tool/home.html')
            elif 'add cours' in request.POST :
                return redirect(choose_extra_courses,eleve.id)
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
            eleve.elevepotentiel_ptr.num=form.cleaned_data["num"]
            eleve.save()
            elevepotentiel.save()
            form.save_m2m()
            for cours in form.cleaned_data["cours"] :
                    
                if Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session):
                    requete=Requete.objects.filter(eleve=elevepotentiel).filter(session=cours.session)
                    requete.delete()
            for ptr in eleve.famille.parent_set.filter(estResponsable=True) :
                parent=ptr.id
            if 'end' in request.POST :#test if the user choosed "submit" 
                if form.cleaned_data["cours"]:
                    return redirect(makePayement,parent)
                else :
                    return render(request,'TGA_tool/home.html')
            elif 'add cours' in request.POST :
                return redirect(choose_extra_courses,eleve.id)
            elif 'submit & add other' in request.POST :#or "submit && add" 
                form=EleveForm()#Vider le formulaire 
                return render(request,'TGA_tool/nouveau-eleve.html', locals())
    return render(request,'TGA_tool/nouveau-eleve.html', locals())	

def ChooseEleve(request):
    extra=True
    already_in=True
    form=SelectEleveForm(request.POST or None)
    if form.is_valid():
        eleve=form.cleaned_data["eleve"]
        return redirect(choose_extra_courses,eleve.id)
    return render(request,'TGA_tool/nouveau-eleve.html', locals())

def choose_extra_courses(request,id):
    extra=True
    client=False
    form=ChooseCoursForm(request.POST or None)
    
    print(form.errors)
    if form.is_valid():
        parent=0
        try :
            eleve=Eleve.objects.get(id=id)
        except ObjectDoesNotExist:
            eleve=Client.objects.get(id=id)
            client=True
            
        if not client :
            for par in eleve.famille.parent_set.filter(estResponsable=True):
                parent=par.id
                print(parent)
       
        for cours in form.cleaned_data["cours"]:
            eleve.cours.add(cours)
        eleve.save()
        print(eleve)
        
        if 'end' in request.POST :#test if the user choosed "submit" 
                if client :
                    return redirect(makePayement,eleve.id)
                else: 
                    
                    return redirect(makePayement,parent)
        elif 'submit & add other' in request.POST :#or "submit && add" 
                form=ChooseCoursForm()#Vider le formulaire 
                return render(request,'TGA_tool/nouveau-eleve.html', locals())

    return render(request,'TGA_tool/nouveau-eleve.html', locals())	



###############################################################"Coach ############################################################################
def nouveauCoach(request):
    form = CoachForm(request.POST or None)
    if form.is_valid(): 
        #Création de l'utilisateur 
        user = User.objects.create_user(form.cleaned_data["prenom"], form.cleaned_data["email"] , 'TGA123')
        user.last_name = form.cleaned_data["nom"]
        user.save
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


######################################################### Connexion/deconnexion #################################################################""

def connexion(request):
    error = False
    first_time=False
    change=False
    
    form = ConnexionForm(request.POST or None)
    password_form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
        if user is not None:  # Si l'objet renvoyé n'est pas None
            if user.last_login == None :
                login(request, user)  # nous connectons l'utilisateur
                change=True
        
            else :
                login(request, user)  
                return redirect('home.html')
        else : 
            error = True # sinon une erreur sera affichée
    elif password_form.is_valid():
            password_form.save()
            first_time=True
            change=False
            update_session_auth_hash(request, password_form.user)
    print(password_form.errors)
            
    
    
    return render(request, 'TGA_tool/login-coach.html', locals())

def deconnexion(request):
    logout(request)
    return redirect("connexion")


############################################################# Nouveau cours ##################################################################


def nouveauCours(request,choice):
    exist=True
    many=False
    number=0
    frequency_form=FrequenceForm(request.POST or None)
    if choice=="VIP":
        cours_form=VIPCoursForm(request.POST or None)
    else :
        cours_form=CoursForm(request.POST or None)
    
    if cours_form.is_valid() and frequency_form.is_valid():
        frequence=frequency_form.save()
        session=cours_form.cleaned_data['session']
        try :
            Cours.objects.get(langue=session.langue,session=session,coach=cours_form.cleaned_data['coach'])
        
        except ObjectDoesNotExist :
            exist=False
            

        except MultipleObjectsReturned :
            
            many=True
            cours=Cours.objects.filter(langue=session.langue,session=session,coach=cours_form.cleaned_data['coach'])
            number=len(cours)


        
        if exist and not many:
            Cours.objects.create(langue=session.langue,session=session,coach=cours_form.cleaned_data['coach'],frequence=frequence,match_indic=" 1 ")
            
           
        elif not exist :    
            Cours.objects.create(langue=session.langue,session=session,coach=cours_form.cleaned_data['coach'],frequence=frequence)
            
        elif many :
            print(number)
            indic=" " + str(number) + " "
            print(indic)
            Cours.objects.create(langue=session.langue,session=session,coach=cours_form.cleaned_data['coach'],frequence=frequence,match_indic=indic)


            
        #Cette partie concerne le traitement du type de la réponse 
        if 'end' in request.POST:

            return redirect('/TGA_tool/home.html')
        elif 'submit & add other' in request.POST :
            frequency_form=FrequenceForm()
            cours_form=CoursForm()#Vider les formulaires
            return render(request, 'TGA_tool/nouveau-cours.html',locals())
    return render(request, 'TGA_tool/nouveau-cours.html',locals())


def ajaxNewCours(request):
    # Cette fonction n'est pas dans la fonction nouveauEleve par ce que je n'ai pas trrouvé comment envoyer un post a un url 
    # qui contient un id sans affecter l'id (j'avais toujours id=0)
    if 'langue_id' in list(request.POST.keys()):
        form = CoursForm(request.POST or None)
        id_2=int(request.POST['langue_id'])
        langue= Langue.objects.get(id=id_2)
        form.fields['session'].queryset=Session.objects.filter(langue=langue)
        data=[]
        data=form["session"]
        
        return HttpResponse(str(data))



############################################################### Cours du coach #####################################
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


########################################################## Home Calendar mes séances ###################################################################
# Create your views here.
def home(request):
    return render(request, 'TGA_tool/home.html')

def calendar(request):
    return render(request,'TGA_tool/calendar.html')


def mesSeances(request):
    checker=""
    vip=""#remplir cette var avec VIP si le cours est de type vip
    parents_group = Group.objects.get(name='Parents') 
    clients_group = Group.objects.get(name='Clients') 
    if parents_group in request.user.groups.all():
        group="Parents"
        checker="A"
            
    if clients_group in request.user.groups.all():
        group="Clients"
        checker+="A"
    
    listeseances =[]

    if request.user.is_staff == 0 :
        
        #coach = Coach.objects.get(user = id)
        client= request.user.parent
        if group=="Clients" or checker=="AA":
            cours = Cours.objects.filter(Client_cours=client)

            
            for cour in cours:
                if cour.vip :
                    vip = " VIP "#ce cours est vip
                seances = Seance_Cours.objects.filter(cours = cour.id)
                
                for seance in seances:
                    
                    #listeseances.append({'id': seance.id, 'langue': seance.cours.session.langue.langue, 'session': seance.cours.session.session, 'date' : str(seance.date), 'start' : str(seance.creneau.debut)})       
                    listeseances.append({'title': str(seance.cours) + vip + " - "  + str(client.genre) + str(client.prenom) + " - " + str(seance.statut),
                                        'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "displayseance.html/" + str(seance.id)})



        if group=="Parents" or checker=="AA":
            seances_eleve={}
            for eleve in client.famille.eleve_set.all():
                for cour in Cours.objects.filter(Eleve_cours=eleve) :
                    if cour.vip :
                        vip = " VIP "#Ajouter une variable
                    seances = Seance_Cours.objects.filter(cours = cour.id)
                
                    for seance in seances:
                        listeseances.append({'title': str(seance.cours) + vip + " - "  + str(eleve.prenom) + " - " + str(seance.statut),
                                        'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "displayseance.html/" + str(seance.id)})
                    vip=""

        
        
    
    
    elif request.user.is_staff == 1 : #User staff can see all séances and corses 
        cours=Cours.objects.all()
        coachings=Seance_Coaching.objects.all()
        
        if coachings :
            for seance in coachings:
                listeseances.append({'title': "Coaching " + seance.session.langue.langue  + " - " + seance.session.session + " - " + str(seance.coach) + " - " + str(seance.statut), 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "display-seance-coaching.html/" + str(seance.id)})
        
        
        for cour in cours:
            seances = Seance_Cours.objects.filter(cours = cour.id)
            if cour.vip==1 :
                vip = " VIP "#Ajouter une variable
            for seance in seances:
                #listeseances.append({'id': seance.id, 'langue': seance.cours.session.langue.langue, 'session': seance.cours.session.session, 'date' : str(seance.date), 'start' : str(seance.creneau.debut)})       
                listeseances.append({'title':  str(seance.cours) + vip + " - "   + str(cour.coach) + " - " + str(seance.statut), 
                    'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "displayseance.html/" + str(seance.id)})
            vip=""
    #Cette partie va récupérer les seances de coaching 
    """coachings=Seance_Coaching.objects.filter(coach= coach.id)
    for seance in coachings:
        listeseances.append({'title': "Coaching " + seance.session.langue.langue + " - " + seance.session.session, 
                'start' : str(seance.date)+"T"+str(seance.creneau.debut), 'url' : "display-seance-coaching.html/" + str(seance.id)})"""
    
    data = listeseances

    return JsonResponse(data, safe=False)


############################################################### Display Seance ########################################################

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
    session = seance.cours.session
    #chapitre = seance.chapitre
    #notions = seance.notions
    eleves = Eleve.objects.filter(cours=seance.cours.id)
    clients= Client.objects.filter(cours=seance.cours.id)
    statut = seance.statut
    if statut == "Effectué":
        eleves_presents=seance.eleves.all()
        clients_presents=seance.clients.all()
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

############################################################### Annuler séance ###############################################################################

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


############################################################### Modifier seance #############################################################################

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

############################################################## Déclaration des séances ###################################################################

def declarerSeance(request,id):
    seance = Seance_Cours.objects.get(id = id)
    seance_id =seance.id
    date_seance = str(seance.date)
    heure_seance = str(seance.creneau.debut)
    salle_seance =  seance.salle
    session = seance.cours.session.session
    #chapitre = seance.chapitre
    #notions = seance.notions.all()
    
    
    statut = seance.statut

    # Renseigner le chapitre et notions vues dans le cours

    # déclarer les élèves présents
        # recupérer les éleves cochés présents
    form = ReportSeanceForm(request.POST or None)
    form.fields['eleves'].queryset=Eleve.objects.filter(cours= seance.cours.id)
    form.fields['clients'].queryset=Client.objects.filter(cours=seance.cours.id)
    if form.is_valid():
        
        seance.statut="Effectué"
        eleves=form.cleaned_data['eleves']
        clients=form.cleaned_data['clients']
        seance.eleves.set(eleves)
        seance.clients.set(clients)
        for eleve in eleves :
                parent=Parent.objects.filter(estResponsable=True).get(famille=eleve.famille)
                print(parent)
                parent.debit-=1000
                parent.solde-=1000
                parent.save()
        coach=seance.cours.coach        
        coach.salaire+=1000
        coach.save()
        seance.save()
        return redirect('/TGA_tool/home.html')
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
        seance.statut="Effectué"
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


####################################################### Création de séances cours/coaching ###############################################################


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


########################################################### Session + chapitre + notions ##################################################################
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





############################################################# Initial data #########################################################################


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

############################################################ Tableau de bord ###########################################################

def presence_checker(request):#A l'aide de cette fonction nous allons renvoyer un tableau pour colorer les cases de présence 
    
    data={}
    ids=[int(x) for x in request.POST.getlist('cours_id[]')]
    
    courss=Cours.objects.filter(id__in=ids)
    if 'eleve_id' in request.POST :
        eleve=Eleve.objects.get(id=int(request.POST['eleve_id']))
        for cours in courss:
            tab=[]
            
            for seance in cours.get_seances() :
                
                if eleve in seance.eleves.all():
                    tab.append("1")
                elif seance.statut=="Effectué":
                    tab.append("2")
                else :
                    tab.append("0")
                    
            
            data[str(cours)]=tab
            
            del tab
    elif 'client_id' in request.POST :
        client=Client.objects.get(id=int(request.POST['client_id']))
        for cours in courss:
            tab=[]
            
            for seance in cours.get_seances() :
                
                if client in seance.clients.all():
                    tab.append("1")
                elif seance.statut=="Effectué":
                    tab.append("2")
                else :
                    tab.append("0")
                    
            
            data[str(cours)]=tab
            
            del tab
    
    return JsonResponse(data, safe=False)

def display(request,type):
    checker=""
    parents_group = Group.objects.get(name='Parents') 
    clients_group = Group.objects.get(name='Clients') 
    if parents_group in request.user.groups.all():
        group="Parents"
        checker="A"
            
    if clients_group in request.user.groups.all():
        group="Clients"
        checker+="A"

    if type=="1":
        print(group)
        if group== "Clients" or checker == "AA" :
            seances=Seance_Cours.objects.filter(clients=request.user.parent)
            client=request.user.parent.client
        seances_kids={}
        if group== "parents" or checker == "AA":
            kids=request.user.parent.famille.eleve_set.all()
            
            
        

    elif type=="2":
        parents=Parent.objects.filter(estResponsable=True)
        #Cette partie est utile si l'utilisateur veut contacter les parents
        #Si la personne responsable ne répond pas on va vers le parent contact qui va 
        #se trouver dans les détails de famille 
    elif type=="3":
        eleves=Eleve.objects.all()
    elif type=="4":
        
        client=Parent.objects.get(id=request.user.parent.id)
        paiements=Payement.objects.filter(parent=client)
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
        requetes=Prospect_courses.objects.filter(date_fin__gte=date.today())
    
    elif type=="9":
        clients=Client.objects.all()
    elif type=="10":
        requetes=Requete.objects.filter(prospect_courses__isnull=True)
    
    return render(request,'TGA_tool/display.html', locals())

def details(request,type,id):
    

    if type=="5" :
        coach=Coach.objects.get(id=id)
        cours=Cours.objects.filter(coach=coach)
        listSeancesEnseigne=[]
        listSeancesRestant=[]
        for cour in cours:
            seances_done = Seance_Cours.objects.filter(cours = cour.id).filter(statut="Effectué")
            seances_planifie= Seance_Cours.objects.filter(cours = cour.id).filter(statut="Planifié")
            listSeancesEnseigne.append(seances_done)
            listSeancesRestant.append(seances_planifie)    
        listSeancesEnseigne.append(Seance_Coaching.objects.filter(coach = coach.id).filter(statut="Effectué"))
        listSeancesRestant.append(Seance_Coaching.objects.filter(coach = coach.id).filter(statut="Planifié"))
        print(listSeancesEnseigne)
        print(listSeancesRestant)
        sancesDone=len(listSeancesEnseigne)
        seancesRestant=len(listSeancesRestant)

    elif type =="1":
        requete=Requete.objects.get(id=id)
        
        dates=DateCreneau.objects.filter(requete=requete)
        print(dates)

    return render(request,'TGA_tool/details.html', locals())    


############################################################### Requete #####################################################

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


def new_requete(request,type,id=0,requete_ids=0):#1 pour une requete externe / 2 pour une requete interne 
    
    ### les formulaires 
    
    eleve_form=SelectEleveForm(request.POST or None)
    eleve_potentiel_form=ElevePotentielForm(request.POST or None)
    
    
    
    
    print(id)
    if type == "1": #Requete externe        
        ind=True#Pour éviter la création de plusieurs instances de eleve potentiel
        if eleve_potentiel_form.is_valid():
            if ind: 
                eleve_potentiel=eleve_potentiel_form.save()
                ind=False
            if 'end' in request.POST:
                id=eleve_potentiel.id
                return redirect(choose_sessions,id,"eleve")
    
    
    elif type == "2":#requete interne en choisisant l'eleve
        
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


def choose_sessions(request,id=0,demandeur="") :
    
    if id > 0 :
        type="step2"
        requete_form=RequeteForm(request.POST or None)
        requetes=[] 
        print(demandeur)
        print(requete_form.errors)        
        if requete_form.is_valid() :
            if demandeur == "eleve" :
                eleve_pot = ElevePotentiel.objects.get(id=id) 
            else :
                client = Client.objects.get(id=id)
            print("verifya")
            for session in requete_form.cleaned_data['session']:
                if demandeur=="eleve" :
                    requete=Requete.objects.create(session=session,eleve=eleve_pot)  
                else :
                    requete=Requete.objects.create(session=session,parent=client.parent_ptr)
                requetes.append(str(requete.id))#Remplir la liste de requetes a transmettre 
                requete.save()

            if 'end' in request.POST:
                response = HttpResponseRedirect(reverse('choose creneaux'))#La vue suivantes qui contient les créneaux 
                response['Location'] += '/' + '&'.join(['requetes={}'.format(x) for x in requetes])#Ajouter les ids des requetes crées 
                
                return response
            elif 'submit & add other' in request.POST :
                requete_form=RequeteForm()
                return redirect(choose_sessions,id)

    return render(request, 'TGA_tool/nouvelle-requete.html', locals())

def choose_creneaux(request,requetes=[]):

    
    parts=request.path.split('/')#Prendre la partie dernière de la requete 
    
    requetes=QueryDict(parts[3]).getlist('requetes')#Créer le querydict des ids envoyées a partir de la requete


    
        
    type = "step3"
    date_creneau_form=DateCreneauRequeteForm(request.POST or None)
    date_creneau_form.errors
    if date_creneau_form.is_valid():
        for id in requetes :
            requete=Requete.objects.get(id=int(id))
            date_creneau=date_creneau_form.save(commit=False)
            date_creneau.requete=requete 
            date_creneau.save()
            date_creneau_form.save_m2m()
        
        if 'end' in request.POST:
            return redirect('/TGA_tool/home.html')

        elif 'submit & add other' in request.POST :
            date_creneau_form=DateCreneauRequeteForm()
            
    return render(request, 'TGA_tool/nouvelle-requete.html', locals())


######################################################## Prospect courses ##################################################################################

def new_prospect_cours(request):
    eleve=True
    parent=True
    form=ProspectForm(request.POST or None)
    eleve_form=ElevePotentielForm(request.POST or None)
    if eleve_form.is_valid() and form.is_valid():
        try :
            ElevePotentiel.objects.get(nom=eleve_form.cleaned_data['nom'],prenom=eleve_form.cleaned_data['prenom'],num=eleve_form.cleaned_data['num'])
        except ObjectDoesNotExist :
            eleve=False
        try :
            Parent.objects.get(nom=eleve_form.cleaned_data['nom'],prenom=eleve_form.cleaned_data['prenom'],telephone=eleve_form.cleaned_data['num'])
        except ObjectDoesNotExist :
            parent=False
        if eleve ==False and parent==False :
            eleve_potentiel=eleve_potentiel_form.save()
            for session in form.cleaned_data['session']:
                Prospect_courses.objects.create(session=session,date_fin=form.cleaned_data['date_fin'],eleve=eleve_potentiel) 
        elif parent :
            parent=Parent.objects.get(nom=eleve_form.cleaned_data['nom'],prenom=eleve_form.cleaned_data['prenom'],telephone=eleve_form.cleaned_data['num'])
            for session in form.cleaned_data['session']:
                
                Prospect_courses.objects.create(session=session,date_fin=form.cleaned_data['date_fin'],parent=parent)
        elif eleve :
            eleve=Eleve.objects.get(nom=eleve_form.cleaned_data['nom'],prenom=eleve_form.cleaned_data['prenom'],num=eleve_form.cleaned_data['num'])
            for session in form.cleaned_data['session']:
                Prospect_courses.objects.create(session=session,date_fin=form.cleaned_data['date_fin'],eleve=eleve)
        if 'end' in request.POST:
            return redirect('/TGA_tool/home.html')
        elif 'submit & add other' in request.POST :
            form=ProspectForm()
            eleve_form=ElevePotentielForm()
       
    
    return render(request, 'TGA_tool/new_prospect.html', locals())

############################################################## Paiments ############################################################################
def makePayement(request,id):
    form = PayementForm(request.POST or None)
    if form.is_valid():
        payement = form.save(commit=False)
        payement.date=datetime.now()
        parent=Parent.objects.get(id=id)
        payement.parent=parent
        payement.save()
        
        
        montant= form.cleaned_data['montant']
        
        parent.credit+=montant
        parent.solde+=montant
        parent.save()
        
        if "did_paid" in request.POST:
            paid=True
        
        return render(request, 'TGA_tool/make-payement.html', locals())


    return render(request, 'TGA_tool/make-payement.html', locals())



###############################################################Utils ##############################################################################"


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
