from django.contrib import admin
from .models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'phone', 'room', 'is_active')
    search_fields = ('full_name', 'specialty', 'phone')
    list_filter = ('specialty', 'is_active')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'phone', 'date_of_birth', 'created_at')
    search_fields = ('full_name', 'phone')
    list_filter = ('gender',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at')
    search_fields = ('patient__full_name', 'doctor__full_name', 'reason')
    list_filter = ('status', 'appointment_date')
