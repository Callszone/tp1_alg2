import pandas as pd
import requests
import time
import urllib.parse
from pyproj import Transformer


transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def buscar_coordenada_pbh(rua, numero):
    if pd.isna(rua) or pd.isna(numero):
        return None, None

    rua_cod = urllib.parse.quote(str(rua).strip())
    num_cod = urllib.parse.quote(str(numero).strip())
    url = f"http://geocoder.pbh.gov.br/geocoder/v2/address?logradouro={rua_cod}&numero={num_cod}"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            dados = res.json().get("endereco", [])
            if dados and "wkt" in dados[0]:
                coords = dados[0]["wkt"].replace("POINT", "").replace("(", "").replace(")", "").split()
                lon, lat = transformer.transform(float(coords[0]), float(coords[1]))
                return lat, lon
        
        return None, None
    except requests.RequestException:
        return None, None

def processar_enderecos(arquivo_entrada, arquivo_saida):
    df = pd.read_csv(arquivo_entrada, dtype=str)

    for col in ['LATITUDE', 'LONGITUDE']:
        if col not in df.columns:
            df[col] = None

    linhas_pendentes = df[df['LATITUDE'].isna()]

    for contador, (index, row) in enumerate(linhas_pendentes.iterrows(), 1):
        lat, lon = buscar_coordenada_pbh(row['NOME_LOGRADOURO'], row['NUMERO_IMOVEL'])
        
        df.loc[index, ['LATITUDE', 'LONGITUDE']] = [lat, lon]
        time.sleep(0.3)
        
        if contador % 50 == 0:
            df.to_csv(arquivo_saida, index=False)

    if not linhas_pendentes.empty:
        df.to_csv("enderecos_geocodificados_final.csv", index=False)

def completar_csv(csv_principal, csv_secundario, csv_saida, chave='_id'):
    df1 = pd.read_csv(csv_principal, index_col=chave)
    df2 = pd.read_csv(csv_secundario, index_col=chave)
    
    # preenche os NaNs do df1 com os dados do df2
    df_final = df1.combine_first(df2)
    
    # retorna a chave para coluna normal, caso tenha sido usada como índice
    if chave:
        df_final = df_final.reset_index()
        
    df_final.to_csv(csv_saida, index=False)

if __name__ == "__main__":
    ENDERECOS_CSV = 'faltantes.csv'
    ENDERECOS_COM_COORDENADAS_CSV = 'faltantes_encontrados.csv'
    processar_enderecos(ENDERECOS_CSV,ENDERECOS_COM_COORDENADAS_CSV)

    CSV_INCOMPLETO = 'bares_com_coords.csv'
    CSV_FINAL = 'coords_final.csv'
    completar_csv(CSV_INCOMPLETO, ENDERECOS_COM_COORDENADAS_CSV, CSV_FINAL)