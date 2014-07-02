import os
import nibabel as nb
import numpy as np

pipelines = ['cpac']
strategies = ['filt_global','filt_noglobal']
derivatives = ['reho']

#testing
strategy = strategies[0]
strategy2 = strategies[1]
pipeline = pipelines[0]
pipeline2 = pipelines[0]
derivative = derivatives[0]

in_file = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline, strategy, derivative)
in_file_2 = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline2, strategy2, derivative)

output_dir = '/home/ubuntu/bootstraps_%s_%s_%s_v_%s_%s_%s' %(pipeline, strategy, derivative, pipeline2, strategy2, derivative)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

X = nb.load(in_file).get_data().flatten()
Y = nb.load(in_file_2).get_data().flatten()

if len(X) != len(Y):
    "WARNING arrays are different lengths, will use the length of %s to shuffle" %(in_file)

scrambling_mat = np.random.permutation(len(X))

newX = X[scrambling_mat]
newY = Y[scrambling_mat]
