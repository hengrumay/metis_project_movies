# ---------------------------------------------------------------------
## Movies_getBudget_matchMvNames_binGenreNStudio.py
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
#
# from bs4 import BeautifulSoup
# import requests
# import time
# import re

from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

from collections import Counter

# ---------------------------------------------------------------------
## get budgets info from the numbers website:
# ---------------------------------------------------------------------
tmp = pd.read_html('http://www.the-numbers.com/movie/budgets/all')
## tmp[0] # interleaved with rows of NaN
tmp0 = tmp[0].dropna().reset_index()
# tmp0

budgetPD = tmp0.iloc[:, 2:7]
budgetPD.columns = ['ReleaseDate', 'mvName', 'ProdBudget', 'DGross', 'WwGross']
# budgetPD

budgetPD['ReleaseDate'] = pd.to_datetime(budgetPD.ReleaseDate)
budgetPD['mvName'] = budgetPD.mvName.apply(lambda x: str(x))
budgetPD['ProdBudget'] = budgetPD.ProdBudget.apply(lambda x: int(x.replace('$', '').replace(',', '')))
budgetPD['DGross'] = budgetPD.DGross.apply(lambda x: int(x.replace('$', '').replace(',', '')))
budgetPD['WwGross'] = budgetPD.WwGross.apply(lambda x: int(x.replace('$', '').replace(',', '')))

# budgetPD.ReleaseDate[1].year
budgetPD.to_csv('mv_thenumbers_pdtbudgetInfo.csv')


# ---------------------------------------------------------------------
## define subset for data 1980--2016
# ---------------------------------------------------------------------

### define subset
budgetPD = pd.read_csv('mv_thenumbers_pdtbudgetInfo.csv')
# budgetPD

rDatesort = budgetPD.sort_values(by=['ReleaseDate'], ascending=False).reset_index()

rDatesort['releaseYR'] = rDatesort.ReleaseDate.apply(lambda x: x.year)
rDatesort['releaseMonth'] = rDatesort.ReleaseDate.apply(lambda x: x.month)

# rDatesort.iloc[23:4972]
budget2016sept1980jan = rDatesort.iloc[23:4972].reset_index()

budget2016sept1980jan.to_csv('mv_thenumbers_pdtbudget_2016sept1980jan.csv')




# ---------------------------------------------------------------------
## combine budget and mvInfo data by matching names
# ---------------------------------------------------------------------

budget2016sept1980jan0 = pd.read_csv('mv_thenumbers_pdtbudget_2016sept1980jan.csv')
budget2016sept1980jan = budget2016sept1980jan0.iloc[:, 3:]


mvInfotmp = pd.read_csv('mvInfo_1-14258_excludedError_v4.csv')
# mvInfotmp.columns
mvInfo = mvInfotmp.drop(['Unnamed: 0'], axis=1)
# mvInfo.mName.to_frame()
# mvInfo


# ---------------------------------------------------------------------
## Use Fuzzywuzzy to help with string matching
# https://pypi.python.org/pypi/fuzzywuzzy
# ---------------------------------------------------------------------

# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

# fuzz.token_set_ratio(mvInfo.mName[528], "Star Wars Ep. VII: The Force Awakens") # 100

mvbudgetNamesCheck = []

headers = ['budgetListIDX', 'budgetListName', 'bLnameLength',
           'MvName', 'mvNameLength',
           'maxFuzzRatioIDX', 'maxFuzzRatio',
           'maxFuzzSetRatioIDX', 'maxFuzzSetRatio',
           'budgetListMvReleaseYR', 'MvReleaseYR']

# for nb in budget2016sept1980jan.mvName[167:168]:
# for ni in range(167,169):

for ni in range(0, len(budget2016sept1980jan.mvName)):
    # for ni in range(0,100):
    print(ni)
    budgetList_Name = budget2016sept1980jan.mvName[ni]
    # print(ni, budgetList_Name)

    fuzzRatioList = []
    fuzzSetRatioList = []
    for nm in mvInfo.mName:
        fuzzSetRatioList.append(fuzz.token_set_ratio(budgetList_Name, nm))
        fuzzRatioList.append(fuzz.ratio(budgetList_Name, nm))

    maxFuzzRatioIDX, maxFuzzRatio = np.array(fuzzRatioList).argmax(), np.array(fuzzRatioList).max()
    maxFuzzSetRatioIDX, maxFuzzSetRatio = np.array(fuzzSetRatioList).argmax(), np.array(fuzzSetRatioList).max()

    mvInfo_Name = mvInfo.mName[maxFuzzSetRatioIDX]  # as a potential diff name
    mvInfo_mvReleaseYr = pd.to_datetime(mvInfo.openWkdate[maxFuzzSetRatioIDX]).year

    budgetList_mvReleaseYr = pd.to_datetime(budget2016sept1980jan.ReleaseDate[ni]).year
    # budgetList_idx = ni

    # print(ni, budgetList_Name,)

    mvNamesCheck_dict = dict(zip(headers, [ni, budgetList_Name, len(budgetList_Name),
                                           mvInfo_Name, len(mvInfo_Name),
                                           maxFuzzRatioIDX, maxFuzzRatio,
                                           maxFuzzSetRatioIDX, maxFuzzSetRatio,
                                           budgetList_mvReleaseYr, mvInfo_mvReleaseYr]))

    mvbudgetNamesCheck.append(mvNamesCheck_dict)

    # print(mvNamesCheck_dict)
    # break

mvNamesCheck = pd.DataFrame(mvbudgetNamesCheck, columns=headers)
mvNamesCheck.to_csv('mvInfo_FuzzyWuzzy_mvNamesCheck_v2.csv')





# ---------------------------------------------------------------------
## Select combined list with same YR releases then
## use fuzzRatio and fuzzSetRatio to determine movie names (exact/non-exact) matches
# ---------------------------------------------------------------------

mvNamesCheck = pd.read_csv('mvInfo_FuzzyWuzzy_mvNamesCheck_v2.csv')
# mvNamesCheck.columns


Index(['Unnamed: 0', 'budgetListIDX', 'budgetListName', 'bLnameLength',
       'MvName', 'mvNameLength', 'maxFuzzRatioIDX', 'maxFuzzRatio',
       'maxFuzzSetRatioIDX', 'maxFuzzSetRatio', 'budgetListMvReleaseYR',
       'MvReleaseYR'],
      dtype='object')

nameCheck = mvNamesCheck.drop(['Unnamed: 0'], axis=1)
# len(nameCheck) #4949

## Use YR bool and then check IDX
sameYRbool = nameCheck.budgetListMvReleaseYR == nameCheck.MvReleaseYR
# sum((nameCheck.budgetListMvReleaseYR == nameCheck.MvReleaseYR).astype(int)) # 3144

nameCheckYR = nameCheck[sameYRbool].reset_index()

nameCheckYRFuzzRatio = nameCheckYR[nameCheckYR.maxFuzzRatio >= 80].reset_index()
# len(nameCheckYRFuzzRatio) # 3034

nameCheckYRFuzzRatioFuzzSetRatio = nameCheckYRFuzzRatio[nameCheckYRFuzzRatio.maxFuzzSetRatio >= 90]
maxIDXmatch = nameCheckYRFuzzRatioFuzzSetRatio.maxFuzzRatioIDX == nameCheckYRFuzzRatioFuzzSetRatio.maxFuzzSetRatioIDX

IDXmatchMVs = nameCheckYRFuzzRatioFuzzSetRatio[maxIDXmatch.astype(int) == 1]
# IDXmatchMVs
# len(IDXmatchMVs)

nonIDXmatchMVs = nameCheckYRFuzzRatioFuzzSetRatio[maxIDXmatch.astype(int) == 0]
# len(nonIDXmatchMVs) # 92



# ---------------------------------------------------------------------
## run check those non-matched movie names for maxID and Release Date match
# ---------------------------------------------------------------------


mvInfoIDX = []

for n in range(0, len(nonIDXmatchMVs)):
    # print (nonIDXmatch.iloc[n])

    bIDX = nonIDXmatchMVs.iloc[n].budgetListIDX
    FratioIDX = nonIDXmatchMVs.iloc[n].maxFuzzRatioIDX
    FSratioIDX = nonIDXmatchMVs.iloc[n].maxFuzzSetRatioIDX

    # budget2016sept1980jan.iloc[281].releaseYR
    if mvInfo.iloc[FSratioIDX].openWkdate == budget2016sept1980jan.iloc[bIDX].ReleaseDate:
        mvInfoIDX.append(FSratioIDX)
    elif mvInfo.iloc[FratioIDX].openWkdate == budget2016sept1980jan.iloc[bIDX].ReleaseDate:
        mvInfoIDX.append(FratioIDX)

    else:
        if pd.to_datetime(mvInfo.iloc[FSratioIDX].openWkdate).year == pd.to_datetime(
                budget2016sept1980jan.iloc[bIDX].ReleaseDate).year:
            mvInfoIDX.append(FSratioIDX)
        elif pd.to_datetime(mvInfo.iloc[FratioIDX].openWkdate).year == pd.to_datetime(
                budget2016sept1980jan.iloc[bIDX].ReleaseDate).year:
            mvInfoIDX.append(FratioIDX)


# len(mvInfoIDX) # 92
# mvInfoIDX

nonIDXmatchMVs['mvInfoIDX'] = mvInfoIDX
nonIDXmatchMVs.iloc[:, 2:].reset_index()

CombineIDXmatch = pd.concat([IDXmatchMVs.iloc[:, 2:].reset_index(), nonIDXmatchMVs.iloc[:, 2:].reset_index()], axis=0)

CombineIDXmatch1 = CombineIDXmatch.sort_values(by=['budgetListIDX']).reset_index().iloc[:, 2:]
# CombineIDXmatch1


# ---------------------------------------------------------------------
## Create subset of data with matched movie names indices
# ---------------------------------------------------------------------

budget2016sept1980jan_subset = budget2016sept1980jan.iloc[CombineIDXmatch1.budgetListIDX, :].reset_index()
# len(budget2016sept1980jan_subset)
# budget2016sept1980jan_subset

budget2016sept1980jan_subset1 = budget2016sept1980jan_subset.iloc[:, 1:].reset_index()
# budget2016sept1980jan_subset1.head(8)



# ---------------------------------------------------------------------
## Account for Inflation:
# http://www.usinflationcalculator.com/
# http://inflationdata.com/Inflation/Inflation_Calculators/Inflation_Rate_Calculator.asp
# ---------------------------------------------------------------------

yr = [1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998,
      1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]

inflrateWRT2016 = [2.92, 2.65, 2.50, 2.42, 2.32, 2.24, 2.20, 2.12, 2.04, 1.94, 1.84, 1.77, 1.72, 1.67, 1.63, 1.58, 1.54,
                   1.50, 1.48,
                   1.45, 1.40, 1.36, 1.34, 1.31, 1.28, 1.23, 1.19, 1.16, 1.12, 1.12, 1.10, 1.07, 1.05, 1.03, 1.02, 1.02,
                   1]

yr = yr[::-1]
inflrateWRT2016 = inflrateWRT2016[::-1]

inflrateDict = dict(zip(yr, inflrateWRT2016))

inflrateTmp = np.zeros((len(budget2016sept1980jan_subset1), 1))

for y in yr:
    # print(y)
    yrIDX = budget2016sept1980jan_subset1[budget2016sept1980jan_subset1['releaseYR'] == y].index.tolist()
    inflrateTmp[yrIDX] = inflrateDict[y]  # *len(yrIDX))

inflrateCol = pd.DataFrame(inflrateTmp)


# ---------------------------------------------------------------------
## Adjust Budget/Gross info for inflation
# ---------------------------------------------------------------------

budget2016sept1980jan_subset1['inflrateWRT2016'] = inflrateCol

budget2016sept1980jan_subset1['ProdBudgetCorr'] = budget2016sept1980jan_subset1.ProdBudget * budget2016sept1980jan_subset1.inflrateWRT2016
budget2016sept1980jan_subset1['DGrossCorr'] = budget2016sept1980jan_subset1.DGross * budget2016sept1980jan_subset1.inflrateWRT2016
budget2016sept1980jan_subset1['WwGrossCorr'] = budget2016sept1980jan_subset1.WwGross * budget2016sept1980jan_subset1.inflrateWRT2016

budget2016sept1980jan_subset1.to_csv('mv_thenumbers_pdtbudget_CPICorr_2016sept1980jan')





# ---------------------------------------------------------------------
## Update Inflation Adjusted Financial info in mvInfo -- save as new DataFrame
# ---------------------------------------------------------------------

# mvInfotmp = pd.read_csv('mvInfo_1-14258_excludedError_v4.csv')
# mvInfo = mvInfotmp.drop(['Unnamed: 0'], axis=1)
# mvInfo
mvInfo_subset = mvInfo.iloc[CombineIDXmatch1.mvInfoIDX].reset_index()

# len(mvInfo_subset)
# mvInfo_subset

mvInfo_subset2 = mvInfo_subset[['index', 'mID', 'mName', 'mYrank', 'mStudio',
                                'openWkdate', 'DURrelease', 'openDTheatre', 'openDGross',
                                'totalDTheatre', 'PD_budget', 'totalDGross', 'W_gross', 'F_gross',
                                'Genre', 'mv_runtime',
                                'mv_Dir', 'mv_Prod', 'mv_Comp',
                                'OscarNom', 'OscarInfoURL']].reset_index()

mvInfo_subset2 = mvInfo_subset2.iloc[:, 2:]
# mvInfo_subset2

mvInfo_subset2['PD_budget'] = budget2016sept1980jan_subset1.ProdBudgetCorr
mvInfo_subset2['totalDGross'] = budget2016sept1980jan_subset1.DGrossCorr
mvInfo_subset2['W_gross'] = budget2016sept1980jan_subset1.WwGrossCorr

mvInfo_subset2['F_gross'] = mvInfo_subset2.W_gross - mvInfo_subset2.totalDGross
mvInfo_subset2['openDGross'] = mvInfo_subset2.openDGross * budget2016sept1980jan_subset1.inflrateWRT2016


mvInfo_subset2.to_csv('mvInfo_subset_MatchIDX_withPDbudget_CPICorr.csv')

# sum(mvInfo_subset2.OscarNom) / len(mvInfo_subset2)




# ---------------------------------------------------------------------
## Bin Genres as dummy vars -- save as separate DataFrame for combining
#  ---------------------------------------------------------------------

# from collections import Counter

Counter(mvInfo_subset2.Genre).most_common()

import re

GenreList = ['Animation', 'Adventure', 'Action', 'Comedy', 'Drama', 'Documentary', 'Family', 'Fantasy', 'Foreign',
             'Horror', 'Period', 'Sci-Fi', 'Thriller', 'Western', 'Romantic', 'Romance']

ALLgenreList = []
​
for mi in range(0, len(mvInfo_subset2.Genre)):
    if pd.notnull(mvInfo_subset2['Genre'][mi]):
        genreDict = {}
        for g in GenreList:
            bool = g in mvInfo_subset2.Genre[mi]  # 'Romantic Comedy'#'Sci-Fi / Fantasy'
            genreDict[g] = int(bool)
            # print(g, int(bool))
    else:
        print(g, mvInfo_subset2.Genre[mi], mi)
        genreDict = {}
        for g in GenreList:
            # bool = g in mvInfo_subset2.Genre[mi] #'Romantic Comedy'#'Sci-Fi / Fantasy'
            genreDict[g] = np.nan
    # print(genreDict)
    ALLgenreList.append(genreDict)

# pd.notnull(mvInfo_subset2['Genre'][0])
# bool, g, mvInfo_subset2.Genre[mi], mi
# len(ALLgenreList)

genreDF = pd.DataFrame(ALLgenreList, columns=GenreList)
genreDF['Romance'] = genreDF.Romance + genreDF.Romantic
genreDF2 = genreDF.drop(['Romantic'], axis=1)

pd.np.sum(genreDF2['Romance'])

genreDF3 = pd.concat([mvInfo_subset2.Genre.to_frame(), genreDF2], axis=1)
# genreDF3
genreDF3.to_csv('mvInfo_subset_MatchIDX_genres.csv')




# ---------------------------------------------------------------------
## Bin Studios as dummy vars -- save as separate DataFrame for combining
# ---------------------------------------------------------------------

# from collections import Counter

​Counter(mvInfo_subset2.mStudio).most_common(20)

studioList = ['warnerbros', 'universal', 'fox', 'buenavista', 'sony', 'paramount', 'miramax', 'newline',
              'foxsearchlight', 'sonyclassics', 'lionsgate', 'mgm', 'screengems', 'weinsteincompany',
              'focus', 'magnolia', 'ifc', 'wb-newline', 'lions_gate', 'dreamworks']

ALLstudioList = []
​
for mi in range(0, len(mvInfo_subset2.mStudio)):
    if pd.notnull(mvInfo_subset2['mStudio'][mi]):
        studioDict = {}
        for g in studioList:
            bool = g in mvInfo_subset2.mStudio[mi]  # 'Romantic Comedy'#'Sci-Fi / Fantasy'
            studioDict[g] = int(bool)
            # print(g, int(bool))
    else:
        print(g, mvInfo_subset2.mStudio[mi], mi)
        studioDict = {}
        for g in studioList:
            # bool = g in mvInfo_subset2.Genre[mi] #'Romantic Comedy'#'Sci-Fi / Fantasy'
            studioDict[g] = np.nan
    # print()
    ALLstudioList.append(studioDict)

studioDF = pd.DataFrame(ALLstudioList, columns=studioList)
# studioDF

studioDF2 = pd.concat([mvInfo_subset2.mStudio.to_frame(), studioDF], axis=1)

studioDF2.to_csv('mvInfo_subset_MatchIDX_studio.csv')



