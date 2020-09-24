import flag_mean
import flag_median
import load_mnist_data
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import mds
from sklearn.decomposition import PCA
import distances
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def load_data(k = 5, ss_big = 500, digits = [0,1,2,3,4,5,6,7,8,9], st = 'train'):
    data = []
    labels_before = []
    for d in digits:
            [dta, lbl] = load_mnist_data.load_mnist_data(d, ss_big, st)
            for i in range(int(ss_big/k)):
                data.append(np.linalg.qr(dta[:,i*k:(i+1)*(k)])[0])
                labels_before.append(lbl[0])
    return [data,labels_before]

ss_big = 500
#gr(k,n), k<n and k must divide ss_big
k=5
#out_k is number of singular vectors (space for the median or the mean)
out_k = 5
#load the data
[data0,labels_before0] = load_data(k, ss_big, digits = [1])
[data1,labels_before1] = load_data(k, ss_big, digits = [8])
data = data0 + data1

medians = []
means = []
for i in range(20):
    #load the data  
    medians.append(flag_median.flag_median(data[:100+ 10*i],.000001,k))
    means.append(flag_mean.flag_mean(data[:100 + 10*i]))


medians_list = []
means_list = []
for i in range(len(medians)):
    medians_list.append(medians[i][:,0])
    means_list.append(means[i][:,0])

medians_vec = np.vstack(medians_list)
means_vec = np.vstack(means_list)


svm_data_list = []
svm_labels = []
num_samples = 400
for d in [1,8]:
    [dta, lbl] = load_mnist_data.load_mnist_data(d, num_samples, 'train')
    for i in range(int(num_samples)):
        svm_data_list.append(dta[:,i])
        svm_labels.append(lbl[0])

svm_data = np.vstack(svm_data_list)

clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(svm_data, svm_labels)



clf.predict(means_vec)