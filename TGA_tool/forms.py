from django import forms
from TGA_tool.models import *


class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail", required=True)
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = '__all__'

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = '__all__'

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = '__all__'
    
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = '__all__'

class Seance_CoachingForm(forms.ModelForm):
    class Meta:
        model = Seance_Coaching
        fields = '__all__'

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = '__all__'

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'

class FrequenceForm(forms.ModelForm):
    class Meta:
        model = Frequence
        fields = '__all__'
