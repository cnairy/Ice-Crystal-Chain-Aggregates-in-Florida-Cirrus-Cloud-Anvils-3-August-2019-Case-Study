#When running in a separate Python script, use the following syntax:
from GOESLib_christian_nldn import *
date_str = '201908031531'  # date_str in YYYYMMDDHHMM format, for whatever the time of the GOES file 
scan_end = '1534'
channel = 2

plot_GOES_satpy(date_str, scan_end, 2)













