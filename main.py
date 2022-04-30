from src.solver import solver, visualize_routes
import numpy as np


def test(n):

    distances = []
    routes = []

    for i in range(n):
        route, distance = solver()
        distances.append(distance)
        routes.append(route)
        print(distance)

    # Return best route
    distances = np.array(distances)
    best_route = routes[np.argmin(distances)]
    
    return best_route, distances.min()


if __name__ == '__main__':
    best_route, distance = test(10)
    print('Minimal distance:', distance / 100)
    visualize_routes(best_route)
