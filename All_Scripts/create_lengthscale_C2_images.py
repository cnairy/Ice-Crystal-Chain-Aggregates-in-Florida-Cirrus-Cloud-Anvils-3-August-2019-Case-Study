"""
Syntax: ./create_lengthscale_C2_images.py

Purpose: Rescale PHIPS C2 images to match the same length scale as the C1 images.


Author: @christian.nairy
"""

#Imports
import cv2
import glob
import os
import numpy as np
import pandas as pd

#Path to C2 images
filepath2 = '/nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/PHIPS_Data/enhanced_images/Enhanced_images/FL1/Resized/C2'

#GET NEW TIME DATA###############################################
timedata = np.loadtxt('PhipsData_20110221-0001_level_3.csv', dtype=object, delimiter=';', usecols=(1,5),skiprows=1)
# imagenumber = np.loadtxt('PhipsData_20110221-0001_level_3.csv', delimiter=';', usecols=(5), skiprows=1)


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
#####################################################################

i = 0
for raw_img in glob.glob('*.png'):
    num = raw_img[39:45]
    # print(num)
    newtime = timedata_df.loc[[num]]
    newtime = newtime['time'].tolist()
    newtime = " ".join(newtime)

    times = newtime
    #"""Get Seconds from time."""
    h, m, s = times.split(':')
    times = int(h) * 3600 + int(m) * 60 + float(s)
    #Convert to seconds from midnight.
    seconds = times % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    k = "%.3f" % (seconds-int(seconds))
    CurrentImageFileTime = "%02d:%02d:%02d" % (hour,minutes,seconds) + k[1:]
    # print(CurrentImageFileTime)

    image = cv2.imread(raw_img)
    print(raw_img)

#Change scale based on PHIPS Magnification of C2 images during the 20190803 flight.
    scale_percent = 1.10
    width = int(image.shape[1]*scale_percent)
    height = int(image.shape[0]*scale_percent)
    dimension = (width,height)
    resized=cv2.resize(image,dimension,interpolation=cv2.INTER_AREA)
    start_point = (646,35)
    end_point = (850,35)
    color = (0,0,255) #red line
    timestamp_color = (0,0,0)
    thickness = 10
    # #text information
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (685, 70)
    timestamp_loc = (500,70)
    fontScale = 1
    timestamp_fontscale = 2
    thickness_text = 3
    border_color = (0,0,0)
    image1 = cv2.putText(resized, '200 um', org, font, 
                fontScale, color, thickness_text, cv2.LINE_AA)
    image2 = cv2.line(image1, start_point, end_point, color, thickness)
    image3 = cv2.copyMakeBorder(image2, 100, 0, 0, 0, cv2.BORDER_CONSTANT, value=border_color)
    image4 = cv2.putText(image3, CurrentImageFileTime + ' ' + 'UTC', timestamp_loc, font, 
                timestamp_fontscale, color, thickness_text, cv2.LINE_AA) # for C1
    # cv2.imshow('image',resized)

    cv2.imwrite(os.path.join(filepath2, 'PhipsData_20190903a_' + CurrentImageFileTime + '_' + raw_img[39:46] + 'Resized_with_lengthscale_C2.png'), image4)
    i +=1




