# функції для запису результатів у файл

def save(results, filename):
    num_of_experiment = find_exp_num(filename)
    with open(filename, "a", encoding="utf-8") as file:
        try:
            # якщо файл пустий - записати ключі
            if num_of_experiment == 0:
                first_iteration = True #для коректного запису
                for key in results:
                    if first_iteration:
                        file.write(f"Experiment,{key}")
                    else:
                        file.write(","+key)
                    first_iteration = False
                file.write("\n")
                num_of_experiment = 1

            # запис результатів
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

# знаходить номер поточного експерименту
def find_exp_num(filename):
    num_of_experiment = 0
    try:
        with open(filename, "r", encoding="utf-8")as file:
            try:
                num_of_experiment = len(file.readlines())
            except Exception as e:
                print(e)
    # якщо файлу не існує - створити
    except FileNotFoundError:
        open(filename, "w").close()
    return num_of_experiment

# красиво називає файл
def name_file(num_v, density, static):
    if static == "density":
        filename = f"results_d_{density}.csv"
    elif static == "vertexes":
        filename = f"results_v_{num_v}.csv"
    else:
        filename = f"results_v_{num_v}_d_{density}.csv"
    return filename