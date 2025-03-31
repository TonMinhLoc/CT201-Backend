from django.db import models
from course.models import Course, Teacher
from user.models import User
from question.models import Question, Choice
import uuid

# Create your models here.

class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    pdf_file = models.FileField(upload_to="lesson_pdfs/")
    video_file = models.FileField(upload_to="lesson_video", blank=False, null=False)
    duration = models.IntegerField(editable=False)
    numerical_order = models.IntegerField(blank=False, null=False)
    number_of_lesson_views = models.IntegerField(blank=False, null=False, default=0, editable=False)
    number_of_likes = models.IntegerField(blank=False, null=False, default=0, editable=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="lesson")

class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=False, null=False)
    total_time = models.IntegerField()
    total_questions = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    pdf_file = models.FileField(upload_to="exercises_pdfs/")
    number_of_lesson_exercise = models.IntegerField(blank=False, null=False, default=0, editable=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="exercises")
    questions = models.ManyToManyField(Question)

class LessonComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(blank=False, null=False)
    number_of_likes = models.IntegerField(blank=False, null=False, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class StudentWorkResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    total_correct_questions = models.PositiveIntegerField(blank=False, null=False, editable=False)
    total_complite_time = models.IntegerField(null=False, blank=False)
    is_complite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    choice = models.ManyToManyField(Choice)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_work_result")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)


    
    
    
