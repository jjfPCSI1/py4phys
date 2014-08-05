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
Created on Fri May 31 10:33:06 2014

@author: Sylvain Condamin, adapté d'un code de Thierry Pré. 

On prend mu0/(2*Pi) =1 
Ce programme permet de tracer les lignes de champ magnétique d'un ensemble de
lignes orthogonales au plan, de spires dont l'axe est dans le plan, et de
moments magnétiques dans le plan. Il faut commencer par créer un objet
Diagramme, puis ajouter les différents objets magnétiques à l'aide des
méthodes dédiées, puis utiliser la méthode draw pour tracer le diagramme.
Cf. description des méthodes, et exemple final pour plus d'information. 
"""

import numpy as np
import scipy.special as sp
import matplotlib.pyplot as pl
from scipy.integrate import odeint



class Diagramme(object):
    """ La classe Diagramme s'occupe de tout ce qui concerne les tracés."""
    def __init__(self,size=1,title="",numpoints=1000,k=1):
        """
        Routine d'initialisation d'un diagramme de lignes de champ:
        * size est la taille de la fenêtre utilisée. (x et y varient de -size à +size) 
        * numpoints est le nombre de points utilisé pour le tracé. 
        * Le coefficient k permet de régler la longueur des lignes
        tracées. Le défaut k=1 assure normalement que les lignes bouclent
        correctement, mais il est possible de le réduire pour améliorer le temps
        de calcul. 
        """
        self.size = float(size)
        self.title=title
        self.numpoints=numpoints
        self.objects=[]
        self.startpoints=[]
        self.maxint=0 # Ceci correspond au temps d'intégration à utiliser pour
                      # le tracé des courbes.
        self.k=k

    def addLine(self,x,y,I=1,points=20):
        """
        Permet d'ajouter une ligne de courant infinie, orthogonale au
        plan du tracé. Par défaut cela ajoute des points de départ de
        lignes de champ. 
        """
        self.objects.append(Line(x,y,I))
        for i in range(points):
            self.startpoints.append([x+2*(i+1)*self.size/points,y])
        self.maxint = pow(pow(2*np.pi,3)*abs(I)*self.size**2+self.maxint**3,1/3)

    def addSpire(self,x,y,a,I=1,theta=0,points=20):
        """
        Permet de définir une spire: x et y désignent le centre, a le
        rayon, I l'intensité, et theta l'angle que fait l'axe
        de la spire par rapport à la verticale. Par défaut cela ajoute
        des points de départ de lignes de champ. 
        """
        self.objects.append(Spire(x,y,a,I,theta))
        for i in range(points):
            l = -a+2*a*float(1+i)/(1+points)
            self.startpoints.append([x+l*np.cos(theta),y+l*np.sin(theta)])
        self.maxint += pow(100*abs(I)*np.pi*a*a+self.maxint**3,1/3)
        
    def addDipole(self,x,y,m,theta=0,points=20):
        """
        Permet d'ajouter un dipôle magnétique m, à la position x et
        y. theta désigne l'ange que fait la spire par rapport à la
        verticale. Par défaut cela ajoute des points de départ de
        lignes de champ. 
        """
        self.objects.append(Dipole(x,y,m,theta))
        s = self.size/5
        x0 = x-s*np.sin(theta)
        y0 = y + s*np.cos(theta)
        for i in range(points):
            phi = theta+2*(i+1)*np.pi/(1+points)
            self.startpoints.append([x0+s*np.sin(phi),y0-s*np.cos(phi)])
        self.maxint += pow(1000*abs(m)+self.maxint**3,1./3.)    
        
    def addStartPoints(self,x,y):
        """
        Permet d'ajouter des points de départ de lignes de champ.
        """
        self.startpoints.append([x,y])

    def B(self,P):
        Bx = 0
        By = 0
        for magnet in self.objects: 
            Bx += magnet.B(P)[0]
            By += magnet.B(P)[1]
        return [Bx,By]

    def draw(self,file=None):
        """
        Trace l'ensemble des lignes de champ passant par les points de départ 
        stockés dans Startpoints. Si un nom de fichier est donné, enregistre 
        la figure dans le fichier mais n'affiche rien à l'écran
        """

        def fun(P,t):
            B = self.B(P)
            Bx = B[0]
            By = B[1]
            B = np.sqrt(Bx*Bx+By*By)
            return [Bx/pow(B,4./3.),By/pow(B,4./3.)]

        t = np.linspace(0,self.k*self.maxint,self.numpoints/2)
        t2 = - t
        for P0 in self.startpoints:
            sol = odeint(fun,P0,t)
            x = sol[:,0]
            y = sol[:,1]
            pl.plot(x,y,'-',color='k')
            sol = odeint(fun,P0,t2)
            x = sol[1:,0]
            y = sol[1:,1]
            pl.plot(x,y,'-',color='k')
            pl.arrow(x[1],y[1],x[0]-x[1],y[0]-y[1],color='k')
        pl.title(self.title)
        pl.xlim([-self.size,self.size])
        pl.ylim([-self.size,self.size])
        if file:
            pl.savefig(file)
            pl.close()
        else:
            pl.show()

class MagneticObjects(object):
    def __init__(self):
        pass
    
    def B(self,P):
        raise NotImplementedError()

class Line(MagneticObjects):
    def __init__(self,x,y,I):
        self.x0 = x
        self.y0 = y
        self.I = I

    def B(self,P):
        x = P[0]- self.x0
        y = P[1]- self.y0
        return([-self.I*y/(x*x+y*y),self.I*x/(x*x+y*y)])

class Spire(MagneticObjects):
    def __init__(self,x,y,a,I,theta):
        self.x0 = x
        self.y0 = y
        self.a = a
        self.I = I
        self.theta = theta

    def B(self,P):
        a = self.a
        theta = self.theta
        x = P[0] - self.x0
        y = P[1] - self.y0
        r = x*np.cos(theta)+y*np.sin(theta)
        z = -x*np.sin(theta)+y*np.cos(theta) # On se ramène à des
        # coordonnées cylindriques par rapport à la spire. Pour la
        # suite des calculs, voir l'aticle de T.Pré
        # http://www.udppc.asso.fr/bupdoc/textes/fichierjoint/918/0918D119.zip 
        k= 4.*abs(r)*a/((a+abs(r))**2+z**2)
        Kk=sp.ellipk(k)
        Ek=sp.ellipe(k)
        Br=self.I*(z/r)/np.sqrt((a+abs(r))**2+z**2)*(-Kk+(a**2+r**2+z**2)/((a-abs(r))**2+z**2)*Ek)
        Bz=(self.I/np.sqrt((a+abs(r))**2+z**2))*(Kk+((a**2-r**2-z**2)/((a-abs(r))**2+z**2))*Ek)        
        return([Br*np.cos(theta)-Bz*np.sin(theta),Br*np.sin(theta)+Bz*np.cos(theta)])

class Dipole(MagneticObjects):
    def __init__(self,x,y,m,theta):
        self.x0 = x
        self.y0 = y
        self.m = m
        self.theta = theta

    def B(self,P):
        m = self.m
        theta = self.theta
        x = P[0] - self.x0
        y = P[1] - self.y0
        r = np.sqrt(x*x+y*y)
        Bx = (m/(2*r**3))*((-x*np.sin(theta)+y*np.cos(theta))*3*(x/r**2)+np.sin(theta))
        By = (m/(2*r**3))*((-x*np.sin(theta)+y*np.cos(theta))*3*(y/r**2)-np.cos(theta))
        return([Bx,By])

# Premier exemple: deux spires en configuration de Helmholtz    
diag = Diagramme()
diag.addSpire(0,0.25,a=0.5,I=1)
diag.addSpire(0,-0.25,a=0.5,I=1)
diag.draw('PNG/I1_lignes_champ_magnetique_helmholtz.png')

# Deuxième exemple: un dipôle avec un fil perpendiculaire au plan de la figure.
diag = Diagramme()
diag.addLine(0.5,0.5,I=1)
diag.addDipole(0,0,m=1,points=10)
diag.draw('PNG/I1_lignes_champ_magnetique_fil_et_dipole.png')




