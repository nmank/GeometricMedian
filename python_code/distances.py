import numpy as np
import matplotlib.pyplot as plt

'''
TODO:
Need to add option to check for X == Y case - can use symmetry to reduce calculations
documentation descriptions
also fix the angle one probably

Recent fixes: JESUS CHRIST NOT EVERYTHING IS X==Y WHY DID I HARD CODE THAT ASLKDFJALEIJF
Fixed check for numbers numerically near zero 1/7
'''


def geodesic(C, X, t):
    m = C.shape[0]
    np.dot(np.dot(np.eye(m) - np.dot(C, C.T), X), np.linalg.inv(np.dot(C.T, X)))
    U, S, Vh = np.linalg.svd(np.dot(np.dot(np.eye(m) - np.dot(C, C.T), X), np.linalg.inv(np.dot(C.T, X))),
                             full_matrices=False)
    Y = np.dot(C, np.dot(Vh.T, np.diag(np.cos(np.arctan(S)*t)))) + np.dot(U, np.diag(np.sin(np.arctan(S)*t)))
    Q = np.linalg.qr(Y)[0]
    return Q


def chordal_distance(X, Y):
    # X, Y are lists of array representations of subspaces
    m = len(X)
    n = len(Y)
    distance = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            costheta = np.linalg.svd(np.dot(X[i].T, Y[j]))[1]
            sinsquares = 1 - costheta**2
            distance[i, j] = np.sum(sinsquares)
    distance[distance < 10e-12] = 0
    return distance


def geodesic_distance(X, Y):
    # X, Y are lists of array representations of subspaces
    m = len(X)
    n = len(Y)
    distance = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            costheta = np.linalg.svd(np.dot(X[i].T, Y[j]))[1]
            costheta[costheta >= 1] = 1.  # slight numerical issue; values slightly above one were yielding nans
            theta = np.arccos(costheta)
            distance[i, j] = np.sum(theta**2)
    distance[distance < 10e-12] = 0
    return distance


def prin_angle_distance(X, Y):
    # X, Y are lists of array representations of subspaces
    m = len(X)
    n = len(Y)
    distance = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            costheta = np.linalg.svd(np.dot(X[i].T, Y[j]))[1]
            distance[i, j] = np.arccos(costheta).max()
    distance[distance < 10e-12] = 0
    return distance


def mds(D, eigplot=False):
    # D is a pairwise distance squared matrix
    k = D.shape[0]
    H = np.eye(k) - 1/k*np.ones((k, k))
    B = np.dot(H, np.dot(-.5*D, H))
    eigs, V = np.linalg.eig(B)
    # Again with the numerical issues
    indx = np.argsort(-eigs.real)
    eigs = eigs.real[indx]
    if eigplot:
        h = plt.figure()
        plt.plot(eigs, '-o')
        plt.title('Eigenvalues for MDS')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.show()
    idx = np.nonzero(eigs > 0)[0]
    embedding = np.dot(V.real[:, indx[idx]], np.diag(eigs[idx]**.5))
    return embedding
