# implementação da função de consulta geral

from core.geohash import geohash_encode, geohash_grid
from core.trie import compact_trie
from core.distance import dist_haversine

def escolher_precisao(raio_km):
    if(raio_km <= 0.6):
        return 6
    elif(raio_km <= 5):
        return 5
    else: 
        return 4

def consultar_entregadores(lat_restaurante, long_restaurante, raio_dado, trie:compact_trie, velocidade_media = 25):
    precisao_atual = escolher_precisao(raio_dado)
    restaurante_geo = geohash_encode(lat_restaurante, long_restaurante, precisao_atual)

    grid_geo = geohash_grid(restaurante_geo)
    
    candidatos = []
    ids_vistos = set() 

    for celula in grid_geo.values():
        encontrados = trie.buscar_prefixo(celula)
        for entregador in encontrados:
            if entregador["id"] not in ids_vistos:
                ids_vistos.add(entregador["id"])
                candidatos.append(entregador)

    aceitos = []
    rejeitados = []

    for entregador in candidatos:
        d = dist_haversine(entregador["lat"],entregador["long"], lat_restaurante, long_restaurante)
        
        # tempo em minutos
        tempo_min = (d/velocidade_media) * 60
        
        info = {
            "id": entregador["id"],
            "lat": entregador["lat"],
            "long": entregador["long"],
            "distancia_km": round(d,2),
            "tempo_min": round(tempo_min, 2)
        }

        if d <= raio_dado:
            aceitos.append(info)
        else:
            rejeitados.append(info)
    
    aceitos.sort(key=lambda x: x["distancia_km"])

    return {
        "filtrados": aceitos,
        "descartados": rejeitados,
        "total_candidatos": len(candidatos),
        "total_aceitos": len(aceitos)
    }



