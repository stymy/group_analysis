# Import packages
import sys
import os
import pandas
import urllib
import numpy as np

# --- Download from the S3 bucket based on phenotypic conditions ---

def get_subs(csv_in):
    sub_pheno_list = []
    # Iterate through the csv rows (subjects)
    for r in xrange(len(csv_in)):
        site = csv_in['SITE_ID'][r]
        sub_id = csv_in['SUB_ID'][r]
        file_id = csv_in['FILE_ID'][r]
        sex = csv_in['SEX'][r]
        age = csv_in['AGE_AT_SCAN'][r]
        mfd = csv_in['func_mean_fd'][r]
        dimartino = csv_in['SUB_IN_SMP'][r]
        # Test phenotypic conditions
        if (file_id != 'no_filename' and not np.isnan(mfd) and dimartino == 1):
            sub_pheno_list.append(file_id)
            
    # Strip out 'no_filename's from list
    # sub_pheno_list = [s for s in sub_pheno_list if s != 'no_filename']
    return sub_pheno_list

def get_paths(sub_pheno_list, pipeline, strategy, derivative, download_root):
    # Fetch s3 path for each file_id that met the phenotypic conditions
    path_list = []
    for file_id in sub_pheno_list:
        file_path = pipeline + '/' + strategy + '/' + derivative + \
                    '/' + file_id + '_' + derivative + '.nii.gz'
        path_list.append(os.path.join(download_root, file_path))

    # Print list of paths one can wget to download
    #print path_list
    return path_list

def download(path_list, download_root, s3_prefix):
    # And download the items
    for path in path_list:
        download_dir = os.path.dirname(path)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        if not os.path.exists(path):
            s3_path = os.path.join(s3_prefix,path.lstrip(download_root))
            print('Retrieving: ' + path)
            urllib.urlretrieve(s3_path, path)

if __name__ == "__main__":
    # Path to phenotypic csv file
    csv_path = 'Phenotypic_V1_0b_preprocessed1.csv'
    # Download directory
    download_root = 'DATA/'
    # S3 path prefixn
    s3_prefix = 'https://s3.amazonaws.com/fcp-indi/data/Projects/'\
                'ABIDE_Initiative/Outputs/'

    # Read in phenotypic file csv
    csv_in = pandas.read_csv(csv_path)
    # Get relevant subjects
    sub_pheno_list = get_subs(csv_in)
    
    if len(sys.argv) < 4:
    # Choose pipeline, strategy, and derivative of interest
        pipeline = 'cpac'
        strategy = 'filt_global'
        derivative = 'reho'
    
    else:
        pipeline = sys.argv[1] #'cpac'
        strategy = sys.argv[2] #'filt_noglobal'
        derivative = sys.argv[3] #'vmhc'

    # Download to specified file structure
    path_list = get_paths(sub_pheno_list, pipeline, strategy, derivative, download_root)
    download(path_list, download_root, s3_prefix)
