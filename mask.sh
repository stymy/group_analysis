#!/bin/bash

echo "Concatenate Files"
3dTcat *func_mask.nii.gz

echo "Convert to Nifti"
3dAFNItoNIFTI tcat+orig*

echo "FSLMATHS to creat masks"
fslmaths tcat.nii -Tmean meancat.nii
fslmaths meancat.nii -thr .9 -bin ninety_mask.nii
fslmaths meancat.nii -thr .95 -bin ninetyfive_mask.nii
fslmaths meancat.nii -thr .85 -bin eightyfive_mask.nii
fslmaths meancat.nii -thr .8 -bin eighty_mask.nii