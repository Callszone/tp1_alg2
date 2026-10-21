import dash_leaflet as dl
from dash import Input, Output, State, no_update, html
import time

from core.coord_correction import gerar_entregadores
from core.trie import compact_trie
from core.geohash import geohash_encode
from simulation.search_engine import consultar_entregadores

# Estado global da frota na memória
FROTA_ATUAL = {
    "arvore": None,
    "coords": [],
    "total": 0
}

def registrar_callbacks(app, df_restaurantes):

    # 1. Callback da busca textual 
    @app.callback(
        Output('dropdown-restaurante', 'options'),
        Input('input-busca', 'value')
    )
    def atualizar_dropdown(termo_busca):
        if not termo_busca:
            return []
        filtro = df_restaurantes['NOME_EXIBICAO'].str.contains(termo_busca, case=False, na=False)
        resultados = df_restaurantes[filtro].head(50)
        return [{'label': nome, 'value': nome} for nome in resultados['NOME_EXIBICAO']]

    # 2. GERAR NOVA FROTA
    @app.callback(
        [Output('status-frota', 'children'),
         Output('camada-marcadores', 'children', allow_duplicate=True),
         Output('tabela-entregadores', 'data', allow_duplicate=True),
         Output('metricas-resumo', 'children', allow_duplicate=True)],
        Input('botao-gerar', 'n_clicks'),
        State('input-n-entregadores', 'value'),
        prevent_initial_call=True
    )
    def acao_gerar_frota(n_clicks, n_entregadores):
        if not n_entregadores or n_entregadores <= 0:
            return "Informe uma quantidade válida de entregadores.", no_update, no_update, no_update
        
        t0 = time.time()
        coords = gerar_entregadores(n_entregadores)
        
        arvore = compact_trie()
        for index, (lat, lon) in enumerate(coords):
            entregador = {"id": f"Moto_{index+1}", "lat": lat, "long": lon}
            geo = geohash_encode(lat, lon, 8)
            arvore.inserir(geo, entregador)
            
        FROTA_ATUAL["arvore"] = arvore
        FROTA_ATUAL["coords"] = coords
        FROTA_ATUAL["total"] = len(coords)
        
        tempo = time.time() - t0
        
        # Plota os entregadores gerados no mapa em tom neutro
        marcadores_iniciais = [
            dl.CircleMarker(
                center=(lat, lon), 
                color='#888', fillColor='#888', fillOpacity=0.5, radius=3,
                children=[dl.Tooltip(f"Moto_{i+1}")]
            )
            for i, (lat, lon) in enumerate(coords)
        ]
        
        status_msg = f" Frota com {len(coords)} entregadores gerada em {tempo:.2f}s"
        resumo_vazio = html.Div([
            html.B("Status: "), "Frota gerada. Selecione um restaurante e clique em Buscar."
        ])
        
        return status_msg, marcadores_iniciais, [], resumo_vazio

    # 3. Callback do Botão 2: BUSCAR ENTREGADORES
    @app.callback(
        [Output('camada-marcadores', 'children'),
         Output('tabela-entregadores', 'data'),
         Output('mapa-principal', 'center'),
         Output('metricas-resumo', 'children')],
        Input('botao-buscar', 'n_clicks'),
        [State('dropdown-restaurante', 'value'),
         State('slider-raio', 'value')],
        prevent_initial_call=True
    )
    def acao_buscar_entregadores(n_clicks, restaurante_selecionado, raio_km):
        if FROTA_ATUAL["arvore"] is None:
            aviso = html.Span(" Gere a frota de entregadores primeiro!", style={'color': '#FFB74D'})
            return no_update, no_update, no_update, aviso

        if not restaurante_selecionado:
            aviso = html.Span(" Selecione um restaurante na lista!", style={'color': '#FFB74D'})
            return no_update, no_update, no_update, aviso

        # Coordenadas do restaurante
        linha = df_restaurantes[df_restaurantes['NOME_EXIBICAO'] == restaurante_selecionado].iloc[0]
        lat_rest = float(linha['LATITUDE'])
        long_rest = float(linha['LONGITUDE'])
        raio_busca = float(raio_km) if raio_km else 2.0

        # Consulta 
        t_inicio = time.perf_counter()
        resultado = consultar_entregadores(lat_rest, long_rest, raio_busca, FROTA_ATUAL["arvore"])
        tempo_consulta_ms = (time.perf_counter() - t_inicio) * 1000

        aceitos = resultado["filtrados"]
        rejeitados = resultado["descartados"]

        marcadores = []
        
        # 1. Pino de Destaque do Restaurante
        marcadores.append(
            dl.Marker(position=(lat_rest, long_rest), children=[
                dl.Tooltip(f"Restaurante: {restaurante_selecionado}")
            ])
        )
        
        # 2. Círculo do Raio de Atendimento
        marcadores.append(
            dl.Circle(
                center=(lat_rest, long_rest), 
                radius=raio_busca * 1000, 
                color='#2196F3', fill=True, fillOpacity=0.12, weight=2
            )
        )
        
        # 3. Pinos Vermelhos (Entregadores Aceitos / Dentro do Raio)
        for ent in aceitos:
            marcadores.append(
                dl.CircleMarker(
                    center=(ent['lat'], ent['long']), 
                    color='#D32F2F', fillColor='#F44336', fillOpacity=0.85, radius=6,
                    children=[dl.Tooltip(f"{ent['id']} | Dist: {ent['distancia_km']} km | ~{ent['tempo_min']} min")]
                )
            )

        # 4. Pinos Cinzas (Entregadores Descartados)
        for ent in rejeitados:
            marcadores.append(
                dl.CircleMarker(
                    center=(ent['lat'], ent['long']), 
                    color='#757575', fillColor='#9E9E9E', fillOpacity=0.4, radius=3,
                    children=[dl.Tooltip(f"{ent['id']} (Fora do Raio)")]
                )
            )

        # 5. Métricas Resumo 
        distancia_media = sum(e['distancia_km'] for e in aceitos) / len(aceitos) if aceitos else 0.0
        tempo_medio = sum(e['tempo_min'] for e in aceitos) / len(aceitos) if aceitos else 0.0

        resumo_metricas = html.Div([
            html.H4("Resumo da Consulta:", style={'margin': '5px 0', 'color': '#64B5F6'}),
            html.Div(f"• Total na Frota: {FROTA_ATUAL['total']}"),
            html.Div(f"• Candidatos Trie (3x3): {resultado['total_candidatos']}"),
            html.Div(f"• Aceitos no Raio: {len(aceitos)} ({len(aceitos)/FROTA_ATUAL['total']*100:.1f}%)" if FROTA_ATUAL['total'] > 0 else ""),
            html.Div(f"• Distância Média: {distancia_media:.2f} km"),
            html.Div(f"• Tempo Médio de Chegada: {tempo_medio:.1f} min"),
            html.Div(f"• Tempo de Resposta (Trie): {tempo_consulta_ms:.2f} ms", style={'color': '#81C784', 'fontWeight': 'bold'})
        ])

        return marcadores, aceitos, (lat_rest, long_rest), resumo_metricas
