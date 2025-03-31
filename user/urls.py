from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'teacher', views.TeacherViewSet)
router.register(r'student', views.StudentViewSet)
router.register(r'manager', views.ManagerViewSet)


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('register/', views.StudentRegisterView.as_view(), name='custom_register'),
    path('manager_login/', views.ManagerLoginView.as_view(), name='manager_login'),
    path('teacher_login/', views.TeacherLoginView.as_view(), name='teacher_login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
]
