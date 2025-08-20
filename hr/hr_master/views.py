from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import *
from .serializers import *
from .filters import *
from hr.config import *
from hr.thread_locals import *

import inspect

BASE_PARAMS = [
    OpenApiParameter("include_deleted", OpenApiTypes.BOOL, OpenApiParameter.QUERY,
                     description="If true, get all data with deleted data."),
    OpenApiParameter("only_deleted", OpenApiTypes.BOOL, OpenApiParameter.QUERY,
                     description="If true, get all data only deleted data."),
    OpenApiParameter("page", OpenApiTypes.INT, OpenApiParameter.QUERY,
                     description="Return which page you want to return."),
    OpenApiParameter("page_size", OpenApiTypes.INT, OpenApiParameter.QUERY,
                     description="Return the count of data each page."),
    OpenApiParameter("page_size", OpenApiTypes.STR, OpenApiParameter.QUERY,
                     description="Return the count of data each page."),
    OpenApiParameter("search", OpenApiTypes.STR, OpenApiParameter.QUERY,
                     description="Search based on name (WHERE LIKE %<value>%) and Code (WHERE = <value>)"),
]

# ==============================
# COMPANY
# ==============================
@extend_schema(tags=["Company"])
class CompanyViewSet(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar company dengan pagination & filter.",
        parameters=[
            *generate_filter_parameters_from_basefilter(Company, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: CompanySerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# ==============================
# UNIT
# ==============================
@extend_schema(tags=["Unit"])
class UnitViewSet(BaseViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filterset_class = UnitFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar unit dengan pagination & filter.",
        parameters=[
            *generate_filter_parameters_from_basefilter(Unit, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: UnitSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ==============================
# LEVEL
# ==============================
@extend_schema(tags=["Level"])
class LevelViewSet(BaseViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    filterset_class = LevelFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar level dengan pagination & filter.",
        parameters=[
            *generate_filter_parameters_from_basefilter(Level, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: LevelSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ==============================
# EMPLOYMENT TYPE
# ==============================
@extend_schema(tags=["EmploymentType"])
class EmploymentTypeViewSet(BaseViewSet):
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer
    filterset_class = EmploymentTypeFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar employment_type dengan pagination & filter.",
        parameters=[
            *generate_filter_parameters_from_basefilter(EmploymentType, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: EmploymentTypeSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ==============================
# SHIFT
# ==============================
@extend_schema(tags=["Shift"])
class ShiftViewSet(BaseViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    filterset_class = ShiftFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar shift dengan pagination & filter.",
        parameters=[
            *generate_filter_parameters_from_basefilter(Shift, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: ShiftSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ==============================
# BRANCH
# ==============================
@extend_schema(tags=["Branch"])
class BranchViewSet(BaseViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filterset_class = BranchFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar branch dengan pagination & filter.",
        parameters=[
            *generate_filter_parameters_from_basefilter(Branch, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: BranchSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ==============================
# EMPLOYEE
# ==============================
@extend_schema(tags=["Employee"])
class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter

    @extend_schema(
        description=f"{inspect.getdoc(BaseViewSet)}\n\nAmbil daftar karyawan dengan filter identitas, lokasi, atau status kerja.",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("user_id", int, OpenApiParameter.QUERY, description="User ID karyawan"),
            OpenApiParameter("nik", int, OpenApiParameter.QUERY, description="Nomor Induk Karyawan"),
            OpenApiParameter("city", str, OpenApiParameter.QUERY, description="Kota domisili"),
            OpenApiParameter("province", str, OpenApiParameter.QUERY, description="Provinsi domisili"),
            OpenApiParameter("religion", str, OpenApiParameter.QUERY, description="Agama"),
            OpenApiParameter("marital_status", str, OpenApiParameter.QUERY, description="Status pernikahan"),
            OpenApiParameter("job", str, OpenApiParameter.QUERY, description="Pekerjaan/jabatan"),
            OpenApiParameter("citizenship", str, OpenApiParameter.QUERY, description="Kewarganegaraan"),
            OpenApiParameter("talenta_id", int, OpenApiParameter.QUERY, description="ID Talenta HR"),
            OpenApiParameter("hire_date", str, OpenApiParameter.QUERY, description="Tanggal masuk kerja (YYYY-MM-DD)"),
            OpenApiParameter("resign_date", str, OpenApiParameter.QUERY, description="Tanggal resign (YYYY-MM-DD)"),
            *generate_filter_parameters_from_basefilter(Employee, BaseFilter),
            *BASE_PARAMS
        ],
        responses={200: EmployeeSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)