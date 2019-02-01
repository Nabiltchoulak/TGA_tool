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
    


class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance_Cours
        exclude = ['cours']


class PayementForm(forms.ModelForm):
    class Meta:
        model = Payement
        fields = '__all__'

class Seance_CoursForm(forms.Form):
    seance = forms.ModelChoiceField(queryset=Seance_Cours.objects.all(),help_text='Choisir la séance a éditer') 
    salle = forms.ModelChoiceField(queryset=Salle.objects.all(),help_text='Choisir la salle',required=False)
    chapitre = forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    notion=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False)

"""
class ReportSeanceForm(forms.Form):
    salle = forms.ModelChoiceField(queryset=Salle.objects.all(),help_text='Choisir la salle',required=False)
    chapitre = forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    notions=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False, widget=forms.CheckboxSelectMultiple)
    eleves = forms.ModelChoiceField(queryset=Eleve.objects.all(),help_text='Cocher les élèves présents', required=True, widget=forms.CheckboxSelectMultiple)
    rapport = forms.CharField(label='Rapport de séance', max_length = 300, widget=forms.Textarea)
"""

class ReportSeanceForm(forms.ModelForm):
    """docstring for ReportSeanceForm"""
    eleves = forms.ModelChoiceField(queryset=Eleve.objects.all(),help_text='Cocher les élèves présents', required=True, widget=forms.CheckboxSelectMultiple)
    # A afficher avec du Jquerry en fonction du chapitre choisi (donner la possibilité d'ajouter une nouvelle notion au chapitre)
    notions=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False, widget=forms.CheckboxSelectMultiple)
    rapport = forms.CharField(label='Rapport de séance', max_length = 300, widget=forms.Textarea)
    def __init__(self, seance, arg):
        super(ReportSeanceForm, self).__init__()
        self.arg = arg
        self.fields['eleves'].queryset = Eleve.objects.filter(cours= seance.cours.id) # Montrer que les élèves inscrits à la séance
        self.fields['chapitre'].queryset = Chapitre.objects.filter(matiere = seance.cours.matiere.id) # Montrer que les chapitres de la matière de la séance
        #self.fields['notions'].queryset = Notions.objects.filter(chapitre=seance.chapitre.id)  
    class Meta:
        model = Seance_Cours
        exclude = ['cours']

        
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