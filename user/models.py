from django.db import models
from django.contrib.auth.models import User
import uuid

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/')
    grade = models.IntegerField(default=1)

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birthT = models.DateField(null=True, blank=True)
    phone_numberT = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    professional_certification = models.CharField(max_length=255, null=True, blank=True)
    years_of_experience = models.IntegerField(null=False, blank=False)
    student_rating = models.FloatField()
    workplace = models.CharField(max_length=255, null=True, blank=True)
    academic_degree = models.CharField(max_length=100, null=True, blank=True)
    specialty = models.CharField(max_length=255, null=True, blank=True)

class Manager(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
