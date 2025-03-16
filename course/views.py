from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Subject
from .serializers import CourseSerializer, SubjectSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import logging
from rest_framework import status

logger = logging.getLogger(__name__)


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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


@api_view(['GET'])
def getCourses(request):
    courses = Course.objects.all().prefetch_related('teachers__user')
    courses_info = []
    for course in courses:
        teachers = [{'id': teacher.user.id, 'name': f'{teacher.user.first_name} {teacher.user.last_name}'}
                    for teacher in course.teachers.all()]
        courses_info.append({
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'tuition_fee': course.tuition_fee,
            'discount': course.discount,
            'discount_end_date': course.discount_end_date,
            'lesson_count': course.lesson_count,
            'exercise_count': course.exercise_count,
            'current_student_count': course.current_student_count,
            'graduation_date': course.graduation_date,
            'creation_date': course.creation_date,
            'announcement': course.announcement,
            'average_rating': course.average_rating,
            'img': course.img.url,
            'teachers': teachers
        })
    return Response(courses_info)
