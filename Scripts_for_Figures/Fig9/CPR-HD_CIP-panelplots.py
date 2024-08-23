#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:51:02 2022

Syntax: ./CPR-HD_CIP-panelplots.py

Purpose: Creates CPR-HD plots shown in figure 9 & 10.
         Also plots other CPR-HD plots that are in the Supporting Material Section.


@author: christian.nairy
"""

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
import scipy.io as sio
import math


#%%
#Load in CPR-HD data for FL1 and FL4
path = '/nas/und/Florida/2019/Radar/MCR/'
#Flight Leg1
ac40_dbz = sio.loadmat(path + 'nb12_dbzp5_pp_39_ac40.mat')

#Read in relative range data
ac40_rr = sio.loadmat(path + 'nb12_rrp5_pp_39_ac40.mat')

#Read in time data
ac40_tt = sio.loadmat(path + 'nb12_ttp5_pp_39_ac40.mat')

#read in velocity
ac40_ur = sio.loadmat(path + 'nb12_urp5_pp_39_ac40.mat')

ac40_dbz_data = ac40_dbz['nb12_dbzp5_pp_39_ac40']
ac40_rr_data  = ac40_rr['nb12_rrp5_pp_39_ac40']
ac40_tt_data  = ac40_tt['nb12_ttp5_pp_39_ac40']
ac40_ur_data  = ac40_ur['nb12_urp5_pp_39_ac40']

#Convert relative range to km
ac40_rr_data = ac40_rr_data



time_ac40, rel_range_ac40 = np.meshgrid(ac40_tt_data, ac40_rr_data)

#Flight leg 4
#Read in flight leg 4 MCR data (AC45)
ac45_dbz = sio.loadmat(path + 'nb12_dbzp5_pp_39_ac45.mat')

#Read in relative range data
ac45_rr = sio.loadmat(path + 'nb12_rrp5_pp_39_ac45.mat')

#Read in time data
ac45_tt = sio.loadmat(path + 'nb12_ttp5_pp_39_ac45.mat')

#read in velocity
ac45_ur = sio.loadmat(path + 'nb12_urp5_pp_39_ac45.mat')
#Read in unfolded velocity .mat file
ac45_ur_unfolded = sio.loadmat(path + 'MCR_AC45_vel_mod10.mat')


#grab the dbz, rr, tt data and insert into numpy array
ac45_dbz_data = ac45_dbz['nb12_dbzp5_pp_39_ac45']
ac45_rr_data  = ac45_rr['nb12_rrp5_pp_39_ac45']
ac45_tt_data  = ac45_tt['nb12_ttp5_pp_39_ac45']
ac45_ur_data  = ac45_ur['nb12_urp5_pp_39_ac45']
ac45_ur_unfolded_data = ac45_ur_unfolded['MCR_AC45_vel_mod10']

#Convert relative range to km
# ac45_rr_data = ac45_rr_data / 1000

ac45_rr_data = ac45_rr_data

#Change ac45 time and dbz to match beginning of FL4
# ac45_tt_data = ac45_tt_data[:,329:]
# ac45_dbz_data = ac45_dbz_data[:,329:]

#pluck out min and max of dbz data
dbz_min = ac45_dbz_data.min()
dbz_max = ac45_dbz_data.max()

ur_min = ac45_ur_data.min()
ur_max = ac45_ur_data.max()

rr_min = ac45_rr_data.min()
rr_max = ac45_rr_data.max()

ur_unfolded_min = ac45_ur_unfolded_data.min()
ur_unfolded_max = ac45_ur_unfolded_data.max()


#meshgrid
time, rel_range = np.meshgrid(ac45_tt_data, ac45_rr_data)

#%%
#Loag in elevation, reference range, and azimuth data
#FL1
ac40_refrng = sio.loadmat(path + 'wr1_ref_rng_39_ac40.mat')
ac40_el = sio.loadmat(path + 'wr1_el_39_ac40.mat')
ac40_az = sio.loadmat(path + 'wr1_az_39_ac40.mat')

#access the data
ac40_refrng_data = ac40_refrng['wr1_ref_rng_39_ac40']
ac40_refrng_pd = pd.DataFrame(ac40_refrng_data).T
ac40_refrng_pd.columns = ['ac40_refrng']

ac40_el_data = ac40_el['wr1_el_39_ac40']
ac40_el_pd = pd.DataFrame(ac40_el_data).T
ac40_el_pd.columns = ['ac40_el']

ac40_az_data = ac40_az['wr1_az_39_ac40']
ac40_az_pd = pd.DataFrame(ac40_az_data).T
ac40_az_pd.columns = ['ac40_az']

#Need to average every 32 values
n = 32

ac40_refrng_32avg = ac40_refrng_pd.groupby(np.arange(len(ac40_refrng_pd))//32).mean()
ac40_refrng_32avg_np = ac40_refrng_32avg.to_numpy()
ac40_refrng_32avg_np = ac40_refrng_32avg_np[0:1507].T

ac40_el_32avg = ac40_el_pd.groupby(np.arange(len(ac40_el_pd))//32).mean()
ac40_el_32avg_np = ac40_el_32avg.to_numpy()
ac40_el_32avg_np = ac40_el_32avg_np[0:1507]

ac40_az_32avg = ac40_az_pd.groupby(np.arange(len(ac40_az_pd))//32).mean()
ac40_az_32avg_np = ac40_az_32avg.to_numpy()
ac40_az_32avg_np = ac40_az_32avg_np[0:1507]

##############################################################################
#FL4 (AC45)
ac45_refrng = sio.loadmat(path + 'wr1_ref_rng_39_ac45.mat')
ac45_el = sio.loadmat(path + 'wr1_el_39_ac45.mat')
ac45_az = sio.loadmat(path + 'wr1_az_39_ac45.mat')

#access the data
ac45_refrng_data = ac45_refrng['wr1_ref_rng_39_ac45']
ac45_refrng_pd = pd.DataFrame(ac45_refrng_data).T
ac45_refrng_pd.columns = ['ac45_refrng']

ac45_el_data = ac45_el['wr1_el_39_ac45']
ac45_el_pd = pd.DataFrame(ac45_el_data).T
ac45_el_pd.columns = ['ac45_el']

ac45_az_data = ac45_az['wr1_az_39_ac45']
ac45_az_pd = pd.DataFrame(ac45_az_data).T
ac45_az_pd.columns = ['ac45_az']

#Need to average every 32 values
n = 32

ac45_refrng_32avg = ac45_refrng_pd.groupby(np.arange(len(ac45_refrng_pd))//32).mean()
ac45_refrng_32avg_np = ac45_refrng_32avg.to_numpy()
ac45_refrng_32avg_np = ac45_refrng_32avg_np[0:1511].T

ac45_el_32avg = ac45_el_pd.groupby(np.arange(len(ac45_el_pd))//32).mean()
ac45_el_32avg_np = ac45_el_32avg.to_numpy()
ac45_el_32avg_np = ac45_el_32avg_np[0:1511]

ac45_az_32avg = ac45_az_pd.groupby(np.arange(len(ac45_az_pd))//32).mean()
ac45_az_32avg_np = ac45_az_32avg.to_numpy()
ac45_az_32avg_np = ac45_az_32avg_np[0:1511]


#%%
#utilize ref range and compute two dimentional range 
#AC40
r_new_lst = []

for n in range(1, 13596, 1):

    n_ref = 6400    
    r_new_lst.append(ac40_refrng_32avg_np + (n - n_ref)*1.4989)
    
#Vertically stack the listed numpy arrays -> create one array
range2d = np.vstack(r_new_lst) 


##############################################################################
#AC45
r_new_lst_ac45 = []

for n in range(1, 13596, 1):

    n_ref = 6400    
    r_new_lst_ac45.append(ac45_refrng_32avg_np + (n - n_ref)*1.4989)
    
#Vertically stack the listed numpy arrays -> create one array
range2d_ac45 = np.vstack(r_new_lst_ac45)

#%%
#use elevation and two-dimentional range to get beam height AGL
#AC40

rho40 = range2d / 1000 #

m40 = 13595
n40 = 1507
ones40 = np.ones((13595, 1507))
ae40 = ((4*6371) / 3) * ones40 # 4/3 Earth radius model for radar beam propagation (km)
theta40 = ac40_el_32avg_np*(3.14159 / 180.0) # elevation angle [deg -> rad]
theta2d40 = ones40
for i in range(0,13595,1):
    theta2d40[i, :] = theta40.T

h40 = (ae40**2 + rho40**2 + 2*ae40*rho40*np.sin(theta2d40))**(1/2) - ae40
h40 = h40 + 0.06 # convert MSL to AGL and account for antenna height

##############################################################################
#AC45
rho45 = range2d_ac45 / 1000 #

m45 = 13595
n45 = 1511
ones45 = np.ones((13595, 1511))
ae45 = ((4*6371) / 3) * ones45 # 4/3 Earth radius model for radar beam propagation (km)
theta45 = ac45_el_32avg_np*(3.14159 / 180.0) # elevation angle [deg -> rad]
theta2d45 = ones45
for i in range(0,13595,1):
    theta2d45[i, :] = theta45.T

h45 = (ae45**2 + rho45**2 + 2*ae45*rho45*np.sin(theta2d45))**(1/2) - ae45
h45 = h45 + 0.06 # convert MSL to AGL and account for antenna height


fig = plt.figure(figsize=(12,12), dpi=200)
plt.pcolormesh(time, h45, ac45_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
plt.colorbar()
plt.ylabel('Altitude [km]')
plt.xlabel('Time [SFM]')
plt.xlim(58890,59125)

#%%
#Load in science data
# path2 = '/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'
path2 = '/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190803_142455/CIP_Data/2023/new/'
cap = np.loadtxt(path2 + '19_08_03_14_24_55.cap.230617.new', skiprows = 58, usecols=(0,28,29,30,31,32,33,34,35,36,37,38))

#convert numpy array to pandas DataFrame
cap_df = pd.DataFrame(cap, columns=['sfm','chainagg','confidence','Ex','Ey','Ez','Eq','Emag','DFC','CIP_495um','CIP_105um','CIP_105_315um'])


cap_df[cap_df == 0.0] = np.nan
# cap_df[cap_df['N_CIP_conc'] < 10000] = np.nan
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
# FL4_cap_df = cap_df[6991:7228]
FL5_cap_df = cap_df[8101:8462]


#Calculate 20 point moving average for CIP105um
FL1_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL1_cap_df.CIP_105um.rolling(20,center=True).mean()
FL2_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL2_cap_df.CIP_105um.rolling(20,center=True).mean()
FL3_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL3_cap_df.CIP_105um.rolling(20,center=True).mean()
FL4_cap_df[ 'twenty_pt_rolling_avg_105' ] = FL4_cap_df.CIP_105um.rolling(20,center=True).mean()
# FL5_cap_df[ '5pt_rolling_avg' ] = FL5_cap_df.CIP_495um.rolling(20,center=True).mean()

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

# #%%
# #NEED TO OPEN THE CIP COUNTS. REMOVE FIRST 3 BINS
# #CALCULATE TOTAL > 495 UM
# #CALCULATE TOTAL 105 - 315 UM
# #CALCULATE TOTAL > 105 UM
# #LOOK AT WHITEBOARD AND CALULATE RELATIVE UNCERTANTY THEN ABSOLUTE UNCERTAINTY

# path2 = '/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'
# cip_count = np.loadtxt(path2 + '19_08_03_14_24_55.CIP_V.counts.1Hz', skiprows = 43, usecols=(0,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))

# #convert numpy array to pandas DataFrame
# cip_count_df = pd.DataFrame(cip_count, columns=['sfm','bin4','bin5','bin6','bin7','bin8','bin9','bin10','bin11','bin12','bin13','bin14','bin15','bin16','bin17','bin18','bin19','bin20','bin21','bin22','bin23','bin24'])

# #extract sfm
# sfm = cip_count_df['sfm'].to_frame()

# #extract > 105 um (total counts)
# cip_count_df_105 = cip_count_df[['bin4','bin5','bin6','bin7','bin8','bin9','bin10','bin11','bin12','bin13','bin14','bin15','bin16','bin17','bin18','bin19','bin20','bin21','bin22','bin23','bin24']].copy()
# col_list_105 = list(cip_count_df_105)
# cip_count_df_105['gt105_sum'] = cip_count_df_105[col_list_105].sum(axis=1)
# cip_count_gt105 = cip_count_df_105['gt105_sum'].to_frame()

# #extract > 495um (chain agg counts)
# cip_count_df_495 = cip_count_df[['bin11','bin12','bin13','bin14','bin15','bin16','bin17','bin18','bin19','bin20','bin21','bin22','bin23','bin24']].copy()
# col_list_495 = list(cip_count_df_495)
# cip_count_df_495['gt495_sum'] = cip_count_df_495[col_list_495].sum(axis=1)
# cip_count_gt495 = cip_count_df_495['gt495_sum'].to_frame()

# #extact between 105 and 315 um (nonchain agg counts)
# cip_count_df_105_315 = cip_count_df[['bin4','bin5','bin6','bin7']].copy()
# col_list_105_315 = list(cip_count_df_105_315)
# cip_count_df_105_315['105_315_sum'] = cip_count_df_105_315[col_list_105_315].sum(axis=1)
# cip_count_105_315 = cip_count_df_105_315['105_315_sum'].to_frame()

# count_total = cip_count_df_105['gt105_sum'].sum()

# cip_count_total = np.full((36001), count_total)
# cip_count_total = pd.DataFrame(cip_count_total, columns=['cip_count_total'])

# del_x_counts = (cip_count_df_495['gt495_sum'])**(1/2)
# del_x_counts = del_x_counts.to_frame()
# del_y_counts = (cip_count_df_105['gt105_sum'])**(1/2)
# del_y_counts = del_y_counts.to_frame()

# cip_new_df = pd.concat([sfm, cip_count_gt105, cip_count_gt495, cip_count_105_315, del_x_counts, del_y_counts], axis=1)
# cip_new_df.columns = ['sfm', 'cip_count_gt105', 'cip_count_gt495', 'cip_count_105_315', 'del_x_counts', 'del_y_counts']

# FL1_MCR_cip = cip_new_df[5180:5766]
# FL4_MCR_cip = cip_new_df[6995:7326]


#%%
#plotting

print(ac40_tt_data.min())
print(ac40_tt_data.max())

print(ac45_tt_data.min())
print(ac45_tt_data.max())

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [2,1,1]}, figsize=(14,14), dpi=300)
fig.tight_layout()

# plot1 = ax1.pcolormesh(time_ac40, h40, ac40_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
plot1 = ax1.pcolormesh(time_ac40, rel_range_ac40, ac40_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
# ax1.set_ylim(9,11)
ax1.set_ylim(34500,41900)
ax1.set_title('CPR-HD Merged NB1/NB2 -- FL1', fontsize=32)
ax1.set_ylabel('Altitude (km)', fontsize = 24)
ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax1.tick_params(axis='y', labelsize = 18)
ax1.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
cbar = fig.colorbar(plot1, ax = (ax1, ax2, ax3))
cbar.set_label('Reflectivity (dBZ)', fontsize=20)
cbar.ax.tick_params(labelsize=18)

plot2 = ax3.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c = 'r', linewidth = 3, label = 
                 '$RCAC_{N-C}$')
# plot3 = ax3.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495_div_105, c = 'b', linewidth = 3, linestyle='--', label = 
#                  '$RCAC_{all}$')
# ax3.hlines(y=0.5, xmin = 57225, xmax = 57556, linewidth = 3, color = 'k')
ax3.set_ylabel('$Ratio_{NC}$', fontsize = 24)
ax3.set_xlabel('Time (SFM)', fontsize = 20)
ax3.tick_params(axis='x', labelsize = 18)
# ax3.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax3.tick_params(axis='y', labelsize = 18)
ax3.set_xlim(57255,57556)
ax3.set_ylim(0,5)
# ax3.legend(fontsize = 18, loc = 'upper left')
ax3.grid(which = 'major', axis = 'both', linestyle = '--', linewidth = 3)

plot4 = ax2.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_105_315, c="m", linewidth = 3, label = 
                 '$Non-Chain_{conc}$')
plot5 = ax2.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495, c="g", linewidth = 3, linestyle='--', label = 
                 '$Chain_{conc}$')
ax2.set_ylabel('Concentration (#/cm^3)', fontsize = 24)
ax2.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
# ax3.set_xlabel('Time (SFM)', fontsize = 20)
# ax3.tick_params(axis='x', labelsize = 18)
ax2.tick_params(axis='y', labelsize = 18)
ax2.set_xlim(57255,57556)
ax2.set_yscale('log')
ax2.set_yticks([1e-3,1e-2,1e-1,1e0])
ax2.set_ylim(1e-3,1e0)
ax2.legend(fontsize = 24, loc = 'upper right')
ax2.grid(which = 'major', axis = 'both', linestyle = '--', linewidth = 3)


#%%
#AC45
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [2,1,1]}, figsize=(14,14), dpi=300)
fig.tight_layout()
# params = {'mathtext.defult': 'regular'}
# plt.rcParams.update(params)

plot1 = ax1.pcolormesh(time, h45, ac45_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
ax1.set_ylim(9,11)
ax1.set_title('CPR-HD Merged NB1/NB2 -- FL4', fontsize=32)
ax1.set_ylabel('Altitude (km)', fontsize = 24)
ax1.tick_params(axis='y', labelsize = 18)
ax1.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
ax1.set_xlim(58890,59125)
cbar = fig.colorbar(plot1, ax = (ax1, ax2, ax3))
cbar.set_label('Reflectivity (dBZ)', fontsize=20)
cbar.ax.tick_params(labelsize=18)
ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax1.set_xticklabels([])

plot2 = ax3.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_495_div_105_315, c = 'r', linewidth = 3, label = 
                 '$RCAC_{N-C}$')
# plot3 = ax3.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_495_div_105, c = 'b', linewidth = 3, linestyle='--', label = 
#                  '$RCAC_{all}$')
# ax3.hlines(y=0.5, xmin = 58890, xmax = 59125, linewidth = 3, color = 'k')
ax3.set_ylabel('$Ratio_{NC}$', fontsize = 24)
ax3.set_xlabel('Time (SFM)', fontsize = 20)
# ax3.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax3.tick_params(axis='x', labelsize = 18)
ax3.tick_params(axis='y', labelsize = 18)
ax3.set_xlim(58890,59125)
ax3.set_ylim(0,2)
# ax3.legend(fontsize = 18, loc = 'upper left')
ax3.grid(which = 'major', axis = 'both', linestyle = '--', linewidth = 3)


plot4 = ax2.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_105_315, c="m", linewidth = 3, label = 
                 '$Non-Chain_{conc}$')
plot5 = ax2.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_495, c="g", linewidth = 3, linestyle='--',label = 
                 '$Chain_{conc}$')
ax2.set_ylabel('Concentration (#/cm^3)', fontsize = 24)
ax2.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
# ax2.set_xlabel('Time (SFM)', fontsize = 20)
# ax2.tick_params(axis='x', labelsize = 18)
ax2.tick_params(axis='y', labelsize = 18)
ax2.set_xlim(58890,59125)
ax2.set_yscale('log')
ax2.set_yticks([1e-3,1e-2,1e-1,1e0])
ax2.set_ylim(1e-3,1e0)
ax2.legend(fontsize = 24, loc = 'upper right')
ax2.grid(which = 'major', axis = 'both', linestyle = '--', linewidth = 3)
ax2.set_xticklabels([])



#%%
fig = plt.figure(figsize=(12,12), dpi=200)
plot = plt.pcolormesh(time_ac40, h40, ac40_dbz_data, cmap = 'viridis',
                        vmin = -15, vmax = 20)
plt.title('CPR-HD Merged NB1/NB2 -- FL1', fontsize=24)
plt.ylabel('Altitude (km)', fontsize=20)
plt.xlabel('Time [SFM]', fontsize=20)
cbar = plt.colorbar(plot)
cbar.set_label(label='Reflectivity (dBZ)', fontsize=20)
cbar.ax.tick_params(labelsize=14)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.show()



fig = plt.figure(figsize=(12,12), dpi=200)
plot = plt.pcolormesh(time, h45, ac45_dbz_data, cmap = 'viridis',
                        vmin = -15, vmax = 20)
plt.title('CPR-HD Merged NB1/NB2 -- FL4', fontsize=24)
plt.ylabel('Altitude (km)', fontsize=20)
plt.xlabel('Time [SFM]', fontsize=20)
cbar = plt.colorbar(plot)
cbar.set_label(label='Reflectivity (dBZ)', fontsize=20)
cbar.ax.tick_params(labelsize=14)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlim(58890,59125)

plt.show()

#%%
#Testing
time_ac40_f = np.flip(time_ac40)
h40_f = np.flip(h40)
ac40_dbz_data_f = np.flip(ac40_dbz_data)

# fig = plt.figure(figsize=(12,12), dpi=200)
# plt.pcolormesh(time_ac40, h40_f, ac40_dbz_data_f, cmap = 'viridis', vmin=-15, vmax=20)
# plt.colorbar()
# plt.ylabel('Altitude [km]')
# plt.xlabel('Time [SFM]')

#%%
#Attempt at twin y axis on middle plot
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2,1]}, figsize=(14,14), dpi=300)
fig.tight_layout()

plot1 = ax1.pcolormesh(time_ac40, h40, ac40_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
ax1.set_ylim(9,11)
# ax1.set_title('CPR-HD Merged NB1/NB2 -- FL1', fontsize=32)
ax1.set_ylabel('Altitude (km)', fontsize = 24)
# ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
# ax1.set_xticks([	57296.56, 57377, 57457.56, 57538.56])
ax1.set_xticklabels([])
ax1.set_xlim(57556,57255)
ax1.tick_params(axis='y', labelsize = 22)
ax1.tick_params(axis='y', which='major', length=8, width=5)
ax1.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# cbar = fig.colorbar(plot1, ax = (ax1, ax2, ax3))
# cbar.set_label('Reflectivity (dBZ)', fontsize=20)
# cbar.ax.tick_params(labelsize=18)

ax3 = ax2.twinx()

plot4 = ax2.plot(np.flip(FL1_cap_df.sfm), np.flip(FL1_cap_df.twenty_pt_rolling_avg_105_315), c="k", linewidth = 3, label = 
                 '$Non-Chain_{conc}$')
plot5 = ax2.plot(np.flip(FL1_cap_df.sfm), np.flip(FL1_cap_df.twenty_pt_rolling_avg_495), c="g", linewidth = 3, linestyle='--', label = 
                 '$Chain_{conc}$')

plot2 = ax3.plot(np.flip(FL1_cap_df.sfm), np.flip(FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315), c = 'r', linewidth = 3, label = 
                 '$Ratio_{CN}$')
# plot3 = ax3.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495_div_105, c = 'b', linewidth = 3, linestyle='--', label = 
#                  '$RCAC_{all}$')
# ax3.hlines(y=0.5, xmin = 57225, xmax = 57556, linewidth = 3, color = 'k')
ax2.tick_params(axis='y', labelsize = 22)
ax2.set_xlim(57556,57255)
# ax2.set_xlim(37.83,75.14)
# ax2.xaxis.set_major_locator(plt.MaxNLocator(5))
ax2.set_yscale('log')
ax2.set_yticks([1e-3,1e-2,1e-1,1e0])
# ax2.set_xticks([70,60,50,40])
ax2.tick_params(axis='y', which='major', length=8, width=5)
ax2.tick_params(axis='x', which='major', length=8, width=5)

ax2.set_xticklabels(['69','69','63','57','51','45','39','39'])

ax2.tick_params(axis='y', which='minor', length=4, width=3)
ax2.set_ylim(1e-3,1e0)
ax2.legend(fontsize = 24, loc = 'upper left')
ax2.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# ax2.set_xlabel('Time (SFM)', fontsize = 20)
ax2.set_ylabel('Concentration (#/cm^3)', fontsize = 24)
ax2.tick_params(axis='x', labelsize = 22)
ax2.tick_params(axis='y', labelsize = 22)

ax3.set_ylabel('$Ratio_{CN}$', fontsize = 24, c='r')
ax3.tick_params(axis='y', which='major', length=8, width=5)

# ax3.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax3.tick_params(axis='y', labelsize = 22)
ax3.set_xlim(57556,57255)
# ax3.set_xlim(37.83,75.14)
# ax3.set_xlim(57255,57556)
# ax3.set_xlim(75.14,37.83)
# ax3.set_xticks([70,60,50,40])
# ax3.xaxis.set_major_locator(plt.MaxNLocator(5))
ax3.legend(fontsize = 24, loc = 'upper right')
ax3.set_ylim(0,5)


#%%

fig, (ax1, ax2, ax4) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [2,1,1]}, figsize=(14,14), dpi=300)
fig.tight_layout()

plot1 = ax1.pcolormesh(time, h45, ac45_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
ax1.set_ylim(9,11)
ax1.set_xlim(58900,59125)
ax1.set_xticks([	58900,59012,59125])
# ax1.set_title('CPR-HD Merged NB1/NB2 -- FL1', fontsize=32)
ax1.set_ylabel('Altitude (km)', fontsize = 24)
ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax1.set_xticklabels([])
ax1.tick_params(axis='y', labelsize = 22)
ax1.tick_params(axis='y', which='major', length=8, width=5)
ax1.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# cbar = fig.colorbar(plot1, ax = (ax1, ax2, ax3))
# cbar.set_label('Reflectivity (dBZ)', fontsize=20)
# cbar.ax.tick_params(labelsize=18)

ax3 = ax2.twinx()

# plot4 = ax2.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_105_315, c="k", linewidth = 3, label = 
#                  '$Non-Chain_{conc}$')
# plot5 = ax2.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495, c="g", linewidth = 3, linestyle='--', label = 
#                  '$Chain_{conc}$')

plot2 = ax3.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495_div_105_315, c = 'r', linewidth = 3, label = 
                 '$Ratio_{NC}$')
# plot3 = ax3.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495_div_105, c = 'b', linewidth = 3, linestyle='--', label = 
#                  '$RCAC_{all}$')
# ax3.hlines(y=0.5, xmin = 57225, xmax = 57556, linewidth = 3, color = 'k')
ax2.tick_params(axis='y', labelsize = 22)
# ax3.set_xlim(58900,59125)
ax2.set_xlim(50.41,71.19)
ax2.set_xticks([50.41,59.336,71.19])
ax2.set_yscale('log')
ax2.set_yticks([1e-3,1e-2,1e-1,1e0])
ax2.tick_params(axis='y', which='major', length=8, width=5)
ax2.tick_params(axis='x', which='major', length=8, width=5)
# ax2.set_xticklabels([])
ax2.tick_params(axis='y', which='minor', length=4, width=3)
ax2.set_ylim(1e-3,1e0)
ax2.legend(fontsize = 24, loc = 'upper left')
ax2.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# ax2.set_xlabel('Time (SFM)', fontsize = 20)
ax2.set_ylabel('Concentration (#/cm^3)', fontsize = 24)
ax2.tick_params(axis='x', labelsize = 22)
ax2.tick_params(axis='y', labelsize = 22)

ax3.set_ylabel('$Ratio_{NC}$', fontsize = 24, c='r')
ax3.tick_params(axis='y', which='major', length=8, width=5)

# ax3.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax3.tick_params(axis='y', labelsize = 22)
# ax3.set_xlim(58900,59125)
ax3.set_xlim(50.41,71.19)
ax3.set_xticks([50.41,59.336,71.19])
ax3.legend(fontsize = 24, loc = 'upper right')
ax3.set_ylim(0,2)

# ax4 = fig.add_subplot(111, zorder=-1)
# for _, spine in ax4.spines.items():
#     spine.set_visible(False)
# ax4.tick_params(labelleft=False, labelbottom=False, left=False, right=False )
# ax4.get_shared_x_axes().join(ax3,ax1)
# ax4.grid(axis="x")
plot2 = ax4.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_495_div_105_315, c = 'r', linewidth = 3, label = 
                 '$Ratio_{NC}$')
ax4.set_ylabel('$Ratio_{NC}$', fontsize = 24, c='r')
ax4.tick_params(axis='y', which='major', length=8, width=5)
ax4.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# ax3.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax4.tick_params(axis='y', labelsize = 22)
ax4.tick_params(axis='x', labelsize = 22)
ax4.set_xlim(58900,59125)
ax4.set_xticks([	58900,59012,59125])
# ax4.set_xticks([50.41,59.336,71.19])
ax4.legend(fontsize = 24, loc = 'upper right')
ax4.set_ylim(0,2)

#%%

# from mpl_toolkits.axes_grid1 import make_axes_locatable

# fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2,1]}, figsize=(14,14), dpi=300)
# plot1 = ax1.pcolormesh(time, h45, ac45_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
# ax1.set_ylim(9,11)
# ax1.set_xlim(58900,59125)
# # ax1.set_xticks([	58900,59012,59125])
# # ax1.set_title('CPR-HD Merged NB1/NB2 -- FL1', fontsize=32)
# ax1.set_ylabel('Altitude (km)', fontsize = 24)
# # ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
# # ax1.set_xticklabels([])
# ax1.tick_params(axis='y', labelsize = 22)
# ax1.tick_params(axis='x', labelsize = 22)
# ax1.tick_params(axis='y', which='major', length=8, width=5)


# # axvert = divider.append_axes('right', size='30%', pad=0.5)
# ax2.tick_params(axis='y', labelsize = 22)
# ax2.tick_params(axis='x', labelsize = 22)
# plot2 = ax2.plot(FL4_cap_df.DFC, FL4_cap_df.twenty_pt_rolling_avg_495_div_105_315, c = 'r', linewidth = 3, label = 
#                  '$Ratio_{NC}$')
# # ax2.set_xlim(50.41,71.19)
# # ax2.set_xticks([50.41,59.336,71.19])
# ax2.tick_params(axis='y', labelsize = 22)
# ax2.tick_params(axis='x', labelsize = 22)
# ax2.margins(x=0)
# # ADD THIS LINE
# ax1.set_xticks(np.linspace(ax1.get_xticks()[0], ax1.get_xticks()[-1], len(ax2.get_xticks())))
# plt.show()

#%%
#Plots with sfm instead of DFC (FL4)
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2,1]}, figsize=(14,14), dpi=300)
fig.tight_layout()

plot1 = ax1.pcolormesh(time, h45, ac45_dbz_data, cmap = 'viridis', vmin=-15, vmax=20)
ax1.set_ylim(9,11)
ax1.set_xlim(58890,59125)
# ax1.set_title('CPR-HD Merged NB1/NB2 -- FL1', fontsize=32)
ax1.set_ylabel('Altitude (km)', fontsize = 24)
ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax1.set_xticklabels([])
ax1.tick_params(axis='y', labelsize = 22)
ax1.tick_params(axis='y', which='major', length=8, width=5)
ax1.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# cbar = fig.colorbar(plot1, ax = (ax1, ax2, ax3))
# cbar.set_label('Reflectivity (dBZ)', fontsize=20)
# cbar.ax.tick_params(labelsize=18)

ax3 = ax2.twinx()

plot4 = ax2.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_105_315, c="k", linewidth = 3, label = 
                 '$Non-Chain_{conc}$')
plot5 = ax2.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_495, c="g", linewidth = 3, linestyle='--', label = 
                 '$Chain_{conc}$')

plot2 = ax3.plot(FL4_cap_df.sfm, FL4_cap_df.twenty_pt_rolling_avg_495_div_105_315, c = 'r', linewidth = 3, label = 
                 '$Ratio_{CN}$')
# plot3 = ax3.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495_div_105, c = 'b', linewidth = 3, linestyle='--', label = 
#                  '$RCAC_{all}$')
# ax3.hlines(y=0.5, xmin = 57225, xmax = 57556, linewidth = 3, color = 'k')
ax2.tick_params(axis='y', labelsize = 22)
ax3.set_xlim(58890,59125)
ax2.set_yscale('log')
ax2.set_yticks([1e-3,1e-2,1e-1,1e0])
ax2.tick_params(axis='y', which='major', length=8, width=5)
ax2.tick_params(axis='x', which='major', length=8, width=5)
ax2.set_xticklabels([])
ax2.tick_params(axis='y', which='minor', length=4, width=3)
ax2.set_ylim(1e-3,1e0)
ax2.legend(fontsize = 24, loc = 'upper left')
ax2.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
# ax2.set_xlabel('Time (SFM)', fontsize = 20)
ax2.set_ylabel('Concentration (#/cm^3)', fontsize = 24)
ax2.tick_params(axis='x', labelsize = 22)
ax2.tick_params(axis='y', labelsize = 22)

ax3.set_ylabel('$Ratio_{CN}$', fontsize = 24, c='r')
ax3.tick_params(axis='y', which='major', length=8, width=5)

# ax3.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
ax3.tick_params(axis='y', labelsize = 22)
ax3.set_xlim(58890,59125)
ax3.legend(fontsize = 24, loc = 'upper right')
ax3.set_ylim(0,2)


#%%
ax3.grid(which = 'major', axis = 'both', linestyle = '--', linewidth = 3)

plot4 = ax2.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_105_315, c="m", linewidth = 3, label = 
                 '$Non-Chain_{conc}$')
plot5 = ax2.plot(FL1_cap_df.sfm, FL1_cap_df.twenty_pt_rolling_avg_495, c="g", linewidth = 3, linestyle='--', label = 
                 '$Chain_{conc}$')
ax2.set_ylabel('Concentration (#/cm^3)', fontsize = 24)
ax2.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
# ax3.set_xlabel('Time (SFM)', fontsize = 20)
# ax3.tick_params(axis='x', labelsize = 18)
ax2.tick_params(axis='y', labelsize = 18)
ax2.set_xlim(57255,57556)
ax2.set_yscale('log')
ax2.set_yticks([1e-3,1e-2,1e-1,1e0])
ax2.set_ylim(1e-3,1e0)
ax2.legend(fontsize = 24, loc = 'upper right')
ax2.grid(which = 'major', axis = 'both', linestyle = '--', linewidth = 3)
























