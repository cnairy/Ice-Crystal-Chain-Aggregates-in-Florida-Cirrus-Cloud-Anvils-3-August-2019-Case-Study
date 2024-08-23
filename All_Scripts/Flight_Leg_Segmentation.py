#!/bin/env python3 
"""
  NAME:
    Flight_Leg_Segmentation.py
 
  PURPOSE:
    This script will read in a segment file which you created. The segment file has flight leg information
    (such as flight leg number, start time [sfm], and end time [sfm]). Look at 19_08_03_14_24_55.cap.segments
    as an example. This script will read this file in and then read in the science file (which is called next
    to the script on the command line) and will output science files that correspond to each flight leg.


  CALLS:
    NONE

  EXAMPLE:
    The command:
        Flight_Leg_Segmentation.py 19_08_03_14_24_55.cap.YYMMDD
       

    If you have one flight leg:
    creates: 19_08_03_14_24_55.FL1.cap

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
#IMPORTS.
import sys
import numpy as np
import pandas as pd
import glob
from adpaa_python3 import ADPAA
#Remove pandas warning messages
pd.options.mode.chained_assignment = None


# Define syntax. 
def help_message():
    print('\n')
    print('Syntax:Flight_Leg_Segmentation.py <-h>\n\n')
    print('  Example: Flight_Leg_Segmentation.py <science_file> \n')
    print('\n')
    print(' NOTE: IF YOU HAVE MORE THAN 15 FLIGHT LEG SEGMENTS YOU WILL NEED TO ADJUST THE SCRIPT')

# Check input parameters. 
for param in sys.argv:
    if param.startswith('-h') | param.startswith('-help') | param.startswith('--help') | param.startswith('--h'):
        help_message()
        exit()

#TEST
# path = '/nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'
# file = '19_08_03_14_24_55.cap.segments'

filepath = glob.glob('*.segments')

fo = open(filepath[0])
# fo = open(path + file)

segment = np.genfromtxt(fo, delimiter=",", dtype=float, skip_header=1)

#last FL number value
last_FL_val = segment[-1,0]

#Split the flight leg times from segment file
n = np.array_split(segment, last_FL_val)

#Testing
# path_1 ='/nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'
# filename_1 = '19_08_03_14_24_55.cap.220907'

_infile = sys.argv[1]
cap = ADPAA()
cap.ReadFile(_infile)

# cap.ReadFile(path_1 + filename_1)  #test

#This script will be used to split the total science file into individual files. the number of output science files
#depends on the number of flight legs defined.
data_cap = cap.data

#Grab the number of flight legs into a string list
#might need to fix this and figure out a more efficient loop
dict_list = []
num_list = []
for col in segment:
    if col[0] == 1:
        FL1 = col
        #create a dictionary with fligh leg values. then replace old total dict with this one.
        FL1_pd = pd.DataFrame.from_dict(data_cap)
        FL1_pd = FL1_pd[(FL1_pd['Time'] >= FL1[1]) & (FL1_pd['Time'] < FL1[2])]
        FL1_np = FL1_pd.to_numpy()
        FL1_dict = dict(zip(FL1_pd.columns, FL1_np.T))
        dict_list.append(FL1_dict)
        num_list.append('01')
    if col[0] == 2:
        FL2 = col
        FL2_pd = pd.DataFrame.from_dict(data_cap)
        FL2_pd = FL2_pd[(FL2_pd['Time'] >= FL2[1]) & (FL2_pd['Time'] < FL2[2])]
        FL2_np = FL2_pd.to_numpy()
        FL2_dict = dict(zip(FL2_pd.columns, FL2_np.T))
        dict_list.append(FL2_dict)
        num_list.append('02')
    if col[0] == 3:
        FL3 = col
        FL3_pd = pd.DataFrame.from_dict(data_cap)
        FL3_pd = FL3_pd[(FL3_pd['Time'] >= FL3[1]) & (FL3_pd['Time'] < FL3[2])]
        FL3_np = FL3_pd.to_numpy()
        FL3_dict = dict(zip(FL3_pd.columns, FL3_np.T))
        dict_list.append(FL3_dict)
        num_list.append('03')
    if col[0] == 4:
        FL4 = col
        FL4_pd = pd.DataFrame.from_dict(data_cap)
        FL4_pd = FL4_pd[(FL4_pd['Time'] >= FL4[1]) & (FL4_pd['Time'] < FL4[2])]
        FL4_np = FL4_pd.to_numpy()
        FL4_dict = dict(zip(FL4_pd.columns, FL4_np.T))
        dict_list.append(FL4_dict)
        num_list.append('04')
    if col[0] == 5:
        FL5 = col
        FL5_pd = pd.DataFrame.from_dict(data_cap)
        FL5_pd = FL5_pd[(FL5_pd['Time'] >= FL5[1]) & (FL5_pd['Time'] < FL5[2])]
        FL5_np = FL5_pd.to_numpy()
        FL5_dict = dict(zip(FL5_pd.columns, FL5_np.T))
        dict_list.append(FL5_dict)
        num_list.append('05')
    if col[0] == 6:
        FL6 = col
        FL6_pd = pd.DataFrame.from_dict(data_cap)
        FL6_pd = FL6_pd[(FL6_pd['Time'] >= FL6[1]) & (FL6_pd['Time'] < FL6[2])]
        FL6_np = FL6_pd.to_numpy()
        FL6_dict = dict(zip(FL6_pd.columns, FL6_np.T))
        dict_list.append(FL6_dict)
        num_list.append('06')
    if col[0] == 7:
        FL7 = col
        FL7_pd = pd.DataFrame.from_dict(data_cap)
        FL7_pd = FL7_pd[(FL7_pd['Time'] >= FL7[1]) & (FL7_pd['Time'] < FL7[2])]
        FL7_np = FL7_pd.to_numpy()
        FL7_dict = dict(zip(FL7_pd.columns, FL7_np.T))
        dict_list.append(FL7_dict)
        num_list.append('07')
    if col[0] == 8:
        FL8 = col
        FL8_pd = pd.DataFrame.from_dict(data_cap)
        FL8_pd = FL8_pd[(FL8_pd['Time'] >= FL8[1]) & (FL8_pd['Time'] < FL8[2])]
        FL8_np = FL8_pd.to_numpy()
        FL8_dict = dict(zip(FL8_pd.columns, FL8_np.T))
        dict_list.append(FL8_dict)
        num_list.append('08')
    if col[0] == 9:
        FL9 = col
        FL9_pd = pd.DataFrame.from_dict(data_cap)
        FL9_pd = FL9_pd[(FL9_pd['Time'] >= FL9[1]) & (FL9_pd['Time'] < FL9[2])]
        FL9_np = FL9_pd.to_numpy()
        FL9_dict = dict(zip(FL9_pd.columns, FL9_np.T))
        dict_list.append(FL9_dict)
        num_list.append('09')
    if col[0] == 10:
        FL10 = col
        FL10_pd = pd.DataFrame.from_dict(data_cap)
        FL10_pd = FL10_pd[(FL10_pd['Time'] >= FL10[1]) & (FL10_pd['Time'] < FL10[2])]
        FL10_np = FL10_pd.to_numpy()
        FL10_dict = dict(zip(FL10_pd.columns, FL10_np.T))
        dict_list.append(FL10_dict)
        num_list.append('10')
    if col[0] == 11:
        FL11 = col
        FL11_pd = pd.DataFrame.from_dict(data_cap)
        FL11_pd = FL11_pd[(FL11_pd['Time'] >= FL11[1]) & (FL11_pd['Time'] < FL11[2])]
        FL11_np = FL11_pd.to_numpy()
        FL11_dict = dict(zip(FL11_pd.columns, FL11_np.T))
        dict_list.append(FL11_dict)
        num_list.append('11')
    if col[0] == 12:
        FL12 = col
        FL12_pd = pd.DataFrame.from_dict(data_cap)
        FL12_pd = FL12_pd[(FL12_pd['Time'] >= FL12[1]) & (FL12_pd['Time'] < FL12[2])]
        FL12_np = FL12_pd.to_numpy()
        FL12_dict = dict(zip(FL12_pd.columns, FL12_np.T))
        dict_list.append(FL12_dict)
        num_list.append('12')
    if col[0] == 13:
        FL13 = col
        FL13_pd = pd.DataFrame.from_dict(data_cap)
        FL13_pd = FL13_pd[(FL13_pd['Time'] >= FL13[1]) & (FL13_pd['Time'] < FL13[2])]
        FL13_np = FL13_pd.to_numpy()
        FL13_dict = dict(zip(FL13_pd.columns, FL13_np.T))
        dict_list.append(FL13_dict)
        num_list.append('13')
    if col[0] == 14:
        FL14 = col
        FL14_pd = pd.DataFrame.from_dict(data_cap)
        FL14_pd = FL14_pd[(FL14_pd['Time'] >= FL14[1]) & (FL14_pd['Time'] < FL14[2])]
        FL14_np = FL14_pd.to_numpy()
        FL14_dict = dict(zip(FL14_pd.columns, FL14_np.T))
        dict_list.append(FL14_dict)
        num_list.append('14')
    if col[0] == 15:
        FL15 = col
        FL15_pd = pd.DataFrame.from_dict(data_cap)
        FL15_pd = FL15_pd[(FL15_pd['Time'] >= FL15[1]) & (FL15_pd['Time'] < FL15[2])]
        FL15_np = FL15_pd.to_numpy()
        FL15_dict = dict(zip(FL15_pd.columns, FL15_np.T))
        dict_list.append(FL15_dict)
        num_list.append('15')
        

#Write out NASA files for each flight leg.
for i, j in zip(dict_list, num_list):
    out = ADPAA()
    out.DREV   = 0
    # Fill output object.
    out.NLHEAD = 22
    out.FFI    = 1001
    out.ONAME  = 'Delene, David'
    out.ORG    = 'University of North Dakota'
    out.SNAME  = 'Atmospheric Science Dept.'
    out.MNAME  = 'Flight leg' + j + ' ' + 'Data'
    out.IVOL   = 1
    out.VVOL   = 1
    out.DATE   = cap.DATE
    #out.DATE   = _data_matrix[0][0][:4] + ' ' + _data_matrix[0][0][5:7]+ ' ' + _data_matrix[0][0][8:10]
    # out.RDATE  = (time.strftime("%Y %m %d"))
    out.RDATE  = 'N/A'
    out.DX     = 1.0000
    out.XNAME  = 'Time [second]; UTC seconds from midnight on day measurements started.'
    out.NV     = cap.NV
    out.VSCAL  = cap.VSCAL
    out.VMISS  = cap.VMISS
    out.VNAME  = cap.VNAME
    out.DTYPE  = cap.DTYPE
    out.VFREQ  = cap.VFREQ
    out.VDESC  = cap.VDESC
    out.VUNITS = cap.VUNITS
    out.data   = i
    name_elements = _infile.split('.')
    yy = name_elements[0][0:2]
    mm = name_elements[0][3:5]
    dd = name_elements[0][6:8]
    hh = name_elements[0][9:11]
    mi = name_elements[0][12:14]
    ss = name_elements[0][15:17]
    
    out.name = yy + '_' + mm + '_' + dd + '_' + hh + '_' + mi + '_' + ss + '.FL' + j + '.cap'
    out.WriteFile()
    


