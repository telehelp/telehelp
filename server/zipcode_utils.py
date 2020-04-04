import geopy.distance

def readZipCodeData():
	file_name = 'SE.txt'
	zip_dictionary = {}

	with open(file_name, 'r', encoding='utf-8') as file:
		for line in file:
			input = line.split()
			if len(input)>10:
				zip = input[1]+input[2]
				long = input[8]
				lat = input[9]
				longlat = (long, lat) # as tuple
				zip_dictionary[int(zip)] = longlat
	return zip_dictionary

#Input: coords1 and coords2 as tuples (lat,long)
#Output: distance between zip code locations in km
def getDistanceApart(zip1, zip2):
	zip_dict = readZipCodeData()
	coords1 = zip_dict[zip1]
	coords2 = zip_dict[zip2]
	return geopy.distance.vincenty(coords1, coords2).km

if __name__ == "__main__":
	print(getDistanceApart(17070, 74693))
