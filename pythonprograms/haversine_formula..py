# Taken from: https://www.rosettacode.org/wiki/Haversine_formula#Python

from math import radians, sin, cos, sqrt, asin
 
 
def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8  # Earth radius in kilometers
 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
 
    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))
 
    return R * c

import random
random.seed(2938746787236587687345)

n = 1000000
for _ in range(n):
    haversine(random.randint(1,1000000)+random.random(), random.randint(1,1000000)+random.random(), random.randint(1,1000000)+random.random(), random.randint(1,1000000)+random.random())
    

