from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import random
import psutil
from .models import Disk, CPU, RAM
import json 
from django.db import connection, OperationalError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
import time
def last_disk_view(request):
    last_disk = Disk.objects.last()
    if last_disk is not None:
        data = {
            "total": last_disk.used_disk + last_disk.free_disk,
            "data": {
                "used": last_disk.used_disk,
                "free": last_disk.free_disk
            }
        }

        # Enviar datos por WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'monitor_group',  # Nombre del grupo de WebSocket
            {
                'type': 'send_data',
                'data': data
            }
        )

        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'No Disk records found.'}, status=404)

def chart_view(request):
    
    labels = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    data = [random.randint(0, 100) for _ in labels]

    return JsonResponse({
        'labels': labels,
        'data': data,
    })
    
def disk_view(request):
    last_disk = Disk.objects.last()

    return JsonResponse({
        "total": last_disk.used_disk+last_disk.free_disk,
        "data":{
            "used":last_disk.used_disk,
            "free":last_disk.free_disk
        }
    })
    
def ram_view(request):
    
    last_rams = RAM.objects.order_by('-created_at')[:7][::-1]
    returns = [[],[]]
    for c in range(len(last_rams)):
        returns[0].append(last_rams[c].used_ram) 
        returns[1].append(last_rams[c].free_ram) 
        
    return JsonResponse({
        "total":last_rams[0].used_ram + last_rams[0].free_ram,
        "data":returns
    })
    
def cpu_view(request):
    
    last_cpus = CPU.objects.order_by('-created_at')[:7][::-1]
    num_cores = len(last_cpus[0].cores.split(','))
        
    returns = []
    for i in range(num_cores):
        returns.append([])
    
    for c in range(len(last_cpus)):
        cores = [float(x) for x in last_cpus[c].cores.split(',')]
        for n in range(num_cores):
            returns[n].append(cores[n]) 
    return JsonResponse({
        "data":returns,
    })
        
def db_view(request):  
    status = None
    try:
        connection.ensure_connection()
        status = True
    except:
        status = False
    return JsonResponse({
        "data":  status
    })

        
def api_view(request):  
    url = request.GET.get('url')
    if not url:
        url = "https://github.com/"

    # Inicializa las variables de respuesta y tiempo
    status_code = None
    response_time = None

    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000 
        status_code = response.status_code
        print(f"Estado: {status_code}")
        print(f"Tiempo de respuesta: {response_time:.2f} ms")
        
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        status_code = 500 
        response_time = None

    return JsonResponse({
        "status": status_code,
        "ms": response_time,
        "url": url
    })
    
def index(request):
    return render(request, 'index.html')