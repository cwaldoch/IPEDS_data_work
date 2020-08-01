# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 09:55:43 2020

@author: .3
"""

import pandas as pd
from zipfile import ZipFile
from os import walk

dataLoc = r'C:\Users\.3\Desktop\degrees_data\data\\'
outputLoc = r'C:\Users\.3\Desktop\degrees_data\data_out\\'




def file_walk(directory):
    file_name_list = []
    for (dirpath, dirnames, filenames) in walk(directory):
        file_name_list.extend(filenames)
        break
    return(file_name_list)
    
zipFiles = file_walk(dataLoc)


dfStorage = []
dfDict = {}

for zipF in zipFiles:
    currentZip = ZipFile(dataLoc+zipF)
    zipList = currentZip.filelist
    #print(len(zipList))
    for zippedF in zipList:
        if len(zipList) == 2:
            if 'rv' in zippedF.filename:
                dfInt = pd.read_csv(currentZip.open(zippedF))
                dfInt['year'] = [zippedF.filename[3:5]]*len(dfInt)
                dfStorage.append(dfInt)
                dfDict[zippedF.filename[3:5]] = dfInt
                print(zippedF.filename)
                print(len(dfInt.columns))
                
        else:
            dfInt = pd.read_csv(currentZip.open(zippedF))
            dfInt['year'] = [zippedF.filename[3:5]]*len(dfInt)
            dfStorage.append(dfInt)
            dfDict[zippedF.filename[3:5]] = dfInt
            print(zippedF.filename)
            print(len(dfInt.columns))
        
        
#z = dfDict['99']
        
col6 = ['80','84','85','86','87','88','89','91','92','93','94', '90']
col65 = ['11','12', '13', '14', '15', '16', '17', '18', '19']
col53 = ['99', '02','03','04','05','06','07',]
col39 = ['95', '96', '97', '98', '00', '01', ]
col125 = ['08', '09', '10']

colCounts = [col6, col65, col53, col39, col125]

dfDict2 = {}

for colCt in colCounts:
    dfColCts = []
    for year in colCt:
        dfYear = dfDict[year]
        dfColCts.append(dfYear)
        
    dfColAll = pd.concat(dfColCts, ignore_index=True)
    
    dfColAll.to_csv(outputLoc+colCt[0]+'_start.csv', index=False)
    dfDict2[colCt[0]] = dfColAll
# FIND THE CATEGORIES WITH WAY TOO HIGH NUMBERS, 100636 is one
    # FIGURED IT OUT, just remove 100636 and 372213
df6 = pd.read_csv(outputLoc+'80_start.csv')
df6z = df6[df6['unitid'] != 100636]
df6x = df6z[df6z['unitid'] != 372213]
df6G = df6x.groupby(['cipcode', 'awlevel', 'year']).sum()
dfIdx = df6G.index

df6G['CTOTALT'] = df6G['crace15'] +df6G['crace16']
df6G = df6G[['CTOTALT']]
df6G['cipcode'] = [x[0] for x in dfIdx]
df6G['awlevel'] = [x[1] for x in dfIdx]
df6G['year'] = [x[2] for x in dfIdx]

#keepCols = ['unitid', 'cipcode', 'awlevel', 'year']
#totalDegrees = 'crace15' + 'crace16'
#print(df6.columns)
#
df65 = pd.read_csv(outputLoc+'11_start.csv')

df65z = df65[df65['UNITID'] != 100636]
df65x = df65z[df65z['UNITID'] != 372213]

df65G = df65x.groupby(['CIPCODE', 'AWLEVEL', 'year']).sum()
dfIdx = df65G.index

df65G = df65G[['CTOTALT']]
df65G['cipcode'] = [x[0] for x in dfIdx]
df65G['awlevel'] = [x[1] for x in dfIdx]
df65G['year'] = [x[2] for x in dfIdx]

df53 = pd.read_csv(outputLoc+'99_start.csv')
df53z = df53[df53['unitid'] != 100636]
df53x = df53z[df53z['unitid'] != 372213]
df53G = df53x.groupby(['cipcode', 'awlevel', 'year']).sum()
dfIdx = df53G.index

df53G['CTOTALT'] = df53G['crace15'] +df53G['crace16']
df53G = df53G[['CTOTALT']]
df53G['cipcode'] = [x[0] for x in dfIdx]
df53G['awlevel'] = [x[1] for x in dfIdx]
df53G['year'] = [x[2] for x in dfIdx]

df39 = pd.read_csv(outputLoc+'95_start.csv')
df39z = df39[df39['unitid'] != 100636]
df39x = df39z[df39z['unitid'] != 372213]
df39G = df39x.groupby(['cipcode', 'awlevel', 'year']).sum()
dfIdx = df39G.index

df39G['CTOTALT'] = df39G['crace15'] +df39G['crace16']
df39G = df39G[['CTOTALT']]

df39G['cipcode'] = [x[0] for x in dfIdx]
df39G['awlevel'] = [x[1] for x in dfIdx]
df39G['year'] = [x[2] for x in dfIdx]

df125 = pd.read_csv(outputLoc+'08_start.csv')
df125z = df125[df125['UNITID'] != 100636]
df125x = df125z[df125z['UNITID'] != 372213]
df125G = df125x.groupby(['CIPCODE', 'AWLEVEL', 'year']).sum()
dfIdx = df125G.index

df125G['CTOTALT'] = df125G['CTOTALM'] +df125G['CTOTALW']
df125G = df125G[['CTOTALT']]

df125G['cipcode'] = [x[0] for x in dfIdx]
df125G['awlevel'] = [x[1] for x in dfIdx]
df125G['year'] = [x[2] for x in dfIdx]

dfsAll = [df6G, df65G, df53G, df39G, df125G]

dfComplete = pd.concat(dfsAll, ignore_index = True)

dfComplete.to_csv(outputLoc+r'\\IPEDS_data_work\all_degrees_data.csv', index=False)
