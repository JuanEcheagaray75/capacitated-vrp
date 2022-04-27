import pandas as pd
import os
from geopy.geocoders import Photon
from geopy.extra.rate_limiter import RateLimiter




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



def get_driving_distance():
    pass


if __name__ == '__main__':
    # Check if the file exists
    if not os.path.isfile('data/processed/deliveries-by-address-with-coords.csv'):
        print('Getting coordinates...')
        get_coords(0.5)
        print('Done!')
    
    else:
        print('File already exists, skipping...')

    print('Done!')

