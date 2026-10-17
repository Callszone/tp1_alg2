import math 

# implementação do haversine para cálculo de distância no geoide terreno (aproximado para esfera)

def dist_haversine(lat1, long1, lat2, long2):
    lat1 = math.radians(lat1)
    long1= math.radians(long1)
    lat2 = math.radians(lat2)
    long2= math.radians(long2)

    R = 6371

    #calculo do a:
    deltalat = lat2 - lat1 
    deltalong = long2 - long1 

    a = (math.sin(deltalat/2)**2) + (math.cos(lat1)*math.cos(lat2)*(math.sin(deltalong/2)**2))
    
    #calculo do c:
    c = 2 * math.atan2((math.sqrt(a)), (math.sqrt(1-a)))

    #calculo do d:
    d = R * c 

    return d


