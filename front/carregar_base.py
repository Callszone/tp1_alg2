import pandas as pd
from pathlib import Path

caminho_csv = Path(__file__).resolve().parent.parent / "data" / "coords_final.csv"
df_restaurantes = pd.read_csv(caminho_csv, dtype=str)
