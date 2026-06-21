import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('distancias_do_vertice.csv', dtype=str)
df_filtered = df[df['Distance_From_Source'] != 'Inalcançável'].copy()
df_filtered['Distance_From_Source'] = df_filtered['Distance_From_Source'].astype(float)
df_filtered['Target_Node'] = df_filtered['Target_Node'].astype(float)

# Ordenar do menor para o maior nó
df_sorted = df_filtered.sort_values(by='Target_Node')

# Calcular a média móvel (média a cada 5000 nós) para revelar a tendência
df_sorted['Média_Móvel'] = df_sorted['Distance_From_Source'].rolling(window=5000, min_periods=1).mean()

plt.figure(figsize=(14, 7))
# Plota a evolução
plt.plot(df_sorted['Target_Node'], df_sorted['Média_Móvel'], color='red', linewidth=2, label='Evolução da Distância')
plt.scatter(df_sorted['Target_Node'], df_sorted['Distance_From_Source'], alpha=0.01, s=1, color='gray')

plt.xscale('symlog')
plt.xlabel('Target Node')
plt.ylabel('Distance')
plt.legend()
plt.show()