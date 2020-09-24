import numpy as np
# import sys
# sys.path.append('./covid-chestxrray-dataset/images')
import gr_lbg
import matplotlib
from matplotlib import pyplot as plt
import torch 
import torchvision 
import torchxrayvision as xrv 
from tqdm import tqdm 
import pandas as pd 
import sys
from skimage.transform import resize
from sklearn import metrics
import flag_mean
import flag_median
import distances



def cluster_purity(labels,true_labels):
    contingency_matrix = metrics.cluster.contingency_matrix(true_labels, labels)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix) 

def load_data(data_array, labels_before,k = 2):
	data = []
	labels = []
	label_set = np.unique(labels_before,axis=0)
	ii = 0
	for l in label_set:
		idx = np.where(labels_before == l)[0]
		for i in idx:
			data.append(np.linalg.qr(data_array[i])[0][:,:k])
			labels.append(ii)
		ii+=1


	return [data,labels]

def run_grlbg(do_median, data, labels_before, Ldims = 5,psval = False, purity = False):


        lbg_test_obj = gr_lbg.gr_lbg()

        #center initialization
        lbg_test_obj.center_select = 'random'
        #lbg_test_obj.center_select = 'troubleshoot' #initialize with properly labeled data points

        #last param is the number of left singular vectors that we want.
        if purity:
            #select center from data
            lbg_test_obj.center_select = 'data'
            [centers,labels_after_med] = lbg_test_obj.fit(data,center_count = 6, median = True, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            [centers,labels_after_mean] = lbg_test_obj.fit(data,center_count = 6, median = False, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            return [cluster_purity(labels_after_med,labels_before),cluster_purity(labels_after_mean,labels_before)]
        
        if psval:
            [centers,labels_after,S] = lbg_test_obj.fit(data,center_count = 6, median = do_median, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            print('Cluster Purity: ')
            print(cluster_purity(labels_after,labels_before))
            return centers, S
        else:
            [centers,labels_after] = lbg_test_obj.fit(data,center_count = 6, median = do_median, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            print('Cluster Purity: ')
            print(cluster_purity(labels_after,labels_before))
            
            
            return centers

#gr(k,n), k<n and k must divide ss_big
k=5
#out_k is number of singular vectors (space for the median or the mean)
out_k = 2
#load the data
d_covid19 = xrv.datasets.COVID19_Dataset(views=["PA", "AP", "AP Supine"], 
                                          imgpath="covid-chestxray-dataset/images", 
                                          csvpath="covid-chestxray-dataset/metadata.csv")

labels_raw = []
data_raw = []
count = 0
for d in d_covid19:
    data_raw.append(resize(d['img'][0],(200,200)))
    labels_raw.append(d['lab'])


label_lists = np.unique(labels_raw, axis = 0) 


covid_data_labels = []
for l in label_lists:
    if l[2] != 0:
        covid_data_labels.append(l)

covid_idx = []
healthy_idx = []
ii = 0
for l in labels_raw:
    if (covid_data_labels[0]==l).all() or (covid_data_labels[1]==l).all():
        covid_idx.append(ii)
    if (np.zeros(18) == l).all():
        healthy_idx.append(ii)
    ii += 1

data_covid = []
for idx in covid_idx:
    data_covid.append(np.linalg.qr(data_raw[idx])[0][:,:k])

data_healthy = []
for idx in healthy_idx:
    data_healthy.append(np.linalg.qr(data_raw[idx])[0][:,:k])

data = data_healthy + data_covid

medians = []
means = []
for i in range(20):
    #load the data  
    medians.append(flag_median.flag_median(data[:57+ 2*i],.000001,k))
    means.append(flag_mean.flag_mean(data[:57 + 2*i]))



#plot first column
# data_1comp = np.vstack([d[:,0] for d in data])
# plot_data = np.vstack( [data_1comp, np.vstack([md[:,0] for md in medians]), np.vstack([mn[:,0] for mn in means])] )

#plot all data
plot_data = data + medians + means

#Using sklearn mds
# embedding = mds.MDS(n_components=2) 
# data_transformed = embedding.fit_transform(plot_data)

#Using sklearn PCA
# embedding = PCA(n_components=2) 
# data_transformed = embedding.fit_transform(plot_data)

#Using distances.mds
pairwise_dist = distances.chordal_distance(plot_data, plot_data, False)
data_transformed = distances.mds(pairwise_dist)


for i in range(19):
    plt.scatter(data_transformed[:57,0], data_transformed[:57,1], label = 'Healthy')
    plt.scatter(data_transformed[57:57+ 2*i,0], data_transformed[57:57+ 2*i,1], label = 'Covid')
    plt.scatter(data_transformed[486 + i,0], data_transformed[486 + i,1], marker = 'o', c = 'r', label = 'median')
    plt.scatter(data_transformed[506 + i,0], data_transformed[506 + i,1], marker = 'o', c= 'k', label = 'mean')
    plt.legend()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.savefig('covid_poison_'+str(i)+'.png')
    plt.close()




#GRLGB STUFF

#[data_list, labels_before] = load_data(data_raw[:100], labels_raw[:100])

# run_grlbg(True, data_list, labels_before, Ldims = out_k, purity = True)

# #put it into gr(k,n)

# ###############################

# #return singular values
# #broken
# [centers_median,S_median] = run_grlbg(True, data_list, labels_before, Ldims = out_k, sval = True)
# [centers_mean,S_mean] = run_grlbg(False, data_list, labels_before, Ldims = out_k, sval = True)
# plt.show()
# #plotting singularvalues
# for kk in range(10):
#         plt.plot(S_median[kk]/np.max(S_median[kk]), 'b')
#         plt.plot(S_mean[kk]/np.max(S_mean[kk]), 'r')
# plt.show()

# ###############################

# #return cluster centers
# centers_median = run_grlbg(True, data_list, labels_before, Ldims = out_k)
# centers_mean = run_grlbg(False, data_list, labels_before, Ldims = out_k)
# plt.show()
# #have to tweak around a bit with the plot to line up centers
# fig, axs = plt.subplots(2, 5)
# for kk in range(5):
#         axs[0, kk].imshow(np.reshape(centers_median[3][:,kk],(28,28)))
#         axs[1, kk].imshow(np.reshape(centers_mean[1][:,kk],(28,28)))

# #label the rows:
# axs[0, 0].set_ylabel('Median')
# axs[1, 0].set_ylabel('Mean')  

# # remove the x and y ticks
# for ax in axs:
#         for a in ax:
#             a.set_xticks([])
#             a.set_yticks([])
            
# fig.tight_layout()
# plt.show()


# ###############################
# #mds visualization of centers
# import distances
# from sklearn.manifold import MDS

# centers_median = run_grlbg(True, data_list, labels_before, Ldims = out_k)
# centers_mean = run_grlbg(False, data_list, labels_before, Ldims = out_k)
# plt.show()
# plt.savefig('plot1.png')

# plot_data = centers_median+centers_mean+data_list

# pairwise_dist = distances.chordal_distance(plot_data, plot_data, True)
# embedding = MDS(n_components=2, dissimilarity = 'precomputed')
# embed_coords = embedding.fit_transform(pairwise_dist)


# for i in np.unique(labels_before):
# 	idx = np.where(np.array(labels_before) == i)[0]
# 	plt.plot(embed_coords[idx+6, 0], embed_coords[idx+6, 1], '.', label='Cluster %i' % i)
# plt.plot(embed_coords[0:3,0],embed_coords[0:3,1],'x',color = 'k',label='median')
# plt.plot(embed_coords[3:6,0],embed_coords[3:6,1],'x',color = 'r',label='mean')
# plt.legend()
# plt.savefig('plot2.png')
