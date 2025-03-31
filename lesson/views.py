from django.shortcuts import render
from rest_framework import viewsets
from .serializers import LessonSerializer, Lesson, LessonCommentSerializer, LessonComment, ExerciseSerializer, Exercise
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course_id', 'teacher_id']
    ordering = ['numerical_order']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        course = instance.course
        course.lesson_count -= 1
        course.save()
        lessons_to_update = Lesson.objects.filter(
            course=course, numerical_order__gte=instance.numerical_order+1)
        for lesson in lessons_to_update:
            lesson.numerical_order -= 1
            lesson.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson_id']


class LessonCommentViewSet(viewsets.ModelViewSet):
    queryset = LessonComment.objects.all()
    serializer_class = LessonCommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson__id', 'user__id']
