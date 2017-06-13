# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 20:20:48 2017

@author: Dado
"""

from pression_altitude import *
import numpy as np
import matplotlib.pyplot as plt
from xls_python import *
from equa_diff import *



def simulation_pression_xls(table,col=0,start_row=1,finish_row=None,index=0):
    altitude = xls_to_list(table,col,start_row,finish_row,index)
    pression = []
    for z in altitude:
        pression.append(p(z))
    return (altitude,pression)
    
def simulation_pression(H):
    P_S = []
    for z in H:
        P_S.append(p(z))
    return P_S
    
def simulation_temperature_xls(table,T0=15,col=0,start_row=1,finish_row=None,index=0):
    altitude = xls_to_list(table,col,start_row,finish_row,index)
    temperature = []
    for z in altitude:
        temperature.append(t(z,T0))
    return (altitude,temperature)
    
def ecart(L1,L2):
    Lec = []
    for k in range(min(len(L1),len(L2))):
        Lec.append(round((L1[k]-L2[k]),3))
    return Lec
    
    

    
def trace(xy,titre="Courbe",names=(None,None)):
    x = np.array(xy[0])
    y = np.array(xy[1])
    plt.plot(x,y)  
    plt.title(titre)
    plt.xlabel(names[0])
    plt.ylabel(names[1])  
    plt.show()
    
def reglage(x,y,same_lenght=True):
    """Prend en argument deux listes d'entiers (ou flottants), et renvoie un tuple de ces deux listes tels
    toutes les valeurs non numeriques des listes sont remplacées par la moyenne des valeurs precedent et suivant 
    la valeur non numérique. Si same_lenght == True (par défaut), les listes renvoyees auront la meme longuer,
    la liste la plus courte sera rallongee en ajoutant autant de fois que possible la derniere valeur de la liste."""
    modif =''
    for k in range(len(x)-1):
       if type(x[k])!= int and type(x[k])!= float:
           x[k]=round(((x[k-1]+x[k+1])/2),3)
    for k in range(len(y)-1):
       if type(y[k])!= int and type(y[k])!= float:
           print (k)
           y[k]=round(((y[k-1]+y[k+1])/2),3)
    if same_lenght:
        if len(x)!=len(y):
            M = max(len(x),len(y))
            m = min(len(x),len(y))
            if len(x)<len(y):
                L = x
                modif = "x"
            else:
                L = y
                modif = "y"
                
            dernier = L[m]
            for k in range(m,M):
                L.append(dernier)
            if modif =="x":
                return(L,y)
            else:
                return(x,L)
    return(x,y)

            


