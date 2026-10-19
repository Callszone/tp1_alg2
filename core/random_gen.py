import numpy as np

# distribuir entregadores pela cidade
# distribuição gaussiana centrada nos endereços

def gerar_pontos_distribuidos(coords_base, N, proporcao=0.05, seed=None):
    rng = np.random.default_rng(seed)

    # coords na formatação numpy
    coords = np.array(coords_base)

    # quais coordenadas base serão usadas
    indices = rng.choice(len(coords), size=N, replace=True)

    centros = coords[indices]

    # calcula a escala da distribuição, baseado na amplitude da latitude e longitude
    escala_base = max(np.ptp(coords[:, 0]), np.ptp(coords[:, 1])) * proporcao
    if escala_base == 0: escala_base = 0.001 

    # distribuição normal para latitude
    ruido_lat = rng.normal(loc=0, scale=escala_base, size=N)
    
    # usado para ajustar a longitude
    latitude_media = np.radians(np.mean(coords[:, 0]))
    compensacao_lon_constante = 1.0 / np.cos(latitude_media)
    
    # distribuição normal pra longitude, com devido ajuste de escala
    ruido_lon = rng.normal(loc=0, scale=escala_base, size=N) * compensacao_lon_constante
    
    novas_lats = centros[:, 0] + ruido_lat
    novas_lons = centros[:, 1] + ruido_lon
    
    return np.column_stack((novas_lats, novas_lons))