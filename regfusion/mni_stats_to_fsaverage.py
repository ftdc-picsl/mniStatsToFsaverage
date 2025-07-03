#!/usr/bin/env python

import os
import sys
import argparse
from regfusion import vol_to_fsaverage
import nibabel as nib
import numpy as np
from nibabel.gifti import GiftiImage, GiftiDataArray

class RawDefaultsHelpFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def fix_gifti_intent(in_file, out_file):
    """Ensure intent is compatible with Freeview (set to NIFTI_INTENT_SHAPE)."""
    gii = nib.load(in_file)
    data = gii.darrays[0].data.astype(np.float32)
    da = GiftiDataArray(data=data)
    da.intent = "NIFTI_INTENT_SHAPE"
    new_gii = GiftiImage(darrays=[da])
    nib.save(new_gii, out_file)


def main():
    parser = argparse.ArgumentParser(
        description="Project a volumetric NIfTI in MNI152NLin6Asym space to fsaverage LH/RH surfaces using regfusion.",
        formatter_class=RawDefaultsHelpFormatter
    )
    parser.add_argument("input_nii", help="Input NIfTI file (e.g., pmap.nii.gz) in MNI152NLin6Asym space")
    parser.add_argument("output_dir", help="Directory to write fsaverage surface files")
    parser.add_argument("--interp", choices=["linear", "nearest"], default="linear", help="Interpolation method")

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Running regfusion projection for: {args.input_nii}")
    lh_path, rh_path = vol_to_fsaverage(
        input_img=args.input_nii,
        out_dir=args.output_dir,
        template_type="MNI152_orig",  # Assumes input is in tpl-MNI152NLin6Asym
        rf_type="RF_ANTs",
        interp=args.interp,
        out_type="func.gii"  # Output GIFTI format
    )

    # Fix intent for Freeview
    # regfusion outputs "func.gii", but we actually have "shape" data
    lh_out = os.path.join(args.output_dir, "lh.regfusion.shape.gii")
    rh_out = os.path.join(args.output_dir, "rh.regfusion.shape.gii")
    fix_gifti_intent(lh_path, lh_out)
    fix_gifti_intent(rh_path, rh_out)

    print(f"Wrote surfaces:\n  {lh_out}\n  {rh_out}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: mni_stats_to_fsaverage.py <input.nii.gz> <output_dir> [--interp linear|nearest]")
        sys.exit(1)
    main()
