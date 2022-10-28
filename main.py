
import pandas as pd
import geopandas as gpd
import geopy as gpy

# Load addresses data
df_add = pd.read_csv('./data/adresses.csv') #CSVの列名について指定しておく必要あり

# Make complete addresses
address_format = lambda x: '{}, {}, {}'.format(*x)
df_add['Adresse complète'] = df_add[['Adresse', 'Ville', 'Pays']].apply(address_format, axis=1)

# Geocoding
geolocator = gpy.Nominatim(user_agent='julius2718')

def get_coordinates(address: str, geolocator: gpy.Nominatim):
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)

df_add = df_add.assign(
    Coords=df_add['Adresse complète'].apply(lambda x: get_coordinates(x, geolocator))
)
df_add[['Lat', 'Long']] = pd.DataFrame(df_add['Coords'].tolist(), index=df_add.index)
