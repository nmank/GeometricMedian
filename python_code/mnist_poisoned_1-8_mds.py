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
out_k = 1
#load the data
[data0,labels_before0] = load_data(k, ss_big, digits = [1])
[data1,labels_before1] = load_data(k, 50*9+1, digits = [8])
data = data0 + data1

medians = []
means = []
for i in range(20):
    #load the data  
    medians.append(flag_median.flag_median(data[:100+ 5*i],.000001,k))
    means.append(flag_mean.flag_mean(data[:100 + 5*i]))

#plot first column
# data_1comp = np.vstack([d[:,0] for d in data])
# plot_data = np.vstack( [data_1comp, np.vstack([md[:,0] for md in medians]), np.vstack([mn[:,0] for mn in means])] )


#plot all data



#Using sklearn mds
# embedding = mds.MDS(n_components=2) 
# data_transformed = embedding.fit_transform(plot_data)

#Using sklearn PCA
# embedding = PCA(n_components=2) 
# data_transformed = embedding.fit_transform(plot_data)

#Using distances.mds


for i in range(9):
    plot_data = data[:100 + 5*i] + [medians[i]] + [means[i]]
    pairwise_dist = distances.chordal_distance(plot_data, plot_data, True)
    data_transformed = distances.mds(pairwise_dist)
    plt.scatter(data_transformed[:100,0], data_transformed[:100,1], label = '1')
    plt.scatter(data_transformed[100:100 + 5*i,0], data_transformed[100: 100 + 5*i,1], label = '8')
    plt.scatter(data_transformed[-2,0], data_transformed[-2,1], marker = 'o', c = 'r', label = 'median')
    plt.scatter(data_transformed[-1,0], data_transformed[-1,1], marker = 'o', c= 'k', label = 'mean')
    plt.legend()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.savefig('1mds_poison_1-8_'+str(i)+'.png')
    plt.close()


# fig, axs = plt.subplots(2, 10)
# for kk in range(10):
#         axs[0, kk].imshow(np.reshape(medians[kk][:,0],(28,28)))
#         axs[1, kk].imshow(np.reshape(means[kk][:,0],(28,28)))

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
