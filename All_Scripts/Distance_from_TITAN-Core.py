#!/bin/env python3 
"""
  NAME:
    Distance_from_TITAN-Core.py
 
  PURPOSE:
    The purpose of this script is to read in your science data and TITAN
    case track files to calculate the distance from reflectivity core centroid.
    
  CALLS:
    NONE

  EXAMPLE:
    The command:
        Distance_from_TITAN-Core.py <science_file> <case_track_file>
       

    If you have two flight legs - it creates three files. two files for
    individual flight legs and then one file that concatenates the two into one.
    creates: YY_MM_DD_HH_MI_SS.FL1.DFC; YY_MM_DD_HH_MI_SS.FL2.DFC
             YY_MM_DD_HH_MI_SS.DFC

  MODIFICATIONS:
    Christian Nairy <christian.nairy@und.edu> - 2022/09/30:
      Written...
      
  COPYRIGHT:
    2023 David Delene

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

#Imports
import os
import sys
import numpy as np
import pandas as pd
from adpaa_python3 import ADPAA
import glob


#Turn off pandas warnings - not needed here    
pd.options.mode.chained_assignment = None

# Define syntax. 
def help_message():
    print('\n')
    print('Syntax:Distance_from_TITAN-Core.py <-h>\n\n')
    print('  Example: Distance_from_TITAN-core.py <science_file> <case_track_file> \n')
    print('\n')
    print('NOTE: YOUR CASE TRACK FILE MUST ONLY HAVE THE SAME NUMBER OF LINES AS THE NUMBER OF FLIGHT LEGS.')
    print('      ALSO, YOU NEED TO ADD A FLIGHT LEG NUMBER COLUMN (FIRST COLLUMN) IN YOUR CASE TRACK FILE.')
    print('      YOU MUST RENAME THE END OF THE CASE TRACK FILE (*.segments)')
    print('\n')
    print('Example Case Track File: /nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190731_191704/Analysis/Flight_Legs/science_files/case_tracks_20190731.txt')

# Check input parameters. 
for param in sys.argv:
    if param.startswith('-h') | param.startswith('-help') | param.startswith('--help') | param.startswith('--h'):
        help_message()
        exit()



### TESTING ###
# path = "/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190729_191827/Analysis/Flight_legs/science_files/"
# file1 = '19_07_29_19_18_27.cap'
# file2 = 'case_tracks_20190729.txt'

# # Read in science file data
# sci_file = ADPAA()
# sci_file.ReadFile(path + file1)
# sci_data = sci_file.data

# # read in case track data
# case_tracks = np.genfromtxt(path + file2 ,usecols =(0,2,3,4,5,6,7,8,9,17,18,21))
###############



# call ADPAA
sci_file = ADPAA()
_infile = sys.argv[1]
sci_file.ReadFile(_infile)
sci_data = sci_file.data

_infile2 = sys.argv[2]
case_tracks = np.genfromtxt(_infile2, usecols =(0,2,3,4,5,6,7,8,9,17,18,21))

    
#define the column names of case track file (only the data that we need)
column_names_case_tracks = ['FL_Num','ComplexNum','SimpleNum','Year','Month','Day','Hour','Min','Sec','ReflCentroidLat(deg)','ReflCentroidLon(deg)','ReflCentroidZ(km)']

sci_file_df = pd.DataFrame.from_dict(sci_data)
df_case_tracks = pd.DataFrame(case_tracks, columns=column_names_case_tracks)

#Must convert the altitude form meter to kilometers
sci_file_df['POS_Alt'] = sci_file_df['POS_Alt'] / 1000

#Grab only the time, alt, lat, and lon from sci file (valuable data = val_data)
val_data = sci_file_df[['Time', 'POS_Alt', 'POS_Lat', 'POS_Lon']]

#import segment file
seg_file = glob.glob('*.segments')
seg = open(seg_file[0])
seg_data = np.genfromtxt(seg, delimiter=",", dtype=float, skip_header=1)

##########
#last FL number value
last_FL_val = seg_data[-1,0]

#convert last value to string
last_FL_val_str = str(int(last_FL_val))

#Split the flight leg times from segment file
n = np.array_split(seg_data, last_FL_val)

#Define the algorithm to produce distance from core calc.
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 3)

#get flight leg numbers
num_list = []
numbers = np.arange(1,100,1)
for x, y in zip(seg_data, numbers):
    if x[0] == y:
        num_list.append(str(y))

#empty dictionarys
dict_lst = {}
x_dist_dict = {}
corr_dist_dict = {}
final_dist_dict = {}

#empty lists
#empty array to append the distance data into.
X_distances_km = []
sep_distances = []
corr_dist = []

#loop through the data
for col, num in zip(seg_data, num_list):
    
    key = 'FL' + f'{num}'
    FL_num = int(col[0])
    

    # create a dictionary with flight leg values. then replace old total dict with this one.
    FL1_pd = val_data
    FL1_pd = FL1_pd[(FL1_pd['Time'] >= col[1]) & (FL1_pd['Time'] <= col[2])]

    FL1_case_track = df_case_tracks[(df_case_tracks['FL_Num'] == col[0])]  
    
    FL1_case_track_lat_lon = FL1_case_track[['ReflCentroidLat(deg)','ReflCentroidLon(deg)']]
        
    FL1_pd_lat_lon = FL1_pd[['POS_Lat','POS_Lon']]
        
    start_lat, start_lon = FL1_case_track[['ReflCentroidLat(deg)']], FL1_case_track[['ReflCentroidLon(deg)']]
    
    #convert start lat and lon of case track to float values
    start_lat = start_lat.to_numpy()
    start_lat = float(str(start_lat).strip('[]'))
    start_lon = start_lon.to_numpy()
    start_lon = float(str(start_lon).strip('[]'))
    
  
    #perform the distance calculation
    for row in FL1_pd_lat_lon.itertuples(index=False):
        X_distances_km.append(haversine_distance(start_lat, start_lon, row.POS_Lat, row.POS_Lon))
        x_dist_df = pd.DataFrame(X_distances_km, columns=['x_dist_km'])
        x_dist_dict[key] = x_dist_df
    X_distances_km.clear()




    #Calculate the altitude offset then calculate the accurate distance from core. Za - Alt of Aircraft......Zc - Alt of Reflectivity core centroid.
    Za_Zc = pd.DataFrame(FL1_pd['POS_Alt'].values - FL1_case_track['ReflCentroidZ(km)'].values, columns=['Alt_offset'])
    
    #perform pythagorean theorem for final distance data
    for k in x_dist_dict.values():
        dist_data = pd.DataFrame.from_dict(k)
        for j in Za_Zc.values:
            Distance_squared = pd.DataFrame((j**2) + (dist_data['x_dist_km'].values**2), columns=['distance^2'])
            distance_final = pd.DataFrame((Distance_squared['distance^2'].values**0.5), columns=['DFC'])
    corr_dist_dict[key] = distance_final

    

    #append time and the data into dictionarys    
    for x in corr_dist_dict.values():
        corr_dist_data = pd.DataFrame.from_dict(x)
        columns = corr_dist_data.columns
        corr_dist_data = corr_dist_data.to_numpy()
        time = FL1_pd['Time'].to_numpy()
        time = pd.DataFrame(time, columns=['Time'])
        time_col = time.columns
        time = time.to_numpy()
        dict_ = dict(zip(columns, corr_dist_data.T))
    
    #make time dict
    time_dict = dict(zip(time_col, time.T))
    
    def Merge(time_dict, dict_):
        res = {**time_dict, **dict_}
        return res
    
    #merge the two dictionarys
    merged_data_dict = Merge(time_dict, dict_)
    
    #define date and time of science file
    name_elements = _infile.split('.')
    yy = name_elements[0][0:2]
    mm = name_elements[0][3:5]
    dd = name_elements[0][6:8]
    hh = name_elements[0][9:11]
    mi = name_elements[0][12:14]
    ss = name_elements[0][15:17]
    
    out = ADPAA()
    out.DREV   = 0
    # Fill output object.
    out.NLHEAD = 22
    out.FFI    = 1001
    out.ONAME  = 'Nairy, Christian'
    out.ORG    = 'University of North Dakota'
    out.SNAME  = 'Atmospheric Science Dept.'
    out.MNAME  = 'Distance from TITAN Reflectivity Centroid - ' + key 
    out.IVOL   = 1
    out.VVOL   = 1
    out.DATE   =  '2019 07 31'
    #out.DATE   = _data_matrix[0][0][:4] + ' ' + _data_matrix[0][0][5:7]+ ' ' + _data_matrix[0][0][8:10]
    # out.RDATE  = (time.strftime("%Y %m %d"))
    out.RDATE  = 'N/A'
    out.DX     = 1.0000
    out.XNAME  = 'Time [second]; UTC seconds from midnight on day measurements started.'
    out.NV     = 1
    out.VSCAL  = ['     1.0000']
    out.VMISS  = ['999999.9999']
    out.VNAME  = ['Distance From Core [DFC] Reflectivity Centroid']
    out.DTYPE  = '0'
    out.VFREQ  = '1Hz Frequency'
    out.VDESC  = ['Time', 'DFC']
    out.VUNITS = ['Seconds', 'km']
    out.data   = merged_data_dict
    # date = 
    
    out.name =  yy + '_' + mm + '_' + dd + '_' + hh + '_' + mi + '_' + ss + '.' +  key + '.DFC'
    out.WriteFile()
    print('THE SCRIPT IS WORKING, DO NOT EXIT OUT!')

#NOW NEED TO MERGE THE DATA INTO ONE SCIENCE FILE
#concat the files
os.system('cat *.FL{1..' + last_FL_val_str +'}.DFC > ' + yy + '_' + mm + '_' + dd + '_' + hh + '_' + mi + '_' + ss + '.DFC')

#FINISHED#

###############


































