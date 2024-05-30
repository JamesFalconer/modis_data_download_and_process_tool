import geopandas as gpd
import numpy as np
from shapely.geometry import box
from shapely.geometry import Polygon


def bbox(lng_min, lat_min, lng_max, lat_max):
    return Polygon([[lng_min, lat_min], [lng_min, lat_max],
                    [lng_max, lat_max], [lng_max, lat_min]])

def clip_data(dataset_input, clipping_shapefile):
    shapefile_to_crs = clipping_shapefile.to_crs(dataset_input.rio.crs)

    clip_bound_box = [box(*shapefile_to_crs.total_bounds)]

    clipped_dataset = dataset_input.rio.clip(clip_bound_box,
                                             all_touched=True,
                                             from_disk=True)
    return clipped_dataset


def get_numpy_array_from_dataset(dataset) -> np.ndarray:
    dataset = dataset.to_dataarray().to_numpy()  # transform dataset into dataarray and then to numpy array
    dataset = dataset.transpose(2, 3, 0, 1)  # numpy array has 4 dimensions and shape [x,y,c,c] where the data is
    # on the diagonals of dimensions 3 and 4

    # Reducing the dimensions to 3 by compacting the data on the diagonal
    diagonal_indices = np.arange(dataset.shape[2])
    diagonal_elements = dataset[:,:,diagonal_indices,diagonal_indices]
    collapsed_array = diagonal_elements.reshape(diagonal_elements.shape[0], diagonal_elements.shape[1], -1)
    return collapsed_array

