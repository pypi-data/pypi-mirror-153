import gloce.func
import gloce.area
import gloce.interpolation
import gloce.resample
#----func----
running_mean = gloce.func.running_mean
nanravel = gloce.func.nanravel
listdir = gloce.func.listdir
nanaverage = gloce.func.nanaverage
arrayinfo = gloce.func.arrayinfo
fslice = gloce.func.fslice
exclude_outlier = gloce.func.exclude_outlier
r2a = gloce.func.r2a
n2a = gloce.func.n2a
func_to_landpoint = gloce.func.func_to_landpoint
func_to_ilatilon = gloce.func.func_to_ilatilon
func_to_latlon = gloce.func.func_to_latlon
#------------

#----resample----
downscaling = gloce.resample.downscaling
upscaling = gloce.resample.upscaling
#----------------

#----area----
globalarea = gloce.area.globalarea
gridarea = gloce.area.gridarea
#------------

#----interpolation----
interpolation_map = gloce.interpolation.interpolation_map
interpolation_time = gloce.interpolation.interpolation_time
#---------------------