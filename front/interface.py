import dash
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
diretorio_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(diretorio_raiz))

from dash import dcc, html, dash_table
from front.carregar_base import df_restaurantes
import dash_leaflet as dl

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define formatação da página
app.layout = html.Div(style={
    'fontFamily': 'Segoe UI, Arial, sans-serif', 
    'padding': '20px',
    'backgroundColor': '#121212', 
    'color': '#E0E0E0',           
    'minHeight': '100vh'            
}, children=[
    
    # Cabeçalho
    html.H1("Cheque Mat", style={'textAlign': 'center', 'marginBottom': '5px'}),
    html.P("TP1 - DCC207 Algoritmos 2 | DCC / UFMG", style={'textAlign': 'center', 'color': '#888', 'marginTop': '0'}),
    html.Hr(style={'borderColor': '#333'}),

    # Controles superiores
    html.Div(style={'display': 'flex', 'gap': '25px', 'marginBottom': '20px', 'flexWrap': 'wrap'}, children=[
        
        # Bloco da Esquerda: Seleção de Restaurante e Consulta
        html.Div(style={
            'flex': '2', 'minWidth': '320px', 'backgroundColor': '#1e1e1e', 
            'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #333'
        }, children=[
            html.H3("1. Seleção do Restaurante e Raio", style={'marginTop': '0', 'color': '#64B5F6'}),
            
            html.Label(html.B("Buscar Restaurante (Nome, Rua ou Bairro):")),
            dcc.Input(
                id='input-busca', 
                type='text', 
                debounce=True,
                placeholder='Digite o nome ou bairro e aperte Enter...',
                style={
                    'width': '100%', 'padding': '10px', 'marginBottom': '10px',
                    'backgroundColor': '#2A2A2A', 'color': '#FFF', 'border': '1px solid #555',
                    'borderRadius': '4px', 'boxSizing': 'border-box'
                }
            ),

            html.Label(html.B("Selecione na lista:")),
            dcc.Dropdown(
                id='dropdown-restaurante',
                placeholder='Aguardando termo de busca...',
                options=[],
                value=None,
                style={'width': '100%', 'marginBottom': '15px', 'color': '#000'}
            ),

            html.Label(html.B("Raio de Atendimento (km):")),
            dcc.Slider(
                id='slider-raio',
                min=0.5,
                max=10.0,
                step=0.5,
                value=2.0,
                marks={1: '1 km', 2: '2 km', 3: '3 km', 5: '5 km', 10: '10 km'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            
            html.Button(
                "BUSCAR ENTREGADORES MAIS PRÓXIMOS", 
                id='botao-buscar', 
                n_clicks=0,
                style={
                    'width': '100%', 'padding': '12px', 'marginTop': '15px',
                    'backgroundColor': '#2196F3', 'color': 'white', 
                    'border': 'none', 'borderRadius': '4px', 'fontWeight': 'bold', 'cursor': 'pointer'
                }
            )
        ]),

        # Bloco da Direita: Geração da Frota
        html.Div(style={
            'flex': '1', 'minWidth': '240px', 'backgroundColor': '#1e1e1e', 
            'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #333'
        }, children=[
            html.H3("2. Simulação da Frota", style={'marginTop': '0', 'color': '#81C784'}),
            
            html.Label(html.B("Quantidade de entregadores (N):")),
            dcc.Input(
                id='input-n-entregadores', 
                type='number', 
                value=200, 
                min=1, 
                style={
                    'width': '100%', 'padding': '10px', 'marginBottom': '10px',
                    'backgroundColor': '#2A2A2A', 'color': '#FFF', 'border': '1px solid #555',
                    'borderRadius': '4px', 'boxSizing': 'border-box'
                }
            ),
            
            html.Button(
                "GERAR NOVA FROTA", 
                id='botao-gerar', 
                n_clicks=0,
                style={
                    'width': '100%', 'padding': '14px', 
                    'backgroundColor': '#4CAF50', 'color': 'white', 
                    'border': 'none', 'borderRadius': '4px', 'fontWeight': 'bold', 'cursor': 'pointer'
                }
            ),

            html.Div(id='status-frota', style={'marginTop': '15px', 'color': '#81C784', 'fontSize': '14px'}),
            html.Div(id='metricas-resumo', style={'marginTop': '15px', 'color': '#B0BEC5', 'fontSize': '13px'})
        ])
    ]),

    # Mapa e Tabela
    html.Div(style={'display': 'flex', 'gap': '20px', 'height': '600px'}, children=[
        
        # Mapa Interativo
        html.Div(style={'flex': '2', 'border': '1px solid #444', 'borderRadius': '8px', 'overflow': 'hidden'}, children=[
            dl.Map(
                id='mapa-principal',
                center=(-19.92, -43.93), 
                zoom=12,
                style={'width': '100%', 'height': '100%'},
                children=[
                    dl.TileLayer(),
                    dl.LayerGroup(id='camada-marcadores')
                ]
            )
        ]),

        # Tabela de Entregadores Próximos
        html.Div(style={
            'flex': '1', 'backgroundColor': '#1e1e1e', 'padding': '15px', 
            'borderRadius': '8px', 'border': '1px solid #444', 'overflowY': 'auto'
        }, children=[
            html.H3("Entregadores Filtrados (No Raio)", style={'marginTop': '0', 'color': '#FF5252'}),
            dash_table.DataTable(
                id='tabela-entregadores',
                columns=[
                    {'name': 'ID', 'id': 'id'},
                    {'name': 'Distância (km)', 'id': 'distancia_km'},
                    {'name': 'Tempo Estimado (min)', 'id': 'tempo_min'}
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#2A2A2A', 'color': '#FFF', 'fontWeight': 'bold', 'border': '1px solid #555'},
                style_cell={'backgroundColor': '#1A1A1A', 'color': '#E0E0E0', 'textAlign': 'center', 'padding': '8px', 'border': '1px solid #333'}
            )
        ])
    ])
])

from front.callback import registrar_callbacks
registrar_callbacks(app, df_restaurantes)

if __name__ == '__main__':
    app.run(debug=True)
