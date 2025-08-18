from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import *
from .serializers import *
from .filters import *
from hr.config import *
from hr.thread_locals import *

SOFTDELETE_PARAMS = [
    OpenApiParameter("include_deleted", bool, OpenApiParameter.QUERY,
                     description="Jika true, tampilkan semua data termasuk yang sudah soft delete."),
    OpenApiParameter("only_deleted", bool, OpenApiParameter.QUERY,
                     description="Jika true, tampilkan hanya data yang sudah soft delete."),
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
        summary="List Companies",
        description="Ambil daftar perusahaan dengan pagination & filter.",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("is_active", bool, OpenApiParameter.QUERY, description="True=aktif, False=soft deleted"),
            OpenApiParameter("code", str, OpenApiParameter.QUERY, description="Kode perusahaan"),
            OpenApiParameter("name", str, OpenApiParameter.QUERY, description="Nama perusahaan (partial match)"),
            OpenApiParameter("parent_id", int, OpenApiParameter.QUERY, description="Filter berdasarkan parent ID"),
            *SOFTDELETE_PARAMS
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
        summary="List Units",
        description="Ambil daftar unit dengan pagination & filter.",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("code", str, OpenApiParameter.QUERY, description="Kode unit"),
            OpenApiParameter("name", str, OpenApiParameter.QUERY, description="Nama unit (partial match)"),
            OpenApiParameter("parent_id", int, OpenApiParameter.QUERY, description="Filter berdasarkan parent ID"),
            *SOFTDELETE_PARAMS
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
        summary="List Levels",
        description="Ambil daftar level dengan pagination & filter.",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("code", str, OpenApiParameter.QUERY, description="Kode level"),
            OpenApiParameter("name", str, OpenApiParameter.QUERY, description="Nama level (partial match)"),
            OpenApiParameter("parent_id", int, OpenApiParameter.QUERY, description="Filter berdasarkan parent ID"),
            *SOFTDELETE_PARAMS
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
        summary="List Employment Types",
        description="Ambil daftar jenis employment (tetap, kontrak, dll).",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("code", str, OpenApiParameter.QUERY, description="Kode employment type"),
            OpenApiParameter("name", str, OpenApiParameter.QUERY, description="Nama employment type"),
            *SOFTDELETE_PARAMS
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
        summary="List Shifts",
        description="Ambil daftar shift dengan pagination & filter berdasarkan hari/jam.",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("code", str, OpenApiParameter.QUERY, description="Kode shift"),
            OpenApiParameter("start_day", int, OpenApiParameter.QUERY, description="Hari mulai (0=Sunday, dst)"),
            OpenApiParameter("end_day", int, OpenApiParameter.QUERY, description="Hari selesai"),
            OpenApiParameter("start_time_gte", str, OpenApiParameter.QUERY, description="Mulai dari jam >= ... (HH:MM:SS)"),
            OpenApiParameter("start_time_lte", str, OpenApiParameter.QUERY, description="Mulai sampai jam <= ... (HH:MM:SS)"),
            OpenApiParameter("end_time_gte", str, OpenApiParameter.QUERY, description="Selesai dari jam >= ..."),
            OpenApiParameter("end_time_lte", str, OpenApiParameter.QUERY, description="Selesai sampai jam <= ..."),
            *SOFTDELETE_PARAMS
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
        summary="List Branches",
        description="Ambil daftar cabang perusahaan dengan filter kota, provinsi, kode pos.",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Halaman"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Jumlah item per halaman"),
            OpenApiParameter("code", str, OpenApiParameter.QUERY, description="Kode cabang"),
            OpenApiParameter("city", str, OpenApiParameter.QUERY, description="Nama kota"),
            OpenApiParameter("province", str, OpenApiParameter.QUERY, description="Provinsi"),
            OpenApiParameter("postal_code", str, OpenApiParameter.QUERY, description="Kode pos"),
            *SOFTDELETE_PARAMS
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
        summary="List Employees",
        description="Ambil daftar karyawan dengan filter identitas, lokasi, atau status kerja.",
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
            *SOFTDELETE_PARAMS
        ],
        responses={200: EmployeeSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)