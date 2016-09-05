# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""
Programme proposé par Sylvain Condamin (MP*, Lycée Albert Schweitzer, Le Raincy).
Permet la création de cartes de champ électrique, avec possibilité d'inclure 
des dipôles. Il pourrait sans doute être mieux optimisé mais il fonctionne 
tant qu'on ne lui en demande pas trop.
"""

import numpy as np
import scipy.special as sp
import matplotlib.pyplot as pl
from scipy.integrate import odeint

# On prend 1/(4*Pi*Epsilon0) =1 

# Ce programme permet de tracer les lignes de champ magnétique d'un ensemble de
# lignes orthogonales au plan, de spires dont l'axe est dans le plan, et de
# moments magnétiques dans le plan. Il faut commencer par créer un objet
# Diagramme, puis ajouter les différents objets électriques à l'aide des
# méthodes dédiées, puis utiliser la méthode draw pour tracer le diagramme.
# Cf. description des méthodes, et exemples finaux pour plus d'information. 


class Diagramme(object):
    def __init__(self,size=1,title="",numpoints=1000,numV=10,startcircle=1./20.):
        """
        size est la taille de la fenêtre utilisée. (x et y varient de
        -size à + size). numpoints est le nombre de points utilisés
        pour le tracé. numV est le nombre de lignes de niveau de chaque signe. startcircle est
        la taille relative du cercle portant les points de départ autour de chaque
        objet. Ce paramètre contrôle également la plus haute ligne de niveau. 
        """
        self.size = float(size)
        self.title=title
        self.numpoints=numpoints
        self.objects=[]
        self.startpoints=[]
        self.numV=numV
        self.circle = startcircle
        self.maxV=0 #Ligne de potentiel la plus élevée

    def addCharge(self,x,y,q=1,points=20):
        """
        Permet d'ajouter une charge q. Par défaut cela ajoute des points de 
        départ de lignes de champ. 
        """
        self.objects.append(Charge(x,y,q))
        r = self.size*self.circle
        for i in range(points):
            phi = 2*np.pi*(i+0.5)/points
            self.startpoints.append([x+r*np.cos(phi),y+r*np.sin(phi)])
        self.maxV = max(self.maxV,abs(q)/(self.size*self.circle))

    def addDipole(self,x,y,p,theta=0,points=40):
        """
        Permet d'ajouter un dipôle electrique p, à la position x et
        y. theta désigne l'ange que fait la spire par rapport à la
        verticale. Par défaut cela ajoute des points de départ de
        lignes de champ. 
        """
        self.objects.append(Dipole(x,y,p,theta))
        r = self.size*self.circle
        for i in range(points):
            phi = 2*np.pi*(i+0.5)/points
            self.startpoints.append([x+r*np.cos(phi),y+r*np.sin(phi)])
        self.maxV = max(self.maxV, abs(p)/(self.size*self.size*self.circle*self.circle))  
        
    def addStartPoints(self,x,y):
        """
        Permet d'ajouter des points de départ de lignes de champ.
        """
        self.startpoints.append([x,y])

    def E(self,P):
        """
        Permet d'obtenir le champ électrique au point P
        """
        Ex = 0
        Ey = 0
        for obj in self.objects: 
            Ex += obj.E(P)[0]
            Ey += obj.E(P)[1]
        return [Ex,Ey]

    def V(self,P):
        """
        Permet d'obtenir le potentiel électrique au point P
        """
        V = 0
        for obj in self.objects:
            V += obj.V(P)
        return(V)
    
    def draw(self):
        """
        Trace l'ensemble des lignes de champ passant par les points de
        départ stockés dans Startpoints
        """
        def fun(P,V):
            E = self.E(P)
            Ex = E[0]
            Ey = E[1]
            E2 = Ex*Ex+Ey*Ey
            return [Ex/E2,Ey/E2]
        baseV = np.exp(np.linspace(0,3*np.log(self.circle),self.numpoints))
        for P0 in self.startpoints:
            V0 = self.V(P0)
            if(V0 == 0):
                continue
            V = - V0 * baseV
            sol = odeint(fun,P0,V)
            x = sol[:,0]
            y = sol[:,1]
            pl.plot(x,y,'-',color='k')
            k = int(self.numpoints/4)
            if(V0 > 0):
                pl.arrow(x[k],y[k],x[k+1]-x[k],y[k+1]-y[k],color='k')
            else:
                pl.arrow(x[k],y[k],x[k-1]-x[k],y[k-1]-y[k],color='k')
        S = np.linspace(-self.size,self.size,self.numpoints/10)
        Vs = self.maxV*np.exp(np.linspace(0,2*np.log(self.circle),self.numV))
        Vs = np.append(Vs,-Vs)
        Vs = np.append(Vs,0)
        Vs = np.sort(Vs)
        P = [[self.V([X,Y]) for X in S]for Y in S]
        pl.contour(S,S,P,Vs,colors='b')
        pl.title(self.title)
        pl.xlim([-self.size,self.size])
        pl.ylim([-self.size,self.size])
        #pl.savefig("dipole.eps") #Cette ligne permet de sauvegarder la figure, je la laisse commentée.
        pl.show()

class ElectricObjects(object):
    def __init__(self):
        pass
    
    def E(self,P):
        raise NotImplementedError()
    def V(self,P):
        raise NotImplementedError()

class Charge(ElectricObjects):
    def __init__(self,x,y,q):
        self.x0 = x
        self.y0 = y
        self.q = q

    def E(self,P):
        x = P[0]- self.x0
        y = P[1]- self.y0
        return([self.q*x/pow(x*x+y*y,1.5),self.q*y/pow(x*x+y*y,1.5)])

    def V(self,P):
        x = P[0]- self.x0
        y = P[1]- self.y0
        return(self.q/np.sqrt(x*x+y*y))       

class Dipole(ElectricObjects):
    def __init__(self,x,y,p,theta):
        self.x0 = x
        self.y0 = y
        self.p = p
        self.theta = theta

    def E(self,P):
        p = self.p
        theta = self.theta
        x = P[0] - self.x0
        y = P[1] - self.y0
        r = np.sqrt(x*x+y*y)
        Ex = (p/(r**3))*((-x*np.sin(theta)+y*np.cos(theta))*3*(x/r**2)+np.sin(theta))
        Ey = (p/(r**3))*((-x*np.sin(theta)+y*np.cos(theta))*3*(y/r**2)-np.cos(theta))
        return([Ex,Ey])

    def V(self,P):
        p = self.p
        theta = self.theta
        x = P[0] - self.x0
        y = P[1] - self.y0
        r = np.sqrt(x*x+y*y)
        return((p/r**3)*(-x*np.sin(theta)+y*np.cos(theta)))

#Tracé pour une charge 
#diag = Diagramme(numV = 20) #Crée le diagramme. L'option permet d'avoir plus d'équipotentielles
#diag.addCharge(0,0,q=1) #Ajoute une charge q=1 à la position désirée
#diag.draw() #Réalise le tracé
    
#Tracé pour deux charges identiques    
##diag = Diagramme(numV = 20)
##diag.addCharge(0,0.2,q=1) 
##diag.addCharge(0,-0.2,q=1) #Ajoute une deuxième charge à une position différente
##diag.draw()

#Tracé pour deux charges opposées  
##diag = Diagramme()
##diag.addCharge(0,0.2,q=1) 
##diag.addCharge(0,-0.2,q=-1) #La charge est négative cette fois.
##diag.draw()

#Tracé pour un dipôle 
diag = Diagramme(startcircle = 0.03) #Diminue la taille du cercle autour du dipôle
diag.addDipole(0,0,p=1,points=50) #Ajoute un dipôle
diag.draw()



