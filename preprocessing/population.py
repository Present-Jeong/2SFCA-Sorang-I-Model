import pandas as pd
import numpy as np
import json
import geopandas as gpd
from matplotlib import pyplot as plt
from ipywidgets import interact, interact_manual,IntSlider
from matplotlib import font_manager, rc
from shapely import geometry
from shapely.geometry import Polygon, LineString, Point

state_geo = gpd.read_file('kostat/2018/json/skorea-submunicipalities-2018-geo.json')
state_geo2 = state_geo.iloc[202:226]
state_geo3 = state_geo.iloc[41:49]
state_geo = state_geo3.append(state_geo2,ignore_index=True)
Population = pd.read_csv('population.csv',encoding='cp949')
Population.rename(columns = {'행정구역' : 'name','인구(명)':'population','면적(km2)':'size','인구밀도':'density'}, inplace = True)
Population.replace({'포항시 남구':'포항시남구','포항시 북구':'포항시북구'}, inplace = True)
state_geo =state_geo.merge(Population, on='name')
state_geo = state_geo.to_crs(epsg=5181)
ax = state_geo.plot(figsize=(10,10),column='density',cmap='BuGn',edgecolor='gainsboro',alpha=0.8,legend=True)

plt.show()
plt.savefig('Population.png')
