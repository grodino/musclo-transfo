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
from scipy.optimize import differential_evolution

parametres = {
    "hauteur": 0.1, # (en m)
    "largeur": 0.1, # (en m)
    "profondeur": 0.06, # (en m)
    "largeur_fer": 0.026, # (en m)
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

# TODO : dans inducance.py continuer le calcul des pertes fer (Total Core Loss)
# pour prendre en compte les courbes constructeur

A=Inductance({
    "hauteur": parametres['hauteur'], 
    "largeur": parametres['largeur'],
    "l_active": parametres['profondeur'], 
    "entrefer": parametres['hauteur_entrefer'], 
    "l_dent":parametres['largeur_fer'],
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

print("L'energie de l'inductance est de {0:.3f} J".format(A.calcul_energie()))
print("Le volume externe de l'inductance est de {0:.6f} m^3".format(A.calcul_volume_externe()))
print("Le volume de fer de l'inductance est de {0:.6f} m^3".format(A.calcul_volume_fer()))
print("Le volume de cuivre de l'inductance est de {0:.6f} m^3".format(A.calcul_volume_cuivre()))
print("La masse de fer de l'inductance est de {0:.3f} kg".format(A.calcul_masse_fer()))
print("La masse de cuivre de l'inductance est de {0:.3f} kg".format(A.calcul_masse_cuivre()))
print("Les pertes Joule sont de {0:.1f} W".format(A.calcul_pertes_joule()))
#("Les pertes fer sont de {0:.1f} W".format(A.calcul_pertes_fer()))

# Fermeture de FEMM (à commenter si garder la fenêtre ouverte)
input()
A.fermeture_simulation()