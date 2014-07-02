import pandas
import os
import nibabel as nb
import numpy as np
import itertools as it
from group_spat_corr import do_it as correlate

correlations = pandas.DataFrame()

pipelines = ['cpac']
strategies = ['filt_global','filt_noglobal', 'nofilt_global', 'nofilt_noglobal']
derivatives = ['reho','alff']

for derivative in derivatives:
    for pipeline, pipeline2 in it.combinations_with_replacement(pipelines,2):
        for strategy, strategy2 in it.combinations(strategies,2):
            #PRINT PROGRESS
            print "%s: %s %s VERSUS %s %s" %(derivative, pipeline, strategy, pipeline2, strategy2)

            #LOAD ORIGINAL FILES
            in_file = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline, strategy, derivative)
            in_file_2 = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline2, strategy2, derivative)

            X = nb.load(in_file).get_data().flatten()
            Y = nb.load(in_file_2).get_data().flatten()

            if len(X) != len(Y):
                "WARNING arrays are different lengths, will use the length of %s to shuffle" %(in_file)

            #OUTPUT DIR
            output_dir = 'bootstraps_%s_%s_v_%s_%s' %(pipeline, strategy, pipeline2, strategy2)
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

            #PRINT MEANS
            print correlations.mean()

            correlations.to_pickle(os.path.join(output_dir,'boot_%s.pd'%(derivative)))
