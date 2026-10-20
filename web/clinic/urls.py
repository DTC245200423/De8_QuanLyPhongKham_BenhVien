from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('health/', views.health_check, name='health_check'),
    
    # Bác sĩ
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    
    # Bệnh nhân
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    
    # Lịch khám
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/status/', views.appointment_update_status, name='appointment_update_status'),
]
