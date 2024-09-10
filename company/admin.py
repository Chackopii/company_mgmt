from django.contrib import admin

# Register your models here.
from .models import Manager,Employee

class ManagerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Manager, ManagerAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Employee, EmployeeAdmin)
