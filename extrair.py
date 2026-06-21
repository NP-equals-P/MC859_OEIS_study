import random
import networkx as nx

# =====================================================================
# CONFIGURAÇÕES DO GRAFO
# =====================================================================

input_file = 'data.txt'             # O seu ficheiro original
output_graphml = 'rede_todas_direcionada.graphml'

# 1. MODO DE SELEÇÃO: Aleatório ou Intervalo (Range)?
ALEATORIO = False               # Se True, escolhe X sequências aleatórias. Se False, usa o intervalo abaixo.
QTD_ALEATORIA = 1000            # Se ALEATORIO = True, quantas sequências quer escolher?

# Se ALEATORIO = False, define o intervalo (X a Y) baseado na ordem do ficheiro:
INTERVALO_INICIO = 0            # Índice da primeira sequência (0 é a primeira)
INTERVALO_FIM = 400000    # Índice da última sequência

# 2. TIPO DE GRAFO
DIRECIONADO = True              # True: A->B é diferente de B->A. False: A-B e B-A são a mesma ligação.

# 3. PESOS
COM_PESOS = False                # True: Conta as repetições e cria a coluna 'Weight'. False: Apenas ligações únicas.
FILTRAR_PESO_1 = True           # True: Ignora ligações que só aparecem 1 vez (só funciona se COM_PESOS = True).

# =====================================================================

edges_count = {}
linhas_validas = []

print("A ler o ficheiro para encontrar sequências válidas...")

# 1. Lê todas as sequências válidas para a memória
with open(input_file, 'r') as f:
    for line in f:
        # Ignora comentários ou linhas vazias
        if line.startswith('#') or not line.strip():
            continue
        linhas_validas.append(line)

total_sequencias = len(linhas_validas)
print(f"Total de sequências encontradas no ficheiro: {total_sequencias}")

# 2. Aplica as regras de seleção (Aleatório vs Intervalo)
if ALEATORIO:
    # Garante que não tenta sortear mais do que existe
    qtd_real = min(QTD_ALEATORIA, total_sequencias)
    linhas_selecionadas = random.sample(linhas_validas, qtd_real)
    print(f"Modo Aleatório: Foram sorteadas {qtd_real} sequências.")
else:
    # O Python lida automaticamente se o FIM for maior que o total
    linhas_selecionadas = linhas_validas[INTERVALO_INICIO:INTERVALO_FIM]
    print(f"Modo Intervalo: A processar as sequências do índice {INTERVALO_INICIO} ao {INTERVALO_INICIO + len(linhas_selecionadas) - 1}.")

# 3. Processa as ligações
print("A construir as ligações...")
for line in linhas_selecionadas:
    parts = line.strip().split(',')
    sequence = [p.strip() for p in parts[1:] if p.strip()]
    
    for i in range(len(sequence) - 1):
        u = sequence[i]
        v = sequence[i+1]
        
        # Se NÃO for direcionado, ordenamos os nós para garantir que (1, 2) e (2, 1) sejam contados juntos
        if not DIRECIONADO:
            # Ordenar numericamente (usamos int para lidar corretamente com números negativos e com mais dígitos)
            u, v = str(min(int(u), int(v))), str(max(int(u), int(v)))
            
        edge = (u, v)
        
        # Sistema de contagem
        if edge in edges_count:
            edges_count[edge] += 1
        else:
            edges_count[edge] = 1

# 4. Grava o resultado diretamente em um arquivo GraphML
print("A guardar o ficheiro GraphML...")

# Cria o grafo no NetworkX baseado na sua configuração
if DIRECIONADO:
    G = nx.DiGraph()
else:
    G = nx.Graph()

# Alimenta o grafo do NetworkX com o seu dicionário de arestas
for (u, v), weight in edges_count.items():
    if COM_PESOS:
        if FILTRAR_PESO_1 and weight <= 1:
            continue
        G.add_edge(u, v, weight=weight)
    else:
        G.add_edge(u, v)

# Salva direto no formato GraphML
nx.write_graphml(G, "./instancias/" + output_graphml)

print(f"Concluído! Ficheiro GraphML '{output_graphml}' criado com {G.number_of_edges()} ligações.")