#divisão de intervalos

def geohash_encode(lat,long,precisao):
    alfa_b32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    #alfa_b32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    intervalo_lat = [-90, 90]
    intervalo_long = [-180, 180]
   
    geohash = ""

    turno = False # 0 para long e 1 para lat
    mi = 0
    buffer = ""
    
    # dado uma latitude e longitude gero a string binária que codifica o geohash
    for _ in range(5*precisao): 
        
        #construo os bits:

        #lat
        if (turno):
           mi = (intervalo_lat[0] + intervalo_lat[1])/2
           if(lat >= mi):
                buffer = buffer + "1"
                intervalo_lat = [mi, intervalo_lat[1]]
           else: 
                buffer = buffer + "0"
                intervalo_lat = [intervalo_lat[0], mi]

        #long
        else:
            mi = (intervalo_long[0] + intervalo_long[1]) / 2 
            if(long >= mi):
                buffer = buffer + "1"
                intervalo_long = [mi, intervalo_long[1]]
            else:
                buffer = buffer + "0"
                intervalo_long = [intervalo_long[0], mi]

        # verifico o tamanho do buffer
        if(len(buffer) == 5):
            x = int(buffer, 2)
            geohash = geohash + alfa_b32[x]
            buffer = ""


        turno = not turno 

    return geohash


def geohash_box(s):
    alfa_b32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    #alfa_b32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    intervalo_lat = [-90, 90]
    intervalo_long = [-180, 180]
   
    turno = False # 0 para long e 1 para lat
    mi = 0
    

    for ch in s:
        i = alfa_b32.index(ch)
        convert = f"{i:05b}"
        
        for b in convert:
            if(turno):
                mi = (intervalo_lat[0] + intervalo_lat[1])/2
                if(b == "1"):
                    intervalo_lat = [mi, intervalo_lat[1]]
                else:
                    intervalo_lat = [intervalo_lat[0], mi]
            else:
                mi = (intervalo_long[0] + intervalo_long[1])/2
                if(b == "1"):
                    intervalo_long= [mi, intervalo_long[1]]
                else:
                    intervalo_long = [intervalo_long[0], mi]
            turno = not turno 

    lat_centro = (intervalo_lat[0] + intervalo_lat[1])/2
    long_centro = (intervalo_long[0] + intervalo_long[1])/2 

    centro_da_box = [lat_centro, long_centro]

    return (centro_da_box, intervalo_lat, intervalo_long)

def geohash_grid(s):

    base = geohash_box(s)

    precisao = len(s) 
    centro = base[0]

    lat_centro = centro[0]
    long_centro = centro[1]

    intervalo_lat = base[1]
    intervalo_long = base[2]
    
    h = intervalo_lat[1] - intervalo_lat[0]
    w = intervalo_long[1] - intervalo_long[0]
    
    norte = [(lat_centro + h), long_centro]
    sul = [(lat_centro - h), long_centro]
    leste = [lat_centro, (long_centro + w)]
    oeste = [lat_centro, (long_centro - w)]
    
    nordeste = [(lat_centro + h), (long_centro + w)]
    noroeste = [(lat_centro + h), (long_centro - w)]
    sudeste = [(lat_centro - h), (long_centro + w)]
    sudoeste = [(lat_centro - h), (long_centro - w)]

    alvo = {"c": s, "n": geohash_encode(norte[0], norte[1], precisao), "s": geohash_encode(sul[0], sul[1], precisao), "e": geohash_encode(leste[0],leste[1], precisao), 
            "w": geohash_encode(oeste[0], oeste[1], precisao), "ne": geohash_encode(nordeste[0], nordeste[1], precisao), "nw": geohash_encode(noroeste[0], noroeste[1],precisao),
           "se": geohash_encode(sudeste[0], sudeste[1], precisao), "sw": geohash_encode(sudoeste[0], sudoeste[1], precisao)
           }

    return alvo 


print("-19.869, -43.963")
teste1  = geohash_encode(-19.869, -43.963, 8)
print(teste1)
print(len(teste1))

teste2 = geohash_box(teste1)
print(teste2)

    
