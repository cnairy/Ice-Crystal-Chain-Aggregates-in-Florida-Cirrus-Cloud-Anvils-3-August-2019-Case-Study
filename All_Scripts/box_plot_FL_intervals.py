#Create box plots of the chain aggregate information (e.g. Diameter) within
#the Individual flight legs.
#Written by: Christian Nairy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = '/nas/und/Florida/2019/Aircraft/CitationII_N555DS/FlightData/20190803_142455/PHIPS_Images/'

#Diameter of Chains
C1_C2 = np.loadtxt(path + '19_08_03_14_24_00.phips_pbp_chains_conf.raw', skiprows=2496, usecols=(0,5,11,20,46,47))

df_C1_C2 = pd.DataFrame(C1_C2)

df_C1_C2.columns = ['sfm','Image_Num','Dmax_C1','Dmax_C2','Chains','Confidence']

#drop unnessessary data rows
df_C1_C2 = df_C1_C2[df_C1_C2.Image_Num != 9999999]

#remove confidence values for non chains
df_C1_C2.loc[df_C1_C2.Chains == 0.0, 'Confidence'] = 0.0
df_C1_C2.loc[df_C1_C2.Chains == 99999.999, 'Confidence'] = 0.0

#replace 0's and 9999999 with NaN's
df_C1_C2 = df_C1_C2.replace(0.0,np.nan)
df_C1_C2 = df_C1_C2.replace(999999.9999,0.0)
df_C1_C2 = df_C1_C2.replace(99999.999,np.nan)

chains_all_conf = df_C1_C2.loc[df_C1_C2['Chains'] >= 1]
chains_conf_high = df_C1_C2.loc[df_C1_C2['Confidence'] >= 2]
# chains_conf_high = chains_conf_high.replace(-99999.999, np.nan)



# chains_conf_high.Diameter_C1.fillna(chains_conf_high.Diameter_C2, inplace=True)
# chains_conf_high.Diameter_C2.fillna(chains_conf_high.Diameter_C1, inplace=True)

highest_diameter_C1 = chains_conf_high.loc[(chains_conf_high['Dmax_C1'] > chains_conf_high['Dmax_C2'])] 
highest_diameter_C2 = chains_conf_high.loc[(chains_conf_high['Dmax_C2'] > chains_conf_high['Dmax_C1'])] 
del highest_diameter_C1['sfm']
del highest_diameter_C1['Dmax_C2']
del highest_diameter_C1['Chains']
del highest_diameter_C1['Confidence']
del highest_diameter_C2['sfm']
del highest_diameter_C2['Dmax_C1']
del highest_diameter_C2['Chains']
del highest_diameter_C2['Confidence']

highest_diameter_C1.columns = ['Image_Num','Dmax']
highest_diameter_C2.columns = ['Image_Num','Dmax']

del chains_conf_high['Dmax_C1']
del chains_conf_high['Dmax_C2']

max_diameter = highest_diameter_C1.append(highest_diameter_C2, ignore_index=True)
max_diameter.sort_values(by=['Image_Num'],inplace=True,ascending=True)

df_Dmax_with_chains = pd.merge(chains_conf_high, max_diameter, on='Image_Num')

#Remove rows with diamter than than 10um
df_Dmax_with_chains = df_Dmax_with_chains[~(df_Dmax_with_chains['Dmax'] <= 10)]

# #Define the Flight legs
# #FL1
FL1_first = df_Dmax_with_chains.loc[0:21,:]
FL1_second = df_Dmax_with_chains.loc[22:56,:]
FL1_third = df_Dmax_with_chains.loc[57:90,:]
# #FL2
FL2_first = df_Dmax_with_chains.loc[91:101,:] # zero chains found in this segment
FL2_second = df_Dmax_with_chains.loc[102:113,:]
FL2_third = df_Dmax_with_chains.loc[114:137,:]
# #FL3
FL3_first = df_Dmax_with_chains.loc[138:171,:]
FL3_second = df_Dmax_with_chains.loc[172:195,:]
FL3_third = df_Dmax_with_chains.loc[196:220,:]
# #FL4
FL4_first = df_Dmax_with_chains.loc[221:236,:]
FL4_second = df_Dmax_with_chains.loc[237:259,:]
FL4_third = df_Dmax_with_chains.loc[260:282,:]
# #FL5
FL5_first = df_Dmax_with_chains.loc[283:304,:]
FL5_second = df_Dmax_with_chains.loc[305:329,:]
FL5_third = df_Dmax_with_chains.loc[330:350,:]

#########################################################################
#Flight Leg 1 Array manipulation
FL1_first = FL1_first.loc[FL1_first['Confidence'] >= 2]
FL1_second = FL1_second.loc[FL1_second['Confidence'] >= 2]
FL1_third = FL1_third.loc[FL1_third['Confidence'] >= 2]

del FL1_first['sfm']
del FL1_first['Image_Num']
del FL1_first['Chains']
del FL1_first['Confidence']
FL1_first['Data_FL1'] = 'First 1/3 of Flight'

del FL1_second['sfm']
del FL1_second['Image_Num']
del FL1_second['Chains']
del FL1_second['Confidence']
FL1_second['Data_FL1'] = 'Second 1/3 of Flight'

del FL1_third['sfm']
del FL1_third['Image_Num']
del FL1_third['Chains']
del FL1_third['Confidence']
FL1_third['Data_FL1'] = 'Third 1/3 of Flight'

data_FL1 = [FL1_first, FL1_second, FL1_third]
FL1 = pd.concat(data_FL1)

##########################################################################
#Flight Leg 2 Array manipulation
FL2_first = FL2_first.loc[FL2_first['Confidence'] >= 2]
FL2_second = FL2_second.loc[FL2_second['Confidence'] >= 2]
FL2_third = FL2_third.loc[FL2_third['Confidence'] >= 2]

del FL2_first['sfm']
del FL2_first['Image_Num']
del FL2_first['Chains']
del FL2_first['Confidence']
FL2_first['Data_FL2'] = 'First 1/3 of Flight'

del FL2_second['sfm']
del FL2_second['Image_Num']
del FL2_second['Chains']
del FL2_second['Confidence']
FL2_second['Data_FL2'] = 'Second 1/3 of Flight'

del FL2_third['sfm']
del FL2_third['Image_Num']
del FL2_third['Chains']
del FL2_third['Confidence']
FL2_third['Data_FL2'] = 'Third 1/3 of Flight'

data_FL2 = [FL2_first, FL2_second, FL2_third]
FL2 = pd.concat(data_FL2)

#########################################################################
#Flight Leg 3 Array manipulation
FL3_first = FL3_first.loc[FL3_first['Confidence'] >= 2]
FL3_second = FL3_second.loc[FL3_second['Confidence'] >= 2]
FL3_third = FL3_third.loc[FL3_third['Confidence'] >= 2]

del FL3_first['sfm']
del FL3_first['Image_Num']
del FL3_first['Chains']
del FL3_first['Confidence']
FL3_first['Data_FL3'] = 'First 1/3 of Flight'

del FL3_second['sfm']
del FL3_second['Image_Num']
del FL3_second['Chains']
del FL3_second['Confidence']
FL3_second['Data_FL3'] = 'Second 1/3 of Flight'

del FL3_third['sfm']
del FL3_third['Image_Num']
del FL3_third['Chains']
del FL3_third['Confidence']
FL3_third['Data_FL3'] = 'Third 1/3 of Flight'

data_FL3 = [FL3_first, FL3_second, FL3_third]
FL3 = pd.concat(data_FL3)

#########################################################################
#Flight Leg 4 Array manipulation
FL4_first = FL4_first.loc[FL4_first['Confidence'] >= 2]
FL4_second = FL4_second.loc[FL4_second['Confidence'] >= 2]
FL4_third = FL4_third.loc[FL4_third['Confidence'] >= 2]

del FL4_first['sfm']
del FL4_first['Image_Num']
del FL4_first['Chains']
del FL4_first['Confidence']
FL4_first['Data_FL4'] = 'First 1/3 of Flight'

del FL4_second['sfm']
del FL4_second['Image_Num']
del FL4_second['Chains']
del FL4_second['Confidence']
FL4_second['Data_FL4'] = 'Second 1/3 of Flight'

del FL4_third['sfm']
del FL4_third['Image_Num']
del FL4_third['Chains']
del FL4_third['Confidence']
FL4_third['Data_FL4'] = 'Third 1/3 of Flight'

data_FL4 = [FL4_first, FL4_second, FL4_third]
FL4 = pd.concat(data_FL4)

#########################################################################
#Flight Leg 5 Array manipulation
FL5_first = FL5_first.loc[FL5_first['Confidence'] >= 2]
FL5_second = FL5_second.loc[FL5_second['Confidence'] >= 2]
FL5_third = FL5_third.loc[FL5_third['Confidence'] >= 2]

del FL5_first['sfm']
del FL5_first['Image_Num']
del FL5_first['Chains']
del FL5_first['Confidence']
FL5_first['Data_FL5'] = 'First 1/3 of Flight'

del FL5_second['sfm']
del FL5_second['Image_Num']
del FL5_second['Chains']
del FL5_second['Confidence']
FL5_second['Data_FL5'] = 'Second 1/3 of Flight'

del FL5_third['sfm']
del FL5_third['Image_Num']
del FL5_third['Chains']
del FL5_third['Confidence']
FL5_third['Data_FL5'] = 'Third 1/3 of Flight'

data_FL5 = [FL5_first, FL5_second, FL5_third]
FL5 = pd.concat(data_FL5)


#Box plotting
plt.figure()
FL5.boxplot(by="Data_FL5")
title_boxplot = 'FL5: Maximum Diameter of Chain Aggregates with Confidence >= 2'
plt.title(title_boxplot)
plt.ylabel('Diameter (um)')
plt.ylim(0,1000)
plt.suptitle('') # that's what you're after
plt.text(1.02,100,'n = 22')
plt.text(2.02,100,'n = 24')
plt.text(3.02,100,'n = 21')
plt.show()





















