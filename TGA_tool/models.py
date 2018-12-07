from django.db import models 
from django.utils import timezone
from datetime import timedelta,datetime,date
from . import date_manager
#from matrix_field import MatrixField
#from django.utils.managers import InheritanceManager
from django.db.models.signals import post_save
from django.dispatch import receiver 
NB_SEMAINESPARPERIODE=10
NB_MOISPARPERIODE=2

class Parent(models.Model):
	nom= models.CharField(max_length=42,verbose_name="Nom",unique=True)
	num_tel= models.CharField(max_length=15,verbose_name="Telephone",unique=True)
	mail= models.EmailField(verbose_name="E-mail",unique=True)
	adresse = models.CharField(max_length=150,verbose_name="Adresse")
	estResponsable= models.BooleanField(verbose_name="Responsable de l'enfant")
	
	date_inscription = models.DateField(auto_now=True, verbose_name="Date d'inscription")
	#canal = models.
	class Meta:
		verbose_name="parent"
		#ordering=['date_inscription']

	def __str__(self):
		return self.nom


class Eleve(models.Model):
	
	nom= models.CharField(max_length=42,verbose_name="Nom")
	num= models.CharField(max_length=15,null=True,blank=True,verbose_name="Telephone")
	email=models.EmailField(null=True,blank=True,verbose_name="E-mail")
	date_naissance=models.DateField(null=True,verbose_name="Date de naissance")
	parent_resp=models.ForeignKey('Parent',on_delete=models.CASCADE,limit_choices_to={'estResponsable':True},verbose_name="Parent responsable")
	parent_sec=models.ForeignKey('Parent',on_delete=models.SET_NULL,null=True,blank=True,limit_choices_to={'estResponsable':False},related_name="secondaire",verbose_name="Parent contact")
	curriculum=models.ForeignKey('Curriculum',on_delete=models.CASCADE,verbose_name="Curriculum")
	cours=models.ManyToManyField('Cours',related_name='cours',blank=True,verbose_name="Cours")
	etablissement=models.CharField(max_length=20,null=True)
	#dz= models.BooleanField(verbose_name="Programme Algérien")
	date_inscription = models.DateField(auto_now=True, verbose_name="Date d'inscription")
	class Meta:
		verbose_name="eleve"
		#ordering=['date_inscription']
	def __str__(self):
		return self.nom
###################################################################### Création des groupes, se fait automatiquement pas besoin de la toucher 
class CurriculumCreator(models.Manager):
	def create_group(self, niveau):
		group=self.create(niveau=niveau,programme='FR')
		return group

class Curriculum(models.Model):
	niveau=models.CharField(max_length=13)
	programme=models.CharField(max_length=2)
	objects = CurriculumCreator()
	def __str__(self):
		return self.niveau
NIV=['CP','CE','CE2','CM1','CM2','Sixième','Cinquième','Quatrième','DNB','Seconde','Première S','Première ES','Terminal S','Terminal ES']
if (len(Curriculum.objects.all()))<2:
	for niv in range(13):
		Curriculum.objects.create_group(NIV[niv])
#####################################################################
class Cours(models.Model):
	curriculum=models.ForeignKey('Curriculum',on_delete=models.CASCADE,related_name='niv',verbose_name="Curriculum")
	matiere=models.ForeignKey('Matiere',on_delete=models.SET_NULL,null=True,verbose_name="Matiere")
	coach=models.ForeignKey('Coach',on_delete=models.SET_NULL,blank=True,null=True,verbose_name="Coach")
	frequence=models.ForeignKey('Frequence',on_delete=models.SET_NULL,null=True,blank=True)
	
	class Meta:
		verbose_name="cours"
	def __str__(self):
		return "{0} {1}".format(self.matiere, self.curriculum)

class Seance(models.Model):
	date=models.DateField(blank=True,null=True,verbose_name="Date")
	creneau=models.TimeField(blank=True,null=True,verbose_name="Creneau")
	cours=models.ForeignKey('Cours',on_delete=models.CASCADE,null=True,verbose_name="Cours")
	salle=models.ForeignKey('Salle',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Salle")
	chapitre=models.ForeignKey('Chapitre',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Chapitre")
	notions=models.ManyToManyField('Notions',related_name="Titre",blank=True,verbose_name="Notions")
	statut_choices=(("PL","Planifiée"),("EF","Effectuée"),("AN","Annulée"),)
	statut=models.CharField(max_length=2,choices=statut_choices,default="PL",verbose_name="Statut")

	class Meta:
		verbose_name="seance"
	#date
	def __str__(self):
		str_cre=str(self.date)
		return "{0} {1}".format(str_cre, self.cours)
class Matiere(models.Model):
	matiere=models.CharField(max_length=14,verbose_name="Matiere")
	curriculum=models.ForeignKey('Curriculum',on_delete=models.CASCADE,verbose_name="Curriculum")
	class Meta:
		verbose_name="matiere"
	def __str__(self):
		return "{0} {1}".format(self.matiere, self.curriculum)

class Chapitre(models.Model):
	chapitre=models.CharField(max_length=50)
	matiere=models.ForeignKey('Matiere',on_delete=models.CASCADE,verbose_name="Matiere")
	
	def __str__(self):
		return self.chapitre 
	class Meta:
		verbose_name="chapitre"
class Notions(models.Model):
	notion=models.CharField(max_length=50,verbose_name="Notion")
	details=models.TextField(blank=True,null=True,verbose_name="Details")
	chapitre=models.ForeignKey('Chapitre',on_delete=models.CASCADE)
	class Meta:
		verbose_name="notions"
	def __str__(self):
		return self.notion

class Resource(models.Model):
	disponibilité=models.CharField(max_length=15,blank=True)

	class Meta:
		abstract=True
		
class Coach(Resource):
	nom=models.CharField(max_length=42,verbose_name="Nom",unique=True)
	telphone=models.CharField(max_length=15,verbose_name="Telephone",unique=True)
	mail= models.EmailField(verbose_name="E-mail")
	matieres=models.ManyToManyField('Matiere',related_name="enseigne",verbose_name="matieres")
	#matrice_dispo
	#matrice_polyvalence
	class Meta:
		verbose_name="coach"
	def __str__(self):
		return self.nom

class Salle(Resource):
	nom=models.CharField(max_length=42,verbose_name="Nom",unique=True)
	capcite=models.PositiveIntegerField(verbose_name="Capacité")
	ecran=models.BooleanField(verbose_name="Posséde un écean")
	batiment=models.BooleanField(verbose_name="TGA")
	class Meta:
		verbose_name="salle"
	def __str__(self):
		return self.nom



class Frequence(models.Model):
	freq_choices=(
		('Frequence',(
			("Une seance","Une séance"),
			("Chaque jour","Chaque jour"),
			("Un jour chaque semaine","Un jour chaque semaine"),
			("Un jour chaque mois","Un jour chaque mois"),
				)
			),
		('Personalisé',(
			('Jours','Chaque x jours'),
			('Semaines','Chaque x semaines'),
			('Mois','Chaque x mois'),
				)
			),
	)
	frequence=models.CharField(max_length=30,choices=freq_choices,default="Une seance",verbose_name="Fréquence")
	intervalle=models.PositiveIntegerField(verbose_name="Nombre de séance par fréquence",blank=True,null=True)#x times each week/month/day
	day_choices=((7,'Dimanche'),(1,'Lundi'),(2,'Mardi'),(3,'Mercredi'),(4,'Jeudi'),(5,'Vendredi'),(6,'Samedi'),)#les numéros font référence a l'isoweekday
	jour=models.PositiveIntegerField(blank=True,null=True,choices=day_choices)
	day_of_month=models.PositiveIntegerField(verbose_name="Jour du mois",blank=True,null=True)
	date_limite=models.DateField(verbose_name="Fin de la période",blank=True,null=True)
	date_debut=models.DateField(verbose_name="Debut de la période",blank=True,null=True)#le premier jour de la semiane dans la calendrier iso est le lundi
	class Meta:
		verbose_name="fréquence"
	def __str__(self):
		if self.intervalle == None :
			return self.frequence
		else:
			return "chaque {0} {1}".format(self.intervalle, self.frequence)
############ Signal qui génére les séances selon la fréquence 
@receiver(post_save, sender=Cours)
def init_seances(sender, instance, **kwargs):
	if instance.frequence.intervalle == None :
		if instance.frequence.frequence == "Une seance" :
			Seance.objects.create(cours=instance)
		elif instance.frequence.frequence =="Chaque jour" :
			for day in date_manager.daysrange(instance.frequence.date_debut,instance.frequence.date_limite):
				Seance.objects.create(cours=instance,date=day)#Ajouer l'attribut date dans séance 
		elif instance.frequence.frequence =="Un jour chaque semaine":
			for day in date_manager.weeksrange(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.jour):
				Seance.objects.create(cours=instance,date=day)
		elif instance.frequence.frequence =="Un jour chaque mois":
			for day in date_manager.monthsrange(instance.frequence.date_debut,instance.frequence.date_limite,instance.frequence.day_of_month):
				Seance.objects.create(cours=instance,date=day)
