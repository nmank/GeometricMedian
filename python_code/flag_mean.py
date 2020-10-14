import numpy as np

def flag_mean(X, r='default', s_vals = False):
    # X a list of subspaces, r desired dimension
    if type(X) == list and len(X) > 1:
        if r == 'default':
            r = X[0].shape[1]
        A = np.hstack(X)
        if s_vals:
            S = np.linalg.svd(A, full_matrices=False)[1]
            return S
        else:
            U = np.linalg.svd(A, full_matrices=False)[0]
            return U[:,:r]
    else:
        return X
