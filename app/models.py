from django.db import models
from django.utils import timezone

# Create your models here.

class PendingTask(models.Model):
    task_name = models.CharField(max_length=255)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
    
    
class MilkRecord(models.Model):
    cow_name = models.CharField(max_length=100)
    litres = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()

    def __str__(self):
        return f"{self.cow_name}: {self.litres}L on {self.delivery_date}"

        
class VaccinatedCow(models.Model):
    cow_name = models.CharField(max_length=100)
    vaccine_date = models.DateField()

    def __str__(self):
        return f"{self.cow_name} - {self.vaccine_date}"