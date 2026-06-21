import networkx as nx
import random
import time

# =====================================================================
# CONFIGURAÇÃO
# =====================================================================
arquivo_grafo = 'rede_personalizada.graphml'

# Número de passos (iterações) da busca local.
# Como o algoritmo é linear e muito rápido, 5000 a 10000 passos rodam em segundos.
MAX_PASSOS = 5000  
# =====================================================================

def busca_local_cc_clique(G, max_passos):
    """
    Implementação conceitual da Heurística de Busca Local com 
    Configuration Checking (CC) inspirada nos papers de Shaowei Cai.
    """
    # 1. Inicialização
    todos_nos = list(G.nodes())
    if not todos_nos:
        return []

    # Começa com uma clique simples: um nó aleatório
    # no_inicial = random.choice(todos_nos)
    no_inicial = max(todos_nos, key=lambda x: G.degree(x))
    clique_atual = {no_inicial}
    melhor_clique = set(clique_atual)
    
    # Vetor de Configuration Checking (CC)
    # 1 = Permitido testar/adicionar | 0 = Proibido (para evitar loops)
    conf_change = {v: 1 for v in todos_nos}
    
    print("🚀 Iniciando a busca local com Configuration Checking...")
    
    for passo in range(max_passos):
        # Achar candidatos: nós que são vizinhos de TODOS os nós da clique atual
        # e que não estão na clique
        candidatos = set(todos_nos) - clique_atual
        for no in clique_atual:
            candidatos = candidatos.intersection(G.neighbors(no))
            
        # Aplica a regra do Shaowei Cai: Filtra apenas os candidatos que possuem conf_change == 1
        candidatos_validos = [v for v in candidatos if conf_change[v] == 1]
        
        # FASE DE EXPANSÃO (Se houver candidatos permitidos pelo CC)
        if candidatos_validos:
            # Estratégia Gulosa: Escolhe o candidato com maior grau (mais conexões) no grafo
            proximo_no = max(candidatos_validos, key=lambda x: G.degree(x))
            clique_atual.add(proximo_no)
            
            # REGRA CC: Quando um nó é adicionado, a configuração de todos os seus vizinhos muda!
            for vizinho in G.neighbors(proximo_no):
                conf_change[vizinho] = 1
                
        # FASE DE RECONSTRUÇÃO/PODA (Se caiu em um ótimo local e o CC bloqueou a expansão)
        else:
            if clique_atual:
                # Escolhe um nó para remover da clique (o de menor grau, para tentar abrir espaço)
                no_remover = min(clique_atual, key=lambda x: G.degree(x))
                clique_atual.remove(no_remover)
                
                # REGRA CC Crucial: O nó removido fica PROIBIDO (0) de voltar imediatamente
                conf_change[no_remover] = 0
                
                # Mas os vizinhos dele são resetados para PERMITIDO (1)
                for vizinho in G.neighbors(no_remover):
                    conf_change[vizinho] = 1
            else:
                # Se a clique esvaziou completamente, reinicia com um nó permitido qualquer
                permitidos = [v for v in todos_nos if conf_change[v] == 1]
                if permitidos:
                    # clique_atual.add(random.choice(permitidos))
                    clique_atual.add(max(permitidos, key=lambda x: G.degree(x)))
                else:
                    clique_atual.add(random.choice(todos_nos))

        # Atualiza o recorde global da maior clique vista até agora
        if len(clique_atual) > len(melhor_clique):
            melhor_clique = set(clique_atual)
            # Print de progresso caso ele quebre o recorde
            print(f"✨ Recorde quebrado no passo {passo}! Novo tamanho: {len(melhor_clique)}")

    return list(melhor_clique)

# =====================================================================
# EXECUÇÃO PRINCIPAL
# =====================================================================

print(f"Carregando o grafo de '{arquivo_grafo}'... Por favor, aguarde.")

try:
    G = nx.read_graphml(arquivo_grafo)
    print("Grafo carregado com sucesso!")
except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_grafo}' não foi encontrado.")
    exit()

if G.is_directed():
    print("\n⚠️  Convertendo temporariamente para Não-Direcionado...")
    G_analise = G.to_undirected()
else:
    G_analise = G

# Limpeza preventiva de auto-loops
self_loops = list(nx.selfloop_edges(G_analise))
if self_loops:
    G_analise.remove_edges_from(self_loops)

# Medição de tempo
tempo_inicio = time.time()

# Executa a busca inspirada no paper
maior_clique = busca_local_cc_clique(G_analise, max_passos=MAX_PASSOS)

tempo_total = time.time() - tempo_inicio

if maior_clique:
    maior_clique_ordenada = sorted(maior_clique, key=int)
    
    print("\n" + "=" * 50)
    print("🏆 RESULTADO - BUSCA LOCAL COM CONFIGURATION CHECKING")
    print("=" * 50)
    print(f"-> Tempo de execução: {tempo_total:.4f} segundos")
    print(f"-> Tamanho da clique encontrada: {len(maior_clique_ordenada)} vértices")
    print(f"-> Vértices (em ordem numérica):")
    print(", ".join(maior_clique_ordenada))
    print("=" * 50)
else:
    print("\n❌ Nenhuma clique encontrada.")