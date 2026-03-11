from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('calculation/', views.calculation, name='calculation')
    
    #path('', views.upload_excel, name='upload_excel'),
]