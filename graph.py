import random
import networkx as nx
import matplotlib.pyplot as plt
import time

def save(results, filename):
    num_of_experiment = 0
    content = ""
    try:
        with open(filename, "r", encoding="utf-8")as file:
            try:
                content = file.readlines()
                num_of_experiment = len(content)
            except Exception as e:
                print(e)
    except FileNotFoundError:
        open(filename, "w", encoding="utf-8").close()


    with open(filename, "a", encoding="utf-8") as file:
        try:
            if content == [] or content == "":
                first_iteration = True
                for key in results:
                    if first_iteration:
                        file.write(f"Experiment,{key}")
                    else:
                        file.write(","+key)
                    first_iteration = False
                file.write("\n")
                num_of_experiment = 1

            first_iteration = True
            for value in results.values():
                if first_iteration:
                    file.write(f"{str(num_of_experiment)},{value}")
                else:
                    file.write(","+str(value))

                first_iteration = False
            file.write("\n")

        except Exception as e:
            print(e)



def matrix_to_list(adj_matrix):
    adj_list = []
    n = len(adj_matrix)
    for i in range(n):
        adj_list.append([])
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] == 1:
                adj_list[i].append(j)
    return adj_list

def list_to_matrix(adj_list, is_oriented=False):
    adj_matrix = []
    n = len(adj_list)
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        adj_matrix.append(row)

    for i in range(n):
        for j in adj_list[i]:
            adj_matrix[i][j] = 1
            if not is_oriented:
                adj_matrix[j][i] = 1
    return adj_matrix


class Graph:
    def __init__(self, n, density=0.0, oriented=True):
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

        self.reach_matrix = []
        self.warshall_time = 0
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

    def add_vertex(self):
        self.n += 1
        v = self.n
        self.adj_list.append([])
        for i in range(self.n):
            if i < (self.n - 1):
                self.adj_matrix[i].append(0)
            else:
                row = []
                for j in range(self.n):
                    row.append(0)
                self.adj_matrix.append(row)
    # ---------------- ГЕНЕРАЦІЯ ГРАФА ПО ЩІЛЬНОСТІ ----------------

    def generate_random_edges(self):
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if random.random() < self.density:
                        self.add_edge(i, j)

    # ---------------- КОНВЕРСІЇ ----------------

    # ---------------- ВИВІД ----------------

    def print_matrix(self):
        print("Матриця:")
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
            reach.append(row[:])
        start_time = time.time()
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if reach[i][k] and reach[k][j]:
                        reach[i][j] = 1
        # додаємо діагональ
        for i in range(self.n):
            reach[i][i] = 1
        end_time = time.time()
        total_time = end_time - start_time
        self.reach_matrix = reach
        self.warshall_time = round(total_time * 1e6, 2)

    def print_reach_matrix(self):
        print("Матриця досяжності:")
        for row in self.reach_matrix:
            print(row)
        print()

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


        plt.figure(figsize=(8, 5))
        plt.title("Граф")
        pos = nx.spring_layout(g_graph)
        nx.draw(g_graph, pos, with_labels=True, node_color='lightblue', node_size=1000, arrowstyle='->', arrowsize=20)


        plt.figure(figsize=(8, 5))
        plt.title("Граф досяжності")
        nx.draw(g_reach_graph, pos, with_labels=True, node_color='lightblue', node_size=1000, arrowstyle='->', arrowsize=20)

        plt.show()

def run_experiment(num_v, density, static=None):
    g = Graph(num_v, density=density)
    num = 20
    if static == "density":
        filename = f"results_d_{density}.csv"
    elif static == "vertexes":
        filename = f"results_v_{num_v}.csv"
    else:
        filename = f"results_v_{num_v}_d_{density}.csv"
    for i in range(num):
        g.warshall()
        results = {"Vertexes": g.n, "Density": g.density, "Time(mcs)": g.warshall_time}
        save(results, filename)


# -------------------- ДОСЛІДИ ------------------------------

 # Для кожної пари значень (кількість вершин, щільність) проводиться 10 експериментів
 #     num_of_experiments - змінна яка визначає цю кількість
num_of_experiments = 10


 # ДОСЛІД 1: стала щільність(0.3),
 #           кількість вершин варіюється від 20 до 200 з кроком 20
 #                          v_list - список кількостей вершин, для яких будуть проводитись експерименти
 #                          напр. v = [20, 40, 80, ......, 200]

v_list = [i for i in range(20, 201, 20)]
g_density = 0.3
for i in range(num_of_experiments):
    g_v = v_list[i]
    run_experiment(g_v, g_density, static="density")

 # ДОСЛІД 2: стала кількість вершин(200),
 #           щільність варіюється від 0.10 до 0.70 з кроком 0.05
 #                          d_list - список кількостей вершин, для яких будуть проводитись експерименти
 #                          напр. d_list = [0.10, 0.15, 0.20, ......, 0.70]
g_v = 200
d_list = [i/100 for i in range(10, 75, 5)]
for i in range(num_of_experiments):
    g_density = d_list[i]
    run_experiment(g_v, g_density, static="vertexes")
