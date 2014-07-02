import pandas
import os
import nibabel as nb
import numpy as np
from group_spat_corr import do_it as correlate

correlations = pandas.DataFrame()

pipelines = ['cpac']
strategies = ['filt_global','filt_noglobal']
derivatives = ['reho']

#testing
strategy = strategies[0]
strategy2 = strategies[1]
pipeline = pipelines[0]
pipeline2 = pipelines[0]
derivative = derivatives[0]

#outputs
corrs = pandas.DataFrame()
concs = pandas.DataFrame()
spearmans = pandas.DataFrame()
entropies = pandas.DataFrame()
dices = pandas.DataFrame()


#LOAD ORIGINAL FILES
in_file = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline, strategy, derivative)
in_file_2 = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline2, strategy2, derivative)

X = nb.load(in_file).get_data().flatten()
Y = nb.load(in_file_2).get_data().flatten()

if len(X) != len(Y):
    "WARNING arrays are different lengths, will use the length of %s to shuffle" %(in_file)

#OUTPUT DIR
output_dir = 'bootstraps_%s_%s_%s_v_%s_%s_%s' %(pipeline, strategy, derivative, pipeline2, strategy2, derivative)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

iterations = 10
#MAKE PERMUTATIONS
for i in xrange(iterations):
    index = "iter"+str(i)

    scrambling_mat = np.random.permutation(len(X))

    newX = X[scrambling_mat]
    newY = Y[scrambling_mat]

    #CORRELATE
    corr, conc, spear, dice, ecc =  correlate(newX,newY,do_entropy=False)
    correlations.set_value(index,'pearson',corr)
    correlations.set_value(index,'concordance',conc)
    correlations.set_value(index,'spearman',spear)
    correlations.set_value(index,'dice',dice[0])
    correlations.set_value(index,'ecc',ecc)

    #SAVE
    np.save(os.path.join(output_dir,'strap_%s'%(index)), scrambling_mat)

correlations.to_pickle(os.path.join(output_dir,'spat_correlations_%s.pd'%(iterations)))
