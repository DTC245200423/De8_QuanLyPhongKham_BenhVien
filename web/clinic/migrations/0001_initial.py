import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Họ và tên bác sĩ')),
                ('specialty', models.CharField(max_length=100, verbose_name='Chuyên khoa')),
                ('phone', models.CharField(max_length=20, verbose_name='Số điện thoại')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('room', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phòng khám')),
                ('is_active', models.BooleanField(default=True, verbose_name='Đang công tác')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
            ],
            options={
                'verbose_name': 'Bác sĩ',
                'verbose_name_plural': 'Danh sách Bác sĩ',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Họ và tên bệnh nhân')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Ngày sinh')),
                ('gender', models.CharField(choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Khác', 'Khác')], default='Nam', max_length=10, verbose_name='Giới tính')),
                ('phone', models.CharField(max_length=20, verbose_name='Số điện thoại')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Địa chỉ')),
                ('medical_history', models.TextField(blank=True, null=True, verbose_name='Tiền sử bệnh lý / Dị ứng')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày đăng ký')),
            ],
            options={
                'verbose_name': 'Bệnh nhân',
                'verbose_name_plural': 'Danh sách Bệnh nhân',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField(verbose_name='Thời gian hẹn khám')),
                ('reason', models.TextField(verbose_name='Triệu chứng / Lý do khám')),
                ('diagnosis', models.TextField(blank=True, null=True, verbose_name='Kết luận / Đơn thuốc sơ bộ')),
                ('status', models.CharField(choices=[('pending', 'Chờ khám'), ('in_progress', 'Đang khám'), ('completed', 'Đã khám xong'), ('cancelled', 'Đã hủy')], default='pending', max_length=20, verbose_name='Trạng thái')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm đặt lịch')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinic.doctor', verbose_name='Bác sĩ phụ trách')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='clinic.patient', verbose_name='Bệnh nhân')),
            ],
            options={
                'verbose_name': 'Lịch khám',
                'verbose_name_plural': 'Danh sách Lịch khám',
                'ordering': ['-appointment_date'],
            },
        ),
    ]
