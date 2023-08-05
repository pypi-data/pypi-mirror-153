import numpy as np
import ranking_aggregation.preferences.scores as scores

def _boolean_matrix(profile):
    half = (profile[0,1]+profile[1,0])/2
    return (profile > half).astype(np.uint8)

def smith_matrix(profile):
    s = scores.copeland_score(profile)
    # s = scores.scores_to_ranking(s)
    s = np.flip(np.argsort(s))
    print(s)
    bm = _boolean_matrix(profile)
    print(bm)
    bm = bm[s,:]
    bm = bm[:,s]
    result = {}
    result['matrix'] = bm
    result['ids'] = s
    return result

def smith_set(profile):
    the_matrix = smith_matrix(profile)
    alt_names = the_matrix['ids']
    the_matrix = the_matrix['matrix']
    for i in range(1,profile.shape[0]):
        total = 0
        for j in range(i):
            total += profile[i:,j]
        if total == 0: 
            return i
    result = {}
    result['winners'] = alt_names[:i]
    result['losers'] = alt_names[i:]
    return result