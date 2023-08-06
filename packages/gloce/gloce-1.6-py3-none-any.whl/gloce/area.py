import numpy as np
import matplotlib.pyplot as plt
def globalarea(reso,lat = [90, -90],lon=[-180, 180]):
    '''
    Return global or regional area for each grid cell

    Parameters
    ----------
    reso : float
        Resolution of the area (should not be too small or there will be momery error).
    lat : list, optional
        Latitude of interest. The default is [90, -90] (global).
    lon : list, optional
        Longitude of interest. The default is [-180, 180] (global).
        Some frequently-used area: 
            China: lat = [55,15],lon=[70,140]
            SA: lat = [15,-60],lon=[-90,-150]
            Africa: lat = [30,-40],lon=[-150,55]

    Returns
    -------
    2d-array
        Area for each grid cell.

    '''
    lat = np.array(lat)
    lon = np.array(lon)
    if np.any(lat > 90) or np.any(lat < -90):
        raise Exception('Error: latitude out of bound.')
    if np.any(lon > 180) or np.any(lon < -180):
        raise Exception('Error: longitude out of bound.')
    nlon = int(360 / reso)
    nlat = int(180 / reso)
    lat_area = np.zeros(nlat)
    RE = 6371.393  #earth redius 6371.393 k
    for i in np.arange(nlat):
        lat_area[i] = abs(2 * np.pi * (RE**2) *
            (np.cos(np.pi * (i + 1) / nlat) - np.cos(np.pi * i / nlat))) / nlon
    area = np.zeros((nlat, nlon))
    for i in np.arange(nlon):
        area[:, i] = lat_area
    return (area[int((90 - lat[0]) *(1 / reso)):int((90 - lat[1]) * (1 / reso)),
                 int((180 + lon[0]) *(1 / reso)):int((180 + lon[1]) * (1 / reso))])


def gridarea(reso,lat,lon,size=1):
    '''
    Parameters
    ----------
    reso : float
        Resolution of the area.
    lat : float
        Upper latitude.
    lon : float
        Left longitude.
    size : Float, optional
        The number of degree for creating area. Unit: degree.The default is 1.

    Raises
    ------
    Exception
        resolution should be smaller than 1.

    Returns
    -------
    2d-array
        Area for each grid cell.

    '''
    if reso>1:
        raise Exception('Error: resolution > 1.')
    RE = 6371.393  #earth redius 6371.393 k
    nsize = int(size/reso)
    lat_area = np.zeros(nsize)
    for i in np.arange(nsize):
        lat_area[i] = abs(2 * np.pi * (RE**2) *
            (np.sin(np.pi * (lat - i * reso - reso) / 180) -
             np.sin(np.pi * (lat - i * reso) / 180))) * reso / 360
    area = np.zeros((nsize, nsize))
    for i in np.arange(nsize):
        area[:, i] = lat_area
    return (area)






        
