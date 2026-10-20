# Đề 8: Hệ thống Quản lý Phòng khám / Bệnh viện

**Sinh viên:** Nông Thành - DTC245200423 - CNTT K23M

## Mô tả

Hệ thống quản lý phòng khám triển khai bằng Docker Compose với đầy đủ thành phần:

- Ứng dụng web Django + PostgreSQL + pgAdmin
- Nginx Reverse Proxy (Security Headers)
- Prometheus + Grafana (Giám sát)
- Loki + Promtail (Log tập trung)
- Hardening bảo mật

## Yêu cầu hệ thống

- Docker Desktop
- Git

## Hướng dẫn chạy

### Bước 1: Clone repository

git clone https://github.com/DTC245200423/De8_QuanLyPhongKham_BenhVien.git
cd De8_QuanLyPhongKham_BenhVien

### Bước 2: Tạo file .env

copy .env.example .env

### Bước 3: Khởi chạy hệ thống

docker compose up -d

### Bước 4: Kiểm tra trạng thái

docker compose ps

## Các URL truy cập

| Dịch vụ | URL | Tài khoản |
|---------|-----|-----------|
| Website | http://localhost | - |
| pgAdmin | http://localhost:5050 | admin@admin.com / admin |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | - |

## Truy vấn LogQL mẫu (Thực hiện trên Grafana Explore -> Loki)

1. **Xem toàn bộ log của tất cả container:**
   ```logql
   {container_name=~".+"}
   ```
2. **Xem log riêng của ứng dụng Web phòng khám:**
   ```logql
   {container_name=~".*web.*"}
   ```
3. **Lọc log có chứa từ khóa lỗi hoặc cảnh báo:**
   ```logql
   {container_name=~".*"} |= "error"
   ```
4. **Lọc log các request HTTP GET thành công vào hệ thống:**
   ```logql
   {container_name=~".*web.*"} |= "GET /"
   ```

## Dừng hệ thống

docker compose down