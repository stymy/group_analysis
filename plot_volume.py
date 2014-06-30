import os
from surfer import Brain
from surfer.io import project_volume_data
import sys

volume_file = sys.argv[1]

hemi = sys.argv[2]

brain = Brain("fsaverage", hemi , "inflated")

reg_file = os.path.join(os.environ["FREESURFER_HOME"],
                        "average/mni152.register.dat")
zstat = project_volume_data(volume_file, hemi, reg_file)

#zstat = project_volume_data(volume_file, "lh", subject_id="fsaverage", smooth_fwhm=0.5)
                            
brain.add_overlay(zstat)

brain.show_view("medial")
