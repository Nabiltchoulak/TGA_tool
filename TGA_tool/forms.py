from django import forms
from TGA_tool.models import Parent,Eleve,Cours,Seance,Coach,Salle,Chapitre,Notions,Matiere,Frequence,Creneau,Curriculum

class CoursForm(forms.Form):
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all())
    matiere=forms.ModelChoiceField(queryset=Matiere.objects.all())
    coach=forms.ModelChoiceField(queryset=Coach.objects.all())
    frequence=forms.ModelChoiceField(queryset=Frequence.objects.all())

