import osmnx as ox
import networkx as nx
from pathlib import Path

# verificar que todas as ruas são validas, ou seja, se o grafo é fortemente conexo

def garantir_fortemente_conexo(G, caminho_saida):
    # verifica se já é 
    if nx.is_strongly_connected(G):
        G_final = G
    else: # não é, eita
        # encontra maior componente então
        maior_componente = max(nx.strongly_connected_components(G), key=len)
        
        # isola apenas esse continente em um novo grafo independente
        G_final = G.subgraph(maior_componente).copy()
    # salva
    ox.save_graphml(G_final, filepath=caminho_saida) 
    return G_final

if __name__ == "__main__":

    pasta_atual = Path(__file__).parent
    pasta_data = pasta_atual.parent / "data"
    caminho_grafo = pasta_data / "grafo_bh_drive.graphml"
    G = ox.load_graphml(caminho_grafo)

    caminho_saida = "grafo_bh_drive_conexo.graphml"
    G_limpo = garantir_fortemente_conexo(G, caminho_saida)