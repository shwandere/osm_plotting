import osmnx as ox 
#import geopandas as gpd
#from pyroutelib3 import Router
from pyrosm import OSM,get_data
import networkx as nx
import geopandas as gpd
import pandas as pd
from sklearn.neighbors import BallTree
import numpy as np
import mapclassify as mc
import matplotlib.pyplot as plt
import time
import networkx as nx
import igraph as ig 
import osmnx as ox
import folium
import pyrosm




place_name = 'Delhi'

start_lat = 28.553749
start_lon = 77.169316
end_lat = 28.5462837
end_lon = 77.186491

'''
def find_route():
    router = Router("car") # Initialise it
    start = router.findNode(start_lat, start_lon)
    end = router.findNode(end_lat, end_lon)
    status, route = router.doRoute(start, end) # Find the route - a list of OSM nod
    print("status of path found is "+str(status))
    routeLatLons = list(map(router.nodeLatLon, route)) # Get actual route coordinates
    return routeLatLons


def plot_route():
    #get place boundary of place_names as a geodataframe
    route_list = find_route()
    area = ox.geocode_to_gdf(place_name)
    print(type(area))
    ox.plot_graph(area)
    #edge_lengths = ox.utils_graph.get_route_edge_attributes(graph_type[go_type], route, 'length') 
    #edge_travel_time = ox.utils_graph.get_route_edge_attributes( graph_type[go_type], route, 'travel_time') 
    #total_route_length = round(sum(edge_lengths), 1)
    #route_travel_time  = round(sum(edge_travel_time)/60, 2)
    #if plot:
        #ox.plot_graph_route(graph_type[go_type], route, node_size=0, figsize=(40,40))
    #print(route_list)
    #ox.plot_graph_routes(area,route_list)

    #return route, total_route_length, route_travel_time
'''
#OSM()
osm = OSM('delhi-latest.osm.pbf')
print('osm type:',type(osm))
graph_type = {}
#print(osm)
#print(osm.get_boundaries())

n_drive, e_drive = osm.get_network(nodes = True,network_type="driving")
#print(n_drive)
#print(e_drive)
#n_cycling, e_cycling   = osm.get_network(nodes=True, network_type="cycling")
#n_walk,   e_walk       = osm.get_network(nodes=True, network_type="walking")
#n_service, e_service   = osm.get_network(nodes=True, network_type="driving+service")

graph_type['drive']     = ox.add_edge_travel_times(ox.add_edge_speeds(osm.to_graph(n_drive, e_drive)))#, extra_kwargs={"hv":{"car":120}})
#graph_type['walk']   = ox.add_edge_travel_times(ox.add_edge_speeds(osm.to_graph(n_walk, e_walk, graph_type="networkx")))
#graph_type['cycle']   = ox.add_edge_travel_times(ox.add_edge_speeds(osm.to_graph(n_cycling, e_cycling, graph_type="networkx")))
#graph_type['service']   = ox.add_edge_travel_times(ox.add_edge_speeds(osm.to_graph(n_service, e_service, graph_type="networkx")))



def get_route(source_geo, dest_geo, go_type='drive', weight='travel_time',plot=True):
    source_node = ox.get_nearest_node(graph_type[go_type], source_geo)
    target_node = ox.get_nearest_node(graph_type[go_type], dest_geo)
    
    route = nx.shortest_path(graph_type[go_type], source_node, target_node, weight=weight)
    ox.utils_graph.get_nearest_node
    edge_lengths = ox.utils_graph.get_route_edge_attributes(graph_type[go_type], route, 'length') 
    edge_travel_time = ox.utils_graph.get_route_edge_attributes( graph_type[go_type], route, 'travel_time') 
    total_route_length = round(sum(edge_lengths), 1)
    route_travel_time  = round(sum(edge_travel_time)/60, 2)
    if plot:
      ox.plot_graph_route(graph_type[go_type], route, node_size=0, figsize=(40,40))
    return route, total_route_length, route_travel_time

if __name__ == '__main__':
    start_pos = (start_lat,start_lon)
    end_pos = (end_lat,end_lon)
    travel_route, travel_length, travel_time = get_route(start_pos,end_pos)
    print("travel length from munirka to IIT delhi is "+ str(travel_length))
    print("travel time from munirka to IIT delhi is "+ str(travel_time))
    
#osm2 = OSM("iitd_map.osm")
#print(type(osm2))