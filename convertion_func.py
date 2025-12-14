# функції, які конвертують списки суміжності в матриці суміжності і навпаки
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