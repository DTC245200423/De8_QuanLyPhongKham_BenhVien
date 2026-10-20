from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Doctor, Patient, Appointment

def health_check(request):
    """Healthcheck endpoint for monitoring / Nginx"""
    return JsonResponse({
        "status": "healthy",
        "service": "Clinic Management System",
        "time": timezone.now().isoformat()
    })

def dashboard(request):
    today = timezone.now().date()
    
    total_doctors = Doctor.objects.count()
    active_doctors = Doctor.objects.filter(is_active=True).count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    
    today_appointments = Appointment.objects.filter(appointment_date__date=today).count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date')[:6]
    doctors_list = Doctor.objects.filter(is_active=True)[:5]

    context = {
        'total_doctors': total_doctors,
        'active_doctors': active_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'recent_appointments': recent_appointments,
        'doctors_list': doctors_list,
        'active_tab': 'dashboard'
    }
    return render(request, 'clinic/dashboard.html', context)

def doctor_list(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        specialty = request.POST.get('specialty')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        room = request.POST.get('room', '')
        
        if full_name and specialty and phone:
            Doctor.objects.create(
                full_name=full_name,
                specialty=specialty,
                phone=phone,
                email=email,
                room=room
            )
            messages.success(request, f"Đã thêm bác sĩ {full_name} thành công!")
        else:
            messages.error(request, "Vui lòng điền đầy đủ các thông tin bắt buộc.")
        return redirect('doctor_list')

    search = request.GET.get('q', '')
    specialty_filter = request.GET.get('specialty', '')
    
    doctors = Doctor.objects.all()
    if search:
        doctors = doctors.filter(Q(full_name__icontains=search) | Q(phone__icontains=search))
    if specialty_filter:
        doctors = doctors.filter(specialty=specialty_filter)
        
    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
    
    return render(request, 'clinic/doctors.html', {
        'doctors': doctors,
        'specialties': specialties,
        'search': search,
        'selected_specialty': specialty_filter,
        'active_tab': 'doctors'
    })

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    name = doctor.full_name
    doctor.delete()
    messages.success(request, f"Đã xóa bác sĩ {name} khỏi hệ thống.")
    return redirect('doctor_list')

def patient_list(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender', 'Nam')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth') or None
        address = request.POST.get('address', '')
        medical_history = request.POST.get('medical_history', '')
        
        if full_name and phone:
            Patient.objects.create(
                full_name=full_name,
                gender=gender,
                phone=phone,
                date_of_birth=date_of_birth,
                address=address,
                medical_history=medical_history
            )
            messages.success(request, f"Đã tiếp nhận hồ sơ bệnh nhân {full_name}.")
        else:
            messages.error(request, "Vui lòng nhập họ tên và số điện thoại bệnh nhân.")
        return redirect('patient_list')

    search = request.GET.get('q', '')
    patients = Patient.objects.all()
    if search:
        patients = patients.filter(Q(full_name__icontains=search) | Q(phone__icontains=search))
        
    return render(request, 'clinic/patients.html', {
        'patients': patients,
        'search': search,
        'active_tab': 'patients'
    })

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.select_related('doctor').order_by('-appointment_date')
    return render(request, 'clinic/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
        'active_tab': 'patients'
    })

def appointment_list(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        reason = request.POST.get('reason')
        
        if patient_id and doctor_id and appointment_date and reason:
            patient = get_object_or_404(Patient, pk=patient_id)
            doctor = get_object_or_404(Doctor, pk=doctor_id)
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                reason=reason,
                status='pending'
            )
            messages.success(request, "Đã đặt lịch khám bệnh thành công!")
        else:
            messages.error(request, "Vui lòng điền đầy đủ các thông tin hẹn khám.")
        return redirect('appointment_list')

    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    if status_filter:
        appointments = appointments.filter(status=status_filter)
        
    doctors = Doctor.objects.filter(is_active=True)
    patients = Patient.objects.all()
    
    return render(request, 'clinic/appointments.html', {
        'appointments': appointments,
        'doctors': doctors,
        'patients': patients,
        'status_filter': status_filter,
        'active_tab': 'appointments'
    })

def appointment_update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')
    diagnosis = request.POST.get('diagnosis')
    
    if new_status in dict(Appointment.STATUS_CHOICES):
        appointment.status = new_status
        if diagnosis:
            appointment.diagnosis = diagnosis
        appointment.save()
        messages.success(request, f"Đã cập nhật trạng thái lịch hẹn: {appointment.get_status_display()}")
    return redirect('appointment_list')
