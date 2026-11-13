# Neon Parking Manager (Hệ Thống Quản Lý Bãi Giữ Xe Thông Minh)
👨‍💻 Tác giả

Trương Nguyễn Gia Bảo-Lớp DH23TIN02

Sinh viên Công nghệ thông tin – Đại học Nam Cần Thơ.

Dự án được thực hiện nhằm vận dụng kiến thức Python vào một bài toán quản lý thực tế, đồng thời rèn luyện kỹ năng thiết kế phần mềm, tổ chức mã nguồn và làm việc với cơ sở dữ liệu.

Ứng dụng quản lý bãi đỗ xe thông minh dành cho Windows Desktop với giao diện **Light Premium Automotive Management** (kết hợp màu sắc công nghệ Primary Teal `#087F83`, điểm nhấn Champagne Gold `#C5A46D` trên nền xám nhạt `#F3F6F8` và card trắng `#FFFFFF`), được phát triển bằng **Python OOP**, **CustomTkinter** và hệ quản trị cơ sở dữ liệu **MySQL**.

Dự án được nâng cấp từ phiên bản Console CLI nguyên bản, đảm bảo giữ nguyên khả năng vận hành của chương trình dòng lệnh và bảo toàn toàn bộ dữ liệu file TXT sẵn có.

---

## 1. Mục Tiêu Dự Án
- **Hiện đại hóa giao diện**: Chuyển đổi từ giao diện dòng lệnh (Console) sang giao diện đồ họa Desktop chuẩn phong cách Light Premium Automotive Management, tương phản cao, tinh tế, sang trọng và dịu mắt.
- **Quản lý dữ liệu tập trung với MySQL**: Chuyển từ file TXT phẳng sang hệ cơ sở dữ liệu quan hệ (RDBMS) `neon_parking_db` hỗ trợ Transaction (ACID), bảo toàn toàn vẹn dữ liệu và an toàn khi nhiều nhân viên cùng thao tác.
- **Bảo mật & Phân quyền chuẩn mực**:
  - Mã hóa băm mật khẩu bằng **Argon2id** (`argon2-cffi`), tiêu chuẩn an toàn hàng đầu hiện nay.
  - Quy trình thiết lập tài khoản Quản trị viên (Admin) đầu tiên một cách linh hoạt, không hardcode mật khẩu mặc định trong mã nguồn.
  - Phân quyền chặt chẽ ở tầng Nghiệp vụ (Service Layer) giữa **Admin** (toàn quyền quản trị) và **Nhân viên** (tiếp nhận xe, thu phí, xem báo cáo ca trực).
- **Nghiệp vụ giữ xe thực tế**:
  - Hỗ trợ đa dạng phương tiện: Xe đạp (mã định danh riêng, không bắt buộc biển số), Xe máy, Ô tô.
  - Chụp ảnh snapshot đơn giá (`don_gia_ap_dung`) tại thời điểm tiếp nhận, đảm bảo việc điều chỉnh bảng giá sau này không làm thay đổi giá của các vé đang gửi hoặc vé cũ.
  - Tách bạch bảng `thanh_toan` khỏi `ve_xe`, chống tạo trùng thanh toán cho cùng một vé qua ràng buộc `UNIQUE (ma_ve)`.
  - Kiểm soát sức chứa bãi xe an toàn đồng thời (concurrency-safe), tránh trường hợp nhận vượt quá số chỗ trống khi nhiều nhân viên cùng thao tác.
  - Thống kê doanh thu theo ngày, tra cứu lịch sử và xuất báo cáo ra file định dạng TXT chuyên nghiệp.

---

## 2. Công Nghệ Sử Dụng
- **Ngôn ngữ**: Python 3.10+ (đang chạy thực tế trên Python 3.14).
- **Mô hình lập trình**: Hướng đối tượng (Python OOP) áp dụng triệt để tính Đóng gói (Encapsulation), Kế thừa (Inheritance), và Đa hình (Polymorphism).
- **Giao diện Desktop**: `customtkinter` (Dark/Neon theme) kết hợp với `Pillow` (xử lý hình ảnh/icon).
- **Cơ sở dữ liệu**: MySQL Server 8.x / 9.x (`neon_parking_db`), kết nối qua thư viện chính thức `mysql-connector-python`.
- **Bảo mật**: `argon2-cffi` (thuật toán Argon2id chống tấn công dò mật khẩu GPU/ASIC).
- **Quản lý cấu hình**: `python-dotenv` (nạp biến môi trường từ file `.env`, tách biệt thông tin nhạy cảm khỏi mã nguồn).

---

## 3. Thiết Kế Cơ Sở Dữ Liệu MySQL (`neon_parking_db`)

Hệ thống thiết kế chuẩn hóa gồm **7 bảng** chính, áp dụng khóa chính, khóa ngoại, ràng buộc CHECK và chỉ mục INDEX tối ưu:

| STT | Tên bảng | Chức năng chính | Ràng buộc & Điểm đặc biệt |
| :---: | :--- | :--- | :--- |
| 1 | `nguoi_dung` | Quản lý tài khoản & vai trò | Mật khẩu hash Argon2id (`VARCHAR(255)`), vai trò `ADMIN` / `NHAN_VIEN`. Không tạo tài khoản Admin mặc định. |
| 2 | `bang_gia` | Bảng giá theo từng loại xe | `loai_xe` PK, `gia_ve >= 0`. Khởi tạo mặc định: XeDap (2.000đ), XeMay (5.000đ), OTo (20.000đ). |
| 3 | `suc_chua` | Tổng số chỗ đỗ quy định | `loai_xe` PK (FK -> `bang_gia`), `tong_cho >= 0`. Mặc định: XeDap (50), XeMay (150), OTo (30). |
| 4 | `xe` | Danh mục thông tin phương tiện | `ma_dinh_danh` UNIQUE (biển số xe máy/ô tô hoặc mã thẻ xe đạp), `bien_so` cho phép NULL với xe đạp; kiểm soát bắt buộc biển số cho `XeMay`/`OTo` tại tầng Nghiệp vụ (Service Layer). |
| 5 | `ve_xe` | Lượt gửi xe vào / ra | Lưu `don_gia_ap_dung` (snapshot giá lúc gửi). Chuẩn hóa 3NF không lưu trùng `ma_dinh_danh` & `loai_xe` (dùng `id_xe`). Cột ảo `id_xe_dang_gui` + `UNIQUE` chống 1 xe có 2 vé `Dang gui` cùng lúc. |
| 6 | `thanh_toan` | Quản lý giao dịch thu tiền | Tách riêng khỏi vé, liên kết `ma_ve` UNIQUE để chống thanh toán 2 lần cho cùng một vé. Lưu nhân viên thu tiền. |
| 7 | `nhat_ky` | Lịch sử hoạt động (Audit log) | Ghi nhận ai làm gì, vào thời gian nào (nhận xe, trả xe, sửa giá...). |

---

## 4. Cấu Trúc Thư Mục Dự Án

```text
QuanLyBaiGiuXe/
│
├── README.md                   # [Tài liệu dự án] Giới thiệu, kiến trúc, hướng dẫn
├── PROGRESS.md                 # [Nhật ký tiến độ] Theo dõi chi tiết từng giai đoạn phát triển
├── AGENTS.md                   # [Quy tắc làm việc] Hướng dẫn bắt buộc dành cho các AI Agent
├── requirements.txt            # Danh sách thư viện Python cần cài đặt
├── .env.example                # File mẫu cấu hình biến môi trường kết nối MySQL
├── .env                        # File cấu hình thực tế trên máy cục bộ (chứa mật khẩu DB)
├── app_desktop.py              # Điểm khởi chạy ứng dụng Desktop Cyberpunk Neon
├── Start_NeonParking.bat       # File khởi chạy 1-click tiện lợi trên Windows
│
├── main.py                     # [Console CLI] Chương trình chạy trên dòng lệnh nguyên bản (giữ nguyên)
│
├── config/                     # Quản lý cấu hình hệ thống & Giao diện
│   ├── __init__.py
│   ├── database.py             # Đọc thông số kết nối MySQL từ biến môi trường
│   └── theme.py                # Bảng màu Cyberpunk Neon chuẩn (Dark mode, màu nhấn)
│
├── security/                   # Module bảo mật & mã hóa
│   ├── __init__.py
│   └── hasher.py               # Băm và xác thực mật khẩu chuẩn Argon2id
│
├── database/                   # Quản lý cơ sở dữ liệu MySQL
│   ├── __init__.py
│   ├── schema.sql              # Kịch bản DDL tạo database neon_parking_db & 7 bảng quan hệ
│   ├── db_connection.py        # Hàm kết nối, context manager hỗ trợ Transaction & Rollback
│   ├── init_db.py              # Script tự động chạy schema.sql tạo database
│   ├── test_connection.py     # Script kiểm tra 7 bảng và quan hệ khóa ngoại
│   └── repositories/           # Tầng truy vấn CSDL (Repository Pattern)
│       ├── __init__.py
│       ├── user_repository.py  # CRUD người dùng, phân quyền, đổi mật khẩu, nhật ký
│       └── vehicle_repository.py # CRUD phương tiện, vé xe, thanh toán Transaction
│
├── models/                     # Các lớp Đối tượng (OOP Core)
│   ├── xe.py                   # Lớp cơ sở Xe (Console OOP)
│   ├── XeDap.py                # Lớp XeDap kế thừa từ Xe
│   ├── XeMay.py                # Lớp XeMay kế thừa từ Xe
│   ├── Oto.py                  # Lớp OTo kế thừa từ Xe
│   ├── ve_xe.py                # Lớp VeXe quản lý thông tin vé (Console)
│   └── nguoi_dung.py           # Thực thể người dùng hệ thống (Admin, Nhân viên)
│
├── services/                   # Tầng Xử lý Nghiệp vụ (Business Logic Layer)
│   ├── quan_ly_bai_xe.py       # Logic nghiệp vụ Console cũ (giữ nguyên)
│   ├── auth_service.py         # Xác thực người dùng, phiên làm việc, phân quyền
│   └── bai_xe_db_service.py    # Nghiệp vụ tiếp nhận xe, xe ra, tính tiền, vé xe MySQL
│
├── assets/                     # Tài nguyên tĩnh & Branding
│   └── branding/               # Bộ nhận diện thương hiệu độc quyền Cyberpunk
│       ├── logo.svg            # Logo vector chất lượng cao (512x512)
│       ├── logo.png            # Logo PNG nền trong suốt (512x512)
│       ├── logo_small.png      # Logo PNG thu nhỏ (64x64)
│       └── app.ico             # Icon ứng dụng Windows (16x16 -> 256x256)
│
├── services/                   # Tầng Nghiệp vụ (Business Logic)
│   ├── auth_service.py         # Xác thực, đăng nhập, đổi mật khẩu, Argon2id
│   ├── bai_xe_db_service.py    # Tiếp nhận, xe ra, transaction bãi xe
│   ├── user_service.py         # Quản lý nhân viên, tạo, sửa, khóa, reset MK
│   ├── settings_service.py     # Cài đặt bảng giá & sức chứa (ràng buộc nghiệp vụ)
│   ├── audit_service.py        # Nhật ký hoạt động nhat_ky, bộ lọc, phân trang
│   ├── report_service.py       # Xuất báo cáo TXT chuẩn tiếng Việt UTF-8
│   └── quan_ly_bai_xe.py       # Nghiệp vụ bãi xe của bản Console cũ (giữ nguyên)
│
├── gui/                        # Tầng Giao diện Đồ họa Desktop (CustomTkinter)
│   ├── __init__.py
│   ├── main_window.py          # Bộ điều khiển trung tâm (Controller & Routing)
│   ├── components/             # Các widget giao diện dùng chung
│   │   ├── __init__.py
│   │   ├── branding.py         # Tiện ích nạp logo CTkImage & cài đặt icon cửa sổ
│   │   ├── cyber_chart.py      # Trực quan hóa Matplotlib Cyberpunk Dark theme
│   │   ├── dialog.py           # Popup modal Cyberpunk (Error, Success, Confirm)
│   │   ├── header.py           # Thanh tiêu đề, đồng hồ số & nút đổi mật khẩu
│   │   ├── sidebar.py          # Thanh điều hướng hiển thị Logo thương hiệu & 9 menu
│   │   └── stat_card.py        # Thẻ KPI phát sáng Cyberpunk
│   └── modules/                # Toàn bộ 9 phân hệ nghiệp vụ kết nối MySQL thật
│       ├── __init__.py
│       ├── auth/               # Phân hệ Xác thực & Thiết lập (LoginView, SetupAdminView)
│       ├── dashboard/          # Phân hệ Dashboard Tổng Quan (KPI, Matplotlib 7 ngày)
│       ├── vehicles/           # Phân hệ Quản Lý Xe (Check-in, Check-out, Danh sách xe)
│       ├── tickets/            # Phân hệ Quản Lý Vé Xe (Tra cứu, Chi tiết, Thanh toán)
│       ├── revenue/            # Phân hệ Quản Lý Doanh Thu (Biểu đồ, Lọc ngày, Lịch sử, Xuất file TXT)
│       ├── statistics/         # Phân hệ Thống Kê (Tỷ lệ lấp đầy, Biểu đồ giờ cao điểm)
│       ├── users/              # Phân hệ Quản Lý Nhân Viên (Admin Only)
│       ├── settings/           # Phân hệ Cài Đặt Bảng Giá & Sức Chứa (Admin Only)
│       ├── reports/            # Phân hệ Xuất Báo Cáo TXT (4 mẫu báo cáo: Xe gửi, Vé, Doanh thu, Lịch sử GD)
│       └── audit/              # Phân hệ Nhật Ký Hoạt Động Hệ Thống (Admin Only)
│
├── storage/                    # Tầng Lưu trữ File
│   └── file_txt.py             # Đọc/ghi dữ liệu JSON cho Console (giữ nguyên)
│
├── data/                       # Thư mục lưu dữ liệu
│   └── du_lieu_bai_xe.txt      # Dữ liệu vé xe ban đầu của bản Console (giữ nguyên)
│
└── docs/                       # Tài liệu dự án & Báo cáo học phần
    └── report/                 # Hồ sơ hoàn chỉnh phục vụ viết báo cáo khoa học theo PDF trường
        ├── REPORT_REQUIREMENTS.md  # Trích xuất quy định chuẩn định dạng PDF (A4, TNR 13, 11 phần)
        ├── PROJECT_ANALYSIS.md     # Phân tích toàn bộ hệ thống đối chiếu code thực tế
        ├── SOURCE_CODE_MAPPING.md  # Bảng ánh xạ 14 kiến thức Python vào các class/hàm thực tế
        ├── DATABASE_DESIGN.md      # Thiết kế chi tiết 7 bảng MySQL, khóa ngoại & ràng buộc
        ├── DIAGRAM_PLAN.md         # Toàn bộ mã Mermaid: DFD cấp 0, phân cấp, flowchart, UML, ERD
        ├── TEST_CASES.md           # Ma trận 22 kịch bản kiểm thử (PASS 20/22, 2 kịch bản phần cứng)
        ├── REPORT_OUTLINE.md       # Đề cương chi tiết từng chương theo bố cục chuẩn PDF
        ├── REFERENCES.md           # 5 dự án/thư viện Python tham khảo & phân tích sâu 1 dự án
        ├── SCREENSHOT_CHECKLIST.md # Danh sách 20 ảnh chụp màn hình thực tế cần chuẩn bị
        └── LESSON_MAPPING.md       # Khung đối chiếu Bài 1 - Bài 8 khi người dùng cung cấp ảnh
```

---

## 5. Hướng Dẫn Thực Thi Schema Trong MySQL Workbench & Terminal

### Cách 1: Thực thi trực tiếp trong MySQL Workbench
1. Khởi động phần mềm **MySQL Workbench**.
2. Chọn kết nối vào MySQL Server của bạn (Local instance).
3. Vào menu **File** -> **Open SQL Script...** (hoặc phím tắt `Ctrl + Shift + O`).
4. Tìm và chọn file: `database/schema.sql` trong thư mục dự án.
5. Nhấn vào biểu tượng **Tia sét** (Execute) để thực thi toàn bộ script.
6. Trong khung **Navigator** bên trái, click chuột phải vào vùng *Schemas* và chọn **Refresh All**. Bạn sẽ thấy schema `neon_parking_db` xuất hiện cùng đủ **7 bảng**.

### Cách 2: Khởi tạo tự động bằng Python Terminal
1. Mở file `.env` và điền mật khẩu root MySQL:
   ```env
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=mat_khau_cua_ban
   DB_NAME=neon_parking_db
   DB_CHARSET=utf8mb4
   ```
2. Chạy lệnh:
   ```powershell
   .\.venv\Scripts\python.exe database/init_db.py
   ```

### Kiểm tra 7 bảng và quan hệ:
Chạy script kiểm tra:
```powershell
.\.venv\Scripts\python.exe database/test_connection.py
```

### Câu lệnh SQL kiểm tra trực tiếp trong MySQL Workbench:
```sql
USE neon_parking_db;

-- 1. Xem danh sách 7 bảng:
SHOW TABLES;

-- 2. Kiểm tra các khóa ngoại:
SELECT 
    TABLE_NAME AS 'Bảng con', 
    COLUMN_NAME AS 'Cột khóa ngoại', 
    REFERENCED_TABLE_NAME AS 'Bảng cha', 
    REFERENCED_COLUMN_NAME AS 'Cột tham chiếu'
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'neon_parking_db' AND REFERENCED_TABLE_NAME IS NOT NULL;
```

---

## 6. Chạy Chương Trình Console Cũ
Bất cứ lúc nào bạn cũng có thể khởi chạy bản Console nguyên bản độc lập:
```powershell
.\.venv\Scripts\python.exe main.py
```
Mọi tính năng nhập xe, trả xe, xuất file TXT của bản Console đều được bảo toàn 100%.

---

## 7. Module Branding – Bộ Nhận Diện Thương Hiệu Light Premium

Ứng dụng **Neon Parking Manager** được trang bị bộ nhận diện thương hiệu thiết kế riêng theo phong cách **Light Premium Automotive Management**, lấy cảm hứng từ các dải khí động học (Aero Blades), vạch đỗ xe thông minh và điểm nhấn mạ vàng Champagne Gold (`#C5A46D`).

### Danh mục tệp xem trước (Preview) tại `assets/branding/light_preview/`:
- `logo_abstract_light.svg`: Logo vector tỉ lệ chuẩn 512x512, tối ưu cho nền sáng.
- `logo_horizontal_light.svg`: Logo dạng ngang kết hợp biểu tượng và tên ứng dụng `NEON PARKING`.
- `logo_abstract_dark.svg`: Phiên bản vector tương thích nền tối.
- `preview_light_512.png`: Bản xem trước kích thước 512x512 trên nền xám nhạt `#F3F6F8`.
- `preview_dark_512.png`: Bản xem trước trên nền tối `#0A0F14`.
- `preview_icon_64.png`: Bản xem trước icon thu nhỏ 64x64 cho thanh điều hướng Sidebar.
- `preview_horizontal_light.png`: Bản xem trước logo ngang 720x180.
- `BRANDING_DESIGN_GUIDE.md`: Bản giải trình chi tiết ý tưởng hình học và triết lý thiết kế.

*(Ghi chú: Bản xem trước đang chờ Người dùng phê duyệt trước khi ghi đè vào logo chính tại `assets/branding/logo.png`)*.

---

## 8. Kiểm Thử Hệ Thống Thực Tế

Toàn bộ các module nghiệp vụ và giao diện đều có các script kiểm thử tự động:

- **Kiểm thử phân quyền, nghiệp vụ, ràng buộc & xuất file TXT**:
  ```powershell
  .\.venv\Scripts\python.exe scripts/test_phase6.py
  ```
- **Kiểm thử độ ổn định chuyển đổi giao diện liên tục 9 module**:
  ```powershell
  .\.venv\Scripts\python.exe scripts/test_gui_switching.py
  ```
- **Kiểm thử kích thước nút bấm popup & Căn giữa cửa sổ DPI-aware**:
  ```powershell
  .\.venv\Scripts\python.exe scripts/test_dialog_and_centering.py
  ```
- **Kiểm thử độ tương phản màu chữ và trạng thái bảng Quản lý xe**:
  ```powershell
  .\.venv\Scripts\python.exe scripts/test_contrast_vehicle_view.py
  ```

---

## 9. Hồ Sơ Bàn Giao Kỹ Thuật (Handoff to ChatGPT)

Toàn bộ tài liệu phân tích nghiệp vụ, thiết kế cơ sở dữ liệu, ca kiểm thử và ma trận bài học theo đúng chuẩn hướng dẫn viết Báo cáo học phần Lập trình Python – Thực hành (`BaoCao_LapTrinhPython_Maubaocao.pdf`) đã được hoàn thiện 100% tại thư mục `docs/report/`:

- `docs/report/HANDOFF_TO_CHATGPT.md`: Bản tóm lược toàn diện dành cho ChatGPT để chuyển đổi sang Microsoft Word.
- `docs/report/REPORT_REQUIREMENTS.md`: Yêu cầu kỹ thuật & phân tích đề tài.
- `docs/report/PROJECT_ANALYSIS.md`: Phân tích kiến trúc 4 tầng & luồng dữ liệu.
- `docs/report/SOURCE_CODE_MAPPING.md`: Bảng đối chiếu class, method với chức năng.
- `docs/report/DATABASE_DESIGN.md`: Thiết kế lược đồ CSDL chuẩn 3NF.
- `docs/report/DIAGRAM_PLAN.md`: Kế hoạch vẽ sơ đồ Use Case, Class Diagram, Flowchart.
- `docs/report/TEST_CASES.md`: Bộ ca kiểm thử thực tế có bằng chứng.
- `docs/report/REPORT_OUTLINE.md`: Đề cương chi tiết theo mẫu chuẩn của DNC.
- `docs/report/REFERENCES.md`: Tài liệu tham khảo theo quy cách học thuật.
- `docs/report/SCREENSHOT_CHECKLIST.md`: Danh mục ảnh chụp màn hình cần chèn.
- `docs/report/LESSON_MAPPING.md`: Ma trận đối chiếu kiến thức Python vận dụng trong đề tài.

