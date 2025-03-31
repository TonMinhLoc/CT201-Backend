from django.db import models
from user.models import Teacher, Manager, Student
from django.core.validators import MinValueValidator
import uuid


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    # Học phí
    tuition_fee = models.DecimalField(
        max_digits=15, decimal_places=2, blank=False, null=False,
    )
    # Giảm giá
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    # Ngày kết thúc giảm giá
    discount_end_date = models.DateField(blank=True, null=True)
    # Số bài học
    lesson_count = models.IntegerField(default=0, editable=False)
    # Số bài tập
    exercise_count = models.IntegerField(default=0, editable=False)
    # Trạng thái khóa học
    status = models.CharField(max_length=50, default="true")
    # Số học sinh đang đăng kí
    current_student_count = models.IntegerField(default=0, editable=False)
    # Ngày hết hạn đăng kí học
    registration_deadline = models.DateField(blank=True, null=True)
    # Ngày khai giảng khoá học
    graduation_date = models.DateField(blank=False, null=False)
    # Ngày tạo khoá học
    creation_date = models.DateField(auto_now_add=True)
    # Thông báo
    announcement = models.TextField(null=True, blank=True)
    # Số lượt đánh giá
    rating_count = models.PositiveIntegerField(default=0, editable=False)
    # Đánh giá trung bình của học sinh
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=-1, editable=False)
    img = models.ImageField(upload_to='img_course/')
    # mô tả thêm
    bullet_points = models.JSONField(verbose_name="Danh sách mô tả chính", blank=True, null=True)
    highlights = models.JSONField(verbose_name="Đặc điểm nổi bật", blank=True, null=True)
    outcomes = models.JSONField(verbose_name="Kết quả học tập", blank=True, null=True)
    # Môn học
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    # Giảng viên của khoá học
    teachers = models.ManyToManyField(Teacher)
    # Người tạo khoá học
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT)


class RegisterCourse(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('refund', 'Refund'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    registraition_date = models.DateField(
        auto_now_add=True, blank=False, null=False, editable=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="success")
    course_fee_at_registration = models.DecimalField(
        max_digits=15, decimal_places=2, blank=False, null=False, editable=False
    )
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name='registered_course')
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name='registered_student')


class CourseComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(blank=False, null=False)
    number_of_likes = models.IntegerField(
        blank=False, null=False, default=0, validators=[MinValueValidator(0)], editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name='comments')
    user = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name='comments')