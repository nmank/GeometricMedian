import numpy as np 
import gr_lbg
import load_mnist_data
import matplotlib.pyplot as plt
from sklearn import metrics

def cluster_purity(labels,true_labels):
    contingency_matrix = metrics.cluster.contingency_matrix(true_labels, labels)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix) 

def load_data(k = 5, ss_big = 500, digits = [0,1,2,3,4,5,6,7,8,9], st = 'train'):
    data = []
    labels_before = []
    for d in digits:
            [dta, lbl] = load_mnist_data.load_mnist_data(d, ss_big, st)
            for i in range(int(ss_big/k)):
                    data.append(np.linalg.qr(dta[:,i*k:(i+1)*(k)])[0])
                    labels_before.append(lbl[0])
    return [data,labels_before]

def run_grlbg(do_median, data, labels_before, Ldims = 5,psval = False, purity = False):


        lbg_test_obj = gr_lbg.gr_lbg()

        #last param is the number of left singular vectors that we want.
        if purity:
            #select center from data
            lbg_test_obj.center_select = 'data'
            [centers,labels_after_med] = lbg_test_obj.fit(data,center_count = 10, median = True, l_vec_dims = Ldims, plot_svals = psval, distortion_plot=False)
            [centers,labels_after_mean] = lbg_test_obj.fit(data,center_count = 10, median = False, l_vec_dims = Ldims, plot_svals = psval, distortion_plot=False)
            return [cluster_purity(labels_after_med,labels_before),cluster_purity(labels_after_mean,labels_before)]
        
        if psval:
            [centers,labels_after,S] = lbg_test_obj.fit(data,center_count = 10, median = do_median, l_vec_dims = Ldims, plot_svals = psval)
            print('Cluster Purity: ')
            print(cluster_purity(labels_after,labels_before))
            return centers, S
        else:
            [centers,labels_after] = lbg_test_obj.fit(data,center_count = 10, median = do_median, l_vec_dims = Ldims, plot_svals = psval)
            print(cluster_purity(labels_after,labels_before))
            print('Cluster Purity: ')
            
            return centers

ss_big = 500
#gr(k,n), k<n and k must divide ss_big
k=5
#out_k is number of singular vectors (space for the median or the mean)
out_k = 5
#load the data
[data,labels_before] = load_data(k, ss_big)


################################

#repeat Shannon's test
purity_mean = []
purity_median = []
for i in range(100):
    [med,mean] = run_grlbg(True, data, labels_before, Ldims = out_k,purity=True)
    purity_median.append(med)
    purity_mean.append(mean)
    
