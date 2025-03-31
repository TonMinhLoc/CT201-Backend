from rest_framework import serializers
from .models import Competition, TestResult
from user.models import Teacher
from course.models import Course
from question.models import Question


class CompetitionSerializer(serializers.ModelSerializer):
    teacher_id = serializers.UUIDField()
    course_ids = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)
    question_ids = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True)

    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'total_questions', 
                  'total_test_time', 'question_ids', 'course_ids', 'teacher_id']
        read_only_fields = ['id']

    def create(self, validated_data):
        courses_data = validated_data.pop('course_ids', [])
        questions_data = validated_data.pop('question_ids', [])
        competition = Competition.objects.create(**validated_data)
        competition.courses.set(courses_data)
        competition.questions.set(questions_data)
        competition.save()
        return super().create(validated_data)
    
    
