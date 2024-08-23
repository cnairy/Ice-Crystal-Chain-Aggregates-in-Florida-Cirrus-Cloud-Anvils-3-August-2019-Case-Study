
#!/usr/bin/env python3
"""
  NAME:
    convert_PHIPS2nasa.py
 
  PURPOSE:
    Convert text files generated from the PHIPS_Image_Classifier_7.mlapp MATLAB software 
    into NASA format.
    
    Need to be in /nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/PHIPS_Data/MATLAB directory

  CALLS:
    ADPAA

  EXAMPLE:
    The command:

       convert_PHIPS_chains_confidence_1hz_2nasa.py PhipsData_20190803-1424_Image_Classification.txt

    create the 19_08_03_14_24_55_chains_confidence.1Hz.raw file.

  MODIFICATIONS:
    Christian Nairy <christian.nairy@und.edu> - 2020/07/28:
      Written...*** LOOK AT LINE 209! YOU MAY NEED TO ADJUST BEFORE RUNNING THIS SCRIPT ***
    Christian Nairy <christian.nairy@und.edu> - 2020/09/01:
      Corrected minor syntax errors, and allowed data from 20190802_192915 to be processed.
      *** LOOK AT LINE 210! YOU MAY NEED TO ADJUST BEFORE RUNNING THIS SCRIPT ***
    Shawn Wagner <shawn.wagner@und.edu> - 2020/09/08:
      Added information for processesing of the 20190803_2040 data.
    Christian Nairy <christian.nairy@und.edu> - 2021/03/12:
      Removed the confidence levels for non chain aggregates where previously the non-chain confidence 
      levels where adjusting the chain confidence levels.
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

from adpaa_python3 import ADPAA
import numpy as np
import pandas as pd
import re
import sys
import time
import glob
import numpy as np
import os
import datetime

# Check to make sure there is only one command-line argument
# if len(sys.argv) != 2:
#     print("SYNTAX:  convert_PHIPS_chains_confidence_1hz_2nasa.py inputfile")
#     print( "")
#     print( "  inputfile - The PhipsData_20190803-1424_Image_Classification.txt file.")
#     print( "  Example: convert_PHIPS_chains_confidence_1hz_2nasa.py PhipsData_20190803-1424_Image_Classification.txt")
#     print( "")
#     sys.exit()
    
filepath = glob.glob('*0000_C1.txt')

fo = open(filepath[0], 'r')

line1 = fo.readline()
line2 = fo.readline()
line3 = fo.readline()
FirstTimeStamp  = line3[19:36]

# Close opend file
fo.close()

# Set the data and time information from time stamp information.
FirstTimeYYYY   = int(FirstTimeStamp[0:4])
FirstTimeMonth  = int(FirstTimeStamp[4:6])
FirstTimeDay    = int(FirstTimeStamp[6:8])
FirstTimeHour   = int(FirstTimeStamp[8:10])
FirstTimeMin    = int(FirstTimeStamp[10:12])
FirstTimeSec    = int(FirstTimeStamp[12:14])
FirstTimeSecFac = int(FirstTimeStamp[14:17])
FirstTimeSecond = FirstTimeSec + (FirstTimeSecFac/1000.0)

# Define the First Image Time Stamp (UTC) and First Clock Tick.
# The first time stamp is from *C1.txt file,
# for example FirstTimeStamp_C1: 20190803143828932 -> 00793296671400
if (FirstTimeYYYY == 2019):
     if (FirstTimeMonth == 8):
         if (FirstTimeDay == 3):
            if (FirstTimeHour == 14):
                # This is for the 20190803_142455 flight
                FirstClockTick = '00793296671400'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010','0011','0012','0013','0014','0015','0016','0017']
                prefix_input_file = '20190803-1424_'

if (FirstTimeYYYY == 2019):
     if (FirstTimeMonth == 8):
         if (FirstTimeDay == 3):
            if (FirstTimeHour == 21):
                # This is for the 20190803_203840 flight
                FirstClockTick = '01626851003400'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008']
                prefix_input_file = '20190803-2040_'

if (FirstTimeYYYY == 2019):
    if (FirstTimeMonth == 8):
        if (FirstTimeDay == 2):
            if (FirstTimeHour == 19):
                # This is for the 20190802_192915 flight
                FirstClockTick = '00488851739700'
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010']
                prefix_input_file = '20190802-1931_'

# Set the first time information.
FirstImageSecond = FirstTimeSecond+int(FirstClockTick)/(10**9)
FirstImageSFM    = FirstTimeHour*3600.0 + FirstTimeMin*60.0 + FirstImageSecond

# Convert from SFM to HH:MM:SS
time = FirstImageSFM
day = time // (24 * 3600)
time = time % (24 * 3600)
hour = time // 3600
time %= 3600
minutes = time // 60
time %= 60
seconds = time

SFM = []
for dir_id in ids:
    #print( "dir_id = "+dir_id)
    
        # Search for all files with the inputed syntax within the directory. 
    input_file = prefix_input_file+dir_id+'_C1/*C1.png'
    input = sorted(glob.glob(input_file))
#    print(input)
    
    # Loop over the files, and concatenate the data. 
    for file1 in input:
        # Get file number.
        num=file1[61:67]
        
        input2_file = prefix_input_file+dir_id+'_C2/*'
        input2 = sorted(glob.glob(input2_file+num+'*C2.png'))
#        print(input2)
        for file2 in input2:
            num2=file2[61:67]

            if (num == num2):
#                print("    "+num2)
                # Defince current image clock ticks.
                CurrentImageTick = file1[46:60]
                CurrentImageSecond = FirstTimeSecond+int(CurrentImageTick)/(10**9)
                CurrentImageSFM    = FirstTimeHour*3600.0 + FirstTimeMin*60.0 + CurrentImageSecond
#                times = CurrentImageSFM
#                SFM.append(CurrentImageSFM)
                #Convert to seconds from midnight.
                time = CurrentImageSFM
                day = time // (24 * 3600)
                time = time % (24 * 3600)
                hour = time // 3600
                time %= 3600
                minutes = time // 60
                time %= 60
                seconds = time

                 # Define time file name segment.
                k = "%.3f" % (seconds-int(seconds))
                CurrentImageFileTime = "%02d:%02d:%02d" % (hour,minutes,seconds) + k[1:]
                SFM.append(CurrentImageFileTime)

#print(SFM)
SFM_done = np.array(SFM)

#-----------------------------------------------------------------
#-----------------------------------------------------------------




# Get input file name from command-line argument.
pth = "/nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/PHIPS_Data/MATLAB/"

_infile = (pth + 'PhipsData_20190803-1424_Image_Classification_Nairy.txt')



# _infile = sys.argv[1]
# Define empty array.
_data_matrix = []

# Read file.
_fhand = open(_infile, 'r')
_i = 0
for _line in _fhand.readlines():
    _i = _i + 1
    _line = _line.strip()
    _columns = _line.split()
    if _columns.__len__() == 1:
        _data_arr = _columns[0].split(',')
        _data_matrix.append(_data_arr)


#Delete header information and get number of data lines.
_data_matrix = np.delete(_data_matrix, 0, axis=0)

#THIS LINE OF CODE SHOULD ONLY BE UNCOMMENTED FOR FLIGHT 20190803_1424
#IMAGE 1055 IS MISSING -- NEED TO REMOVE THAT LINE IN ARRAY
#FOR THE FLIGHT 20190802_192915 IMAGE 3455 IS MISSING: NEED TO REMOVE THE LINE IN THE ARRAY!
_data_matrix = np.delete(_data_matrix, 1054, axis=0)
#_data_matrix = np.delete(_data_matrix, 3454, axis=0)

#print(_data_matrix)
_data_rows = len(_data_matrix)

  # Create empty arrays.
# sfm                     = np.empty(_data_rows,dtype=float)
Image_number            = np.empty(_data_rows,dtype=float)
Plate                   = np.empty(_data_rows,dtype=float)
Skeleton_Plate          = np.empty(_data_rows,dtype=float)
Sectored_Plate          = np.empty(_data_rows,dtype=float)
SidePlane               = np.empty(_data_rows,dtype=float)
Dendrite                = np.empty(_data_rows,dtype=float)
Column                  = np.empty(_data_rows,dtype=float)
Hollow_Column           = np.empty(_data_rows,dtype=float)
Sheath                  = np.empty(_data_rows,dtype=float)
CappedColumn            = np.empty(_data_rows,dtype=float)
Needle                  = np.empty(_data_rows,dtype=float)
Frozen_droplet          = np.empty(_data_rows,dtype=float)
Bullet_rosette          = np.empty(_data_rows,dtype=float)
Graupel                 = np.empty(_data_rows,dtype=float)
Unidentified            = np.empty(_data_rows,dtype=float)
Droplet                 = np.empty(_data_rows,dtype=float)
Aggregate               = np.empty(_data_rows,dtype=float)
Rimed                   = np.empty(_data_rows,dtype=float)
Pristine                = np.empty(_data_rows,dtype=float)
Shattering              = np.empty(_data_rows,dtype=float)
Multiple                = np.empty(_data_rows,dtype=float)
Cutoff                  = np.empty(_data_rows,dtype=float)
Elongated               = np.empty(_data_rows,dtype=float)
ChainAgg                = np.empty(_data_rows,dtype=float)
Sublimating             = np.empty(_data_rows,dtype=float)
Empty                   = np.empty(_data_rows,dtype=float)
ConfidenceLevel         = np.empty(_data_rows,dtype=float)



for lines in range(_data_rows):
    _temp = _data_matrix[lines][1].split(':')


    Image_number[lines]     = float(_data_matrix[lines][0])
    Plate[lines]            = float(_data_matrix[lines][1])
    Skeleton_Plate[lines]   = float(_data_matrix[lines][2])
    Sectored_Plate[lines]   = float(_data_matrix[lines][3])
    SidePlane[lines]        = float(_data_matrix[lines][4])
    Dendrite[lines]         = float(_data_matrix[lines][5])
    Column[lines]           = float(_data_matrix[lines][6])
    Hollow_Column[lines]    = float(_data_matrix[lines][7])
    Sheath[lines]           = float(_data_matrix[lines][8])
    CappedColumn[lines]     = float(_data_matrix[lines][9])
    Needle[lines]           = float(_data_matrix[lines][10])
    Frozen_droplet[lines]   = float(_data_matrix[lines][11])
    Bullet_rosette[lines]   = float(_data_matrix[lines][12])
    Graupel[lines]          = float(_data_matrix[lines][13])
    Unidentified[lines]     = float(_data_matrix[lines][14])
    Droplet[lines]          = float(_data_matrix[lines][15])
    Aggregate[lines]        = float(_data_matrix[lines][16])
    Rimed[lines]            = float(_data_matrix[lines][17])
    Pristine[lines]         = float(_data_matrix[lines][18])
    Shattering[lines]       = float(_data_matrix[lines][19])
    Multiple[lines]         = float(_data_matrix[lines][20])
    Cutoff[lines]           = float(_data_matrix[lines][21])
    Elongated[lines]        = float(_data_matrix[lines][22])
    ChainAgg[lines]         = float(_data_matrix[lines][23])
    Sublimating[lines]      = float(_data_matrix[lines][24])
    Empty[lines]            = float(_data_matrix[lines][25])
    ConfidenceLevel[lines]  = float(_data_matrix[lines][26])



#dataset = pd.DataFrame([SFM_Done], _data_matrix[1],_data_matrix[2],_data_matrix[3]_data_matrix[4],_data_matrix[5],_data_matrix[6],_data_matrix[7],_data_matrix[8],_data_matrix[9],_data_matrix[10],_data_matrix[11],_data_matrix[12],_data_matrix[13],_data_matrix[14],_data_matrix[15],_data_matrix[16],_data_matrix[17],_data_matrix[18],_data_matrix[19],_data_matrix[20],_data_matrix[21],_data_matrix[22],_data_matrix[23],_data_matrix[24],_data_matrix[25],_data_matrix[26]))

#Newest update: removed confidence values for non chain aggregates
dataset1 = pd.DataFrame(ChainAgg,columns=['chains'])
dataset1.insert(0, "time", SFM_done)
dataset2 = pd.DataFrame(ConfidenceLevel, columns=['confidence'])
dataset1.insert(2, "confidence", dataset2)
dataset1.loc[dataset1['chains'] == 0, 'confidence'] = 0
dataset2 = pd.DataFrame(dataset1['confidence'])
del dataset1['confidence']

            
dataset1.replace(0, np.nan, inplace=True)
dataset2.replace(0, np.nan, inplace=True)
dataset2.insert(0, "time", SFM_done)

dataset1.columns = ['time',"chains"]
dataset2.columns = ['time',"confidence"]

dataset1.time = pd.to_datetime(dataset1.time)
dataset2.time = pd.to_datetime(dataset2.time)

new_chain = dataset1.set_index('time').resample('1S').count()

new_confidence = dataset2.set_index('time').resample('1S').mean().replace(0,np.nan)

new_chain.insert(1,'confidence_avg', new_confidence)

final = new_chain.replace(0,np.nan)
final_ = final.replace(np.nan, -99999.999)


#convert time from hh:mm:ss to seconds from midnight
final_.reset_index(level=0, inplace=True)
df_time = pd.to_datetime(final_["time"])

df_time = (df_time.dt.hour*60+df_time.dt.minute)*60 + df_time.dt.second

done = final_.merge(df_time.to_frame(), left_index=True, right_index=True)

#remove extra time column (don't need)
del done['time_x']

#rename columns
done.columns = ["chains_1s_sum", "confidence_1s_avg", "sfm"]

#Remove confidence values for non-chain aggregates
done.loc[done['chains_1s_sum'] == -99999.999, 'confidence_1s_avg'] = -99999.999


#convert 1 second data back to numpy
sfm_ = done.iloc[:,2].astype(np.float64).to_numpy()
chains_ = done.iloc[:,0].to_numpy()
confidence_ = done.iloc[:,1].to_numpy()


#
#
# Create ADPAA output object.
out = ADPAA()

# Fill output object.
out.NLHEAD = 64
out.FFI    = 1001
out.ONAME  = 'Delene, David'
out.ORG    = 'University of North Dakota'
out.SNAME  = 'Atmospheric Science Dept.'
out.MNAME  = 'PHIPS_Data 1_sec groupings (chains & confidence)'
out.IVOL   = 1
out.VVOL   = 1
out.DATE   = '2019 08 03'
#out.DATE   = _data_matrix[0][0][:4] + ' ' + _data_matrix[0][0][5:7]+ ' ' + _data_matrix[0][0][8:10]
# out.RDATE  = (time.strftime("%Y %m %d"))
out.RDATE  = 'N/A'
out.DX     = 1.0000
out.XNAME  = 'Time [second]; UT seconds from midnight on day measurements started.'
out.NV     = 2
out.VSCAL  = ['        1','        1']
out.VMISS  = ['-99999.999','-99999.999']
out.VNAME  = ['ChainAgg: Summation of all chain aggregates in 1 second', 'Confidence: average confidence of the 1 second summation of chain aggregates: between 1 and 3 (1 being low conficence, 3 being high confidence)']
out.DTYPE  = 'Final Data'
out.DREV   = 0
out.VFREQ  = '1 Hz Data'
out.VDESC  = ['Time','ChainAgg','Confidence']
out.VUNITS = ['seconds','#(1sec_sum)','#(1sec_avg)']
out.data = {"Time":sfm_,'ChainAgg':chains_,'Confidence':confidence_}

# name_elements = _infile.split('.')
# yy = name_elements[0][12:13]
# mm = name_elements[0][8:10]
# dd = name_elements[0][10:12]
# hh = name_elements[0][13:15]
# mi = name_elements[0][15:17]
# ss = name_elements[0][17:19]
out.name = '19_08_03_14_24_55.chains.confidence.1Hz.updated_20210312.raw'
out.WriteFile()
