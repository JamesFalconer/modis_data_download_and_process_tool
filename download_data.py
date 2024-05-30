import earthaccess

import config


def download_modis_data(modis_query_results, download_location=None):
    earthaccess.login(strategy='netrc')
    data_links = [granule.data_links(access="external") for granule in modis_query_results]

    if download_location:
        earthaccess.download(modis_query_results, download_location)
    else:
        earthaccess.download(modis_query_results, config.DATA_LOCATION)

