import random
import networkx as nx
import matplotlib.pyplot as plt
import time

class Graph:
    def __init__(self, n, density=0.0, oriented=True):
        # кількість вершин, щільність, чи орієнтований
        self.n = n
        self.density = density
        self.oriented = oriented

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

        # генерація графа
        self.generate_random_edges()

        self.reach_matrix = []
        self.warshall_time = 0

    # додавання ребра
    def add_edge(self, u, v):
        # перевірка на наявність вершин
        if u > (self.n - 1) or v > (self.n - 1):
            print("impossible to add this edge. this vertexes don't exist")
            raise ValueError
        if u == v:
            pass # без петель
        self.adj_matrix[u][v] = 1
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        # якщо граф неорієнтований, видалення ще однієї пару значень
        if not self.oriented:
            self.adj_matrix[v][u] = 1
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    # додавання вершини
    def add_vertex(self):
        self.n += 1
        self.adj_list.append([])
        for i in range(self.n):
            if i < (self.n - 1):
                self.adj_matrix[i].append(0)
            else:
                row = []
                for j in range(self.n):
                    row.append(0)
                self.adj_matrix.append(row)

    # видалення ребра
    def remove_edge(self, u, v):
        # перевірка на наявність вершин
        if u > (self.n - 1) or v > (self.n - 1):
            print("impossible to remove this edge. this vertexes don't exist")
            raise ValueError
        self.adj_matrix[u][v] = 0
        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)
        if not self.oriented:
            self.adj_matrix[v][u] = 0
            if u not in self.adj_list[v]:
                self.adj_list[v].remove(u)

    # видалення вершини
    def remove_vertex(self):
        self.n -= 1
        adj_matrix = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append(self.adj_matrix[i][j])
            adj_matrix.append(row)
        self.adj_matrix = adj_matrix
        self.adj_list = self.adj_list[:-1]


    # генерація графа з випадковими ребрами
    def generate_random_edges(self):
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if random.random() < self.density:
                        self.add_edge(i, j)

    # вивід матриці
    def print_matrix(self):
        print("Матриця:")
        for row in self.adj_matrix:
            print(row)
        print()

    # вивід списку
    def print_list(self):
        print("Список суміжності:")
        for i in range(self.n):
            print(i, ":", self.adj_list[i])
        print()

    # Алгоритм Уоршелла для матриці досяжності
    def warshall(self):
        reach = []
        for row in self.adj_matrix:
            reach.append(row[:])
        # час
        start_time = time.time()
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if reach[i][k] and reach[k][j]:
                        reach[i][j] = 1
        # діагональ
        for i in range(self.n):
            reach[i][i] = 1
        end_time = time.time()
        total_time = end_time - start_time
        self.reach_matrix = reach
        self.warshall_time = round(total_time * 1e6, 2)

    # вивід матриці досяжності
    def print_reach_matrix(self):
        print("Матриця досяжності:")
        for row in self.reach_matrix:
            print(row)
        print()

    #візуалізація графа та графа досяжності
    def visualize(self):
        g_graph = nx.DiGraph()  # орієнтований граф
        g_reach_graph = nx.DiGraph()
        for i in range(self.n):
            g_graph.add_node(i)
            g_reach_graph.add_node(i)
        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j] == 1:
                    g_graph.add_edge(i, j)
                if self.reach_matrix[i][j] == 1:
                    g_reach_graph.add_edge(i, j)

        # наступний код генерував Chatgpt
        plt.figure(figsize=(8, 5))
        plt.title("Граф")
        pos = nx.spring_layout(g_graph)
        nx.draw(g_graph, pos, with_labels=True, node_color='lightblue', node_size=1000, arrowstyle='->', arrowsize=20)


        plt.figure(figsize=(8, 5))
        plt.title("Граф досяжності")
        nx.draw(g_reach_graph, pos, with_labels=True, node_color='lightblue', node_size=1000, arrowstyle='->', arrowsize=20)

        plt.show()



