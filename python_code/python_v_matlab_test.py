import numpy as np
import flag_median


data = [np.array([[-0.8941, 0.4368, 0.0988]]),   np.array([[-0.3256, 0.5909, -0.7381]]), np.array([[-0.2475, -0.5845,  0.7727 ]]),   np.array([[0.3400,  -0.9399 , -0.0327]]), np.array([[-0.1297, 0.4937, 0.8599]]) ]
data = [d.T for d in data]

labels = np.arange(5)
label_names = labels

eps = .000001

x = flag_median.flag_median(data, eps, data[0].shape[1], init = 'rsf')