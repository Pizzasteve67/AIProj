# -*- coding: utf-8 -*-
"""
@author: cheri
Modified from ThomasLech/CROHME_extractor/visualize.py
Changes: 
    arguments (added pickle_path & output_path, removed box_size), 
    removed need for classes.txt, 
    removed reshaping and decoding since pickle data is now reshaped and decoded
    
Use like:
    !python visualise.py -n 40 -c 8 -p /content/drive/MyDrive/Output/ -o /content/drive/MyDrive/Output
"""

import os
import argparse
import pickle
import math
import random
# Data visualization
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument('-n', '--n_samples', required=True, help="Specify the nubmer of samples to show.")
ap.add_argument('-c', '--columns', required=True, help="Specify the nubmer of columns.")
ap.add_argument('-p', '--pickle_path', required=True, help="Specify the pickle path. eg./content/drive/MyDrive/Output")
ap.add_argument('-o', '--output_path', required=True, help="Specify the output path after extract. eg./content/drive/MyDrive/Output/")
args = vars(ap.parse_args())

pickle_path = os.path.normpath(args.get('pickle_path'))
outputs_rel_path = os.path.normpath(args.get('output_path'))

# Load pickled data
with open(os.path.join(pickle_path, 'train.pickle'), 'rb') as train:
    print('Restoring training set ...')
    train_set = pickle.load(train)

with open(os.path.join(pickle_path, 'test.pickle'), 'rb') as test:
    print('Restoring test set ...')
    test_set = pickle.load(test)

# Extract command-line arguments
n_samples = int(args.get('n_samples'))
n_cols = int(args.get('columns'))

'Compute number of rows with respect to number of both columns and samples provided by user'
rows_numb = math.ceil(n_samples / n_cols)

'Instanciate a figure to plot samples on'
figure, axis_arr = plt.subplots(rows_numb, n_cols, figsize=(12, 4))
figure.patch.set_facecolor((0.91, 0.91, 0.91))


sample_id = 0
for row in range(rows_numb):
    for col in range(n_cols):

        if sample_id < n_samples:
            'Generate random sample id'
            random_id = random.randint(0, len(test_set))
            training_sample = test_set[random_id]

            axis_arr[row, col].imshow(training_sample['features'], cmap='gray')
            axis_arr[row, col].set_title('\"' + training_sample['label'] + '\"', size=13, y=1.2)
            # axis_arr[row, col].set_title('Class: \"' + training_sample['label'] + '\"', size=13, y=1.2)

        'Remove explicit axises'
        axis_arr[row, col].axis('off')

        sample_id += 1

'Adjust spacing between subplots and window border'
figure.subplots_adjust(hspace=1.4, wspace=0.2)
plt.savefig(os.path.join(outputs_rel_path, 'visualization.png'))
# Brings foreground
plt.show()