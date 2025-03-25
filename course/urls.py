from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SubjectViewSet, RegisterCourseViewSet
from . import views

router = DefaultRouter()
router.register(r'course', CourseViewSet)

router.register(r'subject', SubjectViewSet)

router.register(r'registerCourse', RegisterCourseViewSet, basename='registerCourse')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('dashboard/', views.dashBoardManager, name='dashboard'),
    path('check-connection/', views.check_connection, name='check-connection'),
]
