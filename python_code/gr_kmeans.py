import numpy as np
import distances
import random
import plots
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

'''
TODO:
Double check distortion metrics
Possibly add other distortion metric options?
documentation descriptions
Chordal vs. geodesic distances? (will smallest chordal be smallest geodesic?)
add type checks for input variables
epoch/iteration clarification
improve automatic plotting method
do i need to randomize order points are seen?


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


def embed_plot_results(data, centers, true_labels, eigplot=False):
    l = len(data)
    plot_data = data + centers
    pairwise_dist = distances.chordal_distance(plot_data, plot_data)
    embed_coords = distances.mds(pairwise_dist, eigplot=eigplot)
    plt.figure()
    for i in np.unique(true_labels):
        idx = np.where(true_labels == i)[0]
        plt.plot(embed_coords[idx, 0], embed_coords[idx, 1], 'o', label='Cluster %i' % i)
        plt.plot(embed_coords[l+i, 0], embed_coords[l+i, 1], 'o', markeredgecolor='k',
                 markersize=8, label='Center %i' % i)
    plt.legend()
    plt.title('Grassmann K-means Results')
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


class gr_kmeans:
    def __init__(self, center_select='data', eps=10e-6, verbosity=1):
        '''

        '''

        self.center_select = center_select
        self.eps = eps
        self.center_updates = []
        self.distortion_change = []
        self.label_change = []
        self.verbosity = verbosity

    def fit(self, data, true_labels=None, supervised=False, show_cluster_data=True, center_count=1,
            plot_results=False, eigplot=True, distortion_plot=True, numits=1):
        '''

        '''

        if not supervised:
            if self.center_select == 'data':
                centers = random.sample(data, center_count)
            elif self.center_select == 'random':
                centers = []
                for i in range(center_count):
                    centers.append(np.linalg.qr(np.random.rand(data.shape))[0])
            else:
                print("Invalid center selection option. Please choose 'data' or 'random'")
                return

            count = 0
            self.center_updates.append([centers])
            dist = distances.chordal_distance(centers, data)
            labels = np.argmin(dist, axis=0)  # should be MIN in each column
            self.label_change.append([labels])
            avg_dist = cluster_distortion(dist, labels, center_count)
            self.distortion_change.append(avg_dist)
            delta = 1
            n = np.zeros((1, center_count))[0]
            while count < numits and delta > self.eps:
                if self.verbosity > 1:
                    print('Begin epoch %i...' % (count+1))
                for i in range(len(data)):
                    self.center_updates.append([centers])
                    dist = distances.chordal_distance(centers, [data[i]])
                    label = np.argmin(dist, axis=0)[0]  # should be min in each column
                    self.label_change.append([label])
                    n[label] += 1
                    centers[label] = distances.geodesic(centers[label], data[i], 1/(n[label]))

                # Calculate distortion after a single epoch
                dist = distances.chordal_distance(centers, data)
                labels = np.argmin(dist, axis=0)
                avg_dist = cluster_distortion(dist, labels, center_count)
                delta = (self.distortion_change[-1]-avg_dist)/avg_dist
                self.distortion_change.append(avg_dist)
                count += 1
                if self.verbosity > 0:
                    print('Epoch %i cluster distortion: %.8f' % (count, avg_dist))
            # Calculate final post-iteration stuff
            print('Kmeans terminated after %i iterations \n' % count)
            self.center_updates.append([centers])
            dist = distances.chordal_distance(centers, data)
            labels = np.argmin(dist, axis=0)  # should be min in each column
            self.label_change.append([labels])
            avg_dist = cluster_distortion(dist, labels, center_count)
            self.distortion_change.append(avg_dist)
        else:
            pass  # no supervised version yet

        if plot_results:
            embed_plot_results(data, centers, labels, eigplot=eigplot)
        if show_cluster_data:
            print_cluster_data(centers, labels, true_labels)

        if distortion_plot:
            plt.figure()
            plt.plot(self.distortion_change)
            plt.xlabel('Iteration')
            plt.ylabel('Average distortion')
            plt.title('Distortion Change')

        return centers, labels

    def predict(self, test_data):
        pass
