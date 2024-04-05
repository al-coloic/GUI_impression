# main_window_impression.py
# avec mise en page par layout

from PyQt5.QtWidgets import QMainWindow,QHBoxLayout, QVBoxLayout,QWidget,QLabel,QLineEdit,QPushButton,QApplication,QTabWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
import sys,os,fnmatch,time,csv
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

from fiches import *

class MainWindowImpression(QMainWindow):
	"""La fenêtre pour imprimer les fiches
	"""
	def __init__(self):
		# La création de la fenêtre
		super(MainWindowImpression,self).__init__()
		self.resize(600,450)
		self.setWindowTitle("Impression")
		# Le chemin de répertoire de travail
		self.path='Veuillez choisir le répertoire de travail'


		#Une barre de statut en bas de la fenêtre
		self.status = QStatusBar()
		self.setStatusBar(self.status)

		#La barre d'outils
		barreOutils = QToolBar("Répertoire")
		barreOutils.setIconSize(QSize(16, 16))
		self.addToolBar(barreOutils)
		menuFichier = self.menuBar().addMenu("&Répertoire")
		OuvrirFichier_action = QAction(QIcon('ouvrir.png'), "Ouvrir répertoire...", self)
		OuvrirFichier_action.setStatusTip("Ouvrir Répertoire")
		OuvrirFichier_action.triggered.connect(self.file_open)
		menuFichier.addAction(OuvrirFichier_action)
		barreOutils.addAction(OuvrirFichier_action)

		# les éléments de la fenêtre principale
		# contient le chemin
		self.espaceFenetre1 = QWidget(self)
		# contient le tableau et le bouton, emboité dans l'espace précédent
		self.espaceFenetre2 = QWidget(self)

		# Affichage du chemin choisi
		self.cheminChoisi = QLabel(self.path,self)
		# le layout du premier espace
		self.layout1 = QVBoxLayout()
		self.layout1.addWidget(self.cheminChoisi)
		self.layout1.addWidget(self.espaceFenetre2)
		self.espaceFenetre1.setLayout(self.layout1)
		self.setCentralWidget(self.espaceFenetre1)
##################################################################################################""
	def imprimerPdf(self):
		QFileDialog.getSaveFileName
		output = PdfFileWriter()
		for f in self.tab_widget.LLL.NivB:
			pdf_in = open(f.adresse, 'rb')
			pdf_file = PdfFileReader(pdf_in)
			for j in range(f.exemplaire):
				output.append_pages_from_reader(pdf_file)
				if f.paritePage:
					output.add_blank_page()

		output.write(QFileDialog.getSaveFileName(self, 'Save File'))


##########################################################################################
























	def file_open(self):
		""" la fonction qui permet de choisir le dossier de travail, à modifier pour intégrer les erreurs
		"""
		path = str(QFileDialog.getExistingDirectory(self, "Choisir le répertoire"))
		self.path = path
		self.cheminChoisi.setText(path)
		# Une fois le chemin choisi on peut créer la table
		self.creationBDD()

	def creationBDD(self):
		""" Permet de créer le tableau à partir de la base de données reconstruite
		"""
		self.fiches = ListeTI(self.path)
		# Création de la table
		self.tab_widget = MaTableWidget(self,self.path)
		self.buttonOK = QPushButton(self,clicked = self.imprimerPdf)
		self.buttonOK.setText("Créer le pdf")
		# Organisation des éléments de la fenêtre
		self.layout2 = QVBoxLayout()
		self.layout2.addWidget(self.tab_widget)
		self.layout2.addWidget(self.buttonOK)
		self.espaceFenetre2.setLayout(self.layout2)



class MaTableWidget(QTabWidget):
	""" La classe qui permet de créer les 3 onglés B, C, D à partur de la bdd LLL et qui
	permet d'obtenir le nombres d'exemplaires désirés pour chaque fichier
	"""
	def __init__(self, parent,path):
		super(QTabWidget, self).__init__(parent)
		# Taille de la fenetre
		self.resize(600, 400)
		# création de la base de données
		self.LLL = ListeTI(path)
		# construction du dictionnaire des spin associé à chaque nom de fichier
		self.spinner = {}

		# création des barres de défilemens
		self.scrollbarB = QScrollArea(widgetResizable=True)
		self.scrollbarC = QScrollArea(widgetResizable=True)
		self.scrollbarD = QScrollArea(widgetResizable=True)


		# On crée les feuilles du classeurs
		self.nivB = QWidget()
		self.nivC = QWidget()
		self.nivD = QWidget()

        # On attache les barres  de défilements au classeur
		self.addTab(self.scrollbarB,"Niveau B")
		self.addTab(self.scrollbarC, "Niveau C")
		self.addTab(self.scrollbarD, "Niveau D")

		# On crée les différentes table
		self.creationNivB(path)
		self.creationNivC(path)
		self.creationNivD(path)

	def MiseAJourValeur(self,a,b):
		"""met à jour la valeur du nombre d'exemplaire désiré après la modification de l'une des spinbox"""
		a.exemplaire = b.value()


	def creationNivB(self,path):
		"""creation du contenu de l'onglet B"""
		disposition = QFormLayout()
		# on rempli le dictionnaire des spin en bouclant sur la bdd LLL
		for a in self.LLL.NivB:
			"""on boucle sur toutes les fiches du niveau choisi, on rempli le dictionnaire des spinner, des champs"""
			self.spinner[a.nomFichier] = QSpinBox(self)
			b = self.spinner[a.nomFichier]
			disposition.addRow(a.theme+" "+a.niveau,self.spinner[a.nomFichier] )
			b.valueChanged.connect(partial(self.MiseAJourValeur,a,b))

		self.setTabText(0, "Niveau B")
		self.nivB.setLayout(disposition)
		self.scrollbarB.setWidget(self.nivB)

	def creationNivC(self,path):
		"""creation du contenu de l'onglet C"""
		disposition = QFormLayout()
		# on rempli le dictionnaire des spin en bouclant sur la bdd LLL
		for a in self.LLL.NivC:
			"""on boucle sur toutes les fiches du niveau choisi, on rempli le dictionnaire des spinner, des champs"""
			self.spinner[a.nomFichier] = QSpinBox(self)
			b = self.spinner[a.nomFichier]
			disposition.addRow(a.theme+" "+a.niveau,self.spinner[a.nomFichier] )
			b.valueChanged.connect(partial(self.MiseAJourValeur,a,b))

		self.setTabText(1, "Niveau C")
		self.nivC.setLayout(disposition)
		self.scrollbarC.setWidget(self.nivC)

	def creationNivD(self,path):
		"""creation du contenu de l'onglet D"""
		disposition = QFormLayout()
		# on rempli le dictionnaire des spin en bouclant sur la bdd LLL
		for a in self.LLL.NivD:
			"""on boucle sur toutes les fiches du niveau choisi, on rempli le dictionnaire des spinner, des champs"""
			self.spinner[a.nomFichier] = QSpinBox(self)
			b = self.spinner[a.nomFichier]
			disposition.addRow(a.theme+" "+a.niveau,self.spinner[a.nomFichier] )
			b.valueChanged.connect(partial(self.MiseAJourValeur,a,b))

		self.setTabText(2, "Niveau D")
		self.nivD.setLayout(disposition)
		self.scrollbarD.setWidget(self.nivD)


# class PdfCompile:
# 	def __init__(self):
#
#
# 	def compilateur(titre,liste):
# 	    merger = PdfMerger()
# 	    for pdf in liste:
# 	        if self.pariteDesPages:
# 	            merger.append(pdf)
# 	            merger.append('./blanche.pdf')
# 	        else:
# 	            merger.append(pdf)
#
# 	        merger.write(titre)
# 	        merger.close()
