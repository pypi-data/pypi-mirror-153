# -*- coding: utf-8 -*-
"""
Created on Fri May 27 08:57:30 2022

@author: NFactis
"""
def taille(liste):
    c=0
    for i in liste:
        c+=1
    return c

def minimum(liste):
    min=liste[0]
    for i in range(1,taille(liste)):
        if min>liste[1]:
            min=liste[1]
    return min
def maximum(liste):
    max=liste[0]
    for i in range(1,taille(liste)):
        if max<liste[1]:
            max=liste[1]
    return max

def somme(liste):
    sommeListe=0
    for i in range(0,taille(liste)):
        sommeListe+=liste[i]
    return sommeListe

def moyenne(liste):
    moyenne=somme(liste)/taille(liste)
    return moyenne
    

def mediane(liste):
    nlist=[]
    for i in range(0,taille(liste)):
        min=minimum(liste)
        nlist.append(min)
        liste.remove(min)
    
    if taille(nlist)%2==0:
        index1=taille(nlist)//2
        index2=index1-1
        med=(nlist[index1]+nlist[index2])/2
    else:
        index=(taille(nlist)//2)
        med=nlist(index)
    
    return med

def variance(liste):
    xi=0
    sce=0
    x=moyenne(liste)
    
    for i in range(0,taille(liste)):
        xi=(liste[i]-x)*(liste[i]-x)
        sce=sce+xi
        
        variance=sce/taille(liste)
    return variance

def ecart_type(liste):
    ecart=variance(liste)**(1/2)
    return ecart

