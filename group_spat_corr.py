import itertools as it
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
    for percent in [100,50,25,10,5,1]:
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
    derivatives = ['reho', 'alff','degree_weighted','degree_binarize','eigenvector_weighted','lfcd', 'falff', 'eigenvector_binarize']#, 'dual_regression']

    derivs = pandas.Series()

    for derivative in derivatives:

        corrs = pandas.DataFrame()
        concs = pandas.DataFrame()
        spearmans = pandas.DataFrame()
        entropies = pandas.DataFrame()
        dices = pandas.DataFrame()

        for pipeline, pipeline2 in it.combinations_with_replacement(pipelines,2):
            for strategy, strategy2 in it.combinations(strategies,2):
                in_file = 'stats_%s_%s_%s/zstat_merged.nii.gz' %(pipeline, strategy, derivative)
                in_file_2 = 'stats_%s_%s_%s/zstat_merged.nii.gz' %(pipeline2, strategy2, derivative)
                #THIS MAKES SURE THAT DATA IS THERE, \
                #IF NOT, RUNS CORRESPONDING THE GROUP ANALYSIS SCRIPT
                if not os.path.exists('stats_%s_%s_%s' %(pipeline, strategy, derivative)):
                    group_analysis.do_it(pipeline, strategy, derivative)
                if not os.path.exists('stats_%s_%s_%s' %(pipeline2, strategy2, derivative)):
                    group_analysis.do_it(pipeline2, strategy2, derivative)
                if not os.path.exists(in_file):
                    output_image.do_it(pipeline, strategy, derivative)
                if not os.path.exists(in_file_2):
                    output_image.do_it(pipeline2, strategy2, derivative)

                # make a spatial correlation matrix
                print '%s_%s_%s_v_%s_%s_%s' %(pipeline, strategy, derivative, pipeline2, strategy2, derivative)

                if (pipeline == pipeline2 and strategy != strategy2) or (pipeline!=pipeline2 and strategy == strategy2):
                    X = nb.load(in_file).get_data().flatten()
                    Y = nb.load(in_file_2).get_data().flatten()
                    corr, conc, spearman, dice, ecc =  do_it(X,Y)
                    corrs.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, corr)
                    corrs.set_value(pipeline2+'_'+strategy2, pipeline+'_'+strategy, corr)
                    concs.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, conc)
                    concs.set_value(pipeline2+'_'+strategy2, pipeline+'_'+strategy, conc)
                    spearmans.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, spearman)
                    spearmans.set_value(pipeline2+'_'+strategy2, pipeline+'_'+strategy, spearman)                  
                    dices[pipeline+'_'+strategy+'_v_'+pipeline2+'_'+strategy2] = dice.values
                    dices[pipeline2+'_'+strategy2+'_v_'+pipeline+'_'+strategy] = dice.values
                    entropies.set_value(pipeline+'_'+strategy, pipeline2+'_'+strategy2, ecc)
                    entropies.set_value(pipeline2+'_'+strategy2, pipeline+'_'+strategy, ecc)

        #SAVE TO SERIES 
        print derivative
        correlations = pandas.Series([corrs, concs, spearmans, entropies, dices], \
        index=['pearson','concordance','spearmans','entropy','dice'],name=derivative)
        
        derivs[derivative] = correlations
        derivs.to_pickle('spat_corr_dataframes')
    
    #TO ANALYZE, LOAD LIKE THIS:
    #a = pandas.read_pickle('/home/ubuntu/spat_corr_dataframes')
    #a.falff.pearson.cpac_filt_global.cpac_nofilt_global
    #for i, deriv in enumerate(derivs):
      #print derivs.index[i]              
      #print deriv
      #for j, corr in enumerate(deriv):
      #corr.to_csv("spat_corr_%s_%s.csv"%(derivs.index[i], derivs.index[j]))
