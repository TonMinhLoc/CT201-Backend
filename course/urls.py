from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SubjectViewSet
from . import views

router = DefaultRouter()
router.register(r'course', CourseViewSet)

router.register(r'subject', SubjectViewSet)

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('dashboard/', views.dashBoardManager, name='dashboard'),
    path('check-connection/', views.check_connection, name='check-connection'),
    path('courses/', views.getCourses, name='courses'),
]
