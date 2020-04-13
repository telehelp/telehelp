import geopy.distance


def readZipCodeData(file_name):
    location_dictionary = {}
    district_dictionary = {}
    city_dictionary = {}

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            input = line.split("\t")
            if len(input) > 10:
                zipcode = input[1].replace(" ", "")
                long = input[9]
                lat = input[10]
                longlat = (long, lat)  # as tuple
                location_dictionary[int(zipcode)] = longlat
                district_dictionary[int(zipcode)] = input[3]
                city_dictionary[int(zipcode)] = input[2]

    return location_dictionary, district_dictionary, city_dictionary


# Input: path to zipcode file (e.g. SE.txt)
# Output: list of all unique cities (postort)
def getListOfCities(file_name):
    cities = set()
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            input = line.split()
            if len(input) > 10:
                city = input[3]
                if city not in cities:
                    cities.add(city)
    return cities


# Input: coords1 and coords2 as tuples (lat,long)
# Output: distance between zip code locations in km. Returns -1 if not found
def getDistanceApart(zip1, zip2, location_dict):
    try:
        coords1 = location_dict[int(zip1)]
        coords2 = location_dict[int(zip2)]
    except KeyError:  # One of the provided zip codes is not included in SE.txt
        return -1

    return geopy.distance.distance(coords1, coords2).km


# Input: zip code to look up
# Output: zip code's district, swedish 'län'
def getDistrict(zipcode, district_dict):
    try:
        district = district_dict[zipcode]
    except KeyError:
        return "n/a"
    return district


# Input: zip code to look up
# Output: zip code's city, as string. "Okänd ort" returned if unknown zip
# TODO: city_dictionary.get(int(zipcode), "Okänd ort") ska göra samma sak snyggare
def getCity(zipcode, city_dictionary):
    try:
        city = city_dictionary[int(zipcode)]
    except KeyError:
        return "Okänd ort"
    return city
