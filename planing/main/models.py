from django.db import models

class Algorithm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    script = models.FileField(upload_to='algorithms/', verbose_name="Python-файл")
    
    function_name = models.CharField(max_length=50, default='run', verbose_name="Имя функции")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Алгоритм"
        verbose_name_plural = "Алгоритмы"