import time


def calculate_makespan(matrix, order):

    n = len(order)
    m = len(matrix[0])

    C = [[0] * m for _ in range(n)]

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

        for i, job in enumerate(order):

            if i == 0:
                start = C[i][j] - matrix[job][j]
            else:
                start = max(C[i-1][j], C[i][j-1] - matrix[job][j])

            if start > prev_finish:
                idle += start - prev_finish

            prev_finish = start + matrix[job][j]

    return idle


def johnson_order(matrix):

    n = len(matrix)

    jobs = list(range(n))

    left = []
    right = []

    remaining = jobs.copy()

    while remaining:

        min_time = float("inf")
        min_job = None
        min_machine = None

        for j in remaining:

            if matrix[j][0] < min_time:
                min_time = matrix[j][0]
                min_job = j
                min_machine = 0

            if matrix[j][1] < min_time:
                min_time = matrix[j][1]
                min_job = j
                min_machine = 1

        if min_machine == 0:
            left.append(min_job)
        else:
            right.insert(0, min_job)

        remaining.remove(min_job)

    return left + right


def run(matrix, criterion='makespan'):

    start_time = time.time()

    n = len(matrix)
    m = len(matrix[0])

    if m != 2:
        raise ValueError("Алгоритм Джонсона работает только для 2 станков")

    order = johnson_order(matrix)

    makespan, C = calculate_makespan(matrix, order)

    idle = compute_idle(matrix, order)

    if criterion == 'makespan':
        score = makespan
    elif criterion == 'idle':
        score = idle
    else:
        score = makespan + idle

    details = "Алгоритм Джонсона\n\n"

    details += f"Оптимальный порядок деталей: {[i+1 for i in order]}\n"
    details += f"Длительность производственного цикла : {makespan}\n"
    details += f"Общее время простоя оборудования: {idle}\n"
    details += f"Критерий: {criterion}\n"

    calc_time = round(time.time() - start_time, 4)

    return order, makespan, details, calc_time