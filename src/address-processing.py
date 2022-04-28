from turtle import distance
import pandas as pd
import numpy as np
import folium
import os
from geopy.geocoders import Photon
from geopy.extra.rate_limiter import RateLimiter
from math import ceil
from geopy.distance import geodesic
from scipy.spatial.distance import cdist


def get_coords(sample_size: float):

    test_data = pd.read_csv('data/processed/deliveries-by-address.csv')
    test_data = test_data.sample(frac=sample_size, random_state=0)
    locator = Photon(user_agent='mona7501', timeout=10)

    # Create a RateLimiter object to limit requests to the API.
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

    test_data['locations'] = test_data['full_address'].apply(geocode)
    print(f'Found {(1 - test_data.locations.isnull().sum() / len(test_data))*100:.4f} % of the addresses')
    test_data['point'] = test_data['locations'].apply(lambda loc: tuple(loc.point) if loc else None)
    # Drop rows with missing locations
    test_data = test_data[test_data.locations.notnull()]
    test_data[['latitude', 'longitude', 'altitude']] = pd.DataFrame(test_data['point'].tolist(), index=test_data.index)

    test_data.to_csv('data/processed/deliveries-by-address-with-coords.csv', index=False)
    print(f'Proccessed {len(test_data)} addresses')


def get_distance_matrix():

    deliveries_df = pd.read_csv('data/processed/deliveries-by-address-with-coords.csv')
    points = np.array(deliveries_df[['latitude', 'longitude']].values)
    
    distance_matrix = cdist(points, points, lambda u, v: geodesic(u, v).km)
    distance_matrix = pd.DataFrame(distance_matrix, index=deliveries_df.index, columns=deliveries_df.index)
    distance_matrix.to_csv('data/processed/distance_matrix.csv')
    

if __name__ == '__main__':

    sample_size = 1

    # Check if the file exists
    if not os.path.isfile('data/processed/deliveries-by-address-with-coords.csv'):
        print('Getting coordinates...')
        get_coords(sample_size)
        print('Done!')
    
    elif input('File already exists. Do you want to overwrite it? (y/n) ') == 'y':
        print('Getting coordinates...')
        get_coords(sample_size)
    
    elif not os.path.isfile('data/processed/distance_matrix.csv'):
        print('Getting distance matrix...')
        get_distance_matrix()
        print('Done!')

    elif input('Distance matrix already exists. Do you want to overwrite it? (y/n) ') == 'y':
        print('Getting distance matrix...')
        get_distance_matrix()
        print('Done!')

    print('Done!')
