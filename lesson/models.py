from django.db import models

# Create your models here.

class lesson_model(models.Model):
    lesson_title = models.CharField(max_length=200)
    lesson_content = models.TextField()
    lesson_date = models.DateField()
