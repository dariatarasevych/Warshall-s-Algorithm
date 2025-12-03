import random

# --- Клас графа ---
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_matrix = [[0]*vertices for _ in range(vertices)]

    # Додаємо ребро
    def add_edge(self, u, v):
        self.adj_matrix[u][v] = 1

    # Перетворюємо матрицю на список суміжності
    def to_adj_list(self):
        adj_list = {}
        for i in range(self.V):
            adj_list[i] = [j for j, val in enumerate(self.adj_matrix[i]) if val != 0]
        return adj_list

    # Алгоритм Уоршелла для матриці досяжності
    def warshall(self):
        reach = [row[:] for row in self.adj_matrix]
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if reach[i][k] and reach[k][j]:
                        reach[i][j] = 1
        # Прибираємо петлі (діагональ)
        for i in range(self.V):
            reach[i][i] = 0
        return reach

# --- Генерація випадкового графа без петель ---
num_vertices = 5  # можна змінити кількість вершин
g = Graph(num_vertices)

# Рандомно додаємо ребра без петель
for i in range(num_vertices):
    for j in range(num_vertices):
        if i != j:  # не дозволяємо петлі
            g.adj_matrix[i][j] = random.randint(0, 1)

# --- Вивід ---
print("Матриця суміжності:")
for row in g.adj_matrix:
    print(row)

adj_list = g.to_adj_list()
print("\nСписок суміжності:")
for node, neighbors in adj_list.items():
    print(node, "->", neighbors)

closure = g.warshall()
print("\nМатриця досяжності (Уоршелл) без петель:")
for row in closure:
    print(row)



