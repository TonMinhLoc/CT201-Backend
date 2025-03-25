from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, Teacher, Manager
import os


media = os.getenv('MEDIA')

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name',
                  'username', 'email', 'date_joined', 'is_active']
        read_only_fields = ['username']


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'user', 'date_of_birth', 'phone_number',
                  'address', 'profile_picture', 'grade', 'sex')
        
class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'date_of_birth', 'phone_number', 'address', 'profile_picture',
                  'sex', 'years_of_experience', 'work_place',
                  'academic_degree', 'specialty')


class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Manager()
        fields = ('id', 'user')


class StudentRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)

    date_of_birth = serializers.DateField(required=True, allow_null=False)
    phone_number = serializers.CharField(required=True, allow_null=False)
    address = serializers.CharField(required=True, allow_blank=False)
    profile_picture = serializers.ImageField(required=True, allow_null=True)
    grade = serializers.IntegerField(required=True, allow_null=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

        student, created = Student.objects.get_or_create(user=user)

        student.date_of_birth = self.validated_data.get('date_of_birth')
        student.address = self.validated_data.get('address')
        student.phone_number = self.validated_data.get('phone_number')
        student.profile_picture = self.validated_data.get('profile_picture')
        student.grade = self.validated_data.get('grade', 0)

        student.save()

        return user
