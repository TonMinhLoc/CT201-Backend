from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from .serializers import StudentRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher, Manager, Student
from rest_framework.decorators import api_view


class StudentRegisterView(RegisterView):
    serializer_class = StudentRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        print("📌 Received Data:", request.data)  # Debug request data
        
        try:
            response = super().create(request, *args, **kwargs)
            print("✅ Response Data:", response.data)  # Debug response data
            return response
        except Exception as e:
            # Nếu có lỗi, log lỗi ra console
            print("❌ Error creating student:", str(e))

            # Nếu request.data không hợp lệ, hiển thị lỗi chi tiết
            if hasattr(e, 'detail'):
                error_detail = e.detail
            else:
                error_detail = {"error": "Có lỗi xảy ra, vui lòng kiểm tra lại dữ liệu!"}

            return Response({"status": "error", "message": error_detail}, status=status.HTTP_400_BAD_REQUEST)



class ManagerLoginView(LoginView):
    def get_response(self):
        # Gọi phương thức cha để lấy response mặc định
        response = super().get_response()

        user = self.user  # Lấy người dùng hiện tại từ request
        
        # Kiểm tra xem người dùng có phải là Manager không
        if Manager.objects.filter(user=user).exists():
            return Response(response.data, status=status.HTTP_200_OK)
        else:
            # Trả về thông báo lỗi khi người dùng không phải là Manager
            response.data = {
                "message": "Login failed: You are not a manager."
            }
            return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)
            

class CustomLoginView(LoginView):
    def get_response(self):
        # Gọi phương thức cha để lấy response mặc định
        response = super().get_response()

        user = self.user  # Lấy người dùng hiện tại từ request
        
        requested_role = self.request.data.get('role', None)  # Lấy vai trò yêu cầu từ request

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
@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    students_info = []
    for student in students:
        user = student.user
        students_info.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    return Response(students_info)

@api_view(['GET'])
def get_teachers(request):
    teachers = Teacher.objects.all()
    teachers_info = []
    for teacher in teachers:
        user = teacher.user
        teachers_info.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    return Response(teachers_info)

        

