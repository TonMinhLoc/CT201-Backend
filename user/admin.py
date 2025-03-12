from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Manager, Student

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Profile'

class ManagerInline(admin.StackedInline):
    model = Manager
    can_delete = False
    verbose_name_plural = 'Manager Profile'

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Profile'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_teacher', 'is_manager', 'is_student')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ( 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)



    def is_teacher(self, obj):
        return hasattr(obj, 'teacher')  # Kiểm tra user có hồ sơ giáo viên không
    is_teacher.boolean = True
    is_teacher.short_description = "Teacher"

    def is_manager(self, obj):
        return hasattr(obj, 'manager')  # Kiểm tra user có hồ sơ quản lý không
    is_manager.boolean = True
    is_manager.short_description = "Manager"
    
    def is_student(self, obj):
        return hasattr(obj, 'student')  # Kiểm tra user có hồ sơ học sinh không
    is_student.boolean = True
    is_student.short_description = "Student"


    

# Gỡ User mặc định và đăng ký lại với CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Manager)
admin.site.register(Student)