import numpy as np
import flag_mean #
import distances #

'''
-maybe dont use squared error for convergence criteria

'''


def flag_median(X, eps, init = 'random', r='default'):
	# X a list of subspaces, r desired dimension
	m = len(X)
	if r == 'default':
		r = X[0].shape[1]
		
	#initialize median
	if init == 'random':
		#randomly
		n =X[0].shape[0]
		Y_raw = np.random.rand(n,r)
		Y0 = np.linalg.qr(Y_raw)[0]		
	else:
		#flag mean
		Y0 = flag_mean.flag_mean(X,r)	

	i=0
	alph = []
	aX = []
	err = []
	for j in range(m):
		alph[j,i] = (r-trace(np.dot(np.dot(Y.transpose(),X[j]),np.dot(X[j].transpose(),Y))))**(-1/4)
		aX[j] = alph[j,i]*X[j]
	Y0 = Y1
	Y1 = flag_mean.flag_mean(aX,r)
	err[i] = distances.chordal_distance(Y0,Y1)
	cauch = 1

	while cauch > eps:
		aX = []
		for j in range(m):
			alph[j,i] = (r-trace(np.dot(np.dot(Y.transpose(),X[j]),np.dot(X[j].transpose(),Y))))**(-1/4)
			aX[j] = alph[j,i]*X[j]
		Y0 = Y1
		Y1 = flag_mean.flag_mean(X,r)
		i += 1
		err[i] = distances.chordal_distance(Y0,Y1)
		cauch = err[i-1]-err[i]

	if cauch < 0:
		Y1 = Y0
		print('Last iteration of flag meadian increased error!')

	return Y1


