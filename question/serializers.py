from rest_framework import serializers
from .models import Question, Choice, Teacher
from user.serializers import TeacherSerializer

class QuestionSerializer(serializers.ModelSerializer):
    teacher_id = serializers.UUIDField(write_only=True)
    teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'content', 'is_public', 'teacher_id', 'teacher']
        read_only_fields = ['id', 'created_at']
    
    

class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    question_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Choice
        fields = ['id', 'content', 'is_correct', 'question', 'question_id']