import numpy as np 
import gr_lbg
import load_mnist_data
import matplotlib.pyplot as plt


def run_grlbg(do_median, k = 5, ss_big = 200, digits = [3,5,6], st = 'train'):
        data = []
        labels_before = []
        for d in digits:
                [dta, lbl] = load_mnist_data.load_mnist_data(d, ss_big, st)
                for i in range(int(ss_big/k)):
                        data.append(np.linalg.qr(dta[:,i*k:(i+1)*(k)])[0])
                        labels_before.append(lbl[0])


        lbg_test_obj = gr_lbg.gr_lbg()

        #center initialization
        #lbg_test_obj.center_select = 'random'
        lbg_test_obj.center_select = 'troubleshoot' #initialize with properly labeled data points

        [centers,labels_after] = lbg_test_obj.fit(data,center_count = 3, median = do_median)


        # plot distortion change and confusion matrix and mds plot
        # gr_lbg.print_cluster_data(centers, labels_after, labels_before)
        # gr_lbg.embed_plot_results(data,centers,labels_before, mdn = do_median) 

        return centers


ss_big = 200
#gr(k,n), k<n and k must divide ss_big
k=5
#digits =[0,1,2,3,4,5,6,7,8,9]
digits =[3,5,6]
st = 'train'

centers_median = run_grlbg(True)
centers_mean = run_grlbg(False)


#have to tweak around a bit with the plot to line up centers
fig, axs = plt.subplots(2, k)
for kk in range(k):
        axs[0, kk].imshow(np.reshape(centers_median[2][:,kk],(28,28)))
        axs[1, kk].imshow(np.reshape(centers_mean[0][:,kk],(28,28)))

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


