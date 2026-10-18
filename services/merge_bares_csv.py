import pandas as pd
from pyproj import Transformer

def processar_coordenadas(arq_origem, arq_pbh, arq_saida):
    df_orig = pd.read_csv(arq_origem, dtype=str)
    df_pbh = pd.read_csv(arq_pbh, dtype=str, sep=";")

    # padronização nativa do Pandas 
    def limpar_coluna(serie):
        return serie.str.normalize('NFKD').str.encode('ascii', errors='ignore') \
                    .str.decode('utf-8').str.upper().str.strip()

    df_orig['CHAVE_RUA'] = limpar_coluna(df_orig['NOME_LOGRADOURO'])
    df_orig['CHAVE_NUMERO'] = limpar_coluna(df_orig['NUMERO_IMOVEL'])
    df_pbh['CHAVE_RUA'] = limpar_coluna(df_pbh['NOME_LOGRADOURO'])
    df_pbh['CHAVE_NUMERO'] = limpar_coluna(df_pbh['NUMERO_IMOVEL'])

    # remoção de duplicatas e Merge
    df_pbh_reduzido = df_pbh.drop_duplicates(subset=['CHAVE_RUA', 'CHAVE_NUMERO'])[['CHAVE_RUA', 'CHAVE_NUMERO', 'GEOMETRIA']]
    df_resultado = pd.merge(df_orig, df_pbh_reduzido, on=['CHAVE_RUA', 'CHAVE_NUMERO'], how='left')

    # extração via Regex e Conversão Vetorizada de Coordenadas
    coords = df_resultado['GEOMETRIA'].str.extract(r'POINT\s*\(([-\d.]+)\s+([-\d.]+)\)').astype(float)
    mask = coords[0].notna() # filtra apenas as linhas onde a geometria foi encontrada

    conversor = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)
    
    # a transformação é aplicada em bloco (arrays)
    df_resultado.loc[mask, 'LONGITUDE'], df_resultado.loc[mask, 'LATITUDE'] = conversor.transform(
        coords.loc[mask, 0].values, 
        coords.loc[mask, 1].values
    )

    # limpeza final e exportação
    df_resultado.drop(columns=['CHAVE_RUA', 'CHAVE_NUMERO', 'GEOMETRIA'], inplace=True)
    df_resultado.to_csv(arq_saida, index=False)

    df_faltantes = df_resultado[df_resultado['LATITUDE'].isna()]
    if not df_faltantes.empty:
        df_faltantes.to_csv("bares_faltantes.csv", index=False)

if __name__ == "__main__":
    # achamos base_pbh.csv pela página da prefeitura https://dados.pbh.gov.br/pt_BR/dataset/atividade-economica
    processar_coordenadas("bares.csv", "base_pbh.csv", "bares_com_coords.csv")