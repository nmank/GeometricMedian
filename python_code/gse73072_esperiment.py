import sys
sys.path.append('/data3/darpa/calcom')
import numpy as np 
import calcom
import modules
from sklearn import datasets, linear_model
from sklearn.preprocessing import normalize
from numpy import genfromtxt
import matplotlib.pyplot as plt
import scipy.spatial as sp
import csv
import gr_lbg
from sklearn import metrics


#parameters





#load the data
times = [2, 4, 5, 8, 10, 12, 16, 18, 20, 21, 22, 24, 26, 29, 30, 34, 36, 42, 45, 46, 48, 50, 53, 58, 60, 66, 69, 70, 72, 74, 77, 82, 84, 90, 93, 94, 96, 98, 101, 106, 108, 114, 118, 120, 122, 125, 130, 132, 136, 138, 142, 146, 162, 166, 170, 680]
ccd = calcom.io.CCDataSet('/data3/darpa/all_CCD_processed_data/ccd_gse73072_geneid.h5')

#data sorting
sID = ccd.generate_labels('SubjectID')
subject_list = []
for s in sID:
	lil = []
	for t in times:
		q = {'time_id' : t, 'shedding' : True, 'SubjectID' : s}
		idx = ccd.find(q)
		if len(idx) > 0:
			lil.append(t)
	if len(lil) > 0:
		subject_list.append(lil)

counts = [] 
ii=0 
for t in times: 
    counts.append(0) 
    for s in subject_list: 
        if t in s: 
            counts[ii] = counts[ii]+1 
    ii+=1 

idd = np.where(np.array(counts) > 1000)[0]
#time indices with more than 1000 subjects
print(idd)

for i in idd:
    print(times[i])


#TRY DIFFERENT TIMES


#how many subjects do we have with these three times?
small_times = [36,53,60]
count = 0
for s in sID:
	q = {'time_id' : small_times, 'shedding' : True, 'SubjectID' : s}
	idx = ccd.find(q)
	if len(idx) > 0:
		count +=1

idx1 = ccd.feature_sets['pw404']

all_disease = ccd.generate_labels('disease')
data_list = []
subject_ids = []
labels_before = []
for s in sID:
	data_temp = []
	for t in small_times:
		q = {'SubjectID' : s, 'time_id' : t, 'shedding' : True}
		idx = ccd.find(q)
		if len(idx) > 0:
			data_temp.append(np.log((ccd.generate_data_matrix(idx=idx)[:,idx1]).T))
	if len(data_temp) == 3:
		data_list.append(np.linalg.qr(np.hstack(data_temp))[0])
		labels_before.append(all_disease[idx][0])
		subject_ids.append(s)


def cluster_purity(labels,true_labels):
    contingency_matrix = metrics.cluster.contingency_matrix(true_labels, labels)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix) 

def run_grlbg(do_median, data, labels_before, Ldims = 5,psval = False, purity = False):


        lbg_test_obj = gr_lbg.gr_lbg()

        #center initialization
        lbg_test_obj.center_select = 'random'
        #lbg_test_obj.center_select = 'troubleshoot' #initialize with properly labeled data points

        #last param is the number of left singular vectors that we want.
        if purity:
            #select center from data
            lbg_test_obj.center_select = 'data'
            [centers,labels_after_med] = lbg_test_obj.fit(data,center_count = 4, median = True, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            [centers,labels_after_mean] = lbg_test_obj.fit(data,center_count = 4, median = False, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            return [cluster_purity(labels_after_med,labels_before),cluster_purity(labels_after_mean,labels_before)]
        
        if psval:
            [centers,labels_after,S] = lbg_test_obj.fit(data,center_count = 4, median = do_median, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            print('Cluster Purity: ')
            print(cluster_purity(labels_after,labels_before))
            return centers, S
        else:
            [centers,labels_after] = lbg_test_obj.fit(data,center_count = 4, median = do_median, l_vec_dims = Ldims, plot_svals = psval, eigplot = False, distortion_plot = False)
            print('Cluster Purity: ')
            print(cluster_purity(labels_after,labels_before))
            
            
            return centers

#gr(k,n), k<n and k must divide ss_big
k=3
#out_k is number of singular vectors (space for the median or the mean)
out_k = 3



run_grlbg(True, data_list, labels_before, Ldims = out_k, purity = True)


########################################################################################


import distances
from sklearn.manifold import MDS

centers_median = run_grlbg(True, data_list, labels_before, Ldims = out_k)
centers_mean = run_grlbg(False, data_list, labels_before, Ldims = out_k)
plt.show()
plt.savefig('plot1.png')

plot_data = centers_median+centers_mean+data_list

pairwise_dist = distances.chordal_distance(plot_data, plot_data, True)
embedding = MDS(n_components=2, dissimilarity = 'precomputed')
embed_coords = embedding.fit_transform(pairwise_dist)


for i in np.unique(labels_before):
	idx = np.where(np.array(labels_before) == i)[0]
	plt.plot(embed_coords[idx+8, 0], embed_coords[idx+8, 1], '.', label=i)
plt.plot(embed_coords[0:3,0],embed_coords[0:3,1],'x',color = 'k',label='median')
plt.plot(embed_coords[3:6,0],embed_coords[3:6,1],'x',color = 'r',label='mean')
plt.legend()
plt.savefig('plot2.png')



##############################################

#load data and do mds
pairwise_dist = distances.chordal_distance(data_list, data_list, False)
data_transformed = distances.mds(pairwise_dist)
plt.scatter(data_transformed[0,:],data_transformed[1,:])





