from django.shortcuts import render
from .forms import *
# Create your views here.

# Create your views here.
def home(request):
    return render(request, 'TGA_tool/home.html')

def calendar(request):
    return render(request,'TGA_tool/calendar/calendar.html')
def nouveauEleve(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = EleveForm(request.POST or None)
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