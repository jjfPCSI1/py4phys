# coding: latin1

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.
# 
# Si l'encodage vous pose problème, vous pouvez réencoder le fichier à l'aide 
# de la commande
# 
# recode l1..utf8 monfichier.py
# 
# Il faudra alors modifier la première ligne en # coding: utf8
# pour que Python s'y retrouve.




"""
Created on Wed Oct 29 16:03:32 2014

@author: Yohan LOQUAIS

Travail realise par Yohan Loquais (PC, Lycee Fabert, Metz) permettant de
visualiser les parametres d'optimisation pour la synthese de l'ammoniac.

Dans la version 1, on peut faire varier la pression, la temperature et les
quantites de matiere initiales de N2 ou H2.

Dans la version 2, on peut faire varier la pression, la temperature et la
quantite de matiere de gaz initiale et le rapport n(H2)/n(N2). Ce qui permet
de pouvoir faire varier la composition du systeme avec une quantite de matiere
fixee.

Attention, cela demande que les modules Pyside et PyQt4 soient installes sur
la machine pour fonctionner. Ainsi que Python3.

"""

import sys

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#--------------------Definition du graphe---------------------------
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        
        #t = np.arange(0.0, 3.0, 0.01)
        #s = np.cos(2*np.pi*t)
        #self.axes.plot(t,s)
        
        FigureCanvas.__init__(self, self.fig)

        #----Creation des tableaux de donnees-----        
        self.tableau_parametre = []
        self.tableau_rdt = []
        self.tableau_xNH3 = []
        
        self.l_tableau_rdt, = self.axes.plot(self.tableau_parametre, self.tableau_rdt, label="Rendement")
        self.l_tableau_xNH3, = self.axes.plot(self.tableau_parametre, self.tableau_xNH3, label="x(NH3)")        
        self.axes.legend()
        self.axes.set_ylim(0.0, 1.0)
        self.axes.set_xlabel("Rapport initial n(H2)/n(N2)")
        
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        


#-----------------Definition de la fenêtre---------------------------
class FenetrePrincipale(QWidget):
    def __init__(self):
        QWidget.__init__(self)
    
        #------------Creation des spinbox avec les parametres initiaux------------
        #--Nombre de moles initial--
        self.doubleSpinBox_n_init = QDoubleSpinBox()
        self.doubleSpinBox_n_init.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_n_init.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_n_init.setSuffix(" mol")
        self.doubleSpinBox_n_init.setDecimals(1)
        self.doubleSpinBox_n_init.setRange(0.1,1000.0)
        self.doubleSpinBox_n_init.setValue(4.0)
    
        #--Rapport n(H2)/n(N2)--
        self.doubleSpinBox_rapportH2N2 = QDoubleSpinBox()
        self.doubleSpinBox_rapportH2N2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_rapportH2N2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_rapportH2N2.setDecimals(3)
        self.doubleSpinBox_rapportH2N2.setRange(0.001,1000.0)
        self.doubleSpinBox_rapportH2N2.setValue(3.0)
        self.doubleSpinBox_rapportH2N2.setEnabled(False)
    
        #--Pression totale--
        self.doubleSpinBox_Ptot = QDoubleSpinBox()
        self.doubleSpinBox_Ptot.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_Ptot.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_Ptot.setSuffix(" bar")
        self.doubleSpinBox_Ptot.setDecimals(1)
        self.doubleSpinBox_Ptot.setRange(0.1,200.0)
        self.doubleSpinBox_Ptot.setValue(1.0)
    
        #--Temperature--
        self.doubleSpinBox_T = QDoubleSpinBox()
        self.doubleSpinBox_T.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_T.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_T.setSuffix(" K")
        self.doubleSpinBox_T.setDecimals(0)
        self.doubleSpinBox_T.setRange(1.0,1500.0)
        self.doubleSpinBox_T.setValue(300.0)
    
        #--Layout--
        self.glayout_P_T = QGridLayout()
        self.glayout_P_T.addWidget(QLabel("<b>Parametres initiaux :<\b>"),0,0,1,-1)
        self.glayout_P_T.addWidget(QLabel("n(N2) + n(H2) :"),1,0,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_n_init,1,1,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("Pression :"),1,3,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_Ptot,1,4,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("n(H2) / n(N2) :"),2,0,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_rapportH2N2,2,1,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("Temperature :"),2,3,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_T,2,4,QtCore.Qt.AlignRight)    
    
        #---------Creation du parametre a faire varier---------
        self.radio_ntot = QRadioButton("n(N2) + n(H2)")        
        self.radio_rapportH2N2 = QRadioButton("n(H2)/n(N2)")
        self.radio_rapportH2N2.setChecked(True)        
        self.radio_Ptot = QRadioButton("Pression")
        self.radio_T = QRadioButton("Temperature")
        self.connect(self.radio_ntot, SIGNAL("toggled(bool)"), self.slot_radio_ntot)
        self.connect(self.radio_rapportH2N2, SIGNAL("toggled(bool)"), self.slot_radio_rapportH2N2)   
        self.connect(self.radio_Ptot, SIGNAL("toggled(bool)"), self.slot_radio_Ptot)
        self.connect(self.radio_T, SIGNAL("toggled(bool)"), self.slot_radio_T)
    
        self.glayout_radio = QGridLayout()
        self.glayout_radio.addWidget(self.radio_ntot,0,0)
        self.glayout_radio.addWidget(self.radio_rapportH2N2,1,0)
        self.glayout_radio.addWidget(self.radio_Ptot,0,1)
        self.glayout_radio.addWidget(self.radio_T,1,1)
    
        self.doubleSpinBox_variation_1 = QDoubleSpinBox()
        self.doubleSpinBox_variation_1.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_1.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_rapportH2N2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_rapportH2N2.minimum(),self.doubleSpinBox_rapportH2N2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_rapportH2N2.minimum())
    
        self.doubleSpinBox_variation_2 = QDoubleSpinBox()
        self.doubleSpinBox_variation_2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_rapportH2N2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_rapportH2N2.minimum(),self.doubleSpinBox_rapportH2N2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_rapportH2N2.maximum())
    
        self.hlayout_variation_1 = QHBoxLayout()
        self.hlayout_variation_1.addWidget(QLabel("Faire varier le parametre de "))
        self.hlayout_variation_1.addWidget(self.doubleSpinBox_variation_1)
        self.hlayout_variation_1.addWidget(QLabel(" a "))
        self.hlayout_variation_1.addWidget(self.doubleSpinBox_variation_2)
    
        self.doubleSpinBox_variation_pas = QDoubleSpinBox()
        self.doubleSpinBox_variation_pas.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_pas.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_rapportH2N2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_rapportH2N2.minimum(),self.doubleSpinBox_rapportH2N2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_rapportH2N2.minimum())
    
        self.hlayout_variation_2 = QHBoxLayout()
        self.hlayout_variation_2.addWidget(QLabel("Par pas de "))
        self.hlayout_variation_2.addWidget(self.doubleSpinBox_variation_pas)
    
        #--------------------Bouton calculer-------------------
        self.bouton_calculer = QPushButton("Calculer")
        self.connect(self.bouton_calculer, SIGNAL("clicked(bool)"), self.slot_calculer)
        
        #----------------------Zone texte---------------------- 
        self.texte_resultat = "n(H2)/n(N2)     xi/xi_max     x(NH3)"
        
        self.plaintext_resultat = QPlainTextEdit()
        self.plaintext_resultat.setReadOnly(True)
        self.plaintext_resultat.setPlainText(self.texte_resultat)
        
        #--------------------Layout gauche---------------------
        self.vlayout_parametres = QVBoxLayout()
        self.vlayout_parametres.addWidget(QLabel("N2 (g) + 3 H2 (g) = 2 NH3 (g)"),0,QtCore.Qt.AlignHCenter)
        self.vlayout_parametres.addLayout(self.glayout_P_T)
        self.vlayout_parametres.addSpacing(20)
        self.vlayout_parametres.addWidget(QLabel("<b>Variation d'un des parametres initiaux :<\b>"))
        self.vlayout_parametres.addLayout(self.glayout_radio)
        self.vlayout_parametres.addLayout(self.hlayout_variation_1)
        self.vlayout_parametres.addLayout(self.hlayout_variation_2)
        self.vlayout_parametres.addSpacing(20)
        self.vlayout_parametres.addWidget(self.bouton_calculer)
        self.vlayout_parametres.addSpacing(20)
        self.vlayout_parametres.addWidget(self.plaintext_resultat)
    
        #--------------------Layout droite---------------------
        self.qmc = MplCanvas(self)
        self.ntb = NavigationToolbar(self.qmc, self)
    
        self.vlayout_graphe = QVBoxLayout()
        self.vlayout_graphe.addWidget(self.qmc)
        self.vlayout_graphe.addWidget(self.ntb)
    
        #------------------Layout principal--------------------
        self.hlayout_principal = QHBoxLayout()
        self.hlayout_principal.addLayout(self.vlayout_parametres)
        self.hlayout_principal.addLayout(self.vlayout_graphe)
        self.hlayout_principal.setStretch(0,1)        
        self.hlayout_principal.setStretch(1,5)
        
        self.vlayout_principal = QVBoxLayout()
        self.vlayout_principal.addLayout(self.hlayout_principal)
        self.vlayout_principal.addWidget(QLabel("Y. Loquais"),0,QtCore.Qt.AlignRight)
    
        self.setLayout(self.vlayout_principal)

    #----------------------------slots radio-------------------------------
    def slot_radio_ntot(self):
        self.doubleSpinBox_n_init.setEnabled(False)
        self.doubleSpinBox_rapportH2N2.setEnabled(True)
        self.doubleSpinBox_Ptot.setEnabled(True)    
        self.doubleSpinBox_T.setEnabled(True)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_n_init.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_n_init.minimum(),self.doubleSpinBox_n_init.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_n_init.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_n_init.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_n_init.minimum(),self.doubleSpinBox_n_init.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_n_init.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_n_init.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_n_init.minimum(),self.doubleSpinBox_n_init.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_n_init.minimum())
        self.qmc.axes.set_xlabel("Quantite de matiere totale initiale n(N2) + n(H2) (en mol)")
        
    def slot_radio_rapportH2N2(self):
        self.doubleSpinBox_n_init.setEnabled(True)
        self.doubleSpinBox_rapportH2N2.setEnabled(False)
        self.doubleSpinBox_Ptot.setEnabled(True)    
        self.doubleSpinBox_T.setEnabled(True)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_rapportH2N2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_rapportH2N2.minimum(),self.doubleSpinBox_rapportH2N2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_rapportH2N2.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_rapportH2N2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_rapportH2N2.minimum(),self.doubleSpinBox_rapportH2N2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_rapportH2N2.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_rapportH2N2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_rapportH2N2.minimum(),self.doubleSpinBox_rapportH2N2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_rapportH2N2.minimum())
        self.qmc.axes.set_xlabel("Rapport initial n(H2)/n(N2)")        
        
    def slot_radio_Ptot(self):
        self.doubleSpinBox_n_init.setEnabled(True)
        self.doubleSpinBox_rapportH2N2.setEnabled(True)
        self.doubleSpinBox_Ptot.setEnabled(False)    
        self.doubleSpinBox_T.setEnabled(True)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_Ptot.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_Ptot.minimum(),self.doubleSpinBox_Ptot.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_Ptot.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_Ptot.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_Ptot.minimum(),self.doubleSpinBox_Ptot.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_Ptot.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_Ptot.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_Ptot.minimum(),self.doubleSpinBox_Ptot.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_Ptot.minimum())
        self.qmc.axes.set_xlabel("Pression totale (en bar)")
        
    def slot_radio_T(self):
        self.doubleSpinBox_n_init.setEnabled(True)
        self.doubleSpinBox_rapportH2N2.setEnabled(True)
        self.doubleSpinBox_Ptot.setEnabled(True)    
        self.doubleSpinBox_T.setEnabled(False)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_T.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_T.minimum(),self.doubleSpinBox_T.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_T.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_T.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_T.minimum(),self.doubleSpinBox_T.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_T.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_T.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_T.minimum(),self.doubleSpinBox_T.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_T.minimum())
        self.qmc.axes.set_xlabel("Temperature (en K)")
        
    def slot_calculer(self):
        xi = 0.0
        xi_max = 0.0
        delta_r_H0 = 92600.0 / 8.314
        delta_r_S0 = 198.7 / 8.314
        k0 = 0.0
        i = self.doubleSpinBox_variation_1.value()
        x_NH3 = 0.0
        precision = 4
        n_N2_init = 0.0
        n_H2_init = 0.0
        self.qmc.tableau_parametre.clear()
        self.qmc.tableau_rdt.clear()
        self.qmc.tableau_xNH3.clear()
        
        #----------------------Variation de la temperature---------------------
        if self.radio_T.isChecked() == True :
            n_N2_init = self.doubleSpinBox_n_init.value() / (1 + self.doubleSpinBox_rapportH2N2.value())
            n_H2_init = self.doubleSpinBox_n_init.value() * self.doubleSpinBox_rapportH2N2.value() / (1 + self.doubleSpinBox_rapportH2N2.value())
            xi_max = np.minimum(n_N2_init, n_H2_init/3.0)

            self.texte_resultat = "  T          xi/xi_max     x(NH3)\n"
            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value():
                self.qmc.tableau_parametre.append(i)
                #--Calcul de la constante standard d'equilibre--
                k0 = np.exp(delta_r_H0 / i - delta_r_S0)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (n_N2_init + n_H2_init - 2*xi)**2 / ((n_N2_init - xi) * (n_H2_init -3*xi)**3 * (self.doubleSpinBox_Ptot.value())**2)
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1
                
                x_NH3 = (2 * rdt * xi_max) / (n_N2_init + n_H2_init - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(i,0)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
            
        #----------------------Variation de la pression---------------------
        if self.radio_Ptot.isChecked() == True :
            n_N2_init = self.doubleSpinBox_n_init.value() / (1 + self.doubleSpinBox_rapportH2N2.value())
            n_H2_init = self.doubleSpinBox_n_init.value() * self.doubleSpinBox_rapportH2N2.value() / (1 + self.doubleSpinBox_rapportH2N2.value())
            xi_max = np.minimum(n_N2_init, n_H2_init/3.0)
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)
            
            self.texte_resultat = "Ptot       xi/xi_max     x(NH3)\n"
            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (n_N2_init + n_H2_init - 2*xi)**2 / ((n_N2_init - xi) * (n_H2_init -3*xi)**3 * (i**2))
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1

                x_NH3 = (2 * rdt * xi_max) / (n_N2_init + n_H2_init - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(i,0)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
                
        #------------------------Variation de ntot-----------------------
        if self.radio_ntot.isChecked() == True :
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)            
            
            self.texte_resultat = "n(N2)i       n(H2)i       xi/xi_max     x(NH3)\n"
            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                n_N2_init = i / (1 + self.doubleSpinBox_rapportH2N2.value())
                n_H2_init = i * self.doubleSpinBox_rapportH2N2.value() / (1 + self.doubleSpinBox_rapportH2N2.value())
                xi_max = np.minimum(n_N2_init, n_H2_init/3.0)
                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (n_N2_init + n_H2_init - 2*xi)**2 / ((n_N2_init - xi) * (n_H2_init -3*xi)**3 * (self.doubleSpinBox_Ptot.value()**2))
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1
                
                x_NH3 = (2 * rdt * xi_max) / (n_N2_init + n_H2_init - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(n_N2_init,3)) + "       " + str(np.round(n_H2_init,3)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
        
        #------------------------Variation de la n(H2)-----------------------
        if self.radio_rapportH2N2.isChecked() == True :
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)

            self.texte_resultat = "n(N2)i       n(H2)i       xi/xi_max     x(NH3)\n"

            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                n_N2_init = self.doubleSpinBox_n_init.value() / (1 + i)
                n_H2_init = self.doubleSpinBox_n_init.value() * i / (1 + i)
                xi_max = np.minimum(n_N2_init, n_H2_init/3.0)

                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (n_N2_init + n_H2_init - 2*xi)**2 / ((n_N2_init - xi) * (n_H2_init -3*xi)**3 * (self.doubleSpinBox_Ptot.value()**2))
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1
                
                x_NH3 = (2 * rdt * xi_max) / (n_N2_init + n_H2_init - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(n_N2_init,3)) + "       " + str(np.round(n_H2_init,3)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()

        #----------------------Mise a jour du QPlainText---------------------
        self.plaintext_resultat.setPlainText(self.texte_resultat)
        
        #----------------------Mise a jour du graphique----------------------
        self.qmc.axes.set_xlim(self.doubleSpinBox_variation_1.value(),self.doubleSpinBox_variation_2.value())   
        self.qmc.l_tableau_rdt.set_data(self.qmc.tableau_parametre, self.qmc.tableau_rdt)
        self.qmc.l_tableau_xNH3.set_data(self.qmc.tableau_parametre, self.qmc.tableau_xNH3)        
        self.qmc.fig.canvas.draw()
        
#-----------------Lancement de l'application---------------------------    
if __name__=="__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    app.exec_()



