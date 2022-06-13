'''
This file contains the FlagIRLS algorithm.

by Nathan Mankovich
    nathan.mankovich@gmail.com
'''


import numpy as np
import random

'''
TODO

- add L2 Median
- double check gradient descent
- fix PLS code for fast == True
- horst's algorithm?
'''



def gr_log(X,Y):
    '''
    Log map on the Grassmannian.
    
    Inputs:
        X (np.array) a point about which the tangent space has been computed
        Y (np.array) the point on the Grassmannian manifold that's mapped to the tangent space of X
    Outputs:
        TY (np.array) Y in the tangent space of X
    '''
    m = X.shape[0]

    #temp = (np.eye(m)-X @ X.T) @ Y @ np.linalg.inv(X.T@Y)
    #The following line is a slightly faster way to compute temp.

    temp = np.eye(m) @ Y @ np.linalg.inv(X.T @ Y) - X @ (X.T @ Y) @ np.linalg.inv(X.T @ Y)
    U,S,V = np.linalg.svd(temp, full_matrices = False)
    Theta = np.arctan(S)
    
    TY = U @ np.diag(Theta) @ V.T
    
    return TY
                                             

def gr_exp(X, TY):
    '''
    Calculate the exponential map on the Grassmannian.
    Inputs:
        X: (np.array) is the point about which the tangent space has been
          computed.
        TY: (np.array) is a point in the tangent space of X.
    Outputs:
        Y: The output of the exponential map.
    
    '''
    
    U, S, V = np.linalg.svd(TY, full_matrices = False)
    Y = X @ V @ np.diag(np.cos(S)) + U @ np.diag(np.sin(S))

    return Y

def gr_dist(X, Y):
    if X.shape[1] > 1:
        U,S,V = np.linalg.svd(X.T @ Y, full_matrices = False)
        S[np.where(S >1)] = 1
#         S[np.where(S < -1)] = -1
        angles = np.real(np.arccos(S))
#         print(angles)
        dist = np.linalg.norm(angles)
    else:
        dist = calc_error_1_2([X], Y, 'geodesic')
    return dist


def l2_median(data, alpha, r, max_itrs, seed=0, init_datapoint = False):
    
    n = data[0].shape[0]
    
    if init_datapoint:
        np.random.seed(seed)
        Y = data[np.random.randint(len(data))]
    else:
        np.random.seed(seed)
        Y_raw = np.random.rand(n,r)-.5
        Y = np.linalg.qr(Y_raw)[0][:,:r]
    
    itr = 0
    errs = []
    diff = 1
    
    while diff > 0.000001 and itr < max_itrs:
        d_fracs = 0
        ld_fracs = np.empty((n,r))
        dists = []
        for x in data:
            dists.append(gr_dist(x, Y))
            if dists[-1] > .0001:
                d_fracs += 1 / dists[-1]
                ld_fracs += gr_log(Y, x) / dists[-1]
            else:
                print('converged to datapoint')

        if len(ld_fracs)==0:
            return Y
        else:
            vk = ld_fracs/d_fracs
            Y = gr_exp(Y, alpha * vk)
            
            errs.append(np.sum(dists))
            
            if itr > 0:
                diff = np.abs(errs[-2] - errs[-1])
            
            if not np.allclose(Y.T @ Y, np.eye(r,r)):
                Y = np.linalg.qr(Y)[0][:,:r]
            
            itr+=1 
    
    return Y, errs



def calc_error_1_2(data, Y, sin_cos):
    '''
    Calculate objective function value. 

    Inputs:
        data - a list of numpy arrays representing points in Gr(k_i,n)
        Y - a numpy array representing a point on Gr(r,n) 
        sin_cos - a string defining the objective function
                    'cosine' = Maximum Cosine
                    'sine' = Sine Median
                    'sinsq' = Flag Mean
                    'geodesic' = Geodesic Median (CAUTION: only for k_i = r = 1)
    Outputs:
        err - objective function value
    '''
    k = Y.shape[1]
    err = 0
    if sin_cos == 'cosine':
        for x in data:
            err += np.sqrt(np.trace(Y.T @ x @ x.T @ Y))
    elif sin_cos == 'sine':
        for x in data:
            r = np.min([k,x.shape[1]])
            sin_sq = r - np.trace(Y.T @ x @ x.T @ Y)
            #fixes numerical errors
            if sin_sq < 0:
                sin_sq = 0
            err += np.sqrt(sin_sq)
    elif sin_cos == 'sinesq':
        for x in data:
            r = np.min([k,x.shape[1]])
            sin_sq = r - np.trace(Y.T @ x @ x.T @ Y)
            #fixes numerical errors
            if sin_sq < 0:
                sin_sq = 0
            err += sin_sq
    elif sin_cos == 'geodesic':
        for x in data:
            cos = (Y.T @ x @ x.T @ Y)[0][0]
            #fixes numerical errors
            if cos > 1:
                cos = 1
            elif cos < 0:
                cos = 0
            err += np.arccos(np.sqrt(cos))
    elif sin_cos == 'l2_med':
        for x in data:
            err += gr_dist(x, Y)
    return err


'''
Calculate the Flag Mean

Inputs:
    data - list of numpy arrays representing points on Gr(k_i,n)
    r - integer number of columns in flag mean
    fast - use faster eigenvalue calculation
Outputs:
    mean - a numpy array representing the Flag Mean of the data
'''
def flag_mean(data, r, fast = False):
    X = np.hstack(data)
    
    #This doesn't work yet!
    if fast:
        #Initialize
        # U  = X[:,:k][:] 
        mean = np.random.rand(X.shape[0],r)
        V = np.zeros((X.shape[1],r))

        #err[j] stores 2-norm squared difference between ith and (i+1)th iterate of U[:,j]
        err = []
        #iteration of partial least squares
        for j in range(r):
            err1 = []
            err1.append(1)
            while err1[-1] > .000000001:
            # for _ in range(n_iters):
                old_U = mean[:,[j]][:]
                V[:,j] = mean[:,j] @ X / (mean[:,j] @ mean[:,[j]])
                V[:,j] = V[:,j]/np.linalg.norm(V[:,j])
                new_U =  X @ V[:,[j]] / (V[:,j] @ V[:,[j]])
                err1.append(np.linalg.norm(old_U - new_U)**2)
                mean[:,[j]] = new_U[:]
            err.append(err1[1:])
        
    else:
        mean = np.linalg.svd(X, full_matrices = False)[0][:,:r]
    return mean



'''
Calculates a weighted Flag Mean of data using a weight method for FlagIRLS
 eps = .0000001 for paper examples

Inputs:
    data - list of numpy arrays representing points on Gr(k_i,n)
    Y0 - a numpy array representing a point on Gr(r,n)
    weight - a string defining the objective function
                'cosine' = Maximum Cosine
                'sine' = Sine Median
                'sinsq' = Flag Mean
                'geodesic' = Geodesic Median (CAUTION: only for k_i = r = 1)
    fast - use faster eigenvalue calculation
    eps - a small perturbation to the weights to avoid dividing by zero
Outputs:
    Y- the weighted flag mean
'''
def flag_mean_iteration(data, Y0, weight, fast = False, eps = .0000001, stochastic = 0):
    r = Y0.shape[1]
    
    aX = []
    al = []

    ii=0

    if stochastic > 0:
        data = random.sample(data,stochastic)

    for x in data:
        if weight == 'cosine':
            cossq = np.trace(Y0.T @ x @ x.T @ Y0)
            al.append((cossq+eps)**(-1/4))
        elif weight == 'sine':
            m = np.min([r,x.shape[1]])
            sinsq = m - np.trace(Y0.T @ x @ x.T @ Y0)
            al.append((sinsq+eps)**(-1/4))
        elif weight == 'geodesic':
            sinsq = 1 - Y0.T @ x @ x.T @ Y0
            cossq = Y0.T @ x @ x.T @ Y0
            al.append((sinsq*cossq + eps)**(-1/4))
        else:
            print('sin_cos must be geodesic, sine or cosine')
        aX.append(al[-1]*x)
        ii+= 1

    Y = flag_mean(aX, r, fast)

    return Y


'''
Use FlagIRLS on data to output a representative for a point in Gr(r,n) 
which solves the input objection function

Repeats until iterations = n_its or until objective function values of consecutive
iterates are within 0.0000000001 and are decreasing for every algorithm (except increasing for maximum cosine)

Inputs:
    data - list of numpy arrays representing points on Gr(k_i,n)
    r - the number of columns in the output
    n_its - number of iterations for the algorithm
    sin_cos - a string defining the objective function for FlagIRLS
                'cosine' = Maximum Cosine
                'sine' = Sine Median
                'sinsq' = Flag Mean
                'geodesic' = Geodesic Median (CAUTION: only for k_i = r = 1)
    opt_err - string for objective function values in err (same options as sin_cos)
    fast - use faster eigenvalue calculation
    init - string 'random' for random initlalization. 
           otherwise input a numpy array for the inital point
    seed - seed for random initialization, for reproducibility of results
Outputs:
    Y - a numpy array representing the solution to the chosen optimization algorithm
    err - a list of the objective function values at each iteration (objective function chosen by opt_err)
'''
def irls_flag(data, r, n_its, sin_cos, opt_err = 'geodesic', fast = False, init = 'random', seed = 0, stochastic = 0): 
    err = []
    n = data[0].shape[0]


    #initialize
    if init == 'random':
        #randomly
        np.random.seed(seed)
        Y_raw = np.random.rand(n,r)-.5
        Y = np.linalg.qr(Y_raw)[0][:,:r]
    elif init == 'data':
        np.random.seed(seed)
        Y = data[np.random.randint(len(data))]
    else:
        Y = init

    err.append(calc_error_1_2(data, Y, opt_err))

    #flag mean iteration function
    #uncomment the commented lines and 
    #comment others to change convergence criteria
    
    itr = 1
    diff = 1
    #changed from 0.0000000001
    while itr <= n_its and diff > 1e-12:
        Y0 = Y.copy()
        Y = flag_mean_iteration(data, Y, sin_cos, fast, stochastic  = stochastic)
        err.append(calc_error_1_2(data, Y, opt_err))
#         diff = np.abs(err[itr] - err[itr-1])
        diff  = err[itr-1] - err[itr]
        if sin_cos == 'cosine':
            diff = -diff
           
        itr+=1
    
#     if diff < 0.0000000001:
#         print('FlagIRLS not converged')
    
#     return Y, err


    if diff > 0:
        return Y, err
    else:
        return Y0, err[:-1]

'''
Calculates the gradient of a given Y0 and data given an objective function
Inputs:
    data - list of numpy arrays representing points on Gr(k_i,n)
    Y0 - a representative for a point on Gr(r,n)
    weight - a string defining the objective function
                'cosine' = Maximum Cosine
                'sine' = Sine Median
                'sinsq' = Flag Mean
                'geodesic' = Geodesic Median (CAUTION: only for k_i = r = 1)
Output:
    grad - numpy array of the gradient

'''
def calc_gradient(data, Y0, weight):
    k = Y0.shape[1]
    aX = []
    al = []
    for x in data:
        if weight == 'cosine':
            al.append(np.trace(Y0.T @ x @ x.T @ Y0)**(-1/4))
        elif weight == 'sine':
            r = np.min([k,x.shape[1]])
            sin_sq = r - np.trace(Y0.T @ x @ x.T @ Y0)
            if sin_sq < .00000001 :
                sin_sq = 0
                print('converged to datapoint')
            else:
                al.append(sin_sq**(-1/4))
        elif weight == 'geodesic':
            r = np.min([k,x.shape[1]])
            al.append(((1 - Y0.T @ x @ x.T @ Y0)**(-1/4))*((Y0.T @ x @ x.T @ Y0)**(-1/4)))
        else:
            print('sin_cos must be geodesic, sine or cosine')
        aX.append(al[-1]*x)

    big_X = np.hstack(aX)
    
    grad = big_X @ big_X.T @ Y0

    return grad


'''
Runs Grassmannian gradient descent
Inputs:
    data - list of numpy arrays representing points on Gr(k,n)
    r - integer for the number of columns in the output
    alpha - step size
    n_its - number of iterations
    sin_cos - a string defining the objective function
                'cosine' = Maximum Cosine
                'sine' = Sine Median
                'sinsq' = Flag Mean
                'geodesic' = Geodesic Median (CAUTION: only for k_i = r = 1)
    init - string 'random' for random initlalization. 
           otherwise input a numpy array for the inital point
Outputs:
    Y - a numpy array representing the solution to the chosen optimization algorithm
    err - a list of the objective function values at each iteration (objective function chosen by opt_err)
'''
def gradient_descent(data, r, alpha, n_its, sin_cos, init = 'random', seed = 0):
    n = data[0].shape[0]

    #initialize
    if init == 'random':
        np.random.seed(seed)
        #randomly
        Y_raw = np.random.rand(n,r)
        Y = np.linalg.qr(Y_raw)[0][:,:r]
    else:
        Y = init

    err = []
    err.append(calc_error_1_2(data, Y, sin_cos))

    for _ in range(n_its):
        Fy = calc_gradient(data,Y,sin_cos)
        # project the gradient onto the tangent space
        G = (np.eye(n)-Y@Y.T)@Fy
        
        [U,S,V] = np.linalg.svd(G)
        cosin = np.diag(np.cos(-alpha*S))
        sin = np.vstack([np.diag(np.sin(-alpha*S)), np.zeros((n-r,r))])
        if cosin.shape[0] == 1:
            Y = Y*V*cosin*V.T+U@sin *V.T
        else:
            Y = Y@V@cosin@V.T+U@sin@V.T
        
        err.append(calc_error_1_2(data, Y, sin_cos))
    return Y, err