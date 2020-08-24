import numpy as np
import flag_mean
import flag_median
import random
import distances
import plots
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd


'''
TODO:
Double check distortion metrics
Possibly add other distortion metric options?
documentation descriptions
plot method
eventually want to be able to repeat multiple times on clusters for different classes (supervised bit)
options to toggle mds eigenvalue plot
add type checks for input variables
improve automatic plot method
add check for none true labels when cluster data true
verbosity options
heatmap should really be its own file


Change log:
added method for printing confusion matrix type display of centers
added option for passing true labels to fit
added option to select supervised or unsupervised clustering
import heatmap code
removed class attributes for labels, centers - temp fix for the center issue, returned instead
numits no longer a class attribute
plot results, plot center data are now static methods
'''


def cluster_distortion(dist, labels, center_count):
    cluster_dist = []
    for i in range(center_count):
        idx = (labels == i).nonzero()
        cluster_dist.append(dist[i, idx].mean())
    return np.mean(cluster_dist)


def embed_plot_results(data, centers, true_labels, eigplot = False, mdn = False):
    l = len(data)
    plot_data = data + centers
    pairwise_dist = distances.chordal_distance(plot_data, plot_data, mdn)
    embed_coords = distances.mds(pairwise_dist, eigplot=eigplot)
    plt.figure()
    ii=0
    for i in np.unique(true_labels):
        idx = np.where(true_labels == i)[0]
        plt.plot(embed_coords[idx, 0], embed_coords[idx, 1], 'o', label='Cluster %i' % i)
        plt.plot(embed_coords[l+ii, 0], embed_coords[l+ii, 1], 'o', markeredgecolor='k', markersize=8, label='Center %i' % ii)
        ii += 1
    plt.legend()
    plt.title('Grassmann LBG Results')
    plt.show()


def print_cluster_data(centers, labels, true_labels):
    row = len(centers)
    center_labels = []
    for i in range(row):
        center_labels.append('Center %i' % i)
    col = len(np.unique(true_labels))
    class_labels = []
    for i in range(col):
        class_labels.append('Class %i' % np.unique(true_labels)[i])

    centermap = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            idx1 = np.where(labels == i)[0]
            idx2 = np.where(true_labels == np.unique(true_labels)[j])[0]
            idx = np.intersect1d(idx1, idx2)
            centermap[i, j] = len(idx)
    # Plot the heatmap
    fig, ax = plt.subplots()
    im = plots.heatmap(centermap, center_labels, class_labels, ax=ax)
    texts = plots.annotate_heatmap(im, valfmt="{x: .0f}")

    fig.tight_layout()
    plt.show()


class gr_lbg:
    def __init__(self, center_select='data', eps=10e-12, numits=10, verbosity=1):
        self.center_select = center_select
        self.eps = eps
        self.center_updates = []
        self.distortion_change = []
        self.label_change = []
        self.verbosity = verbosity

    def fit(self, data, true_labels=None, supervised=False, show_cluster_data=False, center_count=1,
            plot_results=False, eigplot=True, distortion_plot=True, numits=10, median = True, l_vec_dims = 5, plot_svals = False):

        if not supervised:
            if self.center_select == 'data':
                centers = []
                for i in np.random.choice(len(data),center_count):
                     centers.append(data[i])
                #centers = np.random.sample(data, center_count)
            elif self.center_select == 'random':
                centers = []
                for i in range(center_count):
                    centers.append(np.linalg.qr(np.random.rand(data[0].shape[0],l_vec_dims))[0])
            elif self.center_select == 'troubleshoot':
                centers = []
                centers.append(data[0])
                centers.append(data[1])
                centers.append(data[2])
            else:
                print("Invalid center selection option. Please choose 'data' or 'random'")
                return
            count = 0
            self.center_updates.append([centers])
            dist = distances.chordal_distance(centers, data, median)
            labels = np.argmin(dist, axis=0)  # should be MIN in each column
            self.label_change.append([labels])
            avg_dist = cluster_distortion(dist, labels, center_count)
            self.distortion_change.append(avg_dist)
            delta = 1
            while count < numits and delta > self.eps:
                #  Recalculate centers
                centers = []
                for i in range(center_count):
                    idx = (labels == i).nonzero()[0]
                    cluster_subset = []
                    for q in range(len(idx)):
                        cluster_subset.append(data[idx[q]])
                    if len(cluster_subset) == 1:
                        centers.append(cluster_subset)
                    else:
                        if median == True:
                            centers.append(flag_median.flag_median(cluster_subset,.00001,r=l_vec_dims)) #medians
                        else:
                            centers.append(flag_mean.flag_mean(cluster_subset,r=l_vec_dims)) #means
                count += 1
                self.center_updates.append([centers])
                dist = distances.chordal_distance(centers, data, median)
                labels = np.argmin(dist, axis=0)  # should be min in each column
                self.label_change.append([labels])
                avg_dist = cluster_distortion(dist, labels, center_count)
                if self.verbosity > 0:
                    print('Iteration %i cluster distortion: %.8f' % (count, avg_dist))
                delta = np.abs(self.distortion_change[-1]-avg_dist)/avg_dist
                self.distortion_change.append(avg_dist)
            # Calculate final post-iteration stuff
            print('LBG terminated after %i iterations \n' % count)
            #plot singular values
            #fix this for more complex examples
            if plot_svals:
                S = []
                fig, axs = plt.subplots(1, 3)
                for i in range(center_count):
                    idx = (labels == i).nonzero()[0]
                    cluster_subset = []
                    for q in range(len(idx)):
                        cluster_subset.append(data[idx[q]])
                    if median == True:
                        S.append(flag_median.flag_median(cluster_subset,.00001, r=l_vec_dims, s_vals = True)) #medians
                    else:
                        S.append(flag_mean.flag_mean(cluster_subset,r=l_vec_dims, s_vals = True))
                

        else:
            pass  # gotta add supervised version later

        if plot_results:
            embed_plot_results(data, centers, labels, eigplot=eigplot)
        if show_cluster_data:
            #you need to define true labels before using this
            print_cluster_data(centers, labels, true_labels)

        if distortion_plot:
            plt.figure()
            plt.plot(self.distortion_change)
            plt.xlabel('Iteration')
            plt.ylabel('Average distortion')
            plt.title('Distortion Change')

        if plot_svals:
            return centers, labels, S
        else:
            return centers, labels

    def predict(self, test_data):
        pass
