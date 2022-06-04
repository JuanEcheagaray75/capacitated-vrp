from math import dist
from src.solver import solver, visualize_routes
import numpy as np
import pandas as pd
from progress.bar import Bar


def test(n: int):
    """Test function that finds the best solution on a set of n solutions.

    Args:
        n (int): Number of trials to run.

    Returns:
        list: General list, see description bellow

    - best_route: contains a list of nodes where each node represents a client
    - distances.min: the minimum distance traveled by all the vehicles in the best solution
    - n_clients: a list that contains the number of clients visited by each vehicle in the best solution
    - best_distances: a list that contains the distance traveled by each vehicle in the best solution
    - best_load: a list that contains the load of each vehicle in the best solution

    """    
   
    distances = []
    routes = []
    distances_per_vehicle = []
    loads_per_vehicle = []

    with Bar('Processing...', max=n, suffix='%(percent).1f%% - %(eta)ds') as bar:
        for i in range(n):
            route, distance, total_load, distance_per_vehicle, load_per_vehicle = solver()
            distances.append(distance)
            routes.append(route)
            distances_per_vehicle.append(distance_per_vehicle)
            loads_per_vehicle.append(load_per_vehicle)
            bar.next()

    # Return best route
    distances = np.array(distances)
    best_route = routes[np.argmin(distances)]
    best_distances = distances_per_vehicle[np.argmin(distances)]
    best_loads = loads_per_vehicle[np.argmin(distances)]
    
    n_clients = [len(i) - 1 for i in best_route]
    
    return distances, best_route, distances.min(), n_clients, best_distances, best_loads


if __name__ == '__main__':
    max_load = 18
    mileage = 9.52
    all_distances, best_route, distance, n_clients, distance_per_car, load_per_car = test(10)
    load_per_car = [round(load, 2) for load in load_per_car]
    dead_volume = [round(18 - i, 2) for i in load_per_car]
    gas = [round(i / mileage, 2) for i in distance_per_car]
    carbon_footprint = [round(i * 2.3, 3) for i in gas]

    df = pd.DataFrame(list(zip(n_clients, distance_per_car, load_per_car, dead_volume, gas, carbon_footprint)), 
        columns=['N', 'Distancia (km)', 'Carga (m3)', 'Vol. muerto (m3)', 'Gas (l)', 'CO2 (Kg)'])
    df.to_csv('data/processed/best_route.csv', index=False)

    print(f'''Results:
    ----------------------
    {df}''')

    all_distances = np.array(all_distances) / 100
    print(f'''
    ----------------------
    Minimal distance: {all_distances.min():.2f} km
    Mean distance: {all_distances.mean():.2f} km
    Maximal distance: {all_distances.max():.2f} km
    Standard deviation: {all_distances.std():.2f} km
    Variance distance: {all_distances.var():.2f} km
    Carbon footprint: {sum(carbon_footprint):.2f} kg
    ----------------------''')


    visualize_routes(best_route)
