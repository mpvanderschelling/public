# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:04:41 2020

@author: mpvan
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
from statistics import median,mean


if os.path.exists('./data.txt'):
        dic = json.load(open('data.txt'))
        
 #convert timestamp keys to datetime format   
fmt = mdates.DateFormatter('%H:%M')  
t = [datetime.datetime.fromtimestamp(round(int(i)/1000)) for i in list(dic.keys())]    

keys = list(dic.keys())

for i in range(len(keys)):
    dic[t[i]] = dic.pop(keys[i])
    
#three time-windows

now = list(dic.keys())[-1]
sixhours = now - datetime.timedelta(hours=6)
twentyfour = now - datetime.timedelta(days=1)


def overview(product):      
    
    def timeplot(i,timespan,title):    
        t = [i for i in list(dic.keys()) if i > timespan]
        b = [bdic[product][i] for i in t]
        s = [sdic[product][i] for i in t]
        ax[i].set_title(title, color='w')
        ax[i].set_facecolor('#595959')
        
        bave = []
        for j in range(len(b)):
            im = j-10
            if im<0:
                im=0
            ip = j+10
            if ip>(len(b)-1):
                ip=len(b)-1  
            bave.append(mean(b[im:ip]))
            
        save = []
        for j in range(len(s)):
            im = j-10
            if im<0:
                im=0
            ip = j+10
            if ip>(len(s)-1):
                ip=len(s)-1  
            save.append(mean(s[im:ip]))
        #spines
        ax[i].spines["top"].set_color('#C8C8C8')
        ax[i].spines["bottom"].set_color('#C8C8C8')
        ax[i].spines["right"].set_visible(False)
        ax[i].spines["left"].set_visible(False)
        
        #x-axis date format
        ax[i].xaxis.set_major_formatter(fmt)
        
        
        #plotting
        ax[i].plot(t,b, color='#b3d7ff') #25%
        ax[i].plot(t,bave, color='b') #25%
        ax[i].plot(t,s, color='#99ffeb')
        ax[i].plot(t,save, color='g') #25%        
        #grid
        ax[i].grid(b=True,which='both',axis='y',color='#C8C8C8')  
        
          
        #x-axis
        ax[i].set_xlim((t[0],t[-1]))
        ax[i].tick_params(axis='x', colors='w', labelsize='small')
        
        
        #y-axis
        ax[i].set_ylim((min(s)*0.98,max(b)*1.02))
        ax[i].set_yticks(np.linspace(min(s)*0.98,max(b)*1.02,6))
        ax[i].tick_params(axis='y', which='both', colors='w', labelsize='small', labelleft='on', labelright='on', length=0)

       
        #fill
        ax[i].fill_between(t,b,s, facecolor='#4da6ff', alpha=0.5)
        ax[i].fill_between(t,min(s)*0.98,s, facecolor='#4dffdb', alpha=0.5)



    fig, ax = plt.subplots(3, figsize=(10,9))
    fig.suptitle(product, fontsize=16, color='w')
    fig.patch.set_facecolor('#404040')
    timeplot(0,sixhours,'6 hours') #one hour of data
    timeplot(1,twentyfour, '1 day') #24 hours of data
    timeplot(2,t[0], 'total overview') #the whole dataset


buy = {}



#make product keyed dictionary
productlist = [i for i in list(dic[list(dic.keys())[0]].keys())]
bdic = {}
sdic = {}
for product in productlist:
    bdic[product] = {}
    sdic[product] = {}
    for time in list(dic.keys()):
        bdic[product][time] = dic[time][product]['buyPrice']
        sdic[product][time] = dic[time][product]['sellPrice']

overview('ENCHANTED_LAPIS_LAZULI')

def getproduct(buysell,product,timespan):
    return [buysell[product][i] for i in list(dic.keys()) if i > timespan]


change = {}

for product in productlist:
    a = getproduct(bdic,product,twentyfour)
    try:
        change[product] = 100*((a[-1]-a[0])/a[0])
    except ZeroDivisionError:
        change[product] = 0.0
        
print(min(change, key=change.get))


#for product in dic[list(dic.keys())[0]].keys():
#    buy[product] = {}
#    for time in list(dic.keys()):
#        buy[product][time] = dic[time][product]['buyPrice']
#
#
#plist = [i for i in buy.keys() if median(buy[i].values()) > 600.0 ]        
#
#

#
#def timedata(dictionary,timespan):    
#    t = [i for i in list(dic.keys()) if i > timespan]
#    b = [dictionary[product][i] for i in t for product in plist]
#    return b
#
#
#change = {}
#
#for product in plist: #dic[list(dic.keys())[0]].keys():
#    try:
#        change[product] = 100*((buy[product][now]-buy[product][sixhours])/buy[product][sixhours])
#        #change.append(100*((buy[product][now]-buy[product][onehour])/buy[product][onehour]))
#    except ZeroDivisionError:
#        change[product] = 0.0
#        
#        
#print(min(change, key=change.get))
#
#overview(min(change, key=change.get))

#bave = []
#for i in range(len(b)):
#    im = i-10
#    if im<0:
#        im=0
#    ip = i+10
#    if ip>(len(b)-1):
#        ip=len(b)-1
#        
#    bave.append(mean(b[im:ip]))