import dash_leaflet as dl
from dash import Input, Output, State, no_update

from core.coord_correction import gerar_entregadores
from core.trie import compact_trie
from core.geohash import geohash_encode
from simulation.search_engine import consultar_entregadores

def registrar_callbacks(app, df_restaurantes):
    @app.callback(
        Output('dropdown-restaurante', 'options'),
        Input('input-busca', 'value')
    )
    def atualizar_dropdown(termo_busca):
        if not termo_busca:
            return []
        
        # Filtra restaurantes pela string atual
        filtro = df_restaurantes['NOME_EXIBICAO'].str.contains(termo_busca, case=False, na=False)
        resultados = df_restaurantes[filtro].head(50)
        
        # Retorna no formato demarcado
        return [{'label': nome, 'value': nome} for nome in resultados['NOME_EXIBICAO']]

    @app.callback(
        [Output('camada-marcadores', 'children'),
         Output('tabela-entregadores', 'data'),
         Output('mapa-principal', 'center')],
        Input('botao-gerar', 'n_clicks'),
        [State('dropdown-restaurante', 'value'),
         State('input-n-entregadores', 'value')]
    )
    def atualizar_mapa_e_tabela(n_clicks, restaurante_selecionado, n_entregadores):
        # Não faz nada se o botão não foi clicado ou não há restaurante
        if n_clicks == 0 or not restaurante_selecionado:
            return no_update, no_update, no_update
        
        # Pega as coordenadas do restaurante escolhido
        linha = df_restaurantes[df_restaurantes['NOME_EXIBICAO'] == restaurante_selecionado].iloc[0]
        lat_rest = float(linha['LATITUDE'])
        long_rest = float(linha['LONGITUDE'])
        
        # Gera a frota de entregadores
        coords_frota = gerar_entregadores(n_entregadores)
        
        # preenche a Árvore Trie
        arvore = compact_trie()
        for index, (lat, lon) in enumerate(coords_frota):
            entregador = {"id": f"Moto_{index+1}", "lat": lat, "long": lon}
            geo = geohash_encode(lat, lon, 8) 
            arvore.inserir(geo, entregador)
            
        # Consulta com base no raio os entregadores
        resultado = consultar_entregadores(lat_rest, long_rest, 2.0, arvore)
        aceitos = resultado["filtrados"]
        rejeitados = resultado["descartados"]
        
        # Cria o array para futuras marcacoes sobre o mapa
        marcadores = []
        
        # Pino do Restaurante (Usamos um Marker normal azul para destacar)
        marcadores.append(
            dl.Marker(position=(lat_rest, long_rest), children=[
                dl.Tooltip(f"Ponto Zero: {restaurante_selecionado}")
            ])
        )
        
        # Cria pinos vermelhos para entregadores selecionados
        for ent in aceitos:
            marcadores.append(
                dl.CircleMarker(
                    center=(ent['lat'], ent['long']), 
                    color='red', fillColor='red', fillOpacity=0.7, radius=6,
                    children=[dl.Tooltip(f"{ent['id']} - {ent['distancia_km']}km - ~{ent['tempo_min']}min")]                )
            )
            
        # Cria Pinos cinzas para demais entregadores
        for ent in rejeitados:
            marcadores.append(
                dl.CircleMarker(
                    center=(ent['lat'], ent['long']), 
                    color='gray', fillColor='gray', fillOpacity=0.5, radius=4,
                    children=[dl.Tooltip(f"{ent['id']} - Fora do Raio")]
                )
            )
            
        # Retorna os marcadores a serem inseridos no mapa, dados dos entregadores selecionados e centralização do mapa
        return marcadores, aceitos, (lat_rest, long_rest)
