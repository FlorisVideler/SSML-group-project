# SSML-group-project

# Notebook overview
- `create_RGB_NDSM_FILES.ipynb` - Floris what 1.
- `create_rgb_dsm.py` - Floris what 2.
- `export images.ipynb` - Script for pulling all required images from a clunky webservice `beeldmateriaal.nl`.
- `mosaic_test.ipynb` - Test for preprocessing tiles to mosaics.
- `predict_all.ipynb` - Use a trained model and predict on all available 4-channel GeoTif's.
- `train_model.ipynb` - Has the outline of a U-Net and DeepLabV3+ ready to be trained. Also able to run one cell for tensorflow Dataset preprocessing.

# Conda environment
1. Create the environment: `conda env create -f environment.yml`
2. Activate the environment: `conda activate solar-segmentation`
