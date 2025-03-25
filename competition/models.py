from django.db import models
from user.models import Teacher
from course.models import Course
import uuid

# Create your models here.

# class Competitions(models.Model):
#     competition_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     competition_name = models.CharField(max_length=100, blank=False, null=False)
#     start_date = models.DateTimeField(blank=False, null=False)
#     end_date = models.DateField(blank=False, null=False)
#     description = models.TextField(blank=False, null=False)
#     total_questions = models.IntegerField(null=False, blank=False)
#     total_test_time = models.IntegerField(null=False, blank=False)
#     courses = models.ManyToManyField(Teacher)
#     teacher = models.ForeignKey(Course, on_delete=models.CASCADE)

