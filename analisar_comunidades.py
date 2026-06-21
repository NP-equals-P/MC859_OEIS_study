import csv
import networkx as nx
import math
from sympy import isprime

# =====================================================================
# CONFIGURAÇÃO
# =====================================================================
arquivo_grafo = 'redeCOMPLETA_com_comunidades.graphml'
# =====================================================================

# =====================================================================
# EXECUÇÃO PRINCIPAL
# =====================================================================
print(f"A carregar o grafo de '{arquivo_grafo}'...")

try:
    G = nx.read_graphml(arquivo_grafo)
    print("Grafo carregado com sucesso!\n")
except FileNotFoundError:
    print(f"❌ Erro: O ficheiro '{arquivo_grafo}' não foi encontrado.")
    print("Certifique-se de que já correu o script de deteção de comunidades.")
    exit()

# ---------------------------------------------------------------------
# NOVO PASSO: Calcular os totais GLOBAIS na rede toda
# ---------------------------------------------------------------------
global_primos = 0
global_negativos = 0
global_potencias_2 = 0
global_potencias_10 = 0
global_quadrados = 0
global_fibonacci = 0

print("🧮 Calculando estatísticas globais da rede (isso pode levar alguns segundos)...")

for no in G.nodes():
    try:
        num = int(no)
        if num < 0:
            global_negativos += 1
        if isprime(num):
            global_primos += 1
            
        # Apenas para números não-negativos
        if num >= 0:
            # Potência de 2
            if num > 0 and (num & (num - 1)) == 0:
                global_potencias_2 += 1
                
            # Potência de 10
            s_num = str(num)
            if s_num[0] == '1' and all(c == '0' for c in s_num[1:]):
                global_potencias_10 += 1
                
            # Quadrado Perfeito
            if math.isqrt(num)**2 == num:
                global_quadrados += 1
                
            # Número de Fibonacci (Propriedade: 5n² + 4 ou 5n² - 4 é um quadrado perfeito)
            val1 = 5 * (num**2) + 4
            val2 = 5 * (num**2) - 4
            if (math.isqrt(val1)**2 == val1) or (val2 >= 0 and math.isqrt(val2)**2 == val2):
                global_fibonacci += 1
                
    except ValueError:
        continue

print(f"📊 Totais na rede inteira:")
print(f"   -> Primos: {global_primos} | Negativos: {global_negativos}")
print(f"   -> Potências de 2: {global_potencias_2} | Potências de 10: {global_potencias_10}")
print(f"   -> Quadrados Perfeitos: {global_quadrados} | Números de Fibonacci: {global_fibonacci}\n")
# ---------------------------------------------------------------------

# 1. Agrupar os vértices pelas suas comunidades
comunidades = {}

for no, atributos in G.nodes(data=True):
    id_comunidade = atributos.get('Comunidade', 'Desconhecida')
    
    if id_comunidade not in comunidades:
        comunidades[id_comunidade] = []
        
    comunidades[id_comunidade].append(no)

if 'Desconhecida' in comunidades and len(comunidades) == 1:
    print("❌ Erro: Não encontrei a marcação 'Comunidade' nos vértices.")
    print("Tem a certeza que este é o ficheiro gerado pelo script de Louvain?")
    exit()

# 2. Ordenar as comunidades pelo tamanho (da maior para a menor)
comunidades_ordenadas = sorted(
    [item for item in comunidades.items() if item[0] != 'Desconhecida'], 
    key=lambda x: len(x[1]), 
    reverse=False
)

# Estrutura para armazenar os recordistas de cada classe
recordistas = {
    'Pares': {'id': None, 'val': -1.0, 'tipo': 'da comunidade'},
    'Ímpares': {'id': None, 'val': -1.0, 'tipo': 'da comunidade'},
    'Primos': {'id': None, 'val': -1.0, 'tipo': 'de TODOS os primos da rede'},
    'Negativos': {'id': None, 'val': -1.0, 'tipo': 'de TODOS os negativos da rede'},
    'Potências 2': {'id': None, 'val': -1.0, 'tipo': 'de TODAS as potências de 2 da rede'},
    'Potências 10': {'id': None, 'val': -1.0, 'tipo': 'de TODAS as potências de 10 da rede'},
    'Quadrados Perf': {'id': None, 'val': -1.0, 'tipo': 'de TODOS os quadrados da rede'},
    'Fibonacci': {'id': None, 'val': -1.0, 'tipo': 'de TODOS os Fibonacci da rede'}
}

print("=" * 60)
print("🔬 ANÁLISE MATEMÁTICA AVANÇADA DAS COMUNIDADES")
print("=" * 60)

# 3. Analisar cada comunidade
for id_comunidade, lista_nos in comunidades_ordenadas:
    total_validos = 0
    pares = 0
    impares = 0
    primos = 0
    negativos = 0
    potencias_2 = 0
    potencias_10 = 0
    quadrados = 0
    fibonacci = 0
    
    # Processa cada nó dentro desta comunidade
    for no_str in lista_nos:
        try:
            num = int(no_str)
            total_validos += 1
            
            # Análise de Positivo/Negativo
            if num < 0:
                negativos += 1
                
            # Análise de Par/Ímpar
            if num % 2 == 0:
                pares += 1
            else:
                impares += 1
                
            # Análise de Primos
            if isprime(num):
                primos += 1
                
            # Análises exclusivas para números não-negativos
            if num >= 0:
                # Potências de 2
                if num > 0 and (num & (num - 1)) == 0:
                    potencias_2 += 1
                    
                # Potências de 10
                s_num = str(num)
                if s_num[0] == '1' and all(c == '0' for c in s_num[1:]):
                    potencias_10 += 1
                    
                # Quadrados Perfeitos
                if math.isqrt(num)**2 == num:
                    quadrados += 1
                    
                # Números de Fibonacci
                val1 = 5 * (num**2) + 4
                val2 = 5 * (num**2) - 4
                if (math.isqrt(val1)**2 == val1) or (val2 >= 0 and math.isqrt(val2)**2 == val2):
                    fibonacci += 1
                
        except ValueError:
            continue
            
    # Se a comunidade só tinha texto e não teve números, saltamos a análise
    if total_validos == 0:
        continue
        
    if total_validos > 1:
        # Proporções locais (da própria comunidade)
        perc_pares = (pares / total_validos) * 100
        perc_impares = (impares / total_validos) * 100
        
        # Proporções globais (em relação a toda a base de dados)
        perc_primos = (primos / global_primos) * 100 if global_primos > 0 else 0
        perc_negativos = (negativos / global_negativos) * 100 if global_negativos > 0 else 0
        perc_potencias_2 = (potencias_2 / global_potencias_2) * 100 if global_potencias_2 > 0 else 0
        perc_potencias_10 = (potencias_10 / global_potencias_10) * 100 if global_potencias_10 > 0 else 0
        perc_quadrados = (quadrados / global_quadrados) * 100 if global_quadrados > 0 else 0
        perc_fibonacci = (fibonacci / global_fibonacci) * 100 if global_fibonacci > 0 else 0
        
        # Atualização do dicionário de recordistas
        if perc_pares > recordistas['Pares']['val']:
            recordistas['Pares']['val'], recordistas['Pares']['id'] = perc_pares, id_comunidade
        if perc_impares > recordistas['Ímpares']['val']:
            recordistas['Ímpares']['val'], recordistas['Ímpares']['id'] = perc_impares, id_comunidade
        if perc_primos > recordistas['Primos']['val']:
            recordistas['Primos']['val'], recordistas['Primos']['id'] = perc_primos, id_comunidade
        if perc_negativos > recordistas['Negativos']['val']:
            recordistas['Negativos']['val'], recordistas['Negativos']['id'] = perc_negativos, id_comunidade
        if perc_potencias_2 > recordistas['Potências 2']['val']:
            recordistas['Potências 2']['val'], recordistas['Potências 2']['id'] = perc_potencias_2, id_comunidade
        if perc_potencias_10 > recordistas['Potências 10']['val']:
            recordistas['Potências 10']['val'], recordistas['Potências 10']['id'] = perc_potencias_10, id_comunidade
        if perc_quadrados > recordistas['Quadrados Perf']['val']:
            recordistas['Quadrados Perf']['val'], recordistas['Quadrados Perf']['id'] = perc_quadrados, id_comunidade
        if perc_fibonacci > recordistas['Fibonacci']['val']:
            recordistas['Fibonacci']['val'], recordistas['Fibonacci']['id'] = perc_fibonacci, id_comunidade

        # Impressão dos Resultados Individuais (NÃO REMOVIDOS)
        print(f"🏘️  COMUNIDADE {id_comunidade} (Tamanho: {len(lista_nos)} vértices)")
        print(f"   -> 🔢 Pares:         {perc_pares:.1f}% (da comunidade)")
        print(f"   -> 🔢 Ímpares:       {perc_impares:.1f}% (da comunidade)")
        print(f"   -> ⭐ Primos:        {perc_primos:.1f}% (de TODOS os primos da rede)")
        print(f"   -> ➖ Negativos:     {perc_negativos:.1f}% (de TODOS os negativos da rede)")
        print(f"   -> ⚡ Potências 2:   {perc_potencias_2:.1f}% (de TODAS as potências de 2 da rede)")
        print(f"   -> 🔟 Potências 10:  {perc_potencias_10:.1f}% (de TODAS as potências de 10 da rede)")
        print(f"   -> 📐 Quadrados Perf: {perc_quadrados:.1f}% (de TODOS os quadrados da rede)")
        print(f"   -> 🌿 Fibonacci:     {perc_fibonacci:.1f}% (de TODOS os Fibonacci da rede)")
        print("-" * 60)

# ---------------------------------------------------------------------
# NOVO BLOCO FINAL: Exibir o painel geral de recordistas
# ---------------------------------------------------------------------
print("\n" + "=" * 60)
print("🏆 PAINEL DE RECORDISTAS POR CLASSE MATEMÁTICA")
print("   (Análise realizada exclusivamente entre as grandes comunidades)")
print("=" * 60)

for classe, dados in recordistas.items():
    if dados['id'] is not None:
        print(f"👑 Maior % de {classe:14}: Comunidade {dados['id']} -> {dados['val']:.1f}% ({dados['tipo']})")
    else:
        print(f"⚪ Nenhuma comunidade registrou dados para a classe {classe}.")
        
print("=" * 60)