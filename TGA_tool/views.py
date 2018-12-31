from django.shortcuts import render,redirect
from .forms import *
from django.views.generic import TemplateView
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.urls import reverse
from urllib.parse import urlencode

# Create your views here.

# Create your views here.
def calendar(request):
    return render(request,'TGA_tool/calendar/calendar.html')

    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request,'TGA_tool/nouveau-eleve.html', locals())	


def nouveauParent(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ParentForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        
        form.save()

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'TGA_tool/nouveau-parent.html', locals())	

def nouveauCoach(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = CoachForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        
        form.save()

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'TGA_tool/nouveau-coach.html', locals())	

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
        while form.cleaned_data['chapitre'] == None or form.cleaned_data['salle']==None or form.cleaned_data['notion']==None :
            form.fields['chapitre'].queryset=Chapitre.objects.filter(matiere=seance.cours.matiere)
            #chapitre=form.cleaned_data['chapitre']
            form.fields['notion'].queryset=Notions.objects.filter(chapitre=form.cleaned_data['chapitre'])
            print(seance.pk)
            return render(request,'TGA_tool/modifier-seance_cours.html', locals())
            #print(notion)
            
        seance.salle=form.cleaned_data['salle']
        seance.chapitre=form.cleaned_data['chapitre']
        seance.notion=form.cleaned_data['notion']
        
        if seance.notion != None :
            return render(request,'TGA_tool/home.html', locals())
            print(seance)
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
            """base_url = reverse(nouveauEleve)
            query_string =  urlencode({'ids': ids})  
            url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42"""
            return redirect(nouveauEleve,args=ids)   
    return render(request, 'TGA_tool/eleve-arrive.html',locals())

def nouveauEleve(request,ids):
    #print(request.GET.get('ids'))
    print(request.GET)
    """
    form = EleveForm(request.POST or None)
    if form.is_valid(): 
        eleve=form.save(commit=False)
        eleve.parent_resp=Parent.objects.get(id=ids[0])
        eleve.parent_sec=Parent.objects.get(id=ids[1])
        eleve.save()
        form.save_m2m()
        if 'end' in request.POST :#test if the user choosed "submit" 
            return render(request,'TGA_tool/home.html')
        elif 'submit & add other' in request.POST :#or "submit && add" 
            form=EleveForm()#Vider le formulaire 
            return render(request,'TGA_tool/nouveau-eleve.html', locals())"""
    return render(request, 'TGA_tool/nouveau-eleve.html',locals())