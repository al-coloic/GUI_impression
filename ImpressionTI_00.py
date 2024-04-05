# 2022 loic.rondon@ac-aix-marseille.fr

import os, fnmatch
import csv
import time
import sys
from PyPDF2 import PdfMerger
from PyPDF2 import PdfFileReader
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *

# le répertoire source à changer si besoin
reper_sources='../TI - loic/'



def nbpagespdf(fichierpdf):
    """retourne le nombre de pages du fichier pdf"""
    with open(fichierpdf, "rb") as f:
        return PdfFileReader(f).getNumPages()

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


def compter_perso(source,classe):
    """A partir de la source et du numero de la classe, creer une liste des enonces et des palier"""
    enonce = []
    palier = []
    for row in source:
        q = str2int(row[classe])
        if q > 0:
            chemin_enonce = find('TI*'+row[1]+'*'+row[0]+'*énoncé*.pdf', reper_sources)
            chemin_palier = find('Palier*'+row[1]+'*'+row[0]+'*énoncé*.pdf', reper_sources)
            i = 0
            while (i < q):
                i=i+1
                enonce.extend(chemin_enonce)
                palier.extend(chemin_palier)
        else:
            next
    return enonce,palier

def compter_sol(source):
    solution = []
    for row in source:
        l = [str2int(row[3]),str2int(row[4]),str2int(row[5]),str2int(row[6])]
        if sum(l) > 0:
            chemin_sol = find('TI*'+row[1]+'*'+row[0]+'*solution*.pdf', reper_sources)
            for j in range(6):
                    solution.extend(chemin_sol)
        else:
            next
    return solution

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


EnsembleNoms=find('TI*énoncé*.pdf', reper_sources)
liste=[]
listeTheme=[]
print(len(EnsembleNoms))
for i in EnsembleNoms:
    x=i.split('/') # on découpe le chemin
    y=x[-1].split('-')
    theme=y[1].split(' ')
    if theme[1] not in listeTheme:
        listeTheme.append(theme[1])
    liste.append([i,theme[1],theme[2]])


liste2=sorted(liste,key=lambda x: x[1])
for i in liste2:
    print(i)

########################
