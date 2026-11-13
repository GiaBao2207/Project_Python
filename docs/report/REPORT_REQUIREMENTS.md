# YÊU CẦU VÀ QUY ĐỊNH BÁO CÁO HỌC PHẦN (REPORT_REQUIREMENTS)

> **Học phần**: Lập trình Python – Thực hành  
> **Đơn vị**: Trường Đại học Nam Cần Thơ – Trường Công nghệ số và Trí tuệ nhân tạo  
> **Tài liệu căn cứ**: File chính thức `BaoCao_LapTrinhPython_Maubaocao.pdf` (01/2026)  
> **Đề tài**: Neon Parking Manager – Hệ thống Quản lý Bãi Giữ Xe Thông Minh (Smart Parking Management System)

---

## 1. QUY CÁCH ĐỊNH DẠNG HÌNH THỨC (BẮT BUỘC THEO PDF)

Căn cứ Mục 1 – Trình bày (Trang 2 của PDF mẫu):

| STT | Tiêu chí | Quy định chuẩn theo PDF | Áp dụng cho đồ án Neon Parking Manager |
| :---: | :--- | :--- | :--- |
| 1 | **Khổ giấy** | Khổ giấy **A4** (kích thước tiêu chuẩn $210 \times 297\text{ mm}$). | Khổ A4 đứng (Portrait). |
| 2 | **Căn lề (Margins)** | • Lề trên (Top): **2,0 cm**<br>• Lề dưới (Bottom): **2,0 cm**<br>• Lề trái (Left): **3,5 cm** (chừa gáy đóng tập)<br>• Lề phải (Right): **2,0 cm** | Thiết lập Page Setup chuẩn trong Microsoft Word: Top 2cm, Bottom 2cm, Left 3.5cm, Right 2cm. |
| 3 | **Bảng mã & Font** | Bảng mã **Unicode**; Font chữ **Times New Roman** (hoặc Time Roman theo PDF). | Sử dụng thống nhất bộ gõ tiếng Việt Unicode dựng sẵn và font Times New Roman toàn văn bản. |
| 4 | **Cỡ chữ (Font Size)** | Cỡ chữ tiêu chuẩn: **13 pt**. | Nội dung văn bản thường (Normal text): cỡ 13 pt.<br>Tiêu đề chương (Heading 1): cỡ 16 pt in hoa đậm.<br>Tiêu đề mục (Heading 2): cỡ 14 pt in đậm.<br>Tiêu đề tiểu mục (Heading 3): cỡ 13 pt in đậm/nghiêng. |
| 5 | **Giãn dòng (Line Spacing)** | Chế độ giãn dòng: **1,2 lines**. | Paragraph Line Spacing: Multiple 1.2; Spacing Before: 3pt, Spacing After: 3pt. |
| 6 | **Độ dày báo cáo** | **Tối đa 60 trang** (không tính phần phụ lục). | Giới hạn dung lượng toàn văn báo cáo từ 35 – 55 trang, đảm bảo cô đọng, súc tích, đầy đủ minh chứng. Toàn bộ mã nguồn chi tiết đưa vào Phụ lục. |

---

## 2. BỐ CỤC NỘI DUNG BẮT BUỘC (THEO PDF MẪU)

Báo cáo phải tuân thủ nghiêm ngặt thứ tự 11 phần sau đây, tuyệt đối không tự ý đảo lộn hay cắt xén:

```text
[BỐ CỤC TỔNG THỂ BÁO CÁO THEO PDF]
  ├── 1. Trang bìa (Chuẩn mẫu Trường ĐH Nam Cần Thơ)
  ├── 2. Mục lục
  ├── 3. Danh mục đồ thị, biểu bảng và hình ảnh
  ├── 4. Phần Giới thiệu:
  │     ├── Đặt vấn đề
  │     ├── Những nghiên cứu liên quan (≥ 5 ứng dụng/thư viện, phân tích sâu 1 ứng dụng)
  │     ├── Mục tiêu
  │     ├── Đối tượng và phạm vi nghiên cứu
  │     └── Sơ đồ DFD cấp 0
  ├── 5. Chương 1 – Đặc tả yêu cầu
  ├── 6. Chương 2 – Thiết kế giải pháp
  ├── 7. Chương 3 – Cài đặt giải pháp
  ├── 8. Chương 4 – Đánh giá kiểm thử
  ├── 9. Phần Kết luận
  ├── 10. Tài liệu tham khảo
  └── 11. Phụ lục (Hướng dẫn cài đặt và sử dụng chương trình)
```

---

## 3. CHI TIẾT TỪNG PHẦN THEO YÊU CẦU PDF

### 3.1. Trang bìa (Cover Page)
- **Tên trường & khoa**:
  - Dòng 1: TRƯỜNG ĐẠI HỌC NAM CẦN THƠ
  - Dòng 2: TRƯỜNG CÔNG NGHỆ SỐ VÀ TRÍ TUỆ NHÂN TẠO
- **Loại báo cáo**: BÁO CÁO HỌC PHẦN LẬP TRÌNH PYTHON – THỰC HÀNH
- **Đề tài**:
  - Tên tiếng Việt: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH – NEON PARKING MANAGER
  - Tên tiếng Anh: SMART PARKING MANAGEMENT SYSTEM – NEON PARKING MANAGER
- **Sinh viên thực hiện**: Họ và tên – MSSV – LỚP
- **Địa điểm & Thời gian**: Cần Thơ, 01/2026 (hoặc theo kỳ thi thực tế)

### 3.2. Mục lục & Danh mục biểu bảng, đồ thị, hình ảnh
- Tự động tạo bằng chức năng Table of Contents và List of Figures / List of Tables trong Word.
- Đánh số hình ảnh và bảng biểu theo số thứ tự của chương (Ví dụ: Hình 2.1, Bảng 3.2, Đồ thị 4.1).

### 3.3. Phần Giới thiệu
- **Đặt vấn đề**:
  - Mô tả bài toán thực tế quản lý phương tiện tại các bãi giữ xe (tình trạng ghi vé giấy dễ rách nát, nhầm lẫn tiền bạc, khó kiểm soát số lượng xe tồn, gian lận doanh thu, quá tải giờ cao điểm).
  - Lý do tại sao cần xây dựng phần mềm quản lý bằng mã nguồn Python.
- **Những nghiên cứu liên quan**:
  - Liệt kê ít nhất **5 ứng dụng hoặc thư viện Python** tương tự hiện có trên GitHub hoặc Internet đã tham khảo.
  - Phân tích kỹ **1 ứng dụng chính** để học tập kiến trúc và tư duy logic xử lý.
- **Mục tiêu đề tài**:
  - Giải quyết các bài toán về lưu trữ dữ liệu an toàn, tính toán phí giữ xe tự động, kiểm soát sức chứa theo thời gian thực và tự động hóa thống kê báo cáo.
- **Đối tượng và phạm vi nghiên cứu**:
  - Người dùng cuối (End-user): Nhân viên bảo vệ/thu ngân trực ca và Quản trị viên (Admin).
  - Phương thức vận hành: Phiên bản dòng lệnh Console CLI kết hợp ứng dụng đồ họa Desktop hiện đại (CustomTkinter).
- **Sơ đồ DFD cấp 0 (Data Flow Diagram Level 0)**:
  - Thể hiện luồng dữ liệu hai chiều: Người dùng $\leftrightarrow$ Phần mềm Python $\leftrightarrow$ Cơ sở dữ liệu MySQL (kho dữ liệu chính) và File TXT (xuất báo cáo định kỳ).

### 3.4. Chương 1 – Đặc tả yêu cầu
- Mô tả chi tiết các chức năng cốt lõi của phần mềm:
  1. Đăng nhập, phân quyền vai trò (Admin / Nhân viên) và bảo mật Argon2id.
  2. Tiếp nhận xe vào bãi (Check-in), cấp mã vé tự động, hỗ trợ Xe máy, Ô tô, Xe đạp.
  3. Kiểm soát sức chứa thời gian thực, cảnh báo bãi đầy.
  4. Quản lý danh sách xe đang gửi, tìm kiếm thông minh, lọc trạng thái.
  5. Xử lý xe ra (Check-out), tính thời gian đỗ, áp đơn giá snapshot, thanh toán Tiền mặt / Chuyển khoản qua Transaction an toàn.
  6. Quản lý doanh thu, thống kê lượt xe theo ngày, theo loại xe, phân tích giờ cao điểm.
  7. Quản lý nhân viên trực, khóa/mở khóa tài khoản, đổi mật khẩu.
  8. Cài đặt bảng giá vé và tổng sức chứa.
  9. Xuất báo cáo tổng hợp ra file văn bản TXT định dạng chuẩn tiếng Việt UTF-8.
  10. Ghi nhận nhật ký kiểm toán (Audit log) mọi thao tác hệ thống.

### 3.5. Chương 2 – Thiết kế giải pháp
- **Thiết kế kiến trúc**:
  - Sơ đồ phân cấp các hàm / phân cấp chức năng (Function Decomposition Diagram).
  - Kiến trúc phân tầng 4 lớp: GUI (CustomTkinter) $\rightarrow$ Service (Logic & Security) $\rightarrow$ Repository (Data Access) $\rightarrow$ Database (MySQL Server).
- **Giải thuật & Lưu đồ thuật toán (Flowcharts)**:
  - Lưu đồ thuật toán tiếp nhận phương tiện vào bãi (kiểm tra sức chứa $\rightarrow$ sinh mã vé $\rightarrow$ lưu snapshot giá).
  - Lưu đồ thuật toán xe ra & xử lý thanh toán (tra cứu vé $\rightarrow$ kiểm tra trạng thái $\rightarrow$ tính tiền $\rightarrow$ thực thi MySQL Transaction).
  - Lưu đồ kiểm soát sức chứa đồng thời.
- **Thiết kế cấu trúc dữ liệu**:
  - Mô tả các lớp đối tượng OOP (`Xe`, `XeMay`, `OTo`, `XeDap`, `VeXe`, `NguoiDung`).
  - Cấu trúc Dictionary, List, Tuple trong xử lý nghiệp vụ.
  - Thiết kế lược đồ 7 bảng trong cơ sở dữ liệu MySQL (`neon_parking_db`) và định dạng cấu trúc file TXT xuất báo cáo.

### 3.6. Chương 3 – Cài đặt giải pháp
- **Môi trường phát triển**:
  - Hệ điều hành: Windows 11.
  - Ngôn ngữ: Python 3.10+ (thực tế chạy Python 3.14).
  - IDE: JetBrains PyCharm / VS Code.
  - Hệ quản trị CSDL: MySQL Server (kết nối qua `mysql-connector-python`).
  - Thư viện giao diện: `customtkinter`, `Pillow`, `matplotlib`.
  - Thư viện bảo mật & cấu hình: `argon2-cffi`, `python-dotenv`.
- **Hiện thực mã nguồn**:
  - Trích xuất các đoạn mã nguồn (Source code) trọng tâm, có chú thích chi tiết.
  - **Minh chứng vận dụng kiến thức từ Bài 1 đến Bài 8**: Đối chiếu từng kiến thức học phần vào các dòng code thực tế trong dự án (Biến, Kiểu dữ liệu, If/Else, Vòng lặp For/While, Hàm, List/Dict/Tuple, Module/Package, Class/Object, Constructor, Encapsulation, Inheritance, Polymorphism, Try/Except, Đọc/Ghi File, Giao diện Tkinter).

### 3.7. Chương 4 – Đánh giá kiểm thử
- **Mục tiêu kiểm thử**: Đảm bảo hệ thống vận hành đúng logic, xử lý ngoại lệ an toàn, bảo vệ dữ liệu khi có sự cố.
- **Mô hình kiểm thử**: Kiểm thử hộp đen (Black-box Testing) kết hợp Kịch bản kiểm thử tự động (Automated Test Scripts).
- **Bảng kịch bản kiểm thử (Test Cases)**:
  - Kiểm thử nhập liệu đúng / sai (bỏ trống ô bắt buộc, nhập biển số sai quy cách, nhập số âm...).
  - Kiểm thử tính đúng đắn của logic (tính tiền, áp dụng snapshot giá, ràng buộc chống Admin tự khóa, ràng buộc không giảm sức chứa dưới số xe đang gửi).
  - Kiểm thử lưu trữ & tính toàn vẹn (thực thi Transaction `commit`/`rollback`, kiểm tra dữ liệu sau khi khởi động lại ứng dụng, xuất file TXT UTF-8).
  - Đánh dấu trạng thái trung thực: PASS, FAIL hoặc CHƯA KIỂM THỬ.

### 3.8. Phần Kết luận
- **Kết quả đạt được**:
  - Tổng kết những kỹ năng Python đã làm chủ (Lập trình hướng đối tượng OOP nâng cao, xử lý Transaction cơ sở dữ liệu quan hệ, băm mật khẩu Argon2id, xây dựng giao diện đồ họa CustomTkinter chuẩn mực, trực quan hóa dữ liệu Matplotlib, quản lý file).
- **Hướng phát triển tương lai**:
  - Tích hợp nhận diện biển số xe tự động qua camera (Computer Vision / AI / OCR).
  - Tích hợp cổng thanh toán trực tuyến qua mã QR VietQR / MoMo tự động xác nhận qua Webhook.
  - Triển khai ứng dụng di động cho chủ xe kiểm tra chỗ trống từ xa.

### 3.9. Tài liệu tham khảo
- Danh mục tài liệu tham khảo chính thống, có nguồn gốc kiểm chứng được (Python Documentation, CustomTkinter Docs, MySQL Documentation, Argon2-cffi Docs, các kho mã nguồn mở GitHub tham khảo).

### 3.10. Phụ lục (Hướng dẫn cài đặt và sử dụng)
- Hướng dẫn cài đặt Python, môi trường ảo `venv`, cài đặt các thư viện trong `requirements.txt`.
- Hướng dẫn cấu hình file `.env` kết nối MySQL.
- Hướng dẫn thực thi `schema.sql` tạo CSDL.
- Hướng dẫn chạy chương trình Console (`main.py`) và ứng dụng Desktop (`app_desktop.py` hoặc `Start_NeonParking.bat`).

---

## 4. BẢNG PHÂN ĐỊNH: YÊU CẦU BẮT BUỘC VS ĐIỂM SÁNG TẠO NÂNG CAO

| Hạng mục | Yêu cầu chuẩn theo PDF của trường | Điểm sáng tạo & nâng cấp vượt trội của Dự án |
| :--- | :--- | :--- |
| **Giao diện** | Console hoặc Tkinter cơ bản | Nâng cấp lên **CustomTkinter Light Premium Automotive**, giao diện đồ họa cao cấp, thẩm mỹ chuẩn công nghiệp. Vẫn giữ nguyên 100% bản Console CLI nguyên bản. |
| **Lưu trữ dữ liệu** | File phẳng CSV / TXT | Dùng **MySQL Server** chuẩn hóa 7 bảng, hỗ trợ **ACID Transaction** bảo toàn toàn vẹn dữ liệu; đồng thời giữ nguyên chức năng xuất báo cáo định dạng **TXT** chuẩn UTF-8. |
| **Bảo mật** | Không yêu cầu hoặc lưu text thuần | Ứng dụng tiêu chuẩn mã hóa **Argon2id** (thuật toán số 1 thế giới chống bẻ khóa GPU/ASIC), phân quyền chặt chẽ Admin / Nhân viên tại tầng Service. |
| **Trực quan hóa** | Bảng biểu đơn giản | Tích hợp **Matplotlib** vẽ biểu đồ cột 7 ngày, biểu đồ phân tích 24h giờ cao điểm và xu hướng doanh thu trực tiếp trên GUI. |
| **Kiến trúc phần mềm** | Script đơn lẻ hoặc OOP cơ bản | Áp dụng kiến trúc 4 tầng chuẩn doanh nghiệp: **GUI $\rightarrow$ Service $\rightarrow$ Repository $\rightarrow$ MySQL Database**, triệt để tuân thủ tính đóng gói, kế thừa và đa hình. |
