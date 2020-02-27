import numpy as np


def make_subspaces(data, labels, dim=5, verbosity=0):
    '''
    '''

    classes = np.unique(labels)
    subspaces = []
    sub_lbls = []
    for i in classes:
        idx = np.where(labels == i)[0]
        cl_data = data[:, idx]
        subspace_count = len(idx) // dim
        unused_count = len(idx) % dim

        if verbosity > 0:
            print('Class %i contains %i subspaces, with % i point(s) omitted' % (i, subspace_count, unused_count))

        for j in range(subspace_count):
            subspaces.append(np.linalg.qr(cl_data[:, j*dim:j*dim+dim])[0])
            sub_lbls.append(i)

    return subspaces, sub_lbls
