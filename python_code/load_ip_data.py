import numpy as np

'''
Need to add option to specify by class name, also return class name
'''


def load_ip_data(classes, sample_size = 50, fix=True):
    labels = np.loadtxt('../IndianPines/IP_labels.csv', delimiter=',')

    class_names = {0: 'None', 1: 'Alfalfa', 2: 'Corn-notill', 3: 'Corn-mintill', 4: 'Corn', 5: 'Grass-pasture',
                   6: 'Grass-trees', 7: 'Grass-pasture-mowed', 8: 'Hay-windrowed', 9: 'Oats', 10: 'Soybean-notill',
                   11: 'Soybean-mintill', 12: 'Soybean-clean', 13: 'Wheat', 14: 'Woods',
                   15: 'Buildings-Grass-Trees-Drives', 16: 'Stone-Steel-Towers'}

    if fix:
        data = np.loadtxt('../IndianPines/IP_data_fix.csv', delimiter=',')
    else:
        data = np.loadtxt('../IndianPines/IP_data_raw.csv', delimiter=',')
    if type(classes) == int:
        classes = [classes]

    if type(sample_size) == int:
        sample_size = [sample_size]*len(classes)

    if len(sample_size) != len(classes):
        print('Incorrect number of sample sizes given.')
        return [], []

    return_data = []
    return_labels = []

    for i in range(len(classes)):
        cl = classes[i]
        size = sample_size[i]
        print('Class %i name: %s' % (cl, class_names[cl]))
        idx = np.where(labels == cl)[0]
        if idx.shape[0] < size:
            print('Sample number for class %i reduced to %i' % (cl, len(idx)))
            return_data.append(data[:, idx])
            return_labels.append(labels[idx])
        else:
            subidx = np.random.choice(idx, size)
            return_data.append(data[:, subidx])
            return_labels.append(labels[subidx])

    datamat = return_data[0]
    datamat_labels = return_labels[0]

    if len(classes) > 1:
        for i in range(1, len(classes)):
            datamat = np.hstack((datamat, return_data[i]))
            datamat_labels = np.hstack((datamat_labels, return_labels[i]))

    return datamat, datamat_labels
