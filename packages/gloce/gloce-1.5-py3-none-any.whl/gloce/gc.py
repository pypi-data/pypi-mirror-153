__author__ = 'zl'
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os


def running_mean(x, N):
    cumsum = np.nancumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)




#0412 



def downreso(matrix, rstep, cstep, func=np.sum):
    row, col = np.shape(matrix)
    temp = matrix.reshape(int(row / rstep), rstep, int(col / cstep), cstep)
    temp = func(temp, axis=1)
    temp = func(temp, axis=2)
    return temp
#0412 这个添加了权重，可以考虑加进去
def downreso(matrix, rstep, cstep, we=0):
    row, col = np.shape(matrix)
    temp = matrix.reshape(int(row / rstep), rstep, int(col / cstep), cstep)
    we = we.reshape(int(row / rstep), rstep, int(col / cstep), cstep)
    temp = nanaverage(temp, axis=1,weights = we)
    we = np.nansum(we, axis=1)
    temp = nanaverage(temp, axis=2,weights = we)
    we2 = np.nansum(we, axis=2)
    return temp,we2





def upresolution(matrix, rstep, cstep):
    row, col = np.shape(matrix)
    temp = np.ravel(matrix)
    #Reduce the dimension of the array to one dimension
    temp = np.array([
        temp[int(i / cstep):int(i / cstep) + 1]
        for i in range(cstep * len(temp))
    ])  #Operate horizontally
    temp = temp.reshape(row, int(col * cstep))
    temp = temp.T
    temp = np.ravel(temp)
    temp = np.array([
        temp[int(i / rstep):int(i / rstep) + 1]
        for i in range(rstep * len(temp))
    ])  #Operate vetically
    temp = temp.reshape(int(col * cstep), int(row * rstep))
    temp = temp.T
    return temp


def imshow(matrix,
           lon1=-180,
           lon2=180,
           lat1=-90,
           lat2=90,
           title='',
           cmap='YlOrBr',
           china=False):
    lon = (lon2 - lon1) / 10
    lat = (lat2 - lat1) / 10
    if lon > 20:
        lon = lon / 2
        lat = lat / 2
    fig = plt.figure(figsize=[lon, lat])
    ax = fig.add_subplot(111)
    m = Basemap(llcrnrlon=lon1, llcrnrlat=lat1, urcrnrlon=lon2, urcrnrlat=lat2)
    m.drawcoastlines(linewidth=0.5, color='gray')
    im = m.imshow(matrix, origin='upper', cmap=cmap)
    if china:
        m.readshapefile('E:/shp/china', 'china', drawbounds=True, zorder=40)
    ax.set_title(title)
    cbar_ax = plt.gcf().add_axes([0.90, 0.15, 0.02,
                                  0.7])  #[left,bottom,width,height]
    plt.colorbar(im, cax=cbar_ax)


def nanravel(matrix):
    matrix = np.ravel(matrix)
    matrix = matrix[np.logical_not(np.isnan(matrix))]
    return matrix
os.listdir

def listdir(path, suffix, suffix_on=1, prefix=0):
    # filter path with specific suffix(or prefix)
    if prefix == 1:
        num = len(suffix)
        ls = np.array([])
        for p in tem:
            if p[:num] == suffix:
                ls = np.append(ls, p)
    else:
        tem = os.listdir(path)
        if suffix_on == 1:
            num = len(suffix)
            ls = np.array([])
            for p in tem:
                if p[-num:] == suffix:
                    ls = np.append(ls, p)

        return ls


##############################################################################
# 210818
# interpolation with the nearest value on the map
# defualt: use the nearest 10 pixel to represent this grid cell value
# mask: only execuate interpolation where mask>0.
##############################################################################
def interpolation_map(map_in,min_obs=10,mask = np.nan):
    '''
    interpolation with the nearest value on the map
    
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
    None.
    '''
    lat = map_in.shape[0]
    lon = map_in.shape[1]
    smy = np.zeros((lat,lon))
    smy[:] = np.nan
    filled_value = np.nansum(map_in*mask)/np.nansum(mask)
    if np.isnan(filled_value):
        print('all data is nan, return nan')
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

def nanaverage(data,axis=0,weights=0):
    tem1 = np.nansum(data*weights,axis=axis)
    tem2 = np.nansum(weights,axis=axis)
    return tem1/tem2



# Linear interpolation for known time series
# array: Numpy array: shape(nraw,mcol) nraw: N rows of data; mcol:M column data
# time: a list of time of each colunm; the shape should be the same as M
# the time step is assumed to be 1 year(maybe change in future)
# test
# array = np.array(pd.read_clipboard())
# time = np.array([1850,1900,1949,2000])
def interpolation(array, time):
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



def arrayinfo(array):
    a0 = np.array([1, 2])
    if type(array) != type(a0):
        print("It's not an numpy.ndarray")
        return None
    array_max = np.max(array)
    if np.isnan(array_max):
        print('Nan exists\nmaxium:{:.2f}'.format(np.nanmax(array)))
        print('minmium:{:.2f}'.format(np.nanmin(array)))
    else:
        print('Nan not exists\nmaxium:{:.2f}'.format(array_max))
        print('minmium:{:.2f}'.format(np.min(array)))
    print('shape:', array.shape)
    print('dtype:', array.dtype)


def exclude_outlier(array):
    arraystd = np.nanstd(array, ddof=1)
    arraymean = np.nanmean(array)
    arrayoutlier = np.where(np.abs(array - arraymean) > (3 * arraystd))
    print(array[arrayoutlier])
    print(arraystd)
    array[arrayoutlier] = np.nan
    return array


# 210617
# calculate weighted median
def percentile_mean(array, w, percentile=0.5):
    w = w / np.sum(w)  # normalization
    tem = np.vstack([array, w])
    sort = np.argsort(tem[0])
    tem = tem[:, sort]
    min_loc = np.argmin(abs(np.cumsum(tem[1]) - percentile))
    return tem[0, min_loc]


##############################################################################
# 210915
# equal to ee.remap in GEE.
# Using np.vectorize is much faster than loop
# a should has the dimension of 2.
# very slow(not for large data)
##############################################################################
def remap(a, list_ori = [],list_aft = []):
    my_dict = dict(zip(list_ori,list_aft))
    return np.vectorize(my_dict.__getitem__)(a)
def remap(a, list_ori = [],list_aft = []):
    my_dict = dict(zip(list_ori,list_aft))
    list_ori_ra = np.unique(a)
    list_aft_ra = []
    for i in list_ori_ra:
        list_aft_ra.append(my_dict[i])
    my_dict_ra = dict(zip(list_ori_ra,list_aft_ra))
    return np.vectorize(my_dict_ra.__getitem__)(a)



##############################################################################
# 210924
# equal to Mosaic To New Raster in Arcgis.
# Using gdal_merge.py to mosaics a set of images.
# This utility will automatically mosaic a set of images. 
# All the images must be in the same coordinate system and have a matching number of bands, but they may be overlapping, and at different resolutions. 
# In areas of overlap, the last image will be copied over earlier ones.
##############################################################################
import subprocess
def m2newraster(pathout,pathin,file=0,options='COMPRESS=LZW'):
    '''
    Equal to Mosaic To New Raster in Arcgis.Using gdal_merge.py to mosaics a set of images.
    This utility will automatically mosaic a set of images. 
    All the images must be in the same coordinate system and have a matching number of bands, but they may be overlapping, and at different resolutions. 
    In areas of overlap, the last image will be copied over earlier ones.
    Ref:https://gdal.org/programs/gdal_merge.html
    
    Parameters
    ----------
    pathout : path+file name
        Output directory with file name (end with '.tif')
    pathin : path
        Path of input tif files
    file : List, optional
        The list of input tif flies. If file=0, the input file will use all tif files in 'pathin'. The default is 0.
    options : str, optional
        The options is the 'create_options' in gdal.GetDriverByName.Create(out_file, xsize, ysize, bands,band_type, create_options) 
        The default is 'COMPRESS=LZW' (Compress the output tif file using LZW method). 
    Returns
    -------
    None.
    '''
    import os
    if os.path.exists(pathin):
        if file==0:
            file_all = os.listdir(pathin)
            file = np.array([])
            for p in file_all:
                if p[-4:] == '.tif' or p[-4:] == '.TIF' :
                    file = np.append(file, p)
    else:
        raise ValueError('Path not exists')
    filein = ''
    for i in range(len(file)):
        filein = filein + file[i]+' '
    os.chdir(pathin)#change working directory so that we can find the input tif files
    path_utility = 'D:/anaconda/Scripts/gdal_merge.py'
    os.system('python {0} -co {3} -o {1} {2}'.format(path_utility,pathout,filein,options),capture_output=True, shell=True)



