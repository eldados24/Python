# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 19:15:51 2016

@author: Dado
"""

from math import exp,pi,pow

## Calcul de la pression atmosphérique à une altitude z: p(z)

## Constantes globales: 
    
R = 8.314 #[J·K-1·mol-1]
Mair = 0.029 #[kg/mol]
Mhe = 0.004 #[kg/mol]
P0 = 101325 #[Pa]
G = 6.67384*10**(-11) #[m3/(kg*s2)]
m_terre = 5.9722*10**24 #[kg]
r_terre = 6.371*10**6 #[m]


### Fonctions:

def g(z):
    g = lambda z: G*m_terre/((r_terre+z)**2)
    return round(g(z),4)


def p(z,T=20):
    """ Renvoie la pression atmosphérique à l'altitude z, en Pa"""
    p = lambda z: P0*exp(-z*((Mair*g(z))/(R*(t(z,T)+273.15))))   
    return round (p(z),2)
 
def t(z,T0=20): ##Attention! z < 32162 m
    """ Renvoie la température (°C) à une altitude z (m) donnée et une température au sol T0 (°C) donnée"""
    if z <= 11000:
        T = T0 - (6.5*0.001*z)
    elif z > 11000 and z < 20000:
        T = T0 - 71.5
    elif z >= 20000 and z <= 32162:
        TS = T0 - 71.5
        T = TS + 0.001*(z-20000)
    else:
        return "Altitude excessive!!"
    return round(T,4)

def t_p(z,T0):  ## T [°C] ; P [hPa]
    P = p(z)
    T = t(z,T0)
    TP = {"T": T, "P": P} 
    return TP

def rho_air(z,T0=20):   ## T [°C]   Attention! z < 32162 m
    global R,Mair
    P = p(z,T0)
    T = t(z,T0) + 273.15
    rho = lambda P,T: (P*Mair)/(R*T)
    return round(rho(P,T),4) ## [kg/m3]

def rho_he(z,T0=20):   ## T [°C] , z[m]
    global R,Mhe
    P = p(z,T0)
    T = t(z,T0) + 273.15
    rho = lambda P,T: (P*Mhe)/(R*T)
    return round(rho(P,T),4) ## [kg/m3]

def volume_nécessaire(m,z=0,T0=298): ##Renvoie le volume nécessaire, en m3, à faire décoller une masse m [kg], à partir de l'altitude z et à température T0
    return round((m/(rho_air(z,T0)-rho_he(z,T0))),4)

def R_min(m,z=0,T0=298): ##Renvoie le rayon minimal du ballon nécessaire à soulever une masse de m [kg]
    delta_rho = rho_air(z,T0)-rho_he(z,T0)
    return round(pow((3*m)/(4*pi*delta_rho),1/3.0),3)

def masse_max(r,z=0,T0=298): ##Renvoie la masse maximale soulevée par un ballon de rayon r[m], à l'altitude z[m], température T0 [K]
    return round((rho_air(z,T0)-rho_he(z,T0))*volume(z,r,T0),3)

def volume(z,r=0.8,T0=298):
    """Renvoie le volume du ballon, initialment gonflé au rayon r, à l'altitude z.
    Rq: Pour une enveloppe Howyee 800gr: r0=2.3m """
    #On suppose le gaz comme parfait
    V0 = (4/3)*pi*(r**3)
    Vol = (P0*V0/(p(z,(T0-273.15))))*(t(z,T0)/T0)
    return round(Vol,4) #[m3]

def rayon_volume(vol):
    R = pow((3*vol)/(4*pi),1/3.0)
    return round(R,3)

def Re(v,L,z=0,eta=1.8e-05):
    return rho_he(z)*v*L/eta

def Ft(v,L,z=0,Cx=0.5):
    return -0.5*rho_air(z)*Cx*pi*(L**2)*(v**2)
    

    
