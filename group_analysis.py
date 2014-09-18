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
      orig_derivative = derivative
      if derivative.startswith('dual_regression'):
        derivative = 'dual_regression'
      path_list = get_s3_paths.get_paths(sub_pheno_list, pipeline, strategy, derivative, download_root)
      get_s3_paths.download(path_list, download_root, s3_prefix)
      derivative = orig_derivative

      print "\n----DOWNLOAD COMPLETE----\n"

      #----CONCATENATE TO 4D----#
      if derivative.startswith('dual_regression'):
        for brick in xrange(10):
          new_path_list = [path+'[%s]'%(str(brick)) for path in path_list]
          concat.concat(pipeline, strategy, derivative, new_path_list, brick=str(brick))
      else:
        concat.concat(pipeline, strategy, derivative, path_list)

  #----MAKE MASK----#
  mask_file = 'mask_dparsf.nii' #standard
  #for individual masks
  #if not os.path.exists('mask_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)):
  #download fun_mask from s3 and get 80-90% mask.
  #   print "MASKING..."
  #   masker = fsl.maths.MathsCommand()
  #   masker.inputs.in_file = 'concat_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)
  #   masker.inputs.args = '-abs -Tmin -bin'
  #   masker.inputs.output_type = 'NIFTI_GZ'
  #   masker.inputs.out_file = 'mask_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)
  #   res = masker.run()
  #   mask_file = masker.inputs.out_file
  print "\n----MASKING COMPLETE----\n"

  #----RUN GLM-----#
  flameo = fsl.FLAMEO()
  flameo.inputs.cope_file = 'concat_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)
  flameo.inputs.design_file = modelname+'.mat'
  flameo.inputs.t_con_file = modelname+'.con'
  flameo.inputs.cov_split_file = modelname+'.grp'
  # flameo.inputs.mask_file = 'mask_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)
  flameo.inputs.mask_file = mask_file
  flameo.inputs.log_dir = 'stats_%s_%s_%s' %(pipeline, strategy, derivative)
  flameo.inputs.run_mode = 'ols'
  if not os.path.exists(flameo.inputs.log_dir):
    res = flameo.run()
    print "----GLM COMPLETE----"
  else:
    print "\n----FLAMEO DID NOT RUN. Folder exists. Delete it to recalculate GLM----\n"

  #----CORRECT FOR MULTIPLE COMPARISONS----#
  currentdir = os.getcwd()
  os.chdir(flameo.inputs.log_dir)
  if not os.path.exists("threshcorrected1.nii.gz"):
      zstat_files = glob.glob("zstat*.nii.gz")
      for i, zstat_file in enumerate(zstat_files):
        mask_file = ../mask_dparsf.nii #'../mask_%s_%s_%s.nii.gz' %(pipeline, strategy, derivative)
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

  print "USAGE:\n \
  python group_analysis.py [pipeline] [strategy] [derivative]\n \
  EXAMPLE: python group_analysis.py cpac filt_noglobal vmhc\n"

  derivatives = ['reho','degree_weighted','degree_binarize','eigenvector_weighted','lfcd', 'dual_regression0','dual_regression1','dual_regression2','dual_regression3','dual_regression4','dual_regression5','dual_regression6','dual_regression7','dual_regression8','dual_regression9','eigenvector_binarize', 'vmhc']#'alff', 'falff']
  
    if len(sys.argv) == 2:
        #----VARIABLES----#
        pipeline = sys.argv[1]
        strategies = ['filt_noglobal','filt_global', 'nofilt_global','nofilt_noglobal']
  
        if not pipeline == "niak":
          derivatives.append('alff')
          derivatives.append('falff')
        for strategy in strategies:
          for derivative in derivatives:
            do_it(pipeline, strategy, derivative)

    if len(sys.argv) == 3:
        #----VARIABLES----#
        pipeline = sys.argv[1]
        strategy = sys.argv[2]

        if not pipeline == "niak":
          derivatives.append('alff')
          derivatives.append('falff')

        for derivative in derivatives:
          do_it(pipeline, strategy, derivative)
    else:
        #----VARIABLES----#
        pipeline = sys.argv[1] #'cpac'
        strategy = sys.argv[2] #'filt_noglobal'
        derivative = sys.argv[3] #'vmhc'
        
        do_it(pipeline, strategy, derivative)
