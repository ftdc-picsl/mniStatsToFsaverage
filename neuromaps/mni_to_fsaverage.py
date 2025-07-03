#!/usr/bin/env python

import argparse
import os
import numpy as np
import nibabel as nib
from nilearn import surface, image
from neuromaps.transforms import fslr_to_fsaverage

class RawDefaultsHelpFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def set_gifti_shape_intent(img):
    for da in img.darrays:
        da.intent = 'NIFTI_INTENT_SHAPE'

def process_hemi(hemi, vol_img, mask_img, fsLR_pial, fsLR_white, out_dir):
    print(f"\nProcessing hemisphere: {hemi.upper()}")
    proj_data = surface.vol_to_surf(
        vol_img,
        fsLR_pial,
        mask_img=mask_img,
        inner_mesh=fsLR_white,
        interpolation='linear',
    )

    # Save intermediate fsLR file
    fsLR_func = os.path.join(out_dir, f"{hemi}.fslr.func.gii")
    nib.save(nib.gifti.GiftiImage(darrays=[
        nib.gifti.GiftiDataArray(proj_data.astype(np.float32))
    ]), fsLR_func)

    fsavg_result = fslr_to_fsaverage(fsLR_func, hemi=hemi[0].upper(), target_density='164k')

    if isinstance(fsavg_result, tuple):
        fsavg_img = fsavg_result[0]
    else:
        fsavg_img = fsavg_result

    # Fix intent
    set_gifti_shape_intent(fsavg_img)

    # Rename
    fsavg_out = os.path.join(out_dir, f"{hemi}.fsaverage.shape.gii")
    nib.save(fsavg_img, fsavg_out)
    print(f"Saved fsaverage surface data: {fsavg_out}")
    return fsavg_out

def main():
    parser = argparse.ArgumentParser(
        description="Sample MNI152NLin6Asym volumetric data to fsaverage surface via fsLR 164k.",
        formatter_class=RawDefaultsHelpFormatter,
    )
    parser.add_argument("volume", help="Input volumetric map in MNI152NLin6Asym space (.nii.gz)")
    parser.add_argument("mask", help="Mask image in same space (.nii.gz)")
    parser.add_argument("--lh-pial", default="fsaverage.L.pial_orig.164k_fs_LR.surf.gii",
                        help="Left hemisphere pial surface (fsLR 164k)")
    parser.add_argument("--lh-white", default="fsaverage.L.white_orig.164k_fs_LR.surf.gii",
                        help="Left hemisphere white surface (fsLR 164k)")
    parser.add_argument("--rh-pial", default="fsaverage.R.pial_orig.164k_fs_LR.surf.gii",
                        help="Right hemisphere pial surface (fsLR 164k)")
    parser.add_argument("--rh-white", default="fsaverage.R.white_orig.164k_fs_LR.surf.gii",
                        help="Right hemisphere white surface (fsLR 164k)")
    parser.add_argument("-o", "--out-dir", default="fsaverage_output", help="Directory to save outputs")

    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    vol_img = image.load_img(args.volume)
    mask_img = image.load_img(args.mask)

    lh_out = process_hemi("lh", vol_img, mask_img, args.lh_pial, args.lh_white, args.out_dir)
    rh_out = process_hemi("rh", vol_img, mask_img, args.rh_pial, args.rh_white, args.out_dir)

    print("\nDone. Load these in Freeview with:")
    print(f"  freeview -f $SUBJECTS_DIR/fsaverage/surf/lh.inflated:overlay={lh_out} "
          f"$SUBJECTS_DIR/fsaverage/surf/rh.inflated:overlay={rh_out}")

if __name__ == "__main__":
    main()
