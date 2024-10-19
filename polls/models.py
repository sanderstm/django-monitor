from django.db import models
from django.utils import timezone

# Create your models here.

class Disk(models.Model):
    total_disk = models.FloatField(verbose_name="Total Disk")
    free_disk = models.FloatField(verbose_name="Free Disk")
    used_disk = models.FloatField(verbose_name="Used Disk")
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")


    class Meta:
        db_table = 'disk'
        verbose_name = 'Disk'
        verbose_name_plural = 'Disks'
        ordering = ['id']

    def __str__(self):
        return f"Disk {self.id}: {self.total_disk} GB Total"



class RAM(models.Model):
    total_ram = models.FloatField(verbose_name="Total RAM (GB)")
    free_ram = models.FloatField(verbose_name="Free RAM (GB)")
    used_ram = models.FloatField(verbose_name="Used RAM (GB)")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    class Meta:
        db_table = 'ram'
        verbose_name = 'RAM'
        verbose_name_plural = 'RAMs'
        ordering = ['id']

    def __str__(self):
        return f"RAM {self.id}: {self.total_ram} GB Total"
    
    
class CPU(models.Model):
    cores = models.CharField(max_length=255,null=True, verbose_name="CPU Name") 
    total_usage = models.FloatField(verbose_name="Total CPU Usage (%)", editable=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    class Meta:
        db_table = 'cpu'
        verbose_name = 'CPU'
        verbose_name_plural = 'CPUs'
        ordering = ['id']

    def __str__(self):
        return f"CPU {self.id}: Total Usage {self.total_usage}%"