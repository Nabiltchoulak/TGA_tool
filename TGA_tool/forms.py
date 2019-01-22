from django import forms
from TGA_tool.models import *


class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail", required=True)

class ChapitreForm(forms.Form):
      chapitre = forms.CharField(max_length=100,required=True)

class NotionForm(forms.Form):
    notion = forms.CharField(max_length=50)
    details=forms.CharField(widget=forms.Textarea,required=False)

class CoursForm(forms.Form):
    matiere=forms.ModelChoiceField(queryset=Matiere.objects.all())
    coach=forms.ModelChoiceField(queryset=Coach.objects.all(),required=False)


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['user', 'famille']
    

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        exclude=['user','date_inscription', 'famille']

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        exclude = ['disponibilite', 'user']

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = '__all__'

class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        fields = '__all__'
    

class Seance_CoursForm(forms.Form):
    seance = forms.ModelChoiceField(queryset=Seance_Cours.objects.all(),help_text='Choisir la séance a éditer') 
    salle = forms.ModelChoiceField(queryset=Salle.objects.all(),help_text='Choisir la salle',required=False)
    chapitre = forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    notion=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False)


class Seance_CoachingForm(forms.ModelForm):
    class Meta:
        model = Seance_Coaching
        fields = '__all__'

class MatiereForm(forms.Form):
    matiere=forms.ModelChoiceField(queryset=Matiere.objects.all(),help_text="Choisir la matiere")

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'

class FrequenceForm(forms.ModelForm):
    class Meta:
        model = Frequence
        fields = '__all__'

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)