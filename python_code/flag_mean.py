import numpy as np

'''
TODO:
fix default case for averaging subspaces of different dimensions - choose smallest
documentation descriptions

Change log:
Forgot how python slicing works, finally remembered - 1/7
'''


def flag_mean(X, r='default'):
    # X a list of subspaces, r desired dimension
    m = len(X)
    if r == 'default':
        r = X[0].shape[1]
    A = X[0]
    for i in range(m-1):
        A = np.hstack((A, X[i+1]))
    U = np.linalg.svd(A, full_matrices=False)[0]
    return U[:, 0:r]
