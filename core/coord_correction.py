import osmnx as ox
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
from pathlib import Path
from core.random_gen import gerar_pontos_distribuidos

# Caminhos dos arquivos
pasta_core = Path(__file__).parent
pasta_data = pasta_core.parent / "data"
caminho_grafo = pasta_data / "grafo_bh_drive_conexo.graphml"
G = ox.load_graphml(caminho_grafo)

caminho_df = pasta_data / "coords_final.csv"
df = pd.read_csv(caminho_df, dtype=str)

# Garante que lat e long sejam float
coords_base = df[["LATITUDE", "LONGITUDE"]].astype(float).to_numpy()

def gerar_entregadores(N):
    # Gera os pontos aleatórios
    array_inicial = gerar_pontos_distribuidos(coords_base, N)
    lats = array_inicial[:, 0]
    lons = array_inicial[:, 1]

    # Busca as arestas mais próximas em lote
    edges = ox.distance.nearest_edges(G, X=lons, Y=lats)

    novas_lats = np.empty(N)
    novas_lons = np.empty(N)

    # Projeta os pontos nas ruas
    for idx, (u, v, key) in enumerate(edges):
        dados_rua = G.edges[u, v, key]
        
        if 'geometry' in dados_rua:
            linha_da_rua = dados_rua['geometry']
        else:
            no_u = G.nodes[u]
            no_v = G.nodes[v]
            linha_da_rua = LineString([(no_u['x'], no_u['y']), (no_v['x'], no_v['y'])])

        ponto_corrigido, _ = nearest_points(linha_da_rua, Point(lons[idx], lats[idx]))
        novas_lats[idx] = ponto_corrigido.y
        novas_lons[idx] = ponto_corrigido.x

    return np.column_stack((novas_lats, novas_lons))