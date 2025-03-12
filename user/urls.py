from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from . import views

urlpatterns = [
    path('register/', views.StudentRegisterView.as_view(), name='custom_register'),
    path('manager_login/', views.ManagerLoginView.as_view(), name='manager_login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
    path('students/', views.get_students, name='get_students'),
    path('teachers/', views.get_teachers, name='get_teachers'),
]