# ---------------------------------------------------------------------
## Movies_getMovieInfo.py
# H-RM Tan -- revised Oct 2016
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
## import modules
# ---------------------------------------------------------------------
# Python 2 & 3 Compatibility
from __future__ import print_function, division

# import matplotlib
# % matplotlib inline

import pandas as pd
import numpy as np
# import datetime as dt
# ​import matplotlib.pyplot as plt


from bs4 import BeautifulSoup
import requests
import re
import time
import sys

# ---------------------------------------------------------------------
## load moviecharts_list file
# ---------------------------------------------------------------------
mv_listDF=pd.read_csv('mv_chartListDF_2016_1980.csv')
mv_listDF.columns
# Index(['Unnamed: 0', 'mYrank', 'mID', 'mName', 'mStudio', 'totalDGross',
#        'totalDTheatre', 'openDGross', 'openDTheatre', 'openWkdate',
#        'closeWkdate'],
#       dtype='object')

DF=mv_listDF.drop(['Unnamed: 0'],axis=1)
# DF

# ---------------------------------------------------------------------
## Set up dictionary format and URLs for scraping
# ---------------------------------------------------------------------

mv_info = []
errorList = []

headers = ['mID', 'mName', 'mYrank',
           'mStudio', 'totalDGross',
           'totalDTheatre', 'openDGross', 'openDTheatre', 'openWkdate', 'closeWkdate',
           'F_gross', 'W_gross', 'PD_budget', 'Genre',
           'mv_runtime', 'DURrelease',
           'mv_Dir',
           # 'mv_Write',#'mv_Act', ## maybe also add Ratings
           'mv_Prod', 'mv_Comp',
           'OscarNom', 'OscarInfoURL']

bomjURL = 'http://www.boxofficemojo.com'
mvIDurl = '/movies/?id='
endURL = '.htm'

# ---------------------------------------------------------------------
## Scrap relevant info from individual boxofficemojo movie page
# ---------------------------------------------------------------------

for m in range(0, len(DF)):  # len(DF)#range(0,len(DF)):

    try:
        mvID = DF.mID[m]
        mvName = DF.mName[m]
        mjurl = bomjURL + mvIDurl + mvID + endURL
        print(m)
        # print(m, mjurl)

        pgResp = requests.get(mjurl)
        # pgResp = requests.get(url)
        # pgResp = requests.get('http://www.boxofficemojo.com/movies/?id=pixar2015.htm')
        # pgResp = requests.get('http://www.boxofficemojo.com/movies/?id=piecesofapril.htm')
        # pgResp = requests.get('http://www.boxofficemojo.com/movies/?id=starwars7.htm')

        if pgResp.status_code == 200:
            soup = BeautifulSoup(pgResp.text, 'lxml')

            ForgTMP = soup.find(text=re.compile('Foreign:'))  # .next.nextSibling.text.replace('\xa0','')
            if ForgTMP != None:
                ForGrossTMP = ForgTMP.next.nextSibling.text.replace('\xa0', '')
                if ForGrossTMP.upper() != 'N/A':
                    FGross = int(ForGrossTMP.replace('\xa0', '').replace('$', '').replace(',', ''))
                else:
                    FGross = np.nan
            else:
                FGross = np.nan

            WGrossTMP = soup.find(text=re.compile('Worldwide:'))  # .next.nextSibling.text.replace('\xa0','')
            if WGrossTMP != None:
                WorldGrossTMP = WGrossTMP.next.nextSibling.text.replace('\xa0', '')
                if WorldGrossTMP.upper() != 'N/A':
                    WGross = int(WorldGrossTMP.replace('\xa0', '').replace('$', '').replace(',', ''))
                else:
                    WGross = np.nan
            else:
                WGross = np.nan


            pdtBudgetTMP = soup.find(text=re.compile('Production Budget'))
            if pdtBudgetTMP != None:
                pdtBtmp = pdtBudgetTMP.nextSibling.text
                if pdtBtmp != 'N/A':
                    if pdtBtmp.find(' million') >= 0:
                        pdtBudget = int(pdtBtmp.split(' million')[0].replace('$', '').replace('.', '') + '0' * 6)
                    else:
                        pdtBudget = int(pdtBtmp.replace('$', '').replace(',', ''))
                else:
                    pdtBudget = np.nan
            else:
                pdtBudget = np.nan

            genreTMP = soup.find(text=re.compile('Genre: '))
            if genreTMP != None:
                genreTmp0 = genreTMP.nextSibling.text
                if genreTmp0 != 'N/A':
                    genre = genreTmp0
                else:
                    genre = np.nan
            else:
                genre = np.nan

            runtimeTMP0 = soup.find(text=re.compile('Runtime: '))
            if runtimeTMP0 != None:
                runtimeTMP = runtimeTMP0.nextSibling.text
                if runtimeTMP != 'N/A':
                    H, tmp1, Min, tmp2 = runtimeTMP.split()
                    runtime = (int(H) * 60) + int(Min)
                else:
                    runtime = np.nan
            else:
                runtime = np.nan

            RDurTMP = soup.find(text=re.compile('In Release:'))  # ||NoneType
            if RDurTMP != None:
                ReleaseDays = int(RDurTMP.next.next.text.split()[0].replace(',', ''))
            else:
                ReleaseDays = np.nan

                #
            dirTMP = soup.find(text=re.compile('Director:'))
            if dirTMP != None:
                director = dirTMP.next.text.split(' (co-director)')
            else:
                director = np.nan

                #         writeTMP = soup.find(text = re.compile('Writer'))
                #         if writeTMP !=None:
                #             wtmp000 = writeTMP.next.text.replace('J.J.','Jj').replace('McC','Mcc').replace('D\'S','Ds')
                #             wtmp00 = wtmp000.replace('C. Strouse','Strouse').replace('D. Brown','Brown').replace('Jean-Luc','Jeanluc')
                #             wtmp01 = wtmp00.replace('DuVall','Duvall').replace('Tim Blake','Timblake').replace('LaFauve','Lafauve')
                #             wtmp0 = wtmp01.replace('McQ','Mcq')
                #             writeTmp0 = re.findall('[A-Z][^A-Z]*', wtmp0)
                #             writer = [ writeTmp0[2*(n-1)]+writeTmp0[2*(n-1)+1] for n in range(1,round(len(writeTmp0)/2)+1) ]
                #         else:
                #             writer = np.nan


                #         actorsLtmp = soup.find(text = re.compile('Actor'))
                #         if actorsLtmp.next.text.find(' (Voice)')>0:
                #             actors = [n.split('*')[0] for n in actorsLtmp.next.text.replace(' ','').split('(Voice)')[:-1] ]
                #         #print(actorsNs)
                #         else:
                #             acttmp00 = actorsLtmp.next.text.replace(' ','').replace('TJ','Tj').replace('*(Cameo)','').replace('Common','')
                #             acttmp0 = acttmp00.replace('Smit-McPhee','Smitmcphee').replace('McC','Mcc').replace('K.W','Kw')
                #             acttmp = acttmp0.replace('L.J','Lj').replace('n-W','nw').replace('O\'C','Oc').replace('McG','Mcg')
                #             acttmp = acttmp.replace('MaryElizabethWinstead','MaryelizabethWinstead').replace('JackieEarle','Jackieearle')
                #             actors0 = re.findall('[A-Z][^A-Z]*', acttmp)
                #             searchJR = np.array([a.find('Jr.')+1 for a in actors0])
                #             if any(searchJR)!= False:
                #                 # searchJR.nonzero()
                #                 id = [i for i, x in enumerate(searchJR) if x][0]
                #                 actors0[id-1] = actors0[id-1]+'_Jr.'
                #                 actors0.pop(id)
                #                 #actors0
                #             else:
                #                 pass
                #             actors = [ actors0[2*(n-1)]+actors0[2*(n-1)+1] for n in range(1,round(len(actors0)/2)+1) ]
                #             #print(actorsNs)


            producerTMP = soup.find(text=re.compile('Producer:'))
            if producerTMP != None:
                prodTmp1 = producerTMP.next.find_all('a')
                producer = [p.text.replace('(executive)', '') for p in prodTmp1]
                # proTmp0 = re.findall('[A-Z][^A-Z]*',producerTMP.next.text.replace('J.J.','Jj'))
                # producer = [ proTmp0[2*(n-1)]+proTmp0[2*(n-1)+1] for n in range(1,round(len(proTmp0)/2)+1) ]
            else:
                producer = np.nan

            compTMP = soup.find(text=re.compile('Composer:'))  # .next.text #|| NoneType
            if compTMP != None:
                compTmp1 = compTMP.next.find_all('a')
                composer = [p.text.replace('(executive)', '') for p in compTmp1]
                # comptmp = re.findall('[A-Z][^A-Z]*', compTMP.next.text )
                # composer = [ comptmp[2*(n-1)]+comptmp[2*(n-1)+1] for n in range(1,round(len(comptmp)/2)+1) ]
            else:
                composer = np.nan

                #
            OawardTMP = soup.find(text=re.compile('Academy Awards®'))  # .next.next.find('a')['href']  #|| NoneType
            if OawardTMP != None:
                OawardNom = 1
                OinfoURL = OawardTMP.next.next.find('a')['href']
            else:
                OawardNom = 0
                OinfoURL = np.nan

            ## Combine details:
            mvInfo_dict = dict(zip(headers, [mvID, mvName, DF.mYrank[m],
                                             DF.mStudio[m], DF.totalDGross[m],
                                             DF.totalDTheatre[m], DF.openDGross[m], DF.openDTheatre[m],
                                             DF.openWkdate[m], DF.closeWkdate[m],
                                             FGross, WGross, pdtBudget, genre,
                                             runtime, ReleaseDays,
                                             director,
                                             # writer,#actors,
                                             producer, composer,
                                             OawardNom, OinfoURL]))
            ## append to dictionary
            mv_info.append(mvInfo_dict)

            ## add delay
            time.sleep(0.2)

    except:
        e = sys.exc_info()[0]
        errorList.append((m, mjurl, e))
        print(m, mjurl, e)
        # write_to_page( "<p>Error: %s</p>" % e )

errorListDF = pd.DataFrame(errorList, columns=['mvID', 'mvPgURL', 'ErrType'])
errorListDF.to_csv('mvInfo_1-14258_ERRORS_v4.csv') ## should be empty after debugging

mv_infoDF = pd.DataFrame(mv_info, columns=headers)
mv_infoDF.to_csv('mvInfo_1-14258_excludedError_v4.csv')
