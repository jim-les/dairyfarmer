from django.contrib import admin
from .models import PendingTask, MilkRecord, VaccinatedCow

class PendingTaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'due_date', 'is_completed')
    search_fields = ('task_name',)

class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ('cow_name', 'litres', 'delivery_date')
    list_filter = ('delivery_date',)
    search_fields = ('cow_name',)

class VaccinatedCowAdmin(admin.ModelAdmin):
    list_display = ('cow_name', 'vaccine_date')
    search_fields = ('cow_name',)

# Register your models with the custom admin classes
admin.site.register(PendingTask, PendingTaskAdmin)
admin.site.register(MilkRecord, MilkRecordAdmin)
admin.site.register(VaccinatedCow, VaccinatedCowAdmin)
