import random

class Graph:
    def __init__(self, n, density=0, oriented=True):
        # кількість вершин
        self.n = n
        self.density = density    # щільність графа
        self.oriented = oriented  # орієнтований чи ні

        # матриця суміжності
        self.adj_matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(0)
            self.adj_matrix.append(row)

        # список суміжності
        self.adj_list = []
        for i in range(n):
            self.adj_list.append([])

        # якщо щільність > 0 — генеруємо граф автоматично
        if density > 0:
            self.generate_random_edges()

    # ---------------- ДОДАВАННЯ РЕБРА ----------------

    def add_edge(self, u, v):
        if u == v:
            pass # без петель

        self.adj_matrix[u][v] = 1
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)

        if not self.oriented:
            self.adj_matrix[v][u] = 1
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    # ---------------- ГЕНЕРАЦІЯ ГРАФА ПО ЩІЛЬНОСТІ ----------------

    def generate_random_edges(self):
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if random.random() < self.density:
                        self.add_edge(i, j)

    # ---------------- КОНВЕРСІЇ ----------------

    def matrix_to_list(self):
        new_list = []
        for i in range(self.n):
            new_list.append([])

        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j] == 1:
                    new_list[i].append(j)

        self.adj_list = new_list

    def list_to_matrix(self):
        new_matrix = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append(0)
            new_matrix.append(row)

        for i in range(self.n):
            for j in self.adj_list[i]:
                new_matrix[i][j] = 1
                if not self.oriented:
                    new_matrix[j][i] = 1

        self.adj_matrix = new_matrix

    # ---------------- ВИВІД ----------------

    def print_matrix(self):
        print("Матриця суміжності:")
        for row in self.adj_matrix:
            print(row)
        print()

    def print_list(self):
        print("Список суміжності:")
        for i in range(self.n):
            print(i, ":", self.adj_list[i])
        print()

# Алгоритм Уоршелла для матриці досяжності
    def warshall(self):
        reach = []
        for row in self.adj_matrix:
            reach.append(row)
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if reach[i][k] and reach[k][j]:
                        reach[i][j] = 1
        # Прибираємо петлі (діагональ)
        for i in range(self.n):
            reach[i][i] = 0
        return reach


g = Graph(n=5, density=0.3, oriented=True)

g.print_matrix()
g.print_list()

g.warshall()
g.print_matrix()
