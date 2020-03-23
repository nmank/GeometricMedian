import numpy as np 
import gr_lbg
import load_mnist_data
import matplotlib.pyplot as plt 


ss_big = 200
#gr(k,n), k<n and k must divide ss_big
k=5
#digits =[0,1,2,3,4,5,6,7,8,9]
digits =[3,5,6]
st = 'train'
do_median = True

data = []
labels_before = []
for d in digits:
	[dta, lbl] = load_mnist_data.load_mnist_data(d, ss_big, st)
	for i in range(int(ss_big/k)):
		data.append(np.linalg.qr(dta[:,i*k:(i+1)*(k)])[0])
		labels_before.append(lbl[0])


lbg_test_obj = gr_lbg.gr_lbg()
#lbg_test_obj.center_select = 'random'

[centers,labels_after] = lbg_test_obj.fit(data,center_count = 3, median = do_median)

gr_lbg.print_cluster_data(centers, labels_after, labels_before)
gr_lbg.embed_plot_results(data,centers,labels_before, mdn = do_median) 

plt.imshow(np.reshape(centers[0][:,0],(28,28))) 
plt.imshow(np.reshape(centers[1][:,0],(28,28))) 
plt.imshow(np.reshape(centers[2][:,0],(28,28))) 