import numpy as np
def interpolation_map(map_in,min_obs=10,mask = np.nan):
    '''
    Interpolation with the nearest value on the map
    
    Parameters
    ----------
    map_in : 2d array
        map that need to be interpolated 
    min_obs : int, optional
        the minimum pixels used to interpolate the grid cell
    mask : 2d array, optional
        only execuate interpolation where mask>0.
    Returns
    -------
    smy : 2d array
        Interpolated map.
    '''
    lat = map_in.shape[0]
    lon = map_in.shape[1]
    smy = np.zeros((lat,lon))
    smy[:] = np.nan
    filled_value = np.nansum(map_in*mask)/np.nansum(mask)
    if np.isnan(filled_value):
        raise ValueError('all data is nan, return nan')
    else:
        print('filled_value = {:.2f}'.format(filled_value))
        if np.isnan(mask).all():
            mask=np.ones((lat,lon))
        else:
            print('Mask is used.')
        for i in range(lat):
            print('\r'+'{:.2%}'.format((i+1)/lat),end = '')
            for j in range(lon):
                if mask[i,j]>0:
                    if np.isnan(map_in[i,j]):
                        n = 1
                        data = np.nan
                        while np.isnan(data):
                            xmin = j-n
                            if xmin<0:
                                xmin=0
                            ymin = i-n
                            if ymin<0:
                                ymin=0
                            select = map_in[ymin:i+n+1,xmin:j+n+1]
                            if np.nansum(~np.isnan(select))>=10:
                                data = np.nanmean(select)
                            n=n+1
                            if n>10:
                                data = filled_value
                        smy[i,j] = data
                    else:
                        smy[i,j] = map_in[i,j]
    return smy


def interpolation_time(array, time):
    '''
    Linear interpolation for known time series

    Parameters
    ----------
    array : 2d array
        Shape(nraw,mcol) nraw: N rows of data; mcol:M column data.
    time : list
        A list of time of each colunm; the shape should be the same as M.
        The time step is assumed to be 1 year(maybe change in future)

    Returns
    -------
    smy : 2d array
        Interpolated array.

    '''
    time = np.array(time)
    raws = array.shape[0]
    time = time - time[0]
    smy = np.zeros((raws, (time[-1] + 1)))
    for i in range(len(time) - 1):
        tem = np.zeros((raws, (time[i + 1] - time[i])))
        for j in range(time[i + 1] - time[i]):
            tem[:,
                j] = array[:, i] + (array[:, i + 1] -
                                    array[:, i]) * j / (time[i + 1] - time[i])
        smy[:, time[i]:time[i + 1]] = tem
    smy[:, -1] = array[:, -1]
    return smy






