from django.contrib import admin
from .models import *
from django.db.models import Field

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display

@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display =  [field.name for field in self.model._meta.get_fields() if isinstance(field, Field)]
        readonly_fields = ('id', )
        return list_display