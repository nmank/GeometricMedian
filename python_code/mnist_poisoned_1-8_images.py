import flag_mean
import flag_median
import load_mnist_data
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import mds
from sklearn.decomposition import PCA
import distances


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
k=1
#out_k is number of singular vectors (space for the median or the mean)
out_k = 5
#load the data
[data0,labels_before0] = load_data(k, ss_big, digits = [1])
[data1,labels_before1] = load_data(k, 50*9+1, digits = [8])
data = data0 + data1

medians = []
means = []
for i in range(20):
    #load the data  
    medians.append(flag_median.flag_median(data[:100+ 5*i],.000001,out_k))
    means.append(flag_mean.flag_mean(data[:100 + 5*i], r= out_k))

#plot first column
# data_1comp = np.vstack([d[:,0] for d in data])
# plot_data = np.vstack( [data_1comp, np.vstack([md[:,0] for md in medians]), np.vstack([mn[:,0] for mn in means])] )

#plot all data
plot_data = data + medians + means


for i in range(19):
    fig, axs = plt.subplots(2, out_k)
    for j in range(out_k):
        med_reshape = np.reshape(medians[i][:,j],(28,28))
        if med_reshape[0,0] < 0:
            axs[0, j].imshow(med_reshape)
        else:
            axs[0, j].imshow(-med_reshape)
        mean_reshape = np.reshape(means[i][:,j],(28,28))
        if mean_reshape[0,0] < 0:
            axs[1, j].imshow(mean_reshape)
        else:
            axs[1, j].imshow(-mean_reshape)
    axs[0, 0].set_ylabel('Median')
    axs[1, 0].set_ylabel('Mean') 
    for ax in axs:
        for a in ax:
            a.set_xticks([])
            a.set_yticks([])
    plt.suptitle(str(5*i) + ' eights')
            
    fig.tight_layout()
    plt.savefig('image_poison_1-8_'+str(i)+'.png')
    plt.close()


# 
# for kk in range(10):
#         
#         axs[1, kk].imshow(np.reshape(means[kk][:,0],(28,28)))

# #label the rows:
# axs[0, 0].set_ylabel('Median')
# axs[1, 0].set_ylabel('Mean')  

# # remove the x and y ticks

# plt.show()