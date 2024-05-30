import numpy as np
import matplotlib.pyplot as plt


def implement_mswi_modis(modis_bands: np.ndarray) -> np.ndarray:
    modis_temp = modis_bands.copy()
    modis_temp = modis_temp * 0.0001
    modis_temp[modis_temp <= 0] = 0
    modis_temp[modis_temp > 1] = 1
    img_blue_band = modis_temp[:, :, 2]
    img_nir_band = modis_temp[:, :, 1]
    img_swir1_band = modis_temp[:, :, 4]
    img_swir2_band = modis_temp[:, :, 5]
    img_swir3_band = modis_temp[:, :, 6]
    mswi = (img_blue_band - 1/4*(img_nir_band + img_swir1_band + img_swir2_band + img_swir3_band)) / (img_blue_band + 1/4*(img_nir_band + img_swir1_band + img_swir2_band + img_swir3_band))
    return mswi


def r_nir_index(modis_bands: np.ndarray) -> np.ndarray:
    modis_temp = modis_bands.copy()
    modis_temp = modis_temp * 0.0001
    modis_temp[modis_temp <= 0] = 0
    modis_temp[modis_temp > 1] = 1
    img_red_band = modis_temp[:, :, 0]
    img_nir_band = modis_temp[:, :, 1]
    index_output = (img_red_band - img_nir_band) / (img_red_band + img_nir_band)
    return index_output


def implement_ndrti_modis(modis_bands: np.ndarray) -> np.ndarray:
    modis_temp = modis_bands.copy()
    modis_temp = modis_temp * 0.0001
    modis_temp[modis_temp <= 0] = 0
    modis_temp[modis_temp > 1] = 1
    img_nir_band = modis_temp[:, :, 1]
    img_swir2_band = modis_temp[:, :, 5]
    ndrti_index = (img_nir_band - img_swir2_band) / (img_nir_band + img_swir2_band)
    return ndrti_index


def implement_ndvi_modis(modis_bands: np.ndarray) -> np.ndarray:
    modis_temp = modis_bands.copy()
    modis_temp = modis_temp * 0.0001
    modis_temp[modis_temp <= 0] = 0
    modis_temp[modis_temp > 1] = 1
    img_red_band = modis_temp[:, :, 0]
    img_nir_band = modis_temp[:, :, 1]
    ndvi_index = (img_nir_band - img_red_band) / (img_nir_band + img_red_band)
    return ndvi_index


