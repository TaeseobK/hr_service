from rest_framework.pagination import PageNumberPagination
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status, serializers
from rest_framework.filters import SearchFilter

from hr_dump.models import *

from django.utils import timezone
from django.db import models
from django.db.models import Q

from django_filters.rest_framework import FilterSet, DjangoFilterBackend

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiRequest,
    OpenApiResponse,
    OpenApiExample,
    inline_serializer,
)
from drf_spectacular.types import OpenApiTypes

from .thread_locals import get_current_user_id

import django_filters
import pandas as pd
import math

from drf_spectacular.utils import extend_schema, OpenApiParameter

dump_data = 'hr_dump'
model_dump = HRDump

class CustomPagination(PageNumberPagination) :
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request) or 2
        total_pages = math.ceil(self.page.paginator.count / page_size)

        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
    
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, user_id=None):
        """Soft delete semua record dalam queryset"""
        return super().update(
            deleted_at=timezone.now(),
            deleted_by=user_id or get_current_user_id()
        )

    def hard_delete(self):
        """Hard delete langsung dari DB"""
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def dead(self):
        return SoftDeleteQuerySet(self.model, using=self._db).dead()


class AllObjectsManager(models.Manager):
    """Manager untuk akses semua record termasuk yang sudah dihapus"""
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class BaseModel(models.Model):
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        - Saat pertama kali save → isi created_by
        - Saat update → isi updated_by
        - Kalau created_by masih kosong saat update pertama kali, isi juga
        """
        user_id = kwargs.pop("user_id", None) or get_current_user_id()
        if not self.pk:  # object baru
            if self.created_by is None:
                self.created_by = user_id
                self.updated_by = user_id
        else:  # update object lama
            self.updated_by = user_id

        super().save(*args, **kwargs)

    def delete(self, hard=False, user_id=None):
        """
        Soft delete secara default.
        Kalau hard=True, benar-benar hapus dari DB.
        """
        user_id = user_id or get_current_user_id()
        if hard:
            return super().delete()
        else:
            self.deleted_by = user_id
            self.deleted_at = timezone.now()
            self.save()

    def restore(self, user_id=None):
        """
        Mengembalikan record yang sudah soft delete.
        """
        user_id = user_id or get_current_user_id()
        self.deleted_at = None
        self.deleted_by = None
        self.updated_by = user_id
        self.save()

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class BaseFilter(FilterSet):
    is_active = django_filters.BooleanFilter(field_name='deleted_at', lookup_expr='isnull')
    deleted_by = django_filters.NumberFilter(field_name='deleted_by', lookup_expr='exact')
    created_by = django_filters.NumberFilter(field_name='created_by', lookup_expr='exact')

    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='exact')
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    deleted_at = django_filters.DateFilter(field_name='deleted_at', lookup_expr='exact')
    deleted_at__gte = django_filters.DateTimeFilter(field_name='deleted_at', lookup_expr='gte')
    deleted_at__lte = django_filters.DateTimeFilter(field_name='deleted_at', lookup_expr='lte')

    INCLUDE_SELF_CODE = True

    @classmethod
    def init_dynamic(cls, model_class):
        cls.base_filters = cls.base_filters.copy() if hasattr(cls, 'base_filters') else {}

        # INCLUDE_SELF_CODE
        if cls.INCLUDE_SELF_CODE:
            if hasattr(model_class, '_meta') and 'code' in [f.name for f in model_class._meta.get_fields()]:
                cls.base_filters['code'] = django_filters.CharFilter(field_name='code', lookup_expr='exact')

        # Parent
        try:
            parent_field = model_class._meta.get_field('parent')
            if isinstance(parent_field, models.ForeignKey):
                cls.base_filters['parent_id'] = django_filters.NumberFilter(field_name='parent_id', lookup_expr='exact')
                related_model = parent_field.remote_field.model

                if 'code' in [f.name for f in related_model._meta.get_fields()]:
                    cls.base_filters['parent__code'] = django_filters.CharFilter(field_name='parent__code', lookup_expr='exact')
                if 'name' in [f.name for f in related_model._meta.get_fields()]:
                    cls.base_filters['parent__name'] = django_filters.CharFilter(field_name='parent__name', lookup_expr='icontains')
        except Exception:
            pass

        # ForeignKey
        for field in model_class._meta.get_fields():
            if isinstance(field, models.ForeignKey) and field.name != 'parent':
                f_name = field.name
                cls.base_filters[f"{f_name}_id"] = django_filters.NumberFilter(field_name=f"{f_name}_id", lookup_expr='exact')
                related_model = field.related_model
                if 'code' in [f.name for f in related_model._meta.get_fields()]:
                    cls.base_filters[f"{f_name}__code"] = django_filters.CharFilter(field_name=f"{f_name}__code", lookup_expr='exact')
                if 'name' in [f.name for f in related_model._meta.get_fields()]:
                    cls.base_filters[f"{f_name}__name"] = django_filters.CharFilter(field_name=f"{f_name}__name", lookup_expr='icontains')

        # ManyToMany
        for field in model_class._meta.get_fields():
            if isinstance(field, models.ManyToManyField):
                f_name = field.name
                cls.base_filters[f"{f_name}_id__in"] = NumberInFilter(field_name=f"{f_name}__id", lookup_expr='in')
                related_model = field.related_model
                if 'code' in [f.name for f in related_model._meta.get_fields()]:
                    cls.base_filters[f"{f_name}_code__in"] = CharInFilter(field_name=f"{f_name}__code", lookup_expr='in')
                if 'name' in [f.name for f in related_model._meta.get_fields()]:
                    cls.base_filters[f"{f_name}_name__in"] = django_filters.CharFilter(field_name=f"{f_name}__name", lookup_expr='icontains')

        # Tambahkan semua field model otomatis (kecuali yang sudah ada di base_filters)
        for field in model_class._meta.get_fields():
            if field.name not in cls.base_filters and isinstance(field, (models.CharField, models.IntegerField, models.DecimalField, models.DateField, models.DateTimeField)):
                if isinstance(field, models.CharField):
                    cls.base_filters[field.name] = django_filters.CharFilter(field_name=field.name, lookup_expr='icontains')
                elif isinstance(field, (models.IntegerField, models.DecimalField)):
                    cls.base_filters[field.name] = django_filters.NumberFilter(field_name=field.name, lookup_expr='exact')
                elif isinstance(field, (models.DateField, models.DateTimeField)):
                    cls.base_filters[field.name] = django_filters.DateFilter(field_name=field.name, lookup_expr='exact')

def generate_filter_parameters_from_basefilter(model_class, base_filter_class=BaseFilter):
    """
    Generate OpenApiParameter list dari BaseFilter.init_dynamic().
    """
    # inisialisasi filter
    base_filter_class.init_dynamic(model_class)
    params = []

    LOOKUP_LABELS = {
        "exact": "exact match (=)",
        "iexact": "case-insensitive exact match",
        "contains": "contains",
        "icontains": "case-insensitive contains",
        "gte": "greater than or equal",
        "lte": "less than or equal",
        "in": "in list",
    }

    for name, flt in base_filter_class.base_filters.items():
        # mapping sederhana django-filter ke tipe OpenAPI
        if isinstance(flt, django_filters.BooleanFilter):
            schema_type = bool
        elif isinstance(flt, (django_filters.NumberFilter, NumberInFilter)):
            schema_type = int
        elif isinstance(flt, django_filters.DateFilter):
            schema_type = OpenApiTypes.DATE
        elif isinstance(flt, django_filters.CharFilter) or isinstance(flt, CharInFilter):
            schema_type = str
        elif isinstance(flt, django_filters.DateTimeFilter):
            schema_type = OpenApiTypes.DATETIME
        else:
            schema_type = OpenApiTypes.STR

        # kalau filter lookup-nya pakai "__in", kasih hint array
        if "__in" in name:
            schema_type = OpenApiTypes.INT

        lookup_expr = getattr(flt, "lookup_expr", "iexact")

        lookup_label = LOOKUP_LABELS.get(lookup_expr, lookup_expr)

        params.append(
            OpenApiParameter(
                name,
                schema_type,
                OpenApiParameter.QUERY,
                description=f"Filter by '{name}' (lookup: {lookup_label})"
            )
        )

    return params

class NameCodeSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_value = request.query_params.get(self.search_param, '')

        if not search_value:
            return queryset

        q = Q()
        # kalau field name ada di model, pakai icontains
        if hasattr(queryset.model, "name"):
            q |= Q(name__icontains=search_value)

        # kalau field code ada di model, pakai iexact
        if hasattr(queryset.model, "code"):
            q |= Q(code__iexact=search_value)

        return queryset.filter(q)

# ==============================
# BASE VIEWSET
# ==============================
class BaseViewSet(viewsets.ModelViewSet):
    """
    Standard BaseViewSet:
    - Pagination (CustomPagination)
    - Filter backend (DjangoFilterBackend, SearchFilter)
    - Search: `name` (icontains), `code` (iexact)
    - Softdelete support (include_deleted, only_deleted, restore)
    - Audit trail (model_dump)
    """
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, NameCodeSearchFilter]

    def get_queryset(self):
        qs = self.queryset
        include_deleted = self.request.query_params.get("include_deleted")
        only_deleted = self.request.query_params.get("only_deleted")

        if include_deleted in ["1", "true", "True"]:
            return self.queryset.model.all_objects.all()
        elif only_deleted in ["1", "true", "True"]:
            return self.queryset.model.objects.dead()
        return qs

    def perform_create(self, serializer):
        user_id = get_current_user_id()
        dump_obj = None
        instance = None

        try:
            # simpan ke main DB dulu
            instance = serializer.save()
            full_payload = self.get_serializer(instance).data

            # baru simpan dump pake full data
            dump_obj = model_dump.objects.using(dump_data).create(
                user_id=user_id,
                path=self.request.path,
                method=self.request.method,
                payload=full_payload,
            )
            dump_obj.save()

            return Response({
                'detail': 'Successfully created data.',
                'data': full_payload
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            if instance:  # rollback main jika gagal dump
                instance.delete()
            if dump_obj:
                dump_obj.delete()
            return Response(
                {"detail": f"Failed on create: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        user_id = get_current_user_id()
        instance = self.get_object()
        old_data = self.get_serializer(instance).data
        dump_obj = None
        updated_instance = None

        try:
            updated_instance = serializer.save()
            full_payload = self.get_serializer(updated_instance).data

            dump_obj = model_dump.objects.using(dump_data).create(
                user_id=user_id,
                path=self.request.path,
                method=self.request.method,
                payload={
                    "before": old_data,
                    "after": full_payload
                },
            )
            dump_obj.save()

            return Response({
                'detail': f'Successfully updated data',
                'data': {
                    'before': old_data,
                    'after': full_payload
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            if updated_instance:
                updated_instance.delete()
            if dump_obj:
                dump_obj.delete()
            return Response(
                {'detail': f'Failed update: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        user_id = get_current_user_id()
        instance = self.get_object()
        dump_obj = None

        try:
            full_data = self.get_serializer(instance).data

            dump_obj = model_dump.objects.using(dump_data).create(
                user_id=user_id,
                path=self.request.path,
                method="DELETE",
                payload={"deleted": full_data},
            )
            dump_obj.save()

            instance.delete(user_id=user_id)
            return Response({
                'detail': 'Successfully deleted data.',
                'data': full_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            if dump_obj:
                dump_obj.delete()
            return Response(
                {'detail': f'Failed delete: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        user_id = get_current_user_id()
        dump_obj = None

        try:
            obj = self.queryset.model.all_objects.get(pk=pk)
        except self.queryset.model.DoesNotExist:
            return Response(
                {"detail": f"{self.queryset.model.__name__} not found."},
                status=404,
            )

        try:
            full_data = self.serializer_class(obj).data

            dump_obj = model_dump.objects.using(dump_data).create(
                user_id=user_id,
                path=self.request.path,
                method="RESTORE",
                payload=full_data,
            )
            dump_obj.save()

            obj.restore(user_id=user_id)
            return Response({
                'detail': 'Successfully restoring data.',
                'data': self.serializer_class(obj).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            if dump_obj:
                dump_obj.delete()
            return Response(
                {'detail': f'Failed restore: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    @extend_schema(
    request=inline_serializer(
        name="BulkUploadRequest",
        fields={
            "file": serializers.FileField(),
        },
    ), responses={
            201: OpenApiResponse(OpenApiTypes.OBJECT),
            400: OpenApiResponse(OpenApiTypes.OBJECT),
        },
    )
    @action(detail=False, methods=["post"], url_path="insert-bulk")
    def insert_bulk(self, request):
        """
        Upload Excel (xlsx/csv) untuk bulk insert.
        - Auto isi created_by & updated_by dari request.user.id
        - Rollback kalau ada yang gagal
        """
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"detail": "File not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # load pakai pandas
            if file_obj.name.endswith(".csv"):
                df = pd.read_csv(file_obj)
            else:
                df = pd.read_excel(file_obj)

            data = df.to_dict(orient="records")
            user_id = get_current_user_id()

            # isi otomatis kolom audit
            for row in data:
                row["created_by"] = user_id
                row["updated_by"] = user_id

            serializer = self.get_serializer(data=data, many=True)

            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                serializer.save(user_id=user_id)  # dikirim ke BaseModel.save()

            return Response(
                {"detail": f"Successfully inserted {len(data)} rows"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"detail": f"Bulk insert failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        # Kalau dict field errors, gabung semua ke string
        if isinstance(data, dict) and "detail" not in data:
            messages = []
            for field, errors in data.items():
                # errors bisa list atau string
                if isinstance(errors, (list, tuple)):
                    for err in errors:
                        messages.append(f"{field}: {err}")
                else:
                    messages.append(f"{field}: {errors}")
            response.data = {"detail": " | ".join(messages)}

        else:
            # untuk global error (sudah ada detail)
            response.data = {"detail": data.get("detail", data)}

    return response