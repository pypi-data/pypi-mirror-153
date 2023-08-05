# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:43:19 2022

@author: franc

Per non avere problemi con le librerie creare un nuovo ambiente python dove sono installate solo le librerie utilizzate:
    - os, pandas e geopandas

Gli unici parametri da modificare nel codie sono il valore del raggio di interesse r alla riga 22, e i percorsi che rimandano agli shapefile delle province e dei punti di interesse
"""

#%% Import pacchetti

import os, time
from os.path import basename
import pandas as pd
import geopandas as gpd
from shapely.ops import nearest_points

#%% Creazione della funzione count
class PoisStatistics:
    '''
    This class defines two functions:
    1 - Given a points shapefile of reference points, a lists of polygon shapefile that subdived the study area, a radius r of interest, the desired coordinate reference system (crs), and a series of points shapefile containing the point of interests (POIs), counts the numbers of POIs inside the defined radius r from the reference points. This number is added to a new database column
    2 - Given a points shapefile of reference points, a lists of polygon shapefile that subdived the study area, the desired coordinate reference system (crs), and a series of points shapefile containing the point of interests (POIs), returns the distance between the reference point and the closest POI. The result is added to a new database column
    '''
    
    def __init__(self, point):
        self.point = point

    def CountPois(self, boundaries, pois, crs, r):
    
        pointsOpen = gpd.read_file(self.point)
        pointsUTM = pointsOpen.to_crs(epsg = crs)
        
        # "pois" è la lista che conterrà tutti i layer dei POI
        poisUTM = []
        poisName = []
        
        for poi in pois:
            poiOpen = gpd.GeoDataFrame.from_file(poi)
            poiUTM = poiOpen.to_crs(epsg = crs)
            poisUTM.append(poiUTM)
            poisName.append(basename(poi)[0:-4])
        
        # Ciclo di iterazione tra tutte le province e creazione della lista province
        
        bounds = []
        
        for roots, dirs, files in os.walk(boundaries):
            for name in files:
                if name.endswith('.shp'):
                    path = os.path.join(roots,name)
                    bounds.append(path)
        
        # Ciclo di iterazione tra tutte le province e work-flow
        
        tabelloneSum = gpd.GeoDataFrame()
        
        for bound in bounds:
            tic = time.time()
            print('Processing della provincia: {}'.format(basename(bound)[0:-4]))
            # Aprertura del file provincia e proiezione nel sistema di riferimento EPSG: 32632 con GeoPandas
            boundOpen = gpd.read_file(bound)
            boundUTM = boundOpen.to_crs(epsg=crs)
            
            # Creazione del buffer sul layer province
            boundBuffer = boundUTM.buffer(2*r)
            
            # Clip delle imprese sulla provincia SENZA buffer
            pointsClip = gpd.clip(pointsUTM, boundUTM)
            
            # Creazione del buffer sui punti delle imprese
            pointsClip['geometry'] = pointsClip.geometry.buffer(r)
            
            # Ciclo per il clip dei POI e il conteggio dei POI all'interno del raggio di interesse  
            pointsClipSum = pointsClip.copy()
            
            for j in range(len(poisUTM)):
                poiClip = gpd.clip(poisUTM[j], boundBuffer)
                pointsInPolygon = gpd.sjoin(poiClip, pointsClip, how = 'inner', predicate='intersects')
                pointsInPolygon[poisName[j] + '_in_{}_km'.format(str(int(r/1000)))] = 1
                pointsInPolygonSmall = pointsInPolygon[['cod_ID', poisName[j] +'_in_{}_km'.format(str(int(r/1000)))]].copy()
                pointsInPolygonSmall = pointsInPolygonSmall.groupby('cod_ID').agg({poisName[j] +'_in_{}_km'.format(str(int(r/1000))):'sum'}).reset_index()
                pointsClipSum = pd.merge(pointsClipSum, pointsInPolygonSmall, how='left', left_on = 'cod_ID', right_on = 'cod_ID')
         
            #tabella che contiene il risultato di tutti i POI e tutte le Province
            tabelloneSum = pd.concat([tabelloneSum,pointsClipSum])      
        
            toc=time.time()
            print('il processing della provincia {} ha richiesto {} secondi'.format(basename(bound)[0:-4], toc-tic))
            
        return tabelloneSum

    # Creazione della funzione nearest
    
    def Nearest(self, boundaries, pois, crs):
    
        pointsOpen = gpd.read_file(self.point)
        pointsUTM = pointsOpen.to_crs(epsg = crs)
        
        # "pois" è la lista che conterrà tutti i layer dei POI
        poisUTM = []
        poisName = []
        
        for poi in pois:
            poiOpen = gpd.GeoDataFrame.from_file(poi)
            poiUTM = poiOpen.to_crs(epsg = crs)
            poisUTM.append(poiUTM)
            poisName.append(basename(poi)[0:-4])
        
        # Ciclo di iterazione tra tutte le province e creazione della lista province
        
        bounds = []
        
        for roots, dirs, files in os.walk(boundaries):
            for name in files:
                if name.endswith('.shp'):
                    path = os.path.join(roots,name)
                    bounds.append(path)
        
        # Ciclo di iterazione tra tutte le province e work-flow
        tabelloneNear = gpd.GeoDataFrame()
        
        for bound in bounds:
            tic = time.time()
            print('Processing della provincia: {}'.format(basename(bound)[0:-4]))
            # Aprertura del file provincia e proiezione nel sistema di riferimento EPSG: 32632 con GeoPandas
            boundOpen = gpd.read_file(bound)
            boundUTM = boundOpen.to_crs(epsg=crs)
            
            # Clip delle imprese sulla provincia SENZA buffer
            pointsClip = gpd.clip(pointsUTM, boundUTM)
            pointsClipNB = pointsClip.copy()
            
            # Ciclo per il clip dei POI e il conteggio dei POI all'interno del raggio di interesse  
            pointsClipNear = pointsClipNB.copy()
            
            for j in range(len(poisUTM)):
                # distanza del punto più vicino        
                pointsClipNB[poisName[j]+'_nearest_dist'] = 0
                for index, row in pointsClipNB.iterrows():
                    pointRow = row.geometry
                    poiClipGeom = poisUTM[j].geometry.unary_union
                    pointGeom, nearestGeom = nearest_points(pointRow,poiClipGeom)
                    dist = ((pointGeom.x - nearestGeom.x)**2 + (pointGeom.y - nearestGeom.y)**2)**(1/2)
                    pointsClipNB.loc[index, poisName[j]+'_nearest_dist'] = dist
                pointsClipNBSmall = pointsClipNB[['cod_ID', poisName[j]+'_nearest_dist']].copy()
                pointsClipNear = pd.merge(pointsClipNear, pointsClipNBSmall, how = 'left', left_on = 'cod_ID', right_on = 'cod_ID')
                    
            #tabella che contiene il risultato di tutti i POI e tutte le Province
            tabelloneNear = pd.concat([tabelloneNear,pointsClipNear])        
        
            toc=time.time()
            print('il processing della provincia {} ha richiesto {} secondi'.format(basename(bound)[0:-4], toc-tic))
            
        return tabelloneNear