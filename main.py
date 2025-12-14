from file_work import save, name_file, add_to_final
from graph import Graph

# Для кожної пари значень провести num експериментів
def run_experiment(num_v, density, static=""):
    num = 20
    filename = name_file(num_v, density, static)
    for i in range(num):
        g = Graph(num_v, density=density)
        g.warshall()
        results = {"Vertexes": g.n, "Density": g.density, "Time(mcs)": g.warshall_time}
        # зберігаємо результати в файл
        save(results, filename)
        save(results, "final_results.csv")

 # -------------------- ДОСЛІДИ ------------------------------
 # ДОСЛІД 1: 3 варіанти досліду для сталих щільностей (0.3, 0.5, 0.7)
 #           кількість вершин варіюється від 20 до 200 з кроком 20
 #                          v_list - список кількостей вершин, для яких будуть проводитись експерименти
 #                          напр. v = [20, 40, 80, ......, 200]

v_list = [i for i in range(20, 201, 20)]
d_list = [0.3, 0.5, 0.7]
for d in d_list:
    for v in v_list:
        run_experiment(v, d, static="density")

 # ДОСЛІД 2: стала кількість вершин(200),
 #           щільність варіюється від 0.10 до 0.55 з кроком 0.05
 #                          d_list - список кількостей вершин, для яких будуть проводитись експерименти
 #                          напр. d_list = [0.10, 0.15, 0.20, ......, 0.55]
v = 200
d_list = [i/100 for i in range(10, 55, 5)]
for d in d_list:
    run_experiment(v, d, static="vertexes")

# всі результати в один файл
# unite(results_file)