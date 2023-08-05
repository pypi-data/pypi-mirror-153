# ranking_to_linear

import numpy as np

def print_ranking(ranking, alternatives = None):
    """Print a graphical representation of the ranking

    :param ranking: Ranking to print. Each element of the array contains the 
                    position of the i-th element of the ranking
    :type ranking: np.array

    :param alternatives: Names of the alternatives. If none is given alternatives
                    are named as a0, a1, a2...
    :type alternatives: np.array, optional

    :return: A string representing the ranking
    :rtype: np.array
    """

    if alternatives is None:
        alternatives = np.array(["{}{}".format('a',i) for i in list(np.arange(ranking.size)+1)])
    out=''
    # for n alternatives, x is a numpy array of length n with numbers in [0,n-1]
    for i in range(alternatives.size):
        itemindex, = np.where(ranking == i)
        out+=alternatives[itemindex][0]
        if i < alternatives.size-1:
            out+='>'
    return out

def ranking_to_lineal(r):
    for i in range(max(r)+1):
        # print(i)
        indexes = np.where(r == i)[0]
        # print(indexes)
        if indexes.size > 1: # there are tied candidates
            # Increment all the candidates that are later on the ranking
            # r[r > i] = r[r > i] + indexes.size-1
            # Untie
            values = i - np.arange(indexes.size) 
            values = values[::-1]
            # print("New values {}".format(values))
            r[indexes] = values
    return r