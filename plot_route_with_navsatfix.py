import pickle
import folium 
import osmnx as ox
import networkx as nx
import selenium.webdriver
import time
import os
from geopy.distance import geodesic
import numpy as np
import matplotlib.pyplot as plt
from ipyleaflet import AntPath
from pyroutelib3 import Router
output_file = "map_plot.html"
folder_url="file:///home/dell/lane_detection/BTP_shubh_debo_lane_detection_github/osm_lat_log_error/code/"
map_url = folder_url+output_file

#map_vector = folium
waypoint_file_name = "navsatfix_waypoints4_subset_mavros_all_data1"
tomtom_waypoint_file_name = "Baba Ganganath Marg - South Avenue.txt" 
with open(waypoint_file_name,"rb") as fb:
    waypoints_list = pickle.load(fb)

print(waypoints_list)
#input()
print("intial number of waypoints")
print(len(waypoints_list))
input()
itineraire = []
itineraire.append(waypoints_list[0])
count = 0

############# filtering the points according to the distance between them #### 
diff_x = max([b-a for a,b in zip(waypoints_list[:][0],waypoints_list[1:][0])])
diff_y = max([b-a for a,b in zip(waypoints_list[:][1],waypoints_list[1:][1])])
diff = max(diff_x,diff_y)
print('diff')
print(diff)
for i in waypoints_list[1:]:
    temp = itineraire[count]
    print(i)
    print(temp)
    if (i[0]<temp[0]+120*diff and i[1]<temp[1]+120*diff):
        continue
    else:
        itineraire.append(i)
        count = count + 1
print("after filtering")
print(count)

center = (np.mean([a for a,b in itineraire]), np.mean([b for a,b in itineraire]))

itin = itineraire
# create graph
G = ox.graph_from_point(itin[0],network_type='walk')
#print("G nodes")
#print(G.nodes)
#print(G.edges)
# create the path
#path = []

print("itin")
print(itin) 
print("itin1")
print(itin[1:])
first = itin[0]
second = itin[len(itin)-1]
#first = (28.54504,77.18327)
#second = (28.54495,77.1946)
print(first)
print(second)
one = ox.nearest_nodes(G,first[1],first[0])
two = ox.nearest_nodes(G,second[1],second[0])


#ox.nearest_nodes
print(one)
print(two)
print(G.nodes())
#path= nx.(G,one,two)

if (one == two) :

    nodes = nx.all_neighbors(G,one)
    route = []
    for i in list(nodes):
        route.append(nx.shortest_path(G,i,one))
#print (list(route))
print("path")
#print(path)
#path = []
prev_node = 0

'''
for i in itin:
    print(i)
    node = ox.nearest_nodes(G,i[1],i[0])    
    if (node==prev_node):
        continue
    path.append(node)
    prev_node = node
print(path)
'''
#plt, axs = ox.plot_graph_route(G,path)
#plt.show()


#single_path = path[0]
#[[1261505524], [1261505524, 1261505525, 456520278], [456520278, 1261505525, 4237637413, 5549684249], [5549684249, 4237637412], [4237637412, 4237637410], [4237637410, 460438855], [460438855, 456520295], [456520295, 1261505504]]
# plot the graph in the form of folium map 

#fig = folium.Figure(width=1000,height=1000)
m = folium.Map(center, zoom_start=26, tiles="OpenStreetMap")
#m = ox.plot_graph_folium(G,m)#,edge_color='k', bgcolor='w')

#route1 = ox.plot_route_folium(G,route[0])
#route1.add_to(m)
#m = ox.plot_graph_route()

for pt in itineraire: 
    #marker = folium.Marker([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),icon=folium.Icon(color='red')) #latitude,longitude
    #print("adding child")
    #marker.add_to(map)
    #map.add_child(marker)
    folium.Circle([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),radius = 1,color = 'orange',fill = False,fill_color = 'orange').add_to(m)


'''
router = Router("foot") # Initialise it
#Router
start = router.findNode(first[0], first[1]) # Find start and end nodes
end = router.findNode(second_pickup1[0], second_pickup1[1])

status, route = router.doRoute(end, start) # Find the route - a list of OSM nodes
print(status)
if status == 'success':
    print("found route")
    print(route)
    routeLatLons = list(map(router.nodeLatLon, route)) # Get actual route coordinates
    print(routeLatLons)

#repeat the same process of route points finding 3 times more
start = router.findNode(second_pickup2[0], second_pickup2[1]) # Find start and end nodes
end = router.findNode(second_pickup1[0], second_pickup1[1])

status, route = router.doRoute(end, start) # Find the route - a list of OSM nodes
print(status)
if status == 'success':
    print("found route")
    print(route)
    routeLatLons2 = list(map(router.nodeLatLon, route)) # Get actual route coordinates
    print(routeLatLons2)

for i in routeLatLons2:
    routeLatLons.append(i)


newroute = routeLatLons

for i in range(len(newroute)-1):
    print(i)
    first2 = newroute[i]
    second2 = newroute[i+1]
    start2 = router.findNode(first2[0], first2[1]) # Find start and end nodes
    end2 = router.findNode(second2[0], second2[1])
    status, route = router.doRoute(start2, end2) # Find the route - a list of OSM nodes

    print(status)
    if status == 'success':
        print("found between route")
        print(route)
        routeLatLons2 = list(map(router.nodeLatLon, route)) # Get actual route coordinates
        print(routeLatLons2)
    for i in routeLatLons2:
        routeLatLons.append(i)
print (routeLatLons)
'''

tomtom_waypoint_file_name = "Baba Ganganath Marg - South Avenue.txt" 
routeLatLons = []
with open(tomtom_waypoint_file_name,"r") as fb:

    tags = fb.readline().split('\t')
    for i in fb.readlines():
        values = i.split('\t')
        if (values[0] == 'T'):
            routeLatLons.append((float(values[1]),float(values[2])))

print("routeLatLons")
print(routeLatLons)
for pt in routeLatLons: 
    #marker = folium.Marker([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),icon=folium.Icon(color='red')) #latitude,longitude
    print("adding child")
    #marker.add_to(m)
    #m.add_child(marker)
    folium.Circle([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),radius = 1,color = 'red',fill = False,fill_color = 'red').add_to(m)


m.save(output_file)

driver = selenium.webdriver.Firefox()
driver.set_window_size(1000,1000)
driver.get(map_url)
time.sleep(15)
png_file_name = "plot_route"+waypoint_file_name+'.png' 
driver.save_screenshot(png_file_name)
