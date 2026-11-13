# ĐỀ CƯƠNG CHI TIẾT BÁO CÁO HỌC PHẦN (REPORT_OUTLINE)

> **Căn cứ**: Cấu trúc bắt buộc theo mẫu chính thức `BaoCao_LapTrinhPython_Maubaocao.pdf` (Trường Đại học Nam Cần Thơ – Trường Công nghệ số và Trí tuệ nhân tạo).  
> **Mục tiêu**: Bộ khung sườn toàn diện giúp người dùng và các công cụ biên soạn (như ChatGPT) có thể lập tức chuyển đổi thành báo cáo hoàn chỉnh định dạng Microsoft Word (.docx) mà không bị thiếu bất kỳ hạng mục nào.

---

## MỤC LỤC TỔNG THỂ DỰ KIẾN (THEO CHUẨN PDF)

```text
TRANG BÌA (Chuẩn ĐH Nam Cần Thơ)
MỤC LỤC
DANH MỤC TỪ VIẾT TẮT
DANH MỤC BẢNG BIỂU
DANH MỤC HÌNH ẢNH VÀ ĐỒ THỊ

PHẦN GIỚI THIỆU
  1. Đặt vấn đề
  2. Những nghiên cứu liên quan (≥ 5 ứng dụng/thư viện, phân tích sâu 1 ứng dụng)
  3. Mục tiêu của đề tài
  4. Đối tượng và phạm vi nghiên cứu
  5. Sơ đồ luồng dữ liệu DFD cấp 0

CHƯƠNG 1: ĐẶC TẢ YÊU CẦU
  1.1. Khảo sát nghiệp vụ bãi giữ xe thực tế
  1.2. Yêu cầu chức năng người dùng (Phân quyền Admin & Nhân viên)
  1.3. Yêu cầu phi chức năng (Bảo mật Argon2id, Giao dịch ACID, Hiệu năng)
  1.4. Đặc tả chi tiết 9 phân hệ chức năng cốt lõi

CHƯƠNG 2: THIẾT KẾ GIẢI PHÁP
  2.1. Thiết kế kiến trúc tổng thể (Mô hình 4-Tier Architecture)
  2.2. Sơ đồ phân cấp chức năng (Function Decomposition Diagram)
  2.3. Thiết kế giải thuật và Lưu đồ thuật toán (Flowcharts)
      2.3.1. Lưu đồ thuật toán tiếp nhận phương tiện (Check-in)
      2.3.2. Lưu đồ thuật toán xe ra và xử lý thanh toán (Check-out)
      2.3.3. Lưu đồ thuật toán điều chỉnh cấu hình sức chứa an toàn
  2.4. Thiết kế cấu trúc dữ liệu và mô hình hướng đối tượng (OOP)
      2.4.1. Lớp đối tượng cơ sở Xe và các lớp con (XeMay, OTo, XeDap)
      2.4.2. Lớp đối tượng VeXe và NguoiDung
  2.5. Thiết kế cơ sở dữ liệu MySQL (ERD và chi tiết 7 bảng)
  2.6. Thiết kế định dạng lưu trữ tệp văn bản TXT xuất báo cáo

CHƯƠNG 3: CÀI ĐẶT GIẢI PHÁP
  3.1. Môi trường phát triển và công cụ sử dụng
  3.2. Hiện thực các lớp đối tượng cốt lõi (Tầng Models)
  3.3. Hiện thực tầng truy vấn CSDL và Xử lý giao dịch (Repository & Transaction)
  3.4. Hiện thực tầng xử lý nghiệp vụ và bảo mật (Service Layer)
  3.5. Hiện thực giao diện đồ họa Desktop (CustomTkinter Light Premium)
  3.6. Bảng đối chiếu và minh chứng vận dụng kiến thức từ Bài 1 đến Bài 8

CHƯƠNG 4: ĐÁNH GIÁ VÀ KIỂM THỬ
  4.1. Mục tiêu và phương pháp kiểm thử
  4.2. Kịch bản kiểm thử nhập liệu đúng/sai (Validation Testing)
  4.3. Kịch bản kiểm thử tính đúng đắn của logic nghiệp vụ (Logic Testing)
  4.4. Kịch bản kiểm thử lưu trữ, toàn vẹn dữ liệu và giao dịch (ACID & Storage Testing)
  4.5. Đánh giá kết quả kiểm thử thực tế (Bảng ma trận Test Matrix)

PHẦN KẾT LUẬN
  1. Kết quả đạt được (Kiến thức Python làm chủ)
  2. Hạn chế của đề tài
  3. Hướng phát triển và mở rộng tương lai

TÀI LIỆU THAM KHẢO

PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG PHẦN MỀM
  Phụ lục 1: Hướng dẫn cài đặt môi trường Python và MySQL
  Phụ lục 2: Hướng dẫn chạy chương trình Console và Desktop
```

---

## CHI TIẾT NỘI DUNG TỪNG CHƯƠNG

### PHẦN GIỚI THIỆU
- **Nội dung cần viết**:
  - Tình hình đô thị hóa, gia tăng phương tiện cá nhân tại Việt Nam; khó khăn của bãi xe truyền thống (ghi vé giấy, dễ gian lận, mất vé, ùn tắc).
  - Khảo sát 5 ứng dụng/thư viện: `parking-management-system`, `smart-parking-python`, `openalpr`, `customtkinter`, `mysql-connector-python`. Phân tích sâu 1 dự án mã nguồn mở bãi xe trên GitHub để học tập logic và khắc phục nhược điểm.
  - Mục tiêu: Xây dựng hệ thống quản lý bãi xe thông minh Neon Parking Manager hoàn chỉnh từ Console đến Desktop GUI, áp dụng MySQL Transaction và Argon2id.
  - Phạm vi: Nhân viên thu ngân/bảo vệ trực ca và Quản trị viên quản lý bãi đỗ.
- **Sơ đồ cần vẽ**: Sơ đồ DFD cấp 0 (Người dùng $\leftrightarrow$ Python Script $\leftrightarrow$ MySQL DB & TXT).
- **Mã nguồn liên quan**: `main.py`, `app_desktop.py`.

---

### CHƯƠNG 1: ĐẶC TẢ YÊU CẦU
- **Nội dung cần viết**:
  - Mô tả bài toán nghiệp vụ tiếp nhận xe (Check-in), tính tiền (Check-out), đổi bảng giá bảo toàn snapshot, điều chỉnh sức chứa không âm và không nhỏ hơn số xe đang đỗ thực tế.
  - Bảng đặc tả trường dữ liệu và ràng buộc đối với từng loại xe: Xe máy (bắt buộc biển số), Ô tô (bắt buộc biển số, số chỗ), Xe đạp (mã thẻ định danh, không bắt buộc biển số).
  - Phân quyền: Ma trận phân quyền 9 chức năng giữa Admin và Nhân viên.
- **Bảng cần tạo**:
  - Bảng ma trận phân quyền người dùng (Role Matrix).
  - Bảng đặc tả các phân hệ chức năng.
- **Mã nguồn liên quan**: `services/auth_service.py`, `services/bai_xe_db_service.py`.

---

### CHƯƠNG 2: THIẾT KẾ GIẢI PHÁP
- **Nội dung cần viết**:
  - Kiến trúc phân tầng 4 lớp (GUI $\rightarrow$ Service $\rightarrow$ Repository $\rightarrow$ Database).
  - Sơ đồ phân cấp chức năng (9 phân hệ chính).
  - Phân tích chi tiết 3 lưu đồ thuật toán: Tiếp nhận xe, Cho xe ra thanh toán qua MySQL Transaction, Cài đặt sức chứa an toàn.
  - Thiết kế Hướng đối tượng OOP: Phân tích các class cha `Xe`, các class con `XeMay`, `OTo`, `XeDap` (tính kế thừa và đa hình trong hàm `tinh_tien()`); class `VeXe` (quan hệ chứa đối tượng Composition); class `NguoiDung`.
  - Thiết kế CSDL MySQL: Lược đồ 7 bảng (`nguoi_dung`, `bang_gia`, `suc_chua`, `xe`, `ve_xe`, `thanh_toan`, `nhat_ky`), phân tích cột ảo `id_xe_dang_gui` UNIQUE chống trùng vé, khóa ngoại và chỉ mục tối ưu.
- **Sơ đồ cần vẽ**:
  - Sơ đồ kiến trúc 4 tầng (Mermaid).
  - Sơ đồ phân cấp chức năng (Mermaid).
  - 3 Lưu đồ Flowchart (Mermaid).
  - Sơ đồ lớp UML Class Diagram (Mermaid).
  - Sơ đồ thực thể quan hệ ERD MySQL (Mermaid).
- **Tài liệu tham chiếu**: [DIAGRAM_PLAN.md](file:///c:/Users/phamt/PycharmProjects/PythonProject/QuanLyBaiGiuXe/docs/report/DIAGRAM_PLAN.md), [DATABASE_DESIGN.md](file:///c:/Users/phamt/PycharmProjects/PythonProject/QuanLyBaiGiuXe/docs/report/DATABASE_DESIGN.md).

---

### CHƯƠNG 3: CÀI ĐẶT GIẢI PHÁP
- **Nội dung cần viết**:
  - Môi trường: Python 3.10+, PyCharm, CustomTkinter, MySQL Connector, Argon2-cffi, Matplotlib.
  - Trích dẫn và giải thích các đoạn mã nguồn then chốt:
    1. Đóng gói OOP và Đa hình trong `models/` (`xe.py`, `XeMay.py`, `Oto.py`, `XeDap.py`).
    2. Context manager `giao_dich()` xử lý Transaction commit/rollback trong `database/db_connection.py`.
    3. Bảo mật Argon2id trong `security/hasher.py` và phân quyền trong `services/auth_service.py`.
    4. Xử lý nghiệp vụ tiếp nhận xe và xe ra trong `services/bai_xe_db_service.py`.
    5. Thiết kế giao diện Light Premium trong `config/theme.py`, `gui/main_window.py` và hệ thống Popup 2 lớp `gui/components/dialog.py`.
    6. Xuất báo cáo văn bản định dạng bảng tiếng Việt UTF-8 trong `services/report_service.py`.
  - **Mục then chốt (Bắt buộc theo PDF)**: Bảng đối chiếu và giải thích cách vận dụng các kiến thức từ **Bài 1 đến Bài 8** vào dự án.
- **Hình ảnh cần chụp**: Ảnh các đoạn code tiêu biểu từ PyCharm, giao diện các màn hình đang chạy.
- **Tài liệu tham chiếu**: [SOURCE_CODE_MAPPING.md](file:///c:/Users/phamt/PycharmProjects/PythonProject/QuanLyBaiGiuXe/docs/report/SOURCE_CODE_MAPPING.md), [LESSON_MAPPING.md](file:///c:/Users/phamt/PycharmProjects/PythonProject/QuanLyBaiGiuXe/docs/report/LESSON_MAPPING.md).

---

### CHƯƠNG 4: ĐÁNH GIÁ VÀ KIỂM THỬ
- **Nội dung cần viết**:
  - Mục tiêu kiểm thử: Đảm bảo phần mềm vận hành không lỗi, dữ liệu được bảo vệ an toàn khi có sự cố.
  - Phương pháp kiểm thử: Kiểm thử hộp đen với kịch bản chi tiết + Chạy script kiểm thử tự động.
  - Bảng kiểm thử 22 kịch bản (Test Cases) chi tiết với các cột: Mã test, Tên chức năng, Dữ liệu đầu vào, Các bước thực hiện, Kết quả mong đợi, Kết quả thực tế, Trạng thái (PASS / CHƯA KIỂM THỬ), Bằng chứng kiểm thử.
  - Đánh giá tổng quan: 20 kịch bản PASS (90.9%), 0 kịch bản FAIL.
- **Hình ảnh cần chụp**: Ảnh chụp màn hình Terminal chạy script `test_phase6.py` (PASS 8/8) và `test_gui_switching.py` (PASS 100%), ảnh popup cảnh báo lỗi và popup thành công 2 lớp trên phần mềm thật.
- **Tài liệu tham chiếu**: [TEST_CASES.md](file:///c:/Users/phamt/PycharmProjects/PythonProject/QuanLyBaiGiuXe/docs/report/TEST_CASES.md).

---

### PHẦN KẾT LUẬN & HƯỚNG PHÁT TRIỂN
- **Kết quả đạt được**:
  - Làm chủ toàn diện các kiến thức Python cơ bản đến nâng cao (Hàm, Cấu trúc dữ liệu, OOP, Exception Handling, File I/O).
  - Vận dụng thành công các công nghệ chuyên nghiệp: CustomTkinter Light Premium, MySQL Server với ACID Transaction, Argon2id Password Hashing, Matplotlib trực quan hóa nhúng GUI.
  - Xây dựng hoàn chỉnh một ứng dụng bãi đỗ xe có tính ứng dụng thực tiễn cao, chạy ổn định, bảo mật và thân thiện với người dùng.
- **Hạn chế**: Chưa tích hợp phần cứng nhận diện biển số qua camera; chưa kết nối cổng thanh toán trực tuyến qua ngân hàng.
- **Hướng phát triển**:
  - Tích hợp mô hình AI/Computer Vision (YOLO + OCR) tự động nhận dạng biển số xe khi qua cổng.
  - Tích hợp mã VietQR động để khách hàng quét mã chuyển khoản tự động xác nhận qua Webhook.

---

### TÀI LIỆU THAM KHẢO & PHỤ LỤC
- Tài liệu tham khảo chính thống, kiểm chứng được (Python Docs, CustomTkinter Docs, MySQL Connector Docs, Argon2-cffi Docs, các kho mã nguồn tham khảo).
- Hướng dẫn cài đặt chi tiết từng bước, cách tạo môi trường ảo `.venv`, cài đặt `requirements.txt`, cấu hình `.env`, chạy `schema.sql` và khởi chạy đồ án bằng file 1-click `Start_NeonParking.bat` hoặc lệnh Terminal.
- Toàn bộ mã nguồn cốt lõi đưa vào Phụ lục mã nguồn.
