import csv
import networkx as nx

# =====================================================================
# CONFIGURAÇÕES DA ANÁLISE
# =====================================================================
pasta = './instancias/'
arquivo_grafo = pasta + 'rede_todas_direcionada.graphml'
arquivo_saida_csv = 'distancias_do_vertice.csv'

# DIGITE AQUI O VÉRTICE QUE VOCÊ QUER ANALISAR (entre aspas, como string)
VERTICE_ALVO = '1'  

# =====================================================================

print(f"A carregar o grafo de '{arquivo_grafo}'... Isso pode levar alguns segundos.")

try:
    G = nx.read_graphml(arquivo_grafo)
    print("Grafo carregado com sucesso!")

    # Bloco de identificação da instância
    direcionado = "Sim" if G.is_directed() else "Não"
    tem_peso = "Não"
    if G.number_of_edges() > 0:
        primeira_aresta = list(G.edges(data=True))[0]
        if 'weight' in primeira_aresta[2]:
            tem_peso = "Sim"

    print("-" * 30)
    print("📋 RESUMO DA INSTÂNCIA:")
    print(f"-> Vértices: {G.number_of_nodes()}")
    print(f"-> Arestas: {G.number_of_edges()}")
    print(f"-> É Direcionado? {direcionado}")
    print(f"-> É Ponderado (tem pesos)? {tem_peso}")
    print("-" * 30)

except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_grafo}' não foi encontrado.")
    exit()

# 1. Validação: O vértice escolhido existe neste grafo?
if VERTICE_ALVO not in G.nodes:
    print(f"❌ Erro: O vértice '{VERTICE_ALVO}' não existe no seu grafo atual.")
    print("Verifique se digitou corretamente ou se ele não foi cortado pelos filtros anteriores.")
    exit()

print(f"🧠 Calculando distâncias a partir do vértice '{VERTICE_ALVO}' para toda a rede...")

# 2. Calcula a distância do vértice alvo para TODOS os outros alcançáveis
# Retorna um dicionário no formato: {'outro_vertice': distancia_em_pulos}
mapa_distancias = nx.single_source_shortest_path_length(G, source=VERTICE_ALVO)

print(f"💾 Gravando resultados no arquivo CSV '{arquivo_saida_csv}'...")

# 3. Cria o arquivo CSV com os resultados
with open(arquivo_saida_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Cabeçalho do CSV
    writer.writerow(['Target_Node', 'Distance_From_Source'])
    
    contador_alcancaveis = 0
    
    # Primeiro salvamos todos os vértices que possuem um caminho possível
    for node, distancia in mapa_distancias.items():
        if node == VERTICE_ALVO:
            continue # Pula o próprio vértice alvo (distância 0)
        writer.writerow([node, distancia])
        contador_alcancaveis += 1
        
    # 4. Tratamento de Nós Inalcançáveis (Componentes isoladas/ilhas)
    contador_inalcancaveis = 0
    
    # === MUDANÇA AQUI: Criamos uma lista para guardar quem são os inalcançáveis ===
    lista_inalcancaveis = [] 
    
    for node in G.nodes:
        if node not in mapa_distancias:
            writer.writerow([node, 'Inalcançável'])
            contador_inalcancaveis += 1
            lista_inalcancaveis.append(node) # Guarda o nó na lista

print("-" * 50)
print("📊 RESUMO DA EXECUÇÃO:")
print(f"-> Vértices alcançáveis a partir de '{VERTICE_ALVO}': {contador_alcancaveis}")
print(f"-> Vértices inalcançáveis (outras componentes): {contador_inalcancaveis}")

# === MUDANÇA AQUI: Print dos inalcançáveis no terminal ===
if contador_inalcancaveis > 0:
    print("\n🛑 LISTA DE VÉRTICES INALCANÇÁVEIS:")

    lista_ordenada = sorted(lista_inalcancaveis, key=int)
    # O comando join junta todos os elementos da lista separados por vírgula para não encher a tela de linhas
    print(", ".join(lista_ordenada))
    
print(f"\n🎉 Concluído! O arquivo '{arquivo_saida_csv}' foi gerado com sucesso.")
print("-" * 50)