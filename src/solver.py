import pandas as pd
import numpy as np
import folium
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def solver() -> (list, int):
    
    routes_taken = []
    load_per_vehicle = []
    distance_per_vehicle = []

    distance_matrix = pd.read_csv('data/processed/distance_matrix.csv').multiply(100).to_numpy().tolist()
    needs = pd.read_csv('data/processed/deliveries-by-address-with-coords.csv').Vol.multiply(100).tolist()
    needs.insert(0, 0)
    

    def create_data_model():
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = distance_matrix
        data['demands'] = needs
        data['vehicle_capacities'] = [18*100 for i in range(9)]
        data['num_vehicles'] = 9
        data['depot'] = 0
        return data


    def print_solution(data, manager, routing, solution):

        """Prints solution on console."""
        print(f'Objective: {solution.ObjectiveValue()}')
        total_distance = 0
        total_load = 0
        route_volume = []

        for vehicle_id in range(data['num_vehicles']):
            temp_vehicle_distance = []
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            route_load = 0
            car_i_route = []
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data['demands'][node_index]
                plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                car_i_route.append(node_index)
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)

            car_i_route.append(0)
            routes_taken.append(car_i_route)
            plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                    route_load / 100)
                                                    
            plan_output += 'Distance of the route: {} km\n'.format(route_distance / 100)
            distance_per_vehicle.append(route_distance / 100)
            load_per_vehicle.append(route_load / 100)
            plan_output += 'Load of the route: {}\n'.format(route_load / 100)
            
            print(plan_output)
            total_distance += route_distance
            total_load += route_load
            route_volume.append(route_load / 100)

        distance_traveled = total_distance
        print('Total distance of all routes: {} km'.format(total_distance / 100))
        print('Total load of all routes: {}'.format(total_load / 100))
        # print(f'Distance per vehicle : {distance_per_vehicle}')
        # print(f'Load per vehicle : {load_per_vehicle}')
        return distance_traveled, total_load, route_volume, distance_per_vehicle, load_per_vehicle
        

    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
                                            demand_callback_index,
                                            0,  # null capacity slack
                                            data['vehicle_capacities'],  # vehicle maximum capacities
                                            True,  # start cumul to zero
                                            'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        distance_traveled, vehicle_load, route_volume, distance_per_vehicle, load_per_vehicle = print_solution(data, manager, routing, solution)
        return routes_taken, distance_traveled, vehicle_load, distance_per_vehicle, load_per_vehicle
    else:
        print('No solution found.')


def visualize_routes(solution: list) -> None:

    np.random.seed(7501)

    deliveries_df = pd.read_csv('data/processed/deliveries-by-address-with-coords.csv')
    cedis_locs = pd.read_csv('data/processed/cedis.csv')
    cedis_locs = cedis_locs[cedis_locs['CEDIS REG'] == 'MONTERREY']
    cedis_loc = cedis_locs['coord1'][0], cedis_locs['coord2'][0]
    cedis_row = pd.DataFrame({'full_address': 'Cedis Monterrey',
                            'Vol': np.nan,
                            'locations': np.nan,
                            'points': np.nan,
                            'latitude':	cedis_loc[0],
                            'longitude': cedis_loc[1],
                            'altitude': 0}, index=[0])
    deliveries_df = pd.concat([cedis_row, deliveries_df], ignore_index=True)
    cedis_locs = cedis_locs[cedis_locs['CEDIS REG'] == 'MONTERREY']
    cedis_location = cedis_locs['coord1'], cedis_locs['coord2']

    # Map generation
    map_ = folium.Map(location=cedis_location, zoom_start=12)

    # Add the specific location of cedis to map_
    folium.Marker(location=cedis_location, popup='Cedis Monterrey', icon=folium.Icon(color='red')).add_to(map_)

    solution_dfs = []
    possible_colors = ['darkblue', 'black', 'green', 'pink', 'cadetblue', 
                        'orange', 'red', 'darkpurple', 'lightgreen', 
                        'darkred', 'blue', 'gray', 'darkgreen']

    colors = np.random.choice(possible_colors, len(solution), replace=False)

    # Adding both delivery points and routes. Every route will receive a different color.
    for sol, color, idx in zip(solution, colors, range(len(solution))):

        route_df = deliveries_df.iloc[sol][['latitude', 'longitude', 'full_address', 'Vol']]
        feature_group = folium.FeatureGroup(name='Route ' + str(idx))

        route_df.apply(lambda row: folium.Marker(
                        location=[row['latitude'], 
                        row['longitude']], popup=row['full_address'] + '\n Volume:' + str(row['Vol']), 
                        icon=folium.Icon(color=color, icon='home')).add_to(feature_group), axis=1)
        
        route_df.drop(['full_address', 'Vol'], axis=1, inplace=True)

        # A column swap must be made. Polyline expects data in lat, long format
        cols = ['latitude', 'longitude']
        route_df = route_df[cols]
        points = route_df.to_numpy().tolist()
        folium.PolyLine(points, color=color).add_to(feature_group)
        feature_group.add_to(map_)

        solution_dfs.append(route_df)

    folium.LayerControl().add_to(map_)

    map_.save('routes.html')
