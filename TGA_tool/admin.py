from django.contrib import admin
from TGA_tool.models import Parent,Eleve,Cours,Seance_Cours,Seance_Coaching,Coach,Salle,Chapitre,Notions,Matiere,Frequence,Creneau,Curriculum

# Register your models here.
class ParentAdmin(admin.ModelAdmin):
	list_display   = ('nom', 'mail', 'num_tel', 'mail','adresse','estResponsable')
	list_filter    = ('estResponsable','date_inscription', )
    #date_hierarchy = 'date_inscription'
	ordering       = ('date_inscription', )
	search_fields  = ('nom', 'num_tel','date_inscription')
class EleveAdmin(admin.ModelAdmin):
	list_display   = ('nom','date_naissance','num', 'email','etablissement','parent_resp','parent_sec','curriculum')
	list_filter    = ('date_inscription','parent_resp','parent_sec','curriculum','cours','etablissement' )
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
	list_display=('curriculum','matiere','coach','frequence')
	list_filter=('curriculum','matiere','coach','frequence')
	
class MatiereAdmin(admin.ModelAdmin):
	list_display=('curriculum','matiere')
	list_filter=('curriculum',)
	search_fields=('matiere',)
class ChapitreAdmin(admin.ModelAdmin):
	list_filter=('matiere',)
	list_display=('chapitre','matiere')
class NotionsAdmin(admin.ModelAdmin):
	list_filter=('chapitre',)
	list_display=('chapitre','notion')
class CoursSeanceAdmin(admin.ModelAdmin):
	list_display=('date','creneau','cours','salle','chapitre','statut')
	list_filter=('cours','date','salle','chapitre','notions','statut')
	fieldsets = (
	('Cours',{
		'fields':('cours',)
	}),
	('Ressources',{
		'fields':('date','creneau','salle')
	}),
	('Contenu',{
		'classes': ['collapse',],
		'fields':('chapitre','notions')
	}),
	)
class FrequenceAdmin(admin.ModelAdmin):
	fields=('frequence','creneau','jour','day_of_month','period','date_debut','date_limite')
class CreneauAdmin(admin.ModelAdmin):
	fields=('debut',)
admin.site.register(Parent,ParentAdmin)
admin.site.register(Eleve,EleveAdmin)
admin.site.register(Cours,CoursAdmin)
admin.site.register(Seance_Cours,CoursSeanceAdmin)
admin.site.register(Seance_Coaching)
admin.site.register(Coach)
admin.site.register(Salle)
admin.site.register(Chapitre,ChapitreAdmin)
admin.site.register(Notions,NotionsAdmin)
admin.site.register(Matiere,MatiereAdmin)
admin.site.register(Frequence,FrequenceAdmin)
admin.site.register(Creneau,CreneauAdmin)
admin.site.register(Curriculum)

