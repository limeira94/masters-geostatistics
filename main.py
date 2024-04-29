import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Dados
data = pd.read_excel('data/dados_interpolados.xlsx')

# Calcular a média dos valores reais para cada ponto para todos os parâmetros
real_values = data.groupby('pontos').agg({
    'Temperatura___C_': 'mean',
    'Pressão__hPa_': 'mean',
    'Umidade____': 'mean',
    'Pto__Orvalho___C_': 'mean'
}).reset_index()

# Mapear os métodos de interpolação
data['Method'] = data['SrcID_Rast'].map({0: 'LPI', 1: 'IDW', 2: 'GPI', 3: 'RBF'})

# Agrupar os dados por ponto e método, calcular a média dos erros
plot_data = data.groupby(['pontos', 'Method']).agg({
    'Erro_Absoluto_temp': 'mean',
    'Erro_Absoluto_pressao': 'mean',
    'Erro_Absoluto_umidade': 'mean',
    'Erro_Absoluto_ponto_orv': 'mean'
}).reset_index()

print(real_values.columns)

# Incorporar valores reais ao DataFrame
real_values = real_values.rename(columns={
    'Temperatura___C_': 'Real_Temperatura',
    'Pressão__hPa_': 'Real_Pressão',
    'Umidade____': 'Real_Umidade',
    'Pto__Orvalho___C_': 'Real_Pto_Orvalho'
})
plot_data_extended = pd.merge(plot_data, real_values, on='pontos', how='left')
print(real_values.columns)
# Criar os gráficos com valores reais incluídos
fig, axes = plt.subplots(4, 1, figsize=(12, 24))

# Configurar cores
colors = ['skyblue', 'orange', 'green', 'red', 'purple']

for i, (param, error_col) in enumerate(zip(['Temperatura', 'Pressão', 'Umidade', 'Pto_Orvalho'],
                                           ['Erro_Absoluto_temp', 'Erro_Absoluto_pressao', 'Erro_Absoluto_umidade', 'Erro_Absoluto_ponto_orv'])):
    print(param, error_col)
    sns.barplot(data=plot_data_extended, x='pontos', y=error_col, hue='Method', ax=axes[i], palette=colors[:-1])
    axes[i].bar(real_values['pontos'] - 0.2, real_values['Real_' + param], color=colors[-1], width=0.2, label='Valor Real')
    axes[i].set_title(f'Erro Absoluto e Valor Real da {param} por Ponto')
    axes[i].legend(loc='upper right')
    
    
plt.tight_layout()

# Salvar o gráfico
plt.savefig('result/graph_interp.png', dpi=300)  # Modifique o caminho conforme necessário


