from django.contrib import admin
from TGA_tool.models import Parent,Eleve,Requete,Payement,Cours,Client,ElevePotentiel,Famille,Seance_Cours,Coach,Salle,Chapitre,Notions,Session,Frequence,Creneau,Langue

# Register your models here.
class ParentAdmin(admin.ModelAdmin):
	list_display   = ('nom', 'email', 'telephone', 'email','estResponsable')
	list_filter    = ('estResponsable','date_inscription', )
    #date_hierarchy = 'date_inscription'
	ordering       = ('date_inscription', )
	search_fields  = ('nom', 'telephone','date_inscription')
class EleveAdmin(admin.ModelAdmin):
	list_display   = ('nom','date_naissance','num', 'email','etablissement','famille')
	list_filter    = ('date_inscription','famille','cours','etablissement' )
    #date_hierarchy = 'date_inscription'
	ordering       = ('date_inscription', )
	search_fields  = ('nom','num','date_inscription')
	fieldsets=(
		('Coordonnés',{
		'fields':('nom','prenom','num','email','date_naissance','etablissement')			
			}),
		('Famille',{
			'description':'Famille de l\'élève',
			'fields':('famille',)
			}),
		('Session',{
			'fields':('langue','cours',)
			}),
		)
class CoursAdmin(admin.ModelAdmin):
	list_display=('langue','session','coach','frequence')
	list_filter=('langue','session','coach','frequence')
	
class SessionAdmin(admin.ModelAdmin):
	
	list_filter=('langue',)
	search_fields=('session',)
class ChapitreAdmin(admin.ModelAdmin):
	list_filter=('session',)
	list_display=('chapitre','session')
	fields=('session','chapitre')
class NotionsAdmin(admin.ModelAdmin):
	list_filter=('chapitre',)
	list_display=('chapitre','notion')
class CoursSeanceAdmin(admin.ModelAdmin):
	list_display=('date','creneau','cours','salle','chapitre','statut')
	list_filter=('cours','date','salle','chapitre','notions','statut')
	fieldsets = (
	('Cours',{
		'fields':('cours','statut')
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
#admin.site.register(Seance_Coaching)
admin.site.register(ElevePotentiel)
admin.site.register(Coach)
admin.site.register(Salle)
admin.site.register(Famille)
admin.site.register(Chapitre,ChapitreAdmin)
admin.site.register(Notions,NotionsAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Frequence,FrequenceAdmin)
admin.site.register(Creneau,CreneauAdmin)
admin.site.register(Langue)
admin.site.register(Requete)
admin.site.register(Payement)
admin.site.register(Client)

