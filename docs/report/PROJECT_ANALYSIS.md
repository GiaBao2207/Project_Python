# PHÂN TÍCH TOÀN DIỆN HỆ THỐNG PHẦN MỀM (PROJECT_ANALYSIS)

> **Dự án**: Neon Parking Manager – Hệ Thống Quản Lý Bãi Giữ Xe Thông Minh  
> **Ngôn ngữ**: Python 3.10+ (Đang chạy trên Python 3.14)  
> **Kiến trúc**: 4-Tier Architecture (GUI $\rightarrow$ Service $\rightarrow$ Repository $\rightarrow$ MySQL Database)  
> **Nguồn đối chiếu**: Mã nguồn thực tế tại thư mục gốc `QuanLyBaiGiuXe/`

---

## 1. MỤC TIÊU VÀ BỐI CẢNH DỰ ÁN

### 1.1. Bài toán thực tế
Tại các đô thị và cơ quan, trường học hiện nay, lưu lượng phương tiện ra vào bãi đỗ xe (xe máy, ô tô, xe đạp) là rất lớn. Các phương thức quản lý truyền thống (ghi vé giấy bằng tay, tính tiền nhẩm) bộc lộ nhiều nhược điểm nghiêm trọng:
- Dễ rách, mất vé giấy, khó đối soát phương tiện khi xảy ra tranh chấp hoặc mất cắp.
- Thất thoát doanh thu do gian lận trong thu phí hoặc không có lịch sử ghi nhận minh bạch.
- Không nắm bắt được số lượng chỗ trống theo thời gian thực dẫn đến tình trạng quá tải, ùn tắc tại cổng bãi xe vào giờ cao điểm.
- Khó khăn trong việc tổng hợp báo cáo ca trực và phân tích xu hướng hoạt động.

### 1.2. Mục tiêu phần mềm
Đề tài **Neon Parking Manager** được phát triển nhằm tự động hóa toàn diện quy trình vận hành bãi đỗ xe:
1. **Quản lý dữ liệu tập trung & an toàn**: Ứng dụng hệ quản trị CSDL quan hệ MySQL Server với 7 bảng chuẩn hóa, áp dụng giao dịch Transaction (ACID) để chống mất mát dữ liệu và chặn race condition khi nhiều cổng cùng thao tác.
2. **Bảo mật và phân quyền chuẩn mực**: Băm mật khẩu người dùng bằng thuật toán **Argon2id** (`argon2-cffi`); phân quyền nghiêm ngặt giữa Quản trị viên (Admin) và Nhân viên trực ca tại tầng Nghiệp vụ (Service Layer).
3. **Nghiệp vụ giữ xe thực tế**: Hỗ trợ đa dạng loại phương tiện (Xe máy, Ô tô, Xe đạp); áp dụng cơ chế chụp snapshot đơn giá lúc gửi xe; tách bạch vé xe khỏi giao dịch thanh toán để chống thanh toán trùng.
4. **Trực quan hóa & Báo cáo**: Biểu đồ thống kê thời gian thực nhúng trực tiếp trên giao diện Desktop (Matplotlib); xuất báo cáo văn bản định dạng TXT chuẩn tiếng Việt UTF-8.
5. **Kế thừa & Bảo toàn lịch sử**: Giữ nguyên vẹn phiên bản dòng lệnh Console CLI (`main.py`) và tệp dữ liệu phẳng gốc `data/du_lieu_bai_xe.txt` để minh chứng quá trình nâng cấp từ cơ bản lên nâng cao.

---

## 2. NGƯỜI SỬ DỤNG VÀ PHÂN QUYỀN HỆ THỐNG

Hệ thống phân định rạch ròi 2 nhóm người dùng (vai trò lưu tại cột `vai_tro` bảng `nguoi_dung` và kiểm soát qua `models/nguoi_dung.py`, `services/auth_service.py`):

| Vai trò (Role) | Đối tượng thực tế | Quyền hạn và Phạm vi hoạt động |
| :--- | :--- | :--- |
| **QUẢN TRỊ VIÊN (`ADMIN`)** | Ban quản lý, Chủ bãi xe, Đội trưởng bảo vệ | • Toàn quyền xem và thao tác trên tất cả 9 phân hệ.<br>• Xem bảng điều khiển tổng quan (Dashboard) và doanh thu chi tiết (toàn bãi, theo ngày, theo ca).<br>• Quản lý tài khoản nhân viên: tạo mới nhân viên (Argon2id), sửa thông tin, khóa/mở khóa tài khoản, đặt lại mật khẩu (chống tự khóa chính mình).<br>• Cài đặt hệ thống: thay đổi bảng giá vé từng loại xe (chặn số âm, bảo toàn snapshot vé cũ), điều chỉnh tổng sức chứa (chặn giảm sức chứa dưới số xe đang đỗ thực tế).<br>• Xem và lọc nhật ký kiểm toán (Audit log) mọi hành vi trong hệ thống.<br>• Xuất tất cả các loại báo cáo dữ liệu. |
| **NHÂN VIÊN (`NHAN_VIEN`)** | Nhân viên bảo vệ trực cổng, Thu ngân bãi xe | • Đăng nhập ca trực, đổi mật khẩu cá nhân.<br>• Tiếp nhận phương tiện vào bãi (Check-in), cấp mã vé tự động an toàn.<br>• Tra cứu phương tiện đang gửi (tìm kiếm thông minh, lọc theo loại xe).<br>• Xử lý xe ra bãi (Check-out), thu phí (tiền mặt / chuyển khoản) và mở cổng.<br>• Xem thống kê lấp đầy bãi xe và xuất báo cáo danh sách xe đang gửi.<br>• **Bị chặn tuyệt đối** tại Service Layer khi cố truy cập màn hình Doanh thu, Quản lý nhân viên, Cài đặt bảng giá/sức chứa hoặc xem Nhật ký toàn hệ thống. |

---

## 3. KIẾN TRÚC PHÂN TẦNG HỆ THỐNG (4-TIER ARCHITECTURE)

Dự án tuân thủ nghiêm ngặt mô hình kiến trúc phân tầng 4 lớp hướng đối tượng, tách bạch trách nhiệm (Separation of Concerns):

```text
[KIẾN TRÚC PHÂN TẦNG NEON PARKING MANAGER]

┌──────────────────────────────────────────────────────────────────┐
│ 1. TẦNG GIAO DIỆN (GUI LAYER - CustomTkinter)                     │
│    app_desktop.py, MainWindow, Sidebar, Header, CyberDialog      │
│    9 Modules: Dashboard, Vehicles, Tickets, Revenue, Statistics, │
│               Users, Settings, Reports, Audit                    │
│    (Chỉ bắt sự kiện, hiển thị dữ liệu, TUYỆT ĐỐI không viết SQL) │
└───────────────────────────────┬──────────────────────────────────┘
                                │ Gọi hàm nghiệp vụ / Nhận Object
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. TẦNG NGHIỆP VỤ (SERVICE LAYER)                                 │
│    AuthService: Xác thực Argon2id, quản lý phiên, kiểm tra quyền │
│    BaiXeDbService: Tiếp nhận xe, xe ra, tính tiền, kiểm tra chỗ │
│    UserService: Thao tác tài khoản nhân viên, chống tự khóa      │
│    SettingsService: Ràng buộc giá và sức chứa không âm           │
│    AuditService: Phân trang và bộ lọc nhật ký hệ thống           │
│    ReportService: Xuất tệp báo cáo định dạng TXT UTF-8           │
└───────────────────────────────┬──────────────────────────────────┘
                                │ Chuyển đổi Model & Thực thi logic
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. TẦNG TRUY VẤN DỮ LIỆU (REPOSITORY LAYER)                       │
│    UserRepository: CRUD nguoi_dung, nhat_ky, đếm bản ghi         │
│    VehicleRepository: CRUD xe, ve_xe, bang_gia, suc_chua,        │
│                       thanh_toan, thực thi MySQL Transaction     │
└───────────────────────────────┬──────────────────────────────────┘
                                │ Kết nối / Commit / Rollback
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. TẦNG CƠ SỞ DỮ LIỆU (DATABASE & STORAGE LAYER)                 │
│    MySQL Server: Database neon_parking_db (7 bảng quan hệ)       │
│    Storage TXT: data/du_lieu_bai_xe.txt (bảo toàn bản Console cũ)│
│    Security: hasher.py (Argon2id), config/database.py (.env)     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. CHI TIẾT CÁC PHÂN HỆ NGHIỆP VỤ (MODULES) TRONG MÃ NGUỒN

### 4.1. Phân hệ Xác thực & Phân quyền (`gui/modules/auth/`)
- **Mã nguồn**: `gui/modules/auth/login_view.py`, `setup_admin_view.py`, `change_password_dialog.py`, `services/auth_service.py`, `security/hasher.py`.
- **Cơ chế**:
  - Khi khởi động, `AuthService.kiem_tra_can_setup_admin()` kiểm tra số lượng tài khoản trong bảng `nguoi_dung`. Nếu rỗng, hiển thị màn hình thiết lập Admin đầu tiên (First Admin Setup). Không bao giờ tạo mật khẩu Admin mặc định lộ lọt trong mã nguồn.
  - Mật khẩu được băm bằng chuẩn `argon2-cffi` (`PasswordHasher(time_cost=2, memory_cost=65536, parallelism=1, hash_len=32, type=Type.ID)`), chống lại các cuộc tấn công Brute-force và từ điển bằng phần cứng chuyên dụng.
  - Khi đăng nhập thành công, lưu thông tin thực thể `NguoiDung` vào biến phiên làm việc `AuthService._nguoi_dung_hien_tai`. Khi đăng xuất, xóa sạch thông tin phiên.

### 4.2. Phân hệ Tổng quan bãi xe (`gui/modules/dashboard/`)
- **Mã nguồn**: `gui/modules/dashboard/dashboard_view.py`, `services/bai_xe_db_service.py`, `gui/components/stat_card.py`, `gui/components/cyber_chart.py`.
- **Cơ chế**:
  - 4 thẻ KPI thời gian thực: *Xe đang gửi*, *Chỗ trống hiện có*, *Lượt vào hôm nay*, *Doanh thu hôm nay* (chỉ hiển thị số tiền đối với Admin, hiển thị bảo mật đối với Nhân viên).
  - Tích hợp biểu đồ cột 7 ngày gần nhất vẽ bằng **Matplotlib** nhúng trong CustomTkinter.
  - Bảng thống kê phân bố loại xe (Xe máy, Ô tô, Xe đạp) kèm tỷ lệ phần trăm lấp đầy sức chứa.

### 4.3. Phân hệ Quản lý phương tiện (`gui/modules/vehicles/`)
- **Mã nguồn**: `gui/modules/vehicles/vehicle_view.py`, `services/bai_xe_db_service.py`, `database/repositories/vehicle_repository.py`.
- **Cơ chế**:
  - **Form Tiếp nhận xe (Check-in)**:
    - Chọn loại xe bằng Segmented Button tiếng Việt: `Xe máy`, `Ô tô`, `Xe đạp`.
    - Tự động kiểm tra sức chứa khả dụng trước khi tiếp nhận: `suc_chua_hien_tai - so_xe_dang_gui > 0`. Nếu bãi đầy, từ chối tiếp nhận và thông báo rõ ràng.
    - Kiểm tra xe trùng: Sử dụng cột ảo `id_xe_dang_gui` kết hợp ràng buộc `UNIQUE` trong MySQL để chặn việc 1 phương tiện đang gửi lại được cấp thêm vé thứ 2.
    - Chụp snapshot đơn giá: Lấy giá vé hiện hành từ bảng `bang_gia` và lưu cố định vào cột `don_gia_ap_dung` của bảng `ve_xe`.
  - **Form Cho xe ra & Thanh toán (Check-out)**:
    - Nhập mã vé hoặc chọn vé từ bảng danh sách bên dưới (hỗ trợ cả Single-click và Double-click an toàn).
    - Hiển thị đầy đủ thông tin: Mã vé, Biển số/Mã thẻ, Thời gian vào, Thời gian ra, Thời lượng gửi xe, Đơn giá snapshot và Tổng tiền cần thanh toán.
    - Chọn phương thức: *Tiền mặt* hoặc *Chuyển khoản*.
    - Bật hộp thoại popup xác nhận trước khi thực thi giao dịch.
  - **Bảng danh sách xe đang gửi**:
    - Tích hợp thanh tìm kiếm thông minh theo từ khóa (Mã vé, Biển số, Tên chủ xe, Mã thẻ xe đạp).
    - Bộ lọc nhanh theo loại xe: `Tất cả`, `Xe máy`, `Ô tô`, `Xe đạp`.
    - Phân trang dữ liệu (Pagination) tối ưu hiệu năng: Trang trước / Trang sau, tránh nghẽn giao diện khi số lượng xe lớn.

### 4.4. Phân hệ Quản lý vé xe (`gui/modules/tickets/`)
- **Mã nguồn**: `gui/modules/tickets/ticket_view.py`.
- **Cơ chế**:
  - Tra cứu toàn bộ lịch sử vé xe trong hệ thống (cả vé đang gửi `Dang gui` và vé đã rời bãi `Da thanh toan`).
  - Lọc theo khoảng ngày tạo vé, theo loại phương tiện và trạng thái.
  - Xem chi tiết lịch sử một vé: ai là người tiếp nhận, ai là người thu tiền, thời điểm vào/ra chính xác đến từng giây.

### 4.5. Phân hệ Quản lý doanh thu (`gui/modules/revenue/`)
- **Mã nguồn**: `gui/modules/revenue/revenue_view.py`.
- **Cơ chế** (Chỉ Quản trị viên truy cập):
  - Tổng hợp doanh thu toàn bãi, doanh thu theo khoảng ngày tùy chọn.
  - Tách bạch rõ ràng nguồn tiền: Doanh thu Tiền mặt vs Doanh thu Chuyển khoản.
  - Biểu đồ Matplotlib xếp chồng (Stacked Bar Chart) thể hiện xu hướng biến động doanh thu 15 ngày gần nhất.
  - Bảng kê chi tiết từng giao dịch từ bảng `thanh_toan`, liên kết trực tiếp với mã vé và nhân viên thu tiền.

### 4.6. Phân hệ Thống kê hoạt động (`gui/modules/statistics/`)
- **Mã nguồn**: `gui/modules/statistics/statistics_view.py`.
- **Cơ chế**:
  - Phân tích giờ cao điểm trong 24 giờ của 30 ngày gần nhất (nhúng biểu đồ cột Matplotlib chỉ rõ khung giờ có lượng xe vào cao nhất trong ngày).
  - Thống kê tỷ lệ quay vòng chỗ đỗ (Turnover rate) và tỷ trọng từng loại phương tiện.

### 4.7. Phân hệ Quản lý nhân viên (`gui/modules/users/`)
- **Mã nguồn**: `gui/modules/users/users_view.py`, `services/user_service.py`, `database/repositories/user_repository.py`.
- **Cơ chế** (Chỉ Quản trị viên truy cập):
  - Danh sách tài khoản: Tên đăng nhập, Họ tên, Vai trò, Trạng thái (Hoạt động / Bị khóa), Ngày tạo.
  - Thêm tài khoản nhân viên mới: kiểm tra độ dài tên đăng nhập, kiểm tra trùng lặp và băm mật khẩu bằng Argon2id.
  - Khóa / Mở khóa tài khoản: Tạm dừng quyền đăng nhập của nhân viên khi nghỉ việc.
  - **Quy tắc an toàn cốt lõi**: Tuyệt đối không cho phép tài khoản Admin tự khóa chính mình.
  - Đặt lại mật khẩu (Reset password) cho nhân viên.

### 4.8. Phân hệ Cấu hình hệ thống (`gui/modules/settings/`)
- **Mã nguồn**: `gui/modules/settings/settings_view.py`, `services/settings_service.py`.
- **Cơ chế** (Chỉ Quản trị viên truy cập):
  - Quản lý 2 Tab: *Bảng Giá Vé* và *Sức Chứa Bãi Xe*.
  - Ràng buộc chặn số âm: Không cho phép nhập đơn giá hoặc sức chứa $< 0$.
  - **Ràng buộc nghiệp vụ quan trọng**: Không cho phép giảm sức chứa tối đa của một loại xe xuống thấp hơn số lượng xe loại đó đang thực tế gửi trong bãi (`tong_cho >= so_xe_dang_gui`).
  - Bảo toàn kế toán: Việc sửa đổi bảng giá chỉ có hiệu lực với các lượt xe vào sau thời điểm sửa, không làm thay đổi giá của các vé đang gửi hoặc vé trong quá khứ.

### 4.9. Phân hệ Xuất báo cáo văn bản (`gui/modules/reports/`)
- **Mã nguồn**: `gui/modules/reports/reports_view.py`, `services/report_service.py`.
- **Cơ chế**:
  - Cho phép xuất 3 loại báo cáo ra tệp văn bản định dạng `.txt`:
    1. Báo cáo danh sách phương tiện đang gửi trong bãi.
    2. Báo cáo lịch sử vé xe theo ngày.
    3. Báo cáo doanh thu và chi tiết giao dịch bàn giao ca trực.
  - Sử dụng chuẩn mã hóa **UTF-8**, căn chỉnh lề bảng ngay ngắn (ASCII Table), ghi chú rõ thời gian xuất và người lập báo cáo.
  - Tự động ghi vết sự kiện `XUAT_BAO_CAO` vào bảng `nhat_ky`.

### 4.10. Phân hệ Nhật ký hệ thống (`gui/modules/audit/`)
- **Mã nguồn**: `gui/modules/audit/audit_view.py`, `services/audit_service.py`.
- **Cơ chế** (Chỉ Quản trị viên truy cập):
  - Ghi nhận tự động mọi hành vi: `DANG_NHAP`, `DANG_XUAT`, `TIEP_NHAN_XE`, `XE_RA_THANH_TOAN`, `DOI_MAT_KHAU`, `THEM_NHAN_VIEN`, `SUA_BANG_GIA`, `SUA_SUC_CHUA`, `XUAT_BAO_CAO`...
  - Bộ lọc đa tiêu chí: Lọc theo khoảng ngày, lọc theo tài khoản thực hiện, lọc theo loại thao tác.
  - Hỗ trợ phân trang hiệu năng cao qua mệnh đề SQL `LIMIT` và `OFFSET`.

---

## 5. BẢO MẬT VÀ GIAO DỊCH DỮ LIỆU (TRANSACTIONS)

### 5.1. Xử lý Giao dịch MySQL (ACID Transactions)
Trong quản lý bãi xe, nghiệp vụ xe ra và thanh toán liên quan đến việc cập nhật trạng thái vé ở bảng `ve_xe` và thêm bản ghi thanh toán vào bảng `thanh_toan`. Nếu xảy ra sự cố mất điện hoặc lỗi kết nối giữa 2 câu lệnh, dữ liệu sẽ bị sai lệch (vé đã ra nhưng chưa thu tiền, hoặc đã thu tiền nhưng vé vẫn hiển thị đang gửi).
Dự án giải quyết triệt để vấn đề này qua context manager `giao_dich()` tại `database/db_connection.py`:
- Bắt đầu transaction (`autocommit = False`).
- Thực hiện câu lệnh cập nhật `ve_xe` (`trang_thai = 'Da thanh toan'`, `thoi_gian_ra = NOW()`).
- Thực hiện câu lệnh chèn vào `thanh_toan`.
- Gọi `conn.commit()` để hoàn tất đồng thời.
- Nếu xảy ra bất kỳ ngoại lệ nào, tự động gọi `conn.rollback()` để khôi phục trạng thái ban đầu, ngăn chặn sai lệch kế toán.

### 5.2. Chống Race Condition trong Kiểm tra Sức chứa
Khi nhiều cổng tiếp nhận hoạt động cùng lúc tại thời điểm bãi xe gần đầy (chỉ còn 1 chỗ trống), hai nhân viên có thể đồng thời kiểm tra thấy còn 1 chỗ và cùng bấm nhận xe.
Hệ thống sử dụng truy vấn đếm khóa dòng an toàn hoặc giao dịch kiểm tra điều kiện ngay trước khi chèn bản ghi mới vào `ve_xe`, đảm bảo số lượng xe đang gửi không bao giờ vượt quá `suc_chua.tong_cho`.
