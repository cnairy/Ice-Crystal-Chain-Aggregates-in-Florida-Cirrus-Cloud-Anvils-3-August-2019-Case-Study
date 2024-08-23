"""
Syntax: ./5-panel_CIP_Ez_20220308.py

Purpose:
    Generates Aricraft track plots, and CIP/Ez/RATIOcn time-series plots.

Author: @christian.nairy
"""


#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from datetime import datetime, timedelta
from dateutil import parser
import matplotlib.ticker as mticker
import cmasher as cmr
from sklearn.metrics import r2_score
from scipy.stats import linregress


#%%
###########################
###########################
#Aircraft track information
path = '/Users/christiannairy/Documents/Research/20190803_1424_files/'
data_0803_tit = pd.read_csv(path + '19_08_03_14_24_55.tit', header=None,sep="\s+", engine='python',encoding="utf8")



data_0803_tit.columns =['Name', 'Year', 'Month', 'Day', 'Hour', 'Min', 'Sec', 'Lat', 'Lon', 'Alt', 'Speed']

data_0803_tit1 = data_0803_tit.drop(columns=['Name'])
data_0803_tit2 = data_0803_tit1.drop(columns=['Alt'])
data_0803_tit3 = data_0803_tit2.drop(columns=['Speed'])


data_0803_tit3.replace(',','', regex=True, inplace=True)

data_0803_tit3['DateTime'] = data_0803_tit3[data_0803_tit3.columns[3:6]].apply(
    lambda x: ':'.join(x.dropna().astype(str)),
    axis=1
)


data_0803_tit3_index = pd.to_datetime(data_0803_tit3['Year'] + ' ' + data_0803_tit3['Month'] + ' ' + data_0803_tit3['Day'] + ' ' + data_0803_tit3['DateTime'])

del data_0803_tit3['Year']
del data_0803_tit3['Month']
del data_0803_tit3['Day']
del data_0803_tit3['Hour']
del data_0803_tit3['Min']
del data_0803_tit3['Sec']
del data_0803_tit3['DateTime']

datetime = data_0803_tit3_index.to_frame(name='DateTime')

data_0803_tit4 = data_0803_tit3.join(datetime)
data_0803_tit4 = data_0803_tit4.set_index('DateTime')

data_0803_tit4_final = pd.DataFrame(data_0803_tit4)

data_0803_tit4_final["Lat"] = data_0803_tit4_final.Lat.astype(float)
data_0803_tit4_final["Lon"] = data_0803_tit4_final.Lon.astype(float)

tit_FL1 = data_0803_tit4_final.between_time('15:51:15', '16:01:00')
tit_FL2 = data_0803_tit4_final.between_time('16:02:00', '16:07:00')
tit_FL3 = data_0803_tit4_final.between_time('16:09:00', '16:17:00')
tit_FL4 = data_0803_tit4_final.between_time('16:21:30', '16:27:00')
tit_FL5 = data_0803_tit4_final.between_time('16:40:00', '16:46:00')

#Need to make datetime into a column where we can calculate sfm
tit_FL1['date_and_time'] = tit_FL1.index
tit_FL1['time']=((tit_FL1['date_and_time'].dt.hour*60+tit_FL1['date_and_time'].dt.minute)*60 + tit_FL1['date_and_time'].dt.second)
del tit_FL1['date_and_time']

tit_FL2['date_and_time'] = tit_FL2.index
tit_FL2['time']=((tit_FL2['date_and_time'].dt.hour*60+tit_FL2['date_and_time'].dt.minute)*60 + tit_FL2['date_and_time'].dt.second)
del tit_FL2['date_and_time']

tit_FL3['date_and_time'] = tit_FL3.index
tit_FL3['time']=((tit_FL3['date_and_time'].dt.hour*60+tit_FL3['date_and_time'].dt.minute)*60 + tit_FL3['date_and_time'].dt.second)
del tit_FL3['date_and_time']

tit_FL4['date_and_time'] = tit_FL4.index
tit_FL4['time']=((tit_FL4['date_and_time'].dt.hour*60+tit_FL4['date_and_time'].dt.minute)*60 + tit_FL4['date_and_time'].dt.second)
del tit_FL4['date_and_time']

tit_FL5['date_and_time'] = tit_FL5.index
tit_FL5['time']=((tit_FL5['date_and_time'].dt.hour*60+tit_FL5['date_and_time'].dt.minute)*60 + tit_FL5['date_and_time'].dt.second)
del tit_FL5['date_and_time']

#%%
#############################
#############################
#Load in NLDN data
path_NLDN = '/Users/christiannairy/Documents/Research/lightning/'
data_0803_full = pd.read_csv(path_NLDN + '20190803_NLDN.txt', header=None,sep="\s+", engine='python',encoding="utf8")

data_0803_full.columns =['Date', 'Time UTC', 'Lat', 'Lon', 'Mag', 'Type']

data_0803_full = data_0803_full[15886:24369]
data_0803_index = pd.to_datetime(data_0803_full['Date'] + ' ' + data_0803_full['Time UTC'])
del data_0803_full['Date']

datetime = data_0803_index.to_frame(name='DateTime')
data_0803 = data_0803_full.join(datetime)
data_0803 = data_0803.set_index('DateTime')

data_0803 = data_0803.between_time('14:45:00', '16:30:00')

#Separate CG and CC lightning into their own arrays
types = {}

for i, g in data_0803.groupby('Type'):
    #print 'data_' + str(i)
    #print g
    types.update({'data_0803_' + str(i) : g.reset_index(drop=True)})
    
cloud_lgn_0803 = types['data_0803_C']
ground_lgn_0803 = types['data_0803_G']


cloud_lgn_0803_C_lat = cloud_lgn_0803[(cloud_lgn_0803['Lat'] > 27.9) & (cloud_lgn_0803['Lat'] < 29.)]
cloud_lgn_0803_C_latlon = cloud_lgn_0803_C_lat[(cloud_lgn_0803_C_lat['Lon'] > -82) & (cloud_lgn_0803_C_lat['Lon'] < -80.3)]
bad_data_C = cloud_lgn_0803_C_latlon[(cloud_lgn_0803_C_latlon['Lat'] < 28.2) & (cloud_lgn_0803_C_latlon['Lat'] > 28) & (cloud_lgn_0803_C_latlon['Lon'] > -80.64) & (cloud_lgn_0803_C_latlon['Lon'] < -80)].index
cloud_lgn_0803_C_latlon.drop(bad_data_C, inplace=True)

ground_lgn_0803_G_lat = ground_lgn_0803[(ground_lgn_0803['Lat'] > 27.9) & (ground_lgn_0803['Lat'] < 29.)]
ground_lgn_0803_G_latlon = ground_lgn_0803_G_lat[(ground_lgn_0803_G_lat['Lon'] > -82) & (ground_lgn_0803_G_lat['Lon'] < -80.3)]
bad_data_G = ground_lgn_0803_G_latlon[(ground_lgn_0803_G_latlon['Lat'] < 28.2) & (ground_lgn_0803_G_latlon['Lat'] > 28) & (ground_lgn_0803_G_latlon['Lon'] > -80.64) & (ground_lgn_0803_G_latlon['Lon'] < -80)].index
ground_lgn_0803_G_latlon.drop(bad_data_G, inplace=True)

#Count the # of strokes
cloud_stroke_count = cloud_lgn_0803_C_latlon.Lat.count()
cloud_stroke_count = str(cloud_stroke_count)

ground_stroke_count = ground_lgn_0803_G_latlon.Lat.count()
ground_stroke_count = str(ground_stroke_count)

#Remove millisectonds from datetime
ground_lgn_0803_G_latlon['Time UTC'] = ground_lgn_0803_G_latlon['Time UTC'].astype('datetime64[s]')
ground_lgn_0803_G_latlon['Dates'] = pd.to_datetime(ground_lgn_0803_G_latlon['Time UTC']).dt.date
ground_lgn_0803_G_latlon['Time'] = pd.to_datetime(ground_lgn_0803_G_latlon['Time UTC']).dt.time
del ground_lgn_0803_G_latlon['Dates']
del ground_lgn_0803_G_latlon['Time UTC']

cloud_lgn_0803_C_latlon['Time UTC'] = cloud_lgn_0803_C_latlon['Time UTC'].astype('datetime64[s]')
cloud_lgn_0803_C_latlon['Dates'] = pd.to_datetime(cloud_lgn_0803_C_latlon['Time UTC']).dt.date
cloud_lgn_0803_C_latlon['Time'] = pd.to_datetime(cloud_lgn_0803_C_latlon['Time UTC']).dt.time
del cloud_lgn_0803_C_latlon['Dates']
del cloud_lgn_0803_C_latlon['Time UTC']

#Shift time column (last) to first column
cols = list(ground_lgn_0803_G_latlon.columns)
cols = [cols[-1]] + cols[:-1]
ground_lgn_0803_G_latlon = ground_lgn_0803_G_latlon[cols]

#convert time column to string
ground_lgn_0803_G_latlon['Time'] = ground_lgn_0803_G_latlon['Time'].astype(str)
cloud_lgn_0803_C_latlon['Time'] = cloud_lgn_0803_C_latlon['Time'].astype(str)

cols = list(cloud_lgn_0803_C_latlon.columns)
cols = [cols[-1]] + cols[:-1]
cloud_lgn_0803_C_latlon = cloud_lgn_0803_C_latlon[cols]


#Fill in empty time gaps (1sec frequency) with NaN's
max_dt_G = parser.parse(max(ground_lgn_0803_G_latlon['Time']))
min_dt_G = parser.parse(min(ground_lgn_0803_G_latlon['Time']))
max_dt_C = parser.parse(max(cloud_lgn_0803_C_latlon['Time']))
min_dt_C = parser.parse(min(cloud_lgn_0803_C_latlon['Time']))

dt_range_G = []
dt_range_C = []
while min_dt_G <= max_dt_G:
  dt_range_G.append(min_dt_G.strftime("%H:%M:%S"))
  min_dt_G += timedelta(seconds=1)

while min_dt_C <= max_dt_C:
  dt_range_C.append(min_dt_C.strftime("%H:%M:%S"))
  min_dt_C += timedelta(seconds=1)

complete_df_G = pd.DataFrame({'Time': dt_range_G})
ground_lgn_0803_G_latlon = complete_df_G.merge(ground_lgn_0803_G_latlon, how='left', on='Time')

complete_df_C = pd.DataFrame({'Time': dt_range_C})
cloud_lgn_0803_C_latlon = complete_df_C.merge(cloud_lgn_0803_C_latlon, how='left', on='Time')



#%%
###########################
###########################
#Load in electric field data

E_cap = np.loadtxt(path + '19_08_03_14_24_55.cap.20220306', skiprows = 54, usecols = (0,30,31,32,33,34))

column_names = ['sfm','Ex','Ey','Ez','Eq','Emag']

E_cap_df = pd.DataFrame(E_cap,columns=column_names)

E_cap_df[E_cap_df > 100000] = np.nan

E_cap_df['Eq/Emag'] = (E_cap_df['Eq'] / E_cap_df['Emag'])

FL1_E_cap_df = E_cap_df[5176:5762]
FL2_E_cap_df = E_cap_df[5821:6122]
FL3_E_cap_df = E_cap_df[6241:6722]
FL4_E_cap_df = E_cap_df[6991:7322]
FL5_E_cap_df = E_cap_df[8101:8462]

#convert sfm to UTC
times = FL1_E_cap_df['sfm'].to_numpy()
# times = times.astype(int)

#Fill nan values by taking the mean of the past 5 points
FL1_E_cap_df['Ez'] = FL1_E_cap_df['Ez'].fillna(FL1_E_cap_df['Ez'].rolling(6,min_periods=1).mean())
FL2_E_cap_df['Ez'] = FL2_E_cap_df['Ez'].fillna(FL2_E_cap_df['Ez'].rolling(6,min_periods=1).mean())
FL3_E_cap_df['Ez'] = FL3_E_cap_df['Ez'].fillna(FL3_E_cap_df['Ez'].rolling(6,min_periods=1).mean())
FL4_E_cap_df['Ez'] = FL4_E_cap_df['Ez'].fillna(FL4_E_cap_df['Ez'].rolling(6,min_periods=1).mean())



#Calculate 5 point moving average
FL1_E_cap_df[ 'Ez_twenty_pt_rolling_avg' ] = FL1_E_cap_df.Ez.rolling(20,center=True).mean()
FL2_E_cap_df[ 'Ez_twenty_pt_rolling_avg' ] = FL2_E_cap_df.Ez.rolling(20,center=True).mean()
FL3_E_cap_df[ 'Ez_twenty_pt_rolling_avg' ] = FL3_E_cap_df.Ez.rolling(20,center=True).mean()
FL4_E_cap_df[ 'Ez_twenty_pt_rolling_avg' ] = FL4_E_cap_df.Ez.rolling(20,center=True).mean()

#%%
###########################
###########################
#KMLB Radar Location (lat/lon)
kmlb_lat = 28.1
kmlb_lon = -80.64
#KASPR/CPR-HD location
kaspr_lat = 28.7548
kaspr_lon = -80.7744

#Plotting
reader = shpreader.Reader(path + 'countyl010g_shp_nt00964/countyl010g.shp')
counties = list(reader.geometries())
COUNTIES = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())

fig = plt.figure(figsize=(10, 6),dpi=200)
ax2 = plt.axes(projection=ccrs.PlateCarree())
ax2.add_feature(cfeature.LAND.with_scale('50m'), facecolor='gray')
ax2.add_feature(cfeature.OCEAN.with_scale('50m'))
ax2.add_feature(cfeature.LAKES.with_scale('50m'))
ax2.add_feature(COUNTIES, facecolor='none', edgecolor='white', alpha=0.5)
ax2.coastlines('50m')
ax2.set_extent([-81.45, -80.5, 28.05, 29.15])

#Uncomment these lines out for figure axis information
# ax2.text(-0.20, 0.51, 'Latitude', va='bottom', ha='center',
#         rotation='vertical', rotation_mode='anchor',
#         transform=ax2.transAxes, fontsize = 14)
# ax2.text(0.47, -0.1, 'Longitude', va='bottom', ha='center',
#         rotation='horizontal', rotation_mode='anchor',
#         transform=ax2.transAxes, fontsize = 14)
# ax2.text(0.01,-0.17, 'Total # of Cloud-to-Ground Strokes = ' + ground_stroke_count,va='bottom', ha='left',
#         rotation='horizontal', rotation_mode='anchor',
#         transform=ax2.transAxes, fontsize = 12)
# ax2.text(0.01,-0.22, 'Total # of Cloud-to-Cloud/Intra-Cloud Strokes = ' + cloud_stroke_count,va='bottom', ha='left',
#         rotation='horizontal', rotation_mode='anchor',
#         transform=ax2.transAxes, fontsize = 12)

#gl is gridliner -- needed to add axis
gl = ax2.gridlines(crs=ccrs.PlateCarree(),draw_labels=False,color='white',alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabels_bottom = True
gl.ylabels_left = False
gl.ylocator = mticker.FixedLocator([28,28.1, 28.6, 29.1,29.3])
gl.xlocator = mticker.FixedLocator([-81.6, -81.4, -81, -80.6, -80.4])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# gl.xlabel_style = {'size': 14}
# gl.ylabel_style = {'size': 14}

cmap1 = plt.get_cmap('spring_r')
cmap2 = plt.get_cmap('summer')
cmap3 = plt.get_cmap('cool_r')
cmap4 = plt.get_cmap('winter_r')
# cmap5 = plt.get_cmap('copper')

#Segment the colorbar from the NLDN plot for the individual flight legs
cmap_FL1 = cmr.get_sub_cmap('gist_rainbow', 0.616, 0.714, N=100)
cmap_FL2 = cmr.get_sub_cmap('gist_rainbow', 0.725, 0.775, N=100)
cmap_FL3 = cmr.get_sub_cmap('gist_rainbow', 0.795, 0.875, N=100)
cmap_FL4 = cmr.get_sub_cmap('gist_rainbow', 0.919, 0.974, N=100)

#plot lightning stuff

N_TICKS = 5
cmap = plt.get_cmap('gist_rainbow')
# cmap = cmr.get_sub_cmap('cmr.tropical',0.0,1.0)
# smap = ax2.scatter(cloud_lgn_0803_C_latlon.Lon, cloud_lgn_0803_C_latlon.Lat, c=cloud_lgn_0803_C_latlon.index,
#                   edgecolors='none', cmap=cmap, marker="o", label='NLDN IC Strokes', alpha=0.5)
smap = ax2.scatter(ground_lgn_0803_G_latlon.Lon, ground_lgn_0803_G_latlon.Lat, c=ground_lgn_0803_G_latlon.index,
                  edgecolors='none', cmap=cmap, marker="o", label='NLDN CG Strokes', alpha=0.5)

# indexes = [cloud_lgn_0803_C_latlon.index[i] for i in np.linspace(0,cloud_lgn_0803_C_latlon.shape[0]-1,N_TICKS).astype(int)] 
indexes = [ground_lgn_0803_G_latlon.index[i] for i in np.linspace(0,ground_lgn_0803_G_latlon.shape[0]-1,N_TICKS).astype(int)] 

#Uncomment these following lines if you want to display the color bar.
# cb = fig.colorbar(smap, orientation='horizontal',
#                   ticks= ground_lgn_0803_G_latlon.loc[indexes].index.astype(int),pad=0.1)

# cb.ax.set_xticklabels(['14:50','15:15','15:40','16:05','16:30'])
# cb.ax.set_xticklabels(cb.ax.get_xticklabels(), rotation='horizontal')
# cb.set_label('Time [UTC]',fontsize = 16)
# cb.ax.tick_params(labelsize=16)

#Plot Flight Legs
ax2.scatter(kmlb_lon, kmlb_lat, c='g', s=150, marker='o', label='KMLB')
ax2.scatter(kaspr_lon, kaspr_lat, c='k', s=150, marker='o', label='CPR-HD')
# plt.legend(bbox_to_anchor=(0.91,-0.1), loc='lower right',bbox_transform=fig.transFigure, ncol=2, fontsize = 16, facecolor='white')
ax2.scatter(tit_FL1.Lon, tit_FL1.Lat, c=tit_FL1.time, cmap=cmap_FL1, marker='.', s=1,label='Aircraft Flight Track FL1', alpha=0.8)
ax2.scatter(tit_FL2.Lon, tit_FL2.Lat, c=tit_FL2.time, cmap=cmap_FL2, marker='.',s=1,label='Aircraft Flight Track FL2', alpha=0.8)
ax2.scatter(tit_FL3.Lon, tit_FL3.Lat, c=tit_FL3.time, cmap=cmap_FL3, marker='.',s=1,label='Aircraft Flight Track FL3', alpha=0.8)
ax2.scatter(tit_FL4.Lon, tit_FL4.Lat, c=tit_FL4.time, cmap=cmap_FL4, marker='.',s=1,label='Aircraft Flight Track FL4', alpha=0.8)

#%%
#Next work on the science data (CIP>495um on y; distance from core on x with color bar as time.)
#load in CIP > 495um data
#Also load in electric field data, distance from core, and chain agg/confidence data

cap = np.loadtxt(path + '19_08_03_14_24_55.cap.230617.new', skiprows = 58, usecols=(0,28,29,30,31,32,33,34,35,36,37,38))

#convert numpy array to pandas DataFrame
cap_df = pd.DataFrame(cap, columns=['sfm','chainagg','confidence','Ex','Ey','Ez','Eq','Emag','DFC','CIP_495um','CIP_105um','CIP_105_315um'])



#%%
#turn null values to NaN
cap_df[cap_df == 0.0] = np.nan
cap_df[cap_df['CIP_495um'] < 10] = np.nan
cap_df[cap_df['CIP_105um'] < 10] = np.nan
cap_df[cap_df['CIP_105_315um'] < 10] = np.nan

#Turn CIP #/m^3 to #/cm^3
cap_df['CIP_495um'] = cap_df['CIP_495um'] / 1e6
cap_df['CIP_105um'] = cap_df['CIP_105um'] / 1e6
cap_df['CIP_105_315um'] = cap_df['CIP_105_315um'] / 1e6

cap_df['CIP_495_div_105um'] = cap_df['CIP_495um'] / cap_df['CIP_105um']
cap_df['CIP_495_div_105_315um'] = cap_df['CIP_495um'] / cap_df['CIP_105_315um']

#Define the Flight Legs

#THESE ARE THE ACTUAL (EXACT) FLIGHT LEGS.
FL1_cap_df = cap_df[5176:5762]
FL2_cap_df = cap_df[5821:6122]
FL3_cap_df = cap_df[6241:6722]
FL4_cap_df = cap_df[6991:7322]


#Calculate 20 point moving average for CIP105um
FL1_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL1_cap_df.CIP_105um.rolling(20,center=True).mean()
FL2_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL2_cap_df.CIP_105um.rolling(20,center=True).mean()
FL3_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL3_cap_df.CIP_105um.rolling(20,center=True).mean()
FL4_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL4_cap_df.CIP_105um.rolling(20,center=True).mean()

#Calculate 20 point moving average for CIP495um
FL1_cap_df[ 'twenty_pt_rolling_avg_495' ] = FL1_cap_df.CIP_495um.rolling(20,center=True).mean()
FL2_cap_df[ 'twenty_pt_rolling_avg_495' ] = FL2_cap_df.CIP_495um.rolling(20,center=True).mean()
FL3_cap_df[ 'twenty_pt_rolling_avg_495' ] = FL3_cap_df.CIP_495um.rolling(20,center=True).mean()
FL4_cap_df[ 'twenty_pt_rolling_avg_495' ] = FL4_cap_df.CIP_495um.rolling(20,center=True).mean()

#Calculate 20 point moving average for CIP105-315um
FL1_cap_df[ 'twenty_pt_rolling_avg_105_315' ] = FL1_cap_df.CIP_105_315um.rolling(20,center=True).mean()
FL2_cap_df[ 'twenty_pt_rolling_avg_105_315' ] = FL2_cap_df.CIP_105_315um.rolling(20,center=True).mean()
FL3_cap_df[ 'twenty_pt_rolling_avg_105_315' ] = FL3_cap_df.CIP_105_315um.rolling(20,center=True).mean()
FL4_cap_df[ 'twenty_pt_rolling_avg_105_315' ] = FL4_cap_df.CIP_105_315um.rolling(20,center=True).mean()

#Calculate 20 point moving average for CIP95um divided by CIP105um
FL1_cap_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL1_cap_df.CIP_495_div_105um.rolling(20,center=True).mean()
FL2_cap_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL2_cap_df.CIP_495_div_105um.rolling(20,center=True).mean()
FL3_cap_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL3_cap_df.CIP_495_div_105um.rolling(20,center=True).mean()
FL4_cap_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL4_cap_df.CIP_495_div_105um.rolling(20,center=True).mean()

#Calculate 20 point moving average for CIP95um divided by CIP105-315um
FL1_cap_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL1_cap_df.CIP_495_div_105_315um.rolling(20,center=True).mean()
FL2_cap_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL2_cap_df.CIP_495_div_105_315um.rolling(20,center=True).mean()
FL3_cap_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL3_cap_df.CIP_495_div_105_315um.rolling(20,center=True).mean()
FL4_cap_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL4_cap_df.CIP_495_div_105_315um.rolling(20,center=True).mean()

#%%
#Do some math for some Statistics
#for CIP gt105um
FL1_CIP_gt105um_max = FL1_cap_df['CIP_105um'].max()
FL1_CIP_gt105um_min = FL1_cap_df['CIP_105um'].min()
FL1_CIP_gt105um_avg = FL1_cap_df['CIP_105um'].mean()

FL2_CIP_gt105um_max = FL2_cap_df['CIP_105um'].max()
FL2_CIP_gt105um_min = FL2_cap_df['CIP_105um'].min()
FL2_CIP_gt105um_avg = FL2_cap_df['CIP_105um'].mean()

FL3_CIP_gt105um_max = FL3_cap_df['CIP_105um'].max()
FL3_CIP_gt105um_min = FL3_cap_df['CIP_105um'].min()
FL3_CIP_gt105um_avg = FL3_cap_df['CIP_105um'].mean()

FL4_CIP_gt105um_max = FL4_cap_df['CIP_105um'].max()
FL4_CIP_gt105um_min = FL4_cap_df['CIP_105um'].min()
FL4_CIP_gt105um_avg = FL4_cap_df['CIP_105um'].mean()

#for CIP gt495um
FL1_CIP_gt495um_max = FL1_cap_df['CIP_495um'].max()
FL1_CIP_gt495um_min = FL1_cap_df['CIP_495um'].min()
FL1_CIP_gt495um_avg = FL1_cap_df['CIP_495um'].mean()

FL2_CIP_gt495um_max = FL2_cap_df['CIP_495um'].max()
FL2_CIP_gt495um_min = FL2_cap_df['CIP_495um'].min()
FL2_CIP_gt495um_avg = FL2_cap_df['CIP_495um'].mean()

FL3_CIP_gt495um_max = FL3_cap_df['CIP_495um'].max()
FL3_CIP_gt495um_min = FL3_cap_df['CIP_495um'].min()
FL3_CIP_gt495um_avg = FL3_cap_df['CIP_495um'].mean()

FL4_CIP_gt495um_max = FL4_cap_df['CIP_495um'].max()
FL4_CIP_gt495um_min = FL4_cap_df['CIP_495um'].min()
FL4_CIP_gt495um_avg = FL4_cap_df['CIP_495um'].mean()


#%%
##############################################################################
#Begin Plotting for extended FL plots for CIP data
#Concentration of particles > 495 um
# FL1_cap_df[FL1_cap_df['CIP_495um'] < 1e-4] = np.nan
# FL1_cap_df.dropna(inplace=True)
FL1_cap_df['b'] = np.log10(FL1_cap_df.twenty_pt_rolling_avg_495)


########## FL1 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL1_cap_df.DFC, FL1_cap_df.CIP_495um, c=FL1_cap_df.sfm, s=25, marker='o', cmap=cmap_FL1)
plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3)
#plot linear trendline
coefs = np.polyfit(FL1_cap_df.DFC, FL1_cap_df.b, 1)
fit_coefs = np.poly1d(coefs)
plt.plot(FL1_cap_df.DFC, 10**fit_coefs(FL1_cap_df.DFC), color='red', linestyle='--')
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel('Concentration > 495 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1],fontsize=21)
plt.ylim(1e-4,1e-1)
plt.title('FL1 -- 15:51:15 - 16:01:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL2 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL2_cap_df.DFC, FL2_cap_df.CIP_495um, c=FL2_cap_df.sfm, s=25, marker='o', cmap=cmap_FL2)
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
plt.ylabel('Concentration > 495 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1],fontsize=21)
plt.ylim(1e-4,1e-1)
# FL2_label1 = 'Flight'
# FL2_label2 = 'Leg'
# FL2_label3 = '2'
# FL2_label4 = '[FL2]'
# plt.title(r"$\bf{" + str(FL2_label1) + "}$" ' ' r"$\bf{" + str(FL2_label2) + "}$"
#           ' ' r"$\bf{" + str(FL2_label3) + "}$" ' ' r"$\bf{" + str(FL2_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL2 -- 16:02:00 - 16:07:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL2_cap_df['sfm'].min(), FL2_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:02:00", "16:03:40", "16:05:20", "16:07:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL3 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.rcParams['axes.xmargin'] = 0
# plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL3_cap_df.DFC, FL3_cap_df.CIP_495um, c=FL3_cap_df.sfm, s=25, marker='o', cmap=cmap_FL3)
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.ylim(250,1500)
plt.ylabel('Concentration > 495 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1],fontsize=21)
plt.ylim(1e-4,1e-1)
# plt.yticks([250,500,750,1000,1250,1500],fontsize=21)
# FL3_label1 = 'Flight'
# FL3_label2 = 'Leg'
# FL3_label3 = '3'
# FL3_label4 = '[FL3]'
# plt.title(r"$\bf{" + str(FL3_label1) + "}$" ' ' r"$\bf{" + str(FL3_label2) + "}$"
#           ' ' r"$\bf{" + str(FL3_label3) + "}$" ' ' r"$\bf{" + str(FL3_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL3 -- 16:09:00 - 16:17:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL3_cap_df['sfm'].min(), FL3_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:09:00", "16:11:40", "16:14:20", "16:17:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL4 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL4_cap_df.DFC, FL4_cap_df.CIP_495um, c=FL4_cap_df.sfm, s=25, marker='o', cmap=cmap_FL4)
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
plt.ylabel('Concentration > 495 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1],fontsize=21)
plt.ylim(1e-4,1e-1)
# plt.yticks([250,500,750,1000,1250,1500],fontsize=21)
# FL4_label1 = 'Flight'
# FL4_label2 = 'Leg'
# FL4_label3 = '4'
# FL4_label4 = '[FL4]'
# plt.title(r"$\bf{" + str(FL4_label1) + "}$" ' ' r"$\bf{" + str(FL4_label2) + "}$"
#           ' ' r"$\bf{" + str(FL4_label3) + "}$" ' ' r"$\bf{" + str(FL4_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL4 -- 16:21:30 - 16:27:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL4_cap_df['sfm'].min(), FL4_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:21:30", "16:23:20", "16:25:10", "16:27:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

##############################################################################


##############################################################################
#Begin Plotting for extended FL plots for CIP 105um data

FL1_cap_df['b_105'] = np.log10(FL1_cap_df.twenty_pt_rolling_avg_105)
########## FL1 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL1_cap_df.DFC, FL1_cap_df.CIP_105um, c=FL1_cap_df.sfm, s=25, marker='o', cmap=cmap_FL1)
plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_105, c="black", linestyle='-',linewidth=3)
#plot linear trendline
coefs = np.polyfit(FL1_cap_df.DFC, FL1_cap_df.b_105, 1)
fit_coefs = np.poly1d(coefs)
plt.plot(FL1_cap_df.DFC, 10**fit_coefs(FL1_cap_df.DFC), color='red', linestyle='--')
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel('Concentration > 105 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-3,1e-2,1e-1,1e0],fontsize=21)
plt.ylim(1e-3,1e0)
plt.title('FL1 -- 15:51:15 - 16:01:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL2 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL2_cap_df.DFC, FL2_cap_df.CIP_105um, c=FL2_cap_df.sfm, s=25, marker='o', cmap=cmap_FL2)
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_105, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
plt.ylabel('Concentration > 105 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-3,1e-2,1e-1,1e0],fontsize=21)
plt.ylim(1e-3,1e0)
# FL2_label1 = 'Flight'
# FL2_label2 = 'Leg'
# FL2_label3 = '2'
# FL2_label4 = '[FL2]'
# plt.title(r"$\bf{" + str(FL2_label1) + "}$" ' ' r"$\bf{" + str(FL2_label2) + "}$"
#           ' ' r"$\bf{" + str(FL2_label3) + "}$" ' ' r"$\bf{" + str(FL2_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL2 -- 16:02:00 - 16:07:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL2_cap_df['sfm'].min(), FL2_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:02:00", "16:03:40", "16:05:20", "16:07:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL3 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.rcParams['axes.xmargin'] = 0
# plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL3_cap_df.DFC, FL3_cap_df.CIP_105um, c=FL3_cap_df.sfm, s=25, marker='o', cmap=cmap_FL3)
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_105, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.ylim(250,1500)
plt.ylabel('Concentration > 105 um (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-3,1e-2,1e-1,1e0],fontsize=21)
plt.ylim(1e-3,1e0)
# plt.yticks([250,500,750,1000,1250,1500],fontsize=21)
# FL3_label1 = 'Flight'
# FL3_label2 = 'Leg'
# FL3_label3 = '3'
# FL3_label4 = '[FL3]'
# plt.title(r"$\bf{" + str(FL3_label1) + "}$" ' ' r"$\bf{" + str(FL3_label2) + "}$"
#           ' ' r"$\bf{" + str(FL3_label3) + "}$" ' ' r"$\bf{" + str(FL3_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL3 -- 16:09:00 - 16:17:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL3_cap_df['sfm'].min(), FL3_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:09:00", "16:11:40", "16:14:20", "16:17:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL4 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL4_cap_df.DFC, FL4_cap_df.CIP_105um, c=FL4_cap_df.sfm, s=25, marker='o', cmap=cmap_FL4)
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_105, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=40)
plt.ylabel('Total Number Concentration $(#/cm^3)$',fontsize=40)
plt.xticks([20,40,60,80,100],fontsize=40)
plt.yscale('log',base=10) 
plt.yticks([1e-3,1e-2,1e-1,1e0],fontsize=40)
plt.ylim(1e-3,1e0)
# plt.yticks([250,500,750,1000,1250,1500],fontsize=21)
# FL4_label1 = 'Flight'
# FL4_label2 = 'Leg'
# FL4_label3 = '4'
# FL4_label4 = '[FL4]'
# plt.title(r"$\bf{" + str(FL4_label1) + "}$" ' ' r"$\bf{" + str(FL4_label2) + "}$"
#           ' ' r"$\bf{" + str(FL4_label3) + "}$" ' ' r"$\bf{" + str(FL4_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
# plt.title('FL4 -- 16:21:30 - 16:27:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL4_cap_df['sfm'].min(), FL4_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:21:30", "16:23:20", "16:25:10", "16:27:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

# #FL5 Plotting
# fig = plt.figure(figsize=(10, 6))
# plt.scatter(FL5_cap_df.DFC, FL5_cap_df.CIP_495um, c=FL5_cap_df.sfm, s=10, marker='o', cmap=cmap4)
# plt.xlabel('Distance From Storm Core Refl. Centroid (km)',fontsize=12)
# plt.ylabel('Concentration of CIP particles > 495' u"\u03bcm"' (#/m^3)',fontsize=12)
# FL5_label = 'Flight Leg 5 [FL5]'
# plt.title(r"$\bf{" + str(FL5_label) + "}$" ' -- CIP Particles > 495' u"\u03bcm" ' vs. Distance from Storm Core')
# #manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL5_cap_df['sfm'].min(), FL5_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# # cbar.set_ticklabels(["16:40:00 UTC", "16:03:40 UTC", "16:05:20 UTC", "16:46:00 UTC"])
# plt.grid()
# plt.show()
##############################################################################

#%%
##############################################################################
#Begin Plotting for extended FL plots but for Electric Field


########## FL1 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL1_cap_df.DFC, FL1_E_cap_df.Ez, c=FL1_E_cap_df.sfm, s=25, marker='o', cmap=cmap_FL1)

plt.plot(FL1_cap_df.DFC, FL1_E_cap_df.Ez_twenty_pt_rolling_avg, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel('Vertical E-Field - Ez (kV/m)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.ylim(-20,20)
plt.yticks([-20,-10,0,10,20],fontsize=21)
# FL1_label1 = 'Flight'
# FL1_label2 = 'Leg'
# FL1_label3 = '1'
# FL1_label4 = '[FL1]'
# plt.title(r"$\bf{" + str(FL1_label1) + "}$" ' ' r"$\bf{" + str(FL1_label2) + "}$"
#           ' ' r"$\bf{" + str(FL1_label3) + "}$" ' ' r"$\bf{" + str(FL1_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL1 -- 15:51:15 - 16:01:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL2 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL2_cap_df.DFC, FL2_E_cap_df.Ez, c=FL2_E_cap_df.sfm, s=25, marker='o', cmap=cmap_FL2)
plt.plot(FL2_cap_df.DFC, FL2_E_cap_df.Ez_twenty_pt_rolling_avg, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
plt.ylabel('Vertical E-Field - Ez (kV/m)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.ylim(-20,20)
plt.yticks([-20,-10,0,10,20],fontsize=21)
# FL2_label1 = 'Flight'
# FL2_label2 = 'Leg'
# FL2_label3 = '2'
# FL2_label4 = '[FL2]'
# plt.title(r"$\bf{" + str(FL2_label1) + "}$" ' ' r"$\bf{" + str(FL2_label2) + "}$"
#           ' ' r"$\bf{" + str(FL2_label3) + "}$" ' ' r"$\bf{" + str(FL2_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL2 -- 16:02:00 - 16:07:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL2_cap_df['sfm'].min(), FL2_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:02:00", "16:03:40", "16:05:20", "16:07:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL3 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL3_cap_df.DFC, FL3_E_cap_df.Ez, c=FL3_E_cap_df.sfm, s=25, marker='o', cmap=cmap_FL3)
plt.plot(FL3_cap_df.DFC, FL3_E_cap_df.Ez_twenty_pt_rolling_avg, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.ylim(250,1500)
plt.ylabel('Vertical E-Field - Ez (kV/m)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.ylim(-20,20)
plt.yticks([-20,-10,0,10,20],fontsize=21)
# FL3_label1 = 'Flight'
# FL3_label2 = 'Leg'
# FL3_label3 = '3'
# FL3_label4 = '[FL3]'
# plt.title(r"$\bf{" + str(FL3_label1) + "}$" ' ' r"$\bf{" + str(FL3_label2) + "}$"
#           ' ' r"$\bf{" + str(FL3_label3) + "}$" ' ' r"$\bf{" + str(FL3_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL3 -- 16:09:00 - 16:17:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL3_cap_df['sfm'].min(), FL3_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:09:00", "16:11:40", "16:14:20", "16:17:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL4 Plotting ########## 
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.scatter(FL4_cap_df.DFC, FL4_E_cap_df.Ez, c=FL4_E_cap_df.sfm, s=25, marker='o', cmap=cmap_FL4)
plt.plot(FL4_cap_df.DFC, FL4_E_cap_df.Ez_twenty_pt_rolling_avg, c="black", linestyle='-',linewidth=3)
plt.xlabel('Distance From Core (km)',fontsize=26)
plt.ylabel('Vertical E-Field - Ez (kV/m)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.ylim(-20,20)
plt.yticks([-20,-10,0,10,20],fontsize=21)
# FL4_label1 = 'Flight'
# FL4_label2 = 'Leg'
# FL4_label3 = '4'
# FL4_label4 = '[FL4]'
# plt.title(r"$\bf{" + str(FL4_label1) + "}$" ' ' r"$\bf{" + str(FL4_label2) + "}$"
#           ' ' r"$\bf{" + str(FL4_label3) + "}$" ' ' r"$\bf{" + str(FL4_label4) + "}$"
#           ' -- CIP Particles > 495 ' u"\u03bcm" ' vs. Distance from Storm Core')
plt.title('FL4 -- 16:21:30 - 16:27:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL4_cap_df['sfm'].min(), FL4_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["16:21:30", "16:23:20", "16:25:10", "16:27:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

# #FL5 Plotting
# fig = plt.figure(figsize=(10, 6))
# plt.scatter(FL5_cap_df.DFC, FL5_cap_df.CIP_495um, c=FL5_cap_df.sfm, s=10, marker='o', cmap=cmap4)
# plt.xlabel('Distance From Storm Core Refl. Centroid (km)',fontsize=12)
# plt.ylabel('Concentration of CIP particles > 495' u"\u03bcm"' (#/m^3)',fontsize=12)
# FL5_label = 'Flight Leg 5 [FL5]'
# plt.title(r"$\bf{" + str(FL5_label) + "}$" ' -- CIP Particles > 495' u"\u03bcm" ' vs. Distance from Storm Core')
# #manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL5_cap_df['sfm'].min(), FL5_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# # cbar.set_ticklabels(["16:40:00 UTC", "16:03:40 UTC", "16:05:20 UTC", "16:46:00 UTC"])
# plt.grid()
# plt.show()


#%%

# plot of just the 20 pt rolling averages
fig = plt.figure(figsize=(12, 12), facecolor='white')
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL1')
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_495, c="red", linestyle='-',linewidth=3, label = 'FL2')
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_495, c="green", linestyle='-',linewidth=3, label = 'FL3')
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495, c="orange", linestyle='-',linewidth=3, label = 'FL4')
plt.xlabel('Distance From Core (km)',fontsize=26)
plt.ylabel('Concentration > 495 ' u"\u03bcm"' (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=21)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1],fontsize=21)
plt.ylim(1e-4,1e-1)
plt.title('FL1-4 -- 20 pt. Rolling Averages',fontsize=26)
plt.grid()
plt.legend(loc='upper right', ncol=2, fontsize = 16, facecolor='white')

plt.show()


#%%
#Combbine the 495um and 105um moving average for each FL

#FL1
fig = plt.figure(figsize=(12, 12), facecolor='white', dpi=300)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL1 >495 ' u"\u03bcm"'')
plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_105, c="red", linestyle='-',linewidth=3, label = 'FL1 >105 ' u"\u03bcm"'')
plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 105 - 315 ' u"\u03bcm"'')

plt.scatter(FL1_cap_df.DFC, FL1_cap_df.CIP_495um, s=10, marker='o', c='black', alpha=0.5)
plt.scatter(FL1_cap_df.DFC, FL1_cap_df.CIP_105um, s=10, marker='o', c='red', alpha=0.5)
plt.scatter(FL1_cap_df.DFC, FL1_cap_df.CIP_105_315um, s=10, marker='o', c='green', alpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3)
plt.tick_params(axis='y', which='minor', length=10, width=2)
# plt.xlabel('Distance From Core (km)',fontsize=26)
# plt.ylabel('Concentration (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=30)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=30)
plt.ylim(1e-4,1e-0)
# plt.title('FL1 -- 15:51:50 - 16:01:00 UTC',fontsize=26)
plt.grid()
# plt.legend(loc='upper right', ncol=2, fontsize = 16, facecolor='white')
plt.show()

#FL2
fig = plt.figure(figsize=(12, 12), facecolor='white', dpi=300)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL2 >495 ' u"\u03bcm"'')
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_105, c="red", linestyle='-',linewidth=3, label = 'FL2 >105 ' u"\u03bcm"'')
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_105_315, c="green", linestyle='-',linewidth=3, label = 'FL2 105 - 315 ' u"\u03bcm"'')

plt.scatter(FL2_cap_df.DFC, FL2_cap_df.CIP_495um, s=10, marker='o', c='black', alpha=0.5)
plt.scatter(FL2_cap_df.DFC, FL2_cap_df.CIP_105um, s=10, marker='o', c='red', alpha=0.5)
plt.scatter(FL2_cap_df.DFC, FL2_cap_df.CIP_105_315um, s=10, marker='o', c='green', alpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3)
plt.tick_params(axis='y', which='minor', length=10, width=2)
# plt.xlabel('Distance From Core (km)',fontsize=26)
# plt.ylabel('Concentration (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=30)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=30)
plt.ylim(1e-4,1e-0)
# plt.title('FL2 -- 16:02:00 - 16:07:00 UTC',fontsize=26)
plt.grid()
# plt.legend(loc='upper right', ncol=2, fontsize = 16, facecolor='white')
plt.show()

#FL3
fig = plt.figure(figsize=(12, 12), facecolor='white', dpi=300)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL3 >495 ' u"\u03bcm"'')
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_105, c="red", linestyle='-',linewidth=3, label = 'FL3 >105 ' u"\u03bcm"'')
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_105_315, c="green", linestyle='-',linewidth=3, label = 'FL3 105 - 315 ' u"\u03bcm"'')

plt.scatter(FL3_cap_df.DFC, FL3_cap_df.CIP_495um, s=10, marker='o', c='black', alpha=0.5)
plt.scatter(FL3_cap_df.DFC, FL3_cap_df.CIP_105um, s=10, marker='o', c='red', alpha=0.5)
plt.scatter(FL3_cap_df.DFC, FL3_cap_df.CIP_105_315um, s=10, marker='o', c='green', alpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3)
plt.tick_params(axis='y', which='minor', length=10, width=2)
#plt.xlabel('Distance From Core (km)',fontsize=26)
#plt.ylabel('Concentration (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=30)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=30)
plt.ylim(1e-4,1e-0)
#plt.title('FL3 -- 16:09:00 - 16:17:00 UTC',fontsize=26)
plt.grid()
# plt.legend(loc='upper right', ncol=2, fontsize = 16, facecolor='white')
plt.show()

#FL4
fig = plt.figure(figsize=(12, 12), facecolor='white', dpi=300)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL4 >495 ' u"\u03bcm"'')
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_105, c="red", linestyle='-',linewidth=3, label = 'FL4 >105 ' u"\u03bcm"'')
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_105_315, c="green", linestyle='-',linewidth=3, label = 'FL4 105 - 315 ' u"\u03bcm"'')

plt.scatter(FL4_cap_df.DFC, FL4_cap_df.CIP_495um, s=10, marker='o', c='black', alpha=0.5)
plt.scatter(FL4_cap_df.DFC, FL4_cap_df.CIP_105um, s=10, marker='o', c='red', alpha=0.5)
plt.scatter(FL4_cap_df.DFC, FL4_cap_df.CIP_105_315um, s=10, marker='o', c='green', alpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3)
plt.tick_params(axis='y', which='minor', length=10, width=2)
# plt.xlabel('Distance From Core (km)',fontsize=26)
# plt.ylabel('Concentration (#/cm^3)',fontsize=26)
plt.xticks([20,40,60,80,100],fontsize=30)
plt.yscale('log',base=10) 
plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=30)
plt.ylim(1e-4,1e-0)
# plt.title('FL4 -- 16:21:30 - 16:27:00 UTC',fontsize=26)
plt.grid()
# plt.legend(loc='upper right', ncol=2, fontsize = 16, facecolor='white')
plt.show()


#%%
#Figures showing the CIP495um divided by CIP 105 - 315um
########## FL1 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white', dpi=200)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL1_cap_df.DFC, FL1_cap_df.CIP_495_div_105_315um, c=FL1_cap_df.sfm, s=25, marker='o', cmap=cmap_FL1)

plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
# plt.hlines(y=0.5, xmin=20, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel(r'$Ratio_{CN}$',fontsize=30)
plt.xticks([20,40,60,80,100],fontsize=21)
# plt.yscale('log',base=10) 
plt.yticks([0,1,2,3,4,5],fontsize=21)
plt.ylim(0,5)
plt.title('FL1 -- 15:51:15 - 16:01:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL2 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white',dpi=200)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL2_cap_df.DFC, FL2_cap_df.CIP_495_div_105_315um, c=FL2_cap_df.sfm, s=25, marker='o', cmap=cmap_FL2)
plt.plot(FL2_cap_df.DFC, FL2_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
# plt.hlines(y=0.5, xmin=20, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel(r'$Ratio_{CN}$',fontsize=30)
plt.xticks([20,40,60,80,100],fontsize=21)
# plt.yscale('log',base=10) 
plt.yticks([0,1,2,3,4,5],fontsize=21)
plt.ylim(0,5)
plt.title('FL2 -- 16:02:00 - 16:07:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL3 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white',dpi=200)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL3_cap_df.DFC, FL3_cap_df.CIP_495_div_105_315um, c=FL3_cap_df.sfm, s=25, marker='o', cmap=cmap_FL3)
plt.plot(FL3_cap_df.DFC, FL3_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
# plt.hlines(y=0.5, xmin=20, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel(r'$Ratio_{CN}$',fontsize=30)
plt.xticks([20,40,60,80,100],fontsize=21)
# plt.yscale('log',base=10) 
plt.yticks([0,1,2,3,4,5],fontsize=21)
plt.ylim(0,5)
plt.title('FL3 -- 16:09:00 - 16:17:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

########## FL4 Plotting #########
fig = plt.figure(figsize=(12, 12), facecolor='white',dpi=200)
plt.rcParams['axes.facecolor']='white'
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.ymargin'] = 0
plt.scatter(FL4_cap_df.DFC, FL4_cap_df.CIP_495_div_105_315um, c=FL4_cap_df.sfm, s=25, marker='o', cmap=cmap_FL4)
plt.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
# plt.hlines(y=0.5, xmin=20, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
plt.xlabel('Distance From Core (km)',fontsize=26)
#invert x axis
# plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
plt.ylabel(r'$Ratio_{CN}$',fontsize=30)
plt.xticks([20,40,60,80,100],fontsize=21)
# plt.yscale('log',base=10) 
plt.yticks([0,1,2,3,4,5],fontsize=21)
plt.ylim(0,5)
plt.title('FL4 -- 16:21:30 - 16:27:00 UTC',fontsize=26)
#manually set color tick positions/number of ticks/tick labels
# v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
# cbar=plt.colorbar(ticks=v1)
# cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
# cbar.ax.tick_params(labelsize=14)
plt.grid()
plt.show()

#EOS
