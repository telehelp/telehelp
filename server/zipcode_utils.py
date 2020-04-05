import geopy.distance

def readZipCodeData(file_name):
	location_dictionary = {}
	district_dictionary = {}

	with open(file_name, 'r', encoding='utf-8') as file:
		for line in file:
			input = line.split()
			if len(input)>10:
				zip = input[1]+input[2]
				long = input[8]
				lat = input[9]
				longlat = (long, lat) # as tuple
				location_dictionary[int(zip)] = longlat
				district_dictionary[int(zip)] = input[4]

	return location_dictionary, district_dictionary

#Input: coords1 and coords2 as tuples (lat,long)
#Output: distance between zip code locations in km. Returns -1 if not found
def getDistanceApart(zip1, zip2, location_dict):
	try:
		coords1 = location_dict[int(zip1)]
		coords2 = location_dict[int(zip2)]
	except KeyError: # One of the provided zip codes is not included in SE.txt
		return -1

	return geopy.distance.distance(coords1, coords2).km

# Input: zip code to look up
# Output: zip code's district, swedish 'län'
def getDistrict(zip, district_dict):
	try:
		district = district_dict[zip]
	except KeyError:
		return "n/a"
	return district

# Input: zip code to look up
# Output: zip code's location, as latlong. (0, 0) returned if position is unknown
def getLatLong(zip):
	try:
		latlong = location_dictionary[int(zip)]
	except KeyError:
		return (0, 0)

	return latlong
