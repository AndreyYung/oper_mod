import importlib.util
import sys
import json
import time
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from .models import Algorithm
from .utils import load_matrix_from_post 




def index(request):
    
    algs = Algorithm.objects.filter(is_active=True)

    context = {
        'algorithms': algs  
    }

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        try:
            
            df = pd.read_excel(file, header=None)

            
            matrix = df.fillna(0).astype(int).values.tolist()

            context.update({
                'matrix': matrix,
                'n': len(matrix),
                'm': len(matrix[0]) if len(matrix) > 0 else 0
            })

        except Exception as e:
            context.update({
                'error': f"Ошибка при чтении Excel: {str(e)}"
            })

    return render(request, 'main/index.html', context)




def calculation(request):
    context = {}

    if request.method == 'POST':

        algorithm_id = request.POST.get('algorithm_id')
        criterion = request.POST.get('criterion', 'makespan')
        n_jobs = int(request.POST.get('n_jobs', 3))
        m_machines = int(request.POST.get('m_machines', 3))

        matrix = []
        for i in range(n_jobs):
            row = []
            for j in range(m_machines):
                val = request.POST.get(f'cell_{i}_{j}', 0)
                try:
                    val = int(val)
                except:
                    val = 0
                row.append(val)
            matrix.append(row)

        context.update({'matrix': matrix, 'n': n_jobs, 'm': m_machines})

        algorithm = get_object_or_404(Algorithm, id=algorithm_id)
        context['algorithm_name'] = algorithm.name


        spec = importlib.util.spec_from_file_location("algo_module", algorithm.script.path)
        algo_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(algo_module)

        run_func = getattr(algo_module, algorithm.function_name)


        start_time = time.time()
        best_order, makespan, details, calc_time = run_func(matrix, criterion)
        calc_time = round(time.time() - start_time, 4)

        context.update({
            'order': [i+1 for i in best_order],  # номера деталей с 1
            'makespan': makespan,
            'details': details,
            'calc_time': calc_time
        })


        n = len(matrix)
        m = len(matrix[0])
        C = [[0]*m for _ in range(n)]
        for i, job in enumerate(best_order):
            for j in range(m):
                if i==0 and j==0:
                    C[i][j] = matrix[job][j]
                elif i==0:
                    C[i][j] = C[i][j-1] + matrix[job][j]
                elif j==0:
                    C[i][j] = C[i-1][j] + matrix[job][j]
                else:
                    C[i][j] = max(C[i-1][j], C[i][j-1]) + matrix[job][j]


        gantt_data = []

        for j in range(m): 
            for i, job in enumerate(best_order):  

                duration = matrix[job][j]
                finish = C[i][j]
                start = finish - duration

                gantt_data.append({
                    'job': f'Деталь {job+1}',
                    'machine': f'Станок {j+1}',
                    'start': start,
                    'duration': duration
                })

        context['gantt_data'] = gantt_data


        machine_loads = []
        for j in range(m):
            load = sum(matrix[job][j] for job in best_order)
            machine_loads.append({
                'machine': f'Станок {j+1}',
                'load': load,
                'efficiency': round(load / makespan * 100, 2)
            })
        context['machine_loads'] = machine_loads
    print(context)

    return render(request, 'main/calculation.html', context)




