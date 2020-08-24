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

        #center initialization
        lbg_test_obj.center_select = 'random'
        #lbg_test_obj.center_select = 'troubleshoot' #initialize with properly labeled data points

        #last param is the number of left singular vectors that we want.
        if purity:
            #select center from data
            lbg_test_obj.center_select = 'data'
            [centers,labels_after_med] = lbg_test_obj.fit(data,center_count = 10, median = True, l_vec_dims = Ldims, plot_svals = psval)
            [centers,labels_after_mean] = lbg_test_obj.fit(data,center_count = 10, median = False, l_vec_dims = Ldims, plot_svals = psval)
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

###############################

#return singular values
[centers_median,S_median] = run_grlbg(True, data, labels_before, Ldims = out_k,psval = True)
[centers_mean,S_mean] = run_grlbg(False, data, labels_before, Ldims = out_k,psval = True)
plt.show()
#plotting singularvalues
for kk in range(10):
        plt.plot(S_median[kk]/np.max(S_median[kk]), 'b')
        plt.plot(S_mean[kk]/np.max(S_mean[kk]), 'r')
plt.show()

###############################

#return cluster centers
centers_median = run_grlbg(True, data, labels_before, Ldims = out_k)
centers_mean = run_grlbg(False, data, labels_before, Ldims = out_k)
plt.show()
#have to tweak around a bit with the plot to line up centers
fig, axs = plt.subplots(2, 5)
for kk in range(5):
        axs[0, kk].imshow(np.reshape(centers_median[3][:,kk],(28,28)))
        axs[1, kk].imshow(np.reshape(centers_mean[1][:,kk],(28,28)))

#label the rows:
axs[0, 0].set_ylabel('Median')
axs[1, 0].set_ylabel('Mean')  

# remove the x and y ticks
for ax in axs:
        for a in ax:
            a.set_xticks([])
            a.set_yticks([])
            
fig.tight_layout()
plt.show()


###############################
#mds visualization of centers
import distances

centers_median = run_grlbg(True, data, labels_before, Ldims = out_k)
centers_mean = run_grlbg(False, data, labels_before, Ldims = out_k)
plt.show()

plot_data = centers_median+centers_mean+data

pairwise_dist = distances.chordal_distance(plot_data, plot_data, True)
embed_coords = distances.mds(pairwise_dist)

for i in np.unique(labels_before):
        idx = np.where(labels_before == i)[0]
        plt.plot(embed_coords[idx+20, 0], embed_coords[idx+20, 1], '.', label='Cluster %i' % i)
plt.plot(embed_coords[0:10,0],embed_coords[0:10,1],'x',color = 'k',label='median')
plt.plot(embed_coords[10:20,0],embed_coords[10:20,1],'x',color = 'r',label='mean')
plt.legend()
plt.show()

