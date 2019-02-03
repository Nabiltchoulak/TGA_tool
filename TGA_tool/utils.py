from django.db.models import Q
from TGA_tool.models import *

def init_curriculums():
    NIV=['CP','CE','CE2','CM1','CM2','Sixième','Cinquième','Quatrième','DNB','Seconde','Première S','Première ES','Terminal S','Terminal ES']
    print(len(NIV))
    for niv in NIV:
        Curriculum.objects.create_group(niv)
    

def init_creneaux():
    
    CRE=[]#Nous allons parcourir les séances de la journée

    for i in range(2):#Séances de la matinée i=0 / ceux de l'aprem i=1
        init_hour=8 + 5*i
        for j in range(3+i):
            if j%2==0 and j>0:#ex: 9h30-11h00
                init_hour+=2
            else :
                if j>0 : 
                    init_hour+=1#ex: 8h00-9h30 
            CRE.append(time(hour=init_hour,minute= (30*j)%60))
    #Si on n'a pas de créneau crée le tout 
    ########################################################################
        
    for cren in CRE:
        Creneau.objects.create_creneau(cren)
		#print(Creneau.objects.get())"""


#Cette partie est dédiée pour générer les instances connues déjà de matière 
#dés que le serveur commence a tourner on a un problème de "Models aren't loaded yet"
#On va régler cela avec les middleware 
def init_matieres():
    curriculum= Curriculum.objects.all()
    matieres={}
	#Dans cette partie on va créer un dictionnaire qui va contenir les curriculums comme keys et les matiéres comme values 
    for niveau in curriculum:
        matieres[niveau.niveau]=["Mathématiques","Physique","SVT","Français","Anglais"]
        if niveau.niveau=='Sixieme'or niveau.niveau=='Cinquieme'or niveau.niveau=='Quatrieme'or niveau.niveau=='DNB':
            matieres[niveau.niveau].append("Technologie")
        elif niveau.niveau=='CP'or niveau.niveau=='CE'or niveau.niveau=='CE2'or niveau.niveau=='CM1'or niveau.niveau=='CM2':
            matieres[niveau.niveau].remove("Physique")
            matieres[niveau.niveau].remove("SVT")
        elif niveau.niveau=='Terminal S' or niveau.niveau=='Terminal ES':
            matieres[niveau.niveau].append("Philosophie")
        elif niveau.niveau=='Première ES' or niveau.niveau=='Terminal ES':
            matieres[niveau.niveau].append("SES")
        
    

    
    for groupe in curriculum:
        for matiere in matieres[str(groupe)]:
            Matiere.objects.create_matiere(matiere,groupe)