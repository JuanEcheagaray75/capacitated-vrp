import pandas as pd
import os
from geopy.geocoders import Photon
from geopy.extra.rate_limiter import RateLimiter
import openrouteservice as ors
from math import ceil



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


def get_driving_distance(from_: str='MONTERREY', sample_size: float=0.1):
    # Get data
    deliveries_df = pd.read_csv('data/processed/deliveries-by-address-with-coords.csv')
    # Use of a sample size for testing the library
    deliveries_df = deliveries_df.sample(frac=sample_size, random_state=0)
    
    # Get the coordinates of the cedis
    cedis_locs = pd.read_csv('data/processed/cedis.csv')
    cedis_locs = cedis_locs[cedis_locs['CEDIS REG'] == from_]
    cedis_x, cedis_y = cedis_locs['coord1'][0], cedis_locs['coord2'][0]
    cedis = [cedis_x, cedis_y]

    # Get API key for ORS
    with open(file='api-key.txt', mode='r') as f:
        api_key = f.read()

    # Max volume per unit
    MAX_VOL = 12
    # Max hours per unit
    MAX_HOURS = 8
    needed_units = ceil(deliveries_df['Vol'].sum() / MAX_VOL)
    # Time to wait at delivery site (in minutes)
    WAIT_TIME = 20

    # Units to be sent
    vehicles = list()
    for i in range(needed_units):
        vehicles.append(
            ors.optimization.Vehicle(
                id=i,
                start=list(reversed(cedis)),
                capacity=[MAX_VOL],
                time_window=[0, 60 * 60 * MAX_HOURS]
            )
        )

    # Places for them to go
    clients = list()
    for customer in deliveries_df.itertuples():
        clients.append(
            ors.optimization.Job(
                id=customer.Index,
                location=[customer.latitude, customer.longitude],
                service=60*WAIT_TIME,
                amount=[customer.Vol]
            )
        )

    # Initialize client
    ors_client = ors.Client(api_key=api_key)
    result = ors_client.optimization(
        jobs=clients,
        vehicles=vehicles,
        geometry=True
    )


    
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

    print('Done!')

