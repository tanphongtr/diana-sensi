# import geopy.distance

# coords_1 = (52.2296756, 21.0122287)
# coords_2 = (52.406374, 16.9251681)

# print ( type(geopy.distance.geodesic(coords_1, coords_2).km) )


# import requests
# orig_coord = '18.997739', '72.841280'
# dest_coord = '8.880253', '72.945137'

# url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))

# print(requests.get(url=url).json())


# import googlemaps
# from datetime import datetime

# gmaps = googlemaps.Client(key='AIzaSyAG3A5LS7uZOyxqkNOW_GYEE8gDJ0N4c-8')


# now = datetime.now()
# directions_result = gmaps.directions("18.997739, 72.841280",
#                                      "18.880253, 72.945137",
#                                      mode="driving",
#                                      avoid="ferries",
#                                      departure_time=now
#                                      )

# print(directions_result[0]['legs'][0]['distance']['text'])
# print(directions_result[0]['legs'][0]['duration']['text'])









from geopy import distance

s = {
    977: (23.141747, 53.796469),
    # 946: (23.398398, 55.422916),
    # etc etc
}

d = {
    962: (23.657571, 53.703683),
    745: (23.671971, 52.955976),
    743: (23.766849, 53.770344),
    # etc etc
}

for (ss, a) in s.items():
    best = None
    dist = None
    for (dd, b) in d.items():
        km = distance.distance(a, b).km
        if dist is None or km < dist:
            best = dd
            dist = km

    print(f'{ss} is nearest {best}: {dist} km')