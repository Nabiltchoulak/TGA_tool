from django.shortcuts import render
from .forms import *
# Create your views here.
def acceuil(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)

def cours(request):
    form=CoursForm(request.POST or None)
    if form.is_valid():
        curriculum=form.cleaned_data.get('curriculum')
        matiere=form.cleaned_data.get('matiere')
        coach=form.cleaned_data['coach']
        frequence=form.cleaned_data['frequence']
    return render(request,'cours.html',locals())