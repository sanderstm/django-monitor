from django.core.management.base import BaseCommand
from django.utils import timezone
import random
import time  # Asegúrate de importar el módulo time
import psutil
from polls.models import Disk, CPU, RAM

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            # disk
            diskPs = psutil.disk_usage('/')

            total_disk = format(diskPs.total / (1024 ** 3),".2f")
            free_disk = format(diskPs.free / (1024 ** 3),".2f")
            used_disk = format(diskPs.used / (1024 ** 3),".2f")

            disk = Disk(total_disk=total_disk, free_disk=free_disk, used_disk=used_disk, created_at=timezone.now())
            disk.save()
            print(f"Nuevo registro agregado: {total_disk}")
            
            # cpu
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            
            total_usage = (sum(cpu_per_core)) / len(cpu_per_core)  # Promedio simple

            cpu = CPU(
                cores = ",".join(str(c) for c in cpu_per_core),
                total_usage=total_usage,
                created_at=timezone.now()
            )
            cpu.save()
            print(f"Nuevo registro agregado a CPU: {cpu}")

            # ram
            ram = psutil.virtual_memory()
            total_ram = format(ram.total / (1024 ** 3),".2f")  # Total de RAM en GB
            free_ram = format(ram.available  / (1024 ** 3),".2f")# Genera un valor aleatorio para RAM libre
            used_ram = format(ram.used / (1024 ** 3),".2f")  # Calcula la RAM usada

            ramm = RAM(total_ram=total_ram, free_ram=free_ram, used_ram=used_ram, created_at=timezone.now())
            ramm.save()
            print(f"Nuevo registro agregado a RAM: {ramm}")
            
            time.sleep(2)