import subprocess as sp
import numpy as np
import pandas as pd
import sys 
import folium
from folium.plugins import HeatMap
import geopandas as gpd

sp.call('wget -nc  https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',shell=True)
df=pd.read_csv('all_month.csv',)
print('enter all or value of magnitude')
a= input()

if a == 'all':
        map = folium.Map(location=[48, -102], zoom_start=1)
        df_2=df[['latitude','longitude']]
        geolist=df_2.values.tolist()
        HeatMap(geolist,radius=7,blur=2).add_to(map)
        map.save('map.html')
        map
        #sp.call('open geomap.html',shell=True)
        #sp.call('explorer.exe geomap.html',shell=True)
        #sp.call('start geomap.html',shell=True)
    
elif a.isnumeric(): #数字以上のマグニチュード以上のヒートマップ
        map = folium.Map(location=[48, -102], zoom_start=1)
        df_2=df[['latitude','longitude','mag']]
        df_3=df_2[df_2['mag'] >= float(a)]
        df_4=df_3[['latitude','longitude']]
        geolist=df_4.values.tolist()
        HeatMap(geolist,radius=7,blur=2).add_to(map)
        map.save('map.html')
        map
        #sp.call('explorer.exe geomap.html',shell=True)
        #sp.call('open geomap.html',shell=True)
        #sp.call('start geomap.html',shell=True)
    
else: #マグニチュード５以上の地点のみマッピング
        map = folium.Map(location=[48, -102], zoom_start=1)
        df_2=df[['latitude','longitude','mag']]
        df_3=df_2[df_2['mag'] >= float(5)]
        for i, r in df_3.iterrows():
            folium.Marker(location=[r['latitude'], r['longitude']], popup=r['mag']).add_to(map)
        map.save('map.html')
        map
        #sp.call('explorer.exe geomap.html',shell=True)
        #sp.call('open geomap.html',shell=True)
        #sp.call('start geomap.html',shell=True)

print('saved map.html')