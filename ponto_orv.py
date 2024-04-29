import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
file_path = 'data/dados_interpolados.xlsx'  # Substitua pelo caminho correto do arquivo
data = pd.read_excel(file_path)

interp_mapping = {
    0: 'LPI',
    1: 'IDW',
    2: 'GPI',
    3: 'RBF'
}

# Preparar os dados para plotagem, assumindo que 'data' já contém as colunas necessárias
temperature_data = data[['pontos', 'Pto__Orvalho___C_', 'Ponto_Orv_interp', 'SrcID_Rast']].copy()
temperature_data['Valor_Real'] = temperature_data.groupby('pontos')['Pto__Orvalho___C_'].transform('mean')
plot_data = temperature_data.drop(columns='Pto__Orvalho___C_').drop_duplicates()

# Expansão dos dados para a plotagem lado a lado
expanded_data = []
for i in plot_data['pontos'].unique():
    temp_real = plot_data[plot_data['pontos'] == i]['Valor_Real'].iloc[0]
    methods_data = plot_data[plot_data['pontos'] == i]
    for index, row in methods_data.iterrows():
        expanded_data.append({
            'Ponto': i,
            'Ponto_orv': row['Ponto_Orv_interp'],
            'Tipo': f"{interp_mapping[row['SrcID_Rast']]}"
        })
    expanded_data.append({
        'Ponto': i,
        'Ponto_orv': temp_real,
        'Tipo': 'Valor Real'
    })

expanded_df = pd.DataFrame(expanded_data)

# Criação do gráfico
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(x='Ponto', y='Ponto_orv', hue='Tipo', data=expanded_df, ax=ax, palette='viridis')

ax.set_title('Comparação da Interpolação do Pto. Orvalho e Valor Real por Ponto')
ax.set_ylabel('Pto. Orvalho (°C)')
ax.set_xlabel('Ponto')
ax.set_ylim([0, 30])
plt.legend(loc='upper right')
plt.savefig('result/graph_ponto_orv.png', dpi=300)
