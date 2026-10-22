# Đề 8: Hệ thống Quản lý Phòng khám / Bệnh viện

**Học phần:** Triển khai và Quản trị Hệ thống Phần mềm  
**Sinh viên:** Nông Thành Chung  
**Mã số SV:** DTC245200423  
**Lớp:** CNTT K23M  
**Repository:** [https://github.com/DTC245200423/De8_QuanLyPhongKham_BenhVien.git](https://github.com/DTC245200423/De8_QuanLyPhongKham_BenhVien.git)

---

## 1. Giới thiệu hệ thống

Hệ thống Quản lý Phòng khám / Bệnh viện được đóng gói và triển khai hoàn chỉnh bằng **Docker Compose** với đầy đủ các thành phần theo tiêu chuẩn DevOps:

1. **Ứng dụng Web:** Django (Python) quản lý Bác sĩ, Bệnh nhân và Lịch hẹn khám bệnh với giao diện trực quan và trang quản trị Django Admin.
2. **Cơ sở dữ liệu:** PostgreSQL 15 kèm công cụ quản trị giao diện trực quan pgAdmin 4.
3. **Nginx Reverse Proxy:** Đóng vai trò cổng vào duy nhất (Port 80), điều hướng yêu cầu tới ứng dụng Web và thiết lập các Security Headers bảo vệ ứng dụng.
4. **Hệ thống giám sát (Monitoring):**
   - **Prometheus:** Thu thập metrics thời gian thực từ cAdvisor (Container metrics) và Postgres Exporter (Database metrics).
   - **Grafana:** Tự động nạp Dashboard giám sát tài nguyên CPU, RAM, trạng thái dịch vụ và số lượng kết nối DB.
5. **Hệ thống ghi log tập trung (Logging):**
   - **Promtail:** Thu thập log tự động từ Docker Socket (`/var/run/docker.sock`).
   - **Loki:** Lưu trữ và lập chỉ mục log.
   - **LogQL:** Hỗ trợ truy vấn và phân tích log chuyên sâu trên Grafana Explore.
6. **Bảo mật và Hardening:**
   - Non-root container (`appuser`) trong Dockerfile của Web app.
   - Phân lập mạng nội bộ (`frontend_net` và `backend_net`), chặn truy cập trực tiếp vào Web và Database từ bên ngoài máy chủ.
   - Giới hạn tài nguyên phần cứng (CPU 0.5 core, RAM 512MB) chống tấn công từ chối dịch vụ (DoS).
   - Nginx Security Headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy`) và ẩn thông tin phiên bản (`server_tokens off`).
   - Áp dụng chính sách mật khẩu mạnh đồng bộ trên toàn bộ các dịch vụ.

---

## 2. Yêu cầu môi trường

- **Docker Desktop** (bật WSL2 trên Windows hoặc Docker Engine trên Linux/macOS)
- **Git**

---

## 3. Hướng dẫn cài đặt và vận hành

### Bước 1: Clone mã nguồn
```bash
git clone https://github.com/DTC245200423/De8_QuanLyPhongKham_BenhVien.git
cd De8_QuanLyPhongKham_BenhVien
```

### Bước 2: Khởi tạo file môi trường `.env`
```bash
# Trên Windows (PowerShell / Command Prompt):
copy .env.example .env

# Trên Linux / macOS:
cp .env.example .env
```

### Bước 3: Khởi chạy toàn bộ hệ thống bằng Docker Compose
```bash
docker compose up -d
```
> *Hệ thống sẽ tự động build image, chạy database migration, nạp dữ liệu mẫu khởi tạo (`seed_data`) và cấu hình sẵn Dashboard Grafana.*

### Bước 4: Kiểm tra trạng thái các container
```bash
docker compose ps
```
Đảm bảo tất cả 8 containers (`nginx`, `web`, `db`, `pgadmin`, `prometheus`, `grafana`, `cadvisor`, `postgres-exporter`, `loki`, `promtail`) đều ở trạng thái **running (Up)**.

---

## 4. Danh sách dịch vụ và thông tin tài khoản truy cập

| Dịch vụ | Địa chỉ URL | Cổng Host | Tài khoản đăng nhập / Kết nối |
|:---|:---|:---:|:---|
| **Website Phòng khám** | [http://localhost](http://localhost) | 80 (qua Nginx) | Không cần đăng nhập |
| **Django Admin** | [http://localhost/admin](http://localhost/admin) | 80 (qua Nginx) | `admin` / `StrongPassword123!` |
| **pgAdmin 4** | [http://localhost:5050](http://localhost:5050) | 5050 | `admin@admin.com` / `StrongPassword123!` |
| **Grafana Dashboard** | [http://localhost:3000](http://localhost:3000) | 3000 | `admin` / `StrongPassword123!` |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | 9090 | Truy cập trực tiếp (không mật khẩu) |

### Hướng dẫn kết nối Database trên pgAdmin:
1. Đăng nhập vào `http://localhost:5050` với tài khoản `admin@admin.com` / `StrongPassword123!`.
2. Chuột phải vào **Servers** -> **Register** -> **Server...**
3. Tab **General**: Đặt Name tùy ý (ví dụ: `Clinic_Postgres`).
4. Tab **Connection**:
   - **Host name/address:** `db`
   - **Port:** `5432`
   - **Maintenance database:** `clinic_db`
   - **Username:** `clinic_user`
   - **Password:** `StrongPassword123!`
5. Bấm **Save** để kết nối và xem các bảng `clinic_doctor`, `clinic_patient`, `clinic_appointment`.

---

## 5. Danh mục các câu truy vấn LogQL mẫu (Loki)

Mở Grafana -> Menu **Explore** -> Chọn data source **Loki**:

1. **Xem toàn bộ log của tất cả các container đang chạy:**
   ```logql
   {container_name=~".+"}
   ```
2. **Xem luồng log riêng của ứng dụng Web phòng khám:**
   ```logql
   {container_name=~".*web.*"}
   ```
3. **Lọc log các request HTTP GET thành công vào ứng dụng:**
   ```logql
   {container_name=~".*web.*"} |= "GET /"
   ```
4. **Lọc các dòng log cảnh báo hoặc báo lỗi trên toàn hệ thống:**
   ```logql
   {container_name=~".*"} |= "error"
   ```

---

## 6. Biện pháp bảo mật & Hardening đã áp dụng

1. **Non-root Container:** Container `web` được cấu hình tạo và chuyển sang người dùng thường `appuser` (UID non-root) trong `Dockerfile`, ngăn chặn leo thang đặc quyền khi bị tấn công.
2. **Network Isolation (Phân lập mạng):** 
   - Tách thành 2 mạng: `frontend_net` (Nginx, Web) và `backend_net` (Web, Database, Monitoring).
   - Container `web` không mở cổng 8000 ra máy host; toàn bộ người dùng bắt buộc phải đi qua Reverse Proxy Nginx.
   - Database PostgreSQL chỉ nằm trong `backend_net`, không mở port 5432 ra Internet/Host.
3. **Giới hạn tài nguyên (Resource Quota):** Khống chế tối đa `cpus: '0.50'` và `memory: 512M` cho Web server để chống DoS/cạn kiệt tài nguyên host.
4. **Nginx Security Headers & Server Masking:**
   - Bổ sung `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy`.
   - Cấu hình `server_tokens off;` để giấu phiên bản Nginx đang chạy.
5. **Chính sách mật khẩu mạnh (Strong Passwords):**
   - Đồng bộ mật khẩu phức tạp gồm chữ hoa, chữ thường, chữ số và ký tự đặc biệt (`StrongPassword123!`) cho PostgreSQL, pgAdmin, Grafana và Django Admin.

---

## 7. Dừng và dọn dẹp hệ thống

```bash
# Dừng các container
docker compose down

# Dừng và xóa cả Volume dữ liệu nếu muốn làm mới hoàn toàn
docker compose down -v
```