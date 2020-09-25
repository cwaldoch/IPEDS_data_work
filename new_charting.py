# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:51:09 2020

@author: .3
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
import random
import matplotlib
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import imageio
import os, sys
from math import pi

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

#dfBach.to_csv(r'C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\bachelors_degrees.csv', index=False)
# so can do for years in years then do the dfPivotFam4 things for charts
dfBach = dfBach[~dfBach['fam2'].isin(['Military', 'Misc. Certifications',
                'Multi-disciplinary', 'Other Services'])]
#
#yearTotals = pd.pivot_table(dfBach, values = 'CTOTALT', index=['year2'],
#                            aggfunc = np.sum)

#    throw out 1980
    
def animate(year):
    ax.clear()
   # plt.close()

    dfYear = dfBach[dfBach['year2'] == year]
    
    dfPivotFam4 = pd.pivot_table(dfYear, values = 'CTOTALT', index=['fam2'],
                                 aggfunc = np.sum)
    
    #famNames  = list(set(dfBach['fam2'].values))
    labels = list(dfPivotFam4.index)
    categories=labels
    N = len(categories)
    #    pdb.set_trace() 
    
    categories = ['Ag',
     'Architecture',
     'Arts',
     'Aviation',
     'Business',
     'Comm.',
     'Computer\n Science',
     'Divinity',
     'Education',
     'Engineering',
     'Family\n Home\n Studies',
     'General\n Multi\n International\n Studies',
     'Healthcare',
     'Physical\n Sciences',
     'Public\n Policy',
     'Recreation\n Sports\n Tourism',
     'Social\n Sciences',
     'Trades\n Technicians',
     'Traditional\n Studies']
    totalDegrees = np.sum(dfPivotFam4['CTOTALT'])
    dfPivotFam4['pct'] = [(x/totalDegrees)*100 for x in dfPivotFam4['CTOTALT'].values]
    
    values=list(dfPivotFam4['pct'].values)
    values += values[:1]
    #print(max(dfPivotFam4['pct']))
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
     
    
    #pdb.set_trace()
    
    maxVal = max(values)
    upperBound = int(np.around(maxVal/5, decimals=0)*5)+5
#    upperBound = 25
    
    
    #plt.xticks(angles[:-1], categories, color='k', size=6)
    
   # plt.yticks(list(range(0,upperBound,5)), [str(x)+'%' for x in list(range(0,upperBound,5))], color="grey", size=8)
    
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color='k', size =15)
#    ax.set_yticks(list(range(0,upperBound,5)))
#    ax.set_yticklabels([str(x)+'%' for x in list(range(0,upperBound,5))], size=11, color='k')
#    plt.ylim(0,upperBound)
    yticks = [0,5,10,15,20]
    ax.set_yticks([0,5,10,15,20])
    ax.set_yticklabels([str(x)+'%' for x in yticks], size=11, color='k')
    ax.set_ylim(0,yticks[-1])
    #plt.show()
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid', color='blue')
    #ax.tick_params(rotation='auto')
    ax.axes.tick_params(pad=24)
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    #ax.title('Degrees Granted by % of Total: '+str(year))
    ax.set_title('Degrees Granted by % of Total: '+str(year),
                 fontdict={'fontsize': '20'})
    
   #plt.savefig(r'C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\charts_out\\'+str(year)+'_radar_test1.png', dpi =300)
    plt.close()
    
years = list(set(dfBach['year2'].values) - set([1980]))
    
fig = plt.figure(figsize=(9,9))
ax = fig.add_subplot(111, polar=True)
aniMap = animation.FuncAnimation(fig, animate, years, interval=40, blit=False)
#fig.tight_layout()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=0.75, metadata=dict(artist='Me'), bitrate=4000)



aniMap.save(r'C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\charts_out\mp4_chart.mp4', writer=writer)
    

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(inputpath, targetFormat):
    outputpath = os.path.splitext(inputpath)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=fps)
    for i,im in enumerate(reader):
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
    print("Done.")

convertFile(r'C:\Users\.3\Desktop\degrees_data\IPEDS_data_work\charts_out\mp4_chart.mp4',
            TargetFormat.GIF)
    
    