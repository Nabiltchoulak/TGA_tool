from django.db import models 
from django.utils import timezone
from datetime import timedelta,datetime,date,time
from . import date_manager
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.auth.models import User

class Resource(models.Model):
	disponibilite=models.CharField(max_length=15,blank=True)

	class Meta:
		abstract=True

############################################## UTILISATEURS #######################################################
class Famille(models.Model):
	nom= models.CharField(max_length=42,verbose_name="Nom de famille", unique= False)
	adresse = models.CharField(max_length=100,verbose_name="Adresse de famille", unique = False)

	class Meta:
		verbose_name="Famille"
		ordering=['nom']

	def __str__(self):
		return '{0} - {1}'.format(self.nom, self.adresse)

class Parent(models.Model):
	# Information générales
	genre_choices=(("Mr.","Monsieur"),("Mme.","Madame"),("Mlle","Mademoiselle"),)
	genre=models.CharField(max_length=10,choices=genre_choices,default="M.",verbose_name="Civilité")
	prenom = models.CharField(max_length=42,verbose_name="Prénom",unique=False, default="")
	nom= models.CharField(max_length=42,verbose_name="Nom",unique=False)
	telephone= models.CharField(max_length=40,verbose_name="Telephone",blank=True)
	email= models.EmailField(verbose_name="E-mail",blank=True)
	profession= models.CharField(max_length=100,verbose_name="Profession",blank=True)
	famille = models.ForeignKey('Famille', on_delete = models.CASCADE, verbose_name="Famille", null=True,blank=True)
	estResponsable= models.BooleanField(verbose_name="Parent principal", default=False)
	sessions=models.ManyToManyField("Session",through="Requete", verbose_name="Cours potentiels demandes",blank=True)
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
	nom= models.CharField(max_length=42,verbose_name="Nom",unique=False)
	prenom=models.CharField(max_length=42,verbose_name="Prenom",unique=False)
	num= models.CharField(max_length=15,blank=True,verbose_name="Telephone")
	email=models.EmailField(blank=True,null=True,verbose_name="E-mail")
	sessions=models.ManyToManyField("Session",through="Requete", verbose_name="Cours potentiels demandes",blank=True)
	def __str__(self):
		return '{0} {1}'.format(self.prenom, self.nom)

class Eleve(ElevePotentiel):	

	# Informations générales
	#nom= models.CharField(max_length=42,verbose_name="Prenom",unique=False)
	date_naissance=models.DateField(null=True,blank=True,verbose_name="Date de naissance")
	#num= models.CharField(max_length=15,null=True,blank=True,verbose_name="Telephone",unique=True,help_text="Optionnel")
	#email=models.EmailField(null=True,blank=True,verbose_name="E-mail",unique=True,help_text="Optionnel")
	famille = models.ForeignKey('Famille',on_delete=models.CASCADE,verbose_name="Famille", default=1)

	# Informations scolarités
	etablissement=models.CharField(max_length=20,null=True,blank=True)
	#langue=models.ForeignKey('Langue',on_delete=models.CASCADE,verbose_name="Langue",blank=True,null=True)
	cours=models.ManyToManyField('Cours',related_name='Eleve_cours',blank=True,verbose_name="Cours")

	# Information du compte utilisateur
	user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
	date_inscription = models.DateField(auto_now=True, verbose_name="Date d'inscription")
	def get_courses(self):
		return Cours.objects.filter(Eleve_cours=self)
	def get_seances(self):
		return Seance_Cours.objects.filter(eleves=self)

	def get_remaining_seances(self):
		#Collect the ids in each iteration and in the end get the group bay a filter id__in
		seance_effectue_ids=[]
		seance_restant_ids=[]
		cours=Cours.objects.filter(Eleve_cours=self)
		for cour in cours :
			for seance in Seance_Cours.objects.filter(eleves=self).filter(statut="Effectué"):
				seance_effectue_ids.append(seance.id)
			for seance in Seance_Cours.objects.filter(cours=cour).filter(statut="Planifié"):
				seance_restant_ids.append(seance.id)
		seances_effectue=Seance_Cours.objects.filter(id__in=seance_effectue_ids)
		seance_restant=Seance_Cours.objects.filter(id__in=seance_restant_ids)
		
		return seance_restant
		



	class Meta:
		verbose_name="eleve"
		ordering=['nom']
	def __str__(self):
		return '{0} {1}'.format(self.prenom, self.nom)
class Client(Parent):
	date_naissance=models.DateField(null=True,blank=True,verbose_name="Date de naissance")
	
	cours=models.ManyToManyField('Cours',related_name='Client_cours',blank=True,verbose_name="Cours")
	date_commencement = models.DateField(verbose_name="Date de commencement",null=True,blank=True)
	
	def get_courses(self):
		return Cours.objects.filter(Client_cours=self)
	
	class Meta:
		verbose_name="client"
		ordering=['nom']
	def __str__(self):
		return '{0} {1}'.format(self.prenom, self.nom)



class DateCreneau(models.Model):
	requete=models.ForeignKey("Requete",verbose_name="Requete",on_delete=models.CASCADE)
	
	
	day_choices=(('Dimanche','Dimanche'),('Lundi','Lundi'),('Mardi','Mardi'),('Mercredi','Mercredi'),('Jeudi','Jeudi'),('Vendredi','Vendredi'),('Samedi','Samedi'),)
	jour=models.CharField(null=True,blank=True,choices=day_choices, max_length=70)
	creneau=models.ManyToManyField("Creneau", blank=True)
	def __str__(self):
		return "{0} {1}".format(self.jour,self.creneau.all())
		

class Requete(models.Model):
	eleve=models.ForeignKey("ElevePotentiel", on_delete=models.CASCADE,null=True,blank=True)
	parent=models.ForeignKey("Parent", on_delete=models.CASCADE,null=True,blank=True)
	session = models.ForeignKey("Session", on_delete=models.SET_NULL,null=True,blank=True)
	#day_choices=(('Dimanche','Dimanche'),('Lundi','Lundi'),('Mardi','Mardi'),('Mercredi','Mercredi'),('Jeudi','Jeudi'),('Vendredi','Vendredi'),('Samedi','Samedi'),)
	#jour=models.CharField(null=True,blank=True,choices=day_choices, max_length=70)
	#creneaux=models.ManyToManyField("Creneau",through="DateCreneau",verbose_name='Créneau',blank=True)
	
	class Meta:
		verbose_name="Requetes VIP"
	def __str__(self):
		if self.eleve :
			return "{0} demande {1}".format(self.eleve, self.session)
		else :
			return "{0} demande {1}".format(self.parent, self.session)
class Prospect_courses(Requete):
	date_fin=models.DateField(verbose_name="Date fin de la requete ", auto_now=False, auto_now_add=False)
	
	class Meta:
		verbose_name="Requetes"
		ordering=['date_fin']
	def __str__(self):
		if self.eleve :
			return "{0} demande {1} avant le {2}".format(self.eleve, self.session,self.date_fin)
		else :
			return "{0} demande {1} avant le {2} ".format(self.parent, self.session,self.date_fin)


class Coach(Resource):
	genre_choices=(("M.","Monsieur"),("Mme.","Madame"),("Mlle","Mademoiselle"),)
	genre=models.CharField(max_length=10,choices=genre_choices,default="M.",verbose_name="Civilité")
	prenom=models.CharField(max_length=42,verbose_name="Prénom", default="")
	nom=models.CharField(max_length=42,verbose_name="Nom")
	telephone=models.CharField(max_length=15,verbose_name="Telephone",unique=True,null=True,blank=True)
	email= models.EmailField(verbose_name="E-mail",null=True,blank=True,unique=True)
	sessions=models.ManyToManyField('Session',related_name="enseigne",verbose_name="sessions",help_text='Les matières que peut enseigner ce coach')
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
	date=models.DateTimeField(blank=True,null=True,verbose_name="Date et heure")
	montant = models.DecimalField(max_digits=8, decimal_places=2)
	parent = models.ForeignKey('Parent', on_delete=models.CASCADE, blank=False, null = False, verbose_name = 'Client')

	class Meta:
		verbose_name = "Paiement"
		ordering=['date']

	def __str__(self):
		return 'Paiement de {0} par parent {1}' . format(self.montant, self.parent)


############################################################### Langues ########################################################################""


class LangueCreator(models.Manager):
	def create_group(self, niveau):
		group=self.create(langue=niveau)
		return group

class Langue(models.Model):
	langue=models.CharField(max_length=13)
	#programme=models.CharField(max_length=2,blank=True,null=True)
	objects = LangueCreator()#ajouter une methode manager au object
	def __str__(self):
		return self.langue
######################################################################## Sessions ##########################################################


class SessionCreator(models.Manager):
	def create_session(self, session,langue):
		session=self.create(session=session,langue=langue)
		return session

class Session(models.Model):
	#session_choices=(("Mathematiques","Mathematiques"),("Physique","Physique"),("SVT","SVT"),("Français","Français"),("Anglais","Anglais"),("Technologie","Technologie"),("SES","SES"),("Philosophie","Philosophie"),)
	
	session=models.CharField(max_length=30,verbose_name="Session")
	langue=models.ForeignKey('Langue',on_delete=models.CASCADE,related_name='session',verbose_name="Langue")
	objects = SessionCreator()#ajouter une methode manager au object
	class Meta:
		verbose_name="session"
		ordering=['-langue','session']
	def __str__(self):
		
		langue="{0}".format(self.langue)
		
		if str(self.langue)=="English" :
			parts=self.session.split(" ")
			name=parts[0] + " " + langue + " "
			for part in parts[1:]:#Ca existe !!!
				name+=part + " "
			
			return name
		else:
			
			return "{0} {1}".format(self.langue,self.session)


########################################################### Cours #############################################################################

class Cours(models.Model):#Cours est un langue(niveau ou groupe) avec une matiére et un coach
	langue=models.ForeignKey('Langue',on_delete=models.CASCADE,related_name='langue_du_cours',verbose_name="Langue")
	session=models.ForeignKey('Session',on_delete=models.CASCADE,null=True,verbose_name="Session")
	coach=models.ForeignKey('Coach',on_delete=models.SET_NULL,blank=True,null=True,verbose_name="Coach")
	frequence=models.OneToOneField('Frequence',on_delete=models.SET_NULL,null=True,blank=True)
	match_indic=models.CharField(max_length=10,default='',blank=True)
	vip=models.BooleanField(default=False,blank=True)

	def get_seances(self):
		return Seance_Cours.objects.filter(cours=self)

	class Meta:
		verbose_name="cours"
		ordering=['-langue','session']

	def __str__(self):
		return "{0} {1}".format(self.session,self.match_indic )#session contient déjà le langue


######################################################## Fréquence cours #############################################################################
class Frequence(models.Model):
	freq_choices=(
		('Frequence',(
			("Une seance","Une séance"),
			("Chaque jour","Chaque jour"),
			("Un jour chaque semaine","Chaque semaine"),
			("Deux fois par semaine","Deux fois par semaine"),
			("Trois fois par semaine","Trois fois par semaine"),
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
	jour=models.PositiveIntegerField(blank=True,null=True,choices=day_choices,verbose_name="Jour de la semaine")#jour de la semaine iso 
	jour_two=models.PositiveIntegerField(blank=True,null=True,choices=day_choices,verbose_name="Deuxième jour de la semaine")#jour de la semaine iso 
	jour_three=models.PositiveIntegerField(blank=True,null=True,choices=day_choices,verbose_name="Troisième jour de la semaine")#jour de la semaine iso
	day_of_month=models.PositiveIntegerField(verbose_name="Jour du mois",blank=True,null=True,help_text="Le jour du mois (ex: Chaque 25 du mois)")
	period=models.PositiveIntegerField(verbose_name="Chaque",help_text="",blank=True,null=True)#x times each week/month/day
	date_debut=models.DateField(verbose_name="Debut du cours",blank=True,null=True,help_text="Date du début du cours")#le premier jour de la semiane dans la calendrier iso est le lundi
	date_limite=models.DateField(verbose_name="Fin du cours",blank=True,null=True,help_text="Date de la fin du cours")
	class Meta:
		verbose_name="fréquence"
	
	def has_cours(self):
		try :
			Cours.objects.get(frequence=self)
		except ObjectDoesNotExist :
			return False
		else:
			return True

		
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
############################################################ Séances #######################################################################""
#Intersection entre éléves (cours) ressources 
class Seance(models.Model):#Seance est une classe abstraite qui englobe les attributs en commun entre Seance_cours et seance_coaching 
	date=models.DateField(blank=True,null=True,verbose_name="Date")
	creneau=models.ForeignKey('Creneau',on_delete=models.CASCADE,blank=True,null=True,verbose_name="Creneau")
	salle=models.ForeignKey('Salle',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Salle")
	chapitre=models.ForeignKey('Chapitre',on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Chapitre")
	notions=models.ManyToManyField('Notions',related_name="%(app_label)s_%(class)s_related",blank=True,verbose_name="Notions")#pour ne pas avoir de confusion au moment de l'appel
	statut_choices=(("Planifié","Planifiée"),("Effectué","Effectué"),("Annulé","Annulée"),)
	statut=models.CharField(max_length=8,choices=statut_choices,default="Planifié",verbose_name="Statut")
	class Meta:
		abstract=True


		
class Seance_Cours(Seance):
	
	cours=models.ForeignKey('Cours',on_delete=models.CASCADE,verbose_name="Cours")
	eleves = models.ManyToManyField	('Eleve',blank=True,related_name="presence")
	clients = models.ManyToManyField("Client",blank=True, verbose_name="presence")
	class Meta:
		verbose_name="seance cours"
		ordering=['date','creneau']
	#date
	def __str__(self):
		str_cre=str(self.date)#timefield n'est pas un string ne peut étre retourné 
		return "Cours {0} {1} ".format(self.cours,str_cre)


class Seance_Coaching(Seance):
	session=models.ForeignKey('Session',on_delete=models.CASCADE,null=True,blank=True)
	eleve=models.ManyToManyField('Eleve',related_name="eleve_coaching",blank=True)
	coach=models.ForeignKey('Coach', verbose_name="Coach", on_delete=models.SET_NULL,null=True,blank=True)
	class Meta:
		verbose_name="seance coaching"
		ordering=['date','creneau']
	#date
	def __str__(self):
		str_cre=str(self.date)#timefield n'est pas un string ne peut étre retourné 
		return "Coaching {0} {1} ".format(self.session,str_cre)


############################################################### Contenu pédagogique ###############################################################
class Chapitre(models.Model):
	chapitre=models.CharField(max_length=50)
	session=models.ForeignKey('Session',on_delete=models.CASCADE,verbose_name="Session")
	details=models.TextField(blank=True,null=True,help_text='Précisions sur le chapitre')
	def __str__(self):
		return self.chapitre 
	class Meta:
		verbose_name="chapitre"
		ordering=['session','chapitre']

class Notions(models.Model):
	notion=models.CharField(max_length=50,verbose_name="Notion")
	details=models.TextField(blank=True,null=True,verbose_name="Details")
	chapitre=models.ForeignKey('Chapitre',on_delete=models.CASCADE)
	class Meta:
		verbose_name="notions"
		ordering=['chapitre','details']
	def __str__(self):
		return self.notion



##################################################################### Ressources #####################################################################
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




###################################################################   Signaux  #######################################################################
@receiver(post_save, sender=Frequence)
def spread_modification(sender, instance, **kwargs):
	
	if instance.has_cours():
		cours=instance.cours
		seances=cours.seance_cours_set.all()
		for seance in seances :
			seance.creneau=instance.creneau
			seance.save()
	
	
	

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
			
			
			elif instance.frequence.frequence =="Deux fois par semaine":
				for day in date_manager.two_times_weeks_period(instance.frequence.date_debut,    instance.frequence.date_limite,   instance.frequence.jour , instance.frequence.jour_two):
					Seance_Cours.objects.create(cours=instance,date=day,creneau=instance.frequence.creneau)

			elif instance.frequence.frequence =="Trois fois par semaine":
				for day in date_manager.three_times_weeks_period(instance.frequence.date_debut,    instance.frequence.date_limite,   instance.frequence.jour , instance.frequence.jour_two, instance.frequence.jour_three):
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
