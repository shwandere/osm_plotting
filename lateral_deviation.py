from osm_file_reading import OSMHandler
import numpy as np
import pandas as pd
from gps_lane import calcposNED,revcalcposNED
import pickle 
import matplotlib.pyplot as plt
import folium 
import math
nodes_list = []
initial_node = ()
node_initialization = False
all_perpen_dist = []
reference_point = ()
#def line_finding(p1,p2):
    #x = (p1[0],p2[0])
    #y = (p1[1],p2[1])
    #line_coef = np.polyfit(x,y,1)
    #return line_coef



def perpendicular_distance_finding(p1,p2,p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    print("p1,p2,p3,d")
    print(p1)
    print(p2)
    print(p3)
    d = np.cross((p2-p1),(p3-p1))/np.linalg.norm(p2-p1)
    print(d)
    return d

def closest_node_finding(gps,nodes):
    global node_initialization
    global initial_node
    dist = [] 
    for i in range(len(nodes)):
        temp = np.array(nodes[i])
        gps = np.array(gps)
        d = np.abs(np.linalg.norm(temp-gps))
        dist.append(d)
    
    pos = np.where(dist==np.min(dist))
    pos = pos[0]
    print(node_initialization)
    if(node_initialization == False):
        
        initial_node = nodes[pos[0]]
        print(initial_node)
        #node_initialization = True
    print("returned value from closest node finding")
    print(nodes[pos[0]])
    return nodes[pos[0]]

def plot_final_nodes(worldframe_xy,indices):

    temp_x = [a for a,b in worldframe_xy]
    temp_y = [b for a,b in worldframe_xy]
    x = temp_y
    y = temp_x
    #print(indices)
    #for i in indices:
        #x.append(temp_x[i])
        #y.append(temp_y[i])
    print(len(x))
    print(len(y))
    
    output_file = "JOSM_plotted.html"
    temp = ()
    lat = []
    lon = []
    for i,j in zip(x,y):
        temp = revcalcposNED(i,j,reference_point[0],reference_point[1])
        lat.append(temp[0])
        lon.append(temp[1])
    center = (np.mean(lat), np.mean(lon))
    m = folium.Map(center, zoom_start=26, tiles="OpenStreetMap")
    for pt in zip(lat,lon): 
        folium.Circle([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),radius = 1,color = 'orange',fill = False,fill_color = 'orange').add_to(m)
    m.save(output_file)

def plot_perp_dist_graph(values):
    waypoints_index = []
    print("final values")
    print(len(values))
    filter_values = []
    for i in range(len(values)):
        na = float("nan")
        if (not math.isnan(values[i])):
            waypoints_index.append(i)
            filter_values.append(values[i])
    #fig, ax = plt.plot()
    print(filter_values)
    print(len(filter_values))
    plt.plot(filter_values,color=((255,0,100)))
    #plt.show()
    plt.ylim(-20,20)
    plt.xlabel("GPS waypoints count from initial position")
    plt.ylabel("lateral deviation(in meters)")
    plt.savefig("lateral_deviation_plot_data2_gps_waypoints.jpg")
    return waypoints_index

'''

#reading osm file 
osmhandler = OSMHandler()
osmhandler.apply_file("IITD_roads2.osm") #special for 29 -> IITD_roads_29
data_colnames = ['type', 'id', 'visible', 'lat', 'lon']
df_osm = pd.DataFrame(osmhandler.osm_data, columns=data_colnames)
lat_osm_list = df_osm['lat']
lon_osm_list = df_osm['lon']

reference_point = (lat_osm_list[0],lon_osm_list[0])
node_xw,node_yw = calcposNED(lat_osm_list,lon_osm_list,reference_point[0],reference_point[1])

#reading gps waypoint file
gps_waypoints_list = []

#waypoint_file_name = "navsatfix_waypoints3_subset_mavros_all_data2"

#with open(waypoint_file_name,"rb") as fb:
    #gps_waypoints_list = pickle.load(fb)
#56 is txt
#29 is pickle
#data1,data2 are pickle
waypoint_file_name = "navsatfix_waypoints4_subset_mavros_all_data1"
#waypoint_file_name = "navsatfix_waypoints2_29"

with open(waypoint_file_name,"rb") as fb:
    t = pickle.load(fb)
    print(t)
    print(len(t))
    #input()
    #gps_waypoints_list.extend(t)
    gps_waypoints_list = t
    print(gps_waypoints_list)
    input()
#waypoint_file_name = 'navsatfix_waypoints_with_timestamp_56.txt'
#with open(waypoint_file_name,'r') as f:
    #for lines in f.readlines():
        #print(lines)
        #a,b,c = lines.split()
        #gps_waypoints_list.append((float(a),float(b)))
        #gps_waypoints_list.append((float(a),float(b)))
#gps_waypoints_list.sort()
print("gps and nodes len")
print(len(gps_waypoints_list))
print(len(node_xw))
#gps_lat_list = [a for a,b in gps_waypoints_list]#gps_waypoints_list[:][0]
#gps_lon_list = [b for a,b in gps_waypoints_list]#gps_waypoints_list[:][1]

#gps_xw,gps_yw = calcposNED(gps_lat_list,gps_lon_list,reference_point[0],re#ference_point[1])

nodes_points = [(a,b) for a,b in zip(node_xw,node_yw)]
finalized_node_points = [] 
for lat,lon in gps_waypoints_list:
    x,y = calcposNED(lat,lon,reference_point[0],reference_point[1])
    gps_point = (x,y)

    closest_node = closest_node_finding(gps_point,nodes_points)
    if (node_initialization == False):
        check_node = initial_node
        line_node = check_node
        node_initialization = True
        #check_node = initial_node#closest_node_finding(gps_point,nodes_points)
        #line_node = check_node

    print(check_node)
    print(closest_node)
    print(check_node[0]!=closest_node[0])
    print(check_node[1]!=closest_node[1])
    
    if (check_node[0]!=closest_node[0] and check_node[1]!=closest_node[1]):
        #if (node_initialization==False):
            #print("node initialized")
            #node_initialization = True
    
        line_node = check_node
        check_node = closest_node
        finalized_node_points.append(check_node)
    
    dist = perpendicular_distance_finding(line_node, closest_node, gps_point)
    if (node_initialization==False):
        all_perpen_dist.append(0)
    else  :
        all_perpen_dist.append(dist) 
    

useful_index = plot_perp_dist_graph(all_perpen_dist)
plot_final_nodes(finalized_node_points,useful_index)
'''

