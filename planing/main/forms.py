from django import forms

class InputDataForm(forms.Form):
    # Способ ввода
    INPUT_CHOICES = [
        ('manual', 'Ручной ввод'),
        ('file', 'Загрузить Excel'),
        ('random', 'Случайная генерация'),
    ]
    input_method = forms.ChoiceField(choices=INPUT_CHOICES, initial='random', label='Способ ввода')

    # Для ручного ввода (можно использовать текстовое поле)
    manual_matrix = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        required=False,
        label='Матрица длительностей',
        help_text='Введите строки через точку с запятой, числа через пробел. Например: "3 5; 6 4"'
    )

    # Загрузка файла
    file = forms.FileField(required=False, label='Файл Excel (.xlsx)')

    # Для генерации
    num_jobs = forms.IntegerField(min_value=3, max_value=100, initial=5, label='Количество деталей')
    num_machines = forms.IntegerField(min_value=3, max_value=100, initial=3, label='Количество станков')
    min_duration = forms.IntegerField(min_value=1, initial=1, label='Мин. длительность')
    max_duration = forms.IntegerField(min_value=2, initial=10, label='Макс. длительность')

    # Выбор алгоритма
    ALGORITHM_CHOICES = [
        ('johnson', 'Джонсона (только для 2 станков)'),
        ('petrov', 'Петрова-Соколицина'),
        ('cds', 'CDS (обобщение Джонсона)'),
    ]
    algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES, initial='petrov', label='Алгоритм')