#!/bin/env python3 
"""
  NAME:
    CIP_Chain-Concs_merge.py
 
  PURPOSE:
    This script uses the updated science file that contains the chain, non-chain, and total particle concentration data.
    (CIP > 495um, CIP between 105 - 315 um, CIP > 105 um).
    
    It calculates the RATIOcn and RATIOall then uses mergefield to merge the data file into the over science file.


  CALLS:
    ADPAA

  EXAMPLE:
    The command:
        CIP_Chain-Concs_merge.py 'science file with CIP total, chain, and non chain, concentrations'
        
    For Example:
        CIP_Chain-Concs_merge.py 19_08_04_14_24_55.cap

       

    creates: 
        YY_MM_DD_HH_MI_SS.RCAC.1Hz data file with relative chain agg concentrations.
        &
        YY_MM_DD_HH_MI_SS.cap.YYMMDD - where the yymmdd at the end of the file is todays date.

  MODIFICATIONS:
    Christian Nairy <christian.nairy@und.edu> - 2022/08/22:
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
import os
import sys
from adpaa_python3 import ADPAA
import numpy as np
from datetime import date

#ignore runtime warnings
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 

#Sys argument. read in science file
cap_infile = sys.argv[1]

cap = ADPAA()
cap.ReadFile(cap_infile)


# cap.ReadFile(path_1 + filename_1)  #test
sfm = cap.data['Time']
chain_conc = cap.data['CIPV_495um']
tot_conc = cap.data['CIPV_105um']
non_chain_conc = cap.data['CIPV_105-31']

#does the math to get the RCACnc and RCACall data.
RCACnc = chain_conc / non_chain_conc
RCACall = chain_conc / tot_conc

#MVC
RCACnc[np.isnan(RCACnc)]=99999.999
RCACall[np.isnan(RCACall)]=99999.999

RCACnc[np.isinf(RCACnc)]=99999.999
RCACall[np.isinf(RCACall)]=99999.999

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
out.NV     = 2
out.VSCAL  = ['        1', '        1']
out.VMISS  = ['99999.999', '99999.999', ]
out.VNAME  = ['Relative Chain Aggregates Concentation with respect to non-chain aggregates','Relative Chain Aggregates Concentation with respect to all CIP particles > 105 um']
# out.NSCOML = 0
# out.NNCOML = 4
out.DTYPE  = 'Final Data'
out.DREV   = 0
out.VFREQ  = 'Asychronous'
out.VDESC  = ['Time','RCAC_nc','RCAC_all']
out.VUNITS = ['seconds','      NONE','      NONE',]
out.data = {"Time":sfm,'RCAC_nc':RCACnc,'RCAC_all':RCACall}

name_elements = cap_infile.split('.')
yy = name_elements[0][0:2]
mm = name_elements[0][3:5]
dd = name_elements[0][6:8]
hh = name_elements[0][9:11]
mi = name_elements[0][12:14]
ss = name_elements[0][15:17]
out.name = yy + '_' + mm + '_' + dd + '_' + hh + '_' + mi + '_' + ss + '.RCAC.1Hz'
out.WriteFile()
###############################
#Merge the created file into the overall science file

today = date.today()
today_date = today.strftime("%y.%m.%d")

td_yy = today_date[0:2] 
td_mm = today_date[3:5]
td_dd = today_date[6:8]

tar_1 = cap.NV + 1
tar_1 = str(tar_1)
tar_2 = cap.NV + 2
tar_2 = str(tar_2)


#Call mergefield 
os.system('mergefield field=1,2' + ' target=' + tar_1 + ',' + tar_2 + ' file=' + out.name + ' ' + '< ' + cap_infile + ' > ' + cap_infile + '.' + td_yy + td_mm + td_dd)














