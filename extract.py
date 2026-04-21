import csv

input_file = 'data'
output_file = 'all_network.csv'

edges = {}

print("Processando sequências...")

with open(input_file, 'r') as f:
    for line in f:

        # Pula comentários ou linhas vazias
        if line.startswith('#') or not line.strip():
            continue
        
        # O primeiro item é o ID da sequência (ex: A000001), os outros são os números.
        parts = line.strip().split(',')
        
        sequence = [p.strip() for p in parts[1:] if p.strip()]
        
        # Percorre a sequência criando conexões entre vizinhos diretos
        for i in range(len(sequence) - 1):
            u = sequence[i]
            v = sequence[i+1]
            
            # Adicionamos como uma tupla no dicionário
            edge = (u, v)
            if edge not in edges:
                edges[edge] = True

# Salva o resultado em um CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Source', 'Target'])
    for edge in edges.keys():
        writer.writerow(edge)

print(f"Pronto! Arquivo '{output_file}' criado.")
