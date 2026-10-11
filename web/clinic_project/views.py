from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Chào mừng đến với Hệ thống Quản lý Phòng khám!</h1><p>Hệ thống đang hoạt động tốt.</p>")