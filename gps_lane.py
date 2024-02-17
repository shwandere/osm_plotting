
from pyroutelib3 import Router # Import the router
import numpy as np
from scipy.ndimage import gaussian_filter  # this needs to be installed.
import math as m
import matplotlib.pyplot as plt

def revcalcposNED(X, Y, latReference, lonReference):
	global Z
	earthRadius = 6378145.0
	
	X *= 57.3
	Y *= 57.3
	#latReference /=57.3
	#lonReference /=57.3
	posNEDr = np.zeros(3)
	
	lat = latReference + Y/earthRadius
	#lat = latReference + np.arcsin(Z/earthRadius)
	#lon = lonReference + np.arctan2(Y,X)
	lon = lonReference +  (X/(earthRadius*np.cos(latReference)))
	#lat *= 57.3
	#lon *=57.3
	#lon = np.arctan2(Y,X)
	#lat = np.arccos(np.sqrt(np.square(X)+np.square(Y))/earthRadius/1000)
	print(lat)
	print(lon)
	#lat*=57.3
	#lon*=57.3
	return lat, lon

def calcposNED(lat, lon, latReference, lonReference):
	earthRadius = 6378145.0
	lat /= 57.3
	lon /= 57.3
	latReference /= 57.3
	lonReference /= 57.3
	posNEDr = np.zeros(3)
	Y = earthRadius * (lat - latReference)
	X = earthRadius * np.cos(latReference) * (lon - lonReference)
	return X, Y


def find_route(start_lat,start_lon,end_lat,end_lon, home_lat, home_lon):
	#print("form function")
	#print(start_lat)
	#print(start_lon)
	#print(type(start_lat))
	#print(type(start_lon))
	router = Router("car") # Initialise it
	start = router.findNode(start_lat, start_lon) # Find start and end nodes
	end = router.findNode(end_lat, end_lon)

	status, route = router.doRoute(start, end) # Find the route - a list of OSM nodes
	print(status)
	if status == 'success':
		print("found route")
		routeLatLons = list(map(router.nodeLatLon, route)) # Get actual route coordinates
		#print(routeLatLons)
	Y = np.array([i[0] for i in routeLatLons])
	X = np.array([i[1] for i in routeLatLons])
	orig_X, orig_Y = X,Y
	start_Y = Y[0]
	start_X = X[0]

	X, Y = calcposNED(np.copy(Y), np.copy(X),home_lat, home_lon)

	# find mid points between all consecutive points twice, filter(smoothen) and repeat 3 times
	for i in range(10):
		Y = np.dstack((Y[:-1],Y[:-1] + np.diff(Y)/2.0)).ravel()
		Y = np.dstack((Y[:-1],Y[:-1] + np.diff(Y)/2.0)).ravel()
		X = np.dstack((X[:-1],X[:-1] + np.diff(X)/2.0)).ravel()
		X = np.dstack((X[:-1],X[:-1] + np.diff(X)/2.0)).ravel()

		Y = gaussian_filter(Y,sigma=1)
		X = gaussian_filter(X,sigma=1)
	#print("printing return values from found route function")
	#print(X)
	#print(Y)
	return orig_X, orig_Y
	#return X,Y
