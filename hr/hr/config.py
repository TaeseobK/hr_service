from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math
from .auth_middleware import *
from django.db import models
from django.utils import timezone

class CustomPagination(PageNumberPagination) :
    page_size = 5
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
            deleted_by=user_id
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
        # current_user di-pass manual dari view atau serializer
        user_id = kwargs.pop("user_id", None)
        if not self.pk:
            self.created_by = user_id
        else:
            self.updated_by = user_id
        super().save(*args, **kwargs)

    def delete(self, hard=False, user_id=None):
        if hard:
            return super().delete()
        else:
            self.deleted_by = user_id
            self.deleted_at = timezone.now()
            self.save()

    def restore(self, user_id=None):
        self.deleted_at = None
        self.deleted_by = None
        self.updated_by = user_id
        self.save()