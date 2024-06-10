import numpy as np

# Coordenadas das amostras
coords = np.array([
    [2, 3],  # Ponto A
    [2, 1],  # Ponto B
    [1, 2],  # Ponto C
    [3, 2]   # Ponto D
])

# Valores das amostras
values = np.array([37, 36, 38, 35])

# Ponto de interesse "X"
point_x = np.array([2, 2])

# Parâmetros do variograma exponencial
C0 = 0
C = 6
a = 300

# Função do variograma exponencial
def variogram_exponential(h, C0, C, a):
    return C0 + C * (1 - np.exp(-h / a))

# Distância euclidiana
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Montar a matriz de variância
n = len(coords)
gamma = np.zeros((n+1, n+1))
for i in range(n):
    for j in range(n):
        h = euclidean_distance(coords[i], coords[j])
        gamma[i, j] = variogram_exponential(h, C0, C, a)

# Termos adicionais para a krigagem
gamma[:-1, -1] = 1
gamma[-1, :-1] = 1
gamma[-1, -1] = 0

# Vetor de variância entre o ponto "X" e as amostras
gamma_x = np.zeros(n+1)
for i in range(n):
    h = euclidean_distance(coords[i], point_x)
    gamma_x[i] = variogram_exponential(h, C0, C, a)
gamma_x[-1] = 1

# Resolver o sistema de equações
weights = np.linalg.solve(gamma, gamma_x)

# Estimar o valor no ponto "X"
Z_x = np.sum(weights[:-1] * values)

# Mostrar os resultados
print("Matriz de Variância (gamma):")
print(gamma)

print("\nVetor de Variância (gamma_x):")
print(gamma_x)

print(f"\nEstimativa no ponto X: {Z_x}")
