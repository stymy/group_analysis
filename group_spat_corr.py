import numpy as np
import nibabel as nb
import subprocess
import group_analysis
import output_image
import os
import pandas
from scipy.stats import spearmanr
import npeet.entropy_estimators as ee

def do_it(X,Y,do_entropy=True):
    #pearsons
    corr = np.corrcoef(X,Y)[0,1]
    varx = np.var(X)
    vary = np.var(Y)
    cov = np.cov(X,Y)[0,1]
    meanx = np.mean(X)
    meany = np.mean(Y)

    #concordance
    conc = 2.*float(cov)/(float(varx)+float(vary)+np.square(float(meanx)-float(meany)))
    
    #spearman
    spearman=spearmanr(X,Y)[0]
                    
    #dice coefficient
    U = np.union1d(X,Y)
    dice = pandas.Series()
    for percent in xrange(100):
        threshold = np.percentile(abs(U),percent)
        x = abs(X)>threshold
        y = abs(Y)>threshold
        s = x*y
        xplusy = x.sum()+y.sum()
        if  xplusy == 0:
            die = -1
        else:
            die = 2.*s.sum()/xplusy
            dice[str(percent)+'_'+str(threshold)] = die

    if do_entropy:
        #entropy
        x = ee.vectorize(X)
        y = ee.vectorize(Y)
        mi = ee.mi(x,y)
        hx = -ee.entropy(x)
        hy = -ee.entropy(y)
        ecc= np.sqrt(mi/(0.5*(hx+hy)))
    else:
        ecc = np.nan

    return corr, conc, spearman, dice, ecc

if __name__ == "__main__":

    pipelines = ['cpac']
    strategies = ['filt_noglobal','filt_global', 'nofilt_global','nofilt_noglobal']
    derivatives = ['reho', 'alff','degree_weighted','degree_binarize','eigenvector_weighted','lfcd', 'falff']# 'eigenvector_binarize', vmhc

    derivs = pandas.Series()

    for derivative in derivatives:

        corrs = pandas.DataFrame()
        concs = pandas.DataFrame()
        spearmans = pandas.DataFrame()
        entropies = pandas.DataFrame()
        dices = pandas.DataFrame()

        for pipeline in pipelines:
            for strategy in strategies:

                #THIS MAKES SURE THAT DATA IS THERE, \
                #IF NOT, RUNS CORRESPONDING THE GROUP ANALYSIS SCRIPT
                if not os.path.exists('stats_%s_%s_%s' %(pipeline, strategy, derivative)):
                    group_analysis.do_it(pipeline, strategy, derivative)

                if not os.path.exists('stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline, strategy, derivative)):
                    output_image.do_it(pipeline, strategy, derivative)

                #NOW compare between pipelines/strategies
                in_file = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline, strategy, derivative)

                for pipeline2 in pipelines:
                    for strategy2 in strategies:
                        in_file_2 = 'stats_%s_%s_%s/thresh_corrected_merged.nii.gz' %(pipeline2, strategy2, derivative)
                        if not os.path.exists(in_file_2):
                            group_analysis.do_it(pipeline2, strategy2, derivative)

                        mask_file = 'stats_%s_%s_%s/mask.nii.gz' %(pipeline, strategy, derivative)
                        # make a spatial correlation matrix
                        print '%s_%s_%s_v_%s_%s_%s' %(pipeline, strategy, derivative, pipeline2, strategy2, derivative)

                        if not in_file == in_file_2:
                            X = nb.load(in_file).get_data().flatten()
                            Y = nb.load(in_file_2).get_data().flatten()
                            corr, conc, spearman, dice, ecc =  do_it(X,Y)
                            corrs.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, corr)
                            concs.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, conc)
                            spearmans.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, spearman)
                            dices[pipeline+'_'+strategy+'_V_'+pipeline2+'_'+strategy2] = dice.values
                            entropies.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, ecc)

        #SAVE TO SERIES 
        print derivative
        correlations = pandas.Series([corrs, concs, spearmans, entropies, dices], \
        index=['pearson','concordance','spearmans','entropy','dice'],name=derivative)
        
        derivs[derivative] = correlations
        derivs.to_pickle('spat_corr_dataframes')
    
    #TO ANALYZE, LOAD LIKE THIS:
    #a = pandas.read_pickle('/home/ubuntu/spat_corr_dataframes')
    #a.falff.pearson.cpac_filt_global.cpac_nofilt_global
