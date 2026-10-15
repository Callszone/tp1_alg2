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
        # verifico o tamanho do buffer
        if(len(buffer) == 5):
            x = int(buffer, 2)
            geohash = geohash + alfa_b32[x]
            buffer = ""


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
        
        turno = not turno 

    return geohash

teste  = geohash_encode(-19.869, -43.963, 8)
print(teste)
    
