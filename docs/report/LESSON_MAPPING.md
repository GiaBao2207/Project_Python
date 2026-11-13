# KHUNG ĐỐI CHIẾU KIẾN THỨC BÀI HỌC HỌC PHẦN (LESSON_MAPPING)

> **Mục đích**: Chuẩn bị cấu trúc chuẩn mực để đối chiếu nội dung thực tế của **Bài 1 đến Bài 8** (học phần Lập trình Python – Thực hành) vào mã nguồn dự án Neon Parking Manager ngay khi người dùng cung cấp hình ảnh giáo trình/bài giảng.  
> **Nguyên tắc**: Tuyệt đối không phỏng đoán nội dung khi chưa nhận ảnh chính thức từ người dùng. Khi có hình ảnh, Agent sẽ đọc trực tiếp tên bài học, trích xuất đề mục và điền chính xác vào bảng bên dưới.

---

## 1. KHUNG TIẾP NHẬN BÀI HỌC (BÀI 1 ĐẾN BÀI 8)

| Bài học | Tên bài học chính thức (Từ ảnh) | Trọng tâm kiến thức lý thuyết | Tệp mã nguồn minh họa trong dự án | Hàm / Class / Dòng code cụ thể | Giải thích cơ chế (Dành cho sinh viên mới học) | Kiến thức trong bài chưa áp dụng (nếu có) |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bài 1** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `models/xe.py`, `main.py` | `_bien_so`, kiểu `int`, `str` | Khai báo biến, gán giá trị, in dữ liệu ra màn hình console bằng `print()` | *Chờ đối chiếu* |
| **Bài 2** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `services/bai_xe_db_service.py` | `if`, `elif`, `else` | Rẽ nhánh điều kiện kiểm tra hợp lệ của biển số và kiểm tra sức chứa khả dụng | *Chờ đối chiếu* |
| **Bài 3** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `gui/modules/vehicles/vehicle_view.py` | `for`, `while` | Duyệt qua danh sách phương tiện để hiển thị lên bảng giao diện Desktop | *Chờ đối chiếu* |
| **Bài 4** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `services/auth_service.py` | `def`, tham số, giá trị trả về | Tổ chức code thành các hàm tái sử dụng, truyền tham số và nhận kết quả | *Chờ đối chiếu* |
| **Bài 5** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `gui/components/sidebar.py` | `List`, `Dictionary`, `Tuple` | Quản lý danh mục menu động bằng List of Dictionaries, lưu trữ cặp nhãn-giá trị | *Chờ đối chiếu* |
| **Bài 6** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `storage/file_txt.py`, `services/report_service.py` | `open()`, `with`, `write()` | Mở tệp tin, ghi dữ liệu danh sách xe và doanh thu ra file TXT chuẩn UTF-8 | *Chờ đối chiếu* |
| **Bài 7** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `models/xe.py`, `models/XeMay.py` | `class`, `self`, `__init__`, `super()` | Lập trình hướng đối tượng OOP: Tạo class cha `Xe`, class con `XeMay` kế thừa cha | *Chờ đối chiếu* |
| **Bài 8** | *Chờ cung cấp ảnh* | *Chờ trích xuất từ ảnh* | `app_desktop.py`, `gui/` | `CustomTkinter`, Event Handling | Xây dựng giao diện đồ họa Desktop, bắt sự kiện click nút bấm, hiển thị popup modal | *Chờ đối chiếu* |

---

## 2. QUY TRÌNH XỬ LÝ KHI NGƯỜI DÙNG CUNG CẤP ẢNH BÀI HỌC

Khi người dùng gửi ảnh các slide bài học từ Bài 1 đến Bài 8, các bước xử lý chuẩn mực sẽ được thực hiện như sau:

1. **Đọc và Trích xuất**:
   - Xác định chính xác tiêu đề bài học và các mục con trong ảnh.
   - Ghi lại các khái niệm lý thuyết cốt lõi mà giảng viên giảng dạy trong bài đó.
2. **Đối soát Mã nguồn thực tế**:
   - Tìm kiếm đoạn mã nguồn trong dự án Neon Parking Manager thể hiện rõ nét nhất kiến thức đó.
   - Ưu tiên các ví dụ ngắn gọn, chuẩn Pythonic, có chú thích tiếng Việt dễ hiểu.
3. **Giải thích sư phạm (Thân thiện với người mới học)**:
   - Dùng văn phong sư phạm trong sáng, giải thích tại sao lại viết như vậy, mang lại lợi ích gì trong bài toán quản lý bãi xe thực tế.
4. **Phân định rõ ràng**:
   - Nếu có kiến thức trong bài học chưa được vận dụng trong dự án (ví dụ: đệ quy, con trỏ tệp `seek()`), ghi rõ tại cột *"Kiến thức chưa áp dụng"* một cách trung thực, không cố gượng ép.
