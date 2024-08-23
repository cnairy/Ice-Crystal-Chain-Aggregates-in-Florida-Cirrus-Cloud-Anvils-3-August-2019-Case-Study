#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:14:15 2022

@author: christian.nairy
"""

#Written by: Christian Nairy <christian.nairy@und.edu>
#   2022/02/11 - Written

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = '/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'

phips = np.loadtxt(path + '19_08_03_14_24_00.phips_pbp_chains_conf_cplot.raw', skiprows = 64, usecols = (0,1,2,5,11,20))

column_names = ['time','chainagg','confidence','imagenum','maxD_C1', 'maxD_C2']

phips_df = pd.DataFrame(phips, columns=column_names)


#FL1
phips_df_FL1 = phips_df[19383:31598]

phips_df_FL1.replace(999999.9999, 0.0, inplace=True)
phips_df_FL1 = phips_df_FL1.loc[(phips_df_FL1['maxD_C1'] > 0.0) & phips_df_FL1['maxD_C2'] > 0.0]
phips_df_FL1['maxD'] = (phips_df_FL1['maxD_C1'] + phips_df_FL1['maxD_C2']) / 2.0

del phips_df_FL1['maxD_C1']
del phips_df_FL1['maxD_C2']


phips_df_FL1.loc[phips_df_FL1['chainagg'] > 10, 'confidence'] = 0
phips_df_FL1.loc[phips_df_FL1['chainagg'] == 0, 'confidence'] = 0
phips_df_FL1.loc[(phips_df_FL1['chainagg'] == 0) & (phips_df_FL1['confidence'] > 0), 'confidence'] = np.nan
phips_df_FL1[phips_df_FL1 > 99998] = np.nan
phips_df_FL1.loc[phips_df_FL1['chainagg'] == 0, 'chainagg'] = np.nan
phips_df_FL1.loc[phips_df_FL1['confidence'] == 0, 'confidence'] = np.nan


#FL2
phips_df_FL2 = phips_df[44453:68369]

phips_df_FL2.replace(999999.9999, 0.0, inplace=True)
phips_df_FL2 = phips_df_FL2.loc[(phips_df_FL2['maxD_C1'] > 0.0) & phips_df_FL2['maxD_C2'] > 0.0]
phips_df_FL2['maxD'] = (phips_df_FL2['maxD_C1'] + phips_df_FL2['maxD_C2']) / 2.0

del phips_df_FL2['maxD_C1']
del phips_df_FL2['maxD_C2']


phips_df_FL2.loc[phips_df_FL2['chainagg'] > 10, 'confidence'] = 0
phips_df_FL2.loc[phips_df_FL2['chainagg'] == 0, 'confidence'] = 0
phips_df_FL2.loc[(phips_df_FL2['chainagg'] == 0) & (phips_df_FL2['confidence'] > 0), 'confidence'] = np.nan
phips_df_FL2[phips_df_FL2 > 99998] = np.nan
phips_df_FL2.loc[phips_df_FL2['chainagg'] == 0, 'chainagg'] = np.nan
phips_df_FL2.loc[phips_df_FL2['confidence'] == 0, 'confidence'] = np.nan

#FL3
phips_df_FL3 = phips_df[68796:102429]

phips_df_FL3.replace(999999.9999, 0.0, inplace=True)
phips_df_FL3 = phips_df_FL3.loc[(phips_df_FL3['maxD_C1'] > 0.0) & phips_df_FL3['maxD_C2'] > 0.0]
phips_df_FL3['maxD'] = (phips_df_FL3['maxD_C1'] + phips_df_FL3['maxD_C2']) / 2.0

del phips_df_FL3['maxD_C1']
del phips_df_FL3['maxD_C2']


phips_df_FL3.loc[phips_df_FL3['chainagg'] > 10, 'confidence'] = 0
phips_df_FL3.loc[phips_df_FL3['chainagg'] == 0, 'confidence'] = 0
phips_df_FL3.loc[(phips_df_FL3['chainagg'] == 0) & (phips_df_FL3['confidence'] > 0), 'confidence'] = np.nan
phips_df_FL3[phips_df_FL3 > 99998] = np.nan
phips_df_FL3.loc[phips_df_FL3['chainagg'] == 0, 'chainagg'] = np.nan
phips_df_FL3.loc[phips_df_FL3['confidence'] == 0, 'confidence'] = np.nan


#FL4
phips_df_FL4 = phips_df[127871:141304]

phips_df_FL4.replace(999999.9999, 0.0, inplace=True)

phips_df_FL4 = phips_df_FL4.loc[(phips_df_FL4['maxD_C1'] > 0.0) & phips_df_FL4['maxD_C2'] > 0.0]
phips_df_FL4['maxD'] = (phips_df_FL4['maxD_C1'] + phips_df_FL4['maxD_C2']) / 2.0

del phips_df_FL4['maxD_C1']
del phips_df_FL4['maxD_C2']


phips_df_FL4.loc[phips_df_FL4['chainagg'] > 10, 'confidence'] = 0
phips_df_FL4.loc[phips_df_FL4['chainagg'] == 0, 'confidence'] = 0
phips_df_FL4.loc[(phips_df_FL4['chainagg'] == 0) & (phips_df_FL4['confidence'] > 0), 'confidence'] = np.nan
phips_df_FL4[phips_df_FL4 > 99998] = np.nan
phips_df_FL4.loc[phips_df_FL4['chainagg'] == 0, 'chainagg'] = np.nan
phips_df_FL4.loc[phips_df_FL4['confidence'] == 0, 'confidence'] = np.nan
# ###############################################################################
#grab all chains that have confidence 2 and 3
#FL1 chains
phips_df_FL1_chains = phips_df_FL1[(phips_df_FL1['chainagg'] > 0.5)]
phips_df_FL1_chains = phips_df_FL1[(phips_df_FL1['confidence'] > 1.9)]
print(phips_df_FL1_chains['maxD'].mean())
print(phips_df_FL1_chains['maxD'].min())
print(phips_df_FL1_chains['maxD'].max())


#FL2 chains
phips_df_FL2_chains = phips_df_FL2[(phips_df_FL2['chainagg'] > 0.5)]
phips_df_FL2_chains = phips_df_FL2[(phips_df_FL2['confidence'] > 1.9)]
print(phips_df_FL2_chains['maxD'].mean())
print(phips_df_FL2_chains['maxD'].min())
print(phips_df_FL2_chains['maxD'].max())

#FL3 chains
phips_df_FL3_chains = phips_df_FL3[(phips_df_FL3['chainagg'] > 0.5)]
phips_df_FL3_chains = phips_df_FL3[(phips_df_FL3['confidence'] > 1.9)]
print(phips_df_FL3_chains['maxD'].mean())
print(phips_df_FL3_chains['maxD'].min())
print(phips_df_FL3_chains['maxD'].max())

#FL4 chains
phips_df_FL4_chains = phips_df_FL4[(phips_df_FL4['chainagg'] > 0.5)]
phips_df_FL4_chains = phips_df_FL4[(phips_df_FL4['confidence'] > 1.9)]
print(phips_df_FL4_chains['maxD'].mean())
print(phips_df_FL4_chains['maxD'].min())
print(phips_df_FL4_chains['maxD'].max())

#delete unnessesary columns for box plotting
del phips_df_FL1_chains['time']
del phips_df_FL1_chains['chainagg']
del phips_df_FL1_chains['confidence']
del phips_df_FL1_chains['imagenum']
phips_df_FL1_chains['Flight Legs'] = 'Flight Leg 1'

del phips_df_FL2_chains['time']
del phips_df_FL2_chains['chainagg']
del phips_df_FL2_chains['confidence']
del phips_df_FL2_chains['imagenum']
phips_df_FL2_chains['Flight Legs'] = 'Flight Leg 2'

del phips_df_FL3_chains['time']
del phips_df_FL3_chains['chainagg']
del phips_df_FL3_chains['confidence']
del phips_df_FL3_chains['imagenum']
phips_df_FL3_chains['Flight Legs'] = 'Flight Leg 3'

del phips_df_FL4_chains['time']
del phips_df_FL4_chains['chainagg']
del phips_df_FL4_chains['confidence']
del phips_df_FL4_chains['imagenum']
phips_df_FL4_chains['Flight Legs'] = 'Flight Leg 4'


data_FLs = [phips_df_FL1_chains, phips_df_FL2_chains, phips_df_FL3_chains, phips_df_FL4_chains]
FL = pd.concat(data_FLs)

#Box plotting
#Box plotting
plt.figure(figsize=(12,12))
FL.boxplot(by="Flight Legs")
title_boxplot = 'FL1-4: Size of Chain Aggregates with Confidence >= 2'
plt.title(title_boxplot)
plt.ylabel('Diameter' + ' ' +'(' u"\u03bcm"')')
plt.ylim(0,1000)
plt.suptitle('') # that's what you're after
plt.text(1.02,100,'n = 37')
plt.text(2.02,100,'n = 28')
plt.text(3.02,100,'n = 38')
plt.text(4.02,100,'n = 31')
plt.show()

FL1_chain_size = phips_df_FL1_chains['maxD']
FL2_chain_size = phips_df_FL2_chains['maxD']
FL3_chain_size = phips_df_FL3_chains['maxD']
FL4_chain_size = phips_df_FL4_chains['maxD']

FL1_4_chain_size = pd.concat([FL1_chain_size, FL2_chain_size, FL3_chain_size, FL4_chain_size], axis=1)

quantiles = FL1_4_chain_size.quantile([0.25,0.5,0.75])


#%%
#Now create boxplots wrt to distance from core
#FL1
FL1_100_70 = phips_df_FL1
FL1_100_70 = FL1_100_70[(FL1_100_70['chainagg'] > 0.5)]
FL1_100_70 = FL1_100_70[(FL1_100_70['confidence'] > 1.9)]
FL1_70_40 = phips_df_FL1
FL1_70_40 = FL1_70_40[(FL1_70_40['chainagg'] > 0.5)]
FL1_70_40 = FL1_70_40[(FL1_70_40['confidence'] > 1.9)]
FL1_40_10 = phips_df_FL1
FL1_40_10 = FL1_40_10[(FL1_40_10['chainagg'] > 0.5)]
FL1_40_10 = FL1_40_10[(FL1_40_10['confidence'] > 1.9)]

#FL2
FL2_70_40 = phips_df_FL2
FL2_70_40 = FL2_70_40[(FL2_70_40['chainagg'] > 0.5)]
FL2_70_40 = FL2_70_40[(FL2_70_40['confidence'] > 1.9)]
FL2_40_10 = phips_df_FL2
FL2_40_10 = FL2_40_10[(FL2_40_10['chainagg'] > 0.5)]
FL2_40_10 = FL2_40_10[(FL2_40_10['confidence'] > 1.9)]

#FL3
FL3_100_70 = phips_df_FL3
FL3_100_70 = FL3_100_70[(FL3_100_70['chainagg'] > 0.5)]
FL3_100_70 = FL3_100_70[(FL3_100_70['confidence'] > 1.9)]
FL3_70_40 = phips_df_FL3
FL3_70_40 = FL3_70_40[(FL3_70_40['chainagg'] > 0.5)]
FL3_70_40 = FL3_70_40[(FL3_70_40['confidence'] > 1.9)]
FL3_40_10 = phips_df_FL3
FL3_40_10 = FL3_40_10[(FL3_40_10['chainagg'] > 0.5)]
FL3_40_10 = FL3_40_10[(FL3_40_10['confidence'] > 1.9)]

#FL4
FL4_70_40 = phips_df_FL4
FL4_70_40 = FL4_70_40[(FL4_70_40['chainagg'] > 0.5)]
FL4_70_40 = FL4_70_40[(FL4_70_40['confidence'] > 1.9)]
FL4_100_70 = phips_df_FL4
FL4_100_70 = FL4_100_70[(FL4_100_70['chainagg'] > 0.5)]
FL4_100_70 = FL4_100_70[(FL4_100_70['confidence'] > 1.9)]


#%%

















