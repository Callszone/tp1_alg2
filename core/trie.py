class node_trie:
    def __init__(self, prefixo: str = ""):
        # prefixo salvo pelo no
        self.prefixo = prefixo
        
        # dicionário com chave (primeiro caractere do próximo prefixo) e valor é outro no_trie
        self.filhos = {}
        
        # lista para armazenar os entregadores 
        # cada item pode ser um dict: {"id":, "lat": , "long": }
        self.entregadores = []

    def eh_folha(self) -> bool:
        return len(self.filhos) == 0

# função para a inserção
def maior_prefixo_comum(s1, s2):
    i = 0

    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i += 1

    return i

class compact_trie:

    # construtor padrão
    def __init__(self):
        self.raiz = node_trie("")

    def inserir(self, geohash: str, entregador: dict):
        self._inserir_recursivo(self.raiz, geohash, entregador)

    def _inserir_recursivo(self, no_atual: node_trie, resto: str, entregador: dict):
        if len(resto) == 0:
            no_atual.entregadores.append(entregador)
            return

        primeira_letra = resto[0]

        # primeiro, se não tem filho com essa letra
        if primeira_letra not in no_atual.filhos:

            novo_filho = node_trie(resto)
            novo_filho.entregadores.append(entregador)
            no_atual.filhos[primeira_letra] = novo_filho

            return

        # se já possuir filho
        filho = no_atual.filhos[primeira_letra]
        k = maior_prefixo_comum(filho.prefixo, resto)

        #  se o prefixo inteiro do filho for igual
        if k == len(filho.prefixo):
            self._inserir_recursivo(filho, resto[k:], entregador)
        else:
            # gera-se um no intermediario com a parte comum e trata das partes restantes
            medio = node_trie(filho.prefixo[:k])
            filho.prefixo = filho.prefixo[k:]

            # conecto o filho antigo no novo no
            medio.filhos[filho.prefixo[0]] = filho

            if(len(resto[k:]) == 0):
                medio.entregadores.append(entregador)
            #se sobrou texto
            else:
                novo_no_ao_quadrado = node_trie(resto[k:])
                novo_no_ao_quadrado.entregadores.append(entregador)
                medio.filhos[resto[k:][0]] = novo_no_ao_quadrado
            no_atual.filhos[primeira_letra] = medio

    def dfs_coleta_tudo(self, no_atual: node_trie):
        resultado = list(no_atual.entregadores)
        
        for filho in no_atual.filhos.values():
            entregadores_do_filho = self.dfs_coleta_tudo(filho)
            resultado.extend(entregadores_do_filho)

        return resultado
    
    def buscar_prefixo(self, prefixo):
        return self._buscar_recursivo(self.raiz, prefixo)

    def _buscar_recursivo(self, no_atual:node_trie, resto):
        # se meu prefixo foi completamente consumido
        if(len(resto) == 0):
            return self.dfs_coleta_tudo(no_atual)
        
        primeira_letra = resto[0]
        # se minha primeira letra não aparecer nos filhos do nó, ele não pertence a subarvore
        if(primeira_letra not in no_atual.filhos):
            return []
        else:
            filho = no_atual.filhos[primeira_letra]
            k = maior_prefixo_comum(filho.prefixo, resto)
            
            # prefixo buscado dentro do filho
            if(k == len(resto)):
                return self.dfs_coleta_tudo(filho)
            
            # resta busca no resto do prefixo do filho 
            elif(k == len(filho.prefixo)):
                return self._buscar_recursivo(filho, resto[k:])

            # o casamento quebrou no meio do caminho
            else:
                return []
            





