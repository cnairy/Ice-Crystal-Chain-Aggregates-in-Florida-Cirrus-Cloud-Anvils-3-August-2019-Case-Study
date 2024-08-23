import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units

# Change default to be better for skew-T
plt.rcParams['figure.figsize'] = (9, 9)
plt.rcParams['figure.dpi'] = 300

# Read the data from the file
path = '/home/chains/Documents/masters/science_files/'
data = pd.read_csv(path + 'B215B6-trimmed.txt', delim_whitespace=True, skiprows=1, usecols = [5,4,6,7,8,9],encoding='latin-1')
column_names = ['height', 'pressure', 'temperature', 'rel_hum', 'speed','direction']
data.columns = column_names
data.replace('//',np.nan, inplace=True)
data = data.astype(float)
data['rel_hum'] = data['rel_hum'] / 100.0

# data_np = data.to_numpy()

# Constants
a = 17.27
b = 237.7

# Function to calculate vapor pressure
def calculate_vapor_pressure(temperature, relative_humidity):
    e = (a * temperature) / (b + temperature) + np.log(relative_humidity)
    return e

# Function to calculate dewpoint
def calculate_dewpoint(temperature, relative_humidity):
    e = calculate_vapor_pressure(temperature, relative_humidity)
    dewpoint = (b * e) / (a - e)
    return dewpoint

# Calculate dewpoint and add to DataFrame
data['dewpoint'] = data.apply(lambda row: calculate_dewpoint(row['temperature'], row['rel_hum']), axis=1)


# col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']
df = data.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed'
                       ), how='all').reset_index(drop=True)

p = df['pressure'].values * units.hPa
T = df['temperature'].values * units.degC
Td = df['dewpoint'].values * units.degC
wind_speed = df['speed'].values * units.knots
wind_dir = df['direction'].values * units.degrees
u, v = mpcalc.wind_components(wind_speed, wind_dir)

skew = SkewT()

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p[:3000:35], u[:3000:35], v[:3000:35])

# Set some better labels than the default
skew.ax.set_xlabel('Temperature (\N{DEGREE CELSIUS})',fontsize=16)
skew.ax.set_ylabel('Pressure (mb)',fontsize=16)


# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)

# Add the MetPy logo!
fig = plt.figure(figsize=(16,6))
# add_metpy_logo(fig, 115, 100)
