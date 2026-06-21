import networkx as nx
import time

# =====================================================================
# CONFIGURAÇÃO
# =====================================================================
arquivo_grafo = 'rede_personalizada.graphml'
arquivo_saida_graphml = 'rede_com_comunidades.graphml'
# =====================================================================

print(f"A carregar o grafo de '{arquivo_grafo}'... Por favor, aguarde.")

try:
    G = nx.read_graphml(arquivo_grafo)
    print("Grafo carregado com sucesso!")
except FileNotFoundError:
    print(f"Erro: O ficheiro '{arquivo_grafo}' não foi encontrado.")
    exit()

# O algoritmo de Louvain funciona melhor em grafos Não-Direcionados
if G.is_directed():
    print("A converter temporariamente para Não-Direcionado para a deteção de comunidades...")
    G_analise = G.to_undirected()
else:
    G_analise = G

# Limpeza de auto-ligações (self-loops) para não confundir o algoritmo
self_loops = list(nx.selfloop_edges(G_analise))
if self_loops:
    G_analise.remove_edges_from(self_loops)

print("\n🔍 A executar o algoritmo de Louvain para detetar comunidades...")
tempo_inicio = time.time()

# A MÁGICA ACONTECE AQUI: O NetworkX divide o grafo em comunidades
# Retorna uma lista de conjuntos (sets), onde cada conjunto tem os vértices de uma comunidade
comunidades = nx.community.louvain_communities(G_analise, seed=42)

tempo_total = time.time() - tempo_inicio

# Vamos ordenar as comunidades da maior (mais vértices) para a menor
comunidades = sorted(comunidades, key=len, reverse=True)

numero_de_comunidades = len(comunidades)

print("\n" + "=" * 50)
print("🏘️  RESUMO DAS COMUNIDADES ENCONTRADAS")
print("=" * 50)
print(f"-> Tempo de execução: {tempo_total:.4f} segundos")
print(f"-> Total de comunidades detetadas: {numero_de_comunidades}")
print("-" * 50)

# Vamos imprimir as 10 maiores comunidades para ter uma ideia
top_n = min(10, numero_de_comunidades)
print(f"📊 Top {top_n} Maiores Comunidades:")

for i in range(top_n):
    tamanho = len(comunidades[i])
    # Mostra até 5 nós como exemplo para não encher o ecrã
    exemplo_nos = list(comunidades[i])[:5] 
    print(f"  Comunidade {i+1}: {tamanho} vértices. Exemplo de membros: {exemplo_nos}...")

# =====================================================================
# INSERIR OS DADOS NO GRAFO ORIGINAL E GRAVAR
# =====================================================================
print("\n💾 A gravar os resultados no grafo original...")

# Para cada comunidade encontrada, damos um ID e marcamos cada vértice no grafo
for id_comunidade, grupo_de_nos in enumerate(comunidades):
    for no in grupo_de_nos:
        # Cria um novo atributo chamado 'Comunidade' dentro do grafo original
        G.nodes[no]['Comunidade'] = str(id_comunidade + 1)

# Grava o novo ficheiro GraphML com esta informação embutida
nx.write_graphml(G, arquivo_saida_graphml)

print(f"🎉 Concluído! O ficheiro '{arquivo_saida_graphml}' foi gerado.")
print("Agora pode abri-lo no Cytoscape e pintar os nós com base no atributo 'Comunidade'!")
print("=" * 50)