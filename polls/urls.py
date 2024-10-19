from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('chart-data/', views.chart_view, name='chart_data'),
    path('disk-data/', views.disk_view, name='disk_data'),
    path('cpu-data/', views.cpu_view, name='cpu_data'),
    path('ram-data/', views.ram_view, name='ram_data'),
    path('db-data/', views.db_view, name='db_data'),
    path('api-data/', views.api_view, name='api_data'),
]
from django.http import HttpResponse