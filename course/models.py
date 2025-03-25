from django.db import models
from user.models import Teacher, Manager, Student
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.

class CustomMinValueValidator(MinValueValidator):
    def __init__(self, limit_value, message=None):
        if message is None:
            message = _('Giá trị phải lớn hơn hoặc bằng %(limit_value)s.')
        super().__init__(limit_value, message)


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    # Học phía
    tuition_fee = models.DecimalField(
        max_digits=15, decimal_places=2, blank=False, null=False, validators=[CustomMinValueValidator(0.00)])
    # Giảm giá
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    # Ngày kết thúc giảm giá
    discount_end_date = models.DateField()
    # Số bài học
    lesson_count = models.IntegerField(default=0, editable=False)
    # Số bài tập
    exercise_count = models.IntegerField(default=0, editable=False)
    # Trạng thái khóa học
    status = models.CharField(max_length=50, default="active", editable=False)
    # Số học sinh đang đăng kí
    current_student_count = models.IntegerField(default=0, editable=False)
    # Ngày hết hạn đăng kí học
    registration_deadline = models.DateField(blank=False, null=False)
    # Ngày khai giảng khoá học
    graduation_date = models.DateField(blank=False, null=False)
    # Ngày tạo khoa hoc
    creation_date = models.DateField(auto_now_add=True)
    # Thông báo
    announcement = models.TextField(null=True, blank=True)
    # Đánh giá trung bình của học sinh
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=-1, editable=False)
    #
    img = models.ImageField(upload_to='img_course/')
    # Môn học
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    # Giảng viên của khoá học
    teachers = models.ManyToManyField(Teacher)
    # Quản lý của khoá học
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT)


class RegisterCourse(models.Model):
    STATUS_CHOICES = [
        ('PendingRegistrationApproval', 'Đang chờ duyệt đăng kí'),
        ('RegistrationSuccessful', 'Đăng kí thành công'),
        ('RegistrationNotApproved', 'Không được duyệt đăng kí'),
        ('PendingRefundApproval', 'Đang chờ duyệt hoàn tiền'),
        ('RefundSuccessful', 'Hoàn tiền thành công'),
        ('RefundNotApproved', 'Không được duyệt hoàn tiền'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    registraition_date = models.DateField(
        auto_now_add=True, blank=False, null=False, editable=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='PendingRegistrationApproval', editable=False)
    course_fee_at_registration = models.DecimalField(
        max_digits=15, decimal_places=2, blank=False, null=False, validators=[CustomMinValueValidator(0.00)])
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name='registered_course')
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name='registered_student')
