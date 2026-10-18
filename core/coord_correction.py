import osmnx as ox
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
from pathlib import Path
from core.random_gen import gerar_pontos_distribuidos

# lendo os arquivos em data que serão usados

pasta_core = Path(__file__).parent
pasta_data = pasta_core.parent / "data"
caminho_grafo = pasta_data / "grafo_bh_drive.graphml"
G = ox.load_graphml(caminho_grafo)
caminho_df = pasta_data / "coords_final.csv"
df = pd.read_csv(caminho_df, dtype=str)
coords_base = df[["LATITUDE", "LONGITUDE"]].to_numpy()

def corrigir_coordenadas(latitude, longitude):
    # pega a rua mais próxima
    rua_id = ox.distance.nearest_edges(G, X=longitude, Y=latitude)
    u, v, key = rua_id

    # pega os dados físicos dessa rua dentro do grafo
    dados_rua = G.edges[u, v, key]

    # extraimos a linha da rua (geometria, pode ser curva)
    if 'geometry' in dados_rua:
        # é curva:
        linha_da_rua = dados_rua['geometry']
    else:
        # é uma reta, só conectamos os nós
        no_u = G.nodes[u]
        no_v = G.nodes[v]
        linha_da_rua = LineString([(no_u['x'], no_u['y']), (no_v['x'], no_v['y'])])

    # função que pega o ponto mais próximo da linha da rua
    # nearest_points retorna uma tupla com: (ponto_projetado_na_linha, ponto_original)
    ponto_corrigido, _ = nearest_points(linha_da_rua, Point(longitude,latitude))

    return ponto_corrigido.y, ponto_corrigido.x

# vetorizando a operação corrigir_coordenadas
corrigir_vetorizado = np.vectorize(corrigir_coordenadas)

def gerar_entregadores(N):
    array_inicial = gerar_pontos_distribuidos(coords_base, N)
    lats = array_inicial[:, 0]
    lons = array_inicial[:, 1]

    # aplica a correção pro array aleatório gerado
    novas_lats, novas_lons = corrigir_vetorizado(lats, lons)

    return np.column_stack((novas_lats, novas_lons))