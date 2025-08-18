from django.db import models

# Create your models here.
class HRDump(models.Model):
    user_id = models.IntegerField()
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=12)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_dump'