import subprocess
import nipype.interfaces.afni as afni
import os

def do_it(pipeline, strategy, derivative):
    currentdir = os.getcwd()
    if not os.path.exists("images"):
        os.mkdir("images")
    if not os.path.exists(os.path.join(currentdir,'images/%s_%s_%s_saggital.png' %(pipeline, strategy, derivative))):
        stats_dir = os.path.join(currentdir,'stats_%s_%s_%s' %(pipeline, strategy, derivative))

        if not os.path.exists(stats_dir):
            print stats_dir+" does not exist"
            return_run_status = stats_dir
        else:
            os.chdir(stats_dir)
            
            thisdir = os.getcwd()
            if not os.path.exists('thresh_corrected_merged.nii.gz'):
                print os.path.exists('thresh_corrected1.nii.gz'), stats_dir
                #merge the positive and negative values
                merge = afni.Calc()
                merge.inputs.in_file_a = 'thresh_corrected1.nii.gz'
                merge.inputs.in_file_b = 'thresh_corrected2.nii.gz'
                merge.inputs.expr = "b-a"
                merge.inputs.out_file = 'thresh_corrected_merged.nii.gz'
                merge.inputs.args = "-overwrite"
                merge.outputtype = "NIFTI"
                print merge.cmdline
                res = merge.run()

            if not os.path.exists('zstat_merged.nii.gz'):
                merge2 = afni.Calc()
                merge2.inputs.in_file_a = 'zstat1.nii.gz'
                merge2.inputs.in_file_b = 'zstat2.nii.gz'
                merge2.inputs.expr = "b-a"
                merge2.inputs.out_file = 'zstat_merged.nii.gz'
                merge2.inputs.args = "-overwrite"
                merge2.outputtype = "NIFTI"
                print merge2.cmdline
                res2 = merge2.run()
                
                print "--MERGE DONE--"

            #make symbolic link to standard underlay image
            from_dir = os.path.join(currentdir,"MNI152_.5mm_masked_edged_tt.nii.gz")
            to_dir = os.path.join(thisdir, "MNI152_.5mm_masked_edged_tt.nii.gz")
            subprocess.call(["ln", "-s", from_dir, to_dir])
            print "--LINKED TO STANDARD--"

            # plot with afni driver
            in_file = os.path.realpath("thresh_corrected_merged.nii.gz")
            out_file = os.path.join(currentdir,"images/%s_%s_%s" %(pipeline, strategy, derivative))
            subprocess.call(["sh", \
                                 "../afni_plot.bash", \
                                 in_file, \
                                 out_file])

            os.chdir(currentdir)

if __name__ == "__main__":
    pipelines = ['niak','cpac','dparsf','ccs']
    strategies = ['filt_noglobal','filt_global','nofilt_global','nofilt_noglobal']
    derivatives = ['reho','degree_weighted','degree_binarize','eigenvector_weighted','lfcd','dual_regression0','dual_regression1','dual_regression2','dual_regression3','dual_regression4','dual_regression5','dual_regression6','dual_regression7','dual_regression8','dual_regression9','eigenvector_binarize', 'vmhc']#alff, falff, reho

    for pipeline in pipelines:
        for strategy in strategies:
            if not pipeline == "niak":
                 derivatives.append("alff")
                 derivatives.append("falff")
            for derivative in derivatives:
                do_it(pipeline, strategy, derivative)
