# petr.py
import time

def calculate_makespan(matrix, order):

    n = len(order)
    m = len(matrix[0])
    C = [[0]*m for _ in range(n)]

    for i in range(n):
        job = order[i]
        for j in range(m):
            if i == 0 and j == 0:
                C[i][j] = matrix[job][j]
            elif i == 0:
                C[i][j] = C[i][j-1] + matrix[job][j]
            elif j == 0:
                C[i][j] = C[i-1][j] + matrix[job][j]
            else:
                C[i][j] = max(C[i-1][j], C[i][j-1]) + matrix[job][j]

    makespan = C[-1][-1]
    return makespan, C

def compute_idle(matrix, order):

    n = len(order)
    m = len(matrix[0])
    makespan, C = calculate_makespan(matrix, order)

    idle = [[0]*m for _ in range(n)]
    for i in range(n):
        job = order[i]
        for j in range(m):
            start_time = 0
            if i > 0:
                start_time = max(start_time, C[i-1][j])
            if j > 0:
                start_time = max(start_time, C[i][j-1] - matrix[job][j])
            idle[i][j] = max(0, start_time - (C[i-1][j] if i>0 else 0))
    total_idle = sum(sum(row) for row in idle)
    return total_idle

def run(matrix, criterion='makespan'):

    start_time = time.time()
    n = len(matrix)
    m = len(matrix[0])

    S1 = [(i, sum(matrix[i][1:])) for i in range(n)]  
    S2 = [(i, sum(matrix[i][:-1])) for i in range(n)] 

    order1 = [i for i, _ in sorted(S1, key=lambda x: x[1], reverse=True)]
    order2 = [i for i, _ in sorted(S2, key=lambda x: x[1])]
    diffs = [(i, S1[i][1] - S2[i][1]) for i in range(n)]
    order3 = [i for i, _ in sorted(diffs, key=lambda x: x[1], reverse=True)]


    variants = []
    for ord_ in [order1, order2, order3]:
        makespan, _ = calculate_makespan(matrix, ord_)
        idle = compute_idle(matrix, ord_)
        if criterion == 'makespan':
            score = makespan
        elif criterion == 'idle':
            score = idle
        else:  
            score = makespan + idle
        variants.append((score, ord_, makespan, idle))


    best_variant = min(variants, key=lambda x: x[0])
    best_order = best_variant[1]
    best_makespan = best_variant[2]
    best_idle = best_variant[3]


    details = "Метод Петрова-Соколицына\nРассмотрены порядки:\n"
    for score, ord_, mk, idl in variants:
        details += f"  Порядок: {[i+1 for i in ord_]}, Длительность производственного цикла={mk}, Общее время простоя оборудования={idl}\n"
    details += f"Выбран порядок: {[i+1 for i in best_order]}, Длительность производственного цикла={best_makespan}, Итоговое общее время простоя оборудования={best_idle}"

    calc_time = round(time.time() - start_time, 4)

    return best_order, best_makespan, details, calc_time