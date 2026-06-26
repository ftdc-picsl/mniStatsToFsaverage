#!/bin/bash

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <volume_data> <output_name> <template_dir>

  Volume data should be in MNI152NLin6Asym space.

  Template mesh directory should contain the following files:
   fsaverage.L.midthickness_orig.32k_fs_LR.surf.gii
   fsaverage.L.white_orig.32k_fs_LR.surf.gii
   fsaverage.L.pial_orig.32k_fs_LR.surf.gii

   These can be downloaded from the CBIG repository: https://github.com/ThomasYeoLab/CBIG

   If you clone the main repository, the files can be found in: CBIG/data/templates/surface/fs_LR_32k

"
  exit 1
fi

volume_data=$1
output_name=$2
template_dir=$3

if [[ ! -f "$volume_data" ]]; then
  echo "Error: Volume data file '$volume_data' does not exist."
  exit 1
fi

wb_command -volume-to-surface-mapping \
  ${volume_data} \
  ${template_dir}/fsaverage.L.midthickness_orig.32k_fs_LR.surf.gii \
  L.${output_name}.32k_fs_LR.func.gii \
  -ribbon-constrained \
  ${template_dir}/fsaverage.L.white_orig.32k_fs_LR.surf.gii \
  ${template_dir}/fsaverage.L.pial_orig.32k_fs_LR.surf.gii

wb_command -volume-to-surface-mapping \
  ${volume_data} \
  ${template_dir}/fsaverage.R.midthickness_orig.32k_fs_LR.surf.gii \
  R.${output_name}.32k_fs_LR.func.gii \
  -ribbon-constrained \
  ${template_dir}/fsaverage.R.white_orig.32k_fs_LR.surf.gii \
  ${template_dir}/fsaverage.R.pial_orig.32k_fs_LR.surf.gii