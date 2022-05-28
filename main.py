from src.solver import solver, visualize_routes
import numpy as np
import pandas as pd


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

    for i in range(n):
        print('-----------------')
        route, distance, total_load, distance_per_vehicle, load_per_vehicle = solver()
        distances.append(distance)
        routes.append(route)
        distances_per_vehicle.append(distance_per_vehicle)
        loads_per_vehicle.append(load_per_vehicle)

    # Return best route
    distances = np.array(distances)
    best_route = routes[np.argmin(distances)]
    best_distances = distances_per_vehicle[np.argmin(distances)]
    best_loads = loads_per_vehicle[np.argmin(distances)]
    
    n_clients = [len(i) - 1 for i in best_route]
    
    return best_route, distances.min(), n_clients, best_distances, best_loads


if __name__ == '__main__':
    best_route, distance, n_clients, distance_per_car, load_per_car = test(10)
    dead_volume = [18 - i for i in load_per_car]
    print(f'''
    ----------------------
    Minimal distance: {distance / 100} km''')

    df = pd.DataFrame(list(zip(n_clients, distance_per_car, load_per_car, dead_volume)), 
        columns=['n_clients', 'distance (km)', 'load (m3)', 'wasted vol (m3)'])
    df.to_csv('data/processed/best_route.csv', index=False)

    print(f'''
    Summary:
    {df}''')


    visualize_routes(best_route)
