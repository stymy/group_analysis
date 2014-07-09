import sys
import glob
import os
import nipype.interfaces.fsl as fsl
import pandas
import subprocess
import get_s3_paths
import concat

def do_it(pipeline, strategy, derivative):
  modelname = "ABIDE_dx_age_site_fiq_meanfd"

  csv_path = 'Phenotypic_V1_0b_preprocessed1.csv'
  csv_in = pandas.read_csv(csv_path)
  sub_pheno_list = get_s3_paths.get_subs(csv_in)

  if not os.path.exists('concat_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)):
      #----DOWNLOAD FILES----#
      download_root = 'DATA/'
      s3_prefix = 'https://s3.amazonaws.com/fcp-indi/data/Projects/ABIDE_Initiative/Outputs/' 
      path_list = get_s3_paths.get_paths(sub_pheno_list, pipeline, strategy, derivative, download_root)
      get_s3_paths.download(path_list, download_root, s3_prefix)

      print "\n----DOWNLOAD COMPLETE----\n"
      
      #----CONCATENATE TO 4D----#
      if derivative.startswith('dual_regression'):
        for brick in xrange(10):
          new_path_list = [path+'[%d]'%(brick) for path in path_list]
          concat.concat(pipeline, strategy, derivative, new_path_list, brick=str(brick))
      else:
        concat.concat(pipeline, strategy, derivative, path_list)

  #----RUN GLM-----#
  flameo = fsl.FLAMEO()
  flameo.inputs.cope_file = 'concat_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)
  flameo.inputs.design_file = modelname+'.mat'
  flameo.inputs.t_con_file = modelname+'.con'
  flameo.inputs.cov_split_file = modelname+'.grp'
  if derivative == 'vmhc':
    flameo.inputs.mask_file = 'vmhc_mask.nii'
  else:
    flameo.inputs.mask_file = 'automask.nii'
  flameo.inputs.log_dir = 'stats_%s_%s_%s' %(pipeline, strategy, derivative)
  flameo.inputs.run_mode = 'ols'
  if not os.path.exists(flameo.inputs.log_dir):
      res = flameo.run()
      "----GLM COMPLETE----"
  else:
      print "\n----FLAMEO DID NOT RUN. Folder exists. Delete it to recalculate GLM----\n"

  #----CORRECT FOR MULTIPLE COMPARISONS----#
  currentdir = os.getcwd()
  os.chdir(flameo.inputs.log_dir)
  zstat_files = glob.glob("zstat*.nii.gz")
  for i, zstat_file in enumerate(zstat_files):
    mask_file = "mask.nii.gz"
    z_threshold = "2.3"
    p_threshold = "0.05"
    underlay_img = os.path.join(currentdir, "std_3mm_brain.nii.gz")
    output_suffix = "corrected"+str(i+1)
    subprocess.call(["easythresh",  \
                     zstat_file,    \
                     mask_file,     \
                     z_threshold,   \
                     p_threshold,   \
                     underlay_img,  \
                     output_suffix])
  print "\n----CORRECTION COMPLETE----\n"
  os.chdir(currentdir)
  print "\n----GROUP ANALYSIS COMPLETE----\n"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "USAGE:\n \
        python group_analysis.py [pipeline] [strategy] [derivative]\n \
        EXAMPLE: python group_analysis.py cpac filt_noglobal vmhc\n"
    else:
        #----VARIABLES----#
        pipeline = sys.argv[1] #'cpac'
        strategy = sys.argv[2] #'filt_noglobal'
        derivative = sys.argv[3] #'vmhc'
        
        do_it(pipeline, strategy, derivative)
