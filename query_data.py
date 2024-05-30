import earthaccess

import config


def query(satellite: str, dates, location, res_250=False):
    earthaccess.login(strategy='netrc')

    if satellite == config.MODIS_SATELLITE:
        query_data = query_modis_data(dates, location, res_250)
        return query_data


def query_modis_data(dates, location, res_250):
    if res_250:
        modis_query = earthaccess.search_data(short_name=config.SHORT_NAME_MODGQ,
                                              bounding_box=location,
                                              temporal=dates,
                                              cloud_hosted=True,
                                              count=-1)
    else:
        modis_query = earthaccess.search_data(short_name=config.SHORT_NAME_MODIS_500_DAILY,
                                          bounding_box=location,
                                          temporal=dates,
                                          cloud_hosted=True,
                                          count=-1)  # note - have to have "count" variable for it to work

    return modis_query


def get_collections(data_query):
    collections = data_query.get()
    return collections
