# ---------------------------------------------------------------------
## Movies_combineData.py
# H-RM Tan -- revised Oct 2016
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
## import modules
# ---------------------------------------------------------------------

from __future__ import print_function, division

# import matplotlib
# % matplotlib inline

import pandas as pd
import numpy as np
# import datetime as dt
# import datetime


# ---------------------------------------------------------------------
## load & Combine movie -  genre + studio dataset
# ---------------------------------------------------------------------

# genreInfo
genreInfo = pd.read_csv('mvInfo_subset_MatchIDX_genres.csv')

# studioInfo
studioInfo = pd.read_csv('mvInfo_subset_MatchIDX_studio.csv')
# studioInfo.iloc[:,2:]

tmpDF = pd.read_csv('mvInfo_subset_MatchIDX_withPDbudget_CPICorr.csv')
# tmpDF.columns
# Index(['Unnamed: 0', 'mID', 'mName', 'mYrank', 'mStudio', 'openWkdate',
#        'DURrelease', 'openDTheatre', 'openDGross', 'totalDTheatre',
#        'PD_budget', 'totalDGross', 'W_gross', 'F_gross', 'Genre', 'mv_runtime',
#        'mv_Dir', 'mv_Prod', 'mv_Comp', 'OscarNom', 'OscarInfoURL'],
#       dtype='object')

tmpDF2 = tmpDF.drop('Unnamed: 0',axis=1)#.reset_index()

combiDF = pd.concat([tmpDF2,genreInfo.iloc[:,2:],studioInfo.iloc[:,2:]], axis=1)
# combiDF#.duplicated()#.dropna()


# ---------------------------------------------------------------------
## Select non-extreme values...
# ---------------------------------------------------------------------
# combiDF.PD_budget.sort_values(ascending=True).head(2800).plot.box()
# combiDF.PD_budget.sort_values(ascending=True).head(2800).describe()

idxOI = combiDF[combiDF['PD_budget'] <=400000000].index.tolist()
# len(idxOI)/len(tmpDF)
# 0.8175206611570248

combiDF2 = combiDF.loc[idxOI,:].reset_index()#.describe()
# combiDF.loc[idxOI,:].reset_index()
# combiDF2


# ---------------------------------------------------------------------
## Make Rows fattened and without zeros
# ---------------------------------------------------------------------

combiDF2i = combiDF2[combiDF2.totalDGross!=0]

combiDF2ii = combiDF2i[combiDF2i.W_gross!=0]

combiDF2ii.W_gross.describe()
combiDF2ii['F_gross'] = combiDF2ii.F_gross.replace(0,1)

# ---------------------------------------------------------------------
## calculated ROI and ln(ROI)
# ---------------------------------------------------------------------
# plt.hist(np.log(combiDF2ii.F_gross))

combiDF2ii['D_RtnOInvest'] = combiDF2ii.totalDGross / combiDF2ii.PD_budget

combiDF2ii['W_RtnOInvest'] = combiDF2ii.W_gross / combiDF2ii.PD_budget

combiDF2ii['logD_RtnOInvest'] = np.log(combiDF2ii['D_RtnOInvest'] )

combiDF2ii['logW_RtnOInvest'] = np.log(combiDF2ii['W_RtnOInvest'] )

combiDF2ii.logD_RtnOInvest.plot.hist() #(100)

combiDF2ii.logW_RtnOInvest.plot.hist()

plt.hist((combiDF2ii.logW_RtnOInvest - combiDF2ii.logD_RtnOInvest))


# ---------------------------------------------------------------------
##logging on fo less.
# ---------------------------------------------------------------------
# combiDF2ii.logW_RtnOInvest.plot.hist()

combiDF2ii['logDURrelease'] = np.log(combiDF2ii.DURrelease)
combiDF2ii['logOpenDGross'] = np.log(combiDF2ii.openDGross)
combiDF2ii['logTotalDGross'] = np.log(combiDF2ii.totalDGross)

combiDF2ii['openWkdate'] = pd.to_datetime(combiDF2ii.openWkdate)

combiDF2ii['openYR'] = combiDF2ii.openWkdate.apply(lambda x: x.year)
combiDF2ii['openWK'] = combiDF2ii.openWkdate.apply(lambda x: x.week)
combiDF2ii['openDay'] = combiDF2ii.openWkdate.apply(lambda x: x.day)
combiDF2ii['openWkday'] = combiDF2ii.openWkdate.apply(lambda x: x.weekday())

combiDF2a = combiDF2ii #.drop(['Unnamed: 0'],axis=1)
# combiDF2a


# ---------------------------------------------------------------------
## FILL MISSING Values
# ---------------------------------------------------------------------
# combiDF2a.DURrelease.plot.hist()
# combiDF2a.logDURrelease.plot.hist()
combiDF2a['DURrelease'] = combiDF2a.DURrelease.fillna(combiDF2a.DURrelease.median()) #.DURrelease.median()
combiDF2a['logDURrelease'] = combiDF2a.logDURrelease.fillna(combiDF2a.logDURrelease.median()) #.DURrelease.median()


combiDF2b = combiDF2a.drop('index', axis=1)

# ---------------------------------------------------------------------
## Save dataframe as subset
# ---------------------------------------------------------------------
## SAVING "cleaned" Data
combiDF2b.to_csv('mvInfo_subset_MatchIDX_COMBINEDcleaned')

