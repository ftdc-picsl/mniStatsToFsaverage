# mniStatsToFsaverage
Workflow to project group data from MNI to fsaverage for visualization

## This is a WIP

Validate outputs carefully! It would be wise to include slices of the MNI data as
supplementary figures.

Note that no masking is applied here, so if your input data does not align well to the MNI
cortex, projections may include background voxels.


## Requirements

    * Python with the regfusion package installed (`pip install regfusion`)
    * Freesurfer


## Usage

```
./mni_stats_to_fsaverage.py input.nii.gz output_dir [--interp linear|nearest]
```

Where `input.nii.gz` is a group-level statistical map in MNI152NLin6Asym space, and
`output_dir` is the directory where the output files will be written.

The original outputs are "func.gii" files, but we fix the intent to "shape" so that
Freeview can load them correctly. The output files will be named `lh.regfusion.shape.gii` and
`rh.regfusion.shape.gii` for the left and right hemispheres, respectively.
```

## Visualization

First load the hemisphere into freeview, then interactively load the output as an overlay

```
freeview \
  -f $FREESURFER_HOME/subjects/fsaverage/surf/lh.inflated \
  -f $FREESURFER_HOME/subjects/fsaverage/surf/rh.inflated
```

You can then load the output files as a "generic" overlay. For reasons I don't understand,
it won't load if specified on the command line.

## Citation

Please credit the Python package

https://github.com/danjgale/reg-fusion

and cite the original paper:

Wu J, Ngo GH, Greve DN, Li J, He T, Fischl B, Eickhoff SB, Yeo BTT. Accurate nonlinear mapping between MNI volumetric and FreeSurfer surface coordinate systems, Human Brain Mapping 39:3793–3808, 2018.