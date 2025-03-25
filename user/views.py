from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from .serializers import StudentRegisterSerializer, TeacherSerializer, ManagerSerializer, StudentSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher, Manager, Student, User
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__id']

class ManagerViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__id']


class StudentRegisterView(RegisterView):
    serializer_class = StudentRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response

        except ValidationError as e:
            return Response({
                "error": "Lỗi xác thực",
                "details": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "error": "Đã xảy ra lỗi không mong muốn",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManagerLoginView(LoginView):
    def get_response(self):
        # Gọi phương thức cha để lấy response mặc định
        response = super().get_response()

        user = self.user  # Lấy người dùng hiện tại từ request

        # Kiểm tra xem người dùng có phải là Manager không
        # Sử dụng filter().first() thay vì get()
        manager = Manager.objects.filter(user=user).first()
        if manager:
            # Tuần tự hóa thông tin Manager
            manager_serializer = ManagerSerializer(manager)
            response.data['manager'] = manager_serializer.data
            return Response(response.data, status=status.HTTP_200_OK)
        else:
            response.data = {
                "error": "Unauthorized",
                "message": "Login failed: You are not a manager."
            }
            return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)


class CustomLoginView(LoginView):
    def get_response(self):
        # Gọi phương thức cha để lấy response mặc định
        response = super().get_response()

        user = self.user  # Lấy người dùng hiện tại từ request

        requested_role = self.request.data.get(
            'role', None)  # Lấy vai trò yêu cầu từ request

        # Xác định vai trò thực tế của người dùng
        if Teacher.objects.filter(user=user).exists():
            actual_role = 'teacher'
        elif Manager.objects.filter(user=user).exists():
            actual_role = 'manager'
        elif Student.objects.filter(user=user).exists():
            actual_role = 'student'
        else:
            actual_role = 'unknown'

        # Kiểm tra nếu vai trò yêu cầu không khớp với vai trò thực tế hoặc nếu vai trò yêu cầu là None
        if requested_role is None or requested_role != actual_role:
            response.data = {
                'error': f'Login failed: The requested role "{requested_role}" does not match the actual role "{actual_role}".'
            }
            return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)

        # Nếu vai trò khớp, trả về thông tin với vai trò thực tế
        response.data['role'] = actual_role
        return Response(response.data, status=status.HTTP_200_OK)

