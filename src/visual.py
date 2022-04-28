import pandas as pd
import folium


def visualize_address():
    deliveries = pd.read_csv('data/processed/deliveries-by-address-with-coords.csv')
    cedis_locs = pd.read_csv('data/processed/cedis.csv')
    # Get Monterrey Cedis locations
    cedis_locs = cedis_locs[cedis_locs['CEDIS REG'] == 'MONTERREY']
    cedis_location = cedis_locs['coord1'], cedis_locs['coord2']

    map_ = folium.Map(location=cedis_location, zoom_start=12)
    # Add the specific location of cedis to map_
    folium.Marker(location=cedis_location, popup='Cedis Monterrey', icon=folium.Icon(color='red')).add_to(map_)
    deliveries.apply(lambda row: folium.Marker(
                                location=[row['latitude'], 
                                row['longitude']], popup=row['full_address'] + '\n Volume:' + str(row['Vol'])
                                ).add_to(map_), axis=1)
    map_.save('deliveries_map.html')


def visualize_routes():
    pass


if __name__ == '__main__':
    visualize_address()