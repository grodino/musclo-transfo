"""
Optimisation de la masse totale et des pertes fer d'un inductance
"""

__author__ = "Augustin GODINOT"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Augustin GODINOT"
__email__ = "augustin.godinot@ens-paris-saclay.fr"
__status__ = "Education"

from pprint import pprint

import numpy as np
from scipy.optimize import minimize

from inductance import Inductance
from optimisation import cuvette, mur


parametres = {
    "hauteur": 0.1, # (en m)
    "largeur": 0.1, # (en m)
    "profondeur": 0.06, # (en m)
    "largeur_dent": 0.0026, # (en m)
    "hauteur_entrefer": 0.0006 # (en m)
}
contraintes = {
    "energie_stockee": 4, # (en J)
    "courant_max": 20, # (en A)
    "j_max": 5e6, # (en A/m²)
    "volume_max": 1.31e-3, # (en m^3)
}
variables = {
    "masse_totale": 0, # (en kg)
    "pertes_fer": 0 # (en J)
}


valeurs_params = []
valeurs_critere = []


def critere(parametres):
    """ Fonction coût considérée pour le problème """

    # Si la largeur totale de fer est supérieure à la largeur du transfo
    if 2*parametres[4] >= parametres[1]:
        return np.inf

    A=Inductance({
        "hauteur": parametres[0], 
        "largeur": parametres[1],
        "l_active": parametres[2], 
        "entrefer": parametres[3], 
        "l_dent":parametres[4],
        "k_b":0.4, 
        "j_max": contraintes['j_max'], 
        "i_max": contraintes['courant_max']
    })
    A.creation_FEMM()
    A.creation_geometrie()
    A.fit_zoom()
    A.affectation_materiaux()
    A.conditions_limites()
    A.sauvegarde_simulation()
    A.maillage()
    A.simulation()

    masse =  A.masse_totale
    energie = A.energie_stockee

    TOL_NRJ = contraintes['energie_stockee']/4

    crit = masse**2 + A.pertes_fer**2 \
            + cuvette(energie, contraintes['energie_stockee'], TOL_NRJ) \
            + mur(A.volume_externe, contraintes['volume_max'], 'droite') \
            + mur(A.l_dent, A.largeur/2, 'droite')

    valeurs_critere.append(crit)
    valeurs_params.append(parametres)
    print(f'CRITERE {crit:6.3f} || ENERGIE {A.energie_stockee:.3f} || PARAMETRES {parametres}')

    A.fermeture_simulation()

    return crit


parametres_array = np.array([
    parametres['hauteur'],
    parametres['largeur'],
    parametres['profondeur'],
    parametres['largeur_dent'],
    parametres['hauteur_entrefer']
])

A = Inductance({
    "hauteur": parametres_array[0], 
    "largeur": parametres_array[1],
    "l_active": parametres_array[2], 
    "entrefer": parametres_array[3], 
    "l_dent":parametres_array[4],
    "k_b":0.4, 
    "j_max": contraintes['j_max'], 
    "i_max": contraintes['courant_max']
})
A.creation_FEMM()
A.creation_geometrie()
A.fit_zoom()
A.affectation_materiaux()
A.conditions_limites()
A.sauvegarde_simulation()
A.maillage()
A.simulation()

print(f'ENERGIE INITIALE : {A.energie_stockee}')
A.fermeture_simulation()

limites = [(0.001, None), (0.001, None), (0.001, None), (0.0001, None), (0.0001, None)]
result = minimize(
    critere, 
    parametres_array, 
    method='L-BFGS-B', 
    bounds=limites,
    options={
        'ftol': 0.0001,
        'disp': True,
        'maxls': 20,
        'eps': 0.0001,
        #'stepmx': 1000
    })
pprint(result)
pprint(valeurs_critere)
pprint(valeurs_params)

A=Inductance({
    "hauteur": result.x[0], 
    "largeur": result.x[1],
    "l_active": result.x[2], 
    "entrefer": result.x[3], 
    "l_dent":result.x[4],
    "k_b":0.4, 
    "j_max": contraintes['j_max'], 
    "i_max": contraintes['courant_max']
})
A.creation_FEMM(display=True)
A.creation_geometrie()
A.fit_zoom()
A.affectation_materiaux()
A.conditions_limites()
A.sauvegarde_simulation()
A.maillage()
A.simulation()


print("L'energie de l'inductance est de {0:.3f} J".format(A.energie_stockee))
print("Le volume externe de l'inductance est de {0:.6f} m^3".format(A.volume_externe))
print("Le volume de fer de l'inductance est de {0:.6f} m^3".format(A.volume_fer))
print("Le volume de cuivre de l'inductance est de {0:.6f} m^3".format(A.volume_cuivre))
print("La masse de fer de l'inductance est de {0:.3f} kg".format(A.masse_fer))
print("La masse de cuivre de l'inductance est de {0:.3f} kg".format(A.masse_cuivre))
print("Les pertes Joule sont de {0:.1f} W".format(A.pertes_joule))
print("Les pertes fer sont de {0:.1f} W".format(A.pertes_fer))

# Fermeture de FEMM (à commenter si garder la fenêtre ouverte)
input()
A.fermeture_simulation()