from rest_framework import serializers
from .models import Course, Subject, RegisterCourse
from user.models import Manager, Teacher, Student
from user.serializers import TeacherSerializer, ManagerSerializer, StudentSerializer
from datetime import date
from django.shortcuts import get_object_or_404
import django_filters


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
            'teachers', 'teachers_ids', 'manager_id', 'subject_id', 'img', 
            'bullet_points', 'highlights', 'outcomes', 'rating_count'
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
        tuition_fee = attrs.get('tuition_fee')
        discount = attrs.get('discount')
        registration_deadline = attrs.get('registration_deadline')
        graduation_date = attrs.get('graduation_date')
        discount_end_date = attrs.get('discount_end_date')

        if tuition_fee < 0:
            raise serializers.ValidationError("Học phí không thể nhỏ hơn 0.")

        if discount > tuition_fee:
            raise serializers.ValidationError(
                "Giảm giá không thể lớn hơn học phí.")

        if registration_deadline is not None and registration_deadline <= date.today():
            raise serializers.ValidationError(
                "Ngày đăng ký phải sau ngày hiện tại.")

        if discount_end_date is not None and discount_end_date <= date.today():
            raise serializers.ValidationError(
                "Ngày kết thúc giảm giá phải sau ngày hiện tại.")

        if graduation_date is not None and graduation_date <= date.today():
            raise serializers.ValidationError(
                "Ngày khai giảng phải sau ngày hiện tại.")

        return super().validate(attrs)


class RegisterCourseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    course_id = serializers.UUIDField(write_only=True)
    student_id = serializers.UUIDField()
    course = CourseSerializer(read_only=True)

    class Meta:
        model = RegisterCourse
        fields = ['id', 'registraition_date', 'status',
                  'course_fee_at_registration', 'course_id', 'student_id', 'course']

    def validate(self, attrs):
        student_id = attrs.get('student_id')
        course_id = attrs.get('course_id')
        if student_id and course_id:
            register_course_exists = RegisterCourse.objects.filter(
                student_id=student_id, course_id=course_id)
            if register_course_exists.exists() and register_course_exists[0].status == "success":
                raise serializers.ValidationError(
                    "Học viên đã đăng ký khóa học này rồi.")

            student = get_object_or_404(Student, id=student_id)
            course = get_object_or_404(Course, id=course_id)

            if student.current_amount < course.tuition_fee:
                raise serializers.ValidationError(
                    "Học viên không đủ tiền đăng kí khoá học.")

            attrs['course_fee_at_registration'] = course.tuition_fee - \
                course.discount

        return super().validate(attrs)

    def create(self, validated_data):
        student = get_object_or_404(
            Student, id=validated_data.get('student_id'))
        student.current_amount -= validated_data.get(
            'course_fee_at_registration')
        student.save()
        return super().create(validated_data)


class RegisterCourseFilter(django_filters.FilterSet):
    registraition_date = django_filters.DateFromToRangeFilter(
        field_name='registraition_date',
        label='Ngày đăng ký'
    )

    student__user__id = django_filters.NumberFilter(
        field_name='student__user__id',
        label='ID người dùng'
    )

    status = django_filters.ChoiceFilter(
        choices=RegisterCourse.STATUS_CHOICES,  # Nếu có choices
        label='Trạng thái'
    )

    class Meta:
        model = RegisterCourse
        fields = ['student__user__id', 'registraition_date', 'status']
