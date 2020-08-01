# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 21:19:25 2020

@author: .3
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb

df = pd.read_csv('all_degrees_data.csv')
#df = df.astype(str)
# removing the "all" categories still in the data
df = df[df['cipcode'] != 99000]

dfMap = pd.read_csv('degree_family_mapping_complete.csv')
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

df['year2'] = [year_fix(x) for x in df['year'].values]


dfMap = dfMap[dfMap['cipName'].isna() == False]

dfMap['upName'] = [x.upper() for x in dfMap['cipName'].values]

famDict1 = dict(zip(dfMap['upName'].values, dfMap['my_cat1'].values))
famDict2 = dict(zip(dfMap['upName'].values, dfMap['my_cat2'].values))

df['fam1'] = [famDict1[x.upper()] for x in df['name'].values]
df['fam2'] = [famDict2[x.upper()] for x in df['name'].values]

dfBach = df[df['awlevel'] == 5]

dfPivotFam1 = pd.pivot_table(dfBach, values = 'CTOTALT', index=['year2'],
                             columns=['fam1'], aggfunc = np.sum)
dfPivotFam2 = pd.pivot_table(dfBach, values = 'CTOTALT', index=['year2'],
                             columns=['fam2'], aggfunc = np.sum)


fig = plt.figure(figsize=(14,8))

for col in dfPivotFam2:
    
    plt.scatter(dfPivotFam2.index, dfPivotFam2[col], label = col)
    
#plt.legend(ncol=3)
plt.legend(ncol=3,loc='lower center', bbox_to_anchor=(0.5, -0.4))
plt.savefig('first_scatter_out.png', dpi=300)
#plt.show()