import dash
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dash import dcc, html, dash_table
from carregar_base import df_restaurantes
import dash_leaflet as dl

# Inicializa o Dash
app = dash.Dash(__name__)

# Define formatação da pagina
app.layout = html.Div(style={
    'fontFamily': 'Times new Roman, sans-serif', 
    'padding': '20px',
    'backgroundColor': '#121212', # Fundo escuro
    'color': '#E0E0E0',           # Texto branco
    'minHeight': '100vh'            # Garante que o fundo cubra a tela toda
}, children=[
    
    # Cabeçalho
    html.H1("Entregas (nome a decidir)", style={'textAlign': 'center'}),
    html.Hr(),

    # Define caixas de texto e botao
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}, children=[
        
        html.Div(style={'flex': '2', 'minWidth': '300px'}, children=[
            # Bloco de Busca do Restaurante
            html.Label(html.B("Buscar Restaurante (Nome, Rua ou Bairro):")),
            dcc.Input(
                id='input-busca', 
                type='text',
                debounce=True,
                style={
                    'width': '100%', 'padding': '10px', 'marginBottom': '10px',
                    'backgroundColor': '#2A2A2A', # Fundo cinza escuro
                    'color': '#E0E0E0',           # Texto branco
                    'border': '1px solid #444'    # Borda
                }
            ),

            # Bloco de seleção do restaurante
            html.Label(html.B("Selecione o Restaurante")),
            dcc.Dropdown(
                id='dropdown-restaurante',
                placeholder='Aguardando busca...',
                options=[],
                value=None,
                style={
                    'width': '100%', 'padding': '10px', 'marginBottom': '10px',
                    'backgroundColor': '#2A2A2A', # Fundo cinza escuro
                    'color': '#E0E0E0',           # Texto branco
                    'border': '1px solid #444'      # Borda
                }
            )
        ]),

        # Bloco de Geração de Frota
        html.Div(style={'flex': '1', 'minWidth': '200px'}, children=[
            html.Label(html.B("Quantidade de entregadores:")),
            dcc.Input(
                id='input-n-entregadores', 
                type='number', 
                value=100, # Valor padrão inicial
                min=1, 
                style={
                    'width': '100%', 'padding': '10px', 'marginBottom': '10px',
                    'backgroundColor': '#2A2A2A', # Fundo cinza escuro
                    'color': '#E0E0E0',           # Texto branco
                    'border': '1px solid #444'      # Borda
                }
            ),
            
            html.Button(
                "GERAR ENTREGADORES", 
                id='botao-gerar', 
                n_clicks=0,
                style={
                    'width': '100%', 'padding': '15px', 
                    'backgroundColor': '#4CAF50', 'color': 'white', 
                    'border': 'none', 'fontWeight': 'bold', 'cursor': 'pointer'
                }
            )
        ])
    ]),

    # Mapa e Tabela
    html.Div(style={'display': 'flex', 'gap': '20px', 'height': '600px'}, children=[
        
        # Mapa
        html.Div(style={'flex': '2', 'border': '1px solid #ccc', 'position': 'relative'}, children=[
            dl.Map(
                id='mapa-principal',
                # Coordenadas iniciais em BH
                center=(-19.92,-43.93), 
                zoom=12,
                style={'width': '100%', 'height': '100%', 'margin': 'auto', 'display': 'block'},
                children=[
                    # A camada base vinda do OpenStreetMap
                    dl.TileLayer(),
                    
                    # Pinos dos entregadores
                    dl.LayerGroup(id='camada-marcadores')
                ]
            )
        ]),

        # Tabela de Motoristas Próximos
        html.Div(style={'flex': '1', 'overflowY': 'auto'}, children=[
            html.H3("Motoristas Mais Próximos (Raio)"),
            dash_table.DataTable(
                id='tabela-entregadores',
                columns=[
                    {'name': 'ID Motorista', 'id': 'id'},
                    {'name': 'Distância (km)', 'id': 'distancia_km'},
                    {'name': 'Tempo Estimado (min)', 'id': 'tempo_min'}
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#333333', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid #555'},
                style_cell={'backgroundColor': '#222222', 'color': 'white', 'textAlign': 'center', 'padding': '5px', 'border': '1px solid #444'}
            )
        ])
    ])
])

from callback import registrar_callbacks

registrar_callbacks(app, df_restaurantes)

# Roda a aplicação
if __name__ == '__main__':
    app.run(debug=True)
