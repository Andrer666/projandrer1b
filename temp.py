import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optim
#----- variable globales -----#
bat_init = 0
bat_end = 1
E_Wmin = 100 # Wh
P_W= 3
t_init_s = 0
t_end_s = 0
pas_s = 15
n_i =  10 # 96
#-----------------------------#

def calcul_temps_charge_cont(): # calcul le temps nécessaire pour charger la batterie en fonction du taux de charge au début
    return (bat_end - bat_init)*E_Wmin/P_W

def liste_puissance_cont(t): # créer la liste des puissance*pas (colonne de la matrice)
    print(t)    
    n = int(t//pas_s)
    print(n)
    return [P_W*pas_s for k in range(n)]+[P_W*t%pas_s]

def indice_final(): # renvoie le nombre de quart d'heure nécessaire pour charger la batterie entièrement
    return (t_end_s - t_init_s)//pas_s 

def put_liste_somewhere(L,pos,taille=n_i):
    
    R=[]
    print(L)
    for k in range(pos):
      
        R+= [0]

    R+= L
    for k in range(taille-len(R)):
      
        R+= [0]
    return(np.array(R))
def transpose(L):
    P1 = np.array([[L[k]] for k in range(len(L))]) 
    return(P1)
L_P = liste_puissance_cont(calcul_temps_charge_cont())
i_end = indice_final()
I = np.eye(n_i) # Créer la matrice identité
P = put_liste_somewhere(L_P, 3)
P1 = transpose(P)
print(P1)
A = np.concatenate((I,P1),axis=1)

P = put_liste_somewhere(L_P, 4)
P1 = transpose(P)
print(P1)
A = np.concatenate((A,P1),axis=1)
print(A)
print(P1)
#---------- def courbes ----------# 
x = np.linspace(0,95,96)
prod = np.sin(x * 2 * 3.14 /48) + 1.0 
conso = np.cos(x * 2 * 3.14 /96) + 1.0 
plt.plot(x, prod)
plt.plot(x, conso)
plt.plot(x,-prod+conso)
#---------------------------------#

result = optim.milp(np.ones(96),
           integrality = np.zeros(96),
           bounds      = optim.Bounds(lb = 0, ub = np.inf),
           constraints = optim.LinearConstraint(I, conso - prod, ub = np.inf),
           )
plt.plot(x, result.x)
plt.show()

