import nipype.interfaces.afni as afni
from get_s3_paths import get_subs, get_paths
import pandas
import os

def concat(pipeline, strategy, derivative, path_list, subbrick=""):
    out_file = 'concat_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative+subbrick)
    
    if not os.path.exists(out_file):
        tcat = afni.TCat()
        tcat.inputs.in_files = path_list
        tcat.inputs.out_file = out_file
        res = tcat.run()
    else:
        print "%s already exists. Delete to rewrite" % out_file

if __name__ == "__main__":
    # Choose pipeline, strategy, and derivative of interest
    pipeline = 'cpac'
    strategy = 'filt_noglobal'
    derivative = 'dual_regression'

    # Path to phenotypic csv file
    csv_path = 'Phenotypic_V1_0b_preprocessed1.csv'

    #Read in phenotypic file csv
    csv_in = pandas.read_csv(csv_path)
    # Get relevant subjects
    sub_pheno_list = get_subs(csv_in)

    # Get file list
    path_list = get_paths(sub_pheno_list, pipeline, strategy, derivative, 'DATA/')

    concat(pipeline, strategy, derivative, path_list)
