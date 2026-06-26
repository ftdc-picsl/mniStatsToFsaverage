# Connectome workbench resample to surface

This script uses the CBIG fslr-32k surfaces and the Connectome Workbench wb_command to
resample volumetric data from MNI6 to the fsLR 32k surface space.

Unlike the other methods, this just outputs in the fsLR space directly, and does not use
any transform to fsaverage space.

See

https://www.humanconnectome.org/software/workbench-command/-volume-to-surface-mapping

for additional options that may be useful including `-volume-roi` (using a mask in volume
space), `-gaussian` (downweight away from the target surface) and `-dilate-missing`.

The results can be displayed in freeview, overlaid on the CBIG surfaces.

Note: Load all surface data before loading any volumes, for some reason doing it the other
way causes surfaces to appear rotated in freeview.