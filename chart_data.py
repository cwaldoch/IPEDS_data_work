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

dfMap = pd.read_csv('collated_data_dict.csv')
#dfMap = dfMap.astype(str)

"""
oh god, the underlying data has a bunch of nines, it's unrounded, need to think
about a solution to this, not sure how easy it will be or not, don't
have a great solution right now. . . .

eh, manual fixes and additions also not working great, something is up with the
way this dat ahas been stored, what a hassle.
"""


degreeDict = dict(zip(dfMap['codevalue'], dfMap['valuelabel']))

degreeNames = []
uCodes = list(set(df['cipcode']))

for uCode in uCodes:
    if uCode < 100:
        try:
            n = degreeDict[uCode]
        except KeyError:
            if len(str(uCode)) >7:
                uCode = np.round(uCode,3)
                n = degreeDict[uCode]
            else:
                pdb.set_trace()
        
#df['code_name'] = [degreeDict[x] for x in df['cipcode'].values]
