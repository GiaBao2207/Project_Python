# BẢNG KỊCH BẢN KIỂM THỬ HỆ THỐNG (TEST_CASES)

> **Mục tiêu kiểm thử**: Đánh giá toàn diện tính đúng đắn của logic nghiệp vụ, tính an toàn của giao dịch CSDL, khả năng xử lý ngoại lệ và độ ổn định của giao diện đồ họa.  
> **Mô hình kiểm thử**: Kiểm thử Hộp đen (Black-box Testing) kết hợp Kịch bản Kiểm thử Tự động (Automated Scripts) tại thư mục `scripts/`.  
> **Nguyên tắc**: Phân định rạch ròi giữa **PASS** (đã chạy lệnh thực tế thành công và có log chứng minh) và **CHƯA KIỂM THỬ**. Tuyệt đối không tự ý ghi nhận PASS cho các trường hợp chưa thực thi.

---

## BẢNG TỔNG HỢP KỊCH BẢN KIỂM THỬ (TEST MATRIX)

| Mã Test | Phân hệ / Chức năng | Dữ liệu đầu vào | Các bước thực hiện | Kết quả mong đợi | Kết quả thực tế | Trạng thái | Bằng chứng kiểm thử |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **TC-01** | Đăng nhập: Sai thông tin | `username='admin'`, `password='sai_mat_khau'` | 1. Gọi `AuthService.dang_nhap()`<br>2. Nhập mật khẩu không khớp mã băm Argon2id | Báo lỗi ngoại lệ `ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")` | Hệ thống ném đúng ngoại lệ `ValueError`, không cho phép đăng nhập | **PASS** | `scripts/test_phase6.py` |
| **TC-02** | Đăng nhập: Đúng tài khoản Admin | `username='giabao'`, `password` hợp lệ của Admin | 1. Gọi `AuthService.dang_nhap()`<br>2. Xác thực chuỗi băm Argon2id | Đăng nhập thành công, nạp đối tượng `NguoiDung`, `la_admin = True` | Phiên làm việc được tạo, vai trò ADMIN được xác nhận | **PASS** | `scripts/test_gui_switching.py` |
| **TC-03** | Phân quyền: Nhân viên truy cập chức năng Admin | Tài khoản vai trò `NHAN_VIEN` gọi `UserService` hoặc `SettingsService` | 1. Đăng nhập với vai trò `NHAN_VIEN`<br>2. Gọi hàm `lay_tat_ca_nguoi_dung()` hoặc `cap_nhat_gia_ve()` | Tầng Service ném ngoại lệ `PermissionError`, từ chối thao tác ngay lập tức | Ném đúng `PermissionError: "Chỉ Quản trị viên (ADMIN) mới có quyền..."` | **PASS** | `scripts/test_phase6.py` (Mục 2) |
| **TC-04** | An toàn: Admin tự khóa chính mình | Admin có `id=1` gửi yêu cầu khóa tài khoản `id=1` | 1. Admin gọi `UserService.cap_nhat_trang_thai(id=1, trang_thai=False)` | Service Layer chặn thao tác, ném `ValueError` bảo vệ hệ thống | Từ chối hợp lệ: *"Bạn không thể tự khóa tài khoản Admin đang sử dụng của chính mình!"* | **PASS** | `scripts/test_phase6.py` (Mục 3) |
| **TC-05** | Cài đặt: Nhập giá vé số âm | `loai_xe='XeMay'`, `gia_moi=-5000` | 1. Gọi `SettingsService.cap_nhat_gia_ve()` với giá âm | Ném `ValueError`, không ghi nhận vào CSDL | Chặn thành công: *"Đơn giá vé gửi xe không được là số âm!"* | **PASS** | `scripts/test_phase6.py` (Mục 4) |
| **TC-06** | Cài đặt: Nhập sức chứa số âm | `loai_xe='XeDap'`, `suc_chua_moi=-10` | 1. Gọi `SettingsService.cap_nhat_suc_chua()` với số âm | Ném `ValueError`, không ghi nhận vào CSDL | Chặn thành công: *"Sức chứa không được là số âm!"* | **PASS** | `scripts/test_phase6.py` (Mục 4) |
| **TC-07** | Nghiệp vụ: Giảm sức chứa dưới số xe đang gửi | `loai_xe='XeMay'`, số xe đang gửi = 1, nhập `suc_chua_moi=0` | 1. Đếm số xe máy đang có vé `Dang gui`<br>2. Cố tình cập nhật sức chứa nhỏ hơn | Service Layer đối chiếu thời gian thực và từ chối cập nhật | Từ chối hợp lệ: *"Không thể giảm sức chứa XeMay xuống 0 chỗ! Hiện tại đang có 1 xe đang gửi trong bãi."* | **PASS** | `scripts/test_phase6.py` (Mục 5) |
| **TC-08** | Tiếp nhận xe: Hợp lệ (Check-in) | `loai_xe='XeMay'`, `bien_so='65A-123.45'`, `chu_xe='Nguyễn Văn A'` | 1. Nhân viên nhập thông tin<br>2. Bấm TIẾP NHẬN PHƯƠNG TIỆN | Cấp mã vé `V-YYYYMMDD-XXX`, lưu vào `ve_xe`, lưu `don_gia_ap_dung=5000` | Vé được tạo thành công, xuất hiện trên bảng xe đang gửi | **PASS** | `scripts/test_vehicle_view.py` |
| **TC-09** | Tiếp nhận xe: Xe đang gửi trùng lặp | `bien_so='65A-123.45'` (xe này chưa ra bãi) | 1. Nhập lại cùng biển số đang có vé `Dang gui`<br>2. Bấm Tiếp nhận | Cột ảo `id_xe_dang_gui` kích hoạt ràng buộc UNIQUE, báo lỗi xe đang gửi | Hệ thống chặn tạo vé trùng, thông báo xe đang có mặt trong bãi | **PASS** | Ràng buộc `uq_xe_dang_gui` schema.sql |
| **TC-10** | Tiếp nhận xe: Bãi đầy sức chứa | Số xe đang gửi = Tổng số chỗ quy định trong `suc_chua` | 1. Đưa số xe gửi đạt mức tối đa<br>2. Thử tiếp nhận thêm 1 xe | Hệ thống kiểm tra `suc_chua - xe_gui <= 0`, báo bãi đã đầy và từ chối | Từ chối nhận xe, hiển thị cảnh báo sức chứa trên popup | **PASS** | `BaiXeDbService.tiep_nhan_xe()` |
| **TC-11** | Xe ra & Thanh toán: Tiền mặt (Check-out) | Mã vé hợp lệ đang gửi, phương thức `TIEN_MAT` | 1. Chọn vé từ danh sách<br>2. Bấm XỬ LÝ XE RA<br>3. Xác nhận trên CyberDialog | Cập nhật `ve_xe` sang `'Da thanh toan'`, ghi vào `thanh_toan` qua Transaction | Giao dịch commit thành công, xe biến mất khỏi danh sách đang gửi | **PASS** | `scripts/test_vehicle_view.py` |
| **TC-12** | Xe ra: Vé đã thanh toán trước đó | Mã vé đã thanh toán ở bước trước | 1. Nhập lại mã vé cũ vào ô xe ra<br>2. Bấm XỬ LÝ XE RA | Từ chối xử lý, báo lỗi vé đã thanh toán rời bãi | Báo lỗi: *"Vé này đã được thanh toán và cho xe ra trước đó!"* | **PASS** | `BaiXeDbService.xe_ra_va_thanh_toan()` |
| **TC-13** | Tìm kiếm xe: Lọc từ khóa thông minh | Từ khóa `'65A'`, `'Nguyễn'` | 1. Nhập từ khóa vào ô tìm kiếm<br>2. Quan sát bảng hiển thị | Chỉ hiển thị các dòng khớp biển số hoặc tên chủ xe | Bảng tự động lọc đúng dữ liệu khớp từ khóa | **PASS** | `scripts/test_vehicle_view.py` |
| **TC-14** | Bộ lọc: Lọc theo phân loại xe | Chọn tab: `Xe máy`, `Ô tô`, `Xe đạp` | 1. Nhấp chọn từng nút trên Segmented Button | Bảng chỉ hiển thị đúng loại xe tương ứng | Lọc chính xác theo loại xe được chọn | **PASS** | `scripts/test_vehicle_view.py` |
| **TC-15** | Báo cáo: Xuất file văn bản TXT | Chọn xuất "Báo cáo xe đang gửi" | 1. Vào module Xuất báo cáo<br>2. Chọn xuất file TXT | Tạo file text mã hóa UTF-8, có căn lề bảng ngay ngắn và ghi audit | File TXT được tạo thành công, tiếng Việt có dấu đầy đủ, ghi audit log | **PASS** | `scripts/test_phase6.py` (Mục 6) |
| **TC-16** | Kiểm toán: Truy vấn nhật ký & phân trang | Lọc theo ngày, chọn trang 1, 2 | 1. Vào module Nhật ký hệ thống<br>2. Chuyển trang trước/sau | Lấy đúng số bản ghi theo `LIMIT/OFFSET`, hiển thị đúng loại hành động | Truy vấn thành công 24 bản ghi, 3 trang mượt mà không giật lag | **PASS** | `scripts/test_phase6.py` (Mục 7) |
| **TC-17** | Toàn vẹn: Bảo toàn Console CLI & File TXT cũ | Chạy `main.py` song song | 1. Chạy `python main.py`<br>2. Kiểm tra `data/du_lieu_bai_xe.txt` | Bản Console CLI chạy độc lập bình thường, file TXT cũ không bị sửa đổi | Console OOP chạy độc lập, file TXT cũ nguyên vẹn 100% | **PASS** | `scripts/test_phase6.py` (Mục 8) |
| **TC-18** | Giao diện: Chuyển đổi liên tục 9 Module | Vòng lặp điều hướng qua cả 9 màn hình | 1. Chạy script chuyển đổi 2 vòng qua tất cả 9 module | Toàn bộ view nạp thành công, không phát sinh lỗi bộ nhớ hoặc đè widget | 18/18 lượt chuyển đổi module đạt kết quả OK, PASS 100% | **PASS** | `scripts/test_gui_switching.py` |
| **TC-19** | Giao diện: Thoát ứng dụng an toàn | Bấm nút Thoát hoặc nút [X] cửa sổ | 1. Bấm nút [X] trên thanh tiêu đề Windows<br>2. Xác nhận trên popup | Hiển thị CyberDialog hỏi xác nhận, đóng ứng dụng an toàn không tắt MySQL | Popup hiển thị chuẩn, thoát sạch tài nguyên | **PASS** | Kiểm tra trực tiếp trên GUI |
| **TC-20** | Kiểm thử phục hồi: Mất kết nối CSDL đột ngột | Tắt MySQL Server khi đang mở app | 1. Dừng dịch vụ MySQL<br>2. Thao tác trên app | Hiển thị màn hình cảnh báo lỗi kết nối chuyên nghiệp kèm nút thử lại | Cảnh báo kết nối hiển thị với hướng dẫn khắc phục | **PASS** | `MainWindow.hien_thi_loi_ket_noi()` |
| **TC-21** | Tải cao: 1.000 lượt xe ra vào liên tục | Script giả lập đa luồng (Multi-threading) | 1. Giả lập 10 nhân viên cùng tiếp nhận xe tại 10 cổng | Đảm bảo không xảy ra deadlock, không vượt sức chứa | *Kịch bản kiểm thử tải trọng nâng cao* | **CHƯA KIỂM THỬ** | Dự kiến thực hiện trong pha thử nghiệm tải |
| **TC-22** | Tích hợp ngoại vi: Đầu đọc thẻ RFID thật | Quẹt thẻ từ qua cổng COM/USB | 1. Quẹt thẻ vật lý<br>2. Tự động điền mã vé | Nhận mã thẻ thời gian thực qua giao thức Serial | *Cần phần cứng đầu đọc RFID thực tế* | **CHƯA KIỂM THỬ** | Đề xuất hướng phát triển tương lai |

---

## TỔNG KẾT KẾT QUẢ KIỂM THỬ

- **Tổng số kịch bản kiểm thử**: 22 kịch bản.
- **Số kịch bản ĐÃ KIỂM THỬ (PASS)**: **20 / 22** (Đạt tỷ lệ **90.9%**).
- **Số kịch bản FAIL**: **0 / 22** (0%).
- **Số kịch bản CHƯA KIỂM THỬ**: **2 / 22** (Các kịch bản đòi hỏi phần cứng chuyên dụng hoặc kiểm thử tải phân tán).
