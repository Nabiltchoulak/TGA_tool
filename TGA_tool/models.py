from django.db import models 
from django.utils import timezone
from datetime import timedelta,datetime,date,time
from . import date_manager
#from matrix_field import MatrixField
#from django.utils.managers import InheritanceManager
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.auth.models import User

class Resource(models.Model):
	disponibilite=models.CharField(max_length=15,blank=True)

	class Meta:
		abstract=True

########################### UTILISATEURS #######################################################
class Famille(models.Model):
	nom= models.CharField(max_length=42,verbose_name="Nom de famille", unique= False)
	adresse = models.CharField(max_length=100,verbose_name="Adresse de famille", unique = True)

	class Meta:
		verbose_name="Famille"
		ordering=['nom']

	def __str__(self):
		return '{0} - {1}'.format(self.nom, self.adresse)

class Parent(models.Model):
	# Information générales
	genre_choices=(("M.","Monsieur"),("Mme.","Madame"),("Mlle","Mademoiselle"),)
	genre=models.CharField(max_length=10,choices=genre_choices,default="M.",verbose_name="Civilité")
	prenom = models.CharField(max_length=42,verbose_name="Prénom",unique=False, default="")
	nom= models.CharField(max_length=42,verbose_name="Nom",unique=False)
	telephone= models.CharField(max_length=40,verbose_name="Telephone",unique=True)
	email= models.EmailField(verbose_name="E-mail",blank=True)
	famille = models.ForeignKey('Famille', on_delete = models.CASCADE, verbose_name="Famille", null=False,default= 1)
	estResponsable= models.BooleanField(verbose_name="Parent principal", default=False)
	credit=models.IntegerField(default=0)
	debit=models.IntegerField(default=0)
	solde = models.IntegerField(default=0)
	

	# Information du compte utilisateur
	date_inscription = models.DateField(auto_now=True, verbose_name="Date d'inscription")
	user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)

	class Meta:
		verbose_name="parent"
		ordering=['nom']

	def __str__(self):
		return '{0} {1}'.format(self.prenom, self.nom)

class ElevePotentiel(models.Model):
	nom= models.CharField(max_length=42,verbose_name="Nom complet",unique=False)
	num= models.CharField(max_length=15,blank=True,verbose_name="Telephone")
	email=models.EmailField(blank=True,null=True,verbose_name="E-mail")
	matieres=models.ManyToManyField("Matiere",through="Requete", verbose_name="Cours potentiels demandes",blank=True)
	def __str__(self):
		return self.nom

class Eleve(ElevePotentiel):	

	# Informations générales
	#nom= models.CharField(max_length=42,verbose_name="Prenom",unique=False)
	date_naissance=models.DateField(null=True,blank=True,verbose_name="Date de naissance")
	#num= models.CharField(max_length=15,null=True,blank=True,verbose_name="Telephone",unique=True,help_text="Optionnel")
	#email=models.EmailField(null=True,blank=True,verbose_name="E-mail",unique=True,help_text="Optionnel")
	famille = models.ForeignKey('Famille',on_delete=models.CASCADE,verbose_name="Famille", default=1)

	# Informations scolarités
	etablissement=models.CharField(max_length=20,null=True,blank=True)
	curriculum=models.ForeignKey('Curriculum',on_delete=models.CASCADE,verbose_name="Curriculum",blank=True,null=True)
	cours=models.ManyToManyField('Cours',related_name='cours',blank=True,verbose_name="Cours")

	# Information du compte utilisateur
	user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
	date_inscription = models.DateField(auto_now=True, verbose_name="Date d'inscription")
	class Meta:
		verbose_name="eleve"
		ordering=['nom']
	def __str__(self):
		return self.nom


class Requete(models.Model):
	eleve=models.ForeignKey("ElevePotentiel", on_delete=models.CASCADE)
	matiere = models.ForeignKey("Matiere", on_delete=models.SET_NULL,null=True,blank=True)
	day_choices=(('Dimanche','Dimanche'),('Lundi','Lundi'),('Mardi','Mardi'),('Mercredi','Mercredi'),('Jeudi','Jeudi'),('Vendredi','Vendredi'),('Samedi','Samedi'),)
	jour=models.CharField(null=True,blank=True,choices=day_choices, max_length=70)
	creneau=models.ManyToManyField("Creneau",verbose_name='Créneau',blank=True)
	def __str__(self):
		return "{0} demande {1}".format(self.eleve, self.matiere)


class Coach(Resource):
	genre_choices=(("M.","Monsieur"),("Mme.","Madame"),("Mlle","Mademoiselle"),)
	genre=models.CharField(max_length=10,choices=genre_choices,default="M.",verbose_name="Civilité")
	prenom=models.CharField(max_length=42,verbose_name="Prénom", default="")
	nom=models.CharField(max_length=42,verbose_name="Nom")
	telephone=models.CharField(max_length=15,verbose_name="Telephone",unique=True,null=True,blank=True)
	email= models.EmailField(verbose_name="E-mail",null=True,blank=True,unique=True)
	matieres=models.ManyToManyField('Matiere',related_name="enseigne",verbose_name="matieres",help_text='Les matières que peut enseigner ce coach')
	user = models.OneToOneField(User, on_delete = models.CASCADE, default=1)
	salaire = models.DecimalField(max_digits=8, decimal_places=2,default=0)
	grade_choices=(("Junior","Junior"),("Senior","Senior"),("Excellence","Excellence"),)
	grade=models.CharField(max_length=10,choices=grade_choices,default="",blank=True)
	#matrice_dispo pour gérer les disponibilités
	#matrice_polyvalence pour gérer la polyvalence des coachs
	class Meta:
		verbose_name="coach"	
		ordering=['nom']
	def __str__(self):
		return "{0} {1}".format(self.prenom,self.nom)

class Payement(models.Model):
	date=models.DateField(blank=True,null=True,verbose_name="Date")
	montant = models.DecimalField(max_digits=8, decimal_places=2)
	parent = models.ForeignKey('Parent', on_delete=models.CASCADE, blank=False, null = False, verbose_name = 'Parent payeur')

	class Meta:
		verbose_name = "Paiement"
		ordering=['date']

	def __str__(self):
		return 'Paiement de {0} par parent {1}' . format(self.montant, self.parent)


############################################################### Curriculums ########################################################################""


class CurriculumCreator(models.Manager):
	def create_group(self, niveau):
		group=self.create(niveau=niveau,programme='FR')
		return group

class Curriculum(models.Model):
	niveau=models.CharField(max_length=13)
	programme=models.CharField(max_length=2,blank=True,null=True)
	objects = CurriculumCreator()#ajouter une methode manager au object
	def __str__(self):
		return self.niveau


class Cours(models.Model):#Cours est un curriculum(niveau ou groupe) avec une matiére et un coach
	curriculum=models.ForeignKey('Curriculum',on_delete=models.CASCADE,related_name='curriculum',verbose_name="Curriculum")
	matiere=models.ForeignKey('Matiere',on_delete=models.CASCADE,null=True,verbose_name="Matiere")
	coach=models.ForeignKey('Coach',on_delete=models.SET_NULL,blank=True,null=True,verbose_name="Coach")
	frequence=models.OneToOneField('Frequence',on_delete=models.SET_NULL,null=True,blank=True)

	class Meta:
		verbose_name="cours"
		ordering=['-curriculum','matiere']

	def __str__(self):
		return "{0}".format(self.matiere)#matiere contient déjà le curriculum

#Intersection entre éléves (cours) ressources 
class Seance(models.Model):#Seance est une classe abstraite qui englobe les attributs en commun entre Seance_cours et seance_coaching 
	date=models.DateField(blank=True,null=True,verbose_name="Date")
	creneau=models.ForeignKey('Creneau',on_delete=models.CASCADE,blank=True,null=True,verbose_name="Creneau")
	salle=models.ForeignKey('Salle',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Salle")
	chapitre=models.ForeignKey('Chapitre',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Chapitre")
	notions=models.ManyToManyField('Notions',related_name="%(app_label)s_%(class)s_related",blank=True,verbose_name="Notions")#pour ne pas avoir de confusion au moment de l'appel
	statut_choices=(("Planifié","Planifiée"),("Done","Effectué"),("Annulé","Annulée"),)
	statut=models.CharField(max_length=8,choices=statut_choices,default="Planifié",verbose_name="Statut")
	class Meta:
		abstract=True


		
class Seance_Cours(Seance):
	
	cours=models.ForeignKey('Cours',on_delete=models.CASCADE,verbose_name="Cours")
	eleves = models.ManyToManyField	('Eleve',blank=True,related_name="presence")

	class Meta:
		verbose_name="seance cours"
		ordering=['date','creneau']
	#date
	def __str__(self):
		str_cre=str(self.date)#timefield n'est pas un string ne peut étre retourné 
		return "Cours {0} {1} ".format(self.cours,str_cre)

class Seance_Coaching(Seance):
	matiere=models.ForeignKey('Matiere',on_delete=models.CASCADE,null=True,blank=True)
	eleve=models.ManyToManyField('Eleve',related_name="eleve_coaching",blank=True)
	coach=models.ForeignKey('Coach', verbose_name="Coach", on_delete=models.SET_NULL,null=True,blank=True)
	class Meta:
		verbose_name="seance coaching"
		ordering=['date','creneau']
	#date
	def __str__(self):
		str_cre=str(self.date)#timefield n'est pas un string ne peut étre retourné 
		return "Coaching {0} {1} ".format(self.matiere,str_cre)

######################################################################## Matieres ##########################################################


class MatiereCreator(models.Manager):
	def create_matiere(self, matiere,curriculum):
		matiere=self.create(matiere=matiere,curriculum=curriculum)
		return matiere

class Matiere(models.Model):
	#matiere_choices=(("Mathematiques","Mathematiques"),("Physique","Physique"),("SVT","SVT"),("Français","Français"),("Anglais","Anglais"),("Technologie","Technologie"),("SES","SES"),("Philosophie","Philosophie"),)
	
	matiere=models.CharField(max_length=30,verbose_name="Matiere")
	curriculum=models.ForeignKey('Curriculum',on_delete=models.CASCADE,related_name='matiere',verbose_name="Curriculum")
	objects = MatiereCreator()#ajouter une methode manager au object
	class Meta:
		verbose_name="matiere"
		ordering=['-curriculum','matiere']
	def __str__(self):
		return "{0} {1}".format(self.curriculum,self.matiere)



class Chapitre(models.Model):
	chapitre=models.CharField(max_length=50)
	matiere=models.ForeignKey('Matiere',on_delete=models.CASCADE,verbose_name="Matiere")
	details=models.TextField(blank=True,null=True,help_text='Précisions sur le chapitre')
	def __str__(self):
		return self.chapitre 
	class Meta:
		verbose_name="chapitre"
		ordering=['matiere','chapitre']

class Notions(models.Model):
	notion=models.CharField(max_length=50,verbose_name="Notion")
	details=models.TextField(blank=True,null=True,verbose_name="Details")
	chapitre=models.ForeignKey('Chapitre',on_delete=models.CASCADE)
	class Meta:
		verbose_name="notions"
		ordering=['chapitre','details']
	def __str__(self):
		return self.notion




class Salle(Resource):
	nom=models.CharField(max_length=42,verbose_name="Nom",unique=True)
	capcite=models.PositiveIntegerField(verbose_name="Capacité",null=True,blank=True)
	ecran=models.BooleanField(verbose_name="Posséde un écean")
	batiment=models.BooleanField(verbose_name="TGA")
	class Meta:
		verbose_name="salle"
		ordering=['capcite']
	def __str__(self):
		return self.nom



class Frequence(models.Model):
	freq_choices=(
		('Frequence',(
			("Une seance","Une séance"),
			("Chaque jour","Chaque jour"),
			("Un jour chaque semaine","Chaque semaine"),
			("Un jour chaque mois","Chaque mois"),
				)
			),
		('Personalisé',(
			("Jours",'Chaque X jours'),
			("Semaines",'Chaque X semaines'),
			("Mois",'Chaque X mois'),
				)
			),
	)
	day_choices=((7,'Dimanche'),(1,'Lundi'),(2,'Mardi'),(3,'Mercredi'),(4,'Jeudi'),(5,'Vendredi'),(6,'Samedi'),)#les numéros font référence a l'isoweekday
	frequence=models.CharField(max_length=30,choices=freq_choices,default="Une seance",verbose_name="Fréquence")
	creneau=models.ForeignKey('Creneau',on_delete=models.SET_NULL,blank=True,null=True,verbose_name="Creneau",help_text="Créneau dans la journée")
	jour=models.PositiveIntegerField(blank=True,null=True,choices=day_choices,verbose_name="Jour de la semaine",help_text="Le jour de la semaine")#jour de la semaine iso 
	day_of_month=models.PositiveIntegerField(verbose_name="Jour du mois",blank=True,null=True,help_text="Le jour du mois (ex: Chaque 25 du mois)")
	period=models.PositiveIntegerField(verbose_name="Chaque",help_text="",blank=True,null=True)#x times each week/month/day
	date_debut=models.DateField(verbose_name="Debut du cours",blank=True,null=True,help_text="Date du début du cours")#le premier jour de la semiane dans la calendrier iso est le lundi
	date_limite=models.DateField(verbose_name="Fin du cours",blank=True,null=True,help_text="Date de la fin du cours")
	class Meta:
		verbose_name="fréquence"
	def __str__(self):
		if self.period == None :
			return self.frequence
		else:
			return "Chaque {0} {1}".format(self.period, self.frequence)
####################################################################  Créneaux #####################################################################



class CreneauCreator(models.Manager):
	def create_creneau(self,debut):
		creneau=self.create(debut=debut)
		return creneau

class Creneau(models.Model):
	debut=models.TimeField()
	fin=models.TimeField(blank=True,null=True)#Va se préciser lors de l'appel de __str__
	
	objects=CreneauCreator()#pour l'appel du manager
	def __str__(self):
		#Ici on va profiter de l'appel de __str__ pour préciser l'heure de fin pour chaque créneau qui est toujours heuredebut + 1h30
		#
		st_tim=str(self.debut)
		if self.debut.minute == 30 :
			#Le cas 9h30-11h00
			self.fin=time(hour=self.debut.hour +2,minute=(self.debut.minute +30)%60)
		else :
			#Le cas 8h-9h30
			self.fin=time(hour=self.debut.hour +1,minute=(self.debut.minute +30)%60)
		ed_tim=str(self.fin)
		return "{0} - {1}".format(st_tim,ed_tim)
	class Meta :
		verbose_name="créneau"


###################################################################   Signaux  #######################################################################



@receiver(post_save, sender=Cours)
def init_seances(sender, instance, **kwargs):
	if (len(instance.seance_cours_set.all())) == 0:#case when a "cours" is in initiation not been modified 
		if instance.frequence.period == None :#Différence entre perso et proposé présence de la periodicité  
			if instance.frequence.frequence == "Une seance" :#switch case
				Seance_Cours.objects.create(cours=instance,creneau=instance.frequence.creneau,date=instance.frequence.date_debut)
			elif instance.frequence.frequence =="Chaque jour" :
				for day in date_manager.daysrange(instance.frequence.date_debut,instance.frequence.date_limite):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau) 
			elif instance.frequence.frequence =="Un jour chaque semaine":
				for day in date_manager.weeksperiod(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.jour):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau)
			elif instance.frequence.frequence =="Un jour chaque mois":
				for day in date_manager.monthsperiod(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.day_of_month):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau)
		else : #freq perso 
			if instance.frequence.frequence == "Jours" :
				for day in date_manager.spe_daysperiod(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.period):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau)
			elif instance.frequence.frequence == "Semaines" :
				for day in date_manager.spe_weeksperiod(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.period):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau)
			elif instance.frequence.frequence == "Mois" :
				for day in date_manager.spe_monthsrange(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.period,instance.frequence.day_of_month):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau)
	else :
		print('object already exist')#case when an frequence "cours" is updated (instance cours already exist which will create all "seance" again) work on that later   
