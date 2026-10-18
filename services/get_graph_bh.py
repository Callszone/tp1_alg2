import osmnx as ox

ox.settings.log_console = True
ox.settings.use_cache = True

ox.settings.timeout = 900
ox.settings.max_query_area_size = 500000000000
lugar = "Belo Horizonte, Minas Gerais, Brazil"

G = ox.graph_from_place(lugar, network_type="drive")

caminho_arquivo = "grafo_bh_drive.graphml"
ox.save_graphml(G, filepath=caminho_arquivo)