from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'department', 'designation', 'salary', 'date_joined')
    search_fields = ('name', 'email', 'department', 'designation', 'phone')
    list_filter = ('department', 'designation', 'date_joined')
    ordering = ('-date_joined',)
