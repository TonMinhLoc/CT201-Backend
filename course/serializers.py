from rest_framework import serializers
from .models import Course, Subject, RegisterCourse
from user.models import Manager, Teacher, Student
from user.serializers import TeacherSerializer, ManagerSerializer, StudentSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    teachers = TeacherSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    teachers_ids = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), many=True, write_only=True)
    subject_id = serializers.UUIDField(write_only=True)
    manager_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'tuition_fee', 'discount', 'discount_end_date',
            'lesson_count', 'exercise_count', 'status', 'current_student_count', 'registration_deadline',
            'graduation_date', 'creation_date', 'announcement', 'average_rating', 'subject',
            'teachers', 'teachers_ids', 'manager_id', 'subject_id', 'img'
        ]

    def create(self, validated_data):
        teachers_data = validated_data.pop('teachers_ids', [])
        course = Course.objects.create(**validated_data)
        course.teachers.set(teachers_data)
        course.save()
        return course

    def update(self, instance, validated_data):
        teachers_data = validated_data.pop('teachers_ids', None)
        if teachers_data:
            instance.teachers.set(teachers_data)
        return super().update(instance, validated_data)
    
    def validate(self, attrs):

        return attrs


class RegisterCourseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    course_id = serializers.UUIDField()
    student_id = serializers.UUIDField()
    # course = CourseSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = RegisterCourse
        fields = ['student', 'id', 'registraition_date', 'status',
                  'course_fee_at_registration', 'course_id', 'student_id']

    def validate(self, attrs):
        student_id = attrs.get('student_id')
        course_id = attrs.get('course_id')
        if RegisterCourse.objects.filter(student_id=student_id, course_id=course_id).exists():
            raise serializers.ValidationError(
                "Học viên đã đăng ký khóa học này rồi.")
        return attrs
