"""

Programme permettant de calculer le pourcentage theorique
de plaisir ressnti en buvant une biere
( par rapport a la meilleure biere jamais bue )

Basée sur la formule trouvable sur :
http://eljjdx.canalblog.com/archives/2015/04/24/31833344.html

"""

import argparse
import itertools


def pleasure(T: float, W: int, P: int, M: int,
             V: int, S: int, F: int, verbose: bool=False) -> float:
    """
    @return : Plaisir 3ressenti lors de la dégustation d'une bière
    @param T : Température, en °C
    @param W : Temps avant de retourner travailler, en jours
    @param P : Nombre de personne avec qui l'on partage cette bière
    @param M : Humeur (sur une échelle de 1 à 5, 1 = sale journée)
    @param V : Volume du fond sonore (sur une échelle de 1 à 5, 1 = très fort)
    @param S : Qualité de la nourriture disponibles (sur une échelle de 1 à 5)
    @param F : Qualité des snacks disponibles (sur une échelle de 1 à 5)
    """

    for check in (S, F, M, V):
        if check < 1 or check > 5:
            raise ValueError('Les paramètres M, F, V, S \
            doivent etre des entiers entre 1 et 5')

    score = -((.62 * T ** 2) + (39.2 * W ** 2) + (62.4 * P ** 2)) + \
        ((21.8 * T) + (184.4 * W) + (395.4 * P) +
         (94.5 * M) - (90.25 * V)) + 50 * (S + F + 6.4)
    if verbose:
        print('Score de la bière :', score)
    return score


def best_beer(T, W, verbose=False) -> tuple:
    """
    Calcule la meilleure biere possible en fonction
    des conditions initiales inchangeables
    @return tuple contenant le plaisir maximum
    et les conditions de cette biere
    @param t : Température, en °C
    @param W : Temps avant de retourner travailler, en jours
    """
    max_pleasure = 0
    conditions = None

    for P in range(10):
        for M, V, S, F in itertools.product(range(1, 6), repeat=4):
            tmp = pleasure(T, W, P, M, V, S, F)
            if tmp > max_pleasure:
                max_pleasure = tmp
                conditions = (T, W, P, M, V, S, F)

    if verbose:
        print('La meilleure bière possible fait un score de %d' % max_pleasure)
        print('Obtenue avec les paramètres suivants :', conditions)

    return max_pleasure, conditions


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    HELPS = {
        't': 'Température, en °C',
        'w': 'Temps avant de retourner travailler (en jours)',
        'p': 'Nombre de personne avec qui l\'on partage cette bière',
        'm': 'Humeur (sur une échelle de 1 à 5, 1 = sale journée)',
        'v': 'Volume du fond sonore (sur une échelle de 1 à 5, 1 = très fort)',
        's': 'Qualité de la nourriture disponibles (sur une échelle de 1 à 5)',
        'f': 'Qualité des snacks disponibles (sur une échelle de 1 à 5)',
        }

    PARSER.add_argument('-t', help=HELPS['t'], type=float)
    PARSER.add_argument('-w', help=HELPS['w'], type=int)
    PARSER.add_argument('-p', help=HELPS['p'], type=int)
    PARSER.add_argument('-m', help=HELPS['m'], type=int)
    PARSER.add_argument('-v', help=HELPS['v'], type=int)
    PARSER.add_argument('-s', help=HELPS['s'], type=int)
    PARSER.add_argument('-f', help=HELPS['f'], type=int)
    PARSER.add_argument('--verbose',
                        help='Verbose mode (Display equation scores)',
                        action='store_true')
    ARGS = PARSER.parse_args()

    for argument in HELPS:
        if getattr(ARGS, argument) is None:
            setattr(ARGS, argument, input(HELPS[argument] + '\n'))

    print('Votre biere a un score potentiel de %2f%%' %
          (100 * (pleasure(int(ARGS.t), int(ARGS.w), int(ARGS.p),
                           int(ARGS.m), int(ARGS.v), int(ARGS.s),
                           int(ARGS.f), ARGS.verbose) /
                  best_beer(int(ARGS.t), int(ARGS.w), ARGS.verbose)[0])))
