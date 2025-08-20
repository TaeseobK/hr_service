from django.db import models
from hr.config import BaseModel

class Company(BaseModel) :
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=24, unique=True)
    legal_name = models.CharField(max_length=86, null=True, blank=True)
    npwp = models.CharField(max_length=86, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    website = models.URLField(null=True, blank=True)

    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        db_table = 'companies'
        managed = True
        verbose_name_plural = 'Companies'
        indexes = [
            models.Index(fields=['parent'])
        ]
    
    def __str__(self):
        return self.name

class Unit(BaseModel) :
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=24, unique=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        db_table = 'units'
        managed = True
        verbose_name_plural = 'Units'
        indexes = [
            models.Index(fields=['parent'])
        ]
    
    def __str__(self):
        return self.name
    
class Level(BaseModel) :
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=24, unique=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        db_table = 'levels'
        managed = True
        verbose_name_plural = 'Levels'
        indexes = [
            models.Index(fields=['parent'])
        ]
    
    def __str__(self):
        return self.name

class EmploymentType(BaseModel) :
    name = models.CharField(max_length=24)
    code = models.CharField(max_length=24, unique=True)

    class Meta:
        db_table = 'employment_types'
        managed = True
        verbose_name_plural = 'EmploymentTypes'
    
    def __str__(self):
        return self.name
    

DAYS_OF_WEEK = [
    (0, 'SUNDAY'),
    (1, 'MONDAY'),
    (2, 'TUESDAY'),
    (3, 'WEDNESDAY'),
    (4, 'THURSDAY'),
    (5, 'FRIDAY'),
    (6, 'SATURDAY'),
]
class Shift(BaseModel) :
    name = models.CharField(max_length=16, null=True, blank=True)
    code = models.CharField(max_length=24, unique=True)

    start_day = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()

    end_day = models.IntegerField(choices=DAYS_OF_WEEK)
    end_time = models.TimeField()

    class Meta:
        db_table = 'shift'
        managed = True
        verbose_name_plural = 'Shifts'
        indexes = [
            models.Index(fields=['start_day', 'start_time']),
            models.Index(fields=['end_day', 'end_time']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.code}"
    
class Branch(BaseModel) :
    name = models.CharField(max_length=81)
    code = models.CharField(max_length=24, unique=True)

    company = models.ManyToManyField('Company', related_name='companies')

    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    province = models.CharField(max_length=32, null=True, blank=True)
    postal_code = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'branch'
        managed = True
        verbose_name_plural = 'Branches'
        indexes = [
            models.Index(fields=['code'])
        ]
    
    def __str__(self):
        return f"{self.name} - {self.code}"
    
class Employee(BaseModel) :
    user_id = models.IntegerField(db_index=True)
    nik = models.IntegerField()
    code = models.CharField(max_length=24, unique=True)
    full_name = models.CharField(max_length=128)
    role_name = models.CharField(max_length=64, null=True, blank=True)

    first_name = models.CharField(max_length=24, null=True, blank=True)
    middle_name = models.CharField(max_length=24, null=True, blank=True)
    last_name = models.CharField(max_length=24, null=True, blank=True)

    birthplace = models.CharField(max_length=24, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    neighbourhood = models.CharField(max_length=9, null=True, blank=True)
    village = models.CharField(max_length=24, null=True, blank=True)
    district = models.CharField(max_length=24, null=True, blank=True)
    city = models.CharField(max_length=24, null=True, blank=True)
    province = models.CharField(max_length=24, null=True, blank=True)
    postal_code = models.CharField(max_length=12, null=True, blank=True)
    
    religion = models.CharField(max_length=12, null=True, blank=True)
    marital_status = models.CharField(max_length=16, null=True, blank=True)
    job = models.CharField(max_length=36, null=True, blank=True)
    citizenship = models.CharField(max_length=36, null=True, blank=True)

    company = models.ForeignKey('Company', on_delete=models.CASCADE, db_index=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, db_index=True)
    unit = models.ManyToManyField('Unit', related_name='units')
    level = models.ForeignKey('Level', on_delete=models.CASCADE, db_index=True)
    employment_type = models.ForeignKey('EmploymentType', on_delete=models.CASCADE, db_index=True)
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE, db_index=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', db_index=True)

    talenta_id = models.IntegerField(null=True, blank=True, db_index=True)

    hire_date = models.DateField(null=True, blank=True, db_index=True)
    resign_date = models.DateField(null=True, blank=True, db_index=True)

    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'employee'
        managed = True
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['company', 'branch']),
            models.Index(fields=['level'])
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.code}"