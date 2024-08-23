#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 09:47:23 2022

Purpose: This script will read in the PHIPS probe generated php file and will output the number of chains
    based on confidence and distance from core. The script will sum up these values.

NOTE: THIS SCRIPT IS SPECIFICALLY DESIGNED TO ONLY RUN FOR THE 20190803_1424 FLIGHT!
    
@author: christian.nairy
"""
#Number of chains using the phips php file for 20190803 flight
import numpy as np
import pandas as pd
import os
import shutil

path = '/home/christian.nairy/capeex19/Aircraft/CitationII_N555DS/FlightData/20190803_142455/Analysis/Updated_FLs/science_files/'

phips = np.loadtxt(path + '19_08_03_14_24_00.phips_pbp_chains_conf_cplot.raw', skiprows = 64, usecols = (0,1,2,5))

column_names = ['time','chainagg','confidence','imagenum']

phips_df = pd.DataFrame(phips, columns=column_names)

FL1 = phips_df[19383:31598]
FL1 = FL1[FL1['imagenum'] != 9999999.000000]
FL1[FL1 > 99998] = 0
FL1_conf3_chains_old = FL1.loc[(FL1['chainagg'] == 1) & (FL1['confidence'] == 3)]
FL1_conf2_chains_old = FL1.loc[(FL1['chainagg'] == 1) & (FL1['confidence'] == 2)]
FL1_conf2_chains = pd.concat([FL1_conf3_chains_old, FL1_conf2_chains_old])
FL1_conf1_chains = FL1.loc[(FL1['chainagg'] == 1) & (FL1['confidence'] == 1)]

FL2 = phips_df[44453:68370]
FL2 = FL2[FL2['imagenum'] != 9999999.000000]
FL2[FL2 > 99998] = 0
FL2_conf3_chains_old = FL2.loc[(FL2['chainagg'] == 1) & (FL2['confidence'] == 3)]
FL2_conf2_chains_old = FL2.loc[(FL2['chainagg'] == 1) & (FL2['confidence'] == 2)]
FL2_conf2_chains = pd.concat([FL2_conf3_chains_old, FL2_conf2_chains_old])
FL2_conf1_chains = FL2.loc[(FL2['chainagg'] == 1) & (FL2['confidence'] == 1)]

FL3 = phips_df[68796:102429]
FL3 = FL3[FL3['imagenum'] != 9999999.000000]
FL3[FL3 > 99998] = 0
FL3_conf3_chains_old = FL3.loc[(FL3['chainagg'] == 1) & (FL3['confidence'] == 3)]
FL3_conf2_chains_old = FL3.loc[(FL3['chainagg'] == 1) & (FL3['confidence'] == 2)]
FL3_conf2_chains = pd.concat([FL3_conf3_chains_old, FL3_conf2_chains_old])
FL3_conf1_chains = FL3.loc[(FL3['chainagg'] == 1) & (FL3['confidence'] == 1)]


FL4 = phips_df[127871:141306]
FL4 = FL4[FL4['imagenum'] != 9999999.000000]
FL4[FL4 > 99998] = 0
FL4_conf3_chains_old = FL4.loc[(FL4['chainagg'] == 1) & (FL4['confidence'] == 3)]
FL4_conf2_chains_old = FL4.loc[(FL4['chainagg'] == 1) & (FL4['confidence'] == 2)]
FL4_conf2_chains = pd.concat([FL4_conf3_chains_old, FL4_conf2_chains_old])
FL4_conf1_chains = FL4.loc[(FL4['chainagg'] == 1) & (FL4['confidence'] == 1)]

#############################################################
#FL1
FL1_100_70 = FL1[0:510]
FL1_100_70 = FL1_100_70[FL1_100_70.confidence > 1.5]
FL1_100_70_sum = FL1_100_70['chainagg'].sum()

FL1_70_40 = FL1[510:1141]
FL1_70_40 = FL1_70_40[FL1_70_40.confidence > 1.5]
FL1_70_40_sum = FL1_70_40['chainagg'].sum()

FL1_40_10 = FL1[1141:]
FL1_40_10 = FL1_40_10[FL1_40_10.confidence > 1.5]
FL1_40_10_sum = FL1_40_10['chainagg'].sum()


# #FL2
FL2_70_40 = FL2[397:]
FL2_70_40 = FL2_70_40[FL2_70_40.confidence > 1.5]
FL2_70_40_sum = FL2_70_40['chainagg'].sum()

FL2_40_10 = FL2[0:397]
FL2_40_10 = FL2_40_10[FL2_40_10.confidence > 1.5]
FL2_40_10_sum = FL2_40_10['chainagg'].sum()


#FL3
FL3_100_70 = FL3[0:55]
FL3_100_70 = FL3_100_70[FL3_100_70.confidence > 1.5]
FL3_100_70_sum = FL3_100_70['chainagg'].sum()

FL3_70_40 = FL3[55:855]
FL3_70_40 = FL3_70_40[FL3_70_40.confidence > 1.5]
FL3_70_40_sum = FL3_70_40['chainagg'].sum()

FL3_40_10 = FL3[855:]
FL3_40_10 = FL3_40_10[FL3_40_10.confidence > 1.5]
FL3_40_10_sum = FL3_40_10['chainagg'].sum()

#FL4
FL4_100_70 = FL4[677:]
FL4_100_70 = FL4_100_70[FL4_100_70.confidence > 1.5]
FL4_100_70_sum = FL4_100_70['chainagg'].sum()

FL4_70_40 = FL4[0:677]
FL4_70_40 = FL4_70_40[FL4_70_40.confidence > 1.5]
FL4_70_40_sum = FL4_70_40['chainagg'].sum()


#END OF SCRIPT
