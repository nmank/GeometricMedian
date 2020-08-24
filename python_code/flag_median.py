import numpy as np
import flag_mean #
import distances #

'''
-maybe dont use squared error for convergence criteria

'''


def flag_median(X, eps, init = 'random', r='default', s_vals = False):
    #nate changed this
    
    if type(X) != list or len(X) == 0:
        return X
    
    medn = True 
    # X a list of subspaces, r desired dimension
    m = len(X)
    if r == 'default':
        r = X[0].shape[1]

    #initialize median
    if init == 'random':
        #randomly
        n = X[0].shape[0]
        Y_raw = np.random.rand(n,r)
        Y0 = np.linalg.qr(Y_raw)[0]
    else:
        #flag mean
        Y0 = flag_mean.flag_mean(X,r)

    i=0
    alph = []
    aX = []
    err = []
    al = []
    for j in range(m):
        al.append((r-np.trace(np.dot(np.dot(Y0.transpose(),X[j]),np.dot(X[j].transpose(),Y0))))**(-1/4))
        aX.append(al[j]*X[j])
    alph.append(al)
    Y1 = flag_mean.flag_mean(aX,r)
    err.append(distances.chordal_distance(Y0,Y1,medn))
    i += 1
    cauch = 1

    while cauch > eps:
        aX = []
        al = []
        for j in range(m):
            al.append((r-np.trace(np.dot(np.dot(Y1.transpose(),X[j]),np.dot(X[j].transpose(),Y1))))**(-1/4))
            aX.append(al[j]*X[j])
        alph.append(al)
        Y0 = Y1
        Y1 = flag_mean.flag_mean(aX,r)
        err.append(distances.chordal_distance(Y0,Y1,medn))
        cauch = err[i-1]-err[i]
        i += 1

    print(i)

    if cauch < 0:
        Y1 = Y0
        print('Last iteration of flag meadian increased error!')

    if s_vals:
        S = flag_mean.flag_mean(aX,r,s_vals)
        return S
    else:
        return Y1


