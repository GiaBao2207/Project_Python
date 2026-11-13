# TÀI LIỆU HƯỚNG DẪN BÀN GIAO CHO CHATGPT (HANDOFF TO CHATGPT)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH – NEON PARKING MANAGER
**Học phần**: Lập Trình Python – Thực Hành  
**Đơn vị đào tạo**: Khoa Công Nghệ Thông Tin – Trường Đại Học Nam Cần Thơ (DNC)  
**Ngày cập nhật**: 26/10/2026  
**Trạng thái phát triển**: Hoàn thành toàn diện 7 giai đoạn, vượt qua 100% các ca kiểm thử tự động  

---

## 1. TỔNG QUAN TRẠNG THÁI THỰC TẾ CỦA DỰ ÁN

Dự án **Neon Parking Manager** là một hệ thống phần mềm quản lý bãi giữ xe thông minh đa phương tiện (Xe đạp, Xe máy, Ô tô), được kiến trúc phân tầng chuyên nghiệp:
- **Tầng Giao diện (Presentation Layer)**: Xây dựng bằng `CustomTkinter` với phong cách **Light Premium Automotive Management** sang trọng, hiện đại, hỗ trợ DPI Scaling tự động trên Windows, bố cục căn giữa hoàn hảo.
- **Tầng Nghiệp vụ (Business Service Layer)**: Phân quyền vai trò chặt chẽ (Admin / Nhân viên), xử lý logic kế toán, kiểm soát sức chứa thời gian thực, băm mật khẩu chuẩn quân sự bằng `Argon2id`.
- **Tầng Dữ liệu (Repository & Persistence Layer)**: Sử dụng hệ quản trị cơ sở dữ liệu quan hệ `MySQL Server 9.7.1`, bảo toàn tính toàn vẹn dữ liệu bằng **MySQL Database Transaction** (`commit`/`rollback`).
- **Khả năng tương thích ngược (Legacy CLI Compatibility)**: Bảo toàn 100% mã nguồn Console dòng lệnh ban đầu (`main.py`) và tệp dữ liệu lưu trữ văn bản truyền thống `data/du_lieu_bai_xe.txt`.

### Thông số kỹ thuật hiện tại:
- **Ngôn ngữ**: Python 3.10+ (Thực thi trên môi trường ảo `.venv`).
- **Thư viện chính**: `customtkinter`, `mysql-connector-python`, `argon2-cffi`, `python-dotenv`, `pillow`, `matplotlib`.
- **Cơ sở dữ liệu**: MySQL Server (`neon_parking_db`, 7 bảng chuẩn hóa 3NF, 8 ràng buộc khóa ngoại).
- **Hệ thống khởi chạy**: Tệp Batch `Start_NeonParking.bat` thuần ASCII, kiến trúc pure-goto an toàn tuyệt đối trên Windows 10/11.

---

## 2. DANH MỤC CÁC TỆP NGUỒN QUAN TRỌNG TRONG SOURCE CODE

```text
QuanLyBaiGiuXe/
├── app_desktop.py                 # Điểm khởi chạy Desktop GUI chính, căn giữa DPI-aware
├── main.py                        # Chương trình Console OOP dòng lệnh nguyên bản
├── Start_NeonParking.bat          # File launcher Windows an toàn tuyệt đối
├── config/
│   ├── settings.py               # Nạp cấu hình từ biến môi trường .env (Database config)
│   └── theme.py                  # Hệ thống Design Tokens: Light Premium Automotive
├── database/
│   ├── connection.py             # Quản lý kết nối MySQL & Transaction Context Manager
│   └── repositories/             # Các Repository thao tác SQL thuần chuẩn hóa
│       ├── xe_repository.py      # CRUD phương tiện giao thông
│       ├── ve_xe_repository.py   # CRUD vé xe và trạng thái gửi
│       ├── giao_dich_repository.py # Ghi nhận giao dịch thanh toán tài chính
│       ├── user_repository.py    # Quản lý tài khoản nhân viên & quản trị
│       ├── settings_repository.py# Bảng giá dịch vụ & Sức chứa bãi xe
│       └── audit_repository.py   # Ghi nhận nhật ký hệ thống (Audit Trail)
├── models/                       # Mô hình hướng đối tượng OOP (Kế thừa & Đa hình)
│   ├── xe.py                     # Lớp cha trừu tượng Xe
│   ├── xe_dap.py                 # Lớp con XeDap
│   ├── xe_may.py                 # Lớp con XeMay
│   ├── o_to.py                   # Lớp con OTo
│   ├── ve_xe.py                  # Thực thể Vé xe
│   └── nguoi_dung.py             # Thực thể Người dùng & Phân quyền vai trò
├── services/                     # Tầng nghiệp vụ xử lý logic và kiểm tra quyền hạn
│   ├── auth_service.py           # Xác thực Argon2id, quản lý phiên làm việc Session
│   ├── bai_xe_db_service.py      # Nghiệp vụ vào bãi, tính tiền, ra bãi, sức chứa
│   ├── user_service.py           # Quản lý nhân viên, chống tự khóa Admin
│   ├── settings_service.py       # Thay đổi bảng giá (snapshot) & sức chứa
│   ├── report_service.py         # Trích xuất báo cáo TXT chuẩn tiếng Việt UTF-8
│   └── audit_service.py          # Ghi nhận và phân trang nhật ký hoạt động
├── gui/
│   ├── main_window.py            # Main Controller điều phối Routing và Master Shell
│   ├── components/               # Các Widget UI tái sử dụng cao cấp
│   │   ├── dialog.py             # CyberDialog 2 lớp, nút cao 44px, rộng >=135px
│   │   ├── segmented_control.py  # Nút bấm tùy chọn đa trạng thái tương phản cao
│   │   ├── stat_card.py          # Thẻ KPI hiển thị số liệu nổi bật
│   │   ├── cyber_chart.py        # Biểu đồ Matplotlib Light Theme
│   │   ├── header.py             # Thanh tiêu đề, thông tin phiên và nút Đổi mật khẩu
│   │   ├── sidebar.py            # Menu điều hướng 9 module nghiệp vụ
│   │   └── branding.py           # Quản lý hiển thị Logo Vector và Icon cửa sổ
│   ├── utils/
│   │   └── window_helper.py      # Tiện ích center_window căn giữa DPI-Aware
│   └── modules/                  # 9 Phân hệ màn hình chức năng chính
│       ├── dashboard/            # Tổng quan: 4 KPI, phân bố xe, chart 7 ngày
│       ├── vehicles/             # Quản lý tiếp nhận xe vào bãi & danh sách xe
│       ├── tickets/              # Tra cứu vé, chi tiết vé & thanh toán vé
│       ├── revenue/              # Doanh thu chi tiết, lọc ngày, dòng tiền (Admin)
│       ├── statistics/           # Tỷ lệ lấp đầy, giờ cao điểm 24h, cơ cấu xe
│       ├── users/                # Quản lý nhân viên, thêm, sửa, khóa, reset pass (Admin)
│       ├── settings/             # Cấu hình bảng giá và sức chứa (Admin)
│       ├── reports/              # Xuất báo cáo TXT (Xe đang gửi, Lịch sử vé, Doanh thu)
│       └── audit/                # Nhật ký hoạt động, lọc sự kiện & phân trang (Admin)
└── docs/report/                  # 10 tệp tài liệu kỹ thuật chuẩn bị viết báo cáo
```

---

## 3. TỔNG HỢP KIẾN THỨC PYTHON VÀ OOP TƯƠNG ỨNG

Bảng đối chiếu phục vụ viết **Chương 2 (Cơ sở lý thuyết)** và **Chương 3 (Xây dựng chương trình)** trong Báo cáo thực hành:

| STT | Khái niệm Kỹ thuật Python | Vị trí áp dụng cụ thể trong Source Code | Ý nghĩa trong báo cáo |
| :---: | :--- | :--- | :--- |
| **1** | **Kế thừa (Inheritance)** | `models/xe.py` ➔ `models/xe_may.py`, `models/o_to.py`, `models/xe_dap.py` | Lớp cha `Xe` định nghĩa thuộc tính chung; các lớp con mở rộng thuộc tính riêng. |
| **2** | **Đa hình (Polymorphism)** | `tinh_tien(so_gio)` được cài đặt ghi đè (`override`) khác nhau ở từng loại xe | Tính tiền linh hoạt dựa theo đặc tính từng phương tiện. |
| **3** | **Đóng gói (Encapsulation)** | Thuộc tính có tiền tố `_`, truy cập qua `@property` trong các class `models/` | Bảo vệ tính toàn vẹn dữ liệu của thực thể. |
| **4** | **Xử lý Ngoại lệ (Exception Handling)**| Khối `try...except...finally` tại `database/connection.py`, `services/`, `gui/` | Đảm bảo phần mềm không bị crash đột ngột khi gặp sự cố mạng hoặc nhập sai. |
| **5** | **Quản lý Ngữ cảnh (Context Manager)** | `with get_db_cursor(commit=True) as cursor:` trong `database/connection.py` | Tự động hóa `commit` khi thành công và `rollback` khi phát sinh lỗi giao dịch. |
| **6** | **Xử lý Chuỗi & Ngày tháng** | Thư viện chuẩn `datetime`, `re` trong `services/bai_xe_db_service.py` | Tính toán chính xác thời gian đỗ xe, định dạng tiền tệ `{:,.0f} VNĐ`. |
| **7** | **Đọc/Ghi Tệp Văn bản (File I/O)** | `storage/file_txt.py` và `services/report_service.py` | Đọc/ghi UTF-8 lưu trữ danh sách xe và xuất báo cáo nghiệp vụ. |
| **8** | **Bảo mật & Mã hóa Mật khẩu** | Thư viện `argon2-cffi` trong `services/auth_service.py` | Băm mật khẩu người dùng theo tiêu chuẩn an ninh hiện đại nhất. |
| **9** | **Lập trình Giao diện Đồ họa (GUI)** | Thư viện `customtkinter` trong `gui/` | Xây dựng giao diện Desktop trực quan, đa luồng sự kiện (`event-driven`). |
| **10**| **Trực quan hóa Dữ liệu (Visualization)**| Thư viện `matplotlib` nhúng trong Tkinter (`FigureCanvasTkAgg`) | Biểu diễn biểu đồ doanh thu, cơ cấu xe, giờ cao điểm 24h. |

---

## 4. DỮ LIỆU KIỂM THỬ THỰC TẾ ĐÃ ĐƯỢC XÁC MINH (VERIFIED TEST DATA)

ChatGPT có thể sử dụng trực tiếp các số liệu thực tế này để đưa vào bảng kết quả kiểm thử trong báo cáo:

1. **Bộ nhận diện Branding**: Tạo đầy đủ 4 file vector & raster (`logo.svg`, `logo.png` 512x512, `logo_small.png` 64x64, `app.ico` 7 kích thước).
2. **Kiểm thử phân quyền**:
   - Tài khoản Nhân viên thử truy cập màn hình Doanh thu, Cài đặt, Nhân viên, Nhật ký ➔ Bị tầng Service từ chối và ném `PermissionError`.
   - Admin không thể tự khóa tài khoản của chính mình (chặn thao tác tự cô lập quyền quản trị).
3. **Kiểm thử ràng buộc kế toán & sức chứa**:
   - Cập nhật giá vé số âm (-5000) ➔ Bị chặn: *"Đơn giá vé gửi xe không được là số âm!"*.
   - Giảm sức chứa XeMay xuống 0 chỗ khi đang có xe gửi ➔ Bị chặn: *"Không thể giảm sức chứa XeMay xuống 0 chỗ! Hiện tại đang có 1 xe đang gửi trong bãi."*.
4. **Kiểm thử Dialog & Căn giữa màn hình (`scripts/test_dialog_and_centering.py`)**:
   - Màn hình kiểm thử: `1536x864` (DPI Scaling 125%).
   - Cửa sổ chính được căn giữa tại `1474x778+31+42` (Độ lệch tâm <= 13px, an toàn không tràn taskbar).
   - Nút popup CyberDialog: Chiều cao đạt **44px** (yêu cầu >= 42px), Chiều rộng **135px** (yêu cầu >= 120px), Bo góc **8px**, Font chữ `Segoe UI 13 Bold`.
   - Căn giữa Popup so với Cửa sổ cha: Tâm popup trùng khớp tâm cửa sổ cha (Độ lệch X = 8px).
5. **Kiểm thử Điều hướng Chuyển đổi 9 Module (`scripts/test_gui_switching.py`)**:
   - Chạy vòng lặp tự động 2 lượt qua tất cả 9 module (`dashboard`, `vehicles`, `tickets`, `revenue`, `statistics`, `users`, `settings`, `reports`, `audit`).
   - Kết quả: **18/18 lượt nạp view thành công 100%**, không có lỗi bộ nhớ hay rò rỉ widget.
6. **Kiểm thử Khởi chạy Batch Windows (`Start_NeonParking.bat`)**:
   - Kiểm tra thành công trên Windows 10/11, kiểm tra an toàn thư viện Python, khởi động không giật lag.

---

## 5. HƯỚNG DẪN DÀNH CHO BẠN: TẠO TỆP ZIP GỬI CHO CHATGPT

Để nén mã nguồn gửi cho ChatGPT mà **không làm lộ thông tin nhạy cảm** và **giữ dung lượng tệp nhỏ gọn**:

### Danh sách các thư mục & tệp CẦN ĐƯA VÀO ZIP:
- [x] Thư mục `config/`
- [x] Thư mục `database/` (bao gồm `database/schema.sql`)
- [x] Thư mục `models/`
- [x] Thư mục `services/`
- [x] Thư mục `gui/`
- [x] Thư mục `storage/`
- [x] Thư mục `assets/` (chứa logo và icon)
- [x] Thư mục `docs/report/` (chứa toàn bộ 10 file tài liệu kỹ thuật + file này)
- [x] Thư mục `scripts/` (chứa các script test tự động)
- [x] Tệp `app_desktop.py`
- [x] Tệp `main.py`
- [x] Tệp `Start_NeonParking.bat`
- [x] Tệp `requirements.txt`
- [x] Tệp `README.md`, `PROGRESS.md`, `AGENTS.md`
- [x] Tệp `.env.example` (Mẫu cấu hình an toàn không có mật khẩu thực tế)

### Danh sách các thư mục & tệp TUYỆT ĐỐI LOẠI TRỪ (KHÔNG NÉN):
- ❌ **`.env`** (Chứa mật khẩu MySQL thật của máy bạn ➔ TUYỆT ĐỐI KHÔNG GỬI).
- ❌ **`.venv/`** (Môi trường ảo Python nặng hàng trăm MB ➔ Không gửi).
- ❌ **`__pycache__/`** và `*.pyc` (Tệp biên dịch tạm thời).
- ❌ **`.git/`** và `.idea/` (Cấu hình IDE).

---

## 6. LỜI NHẮC LỆNH (PROMPT) GỢI Ý ĐỂ BẠN GỬI CHO CHATGPT

Khi bạn gửi tệp ZIP hoặc các tệp trong thư mục `docs/report/` cho ChatGPT, hãy đính kèm prompt sau:

> *"Chào ChatGPT, tôi gửi cho bạn bộ hồ sơ kỹ thuật hoàn chỉnh của đề tài học phần 'Lập trình Python – Thực hành' có tên: 'Neon Parking Manager – Hệ thống quản lý bãi giữ xe thông minh'.*  
> *Đề tài được phát triển bằng Python OOP, CustomTkinter (Light Premium Theme) và MySQL Server 9.7.1 theo mô hình phân tầng chuẩn mực.*  
> *Trong tệp đính kèm có file `docs/report/HANDOFF_TO_CHATGPT.md` tóm tắt toàn bộ source code, cùng 10 file tài liệu chi tiết từ `REPORT_REQUIREMENTS.md` đến `LESSON_MAPPING.md`.*  
> *Hãy đóng vai trò là Chuyên gia Lập trình Python kiêm Giảng viên CNTT, dựa vào tài liệu mẫu `BaoCao_LapTrinhPython_Maubaocao.pdf` của Trường Đại học Nam Cần Thơ để viết một bài Báo cáo học phần hoàn chỉnh (gồm đầy đủ Mở đầu, Chương 1, Chương 2, Chương 3, Chương 4, Kết luận, Tài liệu tham khảo), định dạng sẵn sàng để xuất ra Microsoft Word chuẩn mực nhất."*
