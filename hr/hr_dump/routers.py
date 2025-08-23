from django.conf import settings
from django.db import connections
from django.apps import apps

class HrDumpRouter :

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'hr_dump':
            return 'hr_dump'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'hr_dump':
            return 'hr_dump'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'hr_dump' and obj2._meta.app_label == 'auth'
        ) or obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'hr_dump':
            return db == 'hr_dump'
        return None