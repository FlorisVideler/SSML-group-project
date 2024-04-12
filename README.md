# SSML-group-project

# Repo overview

## Notebook overview
- `create_rgb_dsm.py` - Script for merging the RGB channels with the DSM.
- `export images.ipynb` - Script for pulling all required images from a clunky webservice `beeldmateriaal.nl`.
- `mosaic_test.ipynb` - Test for preprocessing tiles to mosaics.
- `predict_all.ipynb` - Use a trained model and predict on all available 4-channel GeoTif's.
- `train_model.ipynb` - Has the outline of a U-Net and DeepLabV3+ ready to be trained. Also able to run one cell for tensorflow Dataset preprocessing.
- `surface\ area/calculate\ surface\area.ipynb` - Test code to calculate the surface area of segmented solarpanels based on the area and the slope from the DSM.

## Folder overview
- `masks/` - geoPackage files of 1km^2 with polygons of manually labeled solarpanels. Tiles chosen for patial diversity of the study area.
- `RGB_DSM/` - Tif files of 1km^2, 12500 * 12500 pixels with a resolution of 8cm (per pixel). The tif file contains 4 channels R, G, B & height (DSM).
- `logs/fit/` - Location for Tensorboard to store its graphs.
- `history/*.json` - Model experiment history.
- `predicted/*.tiff` - Predicted outputs of the model from `predict_all.ipynb`. Same size and prediction resolution as input tiles from `RGB_DSM`.
- `surface\ area` - Work done pertaining to calculating the surface area of segmented masks based on area and slope from the DSM.

# Data

## Train, validate, test
- set1
- set2
- set3

# Conda environment
1. Create the environment: `conda env create -f environment.yml`
2. Activate the environment: `conda activate solar-segmentation`
