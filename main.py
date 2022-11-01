
import pandas as pd
import geopandas as gpd
import geopy as gpy

# Load addresses data
df_add = pd.read_csv('./data/adresses.csv')

# Make complete addresses
address_format = lambda x: '{}, {}, {}'.format(*x)
df_add['Adresse complète'] = df_add[['Adresse', 'Ville', 'Pays']].apply(address_format, axis=1)

# Geocoding
geolocator = gpy.Nominatim(user_agent='julius2718')

def get_coordinates(address: str, geolocator: gpy.Nominatim):
    location = geolocator.geocode(address)
    return (location.longitude, location.latitude)

df_add = df_add.assign(
    Coords=df_add['Adresse complète'].apply(lambda x: get_coordinates(x, geolocator))
)
df_add[['Long', 'Lat']] = pd.DataFrame(df_add['Coords'].tolist(), index=df_add.index)

df_points = gpd.tools.geocode(df_add['Adresse complète'], provider='nominatim', user_agent='julius2718')