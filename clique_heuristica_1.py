import networkx as nx
import time  # <-- Biblioteca adicionada para medir o tempo

# =====================================================================
# CONFIGURAÇÃO
# =====================================================================
arquivo_grafo = 'rede_personalizada.graphml'
# =====================================================================

def heuristica_classica_gulosa(G):
    maior_clique_encontrada = []
    
    # Ordena os vértices pelo grau (os mais conectados primeiro)
    # Isso ajuda a encontrar uma clique gigante logo no início da busca!
    nos_por_grau = sorted(G.degree, key=lambda x: x[1], reverse=True)
    
    for no, grau in nos_por_grau:
        # A MÁGICA DA PODA (PRUNING):
        # Se um nó tem grau 5, a maior clique possível que ele pode formar é 6.
        # Se já achamos uma clique de 10, ignoramos este nó e poupamos tempo!
        if grau + 1 <= len(maior_clique_encontrada):
            break
            
        clique_atual = {no}
        candidatos = set(G.neighbors(no))
        candidatos.discard(no) # Previne self-loops ocultos
        
        while candidatos:
            melhor_candidato = None
            max_conexoes = -1
            
            # Avalia qual vizinho tem mais amizades dentro do grupo de candidatos
            for c in candidatos:
                vizinhos_de_c = set(G.neighbors(c))
                conexoes_internas = len(candidatos.intersection(vizinhos_de_c))
                
                if conexoes_internas > max_conexoes:
                    max_conexoes = conexoes_internas
                    melhor_candidato = c
                    
            # Adiciona o campeão à clique
            clique_atual.add(melhor_candidato)
            
            # Filtra: os próximos candidatos TÊM que ser vizinhos do novo membro
            candidatos = candidatos.intersection(G.neighbors(melhor_candidato))
            candidatos.discard(melhor_candidato)
            
        # Atualiza o recorde global
        if len(clique_atual) > len(maior_clique_encontrada):
            maior_clique_encontrada = clique_atual
            
    return list(maior_clique_encontrada)

# =====================================================================
# EXECUÇÃO PRINCIPAL
# =====================================================================

print(f"A carregar o grafo de '{arquivo_grafo}'... Por favor, aguarde.")

try:
    G = nx.read_graphml(arquivo_grafo)
    print("Grafo carregado com sucesso!")
except FileNotFoundError:
    print(f"Erro: O ficheiro '{arquivo_grafo}' não foi encontrado.")
    exit()

if G.is_directed():
    print("\n⚠️  A converter temporariamente para Não-Direcionado (exigência para cliques)...")
    G_analise = G.to_undirected()
else:
    G_analise = G

# --- LIMPEZA DE SELF-LOOPS ---
self_loops = list(nx.selfloop_edges(G_analise))
if self_loops:
    print(f"🧹 A limpar {len(self_loops)} auto-conexões (self-loops) do grafo...")
    G_analise.remove_edges_from(self_loops)

print("\n🧠 A procurar a maior clique usando Heurística Gulosa Clássica...")

# Marca o tempo inicial ANTES da heurística rodar
tempo_inicio = time.time()

# Executa o algoritmo
maior_clique = heuristica_classica_gulosa(G_analise)

# Marca o tempo final DEPOIS que a heurística terminou
tempo_fim = time.time()

# Calcula a duração
tempo_decorrido = tempo_fim - tempo_inicio

if maior_clique:
    maior_clique_ordenada = sorted(maior_clique, key=int)
    
    print("=" * 50)
    print("🏆 CLIQUE ENCONTRADA (VIA GULOSA CLÁSSICA)!")
    print("=" * 50)
    print(f"-> Tempo de busca: {tempo_decorrido:.4f} segundos") # <-- Print do tempo
    print(f"-> Tamanho da clique: {len(maior_clique_ordenada)} vértices")
    print(f"-> Vértices (em ordem numérica):")
    print(", ".join(maior_clique_ordenada))
    print("=" * 50)
else:
    print("\n❌ Nenhuma clique encontrada.")