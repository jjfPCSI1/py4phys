# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""
Created on Wed Oct 29 16:03:32 2014

@author: Yohan LOQUAIS
Adaptation à Qt5 : Eric Bachard

Travail realise par Yohan Loquais (PC, Lycee Fabert, Metz) permettant de
visualiser les parametres d'optimisation pour la synthese de HI.

Attention, cela demande que les modules Pyside et PyQt4 soient installes sur
la machine pour fonctionner. Ainsi que Python3.
"""

import sys

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#--------------------Definition du graphe---------------------------
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)

        #----Creation des tableaux de donnees-----        
        self.tableau_parametre = []
        self.tableau_rdt = []
        self.tableau_xHI = []
        self.tableau_aI2 = []
        self.tableau_aH2 = []
        
        self.l_tableau_rdt, = self.axes.plot(self.tableau_parametre, self.tableau_rdt, color="0.25", linestyle="-", linewidth="2", label="Rendement")
        self.l_tableau_xHI, = self.axes.plot(self.tableau_parametre, self.tableau_xHI,color="red", linestyle="-", linewidth="2", label="x(HI)")
        self.l_tableau_aI2, = self.axes.plot(self.tableau_parametre, self.tableau_xHI, color="blue", linestyle=":", linewidth="4", label="alpha(I2)")  
        self.l_tableau_aH2, = self.axes.plot(self.tableau_parametre, self.tableau_xHI, color="green", linestyle="--", linewidth="3", label="alpha(H2)")
        self.axes.legend()
        self.axes.set_ylim(0.0, 1.0)
        self.axes.set_xlabel("Rapport initial n(H2)/n(I2)")
        
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        


#-----------------Definition de la fenêtre---------------------------
class FenetrePrincipale(QWidget):
    def __init__(self):
        QWidget.__init__(self)
    
        #------------Creation des spinbox avec les parametres initiaux------------
        #--Nombre de moles initial--
        self.doubleSpinBox_n_init = QDoubleSpinBox()
        self.doubleSpinBox_n_init.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_n_init.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_n_init.setSuffix(" mol")
        self.doubleSpinBox_n_init.setDecimals(1)
        self.doubleSpinBox_n_init.setRange(0.1,1000.0)
        self.doubleSpinBox_n_init.setValue(4.0)
    
        #--Rapport n(H2)/n(N2)--
        self.doubleSpinBox_rapportH2I2 = QDoubleSpinBox()
        self.doubleSpinBox_rapportH2I2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_rapportH2I2.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_rapportH2I2.setDecimals(3)
        self.doubleSpinBox_rapportH2I2.setRange(0.001,1000.0)
        self.doubleSpinBox_rapportH2I2.setValue(1.0)
        self.doubleSpinBox_rapportH2I2.setEnabled(False)
    
        #--Pression totale--
        self.doubleSpinBox_Ptot = QDoubleSpinBox()
        self.doubleSpinBox_Ptot.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_Ptot.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_Ptot.setSuffix(" bar")
        self.doubleSpinBox_Ptot.setDecimals(1)
        self.doubleSpinBox_Ptot.setRange(0.1,500.0)
        self.doubleSpinBox_Ptot.setValue(1.0)
    
        #--Temperature--
        self.doubleSpinBox_T = QDoubleSpinBox()
        self.doubleSpinBox_T.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_T.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_T.setSuffix(" K")
        self.doubleSpinBox_T.setDecimals(0)
        self.doubleSpinBox_T.setRange(1.0,1500.0)
        self.doubleSpinBox_T.setValue(300.0)
    
        #--Layout--
        self.glayout_P_T = QGridLayout()
        self.glayout_P_T.addWidget(QLabel("<b>Parametres initiaux :<>"),0,0,1,-1)
        self.glayout_P_T.addWidget(QLabel("n(I2) + n(H2) :"),1,0,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_n_init,1,1,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("Pression :"),1,3,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_Ptot,1,4,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("n(H2) / n(I2) :"),2,0,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_rapportH2I2,2,1,QtCore.Qt.AlignRight)
        self.glayout_P_T.addWidget(QLabel("Temperature :"),2,3,QtCore.Qt.AlignLeft)
        self.glayout_P_T.addWidget(self.doubleSpinBox_T,2,4,QtCore.Qt.AlignRight)    
    
        #---------Creation du parametre à faire varier---------
        self.radio_ntot = QRadioButton("n(I2) + n(H2)")        
        self.radio_rapportH2I2 = QRadioButton("n(H2)/n(I2)")
        self.radio_rapportH2I2.setChecked(True)        
        self.radio_Ptot = QRadioButton("Pression")
        self.radio_T = QRadioButton("Temperature")
        self.radio_ntot.clicked.connect(self.slot_radio_ntot)
        self.radio_rapportH2I2.clicked.connect(self.slot_radio_rapportH2I2)
        self.radio_Ptot.clicked.connect(self.slot_radio_Ptot)
        self.radio_T.clicked.connect(self.slot_radio_T)

#        self.connect(self.radio_Ptot, SIGNAL("toggled(bool)"), self.slot_radio_Ptot)
#        self.connect(self.radio_T, SIGNAL("toggled(bool)"), self.slot_radio_T)

    
        self.glayout_radio = QGridLayout()
        self.glayout_radio.addWidget(self.radio_ntot,0,0)
        self.glayout_radio.addWidget(self.radio_rapportH2I2,1,0)
        self.glayout_radio.addWidget(self.radio_Ptot,0,1)
        self.glayout_radio.addWidget(self.radio_T,1,1)
    
        self.doubleSpinBox_variation_1 = QDoubleSpinBox()
        self.doubleSpinBox_variation_1.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_1.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_rapportH2I2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_rapportH2I2.minimum(),self.doubleSpinBox_rapportH2I2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_rapportH2I2.minimum())
    
        self.doubleSpinBox_variation_2 = QDoubleSpinBox()
        self.doubleSpinBox_variation_2.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_rapportH2I2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_rapportH2I2.minimum(),self.doubleSpinBox_rapportH2I2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_rapportH2I2.maximum())
    
        self.hlayout_variation_1 = QHBoxLayout()
        self.hlayout_variation_1.addWidget(QLabel("Faire varier le parametre de "))
        self.hlayout_variation_1.addWidget(self.doubleSpinBox_variation_1)
        self.hlayout_variation_1.addWidget(QLabel(" à "))
        self.hlayout_variation_1.addWidget(self.doubleSpinBox_variation_2)
    
        self.doubleSpinBox_variation_pas = QDoubleSpinBox()
        self.doubleSpinBox_variation_pas.setAlignment(QtCore.Qt.AlignRight)
        self.doubleSpinBox_variation_pas.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_rapportH2I2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_rapportH2I2.minimum(),self.doubleSpinBox_rapportH2I2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_rapportH2I2.minimum())
    
        self.hlayout_variation_2 = QHBoxLayout()
        self.hlayout_variation_2.addWidget(QLabel("Par pas de "))
        self.hlayout_variation_2.addWidget(self.doubleSpinBox_variation_pas)
    
        #--------------------Bouton calculer-------------------
        self.bouton_calculer = QPushButton("Calculer")
        self.bouton_calculer.clicked.connect(self.slot_calculer)
        
        #----------------------Zone texte---------------------- 
        self.texte_resultat = "n(I2)i   n(H2)i   rdt   x(HI)   alpha(I2)   alpha(H2)\n"
        
        self.plaintext_resultat = QPlainTextEdit()
        self.plaintext_resultat.setReadOnly(True)
        self.plaintext_resultat.setPlainText(self.texte_resultat)
        
        #--------------------Layout gauche---------------------
        self.vlayout_parametres = QVBoxLayout()
        self.vlayout_parametres.addWidget(QLabel("I2 (g) + H2 (g) = 2 HI (g)"),0,QtCore.Qt.AlignHCenter)
        self.vlayout_parametres.addLayout(self.glayout_P_T)
        self.vlayout_parametres.addSpacing(20)
        self.vlayout_parametres.addWidget(QLabel("<b>Variation d'un des parametres initiaux :<>"))
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
        self.doubleSpinBox_rapportH2I2.setEnabled(True)
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
        self.qmc.axes.set_xlabel("Quantite de matiere totale initiale n(I2) + n(H2) (en mol)")
        
    def slot_radio_rapportH2I2(self):
        self.doubleSpinBox_n_init.setEnabled(True)
        self.doubleSpinBox_rapportH2I2.setEnabled(False)
        self.doubleSpinBox_Ptot.setEnabled(True)    
        self.doubleSpinBox_T.setEnabled(True)
        self.doubleSpinBox_variation_1.setDecimals(self.doubleSpinBox_rapportH2I2.decimals())
        self.doubleSpinBox_variation_1.setRange(self.doubleSpinBox_rapportH2I2.minimum(),self.doubleSpinBox_rapportH2I2.maximum())
        self.doubleSpinBox_variation_1.setValue(self.doubleSpinBox_rapportH2I2.minimum())
        self.doubleSpinBox_variation_2.setDecimals(self.doubleSpinBox_rapportH2I2.decimals())
        self.doubleSpinBox_variation_2.setRange(self.doubleSpinBox_rapportH2I2.minimum(),self.doubleSpinBox_rapportH2I2.maximum())
        self.doubleSpinBox_variation_2.setValue(self.doubleSpinBox_rapportH2I2.maximum())
        self.doubleSpinBox_variation_pas.setDecimals(self.doubleSpinBox_rapportH2I2.decimals())
        self.doubleSpinBox_variation_pas.setRange(self.doubleSpinBox_rapportH2I2.minimum(),self.doubleSpinBox_rapportH2I2.maximum()/2)
        self.doubleSpinBox_variation_pas.setValue(self.doubleSpinBox_rapportH2I2.minimum())
        self.qmc.axes.set_xlabel("Rapport initial n(H2)/n(I2)")        
        
    def slot_radio_Ptot(self):
        self.doubleSpinBox_n_init.setEnabled(True)
        self.doubleSpinBox_rapportH2I2.setEnabled(True)
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
        self.doubleSpinBox_rapportH2I2.setEnabled(True)
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
        delta_r_H0 = 9480.0 / 8.314 # - delta_r_H0 / R (en J/mol)
        delta_r_S0 = - 21.806 / 8.314 # - delta_r_S0 / R (en J/mol)
        k0 = 0.0
        i = self.doubleSpinBox_variation_1.value()
        x_HI = 0.0
        precision = 0.00001
        n_I2_init = 0.0
        n_H2_init = 0.0
        del self.qmc.tableau_parametre[:]
        self.qmc.tableau_rdt.clear()
        self.qmc.tableau_xHI.clear()
        self.qmc.tableau_aI2.clear()
        self.qmc.tableau_aH2.clear()
        
        #----------------------Variation de la temperature---------------------
        if self.radio_T.isChecked() == True :
            n_I2_init = self.doubleSpinBox_n_init.value() / (1 + self.doubleSpinBox_rapportH2I2.value())
            n_H2_init = self.doubleSpinBox_n_init.value() * self.doubleSpinBox_rapportH2I2.value() / (1 + self.doubleSpinBox_rapportH2I2.value())
            xi_max = np.minimum(n_I2_init, n_H2_init)

            self.texte_resultat = "   T        rdt      x(HI)    alpha(I2)  alpha(H2)\n"
            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value():
                self.qmc.tableau_parametre.append(i)
                #--Calcul de la constante standard d'equilibre--
                k0 = np.exp(delta_r_H0 / i - delta_r_S0)
                #--Recherche de la valeur de xi telle que qr = k0--
                a = 0.0
                b = 1.0

                while (b - a) > precision :
                    rdt = (a + b) / 2.0
                    xi = rdt * xi_max
                    qr = (2*xi)**2 / ((n_I2_init - xi) * (n_H2_init - xi))
                    
                    if (qr - k0) > 0 :
                        b = rdt
                    if (qr - k0) < 0 :
                        a = rdt
                
                x_HI = (2 * xi) / (n_I2_init + n_H2_init)
                a_I2 = 1.0 - (n_I2_init - xi)/(n_I2_init)
                a_H2 = 1.0 - (n_H2_init - xi)/(n_H2_init)
                #self.texte_resultat += str(np.round(i,0)) + "       " + str(np.round(rdt,4)) + "       " + str(np.round(x_HI,4)) + "\n"
                self.texte_resultat += "%(param)4d     %(rdt).4f     %(xHI).4f     %(aI2).4f     %(aH2).4f\n" %{"param": i,"rdt": rdt, "xHI": x_HI, "aI2": a_I2, "aH2": a_H2}
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xHI.append(x_HI)  
                self.qmc.tableau_aI2.append(a_I2)
                self.qmc.tableau_aH2.append(a_H2)
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
            
        #----------------------Variation de la pression---------------------
        if self.radio_Ptot.isChecked() == True :
            n_I2_init = self.doubleSpinBox_n_init.value() / (1 + self.doubleSpinBox_rapportH2I2.value())
            n_H2_init = self.doubleSpinBox_n_init.value() * self.doubleSpinBox_rapportH2I2.value() / (1 + self.doubleSpinBox_rapportH2I2.value())
            xi_max = np.minimum(n_I2_init, n_H2_init)
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)
            
            self.texte_resultat = "Ptot        rdt      x(HI)    alpha(I2)  alpha(H2)\n"
            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                a = 0.0
                b = 1.0

                while (b - a) > precision :                                        
                    rdt = (a + b) / 2.0
                    xi = rdt * xi_max
                    qr = (2*xi)**2 / ((n_I2_init - xi) * (n_H2_init - xi))
                    
                    if (qr - k0) > 0 :
                        b = rdt
                    if (qr - k0) < 0 :
                        a = rdt

                x_HI = (2 * xi) / (n_I2_init + n_H2_init)
                a_I2 = 1.0 - (n_I2_init - xi)/(n_I2_init)
                a_H2 = 1.0 - (n_H2_init - xi)/(n_H2_init)
                self.texte_resultat += "%(param).1f     %(rdt).4f     %(xHI).4f     %(aI2).4f     %(aH2).4f\n" %{"param": i,"rdt": rdt, "xHI": x_HI, "aI2": a_I2, "aH2": a_H2}
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xHI.append(x_HI)
                self.qmc.tableau_aI2.append(a_I2)
                self.qmc.tableau_aH2.append(a_H2)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
                
        #------------------------Variation de ntot-----------------------
        if self.radio_ntot.isChecked() == True :
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)            
            
            self.texte_resultat = "n(I2)i   n(H2)i   rdt   x(HI)   alpha(I2)   alpha(H2)\n"
            
            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                n_I2_init = i / (1 + self.doubleSpinBox_rapportH2I2.value())
                n_H2_init = i * self.doubleSpinBox_rapportH2I2.value() / (1 + self.doubleSpinBox_rapportH2I2.value())
                xi_max = np.minimum(n_I2_init, n_H2_init)
                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                a = 0.0
                b = 1.0
                
                while (b - a) > precision :                                        
                    rdt = (a + b) / 2.0
                    xi = rdt * xi_max
                    qr = (2*xi)**2 / ((n_I2_init - xi) * (n_H2_init -xi))
                    
                    if (qr - k0) > 0 :
                        b = rdt
                    if (qr - k0) < 0 :
                        a = rdt
                
                x_HI = (2 * xi) / (n_I2_init + n_H2_init)
                a_I2 = 1.0 - (n_I2_init - xi)/(n_I2_init)
                a_H2 = 1.0 - (n_H2_init - xi)/(n_H2_init)
                self.texte_resultat += "%(n_I2_init).3f   %(n_H2_init).3f   %(rdt).3f   %(xHI).3f   %(aI2).3f   %(aH2).3f\n" %{"n_I2_init": n_I2_init,"n_H2_init": n_H2_init,"rdt": rdt, "xHI": x_HI, "aI2": a_I2, "aH2": a_H2}
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xHI.append(x_HI) 
                self.qmc.tableau_aI2.append(a_I2)
                self.qmc.tableau_aH2.append(a_H2)
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()
        
        #------------------------Variation de la n(H2)-----------------------
        if self.radio_rapportH2I2.isChecked() == True :
            k0 = np.exp(delta_r_H0 / self.doubleSpinBox_T.value() - delta_r_S0)

            self.texte_resultat = "n(I2)i   n(H2)i   rdt   x(HI)   alpha(I2)   alpha(H2)\n"

            while i - self.doubleSpinBox_variation_pas.value() < self.doubleSpinBox_variation_2.value() :
                n_I2_init = self.doubleSpinBox_n_init.value() / (1 + i)
                n_H2_init = self.doubleSpinBox_n_init.value() * i / (1 + i)
                xi_max = np.minimum(n_I2_init, n_H2_init)

                self.qmc.tableau_parametre.append(i)
                #--Recherche de la valeur de xi telle que qr = k0--
                a = 0.0
                b = 1.0
                
                while (b - a) > precision :                                        
                    rdt = (a + b) / 2.0
                    xi = rdt * xi_max
                    qr = (2*xi)**2 / ((n_I2_init - xi) * (n_H2_init - xi))
                    
                    if (qr - k0) > 0 :
                        b = rdt
                    if (qr - k0) < 0 :
                        a = rdt
                
                x_HI = (2 * xi) / (n_I2_init + n_H2_init)
                a_I2 = 1.0 - (n_I2_init - xi)/(n_I2_init)
                a_H2 = 1.0 - (n_H2_init - xi)/(n_H2_init)
                self.texte_resultat += "%(n_I2_init).3f   %(n_H2_init).3f   %(rdt).3f   %(xHI).3f   %(aI2).3f   %(aH2).3f\n" %{"n_I2_init": n_I2_init,"n_H2_init": n_H2_init,"rdt": rdt, "xHI": x_HI, "aI2": a_I2, "aH2": a_H2}
                self.qmc.tableau_rdt.append(rdt)
                self.qmc.tableau_xHI.append(x_HI)
                self.qmc.tableau_aI2.append(a_I2)
                self.qmc.tableau_aH2.append(a_H2)                
                #--incrementation de i--
                i += self.doubleSpinBox_variation_pas.value()

        #----------------------Mise à jour du QPlainText---------------------
        self.plaintext_resultat.setPlainText(self.texte_resultat)
        
        #----------------------Mise à jour du graphique----------------------
        self.qmc.axes.set_xlim(self.doubleSpinBox_variation_1.value(),self.doubleSpinBox_variation_2.value())   
        self.qmc.l_tableau_rdt.set_data(self.qmc.tableau_parametre, self.qmc.tableau_rdt)
        self.qmc.l_tableau_xHI.set_data(self.qmc.tableau_parametre, self.qmc.tableau_xHI)    
        self.qmc.l_tableau_aI2.set_data(self.qmc.tableau_parametre, self.qmc.tableau_aI2)
        self.qmc.l_tableau_aH2.set_data(self.qmc.tableau_parametre, self.qmc.tableau_aH2)   
        self.qmc.fig.canvas.draw()
        
#-----------------Lancement de l'application---------------------------    
if __name__=="__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    app.exec_()



