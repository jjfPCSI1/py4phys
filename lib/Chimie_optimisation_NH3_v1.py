# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



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
        self.axes.set_xlabel("Quantite de matiere de N2 (en mol)")
        
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        


#-----------------Definition de la fenêtre---------------------------
class FenetrePrincipale(QWidget):
    def __init__(self):
        QWidget.__init__(self)
    
        #------------Creation de l'equation-bilan------------
        #--diazote--
        self.label_N2 = QLabel("N<sub>2<\sub>")
        self.doubleSpinBox_N2 = QDoubleSpinBox()
        self.doubleSpinBox_N2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_N2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_N2.setSuffix(" mol")
        self.doubleSpinBox_N2.setDecimals(2)
        self.doubleSpinBox_N2.setRange(0.01,100.0)
        self.doubleSpinBox_N2.setValue(1.0)
        self.doubleSpinBox_N2.setEnabled(False)
    
        #--dihydrogene--
        self.label_H2 = QLabel("3 H<sub>2<\sub>")
        self.doubleSpinBox_H2 = QDoubleSpinBox()
        self.doubleSpinBox_H2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_H2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_H2.setSuffix(" mol")
        self.doubleSpinBox_H2.setDecimals(2)
        self.doubleSpinBox_H2.setRange(0.01,100.0)
        self.doubleSpinBox_H2.setValue(1.0)
    
        self.glayout_bilan = QGridLayout()
        self.glayout_bilan.addWidget(self.label_N2,0,0,QtCore.Qt.AlignHCenter)
        self.glayout_bilan.addWidget(self.doubleSpinBox_N2,1,0,QtCore.Qt.AlignHCenter)
        self.glayout_bilan.addWidget(QLabel("+"),0,1,QtCore.Qt.AlignHCenter)
        self.glayout_bilan.addWidget(self.label_H2,0,2,QtCore.Qt.AlignHCenter)
        self.glayout_bilan.addWidget(self.doubleSpinBox_H2,1,2,QtCore.Qt.AlignHCenter)
        self.glayout_bilan.addWidget(QLabel("   =   2 NH<sub>3<\sub>"),0,3,QtCore.Qt.AlignHCenter)
    
        self.hlayout_bilan = QHBoxLayout()
        self.hlayout_bilan.addLayout(self.glayout_bilan)
        self.hlayout_bilan.addStretch()
    

        #------------Creation des parametres P et T------------
        self.doubleSpinBox_Ptot = QDoubleSpinBox()
        self.doubleSpinBox_Ptot.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_Ptot.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_Ptot.setSuffix(" bar")
        self.doubleSpinBox_Ptot.setDecimals(1)
        self.doubleSpinBox_Ptot.setRange(0.1,200.0)
        self.doubleSpinBox_Ptot.setValue(1.0)
    
        self.doubleSpinBox_T = QDoubleSpinBox()
        self.doubleSpinBox_T.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_T.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_T.setSuffix(" K")
        self.doubleSpinBox_T.setDecimals(0)
        self.doubleSpinBox_T.setRange(1.0,1500.0)
        self.doubleSpinBox_T.setValue(300.0)
    
        self.glayout_P_T = QGridLayout()
        self.glayout_P_T.addWidget(QLabel("Pression totale :"),0,0,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_Ptot,0,1,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("Temperature :"),1,0,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_T,1,1,QtCore.Qt.AlignRight)    
    
        #---------Creation du parametre a faire varier---------
        self.radio_N2 = QRadioButton("n(N2)")
        self.radio_N2.setChecked(True)
        self.radio_H2 = QRadioButton("n(H2)")
        self.radio_Ptot = QRadioButton("Pression")
        self.radio_T = QRadioButton("Temperature")
        self.connect(self.radio_N2, SIGNAL("toggled(bool)"), self.slot_radio_N2)
        self.connect(self.radio_H2, SIGNAL("toggled(bool)"), self.slot_radio_H2)   
        self.connect(self.radio_Ptot, SIGNAL("toggled(bool)"), self.slot_radio_Ptot)
        self.connect(self.radio_T, SIGNAL("toggled(bool)"), self.slot_radio_T)


    
    
        self.hlayout_radio = QHBoxLayout()
        self.hlayout_radio.addWidget(self.radio_N2)
        self.hlayout_radio.addWidget(self.radio_H2)
        self.hlayout_radio.addWidget(self.radio_Ptot)
        self.hlayout_radio.addWidget(self.radio_T)
    
        self.doubleSpinBox_variation_1 = QDoubleSpinBox()
        self.doubleSpinBox_variation_1.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_1.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_N2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_N2.minimum(),self.doubleSpinBox_N2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_N2.minimum())
    
        self.doubleSpinBox_variation_2 = QDoubleSpinBox()
        self.doubleSpinBox_variation_2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_2.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_N2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_N2.minimum(),self.doubleSpinBox_N2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_N2.maximum())
    
        self.hlayout_variation_1 = QHBoxLayout()
        self.hlayout_variation_1.addWidget(QLabel("Faire varier le parametre de "))
        self.hlayout_variation_1.addWidget(self.doubleSpinBox_variation_1)
        self.hlayout_variation_1.addWidget(QLabel(" a "))
        self.hlayout_variation_1.addWidget(self.doubleSpinBox_variation_2)
    
        self.doubleSpinBox_variation_pas = QDoubleSpinBox()
        self.doubleSpinBox_variation_pas.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_pas.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_N2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_N2.minimum(),self.doubleSpinBox_N2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_N2.minimum())
    
        self.hlayout_variation_2 = QHBoxLayout()
        self.hlayout_variation_2.addWidget(QLabel("Par pas de "))
        self.hlayout_variation_2.addWidget(self.doubleSpinBox_variation_pas)
    
        #--------------------Bouton calculer-------------------
        self.bouton_calculer = QPushButton("Calculer")
        self.connect(self.bouton_calculer, SIGNAL("clicked(bool)"), self.slot_calculer)
        
        #----------------------Zone texte---------------------- 
        self.texte_resultat = "n(N2)     xi/xi_max     x(NH3)"
        
        self.plaintext_resultat = QPlainTextEdit()
        self.plaintext_resultat.setReadOnly(True)
        self.plaintext_resultat.setPlainText(self.texte_resultat)
        
        #--------------------Layout gauche---------------------
        self.vlayout_parametres = QVBoxLayout()
        self.vlayout_parametres.addLayout(self.hlayout_bilan)
        self.vlayout_parametres.addLayout(self.glayout_P_T)
        self.vlayout_parametres.addSpacing(20)
        self.vlayout_parametres.addWidget(QLabel("<b>Optimisation des parametres :<\b>"))
        self.vlayout_parametres.addLayout(self.hlayout_radio)
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
    def slot_radio_N2(self):
        self.doubleSpinBox_N2.setEnabled(False)
        self.doubleSpinBox_H2.setEnabled(True)
        self.doubleSpinBox_Ptot.setEnabled(True)    
        self.doubleSpinBox_T.setEnabled(True)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_N2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_N2.minimum(),self.doubleSpinBox_N2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_N2.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_N2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_N2.minimum(),self.doubleSpinBox_N2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_N2.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_N2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_N2.minimum(),self.doubleSpinBox_N2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_N2.minimum())
        self.qmc.axes.set_xlabel("Quantite de matiere de N2 (en mol)")
        
    def slot_radio_H2(self):
        self.doubleSpinBox_N2.setEnabled(True)
        self.doubleSpinBox_H2.setEnabled(False)
        self.doubleSpinBox_Ptot.setEnabled(True)    
        self.doubleSpinBox_T.setEnabled(True)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_H2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_H2.minimum(),self.doubleSpinBox_H2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_H2.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_H2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_H2.minimum(),self.doubleSpinBox_H2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_H2.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_H2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_H2.minimum(),self.doubleSpinBox_H2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_H2.minimum())
        self.qmc.axes.set_xlabel("Quantite de matiere de H2 (en mol)")        
        
    def slot_radio_Ptot(self):
        self.doubleSpinBox_N2.setEnabled(True)
        self.doubleSpinBox_H2.setEnabled(True)
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
        self.doubleSpinBox_N2.setEnabled(True)
        self.doubleSpinBox_H2.setEnabled(True)
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
        self.qmc.tableau_parametre.clear()
        self.qmc.tableau_rdt.clear()
        self.qmc.tableau_xNH3.clear()
        
        #----------------------Variation de la temperature---------------------
        if self.radio_T.isChecked() == True :
            xi_max = np.minimum(self.doubleSpinBox_N2.value(), self.doubleSpinBox_H2.value()/3.0)
            self.texte_resultat = "  T          xi/xi_max     x(NH3)\n"            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value():
                self.qmc.tableau_parametre.append(i)
                #--Calcul de la constante standard d'equilibre--
                k0 = np.exp(delta_r_H0 / i - delta_r_S0)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                #self.texte_resultat += "T = " + str(i) + " | K0 = " + str(np.round(k0,3)) + "\n"                
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (self.doubleSpinBox_N2.value() + self.doubleSpinBox_H2.value() - 2*xi)**2 / ((self.doubleSpinBox_N2.value() - xi) * (self.doubleSpinBox_H2.value() -3*xi)**3 * (self.doubleSpinBox_Ptot.value())**2)
                        #self.texte_resultat += "rdt = " + str(np.round(rdt,3)) + " | Qr = " + str(np.round(qr,3)) + "\n"                        
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1
                
                x_NH3 = (2 * rdt * xi_max) / (self.doubleSpinBox_N2.value() + self.doubleSpinBox_H2.value() - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(i,0)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
            
        #----------------------Variation de la pression---------------------
        if self.radio_Ptot.isChecked() == True :
            xi_max = np.minimum(self.doubleSpinBox_N2.value(), self.doubleSpinBox_H2.value()/3.0)
            self.texte_resultat = "Ptot       xi/xi_max     x(NH3)\n"
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)
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
                        qr = (2*xi)**2 * (self.doubleSpinBox_N2.value() + self.doubleSpinBox_H2.value() - 2*xi)**2 / ((self.doubleSpinBox_N2.value() - xi) * (self.doubleSpinBox_H2.value() -3*xi)**3 * (i**2))
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1

                x_NH3 = (2 * rdt * xi_max) / (self.doubleSpinBox_N2.value() + self.doubleSpinBox_H2.value() - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(i,0)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
                
        #------------------------Variation de la n(N2)-----------------------
        if self.radio_N2.isChecked() == True :
            self.texte_resultat = "n(N2)       xi/xi_max     x(NH3)\n"
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                xi_max = np.minimum(i, self.doubleSpinBox_H2.value()/3.0)
                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (i + self.doubleSpinBox_H2.value() - 2*xi)**2 / ((i - xi) * (self.doubleSpinBox_H2.value() -3*xi)**3 * (self.doubleSpinBox_Ptot.value()**2))
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1
                
                x_NH3 = (2 * rdt * xi_max) / (i + self.doubleSpinBox_H2.value() - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(i,2)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xNH3.append(x_NH3)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
        
        #------------------------Variation de la n(H2)-----------------------
        if self.radio_H2.isChecked() == True :
            self.texte_resultat = "n(H2)       xi/xi_max     x(NH3)\n"
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                xi_max = np.minimum(self.doubleSpinBox_N2.value(), i/3.0)
                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                rdt = 0.0
                pas = 0.1
                j = 0
                while j < precision :                                        
                    rdt += pas
                    if rdt < 0.999999 :
                        xi = rdt * xi_max
                        qr = (2*xi)**2 * (i + self.doubleSpinBox_N2.value() - 2*xi)**2 / ((self.doubleSpinBox_N2.value() - xi) * (i -3*xi)**3 * (self.doubleSpinBox_Ptot.value()**2))
                        if qr > k0 :
                            rdt -= pas
                            pas /= 10
                            j += 1
                    else :
                        rdt -= pas
                        pas /= 10
                        j += 1
                
                x_NH3 = (2 * rdt * xi_max) / (i + self.doubleSpinBox_N2.value() - 2 * rdt * xi_max)
                self.texte_resultat += str(np.round(i,2)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_NH3,4)) + "\n"
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




