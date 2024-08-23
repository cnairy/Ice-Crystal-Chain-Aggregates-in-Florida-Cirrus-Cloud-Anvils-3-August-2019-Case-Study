#!/usr/bin/env python3
"""
  NAME:
    convert_PHIPS2nasa.py
 
  PURPOSE:
    Convert text files generated from the PHIPS_Image_Classifier_7.mlapp MATLAB software 
    into NASA format.

    Currently this script only works for the 20190803_142455 PHIPS_data.
    
    Need to be in /nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/PHIPS_Data/MATLAB directory

  CALLS:
    ADPAA

  EXAMPLE:
    The command:

       convert_PHIPS2nasa.py PhipsData_20190803-1424_Image_Classification.txt

    create the 19_08_03_14_24_55_phips.classify.raw file.

  MODIFICATIONS:
    Christian Nairy <christian.nairy@und.edu> - 2020/07/16:
        Written
    Christian Nairy <christian.nairy@und.edu> - 2020/07/20:
        Changed 'from adpaa import ADPAA' to 'from adpaa_python3 import ADPAA'.
        This is needed for accurate timestamps and because this is a python3
        script.
    Christian Nairy <christian.nairy@und.edu> - 2020/07/27:
        Made minor syntax corrections for less user minipulation of the PHIPS data file
        before running this script.
    Christian Nairy <christian.nairy@und.edu> - 2020/09/02:
       Added the nessesary information for this script to process data from 20190802-1931

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
import re
import sys
import time
import glob
import numpy as np
import os
import datetime

# Check to make sure there is only one command-line argument
if len(sys.argv) != 2:
    print("SYNTAX:  convert_PHIPS2nasa.py inputfile")
    print( "")
    print( "  inputfile - The PhipsData_20190803-1424_Image_Classification.txt file.")
    print( "  Example:  convert_PHIPS2nasa.py PhipsData_20190803-1424_Image_Classification.txt")
    print( "")
    sys.exit()
    
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
        if (FirstTimeDay == 2):
            if (FirstTimeHour == 19):
                # This is for the 20190802_1931 flight
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
    
    # Loop over the files, and concatenate the data. 
    for file1 in input:
        # Get file number.
        num=file1[61:67]
        
        input2_file = prefix_input_file+dir_id+'_C2/*'
        input2 = sorted(glob.glob(input2_file+num+'*C2.png'))
        for file2 in input2:
            num2=file2[61:67]

            if (num == num2):
                #print("    "+num2)
                # Defince current image clock ticks.
                CurrentImageTick = file1[46:60]
                CurrentImageSecond = FirstTimeSecond+int(CurrentImageTick)/(10**9)
                CurrentImageSFM    = FirstTimeHour*3600.0 + FirstTimeMin*60.0 + CurrentImageSecond
                times = CurrentImageSFM
                SFM.append(times)
                # Convert to seconds from midnight.
                # time = CurrentImageSFM
                # day = time // (24 * 3600)
                # time = time % (24 * 3600)
                # hour = time // 3600
                # time %= 3600
                # minutes = time // 60
                # time %= 60
                # seconds = time

                # # Define time file name segment.
                # k = "%.3f" % (seconds-int(seconds))
                # CurrentImageFileTime = "_%02d:%02d:%02d" % (hour,minutes,seconds) + k[1:]
                # SFM.append(CurrentImageFileTime)


SFM_ = np.array(SFM)

#Round the SFM to the thousanths place
SFM_done = np.around(SFM_, decimals = 3) 
# print(SFM_done)




#-----------------------------------------------------------------
#-----------------------------------------------------------------

#This part of the script reads in the Phips* .txt file that is user defined on
#the commandline

_infile = sys.argv[1]
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


# Get number of data lines.
#print(_data_matrix)
        
 #Delete header information and get number of data lines.
_data_matrix = np.delete(_data_matrix, 0, axis=0)       

"""
*******************************************************************************
THIS LINE OF CODE... "_data_matrix = np.delete(_data_matrix, 1054, axis=0)"
SHOULD ONLY BE UNCOMMENTED FOR FLIGHT 20190803_1424
IMAGE 1055 IS MISSING -- NEED TO REMOVE THAT LINE IN ARRAY
*******************************************************************************
"""       
_data_matrix = np.delete(_data_matrix, 3454, axis=0)


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

#Define the null data
Plate[np.isnan(Plate)]=99999.999
Skeleton_Plate[np.isnan(Skeleton_Plate)]=99999.999
Sectored_Plate[np.isnan(Sectored_Plate)]=99999.999
SidePlane[np.isnan(SidePlane)]=99999.999
Dendrite[np.isnan(Dendrite)]=99999.999
Column[np.isnan(Column)]=99999.999
Hollow_Column[np.isnan(Hollow_Column)]=99999.999
Sheath[np.isnan(Sheath)]=99999.999
CappedColumn[np.isnan(CappedColumn)]=99999.999
Needle[np.isnan(Needle)]=99999.999
Frozen_droplet[np.isnan(Frozen_droplet)]=99999.999
Bullet_rosette[np.isnan(Bullet_rosette)]=99999.999
Graupel[np.isnan(Graupel)]=99999.999
Unidentified[np.isnan(Unidentified)]=99999.999
Droplet[np.isnan(Droplet)]=99999.999
Aggregate[np.isnan(Aggregate)]=99999.999
Rimed[np.isnan(Rimed)]=99999.999
Pristine[np.isnan(Pristine)]=99999.999
Shattering[np.isnan(Shattering)]=99999.999
Multiple[np.isnan(Multiple)]=99999.999
Cutoff[np.isnan(Cutoff)]=99999.999
Elongated[np.isnan(Elongated)]=99999.999
ChainAgg[np.isnan(ChainAgg)]=99999.9990
Sublimating[np.isnan(Sublimating)]=99999.999
Empty[np.isnan(Empty)]=99999.999
ConfidenceLevel[np.isnan(ConfidenceLevel)]=99999.999



# Create ADPAA output object.
out = ADPAA()

# Fill output object.
out.NLHEAD = 64
out.FFI    = 1001
out.ONAME  = 'Delene, David'
out.ORG    = 'University of North Dakota'
out.SNAME  = 'Atmospheric Science Dept.'
out.MNAME  = 'PHIPS_Data'
out.IVOL   = 1
out.VVOL   = 1
out.DATE   = '2019 08 03'
#out.DATE   = _data_matrix[0][0][:4] + ' ' + _data_matrix[0][0][5:7]+ ' ' + _data_matrix[0][0][8:10]
# out.RDATE  = (time.strftime("%Y %m %d"))
out.RDATE  = 'Asychronous'
out.DX     = 0.1
out.XNAME  = 'Time [second]; UT seconds from midnight on day measurements started.'
out.NV     = 28
out.VSCAL  = ['        1','        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1', '        1.0', '        1', '        1']
out.VMISS  = ['99999.999','99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999', '99999.999']
out.VNAME  = ['Image_number: Image number label','Plate','Skeleton_Plate','Sectored_Plate','SidePlane','Dendrite','Column','Hollow_Column','Sheath','CappedColumn','Needle','Frozen_droplet','Bullet_rosette','Graupel','Unidentified: User was unable to define the particle displayed in the frame','Droplet: Liquid water droplet','Aggregate: Ice aggregates not deemed as a chain aggregate','Rimed','Pristine: Image is clear and in focus with no shattering and with majority of the image in the frame','Shattering: Shattering particles','Multiple: Multiple particles in the frame','Cutoff: Image is partially cutoff in the frame','Elongated: Parameter is used if a chain aggreagate is elongated in the frame','ChainAgg: Aggregates line in a chain-like orientation','Sublimating','Empty: Empty image frame','ConfidenceLevel: confidence that the image is a chain aggregate: between 1 and 3 (1 being low conficence, 3 being high confidence)']
out.NSCOML = 0
out.NNCOML = 4
out.DTYPE  = 'Final Data'
out.DREV   = 0
out.VFREQ  = 'Asychronous'
out.VDESC  = ['Time','Image_num','Plate','Skeleton_Pl','Sectored_Pl','SidePlane','Dendrite','Column','Hollow_Col','Sheath','CappedCol','Needle','Frozen_drop','Bullet_rose','Graupel','Unidenti','Droplet','Aggregate','Rimed','Pristine','Shattering','Multiple','Cutoff','Elongated','ChainAgg','Sublimating','Empty','Confidence']
out.VUNITS = ['seconds','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #','          #']
out.data = {"Time":SFM_done,'Image_num':Image_number,'Plate':Plate,'Skeleton_Pl':Skeleton_Plate,'Sectored_Pl':Sectored_Plate,'SidePlane':SidePlane,'Dendrite':Dendrite,'Column':Column,'Hollow_Col':Hollow_Column,'Sheath':Sheath,'CappedCol':CappedColumn,'Needle':Needle,'Frozen_drop':Frozen_droplet,'Bullet_rose':Bullet_rosette,'Graupel':Graupel,'Unidenti':Unidentified,'Droplet':Droplet,'Aggregate':Aggregate,'Rimed':Rimed,'Pristine':Pristine,'Shattering':Shattering,'Multiple':Multiple,'Cutoff':Cutoff,'Elongated':Elongated,'ChainAgg':ChainAgg,'Sublimating':Sublimating,'Empty':Empty,'Confidence':ConfidenceLevel}

# name_elements = _infile.split('.')
# yy = name_elements[0][12:13]
# mm = name_elements[0][8:10]
# dd = name_elements[0][10:12]
# hh = name_elements[0][13:15]
# mi = name_elements[0][15:17]
# ss = name_elements[0][17:19]
out.name = '19_08_02_19_29_15_phips.classify.raw'
out.WriteFile()















