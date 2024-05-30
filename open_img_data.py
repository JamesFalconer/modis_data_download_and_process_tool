import numpy as np
import rioxarray as rxr
import matplotlib.pyplot as plt
import xarray as xr
import geopandas as gpd
from pyhdf import HDF, V, HC, SD

"""
def open_modis_500m_data(hdf_path: str) -> np.ndarray:
    desired_bands = ["sur_refl_b01_1",
                     "sur_refl_b02_1",
                     "sur_refl_b03_1",
                     "sur_refl_b04_1",
                     "sur_refl_b05_1",
                     "sur_refl_b06_1",
                     "sur_refl_b07_1"]
    
    hdf_file = SD.SD(hdf_path)
    hdf_datasets = hdf_file.datasets()
    
    band_shape = hdf_file.datasets().get('sur_refl_b01_1')[1]
    modis_data = np.zeros((band_shape[0],band_shape[1], 7))
    for i in range(len(desired_bands)):
        band_name = desired_bands[i]
        band = np.array(hdf_file.select(band_name).get())
        modis_data[:,:,i] = band
    
    return modis_data
"""


def open_modis_500m_data(hdf_path: str) -> np.ndarray:
    desired_bands = ["sur_refl_b01_1",
                     "sur_refl_b02_1",
                     "sur_refl_b03_1",
                     "sur_refl_b04_1",
                     "sur_refl_b05_1",
                     "sur_refl_b06_1",
                     "sur_refl_b07_1"]
    modis_pre_bands = rxr.open_rasterio(hdf_path,
                                        masked=True,
                                        variable=desired_bands).squeeze()
    modis_pre_bands = modis_pre_bands.to_dataarray().to_numpy()
    modis_pre_bands = modis_pre_bands.transpose(1, 2, 0)
    return modis_pre_bands


def open_modis_500m_data_as_dataset(hdf_path: str):
    desired_bands = ["sur_refl_b01_1",
                     "sur_refl_b02_1",
                     "sur_refl_b03_1",
                     "sur_refl_b04_1",
                     "sur_refl_b05_1",
                     "sur_refl_b06_1",
                     "sur_refl_b07_1"]
    out_xr = []
    for i, tif_path in enumerate(desired_bands):
        out_xr.append(rxr.open_rasterio(filename=hdf_path, masked=True, variable=tif_path).squeeze())
        out_xr[i]["band"] = i + 1
    return xr.concat(out_xr, dim='band')


def open_modis_250m_data_as_dataset(hdf_path: str):
    desired_bands = ["sur_refl_b01_1",
                     "sur_refl_b02_1",
                     ]
    out_xr = []
    for i, tif_path in enumerate(desired_bands):
        out_xr.append(rxr.open_rasterio(filename=hdf_path, masked=True, variable=tif_path).squeeze())
        out_xr[i]["band"] = i + 1
    return xr.concat(out_xr, dim='band')


def get_shapefile_data(shapefile_path):
    shapefile_data = gpd.read_file(shapefile_path)
    return shapefile_data
