from rest_framework.permissions import BasePermission
from .models import Teacher, Manager, Student

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        try:
            return Teacher.objects.filter(user=request.user).exists()
        except Teacher.DoesNotExist:
            return False

class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            return Manager.objects.filter(user=request.user).exists()
        except Manager.DoesNotExist:
            return False

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        try:
            return Student.objects.filter(user=request.user).exists()
        except Student.DoesNotExist:
            return False