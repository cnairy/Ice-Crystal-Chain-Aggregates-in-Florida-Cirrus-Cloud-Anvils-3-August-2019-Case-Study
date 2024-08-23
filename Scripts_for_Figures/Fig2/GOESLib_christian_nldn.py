#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:00:30 2023

    Syntax: NONE - This script is called by runsatscript.py

    Description:
        This script is called by runsatscript.py and creates individual lat-lon CH02 VIS GOES 
        satellite plots with NLDN Lightning data, aircraft flight track, and radar location
        overlays. This script also separates the lightning data into positive and negative
        strokes.

        NOTE: You will need to adjust the paths in this script for where your lightning data, 
        county .shp file, satellite, and aircraft track data is located. Also, line sections that say
        "between_time" needs to be adjusted to whatever time you need to look at. Currently,
        the aircraft track data is commented out, thus if you need, uncomment "Aircraft Track
        Information" section just below the NLDN lightning code section.

@author: christiannairy
"""
########################################################################
#Imports
import pandas as pd
import os
import pandas as pd
import cmasher as cmr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#########################################################################

path = '/Users/christiannairy/Documents/Research/lightning/'
data_0803_full = pd.read_csv(path + '20190803_NLDN.txt', header=None,sep="\s+", engine='python',encoding="utf8")


data_0803_full.columns =['Date', 'Time UTC', 'Lat', 'Lon', 'Mag', 'Type']

data_0803_full = data_0803_full[15886:24369]
data_0803_index = pd.to_datetime(data_0803_full['Date'] + ' ' + data_0803_full['Time UTC'])
del data_0803_full['Date']
del data_0803_full['Time UTC']

datetime = data_0803_index.to_frame(name='DateTime')

data_0803 = data_0803_full.join(datetime)
data_0803 = data_0803.set_index('DateTime')

data_0803 = data_0803.between_time('15:31:00', '15:34:00')


#Positve or Negative stroke
pos_0803 = data_0803['Mag'] > 0
positive_0803 = data_0803[pos_0803]
positive_0803_lat = positive_0803[(positive_0803['Lat'] > 28.3) & (positive_0803['Lat'] < 29.4)]
positive_0803_latlon = positive_0803_lat[(positive_0803_lat['Lon'] > -81.5) & (positive_0803_lat['Lon'] < -80.3)]

neg_0803 = data_0803['Mag'] < 0
negative_0803 = data_0803[neg_0803]
negative_0803_lat = negative_0803[(negative_0803['Lat'] > 28.3) & (negative_0803['Lat'] < 29.4)]
negative_0803_latlon = negative_0803_lat[(negative_0803_lat['Lon'] > -81.5) & (negative_0803_lat['Lon'] < -80.3)]

#Innercloud or cloud to ground
types = {}


for i, g in data_0803.groupby('Type'):
    #print 'data_' + str(i)
    #print g
    types.update({'data_0803_' + str(i) : g.reset_index(drop=True)})
    
cloud_lgn_0803 = types['data_0803_C']
ground_lgn_0803 = types['data_0803_G']


cloud_lgn_0803_C_lat = cloud_lgn_0803[(cloud_lgn_0803['Lat'] > 28.) & (cloud_lgn_0803['Lat'] < 29.0)]
cloud_lgn_0803_C_latlon = cloud_lgn_0803_C_lat[(cloud_lgn_0803_C_lat['Lon'] > -81.5) & (cloud_lgn_0803_C_lat['Lon'] < -80.1)]

ground_lgn_0803_G_lat = ground_lgn_0803[(ground_lgn_0803['Lat'] > 28.) & (ground_lgn_0803['Lat'] < 29.0)]
ground_lgn_0803_G_latlon = ground_lgn_0803_G_lat[(ground_lgn_0803_G_lat['Lon'] > -81.5) & (ground_lgn_0803_G_lat['Lon'] < -80.1)]

############################
# #Aircraft track information
# path_tit = '/Users/christiannairy/Documents/Research/20190803_1424_files/'
# data_0803_tit = pd.read_csv(path_tit + '19_08_03_14_24_55.tit', header=None,sep="\s+", engine='python',encoding="utf8")



# data_0803_tit.columns =['Name', 'Year', 'Month', 'Day', 'Hour', 'Min', 'Sec', 'Lat', 'Lon', 'Alt', 'Speed']

# data_0803_tit1 = data_0803_tit.drop(columns=['Name'])
# data_0803_tit2 = data_0803_tit1.drop(columns=['Alt'])
# data_0803_tit3 = data_0803_tit2.drop(columns=['Speed'])


# data_0803_tit3.replace(',','', regex=True, inplace=True)

# data_0803_tit3['DateTime'] = data_0803_tit3[data_0803_tit3.columns[3:6]].apply(
#     lambda x: ':'.join(x.dropna().astype(str)),
#     axis=1
# )


# data_0803_tit3_index = pd.to_datetime(data_0803_tit3['Year'] + ' ' + data_0803_tit3['Month'] + ' ' + data_0803_tit3['Day'] + ' ' + data_0803_tit3['DateTime'])

# del data_0803_tit3['Year']
# del data_0803_tit3['Month']
# del data_0803_tit3['Day']
# del data_0803_tit3['Hour']
# del data_0803_tit3['Min']
# del data_0803_tit3['Sec']
# del data_0803_tit3['DateTime']

# datetime = data_0803_tit3_index.to_frame(name='DateTime')

# data_0803_tit4 = data_0803_tit3.join(datetime)
# data_0803_tit4 = data_0803_tit4.set_index('DateTime')

# data_0803_tit4_final = pd.DataFrame(data_0803_tit4)

# data_0803_tit4_final["Lat"] = data_0803_tit4_final.Lat.astype(float)
# data_0803_tit4_final["Lon"] = data_0803_tit4_final.Lon.astype(float)

# tit = data_0803_tit4_final.between_time('15:00:00', '15:30:00')

# tit_tail_lon = pd.DataFrame(tit['Lon'].tail(1))

# tit_tail_lat = pd.DataFrame(tit['Lat'].tail(1))
############################

#Import sat script
import numpy as np
import numpy.ma as ma
import sys
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from satpy import find_files_and_readers
from satpy.scene import Scene
from satpy.writers import get_enhanced_image
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

#Flight Data
import pandas as pd
import cmasher as cmr


kmlb_lat = 28.1
kmlb_lon = -80.64

kaspr_lat = 28.7548
kaspr_lon = -80.7744
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# Set up global variables
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
datacrs = ccrs.PlateCarree()
data_dir = '/Users/christiannairy/Documents/Research/Satellite_20190803/test/'
debug = False

# - 0.64  (band 2, Red)
# - 2.25  (band 6, Cloud particle size)
# - 3.90  (band 7, Shortwave Window)
# - 6.18  (band 8, Upper-Level Water Vapor)
# - 6.95  (band 9, Mid-Level Water Vapor)
# - 7.34  (band 10, Lower-Level Water Vapor)
# - 10.35 (band 13, Clean IR Longwave Window)
channel_dict = {
    '1': {
        'name': 'Blue',
        'wavelength': 0.47
    },\
    '2': {
        'name': 'Red',
        'wavelength': 0.64
    },\
    '3': {
        'name': 'Veggie',
        'wavelength': 0.86
    },\
    '4': {
        'name': 'Cirrus',
        'wavelength': 1.38
    },\
    '5': {
        'name': 'Snow/Ice',
        'wavelength': 1.61
    },\
    '6': {
        'name': 'Cloud Particle Size',
        'wavelength': 2.25
    },\
    '7': {
        'name': 'Shortwave Window',
        'wavelength': 3.90
    },\
    '8': {
        'name': 'Upper-Level Water Vapor',
        'wavelength': 6.18
    },\
    '9': {
        'name': 'Mid-Level Water Vapor',
        'wavelength': 6.95
    },\
    '10': {
        'name': 'Lower-Level Water Vapor',
        'wavelength': 7.34
    },\
    '11': {
        'name': 'Cloud-Top Phase',
        'wavelength': 8.50
    },\
    '12': {
        'name': 'Ozone',
        'wavelength': 9.61
    },\
    '13': {
        'name': 'Clean IR Longwave Window',
        'wavelength': 10.35
    },\
    '14': {
        'name': 'IR Longwave Window',
        'wavelength': 11.20
    },\
    '15': {
        'name': 'Dirty IR Longwave Window',
        'wavelength': 12.30
    },\
    '16': {
        'name': 'CO2 Longwave Infrared',
        'wavelength': 13.30
    }
}

for key in channel_dict.keys():
    if(channel_dict[key]['wavelength'] is not None):
        channel_dict[key]['wavelength_label'] = \
            str(channel_dict[key]['wavelength']) + ' μm'
    else:
        channel_dict[key]['wavelength_label'] = ''

# Subplot label definition
def plot_subplot_label(ax, label, xval = None, yval = None, transform = None, \
        color = 'black', backgroundcolor = None, fontsize = 14, \
        location = 'upper_left'):

    if(location == 'upper_left'):
        y_lim = 0.90
        x_lim = 0.05
    elif(location == 'lower_left'):
        y_lim = 0.05
        x_lim = 0.05
    elif(location == 'upper_right'):
        y_lim = 0.90
        x_lim = 0.90
    elif(location == 'lower_right'):
        y_lim = 0.05
        x_lim = 0.90

    if(xval is None):
        xval = ax.get_xlim()[0] + (ax.get_xlim()[1] - ax.get_xlim()[0]) * x_lim
    if(yval is None):
        yval = ax.get_ylim()[0] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * y_lim
    print('Xval = ',xval, 'Yval = ',yval)

    if(transform is None):
        if(backgroundcolor is None):
            ax.text(xval,yval,label, \
                color=color, weight='bold', \
                fontsize=fontsize)
        else:
            ax.text(xval,yval,label, \
                color=color, weight='bold', \
                fontsize=fontsize, backgroundcolor = backgroundcolor)
    else:
        if(backgroundcolor is None):
            ax.text(xval,yval,label, \
                color=color, weight='bold', \
                transform = transform, fontsize=fontsize)
        else:
            ax.text(xval,yval,label, \
                color=color, weight='bold', \
                transform = transform, fontsize=fontsize, \
                backgroundcolor = backgroundcolor)

def plot_figure_text(ax, text, xval = None, yval = None, transform = None, \
        color = 'black', fontsize = 12, backgroundcolor = 'white',\
        halign = 'left'):

    if(xval is None):
        print(len(text))
        xval = ax.get_xlim()[0] + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.95
    if(yval is None):
        yval = ax.get_ylim()[0] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.05
    print('Xval = ',xval, 'Yval = ',yval)

    if(transform is None):
        ax.text(xval,yval,text, \
            color=color, weight='bold', \
            fontsize=fontsize, backgroundcolor = backgroundcolor, \
            horizontalalignment = halign)
    else:
        ax.text(xval,yval,text, \
            color=color, weight='bold', \
            transform = transform, fontsize=fontsize, \
            backgroundcolor = backgroundcolor, \
            horizontalalignment = halign)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
# Plotting functions
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

calib_dict = {
    0.64: 'reflectance',
    2.25: 'reflectance',
    3.90: 'radiance',
    6.18: 'brightness_temperature',
    6.95: 'brightness_temperature',
    7.34: 'brightness_temperature',
    10.35: 'brightness_temperature'
}   
label_dict = {
    0.64: '%',
    2.25: '%',
    3.90: 'mW m$^{-2}$ Sr$^{-1}$ (cm$^{-1}$)$^{-1}$',
    #6.18: 'mW m$^{-2}$ Sr$^{-1}$ (cm$^{-1}$)$^{-1}$',
    6.18: 'K',
    6.95: 'K',
    7.34: 'K',
    10.35: 'K'
}   
cmap_dict = {
    0.64:  'Greys_r',
    2.25:  'Greys_r',
    3.90:  'plasma',
    6.18:  'plasma',
    6.95:  'plasma',
    7.34:  'plasma',
    10.35: 'plasma'
}   
# Channel must be:
# - 0.64  (band 2, Red)
# - 2.25  (band 6, Cloud particle size)
# - 3.90  (band 7, Shortwave Window)
# - 6.18  (band 8, Upper-Level Water Vapor)
# - 6.95  (band 9, Mid-Level Water Vapor)
# - 7.34  (band 10, Lower-Level Water Vapor)
# - 10.35 (band 13, Clean IR Longwave Window)
def read_GOES_satpy(date_str, channel, zoom = True):


    # Extract the channel wavelength using the input string
    # -----------------------------------------------------
    channel = channel_dict[str(channel)]['wavelength']

    # Determine the correct GOES files associated with the date
    # ---------------------------------------------------------
    dt_date_str = datetime.strptime(date_str,"%Y%m%d%H%M")
    dt_date_str_end = dt_date_str + timedelta(minutes = 10)

    # Use the Satpy find_files_and_readers to grab the files
    # ------------------------------------------------------
    files = find_files_and_readers(start_time = dt_date_str, \
        end_time = dt_date_str_end, base_dir = data_dir, reader = 'abi_l1b')

    print(files)

    # Extract the goes true-color plot limits
    # ----------------------------------------
    #Latitude/Longitude Limits for plotting.
    #ORIGINAL
    # lat_lims = [27.5, 29.5]
    # lon_lims = [-83, -80]
    
    lat_lims = [27.9, 29.4]
    lon_lims = [-82.3, -79.4]
    
    # Use satpy (Scene) to open the file
    # ----------------------------------
    scn = Scene(reader = 'abi_l1b', filenames = files)

    # Load the desired channel data
    # -----------------------------
    scn.load([channel], calibration = [calib_dict[channel]])

    ## Set the map projection and center the data
    ## ------------------------------------------
    #my_area = scn[channel].attrs['area'].compute_optimal_bb_area({\
    #    'proj':'lcc', 'lon_0': lon_lims[0], 'lat_0': lat_lims[0], \
    #    'lat_1': lat_lims[0], 'lat_2': lat_lims[0]})
    #new_scn = scn.resample(my_area)

    ##!## Enhance the image for plotting
    ##!## ------------------------------
    ##!#var = get_enhanced_image(scn[channel]).data
    ##!#var = var.transpose('y','x','bands')

    # Zoom the image on the desired area
    # ----------------------------------
    if(zoom):
        scn = scn.crop(ll_bbox = (lon_lims[0] + 0.65, lat_lims[0], \
            lon_lims[1] - 0.65, lat_lims[1]))


    # Extract the lats, lons, and data
    # -----------------------------------------------------
    lons, lats = scn[channel].attrs['area'].get_lonlats()
    var = scn[channel].data

    # Extract the map projection from the data for plotting
    # -----------------------------------------------------
    crs = scn[channel].attrs['area'].to_cartopy_crs()

    # Extract the appropriate units
    # -----------------------------
    units = label_dict[channel]
    #units = scn[channel].units
    plabel = calib_dict[channel].title() + ' [' + units + ']'

    return var, crs, lons, lats, lat_lims, lon_lims, plabel
    #return var, crs, lat_lims, lon_lims

# channel must be an integer between 1 and 16
def plot_GOES_satpy(date_str, scan_end, channel, ax = None, var = None, crs = None, \
        lons = None, lats = None, lat_lims = None, lon_lims = None, \
        vmin = None, vmax = None, ptitle = None, plabel = None, \
        labelsize = 10, colorbar = True, zoom=True, save=True):

    dt_date_str = datetime.strptime(date_str,"%Y%m%d%H%M")
    dt_scan_end_str = datetime.strptime(scan_end,"%H%M")

    if(var is None): 
        var, crs, lons, lats, lat_lims, lon_lims, plabel = read_GOES_satpy(date_str, channel)

    # Plot the GOES data
    # ------------------
    in_ax = True 
    if(ax is None):
        in_ax = False
        plt.close('all')
        fig = plt.figure(figsize=(8,8),dpi=400)
        # ax = fig.add_subplot(1,1,1, projection=crs)
        

    ##!#ax.imshow(var.data, transform = crs, extent=(var.x[0], var.x[-1], \
    ##!#    var.y[-1], var.y[0]), vmin = vmin, vmax = vmax, origin='upper', \
    ##!#    cmap = 'Greys_r')
    #im1 = ax.imshow(var, transform = crs, vmin = vmin, vmax = vmax, \
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.pcolormesh(lons, lats, var, transform = datacrs, \
        vmin = vmin, vmax = vmax, \
        cmap = cmap_dict[channel_dict[str(channel)]['wavelength']], \
        shading = 'auto')
    ax.add_feature(cfeature.COASTLINE, linewidth = 3, color = 'k')
    #gl is gridliner -- needed to add axis
    gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=False,color='white',alpha=0,linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlabels_bottom = False
    gl.ylabels_left = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    #Original
    # gl.ylocator = mticker.FixedLocator([27.5,28, 28.5, 29,29.5])
    # gl.ylocator = mticker.FixedLocator([28.2,28.7,29.2])
    # gl.xlocator = mticker.FixedLocator([-83, -81.5, -81, -81, -80])
    
    plt1 = ax.scatter(kmlb_lon, kmlb_lat, c='g', s=350, marker='o',zorder=1)
    plt2 = ax.scatter(kaspr_lon, kaspr_lat, c='red', s=350, marker='o',zorder=2)
    plt3 = ax.scatter(cloud_lgn_0803_C_latlon.Lon, cloud_lgn_0803_C_latlon.Lat, c='deeppink', marker="x", alpha=0.6, s=100)
    plt4 = ax.scatter(ground_lgn_0803_G_latlon.Lon, ground_lgn_0803_G_latlon.Lat, c='b', marker="v", alpha=0.6, s=100)
    
    # plt5 = ax.scatter(tit_FL3.Lon, tit_FL3.Lat, c=FL3_cap_df.CIP_495_div_105_315um, cmap='viridis', s=5, zorder=1, vmin=0, vmax=1)
    # plt3 = ax.scatter(tit_FL2.Lon, tit_FL2.Lat, c=FL2_cap_df.CIP_495_div_105_315um, cmap='viridis', s=5, zorder=1, vmin=0, vmax=1)

    # plt2 = ax.scatter(peak_lon, peak_lat, c='r', s=5, zorder=1)

    # cbar = plt.colorbar(plt2, ax=ax)
    # cbar.set_label(r'$RCAC_{N - C}$',fontsize=14)
    
    if(colorbar):
        print('hello')
        # cbar = plt.colorbar(im1, ax = ax, pad = 0.03, fraction = 0.052, \
        #     extend = 'both')
        # cbar.set_label(plabel.replace('_',' '), size = labelsize, weight = 'bold')
    # Zoom in the figure if desired
    # -----------------------------
    if(zoom):
    ##!#    ax.set_extent([lon_lims[0]+0.55,lon_lims[1]-0.6,lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
        zoom_add = '_zoom'
    else:
        zoom_add = ''

    if(ptitle is None):
        ax.set_title('GOES-16\n'+dt_date_str.strftime('%Y-%m-%d %H:%M ') + '-' + dt_scan_end_str.strftime(' %H:%M') + ' ' + 'UTC')
        
    else:
        ax.set_title(ptitle)
        
    

    if(not in_ax): 
        print('here')
        fig.tight_layout()
        if(save):
            outname = 'goes_' + date_str + zoom_add + '.png'
            plt.savefig(outname,dpi=300)
            print("Saved image",outname)
        else:
            plt.show()
            

def plot_GOES_satpy_6panel(date_str, ch1, ch2, ch3, ch4, ch5, ch6, \
        zoom = True, save =False):
    dt_date_str = datetime.strptime(date_str,"%Y%m%d%H%M")

    plt.close('all')
    fig1 = plt.figure(figsize = (10,6))
    var0, crs0, lons0, lats0, lat_lims, lon_lims, plabel0 = read_GOES_satpy(date_str, ch1)
    var1, crs1, lons1, lats1, lat_lims, lon_lims, plabel1 = read_GOES_satpy(date_str, ch2)
    var2, crs2, lons2, lats2, lat_lims, lon_lims, plabel2 = read_GOES_satpy(date_str, ch3)
    var3, crs3, lons3, lats3, lat_lims, lon_lims, plabel3 = read_GOES_satpy(date_str, ch4)
    var4, crs4, lons4, lats4, lat_lims, lon_lims, plabel4 = read_GOES_satpy(date_str, ch5)
    var5, crs5, lons5, lats5, lat_lims, lon_lims, plabel5 = read_GOES_satpy(date_str, ch6)

    ax0 = fig1.add_subplot(2,3,1, projection = crs0)
    ax1 = fig1.add_subplot(2,3,2, projection = crs1)
    ax2 = fig1.add_subplot(2,3,3, projection = crs2)
    ax3 = fig1.add_subplot(2,3,4, projection = crs3)
    ax4 = fig1.add_subplot(2,3,5, projection = crs4)
    ax5 = fig1.add_subplot(2,3,6, projection = crs5)

    ##!#ax1.set_title('GOES-17 Band ' + str(ch2) + '\n' + \
    ##!#    channel_dict[str(ch2)]['name'] + '\n' + \
    labelsize = 11
    font_size = 10
    plot_GOES_satpy(date_str, ch1, ax = ax0, var = var0, crs = crs0, \
        lons = lons0, lats = lats0, lat_lims = lat_lims, lon_lims = lon_lims, \
        vmin = None, vmax = None, ptitle = '', plabel = plabel0, \
        colorbar = True, labelsize = labelsize + 1, zoom=True,save=False)
    plot_GOES_satpy(date_str, ch2, ax = ax1, var = var1, crs = crs0, \
        lons = lons1, lats = lats1, lat_lims = lat_lims, lon_lims = lon_lims, \
        vmin = None, vmax = 30., ptitle = '', plabel = plabel1, \
        colorbar = True, labelsize = labelsize + 1, zoom=True,save=False)
    plot_GOES_satpy(date_str, ch3, ax = ax2, var = var2, crs = crs0, \
        lons = lons2, lats = lats2, lat_lims = lat_lims, lon_lims = lon_lims, \
        vmin = 270, vmax = 330, ptitle = '', plabel = plabel2, \
        colorbar = True, labelsize = labelsize + 1, zoom=True,save=False)
    plot_GOES_satpy(date_str, ch4, ax = ax3, var = var3, crs = crs0, \
        lons = lons3, lats = lats3, lat_lims = lat_lims, lon_lims = lon_lims, \
        vmin = None, vmax = None, ptitle = '', plabel = plabel3, \
        colorbar = True, labelsize = labelsize, zoom=True,save=False)
    plot_GOES_satpy(date_str, ch5, ax = ax4, var = var4, crs = crs0, \
        lons = lons4, lats = lats4, lat_lims = lat_lims, lon_lims = lon_lims, \
        vmin = None, vmax = None, ptitle = '', plabel = plabel4, \
        colorbar = True, labelsize = labelsize, zoom=True,save=False)
    plot_GOES_satpy(date_str, ch6, ax = ax5, var = var5, crs = crs0, \
        lons = lons5, lats = lats5, lat_lims = lat_lims, lon_lims = lon_lims, \
        vmin = None, vmax = None, ptitle = '', plabel = plabel5, \
        colorbar = True, labelsize = labelsize, zoom=True,save=False)

    plot_figure_text(ax0, 'GOES-16 ' + \
        str(channel_dict[str(ch1)]['wavelength']) + ' μm', \
        xval = None, yval = None, transform = None, \
        color = 'red', fontsize = font_size, backgroundcolor = 'white', \
        halign = 'right')
    plot_figure_text(ax1, 'GOES-16 ' + \
        str(channel_dict[str(ch2)]['wavelength']) + ' μm', \
        xval = None, yval = None, transform = None, \
        color = 'red', fontsize = font_size, backgroundcolor = 'white', \
        halign = 'right')
    plot_figure_text(ax2, 'GOES-16 ' + \
        str(channel_dict[str(ch3)]['wavelength']) + ' μm', \
        xval = None, yval = None, transform = None, \
        color = 'red', fontsize = font_size, backgroundcolor = 'white', \
        halign = 'right')
    plot_figure_text(ax3, 'GOES-16 ' + \
        str(channel_dict[str(ch4)]['wavelength']) + ' μm', \
        xval = None, yval = None, transform = None, \
        color = 'red', fontsize = font_size, backgroundcolor = 'white', \
        halign = 'right')
    plot_figure_text(ax4, 'GOES-16 ' + \
        str(channel_dict[str(ch5)]['wavelength']) + ' μm', \
        xval = None, yval = None, transform = None, \
        color = 'red', fontsize = font_size, backgroundcolor = 'white', \
        halign = 'right')
    plot_figure_text(ax5, 'GOES-16 ' + \
        str(channel_dict[str(ch6)]['wavelength']) + ' μm', \
        xval = None, yval = None, transform = None, \
        color = 'red', fontsize = font_size, backgroundcolor = 'white', \
        halign = 'right')

    plot_subplot_label(ax0,  '(a)', backgroundcolor = 'white', fontsize = font_size)
    plot_subplot_label(ax1,  '(b)', backgroundcolor = 'white', fontsize = font_size)
    plot_subplot_label(ax2,  '(c)', backgroundcolor = 'white', fontsize = font_size)
    plot_subplot_label(ax3,  '(d)', backgroundcolor = 'white', fontsize = font_size)
    plot_subplot_label(ax4,  '(e)', backgroundcolor = 'white', fontsize = font_size)
    plot_subplot_label(ax5,  '(f)', backgroundcolor = 'white', fontsize = font_size)

    lon_stn = -120.7605
    lat_stn = 41.2098

    # Zoom in the figure if desired
    # -----------------------------
    if(zoom):
    ##!#    ax0.set_extent([lon_lims[0],lon_lims[1],lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
    ##!#    ax1.set_extent([lon_lims[0],lon_lims[1],lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
    ##!#    ax2.set_extent([lon_lims[0],lon_lims[1],lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
    ##!#    ax3.set_extent([lon_lims[0],lon_lims[1],lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
    ##!#    ax4.set_extent([lon_lims[0],lon_lims[1],lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
    ##!#    ax5.set_extent([lon_lims[0],lon_lims[1],lat_lims[0],lat_lims[1]],\
    ##!#                   crs = ccrs.PlateCarree())
        zoom_add = '_zoom'
    else:
        zoom_add = ''

    fig1.tight_layout()

    if(save):
        outname = 'goes16_'+date_str+'_6panel.png'
        fig1.savefig(outname, dpi = 300)
        print('Saved image', outname)
    else:
        plt.show()



