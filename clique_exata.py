import networkx as nx
import time  # <-- Biblioteca adicionada para medir o tempo

# =====================================================================
# CONFIGURAÇÃO
# =====================================================================
pasta_instancias = './instancias/'
arquivo_grafo = pasta_instancias + 'rede_primeiras2k.graphml'
# =====================================================================

print(f"Carregando o grafo de '{arquivo_grafo}'... Por favor, aguarde.")

try:
    G = nx.read_graphml(arquivo_grafo)
    print("Grafo carregado com sucesso!")
    print(f"Estrutura original: {G.number_of_nodes()} vértices e {G.number_of_edges()} arestas.")
except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_grafo}' não foi encontrado. Verifique o diretório.")
    exit()

# Trata grafos direcionados, pois cliques exigem conexões bidirecionais implícitas
if G.is_directed():
    print("\n⚠️  Aviso: Seu grafo original é DIRECIONADO.")
    print("Como o cálculo de cliques exige conexões mútuas, o grafo")
    print("será convertido para NÃO-DIRECIONADO temporariamente para esta análise.")
    G_analise = G.to_undirected()
else:
    G_analise = G

print("\n🧠 Buscando a Maior Clique na rede...")
print("Nota: Se o grafo for gigante, isso pode levar de alguns segundos a alguns minutos.")

try:
    # Marca o tempo inicial ANTES do algoritmo rodar
    tempo_inicio = time.time()
    
    # nx.find_cliques encontra todas as cliques maximais.
    # O comando max(..., key=len) varre essa lista e pega a que tiver a maior quantidade de nós.
    maior_clique = max(nx.find_cliques(G_analise), key=len)
    
    # Marca o tempo final DEPOIS que o algoritmo terminou
    tempo_fim = time.time()
    
    # Calcula a duração
    tempo_decorrido = tempo_fim - tempo_inicio
    
    # Ordena os vértices numericamente para o print ficar bonito e fácil de ler
    maior_clique_ordenada = sorted(maior_clique, key=int)
    
    print("=" * 50)
    print("🏆 MAIOR CLIQUE ENCONTRADA COM SUCESSO!")
    print("=" * 50)
    print(f"-> Tempo de busca: {tempo_decorrido:.4f} segundos") # <-- Print do tempo
    print(f"-> Quantidade de vértices envolvidos: {len(maior_clique_ordenada)}")
    print("-> Definição: Cada número listado abaixo tem uma ligação direta com TODOS os outros.")
    print("\n🔢 Vértices que compõem a maior clique (em ordem numérica):")
    print(", ".join(maior_clique_ordenada))
    print("=" * 50)

except ValueError:
    print("\n❌ Não foi possível encontrar nenhuma clique. O grafo pode estar vazio ou sem conexões válidas.")