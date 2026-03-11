# branch_and_bound.py
import time
import itertools


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

    return C[-1][-1], C


def compute_idle(matrix, order):

    n = len(order)
    m = len(matrix[0])

    makespan, C = calculate_makespan(matrix, order)

    idle = 0

    for j in range(m):

        prev_finish = 0

        for i in range(n):

            start = 0

            if i > 0:
                start = max(start, C[i-1][j])

            if j > 0:
                start = max(start, C[i][j-1] - matrix[order[i]][j])

            idle += max(0, start - prev_finish)

            prev_finish = start + matrix[order[i]][j]

    return idle


def run(matrix, criterion="makespan"):


    start_time = time.time()

    n = len(matrix)

    jobs = list(range(n))

    best_score = float("inf")
    best_order = None
    best_makespan = None
    best_idle = None

    details = "Метод ветвей и границ\n\n"

    for perm in itertools.permutations(jobs):

        order = list(perm)

        makespan, _ = calculate_makespan(matrix, order)

        idle = compute_idle(matrix, order)

        if criterion == "makespan":
            score = makespan

        elif criterion == "idle":
            score = idle

        else:
            score = makespan + idle

        details += f"Порядок: {[i+1 for i in order]} | Длительность производственного цикла={makespan} | Простои={idle}\n"

        if score < best_score:

            best_score = score
            best_order = order
            best_makespan = makespan
            best_idle = idle

    details += "\nЛучший найденный порядок:\n"
    details += f"{[i+1 for i in best_order]}\n"
    details += f"Длительность производственного цикла = {best_makespan}\n"
    details += f"Общее время простоя оборудования = {best_idle}\n"

    calc_time = round(time.time() - start_time, 4)

    return best_order, best_makespan, details, calc_time