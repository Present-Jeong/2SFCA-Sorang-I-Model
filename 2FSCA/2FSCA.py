from os import stat
import pandas as pd
import numpy as np
import json
import geopandas as gpd
from matplotlib import pyplot as plt
from ipywidgets import interact, interact_manual,IntSlider
from matplotlib import font_manager, rc
from shapely import geometry
from shapely.geometry import Polygon, LineString, Point

# PM = pd.read_excel('population.xlsx')
# PM = PM.loc[PM['읍·면·동별(3)'] == '소계']
# PM = PM[['읍·면·동별(1)','2018.1']]
# PM =PM.dropna(how='any') 
# PM =PM.drop(PM.index[0]) 
# PM= PM.reset_index()
# PM = PM.drop('index',axis=1)
# PM = PM.rename(columns = {'읍·면·동별(1)' : 'name'})
# print(PM)

# state_geo = gpd.read_file('kostat/2018/json/skorea-municipalities-2018-geo.json')
# state_geo2 = state_geo.iloc[202:226]
# state_geo3 = state_geo.iloc[41:49]
# state_geo = state_geo3.append(state_geo2,ignore_index=True)
# print(state_geo)

# merge_outer = pd.merge(state_geo,PM, how='outer',on='name')
# print(merge_outer)

# PM['latitude'] = PM.Coordinate.str.split(',').str[0]
# PM['longitude'] = PM.Coordinate.str.split(',').str[1]
# PM['latitude'] = PM['latitude'].astype(float)
# PM['longitude'] = PM['longitude'].astype(float)
# PM['geometry'] = PM.apply(lambda row : Point([row['X'], row['Y']]), axis=1)
# PM = gpd.GeoDataFrame(PM, geometry='geometry')
# PM = PM.set_crs(epsg = 4326, inplace = True)
# PM = PM.to_crs(epsg=5181)
# print(PM)

import aceso
state_geo = gpd.read_file('kostat/2018/json/skorea-municipalities-2018-geo.json')
state_geo2 = state_geo.iloc[202:226]
state_geo3 = state_geo.iloc[41:49]
state_geo = state_geo3.append(state_geo2,ignore_index=True)
Population = pd.read_csv('population.csv',encoding='cp949')
Population.rename(columns = {'행정구역' : 'name','인구(명)':'population','면적(km2)':'size','인구밀도':'density'}, inplace = True)
Population.replace({'포항시 남구':'포항시남구','포항시 북구':'포항시북구'}, inplace = True)
state_geo =state_geo.merge(Population, on='name')
state_geo = state_geo.to_crs(epsg=5181)
state_geo['centroid'] = state_geo.centroid
centroid = state_geo['centroid']
print(centroid)

from shapely.geometry import Point
mypoints = centroid

listarray = []
for pp in mypoints:
    listarray.append([pp.x, pp.y])
centroid = np.array(listarray)


# Population = pd.read_csv('population.csv',encoding='cp949')
# Population.rename(columns = {'행정구역' : 'name','인구(명)':'population','면적(km2)':'size','인구밀도':'density'}, inplace = True)
# Population.replace({'포항시 남구':'포항시남구','포항시 북구':'포항시북구'}, inplace = True)
# state_geo = pd.read_csv('dataresult.csv')
# state_geo=pd.merge(state_geo,Population,on='name')

hospital = gpd.read_file('hospital.dbf')
hospital2 = hospital[hospital['MEGA_NM'] == '경상북도']
hospital3 = hospital[hospital['MEGA_NM'] == '대구광역시']
hospital = hospital3.append(hospital2,ignore_index=True)

hospital['X_AXIS'] = hospital['X_AXIS'].astype(float)
hospital['Y_AXIS'] = hospital['Y_AXIS'].astype(float)
hospital['geometry'] = hospital.apply(lambda row : Point([row['X_AXIS']-112000, row['Y_AXIS']-97000]), axis=1)
hospital_geo = hospital['geometry']
print(hospital_geo)
# hospital_geo = gpd.GeoDataFrame(hospital_geo)

mypoints = hospital_geo

listarray = []
for pp in mypoints:
    listarray.append([pp.x, pp.y])
hospital_geo = np.array(listarray)

from scipy.spatial import distance_matrix
distance_matrix = distance_matrix(centroid,hospital_geo)
# distance_matrix= gpd.GeoDataFrame([centroid,hospital_geo])
# print(distance_matrix)

model = aceso.TwoStepFCA(radius=80000)
state_geo['access_score'] = model.calculate_accessibility_scores(distance_matrix =distance_matrix,demand_array=state_geo['population'].values) #demand_array=state_geo['population'].values
print(state_geo['access_score'])

# ax = state_geo.plot(figsize=(15,25),column='access_score',edgecolor='white',cmap='Blues',legend=True)
# state_geo['access_score'].plot(ax=ax,marker='.', color='orange')
# plt.savefig('2SFCA.png')
print(state_geo)
# fig, ax = plt.subplots()
import seaborn as sns
sns.barplot(x='name_eng',y='access_score',data=state_geo,dodge=False)
plt.xticks(rotation = 90)
# plt.xticks(state_ge  o['name'])
plt.tight_layout() 

plt.show()
plt.savefig('Accessibility.png')
