from django import forms
from TGA_tool.models import *


# Inscription des utilisateurs (famille, parents, élèves, coachs)

class ClientForm(forms.ModelForm):
    cours=forms.ModelMultipleChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
    langue=langue=forms.ModelChoiceField(queryset=Langue.objects.all())
    class Meta:
        model = Client
        exclude=['famille','solde','debit','credit','estResponsable','date_commencement','sessions','user']

class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        fields = '__all__'


class ParentForm(forms.ModelForm):
    adresse=forms.CharField( max_length=100, required=False)
    class Meta:
        model = Parent
        exclude = ['user', 'famille','solde','debit','credit']
    


class EleveForm(forms.ModelForm): #creation après la famille
    date_naissance = forms.DateField()
    cours=forms.ModelMultipleChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    #Never use the objects.none() if you want to put an empty fieldchoices, juste hide it
    langue=forms.ModelChoiceField(queryset=Langue.objects.all(),empty_label=None)
    class Meta:
        model = Eleve
        exclude=['user','date_inscription', 'famille','sessions']

class EleveForm2(forms.ModelForm): #creation pour un famille existante
    cours=forms.ModelMultipleChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    langue=forms.ModelChoiceField(queryset=Langue.objects.all(),empty_label=None)
    
    class Meta:
        model = Eleve
        exclude=['user','date_inscription','sessions']

class CoachForm(forms.ModelForm):
    
    class Meta:
        model = Coach
        exclude = ['disponibilite', 'user','salaire']

# Création du contenu pédagogique

class LangueForm(forms.ModelForm):
    class Meta:
        model = Langue
        fields = '__all__'

class SessionForm(forms.Form):
    session=forms.ModelChoiceField(queryset=Session.objects.all(),help_text="Choisir la session")

class ChapitreForm(forms.Form):
      chapitre = forms.CharField(max_length=100,required=True)


class NotionForm(forms.Form):
    notion = forms.CharField(max_length=50)
    details=forms.CharField(widget=forms.Textarea,required=False)



# Planification cours / séances
class CoursForm(forms.Form):
    langue=forms.ModelChoiceField(queryset=Langue.objects.all())
    session=forms.ModelChoiceField(queryset=Session.objects.all(),widget=forms.RadioSelect)
    coach=forms.ModelChoiceField(queryset=Coach.objects.all(),required=False)

class VIPCoursForm(CoursForm):
    client=forms.ModelChoiceField(queryset=Client.objects.all(),required=False,widget=forms.RadioSelect)
    eleve=forms.ModelChoiceField(queryset=Eleve.objects.all(),required=False,widget=forms.RadioSelect)

class ChooseCoursForm(forms.Form):
    langue=forms.ModelChoiceField(queryset=Langue.objects.all())
    cours=forms.ModelMultipleChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    

class SeanceForm(forms.ModelForm):
    eleves=forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Seance_Cours
        exclude = ['cours','statut','chapitre','notions']

class SeanceForm2(forms.ModelForm):
    #cours=forms.ModelChoiceField(queryset=Cours.objects.all(),widget=forms.CheckboxSelectMultiple)
    #notions=forms.ModelMultipleChoiceField(queryset=Notions.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    
    langue=forms.ModelChoiceField(queryset=Langue.objects.all())
    field_order=('langue','cours','date','creneau')
    class Meta:
        
        model = Seance_Cours
        exclude = ['statut','eleves','chapitre','notion']

class FrequenceForm(forms.ModelForm):
    class Meta:
        model = Frequence
        fields = '__all__'
        

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'

class RequeteForm(forms.Form):
    
    langue=forms.ModelChoiceField(queryset=Langue.objects.all(),required=False)
    
    session=forms.ModelMultipleChoiceField(queryset=Session.objects.all(), widget=forms.CheckboxSelectMultiple)
    #Never use the objects.none() if you want to put an empty fieldchoices, juste hide it
    #creneau=forms.ModelMultipleChoiceField(queryset=Creneau.objects.all(),help_text="Créneau",required=False, widget=forms.CheckboxSelectMultiple)
    #day_choices=(('Dimanche','Dimanche'),('Lundi','Lundi'),('Mardi','Mardi'),('Mercredi','Mercredi'),('Jeudi','Jeudi'),('Vendredi','Vendredi'),('Samedi','Samedi'),)
    #jour=forms.MultipleChoiceField(choices=day_choices,required=False,help_text="Jours", widget=forms.CheckboxSelectMultiple)

class DateCreneauRequeteForm(forms.ModelForm):
    creneau=forms.ModelMultipleChoiceField(queryset=Creneau.objects.all(),help_text="Créneaux",required=True, widget=forms.CheckboxSelectMultiple)
    class Meta :
        model=DateCreneau
        exclude=['requete']



class ElevePotentielForm(forms.ModelForm):
    
    class Meta:
        model =ElevePotentiel
        exclude=['sessions']

#Suivi séances


class ReportSeanceForm(forms.Form):
    """docstring for ReportSeanceForm"""
    eleves = forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),help_text='Cocher les élèves présents', widget=forms.CheckboxSelectMultiple,required=False)
    clients = forms.ModelMultipleChoiceField(queryset=Client.objects.all(),help_text='Cocher les clients présents', widget=forms.CheckboxSelectMultiple,required=False)
    # A afficher avec du Jquerry en fonction du chapitre choisi (donner la possibilité d'ajouter une nouvelle notion au chapitre)
    #chapitre=forms.ModelChoiceField(queryset=Chapitre.objects.all(),help_text='Choisir le chapitre',required=False)
    #notions=forms.ModelChoiceField(queryset=Notions.objects.all(),help_text='Choisir les notions',required=False, widget=forms.CheckboxSelectMultiple)
    rapport = forms.CharField(label='Rapport de séance', max_length = 300, widget=forms.Textarea,required=False)
    """def __init__(self, seance, arg):
        super(ReportSeanceForm, self).__init__()
        self.arg = arg
        self.fields['eleves'].queryset = Eleve.objects.filter(cours= seance.cours.id) # Montrer que les élèves inscrits à la séance"""
        #self.fields['chapitre'].queryset = Chapitre.objects.filter(session = seance.cours.session.id) # Montrer que les chapitres de la matière de la séance
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
        self.fields['chapitre'].queryset = Chapitre.objects.filter(session = seance.session.id) # Montrer que les chapitres de la matière de la séance
        #self.fields['notions'].queryset = Notions.objects.filter(chapitre=seance.chapitre.id)  
    class Meta:
        model = Seance_Coaching
        fields = '__all__'"""

        
class Seance_CoachingForm(forms.ModelForm):
    langue=forms.ModelChoiceField(queryset=Langue.objects.all())
    #notions=forms.ModelMultipleChoiceField(queryset=Notions.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    field_order=('langue','eleve','session','coach','date','creneau','salle','chapitre','notions')
    eleve=forms.ModelMultipleChoiceField(queryset=Eleve.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Seance_Coaching
        exclude =['statut','chapitre','notions']


#Suivi paiement 
class PayementForm(forms.ModelForm):
    class Meta:
        model = Payement
        exclude=['date','parent']


#Connexion
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



class SelectEleveForm(forms.Form):
    langue=forms.ModelChoiceField(queryset=Langue.objects.all(),help_text="Choisir le langue")
    eleve=forms.ModelChoiceField(queryset=Eleve.objects.all())


class ProspectForm(RequeteForm):
    date_fin=forms.DateField()
    



"""
class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail", required=True)
"""