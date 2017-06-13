# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 13:57:33 2017

@author: Dado
"""
from pression_altitude import *
from scipy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt

""" Integration equation différentielle: """

##Données à modifier!

def init():
    global z,m,T0,r
    z = float(input("Altitude au lancer [m]: "))
    m = float(input("Masse utile [kg]: "))
    T0 = float(input("Température au sol [K]: "))
    r = float(input("Rayon du ballon [m]: "))
    courbe(0,tmps)

z = 0  #Altitude au lancer [m]
m = 1.5  #Masse utile [kg]
T0 = 298 # Température au sol [K]
r = 0.8 #Rayon du ballon [m]          


def deriv(v,t):
    global z,m,T0,r
    f = Ft(v,r,z)
    V = volume(z,r,T0)
    Rhe = rho_he(z,T0-273.15)
    A = g(z)*(((rho_air(z,T0-273.15)*V)/((Rhe*V)+m))-1)
    mt = m + Rhe*V
    return A + (f/mt)

    
#Intervalle d'intégration

t0 = 0
tmax =7.5
npoints = 1000
tmps = linspace(t0,tmax,npoints)

# Condition initiale:
v0 = 0

#Graphe:

def courbe(v0,tmps,title = False):
    global z,m,T0,r
    solution = odeint(deriv,v0,tmps)
    v = solution[:,0]
    plt.plot(tmps,v)
    if title:
        plt.title("Masse sans gaz: "+str(m)+"kg; Rayon ballon: "+str(r)+"m; Température au sol: "+str(T0)+"K; Altitude au lancer: "+str(z)+"m")
    plt.xlabel("Temps [s]")
    plt.ylabel("Vitesse [m*s-1]")
    print ("vmax = "+str(round(v[-1],3))+"m/s.")
    #plt.show()
    
def simulation_rayon(R_max = 2):
    global r,m,T0,z
    print ("Simulation variation rayon! Pour m = "+str(m)+"kg; z = "+str(z)+"m; T0 = "+str(T0)+"K.")
    r_min = R_min(m,z,T0)
    for k in range(1,11):
        r = r_min + k*(R_max-r_min)/10 
        print("Rayon: "+str(round(r,3))+"m.")
        courbe(v0,tmps)
    plt.title("Simulation variation rayon! Pour m = "+str(m)+"kg; z = "+str(z)+"m; T0 = "+str(T0)+"K.\nAvec le rayon variant de "+str(r_min)+"m (bleu foncé), à "+str(r)+"m (bleu clair).")
        
def simulation_masse():
    global m,r,T0,z
    print ("Simulation variation masse! Pour r = "+str(r)+"m; z = "+str(z)+"m; T0 = "+str(T0)+"K.")
    m = 0
    for k in range(10):
        m = k*masse_max(r,z,T0)/9
        print("Masse: "+str(round(m,3))+"kg.")
        courbe(v0,tmps)
    plt.title("Simulation variation masse! Pour r = "+str(r)+"m; z = "+str(z)+"m; T0 = "+str(T0)+"K.\nAvec la masse variant de 0kg (bleu foncé), à "+str(m)+"kg (bleu clair).")

def simulation_temperature(T_init,delta_T = 100):
    global r,m,z,T0
    print ("Simulation variation temperature! Pour r = "+str(r)+"m; m = "+str(m)+"kg; z = "+str(z)+"m.")
    for k in range(1,11):
        T0 = T_init + k*(delta_T)/10
        print("Température: "+str(round(T0,3))+"K.")
        courbe(v0,tmps)
    plt.title("Simulation variation temperature! Pour r = "+str(r)+"m; m = "+str(m)+"kg; z = "+str(z)+"m\nAvec la temperature variant de "+str(T_init)+"K (bleu foncé), à "+str(T0)+"K (bleu clair)")
        
def simulation_altitude(delta_z,z_min=0):
    global m,r,T0,z
    print ("Simulation variation altitude! Pour r = "+str(r)+"m; m = "+str(m)+"kg; T0 = "+str(T0)+"K.")
    z = z_min
    for k in range(1,11):
        z = z_min + k*delta_z/10
        print("Altitude: "+str(round(z,3))+"m.")
        courbe(v0,tmps)
    plt.title("Simulation variation altitude! Pour r = "+str(r)+"m; m = "+str(m)+"kg; T0 = "+str(T0)+"K.\nAvec l'altitude variant de "+str(z_min)+"m (bleu foncé), à "+str(z)+"m (bleu clair).")
    
        
def altitude_temps(v0,tmax=3600,Rmax=2,z0=z):
    global z,m,T0,r
    tmps = linspace(0,tmax,tmax)
    solution = odeint(deriv,v0,tmps)
    vit = solution[:,0]
    alt = []
    dt = (tmax-t0)/npoints
    VolMax = (4/3)*pi*pow(Rmax,3)
    for k in range(len(tmps)):
        if volume(z0,r,T0) < VolMax:
            z0 += dt*vit[k]
            alt.append(z0)
    plt.plot(tmps[:len(alt)],alt)
    plt.axhline(y=max(alt), color='r', linestyle='--')
    plt.axvline(x=tmps[len(alt)], color='r', linestyle='--')
    plt.xlabel("Temps [s]")
    plt.ylabel("Altitude [m]")
    plt.title("Altitude au cours du temps.\nMasse sans gaz: "+str(m)+"kg; Rayon ballon: "+str(r)+"m; Température au sol: "+str(T0)+"K; Altitude au lancer: "+str(z)+"m")
    print("Altitude explosion: "+str(round(z0,2))+"m\nTemps explosion: "+str(round(tmps[len(alt)],2))+"s")
    return round(z0,3)

    
    