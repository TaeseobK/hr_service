from rest_framework.pagination import PageNumberPagination
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status

from hr_dump.models import HRDump

from django.utils import timezone
from django.db import models

from django_filters.rest_framework import FilterSet, DjangoFilterBackend

from .thread_locals import get_current_user_id

import django_filters
import math

from drf_spectacular.utils import extend_schema, OpenApiParameter

TELEGRAM_TOKEN = "8107036456:AAFmc5wbkbqYI5xkGGm3RDVM6J7HhbiQgDw"
CHAT_ID = 8303553610

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
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    deleted_at = django_filters.DateFilter(field_name='deleted_at', lookup_expr='exact')
    deleted_at__gte = django_filters.DateFilter(field_name='deleted_at', lookup_expr='gte')
    deleted_at__lte = django_filters.DateFilter(field_name='deleted_at', lookup_expr='lte')

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


# ==============================
# BASE VIEWSET
# ==============================
class BaseViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "include_deleted",
                bool,
                OpenApiParameter.QUERY,
                description="Jika true, tampilkan semua data termasuk yang sudah soft delete."
            ),
            OpenApiParameter(
                "only_deleted",
                bool,
                OpenApiParameter.QUERY,
                description="Jika true, tampilkan hanya data yang sudah soft delete."
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
        instance = serializer.save()
        user_id = get_current_user_id()

        HRDump.objects.using('hr_dump').create(
            user_id=user_id,
            path=self.request.path,
            method=self.request.method,
            payload=self.get_serializer(instance).data
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        old_data = self.get_serializer(instance).data
        updated_instance = serializer.save()
        new_data = self.get_serializer(updated_instance).data

        user_id = get_current_user_id()
        HRDump.objects.using('hr_dump').create(
            user_id=user_id,
            path=self.request.path,
            method=self.request.method,
            payload={
                "before": old_data,
                "after": new_data
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        snapshot = self.get_serializer(instance).data
        user_id = get_current_user_id()
        
        HRDump.objects.using('hr_dump').create(
            user_id=user_id,
            path=self.request.path,
            method="DELETE",
            payload={
                "deleted": snapshot
            }
        )

        instance.delete(user_id=user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        try:
            obj = self.queryset.model.all_objects.get(pk=pk)
            user_id = get_current_user_id()

            HRDump.objects.using('hr_dump').create(
                user_id=user_id,
                path=self.request.path,
                method="RESTORE",
                payload=self.serializer_class(obj).data
            )

            obj.restore(user_id=user_id)
            return Response(self.serializer_class(obj).data)
        except self.queryset.model.DoesNotExist:
            return Response(
                {"detail": f"{self.queryset.model.__name__} tidak ditemukan"},
                status=404,
            )

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