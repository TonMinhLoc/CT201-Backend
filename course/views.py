from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Subject, RegisterCourse
from .serializers import CourseSerializer, SubjectSerializer, RegisterCourseSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework import status
from user.models import Teacher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['teachers__user__id']


class RegisterCourseViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = RegisterCourse.objects.all()
    serializer_class = RegisterCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student__user__id']


@api_view(['GET'])
@permission_classes([AllowAny])
def check_connection(request):
    return JsonResponse({"status": "200", "message": "Backend is connected to frontend"})


@api_view(['GET'])
# Đảm bảo rằng tất cả người dùng đều có thể truy cập
def dashBoardManager(request):
    # Đếm số lượng khóa học có trạng thái 'Active'
    active_course_count = Course.objects.filter(status='Active').count()
    data = {
        'courses_count': 100,
        'lessons_count': 110,
        'students_count': 90,
        'teachers_count': 89,
        'registrations_count': 32,
        'feedback_count': 12
    }
    return JsonResponse(data)
