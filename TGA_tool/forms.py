from django import forms
from TGA_tool.models import Parent,Eleve,Cours,Seance,Coach,Salle,Chapitre,Notions,Matiere,Frequence,Creneau,Curriculum

class ParentForm(forms.ModelForm):
   class Meta:
       model= Parent
       fields = '__all__'