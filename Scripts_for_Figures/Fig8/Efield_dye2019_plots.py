#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:54:24 2021

Syntax: ./Efield_dye2019_plots.py

Purpose: To generate E-Field plots as shown in Figure 8. Similar plots shown in Dye et al. 2019.

@author: christian.nairy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime


path = '/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'

cap = np.loadtxt(path + '19_08_03_14_24_55.cap', skiprows = 53, usecols = (0,30,31,32,33,34))

column_names = ['sfm','Ex','Ey','Ez','Eq','Emag']

cap_df = pd.DataFrame(cap,columns=column_names)

cap_df[cap_df > 100000] = np.nan

cap_df['Eq/Emag'] = (cap_df['Eq'] / cap_df['Emag'])

FL1 = cap_df[5177:5763]
FL2 = cap_df[5822:6122]
FL3 = cap_df[6242:6722]
FL4 = cap_df[6992:7322]
FL5 = cap_df[8102:8462]

#convert sfm to UTC
times = FL1['sfm'].to_numpy()
times = times.astype(int)
# times = times.tolist()
# times = pd.to_numeric(times, downcast='integer')

seconds = times % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60

time = np.vstack((hour, minutes, seconds)).T

time = pd.DataFrame(time, columns=('hours','minutes','seconds'))
time['hours'] = time['hours'].apply(lambda x: '{0:0>2}'.format(x))
time['minutes'] = time['minutes'].apply(lambda x: '{0:0>2}'.format(x))
time['seconds'] = time['seconds'].apply(lambda x: '{0:0>2}'.format(x))

time = (pd.to_datetime(time['hours'].astype(str) + ':' + time['minutes'].astype(str) + ':' + time['seconds'].astype(str), format='%H:%M:%S').dt.time)



time = time.to_frame()
time.columns = ['time_UTC']

FL1 = FL1.set_index(time['time_UTC'])


#PLOTTING
pd.plotting.register_matplotlib_converters()
from matplotlib.ticker import MaxNLocator


fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
ax2 = ax.twinx()

Ez = ax.plot(FL1.index, FL1['Ez'], c='b', label='Ez')
Emag = ax2.plot(FL1.index, FL1['Emag'], c='r', label='Emag')
Eq_div_Emag = ax.plot(FL1.index,FL1['Eq/Emag'], c='g', linestyle=':', label='Eq/Emag')

ax2.set_yscale('log')
ax2.set_ylim(0.1,100)
ax.set_ylim(-40,40)
ax.axhline(c='black', linestyle=':')
ax.set_xlabel('Time UTC')
ax.set_ylabel('Ez (blue) [Kv/m] \n Eq/Emag (green-dashed) [kV/m]')
ax2.set_ylabel('Emag (red) [kV/m]')
plt.tight_layout()

ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.xaxis.set_major_locator(MaxNLocator(12))
ax.xaxis.grid(linestyle=':')
plt.gcf().autofmt_xdate()


plt.show()

#####FL2

# convert sfm to UTC
times = FL2['sfm'].to_numpy()
times = times.astype(int)
# times = times.tolist()
# times = pd.to_numeric(times, downcast='integer')

seconds = times % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60

time = np.vstack((hour, minutes, seconds)).T

time = pd.DataFrame(time, columns=('hours','minutes','seconds'))
time['hours'] = time['hours'].apply(lambda x: '{0:0>2}'.format(x))
time['minutes'] = time['minutes'].apply(lambda x: '{0:0>2}'.format(x))
time['seconds'] = time['seconds'].apply(lambda x: '{0:0>2}'.format(x))

time = (pd.to_datetime(time['hours'].astype(str) + ':' + time['minutes'].astype(str) + ':' + time['seconds'].astype(str), format='%H:%M:%S').dt.time)



time = time.to_frame()
time.columns = ['time_UTC']

FL2 = FL2.set_index(time['time_UTC'])


#PLOTTING
pd.plotting.register_matplotlib_converters()
from matplotlib.ticker import MaxNLocator


fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
ax2 = ax.twinx()

Ez = ax.plot(FL2.index, FL2['Ez'], c='b', label='Ez')
Emag = ax2.plot(FL2.index, FL2['Emag'], c='r', label='Emag')
Eq_div_Emag = ax.plot(FL2.index,FL2['Eq/Emag'], c='g', linestyle=':', label='Eq/Emag')

ax2.set_yscale('log')
ax2.set_ylim(0.1,100)
ax.set_ylim(-40,40)
ax.axhline(c='black', linestyle=':')
ax.set_ylabel('Ez (blue) [Kv/m] \n Eq/Emag (green-dashed) [kV/m]')
ax.set_xlabel('Time UTC')
ax2.set_ylabel('Emag (red) [kV/m]')
plt.tight_layout()

ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.xaxis.set_major_locator(MaxNLocator(9))
ax.xaxis.grid(linestyle=':')
plt.gcf().autofmt_xdate()


plt.show()

#FL3

# convert sfm to UTC
times = FL3['sfm'].to_numpy()
times = times.astype(int)
# times = times.tolist()
# times = pd.to_numeric(times, downcast='integer')

seconds = times % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60

time = np.vstack((hour, minutes, seconds)).T

time = pd.DataFrame(time, columns=('hours','minutes','seconds'))
time['hours'] = time['hours'].apply(lambda x: '{0:0>2}'.format(x))
time['minutes'] = time['minutes'].apply(lambda x: '{0:0>2}'.format(x))
time['seconds'] = time['seconds'].apply(lambda x: '{0:0>2}'.format(x))

time = (pd.to_datetime(time['hours'].astype(str) + ':' + time['minutes'].astype(str) + ':' + time['seconds'].astype(str), format='%H:%M:%S').dt.time)



time = time.to_frame()
time.columns = ['time_UTC']

FL3 = FL3.set_index(time['time_UTC'])


#PLOTTING
pd.plotting.register_matplotlib_converters()
from matplotlib.ticker import MaxNLocator


fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
ax2 = ax.twinx()

Ez = ax.plot(FL3.index, FL3['Ez'], c='b', label='Ez')
Emag = ax2.plot(FL3.index, FL3['Emag'], c='r', label='Emag')
Eq_div_Emag = ax.plot(FL3.index,FL3['Eq/Emag'], c='g', linestyle=':', label='Eq/Emag')

ax2.set_yscale('log')
ax2.set_ylim(0.1,100)
ax.set_ylim(-40,40)
ax.axhline(c='black', linestyle=':')
ax.set_ylabel('Ez (blue) [Kv/m] \n Eq/Emag (green-dashed) [kV/m]')
ax.set_xlabel('Time UTC')
ax2.set_ylabel('Emag (red) [kV/m]')
plt.tight_layout()

ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.xaxis.set_major_locator(MaxNLocator(6))
ax.xaxis.grid(linestyle=':')
plt.gcf().autofmt_xdate()

plt.show()

#FL4

# convert sfm to UTC
times = FL4['sfm'].to_numpy()
times = times.astype(int)
# times = times.tolist()
# times = pd.to_numeric(times, downcast='integer')

seconds = times % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60

time = np.vstack((hour, minutes, seconds)).T

time = pd.DataFrame(time, columns=('hours','minutes','seconds'))
time['hours'] = time['hours'].apply(lambda x: '{0:0>2}'.format(x))
time['minutes'] = time['minutes'].apply(lambda x: '{0:0>2}'.format(x))
time['seconds'] = time['seconds'].apply(lambda x: '{0:0>2}'.format(x))

time = (pd.to_datetime(time['hours'].astype(str) + ':' + time['minutes'].astype(str) + ':' + time['seconds'].astype(str), format='%H:%M:%S').dt.time)



time = time.to_frame()
time.columns = ['time_UTC']

FL4 = FL4.set_index(time['time_UTC'])


#PLOTTING
pd.plotting.register_matplotlib_converters()
from matplotlib.ticker import MaxNLocator


fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
ax2 = ax.twinx()

Ez = ax.plot(FL4.index, FL4['Ez'], c='b', label='Ez')
Emag = ax2.plot(FL4.index, FL4['Emag'], c='r', label='Emag')
Eq_div_Emag = ax.plot(FL4.index,FL4['Eq/Emag'], c='g', linestyle=':', label='Eq/Emag')

ax2.set_yscale('log')
ax2.set_ylim(0.1,100)
ax.set_ylim(-40,40)
ax.axhline(c='black', linestyle=':')
ax.set_ylabel('Ez (blue) [Kv/m] \n Eq/Emag (green-dashed) [kV/m]')
ax.set_xlabel('Time UTC')
ax2.set_ylabel('Emag (red) [kV/m]')
plt.tight_layout()

ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.xaxis.set_major_locator(MaxNLocator(9))
ax.xaxis.grid(linestyle=':')
plt.gcf().autofmt_xdate()


plt.show()

#FL5

# convert sfm to UTC
times = FL5['sfm'].to_numpy()
times = times.astype(int)
# times = times.tolist()
# times = pd.to_numeric(times, downcast='integer')

seconds = times % (24 * 3600)
hour = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60

time = np.vstack((hour, minutes, seconds)).T

time = pd.DataFrame(time, columns=('hours','minutes','seconds'))
time['hours'] = time['hours'].apply(lambda x: '{0:0>2}'.format(x))
time['minutes'] = time['minutes'].apply(lambda x: '{0:0>2}'.format(x))
time['seconds'] = time['seconds'].apply(lambda x: '{0:0>2}'.format(x))

time = (pd.to_datetime(time['hours'].astype(str) + ':' + time['minutes'].astype(str) + ':' + time['seconds'].astype(str), format='%H:%M:%S').dt.time)



time = time.to_frame()
time.columns = ['time_UTC']

FL5 = FL5.set_index(time['time_UTC'])


#PLOTTING
pd.plotting.register_matplotlib_converters()
from matplotlib.ticker import MaxNLocator


fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
ax2 = ax.twinx()

Ez = ax.plot(FL5.index, FL5['Ez'], c='b', label='Ez')
Emag = ax2.plot(FL5.index, FL5['Emag'], c='r', label='Emag')
Eq_div_Emag = ax.plot(FL5.index,FL5['Eq/Emag'], c='g', linestyle=':', label='Eq/Emag')

ax2.set_yscale('log')
ax2.set_ylim(0.1,100)
ax.set_ylim(-40,40)
ax.axhline(c='black', linestyle=':')
ax.set_ylabel('Ez (blue) [Kv/m] \n Eq/Emag (green-dashed) [kV/m]')
ax.set_xlabel('Time UTC')
ax2.set_ylabel('Emag (red) [kV/m]')
plt.tight_layout()

ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.xaxis.set_major_locator(MaxNLocator(9))
ax.xaxis.grid(linestyle=':')
plt.gcf().autofmt_xdate()


plt.show()



















