import django_filters
from .models import *

class CompanyFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='iexact')
    parent_name = django_filters.CharFilter(field_name='parent__name', lookup_expr='icontains')
    children_name = django_filters.CharFilter(field_name='children__name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    parent_isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr='isnull')

    class Meta:
        model = Company
        fields = ['name', 'code', 'is_active', 'parent_isnull', 'parent_name', 'children_name']

class UnitFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='iexact')
    parent_name = django_filters.CharFilter(field_name='parent__name', lookup_expr='icontains')
    children_name = django_filters.CharFilter(field_name='children__name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    parent_isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr='isnull')

    class Meta:
        model = Unit
        fields = ['name', 'code', 'is_active', 'parent_isnull', 'parent_name', 'children_name']

class LevelFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='iexact')
    parent_name = django_filters.CharFilter(field_name='parent__name', lookup_expr='icontains')
    children_name = django_filters.CharFilter(field_name='children__name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    parent_isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr='isnull')

    class Meta:
        model = Level
        fields = ['name', 'code', 'is_active', 'parent_isnull', 'parent_name', 'children_name']

class EmploymentTypeFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = EmploymentType
        fields = ['name', 'code', 'is_active']

class ShiftFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='iexact')
    start_day = django_filters.NumberFilter(field_name='start_day', lookup_expr='week_day')
    start_time = django_filters.TimeRangeFilter(field_name='start_time', lookup_expr='iexact')
    end_day = django_filters.NumberFilter(field_name='end_day', lookup_expr='week_day')
    end_time = django_filters.TimeRangeFilter(field_name='end_time', lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Shift
        fields = ['name', 'code', 'start_day', 'start_time', 'end_day', 'end_time', 'is_active']

class BranchFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='iexact')
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    company_id = django_filters.NumberFilter(field_name='company', lookup_expr='exact')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    province = django_filters.CharFilter(field_name='province', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Branch
        fields = ['name', 'code', 'city', 'province', 'company_name', 'is_active', 'company_id']

class EmployeeFilter(django_filters.FilterSet) :
    id = django_filters.NumberFilter(field_name='id')
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')
    province = django_filters.CharFilter(field_name='province', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='municipality', lookup_expr='icontains')
    religion = django_filters.CharFilter(field_name='religion', lookup_expr='icontains')
    marital_status = django_filters.CharFilter(field_name='marital_status', lookup_expr='icontains')
    birthplace = django_filters.CharFilter(field_name='birthplace', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='icontains')
    nik = django_filters.NumberFilter(field_name='nik', lookup_expr='startswith')

    parent_full_name = django_filters.CharFilter(field_name='parent__full_name', lookup_expr='icontains')
    children_full_name = django_filters.CharFilter(field_name='children__full_name', lookup_expr='icontains')
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    branch_name = django_filters.CharFilter(field_name='branch__name', lookup_expr='icontains')
    unit_name = django_filters.CharFilter(field_name='unit__name', lookup_expr='icontains')
    level_name = django_filters.CharFilter(field_name='level__name', lookup_expr='icontains')
    employment_type_name = django_filters.CharFilter(field_name='employment_type__name', lookup_expr='icontains')
    shift_name = django_filters.CharFilter(field_name='shift__name', lookup_expr='icontains')

    parent_id = django_filters.NumberFilter(field_name='parent', lookup_expr='exact')
    children_id = django_filters.NumberFilter(field_name='children', lookup_expr='exact')
    company_id = django_filters.NumberFilter(field_name='company', lookup_expr='exact')
    branch_id = django_filters.NumberFilter(field_name='branch', lookup_expr='exact')
    unit_id = django_filters.NumberFilter(field_name='unit', lookup_expr='exact')
    level_id = django_filters.NumberFilter(field_name='level', lookup_expr='exact')
    employment_type_id = django_filters.NumberFilter(field_name='employment_type', lookup_expr='exact')
    shift_id = django_filters.NumberFilter(field_name='shift', lookup_expr='exact')
    talenta_id = django_filters.NumberFilter(field_name='talenta_id', lookup_expr='exact')

    user_id = django_filters.NumberFilter(field_name='user_id')
    parent_isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr='isnull')

    class Meta:
        model = Employee
        fields = [
            'full_name', 'province', 'city', 'religion', 'parent_id', 'talenta_id',
            'marital_status', 'birthplace', 'code', 'nik', 'children_id',
            'parent_full_name', 'children_full_name', 'company_name', 'branch_name', 'company_id',
            'unit_name', 'level_name', 'employment_type_name', 'shift_name', 'branch_id',
            'user_id', 'parent_isnull', 'unit_id', 'level_id', 'employment_type_id', 'shift_id' 
        ]