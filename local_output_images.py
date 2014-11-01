import subprocess
import os

def do_it(pipeline, strategy, derivative):
    currentdir = os.getcwd()

    os.chdir("../")
    workingdir = os.getcwd()

    if not os.path.exists("images"):
        os.mkdir("images")
    if not os.path.exists('images/%s_%s_%s_saggital.png' %(pipeline, strategy, derivative)):
        data_dir = os.path.realpath('data')

        #make symbolic link to standard underlay image
        from_dir = os.path.join(currentdir,"MNI152_.5mm_masked_edged_tt.nii.gz")
        to_dir = os.path.join(workingdir, "MNI152_.5mm_masked_edged_tt.nii.gz")
        subprocess.call(["ln", "-s", from_dir, to_dir])
        print "--LINKED TO STANDARD--"

        standard = os.path.join(currentdir,"MNI152_.5mm_masked_edged_tt.nii.gz")

        # plot with afni driver
        in_file = os.path.join(data_dir,"%s_%s_%s.nii.gz" %(pipeline, strategy, derivative))
        out_file = os.path.join(workingdir,"images/%s_%s_%s" %(pipeline, strategy, derivative))
        subprocess.call(["sh", \
                             "group_analysis/afni_plot.bash", \
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
