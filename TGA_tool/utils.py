from django.db.models import Q
from TGA_tool.models import *

def init_langues():
    NIV=['English','Français','Español']
    print(len(NIV))
    for niv in NIV:
        Langue.objects.create_group(niv)
    

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
def init_sessions():
    Langues= Langue.objects.all()
    
    sessions={}
	#Dans cette partie on va créer un dictionnaire qui va contenir les Langues comme keys et les matiéres comme values 
    
    for langue in Langues:
        niveaux=[" A1"," A2"," B1"," B2"," C1"]
        sessions[langue.langue]=[]
        if langue.langue=='English':
            categories=["Adults","Teens","Kids"]
            types=["General","Business"]

            for categorie in categories:
               
                for niveau in niveaux:
                    
                    if categorie=="Adults":
                        
                        for typ in types:
                            sessions[langue.langue].append(typ + niveau)
                            print(sessions[langue.langue])
                            

                    else:
                        sessions[langue.langue].append("General for " + categorie + niveau)
                        
                    


        elif langue.langue=="Français":
            types=["général","des Affaires"]
           
            for niveau in niveaux:
                
                for typ in types:
                    sessions[langue.langue].append( typ + niveau )
                 



        elif langue.langue=="Español":
            categories=["Adultos","Adolescentes","Niños"]
            i=0
            for niveau in niveaux:
                i=0
                for categorie in categories:
                    sessions[langue.langue].append(" para " + categorie + niveau)
                    

        
    for groupe in Langues:
        for session in sessions[str(groupe)]:
            Session.objects.create_session(session,groupe)


def get_matches(list1,list2):
    matched=[]
    for element_1 in list1 :
        for element_2 in list2 :
            if element_1==element_2:
                matched.append(element_1)
    
    return matched
