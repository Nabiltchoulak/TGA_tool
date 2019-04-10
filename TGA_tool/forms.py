from django import forms
from TGA_tool.models import *


# Inscription des utilisateurs (famille, parents, élèves, coachs)

class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        fields = '__all__'


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['user', 'famille','solde','debit','credit']
    


class EleveForm(forms.ModelForm): #creation après la famille
    date_naissance = forms.DateField()
    cours=forms.ModelMultipleChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    #Never use the objects.none() if you want to put an empty fieldchoices, juste hide it
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all(),empty_label=None)
    class Meta:
        model = Eleve
        exclude=['user','date_inscription', 'famille','matieres']

class EleveForm2(forms.ModelForm): #creation pour un famille existante
    cours=forms.ModelMultipleChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all(),empty_label=None)
    
    class Meta:
        model = Eleve
        exclude=['user','date_inscription','matieres']

class CoachForm(forms.ModelForm):
    matieres=forms.ModelMultipleChoiceField(queryset=Matiere.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Coach
        exclude = ['disponibilite', 'user','salaire','grade']

# Création du contenu pédagogique

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = '__all__'

class MatiereForm(forms.Form):
    matiere=forms.ModelChoiceField(queryset=Matiere.objects.all(),help_text="Choisir la matiere")

class ChapitreForm(forms.Form):
      chapitre = forms.CharField(max_length=100,required=True)


class NotionForm(forms.Form):
    notion = forms.CharField(max_length=50)
    details=forms.CharField(widget=forms.Textarea,required=False)



# Planification cours / séances
class CoursForm(forms.Form):
    matiere=forms.ModelChoiceField(queryset=Matiere.objects.all())
    coach=forms.ModelChoiceField(queryset=Coach.objects.all(),required=False)

class SeanceForm(forms.ModelForm):
    eleves=forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Seance_Cours
        exclude = ['cours','statut','chapitre','notions']

class SeanceForm2(forms.ModelForm):
    #cours=forms.ModelChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    #notions=forms.ModelMultipleChoiceField(queryset=Notions.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all())
    field_order=('curriculum','cours','date','creneau')
    class Meta:
        
        model = Seance_Cours
        exclude = ['statut','eleves','chapitre','notion']

class Seance_CoursForm(forms.Form):
    seance = forms.ModelChoiceField(queryset=Seance_Cours.objects.all(),help_text='Choisir la séance a éditer') 
    salle = forms.ModelChoiceField(queryset=Salle.objects.all(),help_text='Choisir la salle',required=False)
    #chapitre = forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    #notion=forms.ModelMultipleChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False,widget=forms.CheckboxSelectMultiple)


class FrequenceForm(forms.ModelForm):
    class Meta:
        model = Frequence
        fields = '__all__'
        

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'

class RequeteForm(forms.Form):
    matiere=forms.ModelMultipleChoiceField(queryset=Matiere.objects.all(),help_text="Matieres", widget=forms.CheckboxSelectMultiple)
    #Never use the objects.none() if you want to put an empty fieldchoices, juste hide it
    creneau=forms.ModelMultipleChoiceField(queryset=Creneau.objects.all(),help_text="Créneau",required=False, widget=forms.CheckboxSelectMultiple)
    day_choices=(('Dimanche','Dimanche'),('Lundi','Lundi'),('Mardi','Mardi'),('Mercredi','Mercredi'),('Jeudi','Jeudi'),('Vendredi','Vendredi'),('Samedi','Samedi'),)
    jour=forms.MultipleChoiceField(choices=day_choices,required=False,help_text="Jours", widget=forms.CheckboxSelectMultiple)
class ElevePotentielForm(forms.ModelForm):
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all(),required=False)
    field_order=('curriculum')
    class Meta:
        model =ElevePotentiel
        exclude=['matieres']

#Suivi séances

class ReportSeanceForm(forms.Form):
    """docstring for ReportSeanceForm"""
    eleves = forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),help_text='Cocher les élèves présents', widget=forms.CheckboxSelectMultiple)
    # A afficher avec du Jquerry en fonction du chapitre choisi (donner la possibilité d'ajouter une nouvelle notion au chapitre)
    #chapitre=forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    #notions=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False, widget=forms.CheckboxSelectMultiple)
    rapport = forms.CharField(label='Rapport de séance', max_length = 300, widget=forms.Textarea,required=False)
    """def __init__(self, seance, arg):
        super(ReportSeanceForm, self).__init__()
        self.arg = arg
        self.fields['eleves'].queryset = Eleve.objects.filter(cours= seance.cours.id) # Montrer que les élèves inscrits à la séance"""
        #self.fields['chapitre'].queryset = Chapitre.objects.filter(matiere = seance.cours.matiere.id) # Montrer que les chapitres de la matière de la séance
        #self.fields['notions'].queryset = Notions.objects.filter(chapitre=seance.chapitre.id)  
    """class Meta:
        model = Seance_Cours
        exclude = ['cours']"""

class ReportSeanceCoachingForm(forms.Form):
    """docstring for ReportSeanceForm"""
    eleves = forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),help_text='Cocher les élèves présents', required=True, widget=forms.CheckboxSelectMultiple)
    # A afficher avec du Jquerry en fonction du chapitre choisi (donner la possibilité d'ajouter une nouvelle notion au chapitre)
    #chapitre=forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    #notions=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False, widget=forms.CheckboxSelectMultiple)
    rapport = forms.CharField(label='Rapport de séance', max_length = 300,required=False, widget=forms.Textarea)
    """def __init__(self, seance, arg):
        super(ReportSeanceCoachingForm, self).__init__()
        self.arg = arg
        self.fields['eleves'].queryset = seance.eleve.all() # Montrer que les élèves inscrits à la séance
        self.fields['chapitre'].queryset = Chapitre.objects.filter(matiere = seance.matiere.id) # Montrer que les chapitres de la matière de la séance
        #self.fields['notions'].queryset = Notions.objects.filter(chapitre=seance.chapitre.id)  
    class Meta:
        model = Seance_Coaching
        fields = '__all__'"""

        
class Seance_CoachingForm(forms.ModelForm):
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all())
    #notions=forms.ModelMultipleChoiceField(queryset=Notions.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    field_order=('curriculum','eleve','matiere','coach','date','creneau','salle','chapitre','notions')
    eleve=forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Seance_Coaching
        exclude =['statut','chapitre','notions']


#Suivi paiement 
class PayementForm(forms.ModelForm):
    class Meta:
        model = Payement
        fields = '__all__'


#Connexion
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class SelectEleveForm(forms.Form):
    curriculum=forms.ModelChoiceField(queryset=Curriculum.objects.all(),help_text="Choisir le curriculum")
    eleve=forms.ModelChoiceField(queryset=Eleve.objects.all(),widget=forms.RadioSelect)






"""
class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail", required=True)
"""