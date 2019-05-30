import numpy as np


def cuvette(x, centre=0, tolerance=1):
    """ 
    Fonction avec un mur de potentiel de chaque coté de de l'abscisse centre
    avec une largeur de 2*tolerance
    """

    return max(-1/(x-tolerance-centre), 1/(x+tolerance-centre))

def mur(x, position=0, direction='droite'):
    """
    Fonction avec un mur de potentiel au niveau de l'abscisse position, la
    partie donnée par direction ('droite' ou 'gauche') étant interdite
    """

    if direction == 'droite':
        if x > position: return 0

        return -1/(x - position)
    if direction == 'gauche':
        if x < position: return 0
            
        return 1/(x - position)


if __name__ == "__main__": 
    import matplotlib.pyplot as pl
    CENTRE = 6 
    TOLERANCE = 2

    X = np.linspace(CENTRE - 2*TOLERANCE, CENTRE + 2*TOLERANCE, 1000) 
    Y_1 = [cuvette(x, CENTRE, TOLERANCE) for x in X] 
    Y_2 = [mur(x, 3, 'droite') for x in X]

    pl.plot(X, Y_1) 
    pl.plot(X, Y_2)
    pl.title(f'Fonction "cuvette" centrée en {CENTRE}, de tolérance {TOLERANCE}') 
    pl.xlabel('x')
    pl.ylabel('c(x)')
    pl.show()