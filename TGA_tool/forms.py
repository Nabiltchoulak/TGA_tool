from django import forms
from TGA_tool.models import *

from django import forms
from .models import *

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
        