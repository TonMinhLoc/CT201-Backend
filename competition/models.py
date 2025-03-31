from django.db import models
from user.models import Teacher, Student
from course.models import Course
from question.models import Question
import uuid

# Create your models here.

class Competition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=False)
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    total_questions = models.IntegerField(null=False, blank=False)
    total_test_time = models.IntegerField(null=False, blank=False)
    questions = models.ManyToManyField(Question)
    courses = models.ManyToManyField(Course)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    

class TestResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, editable=False)
    total_correct_questions = models.PositiveIntegerField(blank=False, null=False, editable=False)
    total_complite_time = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(Student, related_name="test_result")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="test_result")
