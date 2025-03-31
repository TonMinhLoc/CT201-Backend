from django.db import models
from user.models import Teacher
import uuid

# Create your models here.


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(blank=False, null=False)
    is_public = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="question")
    created_at = models.DateTimeField(auto_now_add=True)


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.CharField(max_length=255, blank=False, null=False)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")

    