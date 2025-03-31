from django.db import models
from django.contrib.auth.models import User
import uuid

sex_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=6, choices=sex_choices, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',null=False, blank=False)
    grade = models.IntegerField(default=1)
    current_amount = models.IntegerField(default=0, editable=False)

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=6, choices=sex_choices, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=False, blank=False)
    years_of_experience = models.IntegerField(null=False, blank=False)
    work_place = models.CharField(max_length=255,null=False, blank=False)
    academic_degree = models.CharField(max_length=100, null=False, blank=False)
    specialty = models.CharField(max_length=255, null=False, blank=False)
    info = models.JSONField(verbose_name="Danh sách mô tả chính", blank=True, null=True)
    description = models.TextField(max_length=255)

class Manager(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
