from django.shortcuts import render
from .forms import *
# Create your views here.
def acceuil(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)

def parent(request):
    form=ParentForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request,'cours.html',locals())
    