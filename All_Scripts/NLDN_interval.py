import pandas as pd
import os
#import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


path = '/Users/christiannairy/Documents/Research/lightning/'
# data_0802 = pd.read_csv(path + '20190802_NLDN.txt', header=None,sep="\s+", engine='python',encoding="utf8")
data_0803_full = pd.read_csv(path + '20190803_NLDN.txt', header=None,sep="\s+", engine='python',encoding="utf8")


data_0803_full.columns =['Date', 'Time UTC', 'Lat', 'Lon', 'Mag', 'Type']
# data_0802.columns =['Date', 'Time UTC', 'Lat', 'Lon', 'Mag', 'Type']



# data_0802 = data_0802[106741:118459]
data_0803_full = data_0803_full[15886:24369]
data_0803_index = pd.to_datetime(data_0803_full['Date'] + ' ' + data_0803_full['Time UTC'])
del data_0803_full['Date']
del data_0803_full['Time UTC']

datetime = data_0803_index.to_frame(name='DateTime')

data_0803 = data_0803_full.join(datetime)
data_0803 = data_0803.set_index('DateTime')

data_0803 = data_0803.between_time('15:00:00', '15:30:00')


# ############################################################################################
# # pos_0802 = data_0802['Mag'] > 0
# # positive_0802 = data_0802[pos_0802]
# # positive_0802_lat = positive_0802[(positive_0802['Lat']> 28.4) & (positive_0802['Lat'] < 29.0)]
# # positive_0802_latlon = positive_0802_lat[(positive_0802_lat['Lon']> -81.25) & (positive_0802_lat['Lon'] < -80.0)]

# # neg_0802 = data_0802['Mag'] < 0
# # negative_0802 = data_0802[neg_0802]
# # negative_0802_lat = negative_0802[(negative_0802['Lat']> 28.4) & (negative_0802['Lat'] < 29.0)]
# # negative_0802_latlon = negative_0802_lat[(negative_0802_lat['Lon']> -81.25) & (negative_0802_lat['Lon'] < -80.0)]

# #############################################################################################

pos_0803 = data_0803['Mag'] > 0
positive_0803 = data_0803[pos_0803]
positive_0803_lat = positive_0803[(positive_0803['Lat'] > 28.3) & (positive_0803['Lat'] < 29.4)]
positive_0803_latlon = positive_0803_lat[(positive_0803_lat['Lon'] > -81.5) & (positive_0803_lat['Lon'] < -80.3)]

neg_0803 = data_0803['Mag'] < 0
negative_0803 = data_0803[neg_0803]
negative_0803_lat = negative_0803[(negative_0803['Lat'] > 28.3) & (negative_0803['Lat'] < 29.4)]
negative_0803_latlon = negative_0803_lat[(negative_0803_lat['Lon'] > -81.5) & (negative_0803_lat['Lon'] < -80.3)]



# ##############################################################################
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

# pos_0803_C = cloud_lgn_0803['Mag'] > 0
# positive_0803_C = cloud_lgn_0803[pos_0803_C]
# positive_0803_C_lat = positive_0803_C[(positive_0803_C['Lat'] > 28.3) & (positive_0803_C['Lat'] < 29.0)]
# positive_0803_C_latlon = positive_0803_C_lat[(positive_0803_C_lat['Lon'] > -81.5) & (positive_0803_C_lat['Lon'] < -80.3)]

# pos_0803_G = ground_lgn_0803['Mag'] > 0
# positive_0803_G = ground_lgn_0803[pos_0803_G]
# positive_0803_G_lat = positive_0803_G[(positive_0803_G['Lat']> 28.3) & (positive_0803_G['Lat'] < 29.0)]
# positive_0803_G_latlon = positive_0803_G_lat[(positive_0803_G_lat['Lon'] > -81.5) & (positive_0803_G_lat['Lon'] < -80.3)]

# neg_0803_C = cloud_lgn_0803['Mag'] < 0
# negative_0803_C = cloud_lgn_0803[neg_0803_C]
# negative_0803_C_lat = negative_0803_C[(negative_0803_C['Lat']> 28.3) & (negative_0803_C['Lat'] < 29.0)]
# negative_0803_C_latlon = negative_0803_C_lat[(negative_0803_C_lat['Lon'] > -81.5) & (negative_0803_C_lat['Lon'] < -80.3)]

# neg_0803_G = ground_lgn_0803['Mag'] < 0
# negative_0803_G = ground_lgn_0803[neg_0803_G]
# negative_0803_G_lat = negative_0803_G[(negative_0803_G['Lat']> 28.3) & (negative_0803_G['Lat'] < 29.0)]
# negative_0803_G_latlon = negative_0803_G_lat[(negative_0803_G_lat['Lon'] > -81.5) & (negative_0803_G_lat['Lon'] < -80.3)]

# ##############################################################################
# types = {}


# for i, g in data_0802.groupby('Type'):
#     #print 'data_' + str(i)
#     #print g
#     types.update({'data_0802_' + str(i) : g.reset_index(drop=True)})
    
# cloud_lgn_0802 = types['data_0802_C']
# ground_lgn_0802 = types['data_0802_G']

# pos_0802_C = cloud_lgn_0802['Mag'] > 0
# positive_0802_C = cloud_lgn_0802[pos_0802_C]
# positive_0802_C_lat = positive_0802_C[(positive_0802_C['Lat']> 28.4) & (positive_0802_C['Lat'] < 29.0)]
# positive_0802_C_latlon = positive_0802_C_lat[(positive_0802_C_lat['Lon']> -81.25) & (positive_0802_C['Lon'] < -80.0)]


# pos_0802_G = ground_lgn_0802['Mag'] > 0
# positive_0802_G = ground_lgn_0802[pos_0802_G]
# positive_0802_G_lat = positive_0802_G[(positive_0802_G['Lat']> 28.4) & (positive_0802_G['Lat'] < 29.0)]
# positive_0802_G_latlon = positive_0802_G_lat[(positive_0802_G_lat['Lon']> -81.25) & (positive_0802_G['Lon'] < -80.0)]

# neg_0802_C = cloud_lgn_0802['Mag'] < 0
# negative_0802_C = cloud_lgn_0802[neg_0802_C]
# negative_0802_C_lat = negative_0802_C[(negative_0802_C['Lat']> 28.4) & (negative_0802_C['Lat'] < 29.0)]
# negative_0802_C_latlon = negative_0802_C_lat[(negative_0802_C_lat['Lon']> -81.25) & (negative_0802_C['Lon'] < -80.0)]

# neg_0802_G = ground_lgn_0802['Mag'] < 0
# negative_0802_G = ground_lgn_0802[neg_0802_G]
# negative_0802_G_lat = negative_0802_G[(negative_0802_G['Lat']> 28.4) & (negative_0802_G['Lat'] < 29.0)]
# negative_0802_G_latlon = negative_0802_G_lat[(negative_0802_G_lat['Lon']> -81.25) & (negative_0802_G['Lon'] < -80.0)]

#Aircraft track information
path_tit = '/Users/christiannairy/Documents/Research/20190803_1424_files/'
data_0803_tit = pd.read_csv(path_tit + '19_08_03_14_24_55.tit', header=None,sep="\s+", engine='python',encoding="utf8")



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

tit = data_0803_tit4_final.between_time('15:00:00', '15:30:00')

tit_tail_lon = pd.DataFrame(tit['Lon'].tail(1))

tit_tail_lat = pd.DataFrame(tit['Lat'].tail(1))





#Radar information

kmlb_lat = 28.1
kmlb_lon = -80.64

kaspr_lat = 28.7548
kaspr_lon = -80.7744
##########

reader = shpreader.Reader(path + 'countyl010g_shp_nt00964/countyl010g.shp')
counties = list(reader.geometries())
COUNTIES = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())

negative_stroke_count = negative_0803_latlon.Lat.count()
negative_stroke_count = str(negative_stroke_count)
positive_stroke_count = positive_0803_latlon.Lat.count()
positive_stroke_count = str(positive_stroke_count)

cloud_stroke_count = cloud_lgn_0803_C_latlon.Lat.count()
cloud_stroke_count = str(cloud_stroke_count)

ground_stroke_count = ground_lgn_0803_G_latlon.Lat.count()
ground_stroke_count = str(ground_stroke_count)

# total_ground_strokes = negative_0803_G_latlon.Lat.count() + positive_0803_G_latlon.Lat.count()
# total_ground_strokes = str(total_ground_strokes)
# total_cloud_strokes = negative_0803_C_latlon.Lat.count() + positive_0803_C_latlon.Lat.count()
# total_cloud_strokes = str(total_cloud_strokes)


# Begin plotting




plt.figure(figsize=(10, 6))
ax2 = plt.axes(projection=ccrs.PlateCarree())
ax2.add_feature(cfeature.LAND.with_scale('50m'))
ax2.add_feature(cfeature.OCEAN.with_scale('50m'))
ax2.add_feature(cfeature.LAKES.with_scale('50m'))
ax2.add_feature(COUNTIES, facecolor='none', edgecolor='gray')
ax2.coastlines('50m')
ax2.set_extent([-81.50, -80, 28, 29])
ax2.text(-0.10, 0.55, 'Latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax2.transAxes, fontsize = 12)
ax2.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax2.transAxes, fontsize = 12)
# ax2.text(0.01,-0.17, 'Total # of Negative Strokes = ' + negative_stroke_count,va='bottom', ha='left',
#         rotation='horizontal', rotation_mode='anchor',
#         transform=ax2.transAxes, fontsize = 12)
# ax2.text(0.01,-0.22, 'Total # of Positive Strokes = ' + positive_stroke_count,va='bottom', ha='left',
#         rotation='horizontal', rotation_mode='anchor',
#         transform=ax2.transAxes, fontsize = 12)
ax2.text(0.01,-0.17, 'Total # of Cloud-to-Ground Strokes = ' + ground_stroke_count,va='bottom', ha='left',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax2.transAxes, fontsize = 12)
ax2.text(0.01,-0.22, 'Total # of Cloud-to-Cloud/Intra-Cloud Strokes = ' + cloud_stroke_count,va='bottom', ha='left',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax2.transAxes, fontsize = 12)

#gl is gridliner -- needed to add axis
gl = ax2.gridlines(draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabels_bottom = True
gl.ylabels_left = True
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER




ax2.scatter(cloud_lgn_0803_C_latlon.Lon, cloud_lgn_0803_C_latlon.Lat, c='r', marker="x", label='NLDN Cloud-to-Cloud/Intra-Cloud Strokes', alpha=0.5)
ax2.scatter(ground_lgn_0803_G_latlon.Lon, ground_lgn_0803_G_latlon.Lat, c='b', marker="v", label='NLDN Cloud-to-Ground Strokes', alpha=0.5)

ax2.scatter(kmlb_lon, kmlb_lat, c='g', s=100, marker='o', label='KMLB')
ax2.scatter(kaspr_lon, kaspr_lat, c='k', s=100, marker='o', label='KASPR/CPR-HD')
# ax2.plot(tit.Lon, tit.Lat, c='black', label='Aircraft Flight Track', linewidth = 2)

plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left', fontsize = 12)
plt.title('15:00:00 - 15:30:00 UTC', fontsize = 14)
plt.show()

#\n [Lat: 28.3N;29.4N] [Lon: 81.5W; 80.3W]'

# ax2.scatter(positive_0802_latlon.Lon, positive_0802_latlon.Lat, c='r', marker="+", label='NLDN Positive Strikes', alpha=0.5)
# ax2.scatter(negative_0802_latlon.Lon, negative_0802_latlon.Lat, c='b', marker="_", label='NLDN Negative Strikes', alpha=0.5)
# ax2.scatter(kmlb_lon, kmlb_lat, c='g', s=100, marker='o', label='KMLB')
# plt.legend(loc='lower right')
# plt.title('NLDN Lightning Stokes - 2019/08/02 19:30:00 - 20:30:00 UTC [Lat: 28.4N;29.0N] [Lon: -81.25W;-80.0W]')
# plt.show()







