#!/bin/env python3 
"""
  NAME:
    CIP_V_FlightLegs.py
 
  PURPOSE:
    This script will read in your segmented flight leg science data file and
    save a Relative Chain Aggregate Concentration (wrt non-chains) vs Distance
    from Core figure for each defined flight leg.


  CALLS:
    NONE

  EXAMPLE:
    The command:
        CIP_V_FlightLegs.py

       

    creates: YYMMDD_CIP_V_RCACnc_FL1.png
             YYMMDD_CIP_V_RCACnc_ALL.png

  MODIFICATIONS:
    Christian Nairy <christian.nairy@und.edu> - 2022/08/11:
      Written...
  COPYRIGHT:
    2017 David Delene

    This program is distributed under terms of the GNU General Public License
 
    This file is part of Airborne Data Processing and Analysis (ADPAA).

    ADPAA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ADPAA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ADPAA.  If not, see <http://www.gnu.org/licenses/>.
"""
#IMPORTS
#Some may be used in the future.
import sys
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from datetime import datetime, timedelta
from dateutil import parser
import matplotlib.ticker as mticker
import cmasher as cmr
import scipy.interpolate as si
import glob
from adpaa_python3 import ADPAA
from random import randint

#Remove pandas warning messages
pd.options.mode.chained_assignment = None

# Define syntax. 
def help_message():
    print('\n')
    print('Syntax: CIP_V_FlightLegs.py <-h>\n\n')
    print('  Example: CIP_V_FlightLegs.py \n')

# Check input parameters. 
for param in sys.argv:
    if param.startswith('-h') | param.startswith('-help') | param.startswith('--help') | param.startswith('--h'):
        help_message()
        exit()

#Gather all flight leg files and arange/sort them in a list
lst_seg_files = sorted(glob.glob('*.FL*.cap'))



#make a list of the total posible number of flight legs
# leg_lst = list(np.arange(1,16))
# leg_lst = [str(x) for x in leg_lst]

#make a data dictionary
data_dict = {}

#make list of maximum and minimum DFC values
max_dfc_fl = []
min_dfc_fl = []
FL_numbers = []

#loop through each flight leg file and read in the data
for i in lst_seg_files:
    leg = ADPAA()
    leg.ReadFile(i)
    data = leg.data
    
    #grab the filename info
    name_elements = i.split('.')
    yy = name_elements[0][0:2]
    mm = name_elements[0][3:5]
    dd = name_elements[0][6:8]
    hh = name_elements[0][9:11]
    mi = name_elements[0][12:14]
    ss = name_elements[0][15:17]
    
    FL_num = name_elements[1][:]
    FL_numbers.append(FL_num)
    
    #make a datafram of the data
    df_data = pd.DataFrame(data)
    df_data.rename(columns = {'CIPV_105-31':'CIPV_105_31'}, inplace = True)

    
    #Turn null data in NaN
    #but first, need to remove time so that does not become a nan value
    Time = df_data.iloc[:,0]
    df_data = df_data.loc[:, df_data.columns != 'Time'] 
    df_data[df_data == 0.0] = np.nan
    
    df_data[df_data['CIPV_495um'] < 10] = np.nan
    df_data[df_data['CIPV_105um'] < 10] = np.nan
    df_data[df_data['CIPV_105_31'] < 10] = np.nan
    df_data[df_data['RCAC_nc'] > 999] = np.nan
    df_data[df_data['RCAC_all'] > 999] = np.nan
    
    df_data = pd.concat([Time, df_data], axis = 1)
    #Convert the CIP data to #/cm^3
    df_data['CIPV_495um'] = df_data['CIPV_495um'] / 1e6
    df_data['CIPV_105um'] = df_data['CIPV_105um'] / 1e6
    df_data['CIPV_105_31'] = df_data['CIPV_105_31'] / 1e6

    #Create 20-pt Moving Averages for the CIP and RCAC data
    df_data[ 'twenty_pt_rolling_avg_105' ] = df_data.CIPV_105um.rolling(20,center=True).mean()
    df_data[ 'twenty_pt_rolling_avg_495' ] = df_data.CIPV_495um.rolling(20,center=True).mean()
    df_data[ 'twenty_pt_rolling_avg_105_315' ] = df_data.CIPV_105_31.rolling(20,center=True).mean()
    df_data[ 'twenty_pt_rolling_avg_RCAC_all' ] = df_data.RCAC_all.rolling(20,center=True).mean()
    df_data[ 'twenty_pt_rolling_avg_RCAC_nc' ] = df_data.RCAC_nc.rolling(20,center=True).mean()
    
    #In order to avoid plotting between the DFC gaps we must add a row of nan's
    #between the transition of neg & pos or pos & neg DFC values.
    #We must first recognize if the first and last value is pos or neg in order to have the 
    #correct order or DFC values.
    
    if 'DFC' in df_data.columns:
        df_data.rename(columns = {'DFC':'Distance'}, inplace = True)
    
    else:
        print('Do no column manipulation')

    # if first_value < 0 and last_value > 0:
    #     # print('first value is negative and the last value is positive')
    #     neg_DFC_values_df = df_data[df_data['Distance'] < 0]
    #     pos_DFC_values_df = df_data[df_data['Distance'] > 0]
    #     #create and insert nan row in order to avoid plotting gaps.
    #     nan = np.empty((1,len(df_data.columns)))
    #     nan[:] = np.nan
    #     nan_df = pd.DataFrame(nan, columns = df_data.columns)

    #     #concat the data with the neg first, then nan, the pos
    #     df_data = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)

    # elif first_value > 0 and last_value < 0:
    #     # print('first value is postive and the last value is negative')
    #     neg_DFC_values_df = df_data[df_data['Distance'] < 0]
    #     pos_DFC_values_df = df_data[df_data['Distance'] > 0]
    #     #create and insert nan row in order to avoid plotting gaps.
    #     nan = np.empty((1,len(df_data.columns)))
    #     nan[:] = np.nan
    #     nan_df = pd.DataFrame(nan, columns = df_data.columns)

    #     #concat the data with the neg first, then nan, the pos
    #     df_data = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
    # elif first_value > 0 and last_value > 0:
    #     print('The aircraft is always North of the cell')
    #     print('No need to manipulate the DFC data.')
    # elif first_value < 0 and last_value < 0:
    #     print('The aircraft is always South of the cell')
    #     print('No need to manipulate the DFC data.')

    #Grab first and last SFM data point and convert to HH:MM:SS
    #First (inital FL time segment)
    time_first = df_data.Time[0]
    day_first = time_first // (24 * 3600)
    time_first = time_first% (24 * 3600)
    hour_first = time_first // 3600
    time_first %= 3600
    minutes_first = time_first // 60
    time_first %= 60
    seconds_first = time_first

    # Define time FL1 intial time segment.
    df_data_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
    
    #Last (final FL time segment)
    time_last = df_data['Time'].tail(1)
    time_last = float(time_last)
    day_last = time_last // (24 * 3600)
    time_last = time_last% (24 * 3600)
    hour_last = time_last // 3600
    time_last %= 3600
    minutes_last = time_last // 60
    time_last %= 60
    seconds_last = time_last

    # Define time FL1 intial time segment.
    df_data_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last)

    #math operation to round down min DFC value to nearest multiple of 10
    def round_down(num, divisor):
        return num - (num%divisor)
    
    def round_up(num, divisor):
        return num + (divisor - num%divisor)
    
    dfc_min = round_down(df_data['Distance'].min(),10)
    dfc_max = round_up(df_data['Distance'].max(),10)
    
    #append values to list
    max_dfc_fl.append(dfc_max)
    min_dfc_fl.append(dfc_min)

    
    #detect RCACnc outliers
    outliers = []
    def detect_outlier(data):
        
        #threshold of 5 standard deviations
        threshold = 5
        mean = np.mean(data)
        std = np.std(data)
        
        for y in data:
            z_score = (y - mean) / std
            if np.abs(z_score) > threshold:
                outliers.append(y)
        
        return outliers
    
    outliers_data = detect_outlier(df_data['RCAC_nc'])
    print(outliers_data)
     
    

    #need to remove time from main data again and then concat the time back
    #after some data manipulation in finding the outliers
    Time2 = df_data.iloc[:,0]
    df_data = df_data.loc[:, df_data.columns != 'Time']
    
    #define empty list for the RCAC maximum (for plotting stuff)
    RCAC_maximum = []
    #remove outliers
    if outliers_data:
        outliers_data = np.array(outliers_data)
        df_data[df_data['RCAC_nc'] >= outliers_data.min()] = np.nan
        
        #round RCACnc max value to nearest multiple of 2
        RCACnc_max = round_up(df_data['RCAC_nc'].max(),2)
        RCAC_maximum.append(RCACnc_max)   
    
    else:
        RCAC_nc_max = df_data['RCAC_nc']
        RCAC_nc_max = RCAC_nc_max.max()        
        RCACnc_max_non_outliers = round_up(RCAC_nc_max,2)
        RCAC_maximum.append(RCACnc_max_non_outliers)
    
    RCAC_maximum = np.array(RCAC_maximum)
    #add back in time
    df_data = pd.concat([Time2, df_data], axis = 1)
    
    ######################################################################
    #Begin Plotting for extended FL plots for CIP data
    ########## RCAC_nc Plotting #########
    # fig = plt.figure(figsize=(12, 12), facecolor='white')
    # plt.rcParams['axes.facecolor']='white'
    # plt.rcParams['axes.xmargin'] = 0
    # plt.rcParams['axes.ymargin'] = 0

    
    # plt.scatter(df_data.Distance, df_data.RCAC_nc, c=df_data.Time, s=25, marker='o')
    
    # # plt.plot(df_data.Distance, df_data.twenty_pt_rolling_avg_RCAC_all, c="black", linestyle='-',linewidth=3)
    # plt.xlabel('Distance From Core (km)',fontsize=26)
    # plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
    
    # plt.xlim(dfc_min, dfc_max)
    # plt.xticks(np.arange(dfc_min, dfc_max + 1, 10), fontsize=21)
    # plt.ylim(0,RCAC_maximum)
    # plt.yticks(np.arange(0, RCAC_maximum + 1, 2), fontsize=21)
    # plt.hlines(y=0.5, xmin=0, xmax=100, linewidth = 3, linestyles = '--', color = 'k')

        
    # plt.title(FL_num, fontsize=26)
    # plt.grid()
    # plt.show()     
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,14))
    fig.tight_layout()
    

    plot1 = ax1.scatter(df_data.Distance, df_data.RCAC_nc, c=df_data.Time, s=50, marker='o')
    plot1a = ax1.plot(df_data.Distance, df_data.twenty_pt_rolling_avg_RCAC_nc, c="black", linestyle='-',linewidth=3)
    ax1.set_ylim(0,RCAC_maximum)
    ax1.set_title(FL_num, fontsize=32)
    ax1.set_ylabel(r'$RCAC_{N - C}$', fontsize = 30)
    ax1.tick_params(axis='y', labelsize = 25)
    ax1.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
    ax1.set_xlim(dfc_min, dfc_max)
    # ax1.set_xlabel('Distance From Core (km)', fontsize = 30)
    # ax1.tick_params(axis='x', labelsize = 18)
    ax1.tick_params(axis='x', bottom = 'off', labelbottom = 'off')
    ax1.set_xticklabels([])


    plot2 = ax2.scatter(df_data.Distance, df_data.CIPV_105um, c=df_data.Time, s=50, marker='o')
    ax2.set_ylim(0,df_data['CIPV_105um'].max())
    # ax2.set_title(FL_num, fontsize=32)
    ax2.set_ylabel('Total Particle Conc. (#/cm^3)', fontsize = 30)
    ax2.tick_params(axis='y', labelsize = 25)
    ax2.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
    ax2.set_xlim(dfc_min, dfc_max)
    ax2.set_xlabel('Distance From Core (km)', fontsize = 30)
    ax2.tick_params(axis='x', labelsize = 25)

    # save figure(s)
    plt.savefig(yy + mm + dd + '_' + 'CIP_V_RCACnc_' + FL_num + '.png', bbox_inches='tight')

######### Next plotting routine ###################

    #save flight leg info into dictionary
    key = f'{FL_num}'
    df_data_np = df_data.to_numpy()
    data_dict[key] = dict(zip(df_data.columns, df_data_np.T))
  
#find maximum and minimum DFC value for entire flight
flight_dfc_max = max(max_dfc_fl)
flight_dfc_min = min(min_dfc_fl)


#Let's generate some random X, Y data X = [ [frst group],[second group] ...]
X = [ [randint(0,50) for i in range(0,5)] for i in range(0,24)]

labels = range(1,len(X)+1)

fig = plt.figure(figsize=(16,16))
ax = fig.add_subplot(111)
for x,lab in zip(data_dict.values(),FL_numbers):
        # ax.scatter(x['Distance'],x['RCAC_nc'],label=lab, marker='o',s=50)
        ax.plot(x['Distance'], x['twenty_pt_rolling_avg_RCAC_nc'],label=lab, linestyle='-',linewidth=3)
        ax.set_xlim(flight_dfc_min, flight_dfc_max)
        ax.set_ylim(0,6)
        ax.set_ylabel(r'$RCAC_{N - C}$', fontsize = 30)
        ax.set_xlabel('Distance From Core (km)', fontsize = 30)
        ax.tick_params(axis='y', labelsize = 25)
        ax.grid(which = 'major', axis = 'x', linestyle = '--', linewidth = 3)
        ax.tick_params(axis='x', labelsize=25)
        ax.set_title('All Flight Legs', fontsize=30)
        #Now this is actually the code that you need, an easy fix your colors just cut and paste not you need ax.
        colormap = plt.cm.gist_ncar #nipy_spectral, Set1,Paired  
        colorst = [colormap(i) for i in np.linspace(0, 0.9,len(ax.collections))]       
        for t,j1 in enumerate(ax.collections):
            j1.set_color(colorst[t])
        
        ax.legend(fontsize=20)
        
        plt.savefig(yy + mm + dd + '_' + 'CIP_V_RCACnc_ALL' + '.png')











#%%
# ########
# user_input = input("Enter the path of your file as well as the data file (~/PATH/TO/FILE/data_file): ")
 
# assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
# f = open(user_input,'r+')
# print("Hooray we found your file!")

# ##########

# date_input = input('Enter the date of the data youre trying to plot (e.g., 20190730): ')
# time_input = input('Enter the column number for the Time data: ') #0
# time_input = int(time_input)
# distance_from_core_input = input('Enter the column number for the Distance From Core data: ') #34
# distance_from_core_input = int(distance_from_core_input)
# cip495_input = input('Enter the column number for the CIP > 495um data: ') #35
# cip495_input = int(cip495_input)
# cip105_input = input('Enter the column number for the CIP < 105um data: ') #36
# cip105_input = int(cip105_input)
# cip105_315_input = input('Enter the column number for the CIP 105 - 315um data: ') #37
# cip105_315_input = int(cip105_315_input)

# #TESTING
# # date_input = '20190730'
# # time_input = 0
# # distance_from_core_input = 34
# # cip495_input = 35
# # cip105_input = 36
# # cip105_315_input = 37
# # cap_np = np.loadtxt(path + filename, skiprows=55, usecols=(time_input, distance_from_core_input, cip495_input, cip105_input, cip105_315_input))


# cap_np = np.loadtxt(user_input, skiprows=55, usecols=(time_input, distance_from_core_input, cip495_input, cip105_input, cip105_315_input))



# column_names = ['Time', 'DFC', 'CIP_495', 'CIP_105', 'CIP_105_315']
# cap_df = pd.DataFrame(cap_np,columns=column_names)

# #turn null values to NaN

# cap_df[cap_df == 0.0] = np.nan
# cap_df[cap_df['CIP_495'] < 10] = np.nan
# cap_df[cap_df['CIP_105'] < 10] = np.nan
# cap_df[cap_df['CIP_105_315'] < 10] = np.nan

# #Turn CIP #/m^3 to #/cm^3
# cap_df['CIP_495'] = cap_df['CIP_495'] / 1e6
# cap_df['CIP_105'] = cap_df['CIP_105'] / 1e6
# cap_df['CIP_105_315'] = cap_df['CIP_105_315'] / 1e6

# cap_df['CIP_495_div_105'] = cap_df['CIP_495'] / cap_df['CIP_105']
# cap_df['CIP_495_div_105_315'] = cap_df['CIP_495'] / cap_df['CIP_105_315']

# #Set flight legs by user input and then subset the total cap file.
# while True:
#     prompt1=input('Do you have time [SFM] bounds for Flight Leg 1? yes/no: ').lower()
#     if prompt1 == 'yes':
#         FL1_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 1: ')
#         FL1_lower = int(FL1_lower)
#         FL1_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 1: ')
#         FL1_upper = int(FL1_upper)        
        
#         #subset cap file
#         FL1_df = cap_df[(cap_df.Time >= FL1_lower) & (cap_df.Time <= FL1_upper)]
        
#         #compute 20-point MA
#         FL1_df[ 'twenty_pt_rolling_avg_105' ] = FL1_df.CIP_105.rolling(20,center=True).mean()
#         FL1_df[ 'twenty_pt_rolling_avg_495' ] = FL1_df.CIP_495.rolling(20,center=True).mean()
#         FL1_df[ 'twenty_pt_rolling_avg_105_315' ] = FL1_df.CIP_105_315.rolling(20,center=True).mean()
#         FL1_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL1_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL1_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL1_df.CIP_495_div_105_315.rolling(20,center=True).mean()
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL1_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL1_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL1_df[FL1_df['DFC'] < 0]
#             pos_DFC_values_df = FL1_df[FL1_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL1_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL1_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL1_df[FL1_df['DFC'] < 0]
#             pos_DFC_values_df = FL1_df[FL1_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL1_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL1_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
        
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL1_df.Time[0]
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL1_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL1_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL1_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)        
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL1 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL1_df.DFC, FL1_df.CIP_495_div_105_315, c=FL1_df.Time, s=25, marker='o')
        
#         plt.plot(FL1_df.DFC, FL1_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL1 \n' + FL1_time_first + '-' + FL1_time_last + ' ' + 'UTC' ,fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL1.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL1
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL1_df.DFC, FL1_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL1 > 495 ' u"\u03bcm"'')
#         plt.plot(FL1_df.DFC, FL1_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL1 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL1 -- 20 pt. Rolling Averages \n' + FL1_time_first + '-' + FL1_time_last + ' ' + 'UTC' ,fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL1.png')
        
        
#     elif prompt1 == 'no':
#        print('This script requires defined flight legs')
#        break
#     prompt2=input('Do you have time [SFM] bounds for Flight Leg 2? yes/no: ')
#     if prompt2 == 'yes':
#         FL2_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 2: ')
#         FL2_lower = int(FL2_lower)
#         FL2_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 2: ')
#         FL2_upper = int(FL2_upper)
#         FL2_df = cap_df[(cap_df.Time >= FL2_lower) & (cap_df.Time <= FL2_upper)]
          
#         #compute 20-point MA
#         FL2_df[ 'twenty_pt_rolling_avg_105' ] = FL2_df.CIP_105.rolling(20,center=True).mean()
#         FL2_df[ 'twenty_pt_rolling_avg_495' ] = FL2_df.CIP_495.rolling(20,center=True).mean()
#         FL2_df[ 'twenty_pt_rolling_avg_105_315' ] = FL2_df.CIP_105_315.rolling(20,center=True).mean()
#         FL2_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL2_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL2_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL2_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL2_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL2_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL2_df[FL2_df['DFC'] < 0]
#             pos_DFC_values_df = FL2_df[FL2_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL2_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL2_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL2_df[FL2_df['DFC'] < 0]
#             pos_DFC_values_df = FL2_df[FL2_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL2_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL2_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL2_df.Time[0]
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL2_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL2_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL2_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)              
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL2 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL2_df.DFC, FL2_df.CIP_495_div_105_315, c=FL2_df.Time, s=25, marker='o')
        
#         plt.plot(FL2_df.DFC, FL2_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL2_df['DFC'].min(), FL2_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL2 \n' + FL2_time_first + '-' + FL2_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL2.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL2
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL2_df.DFC, FL2_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL2 > 495 ' u"\u03bcm"'')
#         plt.plot(FL2_df.DFC, FL2_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL2 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL2_df['DFC'].min(), FL2_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL2 -- 20 pt. Rolling Averages \n' + FL2_time_first + '-' + FL2_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL2.png')
        
#     elif prompt2 == 'no':
#         break
#     prompt3=input('Do you have time [SFM] bounds for Flight Leg 3? yes/no: ')
#     if prompt3 == 'yes':
#         FL3_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 3: ')
#         FL3_lower = int(FL3_lower)
#         FL3_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 3: ')
#         FL3_upper = int(FL3_upper)   
#         FL3_df = cap_df[(cap_df.Time >= FL3_lower) & (cap_df.Time <= FL3_upper)]
        
#         #compute 20-point MA
#         FL3_df[ 'twenty_pt_rolling_avg_105' ] = FL3_df.CIP_105.rolling(20,center=True).mean()
#         FL3_df[ 'twenty_pt_rolling_avg_495' ] = FL3_df.CIP_495.rolling(20,center=True).mean()
#         FL3_df[ 'twenty_pt_rolling_avg_105_315' ] = FL3_df.CIP_105_315.rolling(20,center=True).mean()
#         FL3_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL3_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL3_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL3_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL3_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL3_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL3_df[FL3_df['DFC'] < 0]
#             pos_DFC_values_df = FL3_df[FL3_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL3_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL3_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL3_df[FL3_df['DFC'] < 0]
#             pos_DFC_values_df = FL3_df[FL3_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL3_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL3_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL3_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL3_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL3_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL3_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)             
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL3 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL3_df.DFC, FL3_df.CIP_495_div_105_315, c=FL3_df.Time, s=25, marker='o')
        
#         plt.plot(FL3_df.DFC, FL3_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL3_df['DFC'].min(), FL3_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL3 \n' + FL3_time_first + '-' + FL3_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL3.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL3
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL3_df.DFC, FL3_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL3 > 495 ' u"\u03bcm"'')
#         plt.plot(FL3_df.DFC, FL3_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL3 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL3_df['DFC'].min(), FL3_df['DFC'].max())        
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL3 -- 20 pt. Rolling Averages \n' + FL3_time_first + '-' + FL3_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL3.png')
        
#     elif prompt3 == 'no':
#         break  
#     prompt4=input('Do you have time [SFM] bounds for Flight Leg 4? yes/no: ')
#     if prompt4 == 'yes':
#         FL4_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 4: ')
#         FL4_lower = int(FL4_lower)
#         FL4_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 4: ')
#         FL4_upper = int(FL4_upper)   
#         FL4_df = cap_df[(cap_df.Time >= FL4_lower) & (cap_df.Time <= FL4_upper)]
        
#         #compute 20-point MA
#         FL4_df[ 'twenty_pt_rolling_avg_105' ] = FL4_df.CIP_105.rolling(20,center=True).mean()
#         FL4_df[ 'twenty_pt_rolling_avg_495' ] = FL4_df.CIP_495.rolling(20,center=True).mean()
#         FL4_df[ 'twenty_pt_rolling_avg_105_315' ] = FL4_df.CIP_105_315.rolling(20,center=True).mean()
#         FL4_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL4_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL4_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL4_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL4_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL4_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL4_df[FL4_df['DFC'] < 0]
#             pos_DFC_values_df = FL4_df[FL4_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL4_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL4_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL4_df[FL4_df['DFC'] < 0]
#             pos_DFC_values_df = FL4_df[FL4_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL4_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL4_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL4_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL4_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL4_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL4_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)             
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL4 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL4_df.DFC, FL4_df.CIP_495_div_105_315, c=FL4_df.Time, s=25, marker='o')
        
#         plt.plot(FL4_df.DFC, FL4_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL4_df['DFC'].min(), FL4_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL4 \n' + FL4_time_first + '-' + FL4_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL4.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL4
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL4_df.DFC, FL4_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL4 > 495 ' u"\u03bcm"'')
#         plt.plot(FL4_df.DFC, FL4_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL4 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL4_df['DFC'].min(), FL4_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL4 -- 20 pt. Rolling Averages \n' + FL4_time_first + '-' + FL4_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL4.png')
        
#     elif prompt4 == 'no':
#         break  
#     prompt5=input('Do you have time [SFM] bounds for Flight Leg 5? yes/no: ')
#     if prompt5 == 'yes':
#         FL5_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 5: ')
#         FL5_lower = int(FL5_lower)
#         FL5_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 5: ')
#         FL5_upper = int(FL5_upper) 
#         FL5_df = cap_df[(cap_df.Time >= FL5_lower) & (cap_df.Time <= FL5_upper)]
        
#         #compute 20-point MA
#         FL5_df[ 'twenty_pt_rolling_avg_105' ] = FL5_df.CIP_105.rolling(20,center=True).mean()
#         FL5_df[ 'twenty_pt_rolling_avg_495' ] = FL5_df.CIP_495.rolling(20,center=True).mean()
#         FL5_df[ 'twenty_pt_rolling_avg_105_315' ] = FL5_df.CIP_105_315.rolling(20,center=True).mean()
#         FL5_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL5_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL5_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL5_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL5_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL5_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL5_df[FL5_df['DFC'] < 0]
#             pos_DFC_values_df = FL5_df[FL5_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL5_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL5_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL5_df[FL5_df['DFC'] < 0]
#             pos_DFC_values_df = FL5_df[FL5_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL5_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL5_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL5_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL5_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL5_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL5_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)             
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL5 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL5_df.DFC, FL5_df.CIP_495_div_105_315, c=FL5_df.Time, s=25, marker='o')
        
#         plt.plot(FL5_df.DFC, FL5_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL5_df['DFC'].min(), FL5_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL5 \n' + FL5_time_first + '-' + FL5_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL5.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL5
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL5_df.DFC, FL5_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL5 > 495 ' u"\u03bcm"'')
#         plt.plot(FL5_df.DFC, FL5_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL5 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL5_df['DFC'].min(), FL5_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL5 \n' + FL5_time_first + '-' + FL5_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL5.png')      
        
#     elif prompt5 == 'no':
#         break  
#     prompt6=input('Do you have time [SFM] bounds for Flight Leg 6? yes/no: ').lower()
#     if prompt6 == 'yes':
#         FL6_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 6: ')
#         FL6_lower = int(FL6_lower)
#         FL6_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 6: ')
#         FL6_upper = int(FL6_upper)
#         FL6_df = cap_df[(cap_df.Time >= FL6_lower) & (cap_df.Time <= FL6_upper)]
        
#         #compute 20-point MA
#         FL6_df[ 'twenty_pt_rolling_avg_105' ] = FL6_df.CIP_105.rolling(20,center=True).mean()
#         FL6_df[ 'twenty_pt_rolling_avg_495' ] = FL6_df.CIP_495.rolling(20,center=True).mean()
#         FL6_df[ 'twenty_pt_rolling_avg_105_315' ] = FL6_df.CIP_105_315.rolling(20,center=True).mean()
#         FL6_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL6_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL6_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL6_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL6_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL6_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL6_df[FL6_df['DFC'] < 0]
#             pos_DFC_values_df = FL6_df[FL6_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL6_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL6_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL6_df[FL6_df['DFC'] < 0]
#             pos_DFC_values_df = FL6_df[FL6_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL6_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL6_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL6_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL6_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL6_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL6_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)             
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL5 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL6_df.DFC, FL6_df.CIP_495_div_105_315, c=FL6_df.Time, s=25, marker='o')
        
#         plt.plot(FL6_df.DFC, FL6_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL6_df['DFC'].min(), FL6_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL6 \n' + FL6_time_first + '-' + FL6_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL6.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL6
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL6_df.DFC, FL6_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL6 > 495 ' u"\u03bcm"'')
#         plt.plot(FL6_df.DFC, FL6_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL6 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL6_df['DFC'].min(), FL6_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL6 -- 20 pt. Rolling Averages \n' + FL6_time_first + '-' + FL6_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL6.png')     
        
#     elif prompt6 == 'no':
#        break
#     prompt7=input('Do you have time [SFM] bounds for Flight Leg 7? yes/no: ')
#     if prompt7 == 'yes':
#         FL7_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 7: ')
#         FL7_lower = int(FL7_lower)
#         FL7_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 7: ')
#         FL7_upper = int(FL7_upper)
#         FL7_df = cap_df[(cap_df.Time >= FL7_lower) & (cap_df.Time <= FL7_upper)]
        
#         #compute 20-point MA
#         FL7_df[ 'twenty_pt_rolling_avg_105' ] = FL7_df.CIP_105.rolling(20,center=True).mean()
#         FL7_df[ 'twenty_pt_rolling_avg_495' ] = FL7_df.CIP_495.rolling(20,center=True).mean()
#         FL7_df[ 'twenty_pt_rolling_avg_105_315' ] = FL7_df.CIP_105_315.rolling(20,center=True).mean()
#         FL7_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL7_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL7_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL7_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL7_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL7_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL7_df[FL7_df['DFC'] < 0]
#             pos_DFC_values_df = FL7_df[FL7_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL7_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL7_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL7_df[FL7_df['DFC'] < 0]
#             pos_DFC_values_df = FL7_df[FL7_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL7_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL7_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL7_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL7_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL7_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL7_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)              
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL7 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL7_df.DFC, FL7_df.CIP_495_div_105_315, c=FL7_df.Time, s=25, marker='o')
        
#         plt.plot(FL7_df.DFC, FL7_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL7_df['DFC'].min(), FL7_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL7 \n' + FL7_time_first + '-' + FL7_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL7.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL7
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL7_df.DFC, FL7_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL7 > 495 ' u"\u03bcm"'')
#         plt.plot(FL7_df.DFC, FL7_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL7 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL7_df['DFC'].min(), FL7_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL7 -- 20 pt. Rolling Averages \n' + FL7_time_first + '-' + FL7_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL7.png')
        
#     elif prompt7 == 'no':
#         break
#     prompt8=input('Do you have time [SFM] bounds for Flight Leg 8? yes/no: ')
#     if prompt8 == 'yes':
#         FL8_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 8: ')
#         FL8_lower = int(FL8_lower)
#         FL8_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 8: ')
#         FL8_upper = int(FL8_upper)    
#         FL8_df = cap_df[(cap_df.Time >= FL8_lower) & (cap_df.Time <= FL8_upper)]
        
#         #compute 20-point MA
#         FL8_df[ 'twenty_pt_rolling_avg_105' ] = FL8_df.CIP_105.rolling(20,center=True).mean()
#         FL8_df[ 'twenty_pt_rolling_avg_495' ] = FL8_df.CIP_495.rolling(20,center=True).mean()
#         FL8_df[ 'twenty_pt_rolling_avg_105_315' ] = FL8_df.CIP_105_315.rolling(20,center=True).mean()
#         FL8_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL8_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL8_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL8_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL8_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL8_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL8_df[FL8_df['DFC'] < 0]
#             pos_DFC_values_df = FL8_df[FL8_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL8_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL8_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL8_df[FL8_df['DFC'] < 0]
#             pos_DFC_values_df = FL8_df[FL8_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL8_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL8_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL8_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL8_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL8_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL8_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)              
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL8 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL8_df.DFC, FL8_df.CIP_495_div_105_315, c=FL8_df.Time, s=25, marker='o')
        
#         plt.plot(FL8_df.DFC, FL8_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL8_df['DFC'].min(), FL8_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL8 \n' + FL8_time_first + '-' + FL8_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL8.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL8
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL8_df.DFC, FL8_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL8 > 495 ' u"\u03bcm"'')
#         plt.plot(FL8_df.DFC, FL8_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL8 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL8_df['DFC'].min(), FL8_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL8 -- 20 pt. Rolling Averages \n' + FL8_time_first + '-' + FL8_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL8.png')        
        
#     elif prompt8 == 'no':
#         break  
#     prompt9=input('Do you have time [SFM] bounds for Flight Leg 9? yes/no: ')
#     if prompt9 == 'yes':
#         FL9_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 9: ')
#         FL9_lower = int(FL9_lower)
#         FL9_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 9: ')
#         FL9_upper = int(FL9_upper)   
#         FL9_df = cap_df[(cap_df.Time >= FL9_lower) & (cap_df.Time <= FL9_upper)]
        
#         #compute 20-point MA
#         FL9_df[ 'twenty_pt_rolling_avg_105' ] = FL9_df.CIP_105.rolling(20,center=True).mean()
#         FL9_df[ 'twenty_pt_rolling_avg_495' ] = FL9_df.CIP_495.rolling(20,center=True).mean()
#         FL9_df[ 'twenty_pt_rolling_avg_105_315' ] = FL9_df.CIP_105_315.rolling(20,center=True).mean()
#         FL9_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL9_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL9_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL9_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL9_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL9_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL9_df[FL9_df['DFC'] < 0]
#             pos_DFC_values_df = FL9_df[FL9_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL9_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL9_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL9_df[FL9_df['DFC'] < 0]
#             pos_DFC_values_df = FL9_df[FL9_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL9_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL9_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL9_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL9_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL9_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL9_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)              
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL9 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL9_df.DFC, FL9_df.CIP_495_div_105_315, c=FL9_df.Time, s=25, marker='o')
        
#         plt.plot(FL9_df.DFC, FL9_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL9_df['DFC'].min(), FL9_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL9 \n' + FL9_time_first + '-' + FL9_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL9.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL9
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL9_df.DFC, FL9_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL9 > 495 ' u"\u03bcm"'')
#         plt.plot(FL9_df.DFC, FL9_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL9 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL9_df['DFC'].min(), FL9_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL9 -- 20 pt. Rolling Averages \n' + FL9_time_first + '-' + FL9_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL9.png')        
        
#     elif prompt9 == 'no':
#         break  
#     prompt10=input('Do you have time [SFM] bounds for Flight Leg 10? yes/no: ')
#     if prompt10 == 'yes':
#         FL10_lower = input('Please enter the time [SFM] lower-bound for Flight Leg 10: ')
#         FL10_lower = int(FL10_lower)
#         FL10_upper = input('Please enter the time [SFM] upper-bound for Flight Leg 10: ')
#         FL10_upper = int(FL10_upper)  
#         FL10_df = cap_df[(cap_df.Time >= FL10_lower) & (cap_df.Time <= FL10_upper)]
        
#         #compute 20-point MA
#         FL10_df[ 'twenty_pt_rolling_avg_105' ] = FL10_df.CIP_105.rolling(20,center=True).mean()
#         FL10_df[ 'twenty_pt_rolling_avg_495' ] = FL10_df.CIP_495.rolling(20,center=True).mean()
#         FL10_df[ 'twenty_pt_rolling_avg_105_315' ] = FL10_df.CIP_105_315.rolling(20,center=True).mean()
#         FL10_df[ 'twenty_pt_rolling_avg_495_div_105' ] = FL10_df.CIP_495_div_105.rolling(20,center=True).mean()
#         FL10_df[ 'twenty_pt_rolling_avg_495_div_105_315' ] = FL10_df.CIP_495_div_105_315.rolling(20,center=True).mean()
        
#         ######################################################################
#         #In order to avoid plotting between the DFC gaps we must add a row of nan's
#         #between the transition of neg & pos or pos & neg DFC values.
#         #We must first recognize if the first and last value is pos or neg in order to have the 
#         #correct order or DFC values.
#         first = FL10_df['DFC'].head(1)
#         first_value = float(first)
        
#         last = FL10_df['DFC'].tail(1)
#         last_value = float(last)
        
#         if first_value < 0 and last_value > 0:
#             # print('first value is negative and the last value is positive')
#             neg_DFC_values_df = FL10_df[FL10_df['DFC'] < 0]
#             pos_DFC_values_df = FL10_df[FL10_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL10_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL10_df = pd.concat([neg_DFC_values_df, nan_df, pos_DFC_values_df], ignore_index=True)
            
#         elif first_value > 0 and last_value < 0:
#             # print('first value is postive and the last value is negative')
#             neg_DFC_values_df = FL10_df[FL10_df['DFC'] < 0]
#             pos_DFC_values_df = FL10_df[FL10_df['DFC'] > 0]
#             #create and insert nan row in order to avoid plotting gaps.
#             nan = np.empty((1,12))
#             nan[:] = np.nan
#             nan_df = pd.DataFrame(nan, columns = FL10_df.columns)
            
#             #concat the data with the neg first, then nan, the pos
#             FL10_df = pd.concat([pos_DFC_values_df, nan_df, neg_DFC_values_df], ignore_index=True)
#         elif first_value > 0 and last_value > 0:
#             print('nothing to do DFC data manipulation wise')
#         elif first_value < 0 and last_value < 0:
#             print('nothing to do DFC data manipulation wise')
            
#         ######################################################################
#         #Grab first and last SFM data point and convert to HH:MM:SS
#         #First (inital FL time segment)
#         time_first = FL10_df['Time'].head(1)
#         time_first = float(time_first)
#         day_first = time_first // (24 * 3600)
#         time_first = time_first% (24 * 3600)
#         hour_first = time_first // 3600
#         time_first %= 3600
#         minutes_first = time_first // 60
#         time_first %= 60
#         seconds_first = time_first

#         # Define time FL1 intial time segment.
#         FL10_time_first = "%02d:%02d:%02d" % (hour_first,minutes_first,seconds_first)
        
#         #Last (final FL time segment)
#         time_last = FL10_df['Time'].tail(1)
#         time_last = float(time_last)
#         day_last = time_last // (24 * 3600)
#         time_last = time_last% (24 * 3600)
#         hour_last = time_last // 3600
#         time_last %= 3600
#         minutes_last = time_last // 60
#         time_last %= 60
#         seconds_last = time_last

#         # Define time FL1 intial time segment.
#         FL10_time_last = "%02d:%02d:%02d" % (hour_last,minutes_last,seconds_last + 1)              
        
#         ######################################################################
#         #Begin Plotting for extended FL plots for CIP data
#         #Figures showing the CIP495um divided by CIP 105 - 315um
#         ########## FL10 Plotting #########
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
    
        
#         plt.scatter(FL10_df.DFC, FL10_df.CIP_495_div_105_315, c=FL10_df.Time, s=25, marker='o')
        
#         plt.plot(FL10_df.DFC, FL10_df.twenty_pt_rolling_avg_495_div_105_315, c="black", linestyle='-',linewidth=3)
#         plt.hlines(y=0.5, xmin=-100, xmax=100, linewidth = 3, linestyles = '--', color = 'k')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         #invert x axis
#         # plt.xlim(max(FL1_cap_df['DFC']), min(FL1_cap_df['DFC']))
#         plt.ylabel(r'$RCAC_{N - C}$',fontsize=30)
#         plt.xlim(FL10_df['DFC'].min(), FL10_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yticks([0,0.5,1,1.5,2.0,2.5,3],fontsize=21)
#         plt.ylim(0,3)
#         plt.title('FL10 \n' + FL10_time_first + '-' + FL10_time_last + ' ' + 'UTC',fontsize=26)
#         #manually set color tick positions/number of ticks/tick labels
#         # v1 = np.linspace(FL1_cap_df['sfm'].min(), FL1_cap_df['sfm'].max(), 4, endpoint=True)
#         # cbar=plt.colorbar(ticks=v1)
#         # cbar.set_ticklabels(["15:51:15", "15:54:30", "15:57:45", "16:01:00"])
#         # cbar.ax.tick_params(labelsize=14)
#         plt.grid()
#         plt.savefig(date_input + '_' + 'CIP_V_RCACnc_FL10.png')
        
#         #plot the MA's for CIP > 495um, CIP 105-315um, CIP > 495um div 105-315 um
#         #FL10
#         fig = plt.figure(figsize=(12, 12), facecolor='white')
#         plt.rcParams['axes.facecolor']='white'
#         plt.rcParams['axes.xmargin'] = 0
#         plt.rcParams['axes.ymargin'] = 0
#         plt.plot(FL10_df.DFC, FL10_df.twenty_pt_rolling_avg_495, c="black", linestyle='-',linewidth=3, label = 'FL10 > 495 ' u"\u03bcm"'')
#         plt.plot(FL10_df.DFC, FL10_df.twenty_pt_rolling_avg_105_315, c="red", linestyle='-',linewidth=3, label = 'FL10 105 - 315 ' u"\u03bcm"'')
#         # plt.plot(FL1_cap_df.DFC, FL1_cap_df.twenty_pt_rolling_avg_495_div_105_315, c="green", linestyle='-',linewidth=3, label = 'FL1 > 495 / 105 - 315 ' u"\u03bcm"'')
#         plt.xlabel('Distance From Core (km)',fontsize=26)
#         plt.ylabel('Concentration (#/cm^3)',fontsize=26)
#         plt.xlim(FL10_df['DFC'].min(), FL10_df['DFC'].max())
#         # plt.xticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],fontsize=21)
#         plt.yscale('log') 
#         plt.yticks([1e-4,1e-3,1e-2,1e-1,1e0],fontsize=21)
#         plt.ylim(1e-4,1e0)
#         plt.title('FL10 -- 20 pt. Rolling Averages \n' + FL10_time_first + '-' + FL10_time_last + ' ' + 'UTC',fontsize=26)
#         plt.grid()
#         # plt.legend(loc='lower left', ncol=2, fontsize = 16, facecolor='white')
#         plt.savefig(date_input + '_' + 'CIP_V_chain-nonchain_roll-Avgs_FL10.png')        
        
#     elif prompt10 == 'no':
#         break
#     prompt11=input('Do you have time [SFM] bounds for Flight Leg 11? yes/no: ')
#     if prompt11 == 'yes':
#         print('You will need to adjust the code to add more flight legs')
#         break
#     else:
#        print('Answer yes or no.') #an answer that wouldn't be yes or no
       






