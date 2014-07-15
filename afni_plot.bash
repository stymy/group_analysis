#!/usr/bin/env bash

# This will make axial plots of each of the summary images

fname=$1
outname=$2

cd $(dirname ${fname})
overlay=$(basename ${fname})

# Get Center of Mass
cm=$(3dCM std_1mm_head.nii.gz)

# Open up window 
window=42
`which Xvfb` :${window} -screen 0 1024x768x24 &
echo $overlay

#echo ${fname} | grep func_mean > /dev/null
#is_not_mean=$?

# Use afni to plot axial slicea
afni \
    -com "OPEN_WINDOW sagittalimage" \
    -com "SWITCH_UNDERLAY std_1mm_head.nii.gz" \
    -com "SWITCH_OVERLAY ${overlay}" \
    -com "SET_PBAR_ALL -99 1 Spectrum:yellow_to_cyan+gap" \
    -com "OPEN_WINDOW axialimage mont=5x1:12 geom=1800x430" \
    -com "SET_XHAIRS OFF" \
    -com "SAVE_PNG axialimage ${outname}_axial.png" \
    -com "SAVE_PNG sagittalimage ${outname}_saggital.png" \
    -com "QUIT"
    # -com "SET_FUNC_RANGE 0" \
    # -com "SET_DICOM_XYZ ${cm}" \
    # -com "SET_THRESHNEW 0" \

echo "saved"

# Close imaginary window
killall Xvfb
