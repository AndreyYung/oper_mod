import json
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # header=None → первая строка считается данными
        df = pd.read_excel(file, header=None)

        matrix = df.values.tolist()

        context = {
            'matrix': matrix,
            'n': len(matrix),
            'm': len(matrix[0]) if matrix else 0
        }

        return render(request, 'main/index.html', context)

    return render(request, 'main/index.html')



