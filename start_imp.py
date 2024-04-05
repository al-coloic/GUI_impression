# start_imp.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
from main_window_impression import MainWindowImpression


app = QApplication(sys.argv)


mainWindowBiblio = MainWindowImpression() #Constructin de la fenetre en appelant un autre fichier

mainWindowBiblio.show()
rc = app.exec_()

sys.exit(rc)
