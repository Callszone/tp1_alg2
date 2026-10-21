# Cheque Mat – TP1 Algoritmos 2

## O que é
Um que simula uma frota de entregadores e permite buscar os mais próximos de um restaurante escolhido. A busca usa uma Trie compacta baseada em *Geohash*, com seus resultados traduzidos em um mapa interativo. 

---

## Estrutura de pastas
```
(tp1_alg2)
├─ front/               # UI e layout da aplicação
├─ data/               # dados para aplicação 
├─ core/                # algoritmo (Trie, Geohash, geração de coordenadas)
├─ relatorio/               # relatório e descrição dos algoritmos 
├─ services/               # conjunto de .csv 
├─ simulation/          # motor de consulta na Trie
├─ requirements.txt     # dependências Python
└─ README.md            # este documento
```

---

## Dependências
```text
dash==2.17.0
dash-leaflet==0.1.0
pandas==2.2.2
numpy==1.26.4
osmnx==1.9.2
shapely==2.0.3
pyproj==3.6.1
```
Essas versões estão fixas no arquivo `requirements.txt`.

---

## Como executar? 
```bash
# 1. entrar na pasta do projeto
cd $HOME/tp1_alg2

# 2. criar e ativar um virtualenv 
python3 -m venv .venv
source .venv/bin/activate   

# 3. instalar as dependências
pip install -r requirements.txt

# 4. rodar a aplicação
python front/interface.py
```
A aplicação ficará disponível em `http://127.0.0.1:8050`.

---

## Como usar
1. **Gerar frota** – ajuste a quantidade de entregadores (padrão 200) e clique em **GERAR NOVA FROTA**.
2. **Buscar entregadores** – escolha um restaurante, defina o raio (km) e pressione **BUSCAR ENTREGADORES MAIS PRÓXIMOS**.
3. O mapa mostrará:
   - círculo azul = área de busca;
   - ponto vermelho = entregadores dentro do raio;
   - ponto cinza = entregadores descartados;
   - linha azul = localização do restaurante.
4. A seção *Resumo da Consulta* exibe métricas de desempenho (tempo de resposta, distância média etc.).

---
