import json
from datetime import datetime, timedelta

def prepare_gantt_data(C, order, matrix):
    """
    C - матрица окончаний (n x m)
    order - список индексов деталей в порядке запуска
    matrix - исходная матрица (для определения цветов и т.п.)
    возвращает список задач для Frappe Gantt
    """
    tasks = []
    base_date = datetime(2025, 1, 1)
    # Простая палитра (можно расширить)
    colors = ['#ff9999', '#99ff99', '#9999ff', '#ffff99', '#ff99ff', '#99ffff', '#ffb366', '#c2c2f0', '#ffb3ba', '#baffc9']
    for i, job in enumerate(order):
        start_time = 0
        for j in range(len(matrix[0])):
            end_time = C[i][j]
            start_date = base_date + timedelta(hours=start_time)
            end_date = base_date + timedelta(hours=end_time)
            tasks.append({
                'id': f'job{job}_machine{j}',
                'name': f'Деталь {job+1}',
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'progress': 100,
                'style': f'background-color: {colors[job % len(colors)]};',
            })
            start_time = end_time
    return tasks