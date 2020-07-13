# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:30:14 2020
@author: mpvan
"""
#api = 5d74290b-40ce-4728-ba10-8b7d04d5a649
import requests
import json
import time
import os
import datetime

#.... fetch data

f = requests.get("https://api.hypixel.net/skyblock/bazaar?key=45dc5587-8bce-4c9a-89c0-aee58a68ab9d").json() 

if f['success']:
   
    timestamp = datetime.datetime.fromtimestamp(round(f['lastUpdated']/1000))
    #updates every 10s
    #lastupdated is in ms
    
    #.... only save important data
    
    data = {}
    data[f['lastUpdated']] = {}
    
    for i in list(f['products'].keys()):
        data[f['lastUpdated']][i] = {}  
        
    for i in list(f['products'].keys()):
        for j in list(f['products']['BLAZE_ROD']['quick_status'].keys()):
            data[f['lastUpdated']][i][j] = f['products'][i]['quick_status'][j]
    
    
    #................
        
    if os.path.exists('./data.txt'):
            dic = json.load(open('data.txt'))
    
    else:
        dic = data
        json.dump(dic,open('data.txt','w+'))
        print("made datafile") 
      
    
    dic.update(data)
    json.dump(dic,open('data.txt','w'))
#print("wrote data %d" %k)

#time.sleep(60)
