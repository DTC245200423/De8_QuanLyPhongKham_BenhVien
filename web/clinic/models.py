from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Họ và tên bác sĩ")
    specialty = models.CharField(max_length=100, verbose_name="Chuyên khoa")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    room = models.CharField(max_length=50, blank=True, null=True, verbose_name="Phòng khám")
    is_active = models.BooleanField(default=True, verbose_name="Đang công tác")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Bác sĩ"
        verbose_name_plural = "Danh sách Bác sĩ"
        ordering = ['full_name']

    def __str__(self):
        return f"BS. {self.full_name} ({self.specialty})"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
        ('Khác', 'Khác'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Họ và tên bệnh nhân")
    date_of_birth = models.DateField(verbose_name="Ngày sinh", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Nam', verbose_name="Giới tính")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ")
    medical_history = models.TextField(blank=True, null=True, verbose_name="Tiền sử bệnh lý / Dị ứng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng ký")

    class Meta:
        verbose_name = "Bệnh nhân"
        verbose_name_plural = "Danh sách Bệnh nhân"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ khám'),
        ('in_progress', 'Đang khám'),
        ('completed', 'Đã khám xong'),
        ('cancelled', 'Đã hủy'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name="Bệnh nhân")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Bác sĩ phụ trách")
    appointment_date = models.DateTimeField(verbose_name="Thời gian hẹn khám")
    reason = models.TextField(verbose_name="Triệu chứng / Lý do khám")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Kết luận / Đơn thuốc sơ bộ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời điểm đặt lịch")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    class Meta:
        verbose_name = "Lịch khám"
        verbose_name_plural = "Danh sách Lịch khám"
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Lịch hẹn: {self.patient.full_name} - {self.doctor.full_name} ({self.appointment_date.strftime('%d/%m/%Y %H:%M')})"
