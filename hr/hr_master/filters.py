import django_filters
from .models import *
from hr.config import *

class CompanyFilter(BaseFilter) :
    legal_name = django_filters.CharFilter(field_name='legal_name', lookup_expr='iexact')
    npwp = django_filters.CharFilter(field_name='npwp', lookup_expr='exact')
    email = django_filters.CharFilter(field_name='email', lookup_expr='iexact')
    website = django_filters.CharFilter(field_name='website', lookup_expr='iexact')

    class Meta:
        model = Company
        fields = []

class UnitFilter(BaseFilter) :
    class Meta:
        model = Unit
        fields = []

class LevelFilter(BaseFilter) :
    class Meta:
        model = Level
        fields = []

class EmploymentTypeFilter(BaseFilter) :
    class Meta:
        model = EmploymentType
        fields = []

class ShiftFilter(BaseFilter) :
    start_day = django_filters.NumberFilter(field_name='start_day', lookup_expr='exact')
    end_day = django_filters.NumberFilter(field_name='end_day', lookup_expr='exact')

    start_time_gte = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    start_time_lte = django_filters.TimeFilter(field_name='start_time', lookup_expr='lte')

    end_time_gte = django_filters.TimeFilter(field_name='end_time', lookup_expr='gte')
    end_time_lte = django_filters.TimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = Shift
        fields = []

class BranchFilter(BaseFilter) :
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    province = django_filters.CharFilter(field_name='province', lookup_expr='iexact')
    postal_code = django_filters.CharFilter(field_name='postal_code', lookup_expr='iexact')

    class Meta:
        model = Branch
        fields = []

class EmployeeFilter(BaseFilter) :
    user_id = django_filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    nik = django_filters.NumberFilter(field_name='nik', lookup_expr='exact')

    village = django_filters.CharFilter(field_name='village', lookup_expr='iexact')
    district = django_filters.CharFilter(field_name='district', lookup_expr='iexact')
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    province = django_filters.CharFilter(field_name='province', lookup_expr='iexact')
    postal_code = django_filters.CharFilter(field_name='postal_code', lookup_expr='iexact')

    religion = django_filters.CharFilter(field_name='religion', lookup_expr='iexact')
    marital_status = django_filters.CharFilter(field_name='marital_status', lookup_expr='iexact')
    job = django_filters.CharFilter(field_name='job', lookup_expr='iexact')
    citizenship = django_filters.CharFilter(field_name='citizenship', lookup_expr='iexact')

    talenta_id = django_filters.NumberFilter(field_name='talenta_id', lookup_expr='exact')
    
    hire_date = django_filters.DateFilter(field_name='hire_date', lookup_expr='exact')
    resign_date = django_filters.DateFilter(field_name='resign_date', lookup_expr='exact')
    class Meta:
        model = Employee
        fields = []


#Init init doang ini mah
CompanyFilter.init_dynamic(Company)
UnitFilter.init_dynamic(Unit)
LevelFilter.init_dynamic(Level)
EmploymentTypeFilter.init_dynamic(EmploymentType)
ShiftFilter.init_dynamic(Shift)
BranchFilter.init_dynamic(Branch)
EmployeeFilter.init_dynamic(Employee)