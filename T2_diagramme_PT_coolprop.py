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



from CoolProp.Plots import PropsPlot

ts_plot = PropsPlot('R290', 'Ts')
ts_plot.show()

from CoolProp.Plots import PropsPlot

ref_fluid = 'n-Pentane'
ts_plot = PropsPlot(ref_fluid, 'Ts')
ts_plot.draw_isolines('Q', [0.3, 0.5, 0.7, 0.8])
ts_plot.draw_isolines('P', [100, 2000], num=5)
ts_plot.draw_isolines('D', [2, 600], num=7)
ts_plot.set_axis_limits([-2, 1.5, 200, 500])
ts_plot.show()


from matplotlib import pyplot
from CoolProp.Plots import PropsPlot

ref_fluid = 'R600a'
fig = pyplot.figure(1, figsize=(10, 10), dpi=100)
for i, gtype in enumerate(['PT', 'PD', 'PS', 'PH', 'TD', 'TS', 'HS']):
    ax = pyplot.subplot(4, 2, i+1)
    if gtype.startswith('P'):
        ax.set_yscale('log')
    props_plot = PropsPlot(ref_fluid, gtype, axis=ax)
    props_plot.title(gtype)
    props_plot._draw_graph()
pyplot.tight_layout()
pyplot.show()



