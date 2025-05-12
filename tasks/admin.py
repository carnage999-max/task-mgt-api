from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'status', 'priority', 'deadline']
    list_filter = ['status', 'priority', ]
    search_fields = ['name', 'description']
    ordering = ['-created_at']
