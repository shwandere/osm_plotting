import folium 
import selenium.webdriver
import osmnx as ox
import networkx as nx
import pickle
import numpy as np 
import time
import math
import matplotlib.pyplot as plt
from pyroutelib3 import Router
from sklearn.metrics import mean_squared_error

#waypoint calculation and plotting 
#waypoint_file_name = "Aruna_Asaf_Ali_Marg_to_Aruna_Asaf_Ali_Marg.txt"
#navsatfix_file_name = "navsatfix_waypoints_with_timestamp_mavros_data1.txt"

waypoint_file_name = "South_Avenue_56.txt"
navsatfix_file_name = "navsatfix_waypoints_with_timestamp_56.txt"
saved_new_waypoint_file_name = "New_South_Avenue_56.txt"
map_file_name = waypoint_file_name+'_'+navsatfix_file_name+'_map_plot.html'


output_file = map_file_name
folder_url="file:///home/dell/lane_detection/BTP_shubh_debo_lane_detection_github/osm_lat_log_error/code/"
map_url = folder_url+output_file


with open(waypoint_file_name,'r') as fb:
    read_list = fb.readlines()

new_ = []
waypoints_list = []
itineraire = []
timestamps = []



for i in range(0,len(read_list)):
    str_list = read_list[i].split('\t')
    #timestamps.append(int(str_list[2]))
    print (str_list)
    if (str_list[0] == 'T' and str_list[5]=='\n'):
        waypoints_list.append((float(str_list[1]),float(str_list[2])))



with open(navsatfix_file_name,'r') as fb:
    read_list = fb.readlines()

for i in range(0,len(read_list)):
    str_list = read_list[i].split('\t')
    #timestamps.append(int(str_list[2]))
    
    itineraire.append((float(str_list[0]),float(str_list[1])))
    #input()
    #print(itineraire)
    #input()


radius = 6371; ''' earth's mean radius in km '''

''' Helper function to convert degrees to radians '''
def DegToRad(deg) :
    return (deg * math.pi / 180)

''' Helper function to convert radians to degrees '''
def RadToDeg(rad):
    return (rad * 180 / math.pi)

''' Calculate the (initial) bearing between two points, in degrees '''
def CalculateBearing(startPoint, endPoint) :

    lat1 = DegToRad(startPoint[0]) #starting point latitude
    lat2 = DegToRad(endPoint[0]) #starting point longitude
    deltaLon = DegToRad(endPoint[1] - startPoint[1])

    y = math.sin(deltaLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(deltaLon)
    bearing = math.atan2(y, x)

    ''' since atan2 returns a value between -180 and +180, we need to convert it to 0 - 360 degrees '''
    return (RadToDeg(bearing) + 360) % 360


''' Calculate the destination point from given point having travelled the given distance (in km), on the given initial bearing (bearing may vary before destination is reached) '''
def CalculateDestinationLocation(point, bearing, distance):

    '''convert to angular distance in radians'''
    distance = distance / radius / 2
    '''convert bearing in degrees to radians'''
    bearing = DegToRad(bearing)

    lat1 = DegToRad(point[0]) #latitude
    lon1 = DegToRad(point[1]) #longitude

    lat2 = math.asin(math.sin(lat1) * math.cos(distance) + math.cos(lat1) * math.sin(distance) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance) * math.cos(lat1), math.cos(distance) - math.sin(lat1) * math.sin(lat2))
    ''' normalize to -180 - + 180 degrees'''
    lon2 = (lon2 + 3 * math.pi) % (2 * math.pi) - math.pi 

    return (RadToDeg(lat2), RadToDeg(lon2))

''' Calculate the distance between two points in km '''
def CalculateDistanceBetweenLocations(startPoint, endPoint) :

    lat1 = DegToRad(startPoint[0])
    lon1 = DegToRad(startPoint[1])

    lat2 = DegToRad(endPoint[0])
    lon2 = DegToRad(endPoint[1])

    deltaLat = lat2 - lat1
    deltaLon = lon2 - lon1

    a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(deltaLon / 2) * math.sin(deltaLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return (radius * c)

locations = []



'''assuming duration in full seconds'''
print(math.pi)

#input()
#bearings_python = []


bearings_python = []
bearings_waypoint = []

def func(startLocation,endLocation):
    #global bearings_python
    # duration is used, instead of I have no. of lat, lon points 
        
    #print(waypoints_list[i])
    #print(math.pi)

    #bearings = []
    bearing = CalculateBearing(startLocation, endLocation)
    #bearings_python.append(bearing)
    print(startLocation)
    print(bearing)
    print(endLocation)
    #input()
    distanceInKm = CalculateDistanceBetweenLocations(startLocation,endLocation)#v / 1000

    intermediaryLocation = CalculateDestinationLocation(startLocation, bearing, distanceInKm)

    '''add intermediary location to list'''
    
    locations.append(intermediaryLocation)
    
    #print(distanceInKm)
    #print(intermediaryLocation)
    #print(waypoints_list[i+1])
    dist1 = CalculateDistanceBetweenLocations(startLocation,intermediaryLocation)
    dist2 = CalculateDistanceBetweenLocations(intermediaryLocation,endLocation)
    if (dist1>0.00055):
        func(startLocation,intermediaryLocation)
    if (dist2>0.00055):
        func(intermediaryLocation,endLocation)
    '''set intermediary location as new starting location'''
    #startLocation = intermediaryLocation
    locations.append(waypoints_list[i+1])
    #distanceBetweenPoints = CalculateDistanceBetweenLocations(startPoint, endPoint) * 1000; '''multiply by 1000 to get meters instead of km'''
    #timeRequired = distanceBetweenPoints / v;

locations.append(waypoints_list[0])

for i in range(0,len(waypoints_list)-1):
    startLocation = waypoints_list[i]
    endLocation = waypoints_list[i+1]
    func(startLocation,endLocation)

for i in range(0,len(locations)-1):
    startLocation = locations[i]
    endLocation = locations[i+1]
    bearings_python.append(CalculateBearing(startLocation,endLocation))
    print(startLocation)
    print(endLocation)
    print(CalculateBearing(startLocation,endLocation))
    #input()

print("intial number of waypoints")
print(len(waypoints_list))
#input()
itin = []
itin.append(itineraire[0])
count = 0

############# filtering the points according to the distance between them #### 
diff_x = max([b-a for a,b in zip(itineraire[:][0],itineraire[1:][0])])
diff_y = max([b-a for a,b in zip(itineraire[:][1],itineraire[1:][1])])
diff = max(diff_x,diff_y)
print('diff')
print(diff)
for i in itineraire[1:]:
    temp = itineraire[count]
    print(i)
    print(temp)
    if (i[0]<temp[0]+100*diff and i[1]<temp[1]+100*diff):
        continue
    else:
        itin.append(i)
        count = count + 1
print("after filtering")
print(count)
'''
for i in range(0,len(itin)-1):
    startLocation = itin[i]
    endLocation = itin[i+1]
    bearings_waypoint.append(CalculateBearing(startLocation,endLocation))
    
lon_min = 0
lon_max = 0
count_python = len(locations) 
lon_min = locations[0][1]
lon_max = locations[0][1]
deviation = []
print(len(locations))
print(len(itin))
for i in range(0,len(itin)-1):
    delta_lon = locations[i][1] - itin[i][1]
    delta_lat = locations[i][0] - itin[i][0]
    dev = delta_lat**2 + delta_lon**2
    dev = math.sqrt(dev)
    deviation.append(dev)

    
#lon_min = lon_min
#lon_max = lon_max
center_road = (lon_max+lon_min)/2
delta_lon = []
lon = []
avg = np.average(locations)/locations[0]
lon_max = lon_min + avg
for i in range(0,len(itin)-2):
    difference = itin[i+1][1]-itin[i][1]
    lon.append(difference)

#delta_lon = mean_squared_error(itin[:][1],locations[1:len(itin)-1][1]
for a in lon:
    if (a!=0):
        delta_lon.append(a)


fig, ax = plt.subplots()
plt.hlines(lon_max,0,len(itin))
plt.hlines(lon_min,0,len(itin))
#ax.hlines(lon_min,0,100)
#ax.hlines(delta_lon,0,len(itin))
print(deviation)
plt.plot(delta_lon)
plt.show()


#print(waypoints_list)
#input()
print("navsatfix waypoints")
print(len(itin))
#print(itineraire)

print("python waypoints")
print(len(locations))

'''
#input()

#write the new waypoints in the file new waypoints stored in location named list
with open(saved_new_waypoint_file_name,'w') as f:
    for tup in locations:
        print(tup)
        f.write(str(tup[0]))
        f.write('\t')
        f.write(str(tup[1]))
        f.write('\n')

#fig, ax = plt.subplots()
#plt.plot(bearings_python,label='python waypoints')
#plt.plot(bearings_waypoint, label='navsatfix_waypoints')
#plt.show()




#print(locations)

#center = (np.mean([a for a,b in locations]), np.mean([b for a,b in locations]))

##############################################################################


# change to latitude, longitude order

center = (np.mean([a for a,b in locations]), np.mean([b for a,b in locations]))
map = folium.Map(center, zoom_start=26, tiles="OpenStreetMap")
print('itineraire')
print(itineraire)
#for pt in itineraire: 
    #folium.Circle([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),radius = 1,color = 'orange',fill = True,fill_color = 'orange').add_to(map)

for pt in locations: 
    print(pt)
    folium.Circle([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),radius = 2,color = 'red',fill = False,fill_color = 'red').add_to(map)

for pt in itineraire: 
    print(pt)
    folium.Circle([pt[0], pt[1]],popup=folium.Popup(output_file,parse_html=True),radius = 0.5,color = 'orange',fill = False,fill_color = 'orange').add_to(map)

map.save(map_file_name)

driver = selenium.webdriver.Firefox()
driver.set_window_size(1000,1000)
driver.get(map_url)
time.sleep(5)
png_file_name = "map_plot"+waypoint_file_name+'.png' 
driver.save_screenshot(png_file_name)