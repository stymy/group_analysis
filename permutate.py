import pandas
import os
import nibabel as nb
import numpy as np
import itertools as it
from group_spat_corr import do_it as correlate

pipelines = ['cpac']
strategies = ['filt_noglobal','filt_global', 'nofilt_global','nofilt_noglobal']
derivatives = ['reho', 'alff','degree_weighted','degree_binarize','eigenvector_weighted','lfcd', 'falff', 'eigenvector_binarize', 'vmhc']

for derivative in derivatives:
    for pipeline, pipeline2 in it.combinations_with_replacement(pipelines,2):
        for strategy, strategy2 in it.combinations(strategies,2):

            correlations = pandas.DataFrame()

            #PRINT PROGRESS
            if (pipeline == pipeline2 and strategy != strategy2) or (pipeline!=pipeline2 and strategy == strategy2):
                print "%s: %s %s VERSUS %s %s" %(derivative, pipeline, strategy, pipeline2, strategy2)

                #LOAD ORIGINAL FILES
                in_file = 'stats_%s_%s_%s/zstat_merged.nii.gz' %(pipeline, strategy, derivative)
                in_file_2 = 'stats_%s_%s_%s/zstat_merged.nii.gz' %(pipeline2, strategy2, derivative)

                X = nb.load(in_file).get_data().flatten()
                Y = nb.load(in_file_2).get_data().flatten()

                if len(X) != len(Y):
                    "WARNING arrays are different lengths, will use the length of %s to shuffle" %(in_file)

                #OUTPUT DIR
                output_dir = 'nullstraps_%s_%s_v_%s_%s' %(pipeline, strategy, pipeline2, strategy2)
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)

                iterations = 10
                #MAKE PERMUTES
                for i in xrange(iterations):
                    index = "iter"+str(i)

                    newX = np.random.choice(X,size=(X.shape),replace=False)
                    newY = Y


                    #CORRELATE
                    corr, conc, spear, dice, ecc =  correlate(newX,newY)
                    correlations.set_value(index,'pearson',corr)
                    correlations.set_value(index,'concordance',conc)
                    correlations.set_value(index,'spearman',spear)
                    correlations.set_value(index,'dice',dice[1])
                    correlations.set_value(index,'ecc',ecc)

                #PRINT MEANS
                print correlations.mean()

                correlations.to_pickle(os.path.join(output_dir,'null_%s.pd'%(derivative)))
