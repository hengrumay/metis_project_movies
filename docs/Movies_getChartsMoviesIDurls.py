# ---------------------------------------------------------------------
## Movies_getChartsMoviesIDurls.py
# H-RM Tan -- revised Oct 2016
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
## load modules
# ---------------------------------------------------------------------

# Python 2 & 3 Compatibility
from __future__ import print_function, division

import pandas as pd
import numpy as np
import datetime as dt

from bs4 import BeautifulSoup
import requests
# import time

# ---------------------------------------------------------------------
mvYRlist = [str(i) for i in range(2016, 1979, -1)]
# len(mvYRlist)

## URL Formatting for each chart page:
# http://www.boxofficemojo.com/yearly/chart/?yr=2016&p=.htm
# http://www.boxofficemojo.com/yearly/chart/?yr=####&p=.htm
# http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=2016&p=.htm

# ---------------------------------------------------------------------
## set up URL for scraping...
# ---------------------------------------------------------------------

bomjURL = 'http://www.boxofficemojo.com'
YRpg1viewerURL = '/yearly/chart/?page=1&view=releasedate&view2=domestic&yr='
YRpg1endURL = '&p=.htm'
YRpg1URLlist = [(bomjURL + YRpg1viewerURL + year + YRpg1endURL) for year in mvYRlist]

# len(YRpg1URLlist)
# YRpg1URLlist

# ---------------------------------------------------------------------
## Collect List for PGheaders = ['pgURL', 'startPg', 'endPg']
# ---------------------------------------------------------------------
pgList = []
YstartendPages = []

for y in range(0, len(YRpg1URLlist)):
    url = YRpg1URLlist[y]
    # print(url)

    # Each chart 1st page has 100 listing
    YstartendPages.append([mvYRlist[y], 1, 100])

    pgList.append(url)

    PG1resp = requests.get(url)
    if PG1resp.status_code == 200:
        PG1soup = BeautifulSoup(PG1resp.text, 'lxml')

    pg1_tmp = PG1soup.find_all('center')[0].find_all('a')

    #     pgList = [ (bomjURL+p['href'])
    for p in pg1_tmp:
        pgURLs = (bomjURL + p['href'])
        # print(pgURLs)

        pg_rangeSTR = p.text.replace('#', '').replace('\x96', '')
        pgS, pgE = (int(pg_rangeSTR[0:3]), int(pg_rangeSTR[3:7]))
        # print(pgS, pgE)
        YstartendPages.append((mvYRlist[y], pgS, pgE))

        pgList.append(pgURLs)
        # break

# CHECK
# mvYRlist, YstartendPages


# ---------------------------------------------------------------------
## Scrap table data from list of urls with start and end pg rowNos (esp last page of list per year)
# ---------------------------------------------------------------------
mv_list = []

headers = ['mYrank', 'mID', 'mName', 'mStudio',
           'totalDGross', 'totalDTheatre', 'openDGross', 'openDTheatre', 'openWkdate', 'closeWkdate']

mvCnt = 0

for y in range(0, len(YstartendPages)):

    Year, pgSn, pgEn = YstartendPages[y]
    if (Year, pgSn, pgEn) == ('2016', 501, 530):
        pgSn = 502
    else:
        pass

    mvChartNrows = pgEn - pgSn + 1
    mvCnt += mvChartNrows

    print('Retrieving ' + str(mvChartNrows) + 'rows from: ' + pgList[y])
    pgResp = requests.get(pgList[y])
    
    if pgResp.status_code == 200:
        chartpgSoup = BeautifulSoup(pgResp.text, 'lxml')
        
    if int(Year) <= 2001:
        tableInfo = chartpgSoup.find_all('table')[3].find_all('font')[
                    13:(mvChartNrows * 8) + 13]  ## 8 lines for each table columns *N# mvrows on pg

    else:
        tableInfo = chartpgSoup.find_all('table')[3].find_all('font')[
                    14:(mvChartNrows * 9) + 14]  ## 9 lines for each table columns *N# mvrows on pg

    for i in range(1, mvChartNrows + 1):
        if int(Year) <= 2001:
            mvinfo = tableInfo[8 * (i - 1):8 * i]
        else:
            mvinfo = tableInfo[9 * (i - 1):9 * i]

        mvYRrank = mvinfo[0].text

        ## Movie ID -- to use for scraping individual movie info. later
        if mvinfo[1].find('a') is None:
            mvID = mvinfo[1].text
        else:
            mvID = mvinfo[1].find('a')['href'][12:-4]

        mvName = mvinfo[1].text

        pdtStudio = mvinfo[2].find('a')['href'][22:-4]

        totDGross = int(mvinfo[3].text.replace('$', '').replace(',', ''))

        if mvinfo[4].text != 'N/A':
            totDTheatre = int(mvinfo[4].text.replace(',', ''))
        else:
            totDTheatre = np.nan

        if mvinfo[5].text != 'N/A':
            oDGross = int(mvinfo[5].text.replace('$', '').replace(',', ''))
        else:
            oDGross = np.nan

        if mvinfo[6].text != 'N/A':
            oDTheatre = int(mvinfo[6].text.replace(',', ''))
        else:
            oDTheatre = np.nan

        if mvinfo[7].text != '-' and mvinfo[7].text != 'Jan':
            oWkmd = dt.datetime.strptime((Year + '/' + mvinfo[7].text), '%Y/%m/%d')
            # dt.datetime.strptime(Year + '/' + mvinfo[7].find('a').text,'%m/%d')
        else:
            oWkmd = np.nan

        if int(Year) > 2001:
            if mvinfo[8].text != '-' and mvinfo[8].text != '2/29' and mvinfo[8].text != '2':
                cWkmd = dt.datetime.strptime((Year + '/' + mvinfo[8].text), '%Y/%m/%d')
            else:
                cWkmd = np.nan
        else:
            cWkmd = np.nan

        movie_dict = dict(zip(headers, [mvYRrank, mvID, mvName, pdtStudio,
                                        totDGross, totDTheatre,
                                        oDGross, oDTheatre,
                                        oWkmd, cWkmd]))
        mv_list.append(movie_dict)

        # time.sleep(2)

mv_listDF = pd.DataFrame(mv_list, columns=headers)
mv_listDF.to_csv('mv_chartListDF_2016_1980.csv')

# mv_listDF=pd.read_csv('mv_chartListDF_2016_1980.csv')
