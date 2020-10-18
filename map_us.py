import pandas as pd
import io
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from datetime import datetime, timedelta

# 1 - Cropping and resizing US map (alaska + hawaii)

poly_States = gpd.read_file('datasets/states/cb_2019_us_state_20m.shp')

alaska_gdf = poly_States.loc[poly_States['STUSPS'] == "AK"]
alaska_mp = alaska_gdf['geometry'].values[0]

ak_exp_gdf = gpd.GeoDataFrame(alaska_mp)
ak_exp_gdf.columns = ['geometry']

# create polygon that covers Alaska up to the 180th Meridian
target_poly = Polygon([(-180, 50), (-180, 75),
                       (-100, 75), (-100, 50)])

western_isles = ak_exp_gdf[ak_exp_gdf.intersects(target_poly) == False].copy()
eastern_ak = ak_exp_gdf[ak_exp_gdf.intersects(target_poly)].copy()

# add a column to groupby
eastern_ak['STUSPS'] = 'AK'
# combine polygons/records into a single multipolygon/record
alaska_trimmed = eastern_ak.dissolve(by='STUSPS')

# add this new multipolygon in place of the old alaska multipolygon
states_trimmed = poly_States.copy()
states_trimmed.loc[states_trimmed['STUSPS'] == 'AK', 'geometry'] = alaska_trimmed['geometry'].values

alaska = states_trimmed.STUSPS == "AK"
states_trimmed[alaska] = states_trimmed[alaska].set_geometry(states_trimmed[alaska].scale(.5,.5,.5).translate(40, -40))
hawaii = states_trimmed.STUSPS == "HI"
states_trimmed[hawaii] = states_trimmed[hawaii].set_geometry(states_trimmed[hawaii].translate(70))

# states_trimmed.plot()
# plt.show()


# 2 - Getting Senatorial polls dataset

# sen_df = pd.read_csv('senate_state_toplines_2020.csv')
# sen_df = requests.get('https://projects.fivethirtyeight.com/2020-general-data/presidential_national_toplines_2020.csv')
# sen_df = sen_df.content.decode('utf-8').splitlines()
# print(sen_df)
# sen_df = pd.read_csv(sen_df)

senate_data_url = 'https://projects.fivethirtyeight.com/2020-general-data/senate_state_toplines_2020.csv'
sen_df = pd.read_csv(senate_data_url)

sen_df = sen_df[['forecastdate', 'district', 'winner_Rparty']]
# reformat district names to match that of the shapefile:
sen_df['district'] = sen_df['district'].apply(lambda x: x[:2])
# reformat 'forecastdate' to a date format
sen_df['forecastdate'] = sen_df['forecastdate'].apply(lambda x: datetime.strptime(x, '%m/%d/%y'))
sen_pivot = pd.pivot_table(sen_df, values='winner_Rparty', index=['forecastdate', 'district'], aggfunc=np.mean)
print(sen_df)
sen_df = sen_df.groupby(['forecastdate', 'district'], as_index=False).mean()
print(sen_df)
# print(sen_pivot)
# print(sen_pivot.head())
# print(pd.Timestamp('2020-09-01'), datetime.now()-timedelta(days=60))

# removing rows based on condition:
sen_df = sen_df.drop(sen_df[sen_df.forecastdate < datetime.now()-timedelta(days=60)].index)

# print(datetime.strptime(sen_df['forecastdate'], '%m/%d/%y'))
# for date in sen_df['forecastdate']:
#     print(datetime.strptime(date, '%m/%d/%y'))

# print(datetime.strptime('9/30/20', ))

last_day = max(sen_df['forecastdate'])

print(type(last_day))
print(pd.Timestamp('2020-08-01'))

shapefile_headers2 = ['STUSPS', 'STATENS', 'AFFGEOID', 'GEOID', 'STATEFP', 'NAME', 'LSAD', 'ALAND', 'AWATER', 'geometry']
states_trimmed = states_trimmed[shapefile_headers2]

print(shapefile_headers2)
merged = states_trimmed.merge(sen_df, left_on='STUSPS', right_on='district', how='outer')
merged1 = merged.sort_values(by='forecastdate', ascending=False)
merged2 = merged.sort_values(by='forecastdate', ascending=True)

# merged['winner_Dparty'] = merged['winner_Dparty'].fillna(0)
print(merged)


variable = 'winner_Rparty'
vmin, vmax = 0.2, 0.8
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12,4))
merged1.plot(column=variable, cmap='bwr', linewidth=0.8, ax=ax1, edgecolor='grey', legend=False, missing_kwds={'color': 'lightgrey'})
merged2.plot(column=variable, cmap='bwr', linewidth=0.8, ax=ax2, edgecolor='grey', legend=False, missing_kwds={'color': 'lightgrey'},
             legend_kwds={'orientation': 'horizontal'})
plt.tight_layout()
print(merged)
plt.show()


# print(sen_df)