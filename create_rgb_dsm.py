from tqdm import tqdm

import xarray
import glob
from rioxarray.merge import merge_arrays
import rioxarray

from zipfile import ZipFile
from io import BytesIO

import os
import requests
from datetime import datetime

import warnings

warnings.filterwarnings("ignore")


def download_tif(url, dir_path):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip_ref:
            # Loop through each file in the zip
            for zip_info in zip_ref.infolist():
                # Extract only files, ignore directories
                if not zip_info.is_dir():
                    # Use the file name only, ignoring any directory paths in the zip file
                    zip_info.filename = os.path.basename(zip_info.filename)
                    # Extract the file with the new path
                    zip_ref.extract(zip_info.filename, path=dir_path)
    else:
        print(f"{datetime.now()} {url} failed")


def create_dir(path):
    # Check if the directory exists
    if not os.path.exists(path):
        # Create the directory if it does not exist
        os.makedirs(path)
        print(f"Directory '{path}' was created.")
    else:
        print(f"Directory '{path}' already exists.")


current_dir = os.getcwd()
DSM_dir_path = current_dir + r"\DSM"
DTM_dir_path = current_dir + r"\DTM"
RGB_DSM_dir_path = current_dir + r"\RGB_DSM"

DSM_files = ["https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_31GN2.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_31HN1.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_31HN2.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_32CN1.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_31GZ2.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_31HZ1.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_31HZ2.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_32CZ1.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_38EN2.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_38FN1.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_38FN2.zip",
             "https://ns_hwh.fundaments.nl/hwh-ahn/ahn4/03a_DSM_0.5m/R_39AN1.zip"]

for DSM_file in tqdm(DSM_files):
    download_tif(DSM_file, DSM_dir_path)

# Use glob to find all TIFF files in the directory
tif_files = glob.glob(f"{DSM_dir_path}/*.TIF")

# Load each TIFF file
DSMs = []
for file_path in tif_files:
    DSM = rioxarray.open_rasterio(file_path)
    DSMs.append(DSM)

# Merge all the raster datasets into one big raster
merged_DSM = merge_arrays(DSMs)

no_data_value = 30000

# Replace extreme values with 0
merged_DSM = merged_DSM.where(merged_DSM < no_data_value, 0)

merged_DSM = merged_DSM.fillna(0)

rgb_files = glob.glob("nl_8cm/*.tif")

for rgb_file in tqdm(rgb_files):
    # Load rgb file
    rgb = rioxarray.open_rasterio(rgb_file)
    bounds = rgb.rio.bounds()
    # Slice rgb file outline from NDSM file
    sub_DSM = merged_DSM.rio.clip_box(minx=bounds[0], miny=bounds[1], maxx=bounds[2], maxy=bounds[3])
    # Upsample to same resolution as RGB images
    sub_DSM = sub_DSM.interp(y=rgb.y, x=rgb.x, method='nearest')
    # Merge RGB with DSM
    combined = xarray.concat([rgb, sub_DSM], dim='band')
    # Write R,G,B,DSM file
    filename = rgb_file.split("\\")[-1]  # Corrected: Escape the backslash or use a raw string if needed
    combined.rio.to_raster(f"RGB_DSM/{filename}")
