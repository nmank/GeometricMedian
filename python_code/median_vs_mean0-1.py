import numpy as np 
import gr_lbg
import load_mnist_data
import matplotlib.pyplot as plt
from sklearn import metrics
from  flag_mean import flag_mean
from flag_median import flag_median


k = 10
ss0 = 400
st = 'train'


means = []
medians = []

for ii in range(10):
    ss1 = (ii+1)*20

    data = []
    labels_before = []
    [dta, lbl] = load_mnist_data.load_mnist_data(0, ss0, st)
    for i in range(int(ss0/k)):
        data.append(np.linalg.qr(dta[:,i*k:(i+1)*(k)])[0])
        labels_before.append(lbl[0])
    [dta, lbl] = load_mnist_data.load_mnist_data(1, ss1, st)
    for i in range(int(ss1/k)):
        data.append(np.linalg.qr(dta[:,i*k:(i+1)*(k)])[0])
        labels_before.append(lbl[0])

    means.append(flag_mean(data)[:,0].reshape((28,28)))
    medians.append(flag_median(data,.0000000000001)[:,0].reshape((28,28)))


ig, axs = plt.subplots(2, 5)
for kk in range(5):
        axs[0, kk].imshow(np.abs(medians[kk]))
        axs[1, kk].imshow(np.abs(means[kk]))

#label the rows:
axs[0, 0].set_ylabel('Median')
axs[1, 0].set_ylabel('Mean')  
plt.show()