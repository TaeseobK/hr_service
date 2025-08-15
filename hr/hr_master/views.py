from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters
from hr.config import CustomPagination
from .serializers import *
from .filters import *
from .models import *

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.using('hr_master').all()
    serializer_class = CompanySerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['name', 'email', 'legal_name']
    ordering_fields = ['updated_at', 'created_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
        fields_param = self.request.query_params.get('fields')
        if fields_param:
            fields_list = [f.strip() for f in fields_param.split(',')]
            kwargs['fields'] = fields_list
            kwargs.setdefault('context', self.get_serializer_context())
            kwargs['context']['fields'] = fields_list
        return super().get_serializer(*args, **kwargs)
    
    @extend_schema(
        description="Choose company data with the optional query params",
        parameters=[
            OpenApiParameter(name='parent_name', description="parent-children column based on the parent_name so it'll get you recursive relations -> where parent__name like %ABC%", required=False, type=str),
            OpenApiParameter(name='children_name', description="parent-children column based on the children_name so it'll get you recursive relations -> where children__name like %ABC%", required=False, type=str),
            OpenApiParameter(name='is_active', description="is_active column it's boolean so u don't need the description, right?", required=False, type=bool),
            OpenApiParameter(name='name', description='name column but case-insensitive -> where name like %ABC%"', required=False, type=str),
            OpenApiParameter(name='code', description='code column case-sensitive same with -> where name = ABC', required=False, type=str),
            OpenApiParameter(name='max_depth', description='The recursion depth, if you encountered the maximum of request, this might the best helper. it will limits the recursions to childrens and the parents.', required=False, type=str),
            OpenApiParameter(name='exclude', description='exclude will not show the column you exclude on this params -> exclude=parent,children -> it will not show the parent and the children column.', required=False, type=str),
            OpenApiParameter(name='fields', description='fields it will only take the column that you wanna see -> fields=name,legal_name,code -> will show you only that column.', required=False, type=str),
            OpenApiParameter(name='parent_isnull', description='this params might helps you to find only if the parents is None. it will give you the first parent of this recursion.', required=False, type=bool),
        ],
        responses=CompanySerializer,
        examples=[
            OpenApiExample(
                'Response Example',
                summary='Example Company',
                value={
                    "count": 1,
                    "total_pages": 1,
                    "current_page": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                        "id": 2,
                        "children": [],
                        "parent": {
                            "id": 1,
                            "parent": None,
                            "name": "Mazta Farma",
                            "code": "MAZ",
                            "legal_name": "PT. Mazta Farma",
                            "npwp": None,
                            "email": None,
                            "phone": None,
                            "website": None,
                            "logo": None,
                            "is_active": True,
                            "created_at": "2025-08-12T08:03:39.384155Z",
                            "updated_at": "2025-08-12T08:03:39.384155Z",
                            "deleted_at": None,
                            "created_by": 1,
                            "deleted_by": None
                        },
                        "name": "Mazta Distribusi Indonesia",
                        "code": "MDI",
                        "legal_name": "PT. Mazta Distribusi Indonesia",
                        "npwp": None,
                        "email": None,
                        "phone": None,
                        "website": None,
                        "logo": None,
                        "is_active": True,
                        "created_at": "2025-08-12T08:04:08.124873Z",
                        "updated_at": "2025-08-12T08:04:08.124873Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class UnitViewSet(viewsets.ModelViewSet) :
    queryset = Unit.objects.using('hr_master').all()
    serializer_class = UnitSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = UnitFilter
    search_fields = ['name']
    ordering_fields = ['updated_at', 'created_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
        fields_param = self.request.query_params.get('fields')
        if fields_param:
            fields_list = [f.strip() for f in fields_param.split(',')]
            kwargs['fields'] = fields_list
            kwargs.setdefault('context', self.get_serializer_context())
            kwargs['context']['fields'] = fields_list
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description="Choosing the units data with optional query params.",
        parameters=[
            OpenApiParameter(name='parent_name', description="parent-children column based on the parent_name so it'll get you recursive relations -> where parent__name like %ABC%", required=False, type=str),
            OpenApiParameter(name='children_name', description="parent-children column based on the children_name so it'll get you recursive relations -> where children__name like %ABC%", required=False, type=str),
            OpenApiParameter(name='is_active', description="is_active column it's boolean so u don't need the description, right?", required=False, type=bool),
            OpenApiParameter(name='name', description='name column but case-insensitive -> where name like %ABC%"', required=False, type=str),
            OpenApiParameter(name='code', description='code column case-sensitive same with -> where name = ABC', required=False, type=str),
            OpenApiParameter(name='max_depth', description='The recursion depth, if you encountered the maximum of request, this might the best helper. it will limits the recursions to childrens and the parents.', required=False, type=str),
            OpenApiParameter(name='exclude', description='exclude will not show the column you exclude on this params -> exclude=parent,children -> it will not show the parent and the children column.', required=False, type=str),
            OpenApiParameter(name='fields', description='fields it will only take the column that you wanna see -> fields=name,legal_name,code -> will show you only that column.', required=False, type=str),
            OpenApiParameter(name='parent_isnull', description='this params might helps you to find only if the parents is None. it will give you the first parent of this recursion.', required=False, type=bool),
        ],
        responses=UnitSerializer,
        examples=[
            OpenApiExample(
                'Response Example',
                summary='Example Untis',
                value={
                    "count": 22,
                    "total_pages": 22,
                    "current_page": 1,
                    "next": "http://localhost:8000/api/hr/master/unit/?max_depth=1&page=2&page_size=1",
                    "previous": None,
                    "results": [
                        {
                        "id": 22,
                        "children": [],
                        "parent": {
                            "id": 7,
                            "parent": {
                            "id": 3,
                            "name": "Information Technology"
                            },
                            "name": "IT Security",
                            "code": "ITS",
                            "is_active": True,
                            "created_at": "2025-08-12T08:18:12.144859Z",
                            "updated_at": "2025-08-12T08:18:12.144859Z",
                            "deleted_at": None,
                            "created_by": 1,
                            "deleted_by": None
                        },
                        "name": "Identity & Access Management",
                        "code": "Iam",
                        "is_active": True,
                        "created_at": "2025-08-12T08:23:42.006484Z",
                        "updated_at": "2025-08-12T08:23:42.006484Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class LevelViewSet(viewsets.ModelViewSet) :
    queryset = Level.objects.using('hr_master').all()
    serializer_class = LevelSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = LevelFilter
    search_fields = ['name']
    ordering_fields = ['updated_at', 'created_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
        fields_param = self.request.query_params.get('fields')
        if fields_param:
            fields_list = [f.strip() for f in fields_param.split(',')]
            kwargs['fields'] = fields_list
            kwargs.setdefault('context', self.get_serializer_context())
            kwargs['context']['fields'] = fields_list
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description="Choosing the units data with optional query params.",
        parameters=[
            OpenApiParameter(name='parent_name', description="parent-children column based on the parent_name so it'll get you recursive relations -> where parent__name like %ABC%", required=False, type=str),
            OpenApiParameter(name='children_name', description="parent-children column based on the children_name so it'll get you recursive relations -> where children__name like %ABC%", required=False, type=str),
            OpenApiParameter(name='is_active', description="is_active column it's boolean so u don't need the description, right?", required=False, type=bool),
            OpenApiParameter(name='name', description='name column but case-insensitive -> where name like %ABC%"', required=False, type=str),
            OpenApiParameter(name='code', description='code column case-sensitive same with -> where name = ABC', required=False, type=str),
            OpenApiParameter(name='max_depth', description='The recursion depth, if you encountered the maximum of request, this might the best helper. it will limits the recursions to childrens and the parents.', required=False, type=str),
            OpenApiParameter(name='exclude', description='exclude will not show the column you exclude on this params -> exclude=parent,children -> it will not show the parent and the children column.', required=False, type=str),
            OpenApiParameter(name='fields', description='fields it will only take the column that you wanna see -> fields=name,legal_name,code -> will show you only that column.', required=False, type=str),
            OpenApiParameter(name='parent_isnull', description='this params might helps you to find only if the parents is None. it will give you the first parent of this recursion.', required=False, type=bool),
        ],
        responses=LevelSerializer,
        examples=[
            OpenApiExample(
                'Response Level',
                summary='Example Levels',
                value={
                    "count": 6,
                    "total_pages": 6,
                    "current_page": 2,
                    "next": "http://localhost:8000/api/hr/master/level/?max_depth=1&page=3&page_size=1",
                    "previous": "http://localhost:8000/api/hr/master/level/?max_depth=1&page_size=1",
                    "results": [
                        {
                        "id": 5,
                        "children": [
                            {
                            "id": 6,
                            "children": [],
                            "name": "Internship",
                            "code": "Int",
                            "is_active": True,
                            "created_at": "2025-08-12T08:28:46.987343Z",
                            "updated_at": "2025-08-12T08:28:46.987343Z",
                            "deleted_at": None,
                            "created_by": 1,
                            "deleted_by": None
                            }
                        ],
                        "parent": {
                            "id": 4,
                            "parent": {
                            "id": 3,
                            "name": "Head / Manager"
                            },
                            "name": "Supervison",
                            "code": "Spv",
                            "is_active": True,
                            "created_at": "2025-08-12T08:28:23.119045Z",
                            "updated_at": "2025-08-12T08:28:23.119045Z",
                            "deleted_at": None,
                            "created_by": 1,
                            "deleted_by": None
                        },
                        "name": "Staff",
                        "code": "St",
                        "is_active": True,
                        "created_at": "2025-08-12T08:28:35.349510Z",
                        "updated_at": "2025-08-12T08:28:35.349510Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class EmploymentTypeViewSet(viewsets.ModelViewSet) :
    queryset = EmploymentType.objects.using('hr_master').all()
    serializer_class = EmploymentTypeSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = EmploymentTypeFilter
    search_fields = ['name']
    ordering_fields = ['updated_at', 'created_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
            fields_param = self.request.query_params.get('fields')
            if fields_param:
                fields_list = [f.strip() for f in fields_param.split(',')]
                kwargs['fields'] = fields_list
                kwargs.setdefault('context', self.get_serializer_context())
                kwargs['context']['fields'] = fields_list
            return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description="Choosing the employment type data with optional query params.",
        parameters=[
            OpenApiParameter(name='is_active', description="is_active column it's boolean so u don't need the description, right?", required=False, type=bool),
            OpenApiParameter(name='name', description='name column but case-insensitive -> where name like %ABC%"', required=False, type=str),
            OpenApiParameter(name='code', description='code column case-sensitive same with -> where name = ABC', required=False, type=str),
            OpenApiParameter(name='exclude', description='exclude will not show the column you exclude on this params -> exclude=parent,children -> it will not show the parent and the children column.', required=False, type=str),
            OpenApiParameter(name='fields', description='fields it will only take the column that you wanna see -> fields=name,legal_name,code -> will show you only that column.', required=False, type=str),
        ],
        responses=EmploymentTypeSerializer,
        examples=[
            OpenApiExample(
                'Response Employment Type',
                summary='Example Employment_Types',
                value={
                    "count": 5,
                    "total_pages": 5,
                    "current_page": 1,
                    "next": "http://localhost:8000/api/hr/master/employment-type/?page=2&page_size=1",
                    "previous": None,
                    "results": [
                        {
                        "id": 5,
                        "name": "Probation",
                        "code": "Prb",
                        "is_active": True,
                        "created_at": "2025-08-12T08:31:25.973316Z",
                        "updated_at": "2025-08-12T08:31:25.973316Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ShiftViewSet(viewsets.ModelViewSet) :
    queryset = Shift.objects.using('hr_master').all()
    serializer_class = ShiftSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = ShiftFilter
    search_fields = ['name', 'start_day', 'start_time', 'end_day', 'end_time']
    ordering_fields = ['updated_at', 'created_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
            fields_param = self.request.query_params.get('fields')
            if fields_param:
                fields_list = [f.strip() for f in fields_param.split(',')]
                kwargs['fields'] = fields_list
                kwargs.setdefault('context', self.get_serializer_context())
                kwargs['context']['fields'] = fields_list
            return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description="Choosing the shift data with optional query params.",
        parameters=[
            OpenApiParameter(name='is_active', description="is_active column it's boolean so u don't need the description, right?", required=False, type=bool),
            OpenApiParameter(name='name', description='name column but case-insensitive -> where name like %ABC%"', required=False, type=str),
            OpenApiParameter(name='code', description='code column case-sensitive same with -> where name = ABC', required=False, type=str),
            OpenApiParameter(name='start_day', description='start_day column with case-insensitive -> where start_day = ', required=False, type=str),
            OpenApiParameter(name='end_day', description='end_day column with case-insensitive -> where end_day = ', required=False, type=str),
            OpenApiParameter(name='exclude', description='exclude will not show the column you exclude on this params -> exclude=parent,children -> it will not show the parent and the children column.', required=False, type=str),
            OpenApiParameter(name='fields', description='fields it will only take the column that you wanna see -> fields=name,legal_name,code -> will show you only that column.', required=False, type=str),
        ],
        responses=ShiftSerializer,
        examples=[
            OpenApiExample(
                'Response Shift',
                summary='Example Shifts',
                value={
                    "count": 1,
                    "total_pages": 1,
                    "current_page": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                        "id": 1,
                        "name": "Normal",
                        "code": "N",
                        "start_day": 1,
                        "start_time": "08:30:00",
                        "end_day": 5,
                        "end_time": "17:30:00",
                        "is_active": True,
                        "created_at": "2025-08-12T08:30:24.584131Z",
                        "updated_at": "2025-08-12T08:30:24.584131Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class BranchViewSet(viewsets.ModelViewSet) :
    queryset = Branch.objects.using('hr_master').all()
    serializer_class = BranchSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = BranchFilter
    search_fields = ['name', 'city', 'province']
    ordering_fields = ['updated_at', 'created_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
            fields_param = self.request.query_params.get('fields')
            if fields_param:
                fields_list = [f.strip() for f in fields_param.split(',')]
                kwargs['fields'] = fields_list
                kwargs.setdefault('context', self.get_serializer_context())
                kwargs['context']['fields'] = fields_list
            return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description="Choosing the branch data with optional query params.",
        parameters=[
            OpenApiParameter(name='is_active', description="is_active column it's boolean so u don't need the description, right?", required=False, type=bool),
            OpenApiParameter(name='name', description='name column but case-insensitive -> where name like %ABC%"', required=False, type=str),
            OpenApiParameter(name='code', description='code column case-sensitive same with -> where name = ABC', required=False, type=str),
            OpenApiParameter(name='company_name', description='company column case-insensitive same with -> where company.name like %ABC%', required=False, type=str),
            OpenApiParameter(name='city', description='city column case-insensitive same with -> where city like %ABC%', required=False, type=str),
            OpenApiParameter(name='province', description='province column case-insensitive same with -> where province like %ABC%', required=False, type=str),
            OpenApiParameter(name='company_id', description='company column exact value same with -> where company_id = int(value)', required=False, type=int),
            OpenApiParameter(name='exclude', description='exclude will not show the column you exclude on this params -> exclude=parent,children -> it will not show the parent and the children column.', required=False, type=str),
            OpenApiParameter(name='fields', description='fields it will only take the column that you wanna see -> fields=name,legal_name,code -> will show you only that column.', required=False, type=str),
        ],
        responses=BranchSerializer,
        examples=[
            OpenApiExample(
                'Response Branch',
                summary='Example Branches',
                value={
                    "count": 1,
                    "total_pages": 1,
                    "current_page": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                        "id": 1,
                        "name": "Head Office",
                        "code": "Ho",
                        "address": "",
                        "city": None,
                        "province": None,
                        "postal_code": None,
                        "is_active": True,
                        "created_at": "2025-08-12T08:33:02.699004Z",
                        "updated_at": "2025-08-12T08:33:02.699004Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None,
                        "company": [
                            1
                        ]
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.using('hr_master').all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = [
            'full_name', 'code', 'religion', 'province', 
            'city', 'postal_code', 'citizenship', 'first_name', 
            'middle_name', 'last_name', 'birthplace', 'unit__name',
            'level__name'
        ]
    ordering_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
        fields_param = self.request.query_params.get('fields')
        if fields_param:
            fields_list = [f.strip() for f in fields_param.split(',')]
            kwargs['fields'] = fields_list
            kwargs.setdefault('context', self.get_serializer_context())
            kwargs['context']['fields'] = fields_list
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description="Choosing the employee data with optional query params.",
        parameters=[
            OpenApiParameter(name='full_name', type=str, description='Filter employees by full name (case-insensitive match)'),
            OpenApiParameter(name='province', type=str, description='Filter employees by province (case-insensitive match)'),
            OpenApiParameter(name='city', type=str, description='Filter employees by municipality/city (case-insensitive match)'),
            OpenApiParameter(name='religion', type=str, description='Filter employees by religion (case-insensitive match)'),
            OpenApiParameter(name='marital_status', type=str, description='Filter employees by marital status (case-insensitive match)'),
            OpenApiParameter(name='birthplace', type=str, description='Filter employees by birthplace (case-insensitive match)'),
            OpenApiParameter(name='code', type=str, description='Filter employees by employee code (case-insensitive match)'),
            OpenApiParameter(name='nik', type=int, description='Filter employees whose NIK starts with this number'),
            
            OpenApiParameter(name='parent_full_name', type=str, description='Filter employees by their parent’s full name (case-insensitive match)'),
            OpenApiParameter(name='children_full_name', type=str, description='Filter employees by their children’s full name (case-insensitive match)'),
            OpenApiParameter(name='company_name', type=str, description='Filter employees by company name (case-insensitive match)'),
            OpenApiParameter(name='branch_name', type=str, description='Filter employees by branch name (case-insensitive match)'),
            OpenApiParameter(name='unit_name', type=str, description='Filter employees by unit name (case-insensitive match)'),
            OpenApiParameter(name='level_name', type=str, description='Filter employees by level name (case-insensitive match)'),
            OpenApiParameter(name='employment_type_name', type=str, description='Filter employees by employment type name (case-insensitive match)'),
            OpenApiParameter(name='shift_name', type=str, description='Filter employees by shift name (case-insensitive match)'),

            OpenApiParameter(name='parent_id', type=int, description='Filter employees by exact parent ID'),
            OpenApiParameter(name='children_id', type=int, description='Filter employees by exact children ID'),
            OpenApiParameter(name='company_id', type=int, description='Filter employees by exact company ID'),
            OpenApiParameter(name='branch_id', type=int, description='Filter employees by exact branch ID'),
            OpenApiParameter(name='unit_id', type=int, description='Filter employees by exact unit ID'),
            OpenApiParameter(name='level_id', type=int, description='Filter employees by exact level ID'),
            OpenApiParameter(name='employment_type_id', type=int, description='Filter employees by exact employment type ID'),
            OpenApiParameter(name='shift_id', type=int, description='Filter employees by exact shift ID'),
            OpenApiParameter(name='talenta_id', type=int, description='Filter employees by exact talenta ID'),

            OpenApiParameter(name='user_id', type=int, description='Filter employees by exact user ID'),
            OpenApiParameter(name='parent_isnull', type=bool, description='Filter employees whose parent is null (true/false)'),
        ],
        responses=EmployeeSerializer,
        examples=[
            OpenApiExample(
                'Response Employees',
                summary='Example Employees',
                value={
                    "count": 1,
                    "total_pages": 1,
                    "current_page": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                        "id": 1,
                        "name": "Head Office",
                        "code": "Ho",
                        "address": "",
                        "city": None,
                        "province": None,
                        "postal_code": None,
                        "is_active": True,
                        "created_at": "2025-08-12T08:33:02.699004Z",
                        "updated_at": "2025-08-12T08:33:02.699004Z",
                        "deleted_at": None,
                        "created_by": 1,
                        "deleted_by": None,
                        "company": [
                            1
                        ],
                        "talenta_id": 3
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)