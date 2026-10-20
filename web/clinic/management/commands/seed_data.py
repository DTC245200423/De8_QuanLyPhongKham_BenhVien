from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from clinic.models import Doctor, Patient, Appointment

class Command(BaseCommand):
    help = 'Tự động khởi tạo dữ liệu mẫu cho Hệ thống Quản lý Phòng khám'

    def handle(self, *args, **kwargs):
        self.stdout.write("Bắt đầu nạp dữ liệu mẫu...")

        if Doctor.objects.exists() and Patient.objects.exists():
            self.stdout.write(self.style.WARNING("Dữ liệu đã tồn tại trong hệ thống, bỏ qua seeding."))
            return

        # 1. Bác sĩ mẫu
        doctors_data = [
            {
                'full_name': 'Nguyễn Văn Hùng',
                'specialty': 'Nội tổng quát',
                'phone': '0912345601',
                'email': 'hung.nguyen@clinic.vn',
                'room': 'Phòng 101 - Tầng 1',
                'is_active': True
            },
            {
                'full_name': 'Trần Thị Thu Hà',
                'specialty': 'Nhi khoa',
                'phone': '0912345602',
                'email': 'ha.tran@clinic.vn',
                'room': 'Phòng 102 - Tầng 1',
                'is_active': True
            },
            {
                'full_name': 'Lê Hoàng Nam',
                'specialty': 'Tai Mũi Họng',
                'phone': '0912345603',
                'email': 'nam.le@clinic.vn',
                'room': 'Phòng 201 - Tầng 2',
                'is_active': True
            },
            {
                'full_name': 'Phạm Minh Tuấn',
                'specialty': 'Tim mạch',
                'phone': '0912345604',
                'email': 'tuan.pham@clinic.vn',
                'room': 'Phòng 202 - Tầng 2',
                'is_active': True
            },
            {
                'full_name': 'Đỗ Bích Phương',
                'specialty': 'Răng Hàm Mặt',
                'phone': '0912345605',
                'email': 'phuong.do@clinic.vn',
                'room': 'Phòng 301 - Tầng 3',
                'is_active': True
            },
        ]

        doctors = []
        for d in doctors_data:
            doc, _ = Doctor.objects.get_or_create(phone=d['phone'], defaults=d)
            doctors.append(doc)

        self.stdout.write(self.style.SUCCESS(f"Đã tạo {len(doctors)} bác sĩ mẫu."))

        # 2. Bệnh nhân mẫu
        patients_data = [
            {
                'full_name': 'Hoàng Minh Khang',
                'gender': 'Nam',
                'date_of_birth': date(1995, 4, 12),
                'phone': '0981112233',
                'address': 'Số 15 Hoàng Hoa Thám, Ba Đình, Hà Nội',
                'medical_history': 'Dị ứng phấn hoa và kháng sinh Penicillin nhẹ'
            },
            {
                'full_name': 'Nguyễn Phương Thảo',
                'gender': 'Nữ',
                'date_of_birth': date(2001, 8, 24),
                'phone': '0982223344',
                'address': 'Số 88 Cầu Giấy, Cầu Giấy, Hà Nội',
                'medical_history': 'Tiền sử viêm xoang mãn tính'
            },
            {
                'full_name': 'Vũ Đức Thịnh',
                'gender': 'Nam',
                'date_of_birth': date(1982, 11, 5),
                'phone': '0983334455',
                'address': 'Khu đô thị Times City, Hai Bà Trưng, Hà Nội',
                'medical_history': 'Huyết áp cao nhẹ, đang uống Amlodipine 5mg'
            },
            {
                'full_name': 'Lê Bảo Anh',
                'gender': 'Nam',
                'date_of_birth': date(2018, 6, 15),
                'phone': '0984445566',
                'address': 'Chung cư Ngoại Giao Đoàn, Bắc Từ Liêm, Hà Nội',
                'medical_history': 'Viêm phế quản co thắt khi thay đổi thời tiết'
            },
            {
                'full_name': 'Đặng Mai Lan',
                'gender': 'Nữ',
                'date_of_birth': date(1990, 1, 30),
                'phone': '0985556677',
                'address': 'Số 42 Phố Huế, Hoàn Kiếm, Hà Nội',
                'medical_history': 'Không có tiền sử bệnh lý đặc biệt'
            },
        ]

        patients = []
        for p in patients_data:
            pat, _ = Patient.objects.get_or_create(phone=p['phone'], defaults=p)
            patients.append(pat)

        self.stdout.write(self.style.SUCCESS(f"Đã tạo {len(patients)} bệnh nhân mẫu."))

        # 3. Lịch khám mẫu
        now = timezone.now()
        appointments_data = [
            {
                'patient': patients[0],
                'doctor': doctors[0],
                'appointment_date': now.replace(hour=8, minute=30, second=0),
                'reason': 'Đau tức ngực kèm theo sốt nhẹ và mệt mỏi 2 ngày nay',
                'diagnosis': 'Theo dõi viêm đường hô hấp trên. Kê Paracetamol và Vitamin C.',
                'status': 'completed'
            },
            {
                'patient': patients[1],
                'doctor': doctors[2],
                'appointment_date': now.replace(hour=9, minute=15, second=0),
                'reason': 'Nghẹt mũi kéo dài, đau vùng trán và hốc mắt khi cúi đầu',
                'diagnosis': 'Đợt cấp viêm xoang trán. Kê kháng sinh và xịt mũi.',
                'status': 'in_progress'
            },
            {
                'patient': patients[2],
                'doctor': doctors[3],
                'appointment_date': now.replace(hour=10, minute=0, second=0),
                'reason': 'Khám định kỳ tim mạch và đo lại điện tâm đồ ECG',
                'diagnosis': '',
                'status': 'pending'
            },
            {
                'patient': patients[3],
                'doctor': doctors[1],
                'appointment_date': now.replace(hour=14, minute=0, second=0),
                'reason': 'Bé ho nhiều về đêm, thở khò khè, biếng ăn',
                'diagnosis': '',
                'status': 'pending'
            },
            {
                'patient': patients[4],
                'doctor': doctors[4],
                'appointment_date': now - timedelta(days=1),
                'reason': 'Đau nhức răng hàm số 6 dưới bên phải, buốt khi uống nước lạnh',
                'diagnosis': 'Sâu răng độ 2 đã trám composite. Hẹn tái khám sau 6 tháng.',
                'status': 'completed'
            },
        ]

        for appt in appointments_data:
            Appointment.objects.get_or_create(
                patient=appt['patient'],
                doctor=appt['doctor'],
                appointment_date=appt['appointment_date'],
                defaults=appt
            )

        self.stdout.write(self.style.SUCCESS(f"Đã tạo {len(appointments_data)} lịch khám mẫu."))
        self.stdout.write(self.style.SUCCESS("Khởi tạo dữ liệu mẫu hoàn tất!"))
