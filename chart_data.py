# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 21:19:25 2020

@author: .3
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
import random
import matplotlib

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource

df = pd.read_csv(r"C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\all_degrees_data.csv")
#df = df.astype(str)
# removing the "all" categories still in the data
df = df[df['CIPCODE'] != 99000]

dfColors = pd.read_csv(r"C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\big_color_list2.csv")

dfMap = pd.read_csv(r"C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\degree_family_mapping_complete.csv")
#dfMap = dfMap.astype(str)

def year_fix(year):
    #pdb.set_trace()ye
    if year <10:
        year = int('200'+str(year))
    elif year <80:
        year = int('20'+str(year))
    else:
        year = int('19'+str(year))
        
    return(year)

df['year2'] = [year_fix(x) for x in df['YEAR'].values]


dfMap = dfMap[dfMap['cipName'].isna() == False]

dfMap['upName'] = [x.upper() for x in dfMap['cipName'].values]

famDict1 = dict(zip(dfMap['upName'].values, dfMap['my_cat1'].values))
famDict2 = dict(zip(dfMap['upName'].values, dfMap['my_cat2'].values))

df['fam1'] = [famDict1[x.upper()] for x in df['name'].values]
df['fam2'] = [famDict2[x.upper()] for x in df['name'].values]

df = df[df['name'] != 'Grand total']

dfBach = df[df['AWLEVEL'] == 5]

dfBach.to_csv(r'C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\bachelors_degrees.csv', index=False)

dfBach = dfBach[~dfBach['fam2'].isin(['Military', 'Misc. Certifications',
                'Multi-disciplinary', 'Other Services'])]

yearTotals = pd.pivot_table(dfBach, values = 'CTOTALT', index=['year2'],
                            aggfunc = np.sum)

dfPivotFam4 = pd.pivot_table(dfBach, values = 'CTOTALT', index=['fam2'],
                             aggfunc = np.sum)
dfSort = dfPivotFam4.sort_values('CTOTALT', ascending=False)

topTen = list(dfSort.iloc[:12].index)

dfTT = dfBach[dfBach['fam2'].isin(topTen)]

dfPivotFam3 = pd.pivot_table(dfTT, values = 'CTOTALT', index=['year2'],
                             columns=['fam2'], aggfunc = np.sum)
#dfPivotFam2 = pd.pivot_table(dfBach, values = 'CTOTALT', index=['year2'],
#                             columns=['fam2'], aggfunc = np.sum)
#dfPivotFam3 = pd.pivot_table(dfBach, values = 'CTOTALT', index=['year2'],
#                             columns=['name'], aggfunc = np.sum)


fig = plt.figure(figsize=(14,8))
i = 0
usedColorDict = {}
for col in dfPivotFam3:
#    if np.average(dfPivotFam2[col]) >1000:
    plt.scatter(dfPivotFam3.index, dfPivotFam3[col], label = col,
                color = dfColors.iloc[i,0])
    usedColorDict[col] = dfColors.iloc[i,0]
    i += 4
matplotlib.rcParams['font.weight']= 'bold'

#plt.legend(ncol=3)
plt.legend(ncol=3,loc='lower center', bbox_to_anchor=(0.5, -0.18))
plt.tight_layout()
plt.grid()
plt.savefig('fam2_12_scatter.png', dpi=300)
#plt.show()

#dfPivotFam3 = dfPivotFam3.fillna(0)
#
#output_file('all_names.html')
#colDict = {}
#colDict['x'] = list(dfPivotFam3.index)
#
#
#for col in dfPivotFam3.columns:
#    #print(col)
#    colDict[col]= list(dfPivotFam3[col].values)
#	
#
#
#source = ColumnDataSource(data = colDict)
#TOOLTIPS = []
#
#for col in dfPivotFam3.columns:
#	TOOLTIPS.append((col, '@'+col))
#
##colors = colors[:len(dfPivotFam3.columns)]
#
#p = figure(plot_width=1400, plot_height=800, tooltips=TOOLTIPS)
#
#for col in dfPivotFam3.columns:
#    p.circle(x = 'x', y = col, color=usedColorDict[col],
#             source=source)
#p.legend.location = 'top_left'
#p.legend.orientation = 'vertical'
#
#show(p)