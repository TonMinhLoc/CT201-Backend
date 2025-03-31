from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'lesson', views.LessonViewSet)
router.register(r'lesson_comment', views.LessonCommentViewSet)
router.register(r'exercise', views.ExerciseViewSet)

urlpatterns = [
    path('viewset/', include(router.urls)),
]
