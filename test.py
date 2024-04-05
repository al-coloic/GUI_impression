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
reper_sources="/home/loic/Documents/prog/TI - loic"

# def paritePage(cheminFichier):
# 	"""retourne le nombre de pages du fichier pdf"""
#     with open(cheminFichier, "rb") as f:
#         return PdfFileReader(f).getNumPages()%2

def nomFichier(a):
    x = a.split('/')
    return x[len(x)-1]

def extraireThemeEtNiv(a):
    x = a.split(' - ')
    y = x[1]
    return y.split(' ')

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


# chemin_enonce = rechercheFiche('TI','énoncé',reper_sources)
# listeFiches=[]
# listeThemes=[]
# for i in chemin_enonce:
#     a = extraireThemeEtNiv(nomFichier(i))
#     if a[0] not in listeThemes:
#         listeThemes.append(a[0])
#     z = (i,nomFichier(i),a[0],a[-1])
#     listeFiches.append(z)

# print(listeFiches)

# sorted(z,key=lambda student: student[1])

# listeOrdo=sorted(listeFiches,key=itemgetter(1,2))


# for i in listeOrdo:
#     print(i[-2],i[-1])


# avec les class
class FicheTI:
    def __init__(self,adresse):
        self.adresse = adresse
        self.nomFichier = self.nomFichier()

    def nomFichier(self):
        x = self.adresse.split('/')
        return x[len(x)-1]

    def __repr__(self):
        return repr((self.adress))

chemin_enonce = rechercheFiche('TI','énoncé',reper_sources)
listeFiches=[]
listeThemes=[]
for i in chemin_enonce:
    listeFiches.append(FicheTI(i))
    print(FicheTI(i))
    # a = extraireThemeEtNiv(nomFichier(i))
    # if a[0] not in listeThemes:
    #     listeThemes.append(a[0])
    # z = (i,nomFichier(i),a[0],a[-1])

#
# liste_Fiche = []
#
# listeOrdo=sorted(listeFiches,key=attrgetter('theme','niveau'))


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
