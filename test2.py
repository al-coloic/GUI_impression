# 2022 loic.rondon@ac-aix-marseille.fr

import os, fnmatch
import csv
import time
import sys
from PyPDF2 import PdfMerger
from PyPDF2 import PdfFileReader
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
from operator import itemgetter,attrgetter

# le répertoire source à changer si besoin
reper_sources="/mnt/7c591785-501f-40d9-b199-f95fe2f9ce24/nextcloud académie/TI - loic"


def str2int(chaine):
    """converti un string en integer, 0 si la chaine est vide"""
    if chaine =='':
        return 0
    else:
        return int(chaine)

def find(pattern, path):
    """cherche un fichier pattern dans le chemin path"""
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def rechercheFiche(a,b,rep_s):
    return find(a+'*'+'*'+b+'.pdf', rep_s)


class FicheTI:
    """Une fiche que ce soit TI ou palier énoncé ou corrigé avec :
    - adresse
    - nom du fichier
    - genre
    - theme
    - niveau
    """

    def __init__(self,adresse,genre):
        self.adresse = adresse
        self.nomFichier = self.nomFichier()
        self.extraireThemeEtNiv()
        # self.paritePage()
        self.genre = genre
        self.exemplaire = 0

    def nomFichier(self):
        """pour trouver le nom du fichier"""
        x = self.adresse.split('/')
        return x[len(x)-1]

    def extraireThemeEtNiv(self):
        """pour extraire theme et niveau"""
        x = self.nomFichier.split(' - ')
        y = x[1]
        z = y.split(' ')
        self.theme = z[0]
        self.niveau = z[-1]

    # def paritePage(self):
    #     """retourne le nombre de pages du fichier pdf"""
    #     with open(self.adresse, "rb") as f:
    #         self.paritePage = PdfReader(f).getNumPages()%2


    def __repr__(self):
        return repr((
            self.adresse,
            self.nomFichier,
            self.theme,
            self.niveau,
            self.genre))

class ListeTI:
    """la classe qui regroupe toutes les fiches TI d'un même genre :
    - avec la liste des thèmes
    - la liste Ordonnée par thème puis niveau"""
    def __init__(self,reper_sources):
        chemin_enonce = rechercheFiche('TI','énoncé',reper_sources)
        listeFiches=[]
        self.listeThemes=[]
        for i in chemin_enonce:
            a = FicheTI(i,'énoncé')
            listeFiches.append(a)
            if a.theme not in self.listeThemes:
                self.listeThemes.append(a.theme)

        self.listeOrdo = sorted(listeFiches,key=attrgetter('theme','niveau'))

        self.NivB=[]
        self.NivC=[]
        self.NivD=[]
        for i in self.listeOrdo:
            x = i.niveau[0]
            match x:
                case 'B':
                    self.NivB.append(i)
                case 'C':
                    self.NivC.append(i)
                case 'D':
                    self.NivD.append(i)


# maintenant : ça marche avec des tableaux, il faut construire une class pour les fiches, ce qu'on avait commencé à faire
# les class se trie sur les attributs avec attrgetter

def compilateur(titre,liste):
    merger = PdfMerger()
    for pdf in liste:
        parite_page = nbpagespdf(pdf) % 2
        if parite_page:
            merger.append(pdf)
            merger.append('./blanche.pdf')
        else:
            merger.append(pdf)

        merger.write(titre)
        merger.close()


# EnsembleNoms=find('TI*énoncé*.pdf', reper_sources)
# liste=[]
# listeTheme=[]
# print(len(EnsembleNoms))
# for i in EnsembleNoms:
#     x=i.split('/') # on découpe le chemin
#     y=x[-1].split('-')
#     theme=y[1].split(' ')
#     if theme[1] not in listeTheme:
#         listeTheme.append(theme[1])
#     liste.append([i,theme[1],theme[2]])
#
#
# liste2=sorted(liste,key=lambda x: x[1])
# for i in liste2:
#     print(i)

########################
# def nbpagespdf(fichierpdf):
#     """retourne le nombre de pages du fichier pdf"""
#     with open(fichierpdf, "rb") as f:
#         return PdfFileReader(f).getNumPages()
