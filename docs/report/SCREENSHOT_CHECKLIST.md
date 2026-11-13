# DANH MỤC HÌNH ẢNH CẦN CHỤP MINH CHỨNG (SCREENSHOT_CHECKLIST)

> **Mục tiêu**: Danh sách kiểm kê các ảnh chụp màn hình thực tế của ứng dụng Neon Parking Manager và môi trường phát triển để chuẩn bị chèn vào báo cáo Word theo đúng bố cục của PDF mẫu.  
> **Nguyên tắc**: 100% là ảnh chụp thực tế từ phần mềm đang chạy trên máy tính, tuyệt đối không dùng ảnh mockup hoặc ảnh giả lập.

---

## BẢNG THEO DÕI HÌNH ẢNH BÁO CÁO

| STT | Mã hình | Tên màn hình / Nội dung cần chụp | Thao tác thực tế trên phần mềm | Vị trí chèn trong báo cáo | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | **HINH-01** | Màn hình Khởi tạo Admin đầu tiên (First Admin Setup) | Khởi động app khi CSDL chưa có tài khoản, hiển thị form thiết lập Admin an toàn | Chương 1 & Chương 3 (Bảo mật) | *Cần chụp* |
| 2 | **HINH-02** | Màn hình Đăng nhập (Login View) | Giao diện đăng nhập Light Premium sang trọng, logo thương hiệu, nhập username & password | Chương 3 (Hiện thực) | *Cần chụp* |
| 3 | **HINH-03** | Màn hình Cảnh báo Lỗi Kết nối CSDL | Mô phỏng khi MySQL dừng hoạt động, hiển thị card thông báo lỗi chuyên nghiệp và nút thử lại | Chương 3 & Chương 4 (Xử lý lỗi) | *Cần chụp* |
| 4 | **HINH-04** | Tổng quan bãi xe (Dashboard View) | Hiển thị 4 thẻ KPI thời gian thực, bảng phân bố loại xe và biểu đồ cột Matplotlib 7 ngày gần nhất | Chương 1 & Chương 3 | *Cần chụp* |
| 5 | **HINH-05** | Quản lý phương tiện: Tiếp nhận xe vào bãi (Check-in) | Thao tác nhập biển số, chọn loại xe (Xe máy, Ô tô, Xe đạp), bấm tiếp nhận | Chương 1 & Chương 3 | *Cần chụp* |
| 6 | **HINH-06** | Popup 2 lớp: Tiếp nhận xe thành công | CyberDialog 2 lớp hiển thị đầy đủ thông tin: Mã vé, Loại xe, Biển số, Thời gian vào, Phí xe | Chương 3 (Popup 2 lớp) & Chương 4 | *Cần chụp* |
| 7 | **HINH-07** | Bảng danh sách xe đang gửi & Thanh tìm kiếm | Nhập từ khóa tìm kiếm (biển số/chủ xe), bộ lọc tab loại xe và các nút phân trang | Chương 1 & Chương 3 | *Cần chụp* |
| 8 | **HINH-08** | Xử lý xe ra và Popup xác nhận thanh toán | Chọn vé từ danh sách, hiển thị tính tiền và popup CyberDialog xác nhận trước khi thanh toán | Chương 1, 2 & Chương 3 | *Cần chụp* |
| 9 | **HINH-09** | Popup 2 lớp: Thanh toán thành công & Mở cổng | CyberDialog chi tiết giao dịch thu tiền (tiền mặt / chuyển khoản), thời gian ra | Chương 3 & Chương 4 | *Cần chụp* |
| 10 | **HINH-10** | Quản lý vé xe (Tickets View) | Bảng tra cứu lịch sử vé xe, lọc theo trạng thái Đang gửi / Đã thanh toán | Chương 1 & Chương 3 | *Cần chụp* |
| 11 | **HINH-11** | Quản lý doanh thu (Revenue View - Admin Only) | Thẻ KPI doanh thu tổng, tiền mặt, chuyển khoản và biểu đồ Matplotlib xu hướng ngày | Chương 1 & Chương 3 | *Cần chụp* |
| 12 | **HINH-12** | Thống kê hoạt động (Statistics View) | Biểu đồ Matplotlib phân tích 24h giờ cao điểm trong ngày và tỷ lệ lấp đầy bãi xe | Chương 1 & Chương 3 | *Cần chụp* |
| 13 | **HINH-13** | Quản lý nhân viên (Users View - Admin Only) | Danh sách tài khoản nhân viên, popup thêm nhân viên mới, trạng thái hoạt động/khóa | Chương 1 & Chương 3 | *Cần chụp* |
| 14 | **HINH-14** | Cấu hình hệ thống (Settings View - Admin Only) | Tab cài đặt Bảng giá vé và Tab Sức chứa bãi xe với thanh tiến trình lấp đầy | Chương 1 & Chương 3 | *Cần chụp* |
| 15 | **HINH-15** | Xuất báo cáo (Reports View) | Màn hình 3 card xuất báo cáo văn bản TXT và hộp thoại lưu file của Windows | Chương 1 & Chương 3 | *Cần chụp* |
| 16 | **HINH-16** | Tệp báo cáo văn bản TXT thực tế | Mở file TXT xuất ra trong Notepad, hiển thị bảng tiếng Việt UTF-8 căn lề ngay ngắn | Chương 3 & Chương 4 | *Cần chụp* |
| 17 | **HINH-17** | Nhật ký hệ thống (Audit View - Admin Only) | Bảng theo dõi lịch sử thao tác hệ thống, bộ lọc loại hành động và phân trang | Chương 1 & Chương 3 | *Cần chụp* |
| 18 | **HINH-18** | Cấu trúc CSDL trong MySQL Workbench | Ảnh chụp màn hình MySQL Workbench hiển thị 7 bảng và schema `neon_parking_db` | Chương 2 (CSDL) | *Cần chụp* |
| 19 | **HINH-19** | Kết quả chạy Test Script tự động Terminal | Màn hình PowerShell chạy `test_phase6.py` hiển thị PASS 8/8 và `test_gui_switching.py` PASS 100% | Chương 4 (Kiểm thử) | *Cần chụp* |
| 20 | **HINH-20** | Chương trình Console dòng lệnh độc lập | Màn hình chạy `python main.py` minh chứng bản Console nguyên bản vẫn hoạt động tốt | Chương 3 (Bảo toàn mã cũ) | *Cần chụp* |

---

## HƯỚNG DẪN CHỤP ẢNH CHUẨN ĐỒ HỌA BÁO CÁO
1. **Độ phân giải**: Chụp ảnh màn hình ở độ phân giải tiêu chuẩn (tối thiểu $1280 \times 800$ hoặc Full HD $1920 \times 1080$).
2. **Công cụ**: Sử dụng công cụ Snipping Tool hoặc phím tắt `Windows + Shift + S` trên Windows để cắt khung hình gọn gàng, không dính thanh taskbar nếu không cần thiết.
3. **Lưu trữ**: Lưu toàn bộ ảnh vào thư mục `docs/report/images/` với tên tệp chuẩn hóa (VD: `hinh_04_dashboard.png`, `hinh_06_popup_tiep_nhan.png`).
4. **Định dạng**: Định dạng PNG chất lượng cao không nén nhòe.
