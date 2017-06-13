# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 19:05:01 2016

@author: Dado
"""

from xlrd import *
import os

def change_path(path): ### ex: path = "C://Windows//Win32"
    os.chdir(path)
    print (os.getcwd())


"""---Description: xls_to_list

   Renvoie une liste contenant les valeurs entre les lignes "start_row"
   et "finish_row", de la colonne "col" de la feuille indexée "index",
   dans la table "table". 
   
   --Attention: On doir etre dans le meme repertoire de travail
   dans lequel se trouve la table. Utiliser la fonction change_path()
   pour changer de repertoire de travail...--
   
   --Remarque: si on ne donne que l'argument "table" la fonction renvoie
   toutes les valeurs de la première colonne de la première feuille. """

def xls_to_list(table,col=0,start_row=0,finish_row=None,index=0):
    table = open_workbook(table)
    nfeuilles = table.nsheets
    nom_feuilles = table.sheet_names()
    if nfeuilles ==1 or index != 0:
        cell = table.sheet_by_index(index)
    elif nfeuilles !=1:
        print("Selectionner la feuille: ")
        for i in range(len(nom_feuilles)):
            print(i,": ",nom_feuilles[i])
        index = int(input("Feuille n: "))
        cell = table.sheet_by_index(index)
    cells = cell.col(col,start_row,finish_row)
    L = []
    for val in cells:
        L.append(val.value)
    return L

