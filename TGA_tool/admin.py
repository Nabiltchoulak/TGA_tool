from django.contrib import admin
from TGA_tool.models import Parent,Eleve,Cours,Seance,Coach,Salle,Chapitre,Notions,Matiere,Frequence
"""
# Register your models here.
class ParentAdmin(admin.ModelAdmin):
	list_display   = ('nom', 'mail', 'num_tel', 'mail','adresse','estResponsable')
	list_filter    = ('estResponsable','date_inscription', )
    #date_hierarchy = 'date_inscription'
	ordering       = ('date_inscription', )
	search_fields  = ('nom', 'num_tel','date_inscription')
class EleveAdmin(admin.ModelAdmin):
	list_display   = ('nom','date_naissance','num', 'email','etablissement','parent_resp','parent_sec','curriculum')
	list_filter    = ('date_inscription','parent_resp','parent_sec','curriculum','cours','etablissement','dz' )
    #date_hierarchy = 'date_inscription'
	ordering       = ('date_inscription', )
	search_fields  = ('nom','num','date_inscription')
	fieldsets=(
		('Coordonnés',{
		'fields':('nom','num','email','date_naissance','etablissement')			
			}),
		('Parents',{
			'description':'Tuteurs de l\'élève',
			'fields':('parent_resp','parent_sec',)
			}),
		('Matiere',{
			'fields':('curriculum','cours',)
			}),
		)
class CoursAdmin(admin.ModelAdmin):
	list_filter=('groupe','matiere')
	search_fields=('matiere','groupe')
class ChapitreAdmin(admin.ModelAdmin):
	list_filter=('matiere',)
	list_display=('chapitre','matiere')
class NotionsAdmin(admin.ModelAdmin):
	list_filter=('chapitre',)
	list_display=('chapitre','notion')
class SeanceAdmin(admin.ModelAdmin):
	list_display=('creneau','cours','coach','salle','chapitre')
	list_filter=('cours','coach','salle','chapitre','notions')
	fieldsets = (
	('Cours',{
		'fields':('cours',)
	}),
	('Ressources',{
		'fields':('creneau','coach','salle')
	}),
	('Contenu',{
		'classes': ['collapse',],
		'fields':('chapitre','notions')
	}),
	)"""
admin.site.register(Parent)
admin.site.register(Eleve)
admin.site.register(Cours)
admin.site.register(Seance)
admin.site.register(Coach)
admin.site.register(Salle)
admin.site.register(Chapitre)
admin.site.register(Notions)
admin.site.register(Matiere)
admin.site.register(Frequence)
