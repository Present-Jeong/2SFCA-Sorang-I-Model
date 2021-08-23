from os import stat
import pandas as pd
import numpy as np
import json
import geopandas as gpd
from matplotlib import pyplot as plt
from ipywidgets import interact, interact_manual,IntSlider
from matplotlib import font_manager, rc
from shapely.geometry import Polygon, LineString, Point

state_geo = gpd.read_file('kostat/2018/json/skorea-municipalities-2018-geo.json')
state_geo2 = state_geo.iloc[202:226]
state_geo3 = state_geo.iloc[41:49]
state_geo = state_geo3.append(state_geo2,ignore_index=True)
# state_geo.to_csv('dataresult.csv',encoding='utf-8-sig')
# state_geo.plot(figsize=(10,10),color='none',edgecolor='gainsboro',zorder=3)
# print(state_geo.centroid.head())
Population = pd.read_csv('population.csv',encoding='cp949')
Population.rename(columns = {'행정구역' : 'name','인구(명)':'population','면적(km2)':'size','인구밀도':'density'}, inplace = True)
Population.replace({'포항시 남구':'포항시남구','포항시 북구':'포항시북구'}, inplace = True)
state_geo =state_geo.merge(Population, on='name')

hospital = gpd.read_file('hospital.dbf')
hospital2 = hospital[hospital['MEGA_NM'] == '경상북도']
hospital3 = hospital[hospital['MEGA_NM'] == '대구광역시']
hospital = hospital3.append(hospital2,ignore_index=True)

hospital['X_AXIS'] = hospital['X_AXIS'].astype(float)
hospital['Y_AXIS'] = hospital['Y_AXIS'].astype(float)
hospital['geometry'] = hospital.apply(lambda row : Point([row['X_AXIS']-112000, row['Y_AXIS']-97000]), axis=1)
hospital = gpd.GeoDataFrame(hospital, geometry='geometry')
hospital.crs = "EPSG:5181"
state_geo = state_geo.to_crs(epsg=5181)
# hospital.to_csv('hospital.csv',encoding='utf-8-sig')

EMR = pd.read_csv('EMR.csv',encoding='cp949')
EMR['latitude'] = EMR.Coordinate.str.split(',').str[0]
EMR['longitude'] = EMR.Coordinate.str.split(',').str[1]
EMR['latitude'] = EMR['latitude'].astype(float)
EMR['longitude'] = EMR['longitude'].astype(float)
EMR['geometry'] = EMR.apply(lambda row : Point([row['longitude'], row['latitude']]), axis=1)
EMR = gpd.GeoDataFrame(EMR, geometry='geometry')
EMR = EMR.set_crs(epsg = 4326, inplace = True)
EMR = EMR.to_crs(epsg=5181)

PH = pd.read_csv('Public Health.csv',encoding='cp949')
PH['geometry'] = PH.apply(lambda row : Point([row['X']-0.01, row['Y']+0.01]), axis=1)
PH = gpd.GeoDataFrame(PH, geometry='geometry')
PH = PH.set_crs(epsg = 4326, inplace = True)
PH = PH.to_crs(epsg=5181)


PM = pd.read_csv('Pharmacy.csv',encoding='cp949')
PM['geometry'] = PM.apply(lambda row : Point([row['X'], row['Y']]), axis=1)
PM = gpd.GeoDataFrame(PM, geometry='geometry')
PM = PM.set_crs(epsg = 4326, inplace = True)
PM = PM.to_crs(epsg=5181)


# state_geo = state_geo.set_crs(epsg=5179)
print(state_geo.crs)
print(hospital.crs)
print(EMR.crs)
print(PH.crs)

# ax = state_geo.plot(figsize=(10,10),color='none',edgecolor='gainsboro',zorder=3)
ax = state_geo.plot(figsize=(15,25),color='green',alpha=0.2,edgecolor='gainsboro')

hospital.plot(ax=ax, marker='.', color='green', label='Hospital')
# hospital.plot(ax=ax, marker='.', color='blue', label='Hospital, Public Health')


# PH.plot(ax=ax,marker='.', color='yellow',label='Public Center')
# # PH.plot(ax=ax,marker='.', color='lightgreen', label='Public Center')

PM.plot(ax=ax,marker='.', color='maroon',label='Pharmacy',alpha=0.5)

EMR.plot(ax=ax,marker='v', color='blue',label='EMR')
# # EMR.plot(ax=ax,marker='.', color='black', label='EMR')

# ax.set_title("Kyoung Buk", fontsize=20)
# ax.set_axis_off()
plt.legend()
plt.show()
plt.savefig('kyoungbuk.png')

# buf_poly = gpd.GeoDataFrame({'geometry': hospital.buffer(3000)})
# origin_ = state_geo.groupby(['name']).apply(lambda gr : gr.area.sum())
# ax = state_geo.plot(column='name', figsize=(8,8), alpha=0.8,edgecolor='white')
# hospital.plot(ax=ax, marker='.', color='white', label='Hospital',markersize=0.5)
# buf_poly.plot(ax=ax, color='white')
# # ax.set_axis_off()
# plt.show()
# plt.savefig('hospital buffer - 3000.png')

# dif_area = gpd.overlay(state_geo, buf_poly, how='difference')
# dif_area = dif_area.dissolve(by='name')
# ax = dif_area.plot(color='black',figsize=(8,8), alpha=0.8)
# # ax.set_axis_off()
# plt.show()
# plt.savefig('Without buffer - 3000.png')


# print("전체 대비 미커버지역 비율")
# print((dif_area.area / origin_)* 100)

