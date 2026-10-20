import pandas as pd

def preparar_csv_frontend(caminho_arquivo):
    print(f"Lendo o arquivo de origem: {caminho_arquivo}...")
    
    # Carrega o CSV
    df = pd.read_csv(caminho_arquivo, dtype=str)
    
    # Completa os vazios de NOME_FANTASIA com o NOME
    if 'NOME_FANTASIA' in df.columns and 'NOME' in df.columns:
        df['NOME_FANTASIA'] = df['NOME_FANTASIA'].fillna(df['NOME'])
        print("Valores vazios de NOME_FANTASIA preenchidos.")

    # Cria uma string para representar os restaurantes na pesquisa
    df['NOME_EXIBICAO'] = (
        df['NOME_FANTASIA'].fillna("") + " - " + 
        df['NOME_BAIRRO'].fillna("") + " (" + 
        df['DESC_LOGRADOURO'].fillna("") + " " + 
        df['NOME_LOGRADOURO'].fillna("") + ", " + 
        df['NUMERO_IMOVEL'].fillna("S/N").astype(str) + ")"
    )
    print("Coluna NOME_EXIBICAO criada com sucesso.")

    # Sobrescreve o arquivo csv
    df.to_csv(caminho_arquivo, index=False)
    print(f"Arquivo salvo e atualizado em: {caminho_arquivo}")

if __name__ == "__main__":
    # Caminho do arquivo
    ARQUIVO_ALVO = 'data/coords_final.csv'
    
    preparar_csv_frontend(ARQUIVO_ALVO)