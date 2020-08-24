import numpy as np

def flag_mean(X, r='default', s_vals = False):
    # X a list of subspaces, r desired dimension
    if type(X) == list and len(X) > 1:
        m = len(X)
        if r == 'default':
            r = X[0].shape[1]
        A = X[0]
        for i in range(m-1):
            A = np.hstack((A, X[i+1]))
        if s_vals:
            S = np.linalg.svd(A, full_matrices=False)[1]
            return S
        else:
            U = np.linalg.svd(A, full_matrices=False)[0]
            return U[:,:r]
    else:
        return X
