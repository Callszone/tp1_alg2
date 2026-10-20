import pandas as pd
from pathlib import Path

# Caminho do arquivo
pasta_core = Path(__file__).parent
pasta_data = pasta_core.parent / "data"
caminho_df = pasta_data / "coords_final.csv"
# Carrega o CSV
df_restaurantes = pd.read_csv(caminho_df, dtype=str)