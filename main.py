import os

import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

import config
import query_data
import download_data
import open_img_data
import clip_data
import index_implementation
import test_site_dict


def run(site, res_250=False):
    dates = site['dates']
    location_plot_name = site['location_plot_name']
    location_save_name = site['location_save_name']
    location_bounds = site['location_bounds']
    location = site['location']

    location_dataframe = gpd.GeoDataFrame(pd.DataFrame(['p1'], columns=['geom']),
                                          crs={'init': 'epsg:4326'},
                                          geometry=[clip_data.bbox(location_bounds[0], location_bounds[1],
                                                                   location_bounds[2], location_bounds[3])])

    if not os.path.exists('data/'):
        os.mkdir('data')

    img_dir = 'data/' + location_save_name + '/'

    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    output_dir = img_dir + 'images/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # Query data
    modis_results = query_data.query(satellite=config.MODIS_SATELLITE, dates=(dates[0], dates[1]),
                                     location=(location[0], location[1], location[0], location[1]), res_250=res_250)

    result_list = []
    for result in modis_results:
        print(result['meta']['native-id'])
        result_list.append(result['meta']['native-id'])

    # Download data
    download_data.download_modis_data(modis_results, download_location=img_dir)
    # Open Data

    # Open data
    # shape_file_path =
    for file in os.listdir(img_dir):

        if os.path.isfile(img_dir + file):

            if res_250 and file.__contains__('GQ'):
                data = open_img_data.open_modis_250m_data_as_dataset(img_dir + file)
                date = data.RANGEBEGINNINGDATE
                clipped_data = clip_data.clip_data(data, location_dataframe)

                clipped_data_numpy = clip_data.get_numpy_array_from_dataset(clipped_data)

                """plt.figure()
                plt.imshow(clipped_data_numpy[:,:,0])
                plt.figure()
                plt.imshow(clipped_data_numpy[:,:,1])"""
                plt.figure()
                plt.imshow(clipped_data_numpy[:, :, 0], cmap='gray')
                plt.axis('off')
                plt.title(location_plot_name + ' ' + str(date) + ' Red Band')
                plt.savefig(output_dir + location_save_name + '_' + str(date) + 'red_band.jpg', dpi=1500)

                plt.figure()
                plt.imshow(clipped_data_numpy[:, :, 1], cmap='gray')
                plt.title(location_plot_name + ' ' + str(date) + ' NIR Band')
                plt.axis('off')
                plt.savefig(output_dir + location_save_name + '_' + str(date) + 'nir_band.jpg', dpi=1500)

                index_output = index_implementation.r_nir_index(clipped_data_numpy)
                index_output[index_output > 1] = np.nan
                index_output[index_output < -1] = np.nan
                plt.figure()
                plt.imshow(index_output, cmap='gray', interpolation=None)
                plt.title(location_plot_name + ' ' + str(date))
                plt.axis('off')
                plt.savefig(output_dir + location_save_name + '_' + str(date) + 'index_250.jpg', dpi=1500)

            elif not res_250 and file.__contains__('GA'):

                print("Starting Process")
                # clipped_data = open_img_data.open_clipped_img(img_dir + file, shape_file_path)
                data = open_img_data.open_modis_500m_data_as_dataset(img_dir + file)
                date = data.RANGEBEGINNINGDATE

                clipped_data = clip_data.clip_data(data, location_dataframe)

                clipped_data_numpy = clip_data.get_numpy_array_from_dataset(clipped_data)
                rgb = np.zeros((clipped_data_numpy.shape[0], clipped_data_numpy.shape[1], 3))

                rgb[:, :, 0] = clipped_data_numpy[:, :, 0]
                rgb[:, :, 1] = clipped_data_numpy[:, :, 3]
                rgb[:, :, 2] = clipped_data_numpy[:, :, 2]
                rgb[rgb == np.nan] = 0
                rgb = (rgb - np.nanmin(rgb)) / (np.nanmax(rgb) - np.nanmin(rgb))
                plt.figure()
                plt.imshow(rgb)
                plt.title(location_plot_name + ' ' + str(date))
                plt.axis('off')
                plt.savefig(output_dir + location_save_name + '_' + str(date) + 'rgb.jpg', dpi=1500)

                # data = open_img_data.open_modis_500m_data(img_dir + file)

                # Process data
                ndrti_output = index_implementation.implement_ndrti_modis(clipped_data_numpy)
                ndrti_output[ndrti_output > 1] = np.nan
                ndrti_output[ndrti_output < -1] = np.nan

                plt.figure()
                plt.imshow(ndrti_output, cmap='gray', interpolation=None)
                plt.title(location_plot_name + ' ' + str(date))
                plt.axis('off')
                plt.savefig(output_dir + location_save_name + '_' + str(date) + 'index.jpg', dpi=1500)
                # plt.show()

                plt.figure()
                plt.hist(ndrti_output.ravel(), bins=256, range=[-1, 1])
    #plt.show()
            plt.close('all')


if __name__ == '__main__':
    # Setup values
    vals = ['0', '1', '2', '3', '4', '5', '6']
    vals = ['8']
    # vals = []

    for site_num in vals:
        site = test_site_dict.test_sites[site_num]
        run(site, res_250=True)
        run(site, res_250=False)
