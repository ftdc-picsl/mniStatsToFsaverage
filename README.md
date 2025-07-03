# mniStatsToFsaverage
Workflow to project group data from MNI to fsaverage for visualization

## This is a WIP

Validate outputs carefully! It would be wise to include slices of the MNI data as
supplementary figures.


## regfusion

This uses the regfusion package to project group-level statistical maps from MNI152NLin6Asym space
to the fsaverage surface space. It is based on the original method by Wu et al. (2018).
See the README for citations and usage instructions.


## neuromaps

This uses nilearn and neuromaps, and offers a bit more flexibility in terms of sampling.
See the README for citations and usage instructions.