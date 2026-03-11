from django.contrib import admin

from .models import Algorithm

@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')