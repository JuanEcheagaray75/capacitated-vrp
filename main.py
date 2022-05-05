from src.solver import solver, visualize_routes
import numpy as np


def test(n):

    distances = []
    routes = []

    for i in range(n):
        print('-----------------')
        route, distance = solver()
        distances.append(distance)
        routes.append(route)
        print(f'Distance_traveled: {distance}')

    # Return best route
    distances = np.array(distances)
    best_route = routes[np.argmin(distances)]
    
    n_clients = [len(i) - 1 for i in best_route]
    
    return best_route, distances.min(), n_clients


if __name__ == '__main__':
    best_route, distance, n_clients = test(10)
    print(f'Minimal distance: {distance / 100}')

    for i in range(len(best_route)):
        print(f'Car {i}: {n_clients[i]}')

    visualize_routes(best_route)
