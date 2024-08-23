#!/bin/env python3 
#
# Name:
#   combine_PHIPS_Images.py
#
# Purpose:
#   To combine two different view of the same particle together for the PHIPS instruments.
#
# Syntax:
#   ./combine_PHIPS_Images.py
#
#   Input NASA/UND formatted Files:
#
#   Output Files:
#
# Execution Example:
#  Need to be in /nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/PHIPS_Data directory
#
# Modification History:
#   2019/12/03 - David Delene <delene@aero.und.edu>
#     Written.
#   2020/02/09 - David Delene <delene@aero.und.edu>
#     Changed location of env.
#   2020/02/09 - David Delene <delene@aero.und.edu>
#     Got code working for 20190803_203840.
#   2020/03/10 - David Delene <delene@aero.und.edu>
#     Added code for 20190802, 20190801, and 20190731
#   2021/08/20 - Christian Nairy <christian.nairy@und.edu>
#     Added working code for 20190730 flight.
#   2021/08/26 - Christian Nairy <christian.nairy@und.edu>
#     Fixed the timestamps for the PHIPS images. Also, added the option to 
#     attach the PHIPS particle elapsed time instead of the instant the particle
#     image was taken.
#
# Copyright 2019, 2020 David Delene
#
# This program is distributed under the terms of the GNU General Public License
#
# This file is part of Airborne Data Processing and Analysis (ADPAA).
#
# ADPAA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADPAA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADPAA.  If not, see <http://www.gnu.org/licenses/>.

import glob 
import numpy as np
import pandas as pd
import os 
import sys 

# Define syntax. 
def help_message():
    print('\n')
    print('Syntax: combine_PHIPS_Images.py <-h>\n\n')
    print('  Example: python combine_PHIPS_Images.py \n')

# Check input parameters. 
for param in sys.argv:
    if param.startswith('-h') | param.startswith('-help') | param.startswith('--help') | param.startswith('--h'):
       help_message()
       exit()

# Get FirstTimeStamp from *0000_C1.txt file.
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

#Convert First Time to Seconds From Midnight

FirstTimeSFM = int(FirstTimeHour) * 3600 + int(FirstTimeMin) * 60 + float(FirstTimeSecond)



# Define the First Image Time Stamp (UTC) and First Clock Tick.
# The first time stamp is from *C1.txt file,
# for example FirstTimeStamp_C1: 20190803143828932 -> 00793296671400
if (FirstTimeYYYY == 2019):
    if (FirstTimeMonth == 7):
        if (FirstTimeDay == 25):
            if (FirstTimeHour == 18):
                # This is for the 20190725_175413 
                FirstClockTick = '00497880189600'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006']
                prefix_input_file = '20190725-1759_'
        if (FirstTimeDay == 26):
            if (FirstTimeHour == 18):
                # This is for the 20190726_190024 
                FirstClockTick = '01145011633900'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010','0011']
                prefix_input_file = '20190726-1830_'
        if (FirstTimeDay == 29):
            if (FirstTimeHour == 21):
                # This is for the 20190729_191827 - Flight_190729b
                FirstClockTick = '06909383906600'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004']
                prefix_input_file = '20190729-2109_'
        if (FirstTimeDay == 30):
            if (FirstTimeHour == 18):
                # This is for the 20190730_174805 - Flight_190730
                FirstClockTick = '01405424119100'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010','0011','0012','0013','0014','0015','0016','0017']
                prefix_input_file = '20190730-1748_'
        if (FirstTimeDay == 31):
            if (FirstTimeHour == 19):
                # This is for the 20190731_191704 - Flight_190731a
                FirstClockTick = '01987193258700'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006']
                prefix_input_file = '20190731-1921_'
            if (FirstTimeHour == 21):
                # Not working, seems to be different format.
                # This is for the 20190731-191704 - Flight_190731b
                FirstClockTick = '08879140031900'
                # Define directory ID
                ids = ['0000','0001']
                prefix_input_file = '20190731-2142_'
    if (FirstTimeMonth == 8):
        if (FirstTimeDay == 1):
            if (FirstTimeHour == 19):
                # This is for the 20190801_192417 - PHIPS_Data/Flight_190801a
                FirstClockTick = '00546309278400'
                # Define directory ID
                ids = ['0000','0001','0002']
                prefix_input_file = '20190801-1926_'
            if (FirstTimeHour == 20):
                # This is for the 20190801_192417 - PHIPS_Data/Flight_190801b
                FirstClockTick = '00126244816900'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005']
                prefix_input_file = '20190801-2015_'
        if (FirstTimeDay == 2):
            if (FirstTimeHour == 14):
                # This is for the 20190802_143407
                FirstClockTick = '00429007976300'
                # Define directory ID
                ids = ['0000']
                prefix_input_file = '20190802-1448_'
            if (FirstTimeHour == 19):
                # This is for the 20190802_192915
                FirstClockTick = '00488851739700'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010']
                prefix_input_file = '20190802-1931_'
        if (FirstTimeDay == 3):
            if (FirstTimeHour == 14):
                # This is for the 20190803_142455
                FirstClockTick = '00793296671400'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008','0009','0010','0011','0012','0013','0014','0015','0016','0017']
                prefix_input_file = '20190803-1424_'
            if (FirstTimeHour == 21):
                # This is for the 20190803_203840
                FirstClockTick = '01626851003400'
                # Define directory ID
                ids = ['0000','0001','0002','0003','0004','0005','0006','0007','0008']
                prefix_input_file = '20190803-2040_'

#Next, Grab the times of the given PHIPS images from the level 3 .csv file.
#This file must be in the directory in which you're working from.
#The following lines create an array in which the index is the particle #'s
#and the first column is the given time of those particle #'s

timedata = np.loadtxt('PhipsData_20110221-0001_level_3.csv', dtype=object, delimiter=';', usecols=(1,5),skiprows=1)
column_names = ['datetime','imagenum']
timedata_df = pd.DataFrame(timedata, columns=column_names)
timedata_df[['datetime','time']] = timedata_df['datetime'].str.split(' ',expand=True)
pd.to_datetime(timedata_df['time'], format='%H:%M:%S.%f')
timedata_df = timedata_df.drop(columns=['datetime'])
timedata_df = timedata_df.set_index('time')
timedata_df.imagenum = timedata_df.imagenum.astype(float)
timedata_df = timedata_df.dropna()
timedata_df.imagenum = timedata_df.imagenum.astype(int)
timedata_df['imagenum'] = timedata_df['imagenum'].apply(lambda x: '{0:0>6}'.format(x))
timedata_df = timedata_df.reset_index()
timedata_df = timedata_df.set_index('imagenum')


# This first for loop looks in your directory to see if there is an existing
#C1-C2 sub directory, if not, then it makes one for you.
for dir_id in ids:
    #print( "dir_id = "+dir_id)
    if not os.path.exists(prefix_input_file+dir_id+'_C1-C2'):
        os.makedirs(prefix_input_file+dir_id+'_C1-C2')

    # Make sure we have output directory created.
    # Search for all files with the inputed syntax within the directory. 
    input_file = prefix_input_file+dir_id+'_C1/*C1.png'
    input = sorted(glob.glob(input_file))

    # Loop over the files, and concatenate the data. 
    for file1 in input:
        # Get file number.
        # For the given file number, grab the respected time from the array
        #created using the csv file.
        num=file1[61:67]
        time = timedata_df.loc[[num]]
        time = time['time'].tolist()
        time = " ".join(time)
        
        input2_file = prefix_input_file+dir_id+'_C2/*'
        input2 = sorted(glob.glob(input2_file+num+'*C2.png'))
        for file2 in input2:
            num2=file2[61:67]


            if (num == num2):
                # print("    "+num2)
                # Run montage shell command to combine png files.
                command = "montage " + file1 + " " + file2 + " -tile 2x1 -geometry +10+0 out" + num2 + ".png"
                os.system(command)
                #Uncomment everything up until END OF PROGRAM if you want the
                #partcle elapsed time attached to the newly created C1-C2 PHIPS
                #image files (see commented section below).
                CurrentImageFileTime = time
#                print(CurrentImageFileTime)

                # Move the file to new name.
                command = "mv out" + num + ".png " + prefix_input_file + dir_id + "_C1-C2/" + file1[21:46] + file1[61:67] + '_' + CurrentImageFileTime + ".C1-C2.png"
                os.system(command)
#END OF PROGRAM

"""                
From Martin on January 21, 2020 email:

PhipsData_<Date-Time of start of data acquisition>_<camera clock ticks>_<consecutive image number>_<camera 1 or camera 2>.png

In case you want to know the UTC time of the image, you can calculate this as following from the <camera clock ticks> contained in the image name:

- calculate the difference between the <camera clock ticks> and the clock ticks that correspond to the first image (stored in the *C1.txt log file of the data set).
- divide the result by 10e9. This gives you the seconds elapsed since the first image was taken.
- add the seconds to the absolute time of the first image (also given in the *C1.txt).

                # Defince current image clock ticks from the PHIPS *.png file.
                # The Current Image Tick when decoded is the elapsed time for
                #the given *.png particle file. If you want your C1-C2 images
                #to have the elapsed time instead of the instantaneous particle time
                #attached to the file name, comment out  uncomment 
                #the following code in this section.
                                                           
                CurrentImageTick = file1[46:60]
                CurrentImageSecond = int(int(CurrentImageTick) - int(FirstClockTick))
                CurrentImageSecond = CurrentImageSecond / 10**9           
                CurrentImageSFM    = FirstTimeSFM + CurrentImageSecond


                # Convert to seconds from midnight.
                seconds = CurrentImageSFM
                seconds = seconds % (24 * 3600)
                hour = seconds // 3600
                seconds %= 3600
                minutes = seconds // 60
                seconds %= 60


                # # Define time file name segment.
                k = "%.3f" % (seconds-int(seconds))
                CurrentImageFileTime = "_%02d:%02d:%02d" % (hour,minutes,seconds) + k[1:]
                print(CurrentImageFileTime)

                # Move the file to new name.
                command = "mv out" + num + ".png " + prefix_input_file + dir_id + "_C1-C2/" + file1[21:67] + CurrentImageFileTime + ".C1-C2.png"
                os.system(command)
"""

