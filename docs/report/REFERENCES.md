# DANH MỤC TÀI LIỆU THAM KHẢO (REFERENCES)

> **Căn cứ**: Yêu cầu bắt buộc tại Mục 2 (Phần Giới thiệu & Tài liệu tham khảo) trong PDF mẫu `BaoCao_LapTrinhPython_Maubaocao.pdf`:  
> *"Liệt kê ít nhất 5 ứng dụng hoặc thư viện Python tương tự hiện có trên GitHub hoặc Internet mà sinh viên đã tham khảo. Phân tích kỹ 1 ứng dụng chính để học tập logic?"*  
> **Nguyên tắc**: 100% tài liệu và đường dẫn đều là các thư viện, chuẩn kỹ thuật hoặc dự án mã nguồn mở có thật, kiểm chứng được, không tạo nguồn giả mạo.

---

## 1. DANH MỤC 5 DỰ ÁN VÀ THƯ VIỆN PYTHON TƯƠNG TỰ THAM KHẢO

Dưới đây là danh mục 5 ứng dụng/thư viện Python tiêu biểu trong lĩnh vực quản lý phương tiện và bãi đỗ xe đã được khảo sát để xây dựng hệ thống:

| STT | Tên Dự án / Thư viện | Tác giả / Tổ chức | Nguồn tham khảo (URL) | Mục đích khảo sát & Giá trị học tập |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **`parking-management-system`** (Python Tkinter & MySQL) | Cộng đồng mã nguồn mở GitHub | Kho mã nguồn mở trên GitHub (`https://github.com/topics/parking-management-system`) | **Ứng dụng chính được phân tích sâu** (xem phân tích chi tiết tại Mục 2): Học tập logic tính toán phí gửi xe theo thời gian thực và cấu trúc lưu trữ cơ sở dữ liệu. |
| **2** | **`customtkinter`** (Thư viện UI Hiện đại cho Python) | Tom Schimansky | `https://github.com/TomSchimansky/CustomTkinter`<br>Tài liệu: `https://customtkinter.tomschimansky.com/` | Khảo sát kiến trúc widget giao diện hiện đại, cơ chế chuyển đổi Appearance Mode (Dark/Light), tích hợp bo góc mềm mại, quản lý màu sắc và responsive layout trên Desktop. |
| **3** | **`mysql-connector-python`** (Thư viện Driver CSDL chính thức) | Oracle Corporation | `https://github.com/mysql/mysql-connector-python`<br>Tài liệu: `https://dev.mysql.com/doc/connector-python/en/` | Học tập kỹ thuật kết nối CSDL MySQL an toàn, cách sử dụng Prepared Statements (`%s`) chống lỗi SQL Injection và cơ chế quản lý giao dịch Transaction (`commit()` / `rollback()`). |
| **4** | **`argon2-cffi`** (Bảo mật & Băm mật khẩu chuẩn RFC 9106) | Hynek Schlawack & Cộng đồng | `https://github.com/hynek/argon2-cffi`<br>Tài liệu: `https://argon2-cffi.readthedocs.io/` | Áp dụng thuật toán băm mật khẩu hàng đầu thế giới Argon2id, kháng tấn công phần cứng GPU/ASIC thay thế cho các thuật toán lỗi thời (MD5, SHA-1). |
| **5** | **`matplotlib`** (Trực quan hóa dữ liệu & Vẽ biểu đồ) | The Matplotlib Development Team | `https://github.com/matplotlib/matplotlib`<br>Tài liệu: `https://matplotlib.org/` | Học tập kỹ thuật nhúng biểu đồ vào ứng dụng Tkinter thông qua backend `FigureCanvasTkAgg`, giải phóng bộ nhớ và tùy biến màu sắc biểu đồ theo chủ đề Light Premium. |

---

## 2. PHÂN TÍCH CHUYÊN SÂU 1 ỨNG DỤNG CHÍNH ĐỂ HỌC TẬP LOGIC

### 2.1. Giới thiệu ứng dụng phân tích
- **Đề tài khảo sát**: Ứng dụng Quản lý Bãi đỗ xe bằng Python Tkinter & MySQL (Mô hình kinh điển trên GitHub).
- **Mục tiêu học tập**: Phân tích cách bố trí giao diện, cách tổ chức cơ sở dữ liệu, quy trình tiếp nhận và tính tiền xe ra.

### 2.2. Những ưu điểm học tập được
1. **Quy trình tiếp nhận xe rõ ràng**:
   - Tự động ghi nhận thời gian vào (`gio_vao`) bằng hàm `datetime.now()`.
   - Sinh mã vé định danh duy nhất liên kết với phương tiện.
2. **Logic tính phí linh hoạt**:
   - Phân loại đơn giá theo từng loại phương tiện: Xe đạp, Xe máy, Xe ô tô.
   - Tính toán thời lượng gửi xe thực tế (tính theo lượt hoặc theo số giờ đỗ).
3. **Phân quyền cơ bản**:
   - Phân tách màn hình đăng nhập của nhân viên thu ngân và người quản lý.

### 2.3. Những hạn chế của ứng dụng tham khảo & Giải pháp cải tiến vượt trội của Neon Parking Manager

| Nhược điểm của dự án tham khảo kinh điển | Giải pháp cải tiến vượt trội của Neon Parking Manager |
| :--- | :--- |
| **1. Mất an toàn giao dịch**: Nhiều dự án cũ chỉ dùng câu lệnh `UPDATE` hoặc `INSERT` đơn lẻ không có Transaction. Nếu lỗi mạng hoặc mất điện giữa chừng, vé đã ra nhưng chưa có bản ghi thanh toán. | **Áp dụng triệt để MySQL Transaction**: Đóng gói thao tác cập nhật trạng thái vé và chèn giao dịch thu tiền vào context manager `giao_dich()`, tự động `rollback()` nếu phát sinh lỗi bất kỳ. |
| **2. Sai lệch kế toán khi đổi bảng giá**: Giá vé thường được tính bằng cách truy vấn trực tiếp bảng giá hiện tại lúc xe ra. Nếu Admin đổi giá khi xe đang đỗ trong bãi, khách hàng sẽ bị tính theo giá mới sai lệch. | **Cơ chế Snapshot Đơn giá**: Chụp lại giá vé tại thời điểm nhận xe và lưu cố định vào cột `don_gia_ap_dung` tại bảng `ve_xe`. Việc đổi bảng giá chỉ có hiệu lực với các lượt xe vào sau. |
| **3. Thanh toán trùng lặp**: Thu ngân bấm nút thanh toán nhiều lần có thể tạo nhiều bản ghi thu tiền cho cùng 1 vé. | **Ràng buộc `UNIQUE (ma_ve)` tại bảng `thanh_toan`**: Đảm bảo 1 vé xe chỉ có duy nhất 1 bản ghi thanh toán thành công, loại trừ 100% rủi ro tạo giao dịch trùng. |
| **4. Cho phép nhận vượt sức chứa bãi**: Không kiểm soát chặt chẽ số lượng xe đang gửi so với sức chứa tối đa. | **Kiểm soát sức chứa an toàn đồng thời**: Kiểm tra `tong_cho - so_xe_dang_gui > 0` và ràng buộc không cho phép giảm sức chứa xuống thấp hơn số xe đang gửi. |
| **5. Bảo mật kém (Lưu text thuần hoặc MD5)**: Mật khẩu lưu dạng văn bản thô hoặc băm MD5/SHA-256 dễ bị lộ khi bị tấn công từ điển. | **Mã hóa băm Argon2id**: Ứng dụng chuẩn bảo mật hiện đại nhất theo tiêu chuẩn bảo mật mật khẩu quốc tế. |
| **6. Giao diện Tkinter cũ kỹ, đơn điệu**: Giao diện xám đơn giản, các nút bấm cổ điển thiếu thẩm mỹ. | **CustomTkinter Light Premium Automotive**: Thiết kế sang trọng, hiện đại, màu sắc tinh tế (Teal `#087F83` + Gold `#C5A46D` trên nền sáng `#F3F6F8`), tích hợp biểu đồ Matplotlib trực quan. |

---

## 3. DANH MỤC TÀI LIỆU CÔNG NGHỆ CHÍNH THỐNG (OFFICIAL DOCUMENTATION)

1. **Python Software Foundation (PSF)**:
   - *Python 3.10+ Documentation*: Cú pháp ngôn ngữ, Lập trình hướng đối tượng (OOP), Quản lý biệt lệ (Exception Handling), Xử lý tệp tin văn bản (File I/O).  
   - URL: `https://docs.python.org/3/`
2. **Oracle MySQL Documentation**:
   - *MySQL 8.0 / 9.x Reference Manual*: Cú pháp DDL, Quản lý Transaction (ACID), Generated Columns, Khóa ngoại và Ràng buộc toàn vẹn dữ liệu.  
   - URL: `https://dev.mysql.com/doc/refman/8.0/en/`
3. **CustomTkinter Documentation**:
   - Hướng dẫn thiết kế giao diện đồ họa Python, quản lý Theme và Widget hiện đại.  
   - URL: `https://customtkinter.tomschimansky.com/documentation/`
4. **Argon2 Password Hashing Standard**:
   - RFC 9106: *Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications*.  
   - URL: `https://datatracker.ietf.org/doc/html/rfc9106`
5. **Matplotlib User Guide**:
   - *Embedding Matplotlib in Graphical User Interfaces (Tkinter)*: Kỹ thuật nhúng đồ thị động vào giao diện Python.  
   - URL: `https://matplotlib.org/stable/users/explain/figure/interactive.html`
