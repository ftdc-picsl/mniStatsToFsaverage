# mniStatsToFsaverage
Workflow to project group data from MNI to fsaverage for visualization.

This version uses nilearn and neuromaps, and offers a bit more flexibility in terms of
sampling than the regfusion approach.


## Requirements

* Python with the `nilearn` and `neuromaps` packages installed (`pip install nilearn
  neuromaps`)
* Connectome workbench (wb_command)
* fsLR meshes


## Input

The main input is a volume in the MNI152NLin6Asym space. The mask should be in the same
space, and defines the domain of sampling.

The script also expects meshes in the "fsLR" template space. These can be downloaded from
the [CBIG repository](https://github.com/ThomasYeoLab/CBIG.git). For compatibility with freeview, use the 164k meshes.

The script calls nilearn's `vol_to_surf` function with the given meshes. Sampling is done
along lines projected from the pial to the white surface. Only voxels within the mask are
sampled.

The resampling to fsaverage space is done using the `neuromaps` package, which calls `wb_command`.