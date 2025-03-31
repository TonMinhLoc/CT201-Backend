from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Subject, RegisterCourse
from .serializers import CourseSerializer, SubjectSerializer, RegisterCourseSerializer, RegisterCourseFilter
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework import status
from user.models import Teacher
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['teachers__user__id', 'status', 'subject__id']


class RegisterCourseViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = RegisterCourse.objects.all()
    serializer_class = RegisterCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #filterset_fields = ['student__user__id', 'registraition_date', 'status']
    filterset_class = RegisterCourseFilter

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        register_course = self.get_object()
        student = register_course.student
        student.current_amount += register_course.course_fee_at_registration
        student.save()
        register_course.delete()
        return Response({'status': 'success', 'message': 'Hoàn tiền và xóa phiếu đăng ký thành công.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def total_fee_by_date_range(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        register_courses = self.filter_queryset(self.get_queryset()).filter(
            registraition_date__gte=start_date,
            registraition_date__lte=end_date
        )
        total_free = register_courses.aggregate(
            models.Sum('course_fee_at_registration'))
        return Response(total_free)


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
