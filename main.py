"""
Optimisation de la masse totale et des pertes fer d'un inductance
"""

__author__ = "Augustin GODINOT"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Augustin GODINOT"
__email__ = "augustin.godinot@ens-paris-saclay.fr"
__status__ = "Education"

from inductance import Inductance

import numpy as np
from scipy.optimize import minimize

parametres = {
    "hauteur": 0.1*10, # (en m)
    "largeur": 0.1, # (en m)
    "profondeur": 0.06, # (en m)
    "largeur_dent": 0.026, # (en m)
    "hauteur_entrefer": 0.006 # (en m)
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

def critere(parametres):
    """ Fonction coût considérée pour le problème """

    print(parametres)

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
    A.fermeture_simulation()

    masse =  A.masse_totale
    print(masse)

    return masse


parametres_array = np.array([
    0.1*10,
    0.1,
    0.06,
    0.026,
    0.006
])
limites = [(0.05, None), (0.05, None), (0.01, None), (0.01, None), (0.001, None)]
result = minimize(critere, parametres_array, method='TNC', bounds=limites)
print(result)


# print("L'energie de l'inductance est de {0:.3f} J".format(A.energie_stockee))
# print("Le volume externe de l'inductance est de {0:.6f} m^3".format(A.volume_externe))
# print("Le volume de fer de l'inductance est de {0:.6f} m^3".format(A.volume_fer))
# print("Le volume de cuivre de l'inductance est de {0:.6f} m^3".format(A.volume_cuivre))
# print("La masse de fer de l'inductance est de {0:.3f} kg".format(A.masse_fer))
# print("La masse de cuivre de l'inductance est de {0:.3f} kg".format(A.masse_cuivre))
# print("Les pertes Joule sont de {0:.1f} W".format(A.pertes_joule))
# print("Les pertes fer sont de {0:.1f} W".format(A.pertes_fer))

# # Fermeture de FEMM (à commenter si garder la fenêtre ouverte)
# input()
# A.fermeture_simulation()