import pandas as pd
import geopy
from geopy.distance import great_circle


# Put the csv file to dataframe

india_grid = pd.read_csv("/home/kamran/documents/merged_grid.csv", index_col=False)

print("India grid csv successfully loaded")


cities = pd.read_csv("/home/kamran/documents/worldcities.csv")

print("Cities csv successfully loaded")


# Take only lat lon in india_grid dataframe

india_grid = india_grid.loc[:, ['lon', 'lat']]

india_grid.columns = ['lng', 'lat']

india_grid['point'] = list(zip(india_grid.lat, india_grid.lng))

print("Updated india grid successfully loaded")


# Take only lat lng city of india in cities dataframe

india_cities = cities.loc[cities.country == 'India', ['lat', 'lng', 'city']]

india_cities['point'] = list(zip(india_cities.lat, india_cities.lng))

india_cities.reset_index(inplace=True, drop=True)

print("Updated cities successfully loaded")


# Define boundaries function

def boundaries(point, span):
    result = {}
    result['lat_min'] = point[0]-span
    result['lat_max'] = point[0]+span
    result['lng_min'] = point[1]-span
    result['lng_max'] = point[1]+span
    
    return result

print("boundaries function success")


# Define subset function

def subset(point, span, df):
    bounds = boundaries(point, span)
    
    sub_lat = (india_cities.lat >= bounds['lat_min']) & (india_cities.lat <= bounds['lat_max'])
    
    sub_lon = (india_cities.lng >= bounds['lng_min']) & (india_cities.lng <= bounds['lng_max'])
    
    sub = sub_lat & sub_lon

    result = df.loc[sub]
    
    return result

print("subset function success")


# Define all_distances function

def all_distances(df_point, span, df_cities):
    """Get distance for every city, for a given point."""
    
    data = subset(df_point, span, df_cities).copy()
    
    distances = data.apply(
        lambda row: great_circle(row['point'], df_point),
        axis=1
    )
        
    data['dist'] = distances

    min_dist = data.dist.min()

    result = data.loc[data.dist == min_dist, 'city'].values[0]
    result2 = data.loc[data.dist == min_dist, 'dist'].values[0]

    return result, result2
    
print("all_distances function success")


# Print out result

result = india_grid.apply(lambda row: all_distances(row['point'], 5, india_cities), axis=1)

india_grid['city'] = result

print("result success")

# Separate the city and dist column
a = pd.DataFrame(india_grid['city'].values.tolist(), columns = ['city','dist'])

india_grid2 = india_grid.drop('city', axis=1).merge(a,how = 'left', right_index=True, left_index=True)

print("separation success")

# Write to csv

india_grid2.to_csv(r'/home/kamran/documents/india_grid_cities.csv', index=False)



