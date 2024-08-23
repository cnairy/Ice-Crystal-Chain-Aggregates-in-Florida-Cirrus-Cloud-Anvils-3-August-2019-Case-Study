#!/usr/bin/env python3
"""
  NAME:
   Fieldmills_make_Emag.py
 
  PURPOSE:
    Use 1Hz fieldmill data (in nasa format) and calculate E magnitude (Emag)

  CALLS:
    ADPAA

  EXAMPLE:
    The command:

       Fieldmills_make_Emag.py 19_08_03_14_29_57.fieldmills.1Hz.raw

    create the 19_08_03_14_24_55.fieldmills.Emag.1Hz.raw file.
   
   ***MUST BE IN DIRECTORY WHERE 19_08_03_14_29_57.fieldmills.1Hz.raw FILE IS LOCATED***

  MODIFICATIONS:
    Christian Nairy <christian.nairy@und.edu> - 2020/07/28:
      Written.
    Christian Nairy <christian.nairy@und.edu> - 2021/09/21:
        Added the calculation for the total scalar magnitude of the E-field

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
import sys


if len(sys.argv) != 2:
      print("SYNTAX:  Fieldmills_make_Emag.py inputfile")
      print( "")
      print( "  inputfile - The 19_08_03_14_29_57.fieldmills.1Hz.raw file.")
      print( "  Example: Fieldmills_make_Emag.py 19_08_03_14_29_57.fieldmills.1Hz.raw")
      print( "")
      sys.exit()


# #import file mentioned on the command line
_infile = sys.argv[1]

#Load text file and skip the rows with ADPAA text
dataset_1Hz = np.loadtxt(_infile, skiprows=23)


#Convert to pandas dataset
dataset_pd_1hz = pd.DataFrame(dataset_1Hz)

#Create column names
dataset_pd_1hz.columns = ['sfm','Ex','Ey','Ez','Eq']

#Change dataset into numpy based arrays
sfm = dataset_pd_1hz.sfm.to_numpy()
Ex = dataset_pd_1hz.Ex.to_numpy()
Ey = dataset_pd_1hz.Ey.to_numpy()
Ez = dataset_pd_1hz.Ez.to_numpy()
Eq = dataset_pd_1hz.Eq.to_numpy()

#Calculate the electric field scalar magnitude
E_mag = ((Ex)**2 + (Ey)**2 + (Ez)**2)**(1/2)
E_mag = np.where(E_mag < 1000, E_mag, 999999.9999)


#Create ADPAA output object.
out = ADPAA()
out.DREV   = 0
# Fill output object.
out.NLHEAD = 22
out.FFI    = 1001
out.ONAME  = 'Delene, David'
out.ORG    = 'University of North Dakota'
out.SNAME  = 'Atmospheric Science Dept.'
out.MNAME  = 'Rotating Vane Electric Field Mill Data taken from the Citation II'
out.IVOL   = 1
out.VVOL   = 1
out.DATE   = '2019 08 03'
#out.DATE   = _data_matrix[0][0][:4] + ' ' + _data_matrix[0][0][5:7]+ ' ' + _data_matrix[0][0][8:10]
# out.RDATE  = (time.strftime("%Y %m %d"))
out.RDATE  = 'N/A'
out.DX     = 1.0000
out.XNAME  = 'Time [second]; UT seconds from midnight on day measurements started.'
out.NV     = 5
out.VSCAL  = ['     1.0000','     1.0000','     1.0000','     1.0000','     1.0000']
out.VMISS  = ['999999.9999','999999.9999','999999.9999','999999.9999','999999.9999']
out.VNAME  = ['Ex Electric field out of the length of the plane (forward +) [kV/m]','Ey Electric field along the wings of the plane (port +)[kV/m]','Ez Electric field along the top and bottom of plane (up +)[kV/m]','Eq Electric field due to charging on the planes surface[kV/m]', 'Emag Electric field vector scalar magnitude [kV/m]']
out.DTYPE  = 'Cal signal data times have been set to 999999.9999'
out.VFREQ  = '1 Hz Data'
out.VDESC  = ['Time','Ex','Ey','Ez','Eq','Emag']
out.VUNITS = ['s','kV/m','kV/m','kV/m','kV/m','kV/m']
out.data = {"Time":sfm,"Ex":Ex,"Ey":Ey,"Ez":Ez,"Eq":Eq,"Emag":E_mag}

# name_elements = _infile.split('.')
# yy = name_elements[0][12:13]
# mm = name_elements[0][8:10]
# dd = name_elements[0][10:12]
# hh = name_elements[0][13:15]
# mi = name_elements[0][15:17]
# ss = name_elements[0][17:19]
#NEED TO EXPLICITLY NAME THE FILE DUE TO THE TIME OF THE ORIGINAL FILE BEING OFF (19_08_03_14_29_57 should be 19_08_03_14_24_55)
out.name = '19_07_30_17_48_05.fieldmills_Eq.1Hz.raw'
out.WriteFile()


























