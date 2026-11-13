# TỔNG HỢP SƠ ĐỒ VÀ BẢN VẼ HỆ THỐNG (DIAGRAM_PLAN)

> **Mục đích**: Cung cấp toàn bộ các sơ đồ luồng dữ liệu, sơ đồ kiến trúc, lưu đồ thuật toán và sơ đồ lớp hướng đối tượng theo đúng yêu cầu bắt buộc của file PDF mẫu học phần (`BaoCao_LapTrinhPython_Maubaocao.pdf`).  
> **Nguyên tắc**: 100% sơ đồ được xây dựng dựa trên quy trình nghiệp vụ và cấu trúc mã nguồn có thật trong dự án Neon Parking Manager.

---

## 1. SƠ ĐỒ DFD CẤP 0 (DATA FLOW DIAGRAM LEVEL 0)

*Căn cứ*: Phần Giới thiệu trong PDF mẫu yêu cầu mô tả luồng dữ liệu đi từ người dùng vào script Python và lưu xuống kho dữ liệu.
*Lưu ý dự án*: MySQL Server là nơi lưu trữ dữ liệu chính (Operational Database), file TXT là dữ liệu xuất báo cáo định kỳ.

```mermaid
graph LR
    subgraph TacNhanNgoai["TÁC NHÂN NGOÀI"]
        NV["Nhân Viên Trực Cổng"]
        AD["Quản Trị Viên (Admin)"]
    end

    subgraph HeThongPython["HỆ THỐNG PHẦN MỀM PYTHON"]
        APP["Neon Parking Manager<br>(Mã nguồn Python OOP / CustomTkinter)"]
    end

    subgraph KhoDuLieu["KHO LƯU TRỮ DỮ LIỆU"]
        DB[("MySQL Database<br>neon_parking_db<br>(7 Bảng quan hệ ACID)")]
        TXT[("Tệp Báo Cáo TXT<br>(Định dạng UTF-8)")]
        OLD_TXT[("Tệp TXT Gốc<br>du_lieu_bai_xe.txt<br>(Bảo toàn Console cũ)")]
    end

    %% Luồng của Nhân viên
    NV -->|"Thông tin xe vào, biển số, loại xe"| APP
    NV -->|"Mã vé xe ra, phương thức thanh toán"| APP
    APP -->|"Vé xe, thông báo chỗ trống, hóa đơn"| NV

    %% Luồng của Admin
    AD -->|"Cấu hình bảng giá, tổng sức chứa"| APP
    AD -->|"Tài khoản nhân viên mới, phân quyền"| APP
    AD -->|"Yêu cầu xuất báo cáo thống kê"| APP
    APP -->|"Dashboard KPI, doanh thu, nhật ký hệ thống"| AD

    %% Luồng lưu trữ
    APP <-->|"Đọc/Ghi dữ liệu xe, vé, thanh toán (Transaction)"| DB
    APP -->|"Xuất file báo cáo tổng hợp UTF-8"| TXT
    APP <-->|"Đọc/Ghi dữ liệu chế độ Console CLI"| OLD_TXT
```

---

## 2. SƠ ĐỒ PHÂN CẤP CHỨC NĂNG (FUNCTION DECOMPOSITION DIAGRAM)

*Căn cứ*: Chương 2 – Thiết kế kiến trúc theo yêu cầu PDF mẫu.

```mermaid
graph TD
    ROOT["HỆ THỐNG NEON PARKING MANAGER"]

    ROOT --> M1["1. XÁC THỰC & BẢO MẬT"]
    M1 --> M1_1["Thiết lập Admin đầu tiên"]
    M1 --> M1_2["Đăng nhập (Argon2id)"]
    M1 --> M1_3["Đổi mật khẩu cá nhân"]
    M1 --> M1_4["Đăng xuất & Hủy phiên"]

    ROOT --> M2["2. TIẾP NHẬN PHƯƠNG TIỆN"]
    M2 --> M2_1["Kiểm tra sức chứa khả dụng"]
    M2 --> M2_2["Chặn xe đang gửi trùng lặp"]
    M2 --> M2_3["Chụp snapshot đơn giá"]
    M2 --> M2_4["Cấp mã vé và in thẻ"]

    ROOT --> M3["3. XỬ LÝ XE RA & THANH TOÁN"]
    M3 --> M3_1["Tra cứu vé (Biển số / Mã vé)"]
    M3 --> M3_2["Tính toán thời gian & số tiền"]
    M3 --> M3_3["Thanh toán Tiền mặt / Ngân hàng"]
    M3 --> M3_4["Thực thi MySQL Transaction"]

    ROOT --> M4["4. QUẢN TRỊ & THỐNG KÊ (Admin)"]
    M4 --> M4_1["Dashboard KPI thời gian thực"]
    M4 --> M4_2["Thống kê doanh thu & Giờ cao điểm"]
    M4 --> M4_3["Quản lý nhân viên (Chống tự khóa)"]
    M4 --> M4_4["Cài đặt bảng giá & Sức chứa"]
    M4 --> M4_5["Xuất báo cáo văn bản TXT"]
    M4 --> M4_6["Truy vấn nhật ký kiểm toán (Audit)"]
```

---

## 3. LƯU ĐỒ THUẬT TOÁN (FLOWCHARTS) CÁC CHỨC NĂNG CỐT LÕI

### 3.1. Lưu đồ tiếp nhận xe vào bãi (Check-in Flowchart)
Mô tả quy trình xử lý nghiệp vụ khi một phương tiện đến cổng bãi đỗ:

```mermaid
flowchart TD
    Start([Bắt đầu: Tiếp nhận xe]) --> Input[Nhân viên nhập Biển số/Mã thẻ, chọn Loại xe]
    Input --> Validate{Dữ liệu hợp lệ?<br>Biển số không rỗng với Ô tô/Xe máy}
    Validate -- Không --> Err1[Báo lỗi: Thông tin xe không hợp lệ] --> End([Kết thúc])
    Validate -- Có --> CheckCap{Sức chứa khả dụng > 0?<br>tong_cho - so_xe_dang_gui > 0}
    CheckCap -- Không --> Err2[Báo lỗi: Bãi xe đã đầy sức chứa!] --> End
    CheckCap -- Có --> CheckDup{Xe đã có vé 'Dang gui'?<br>Kiểm tra cột ảo id_xe_dang_gui}
    CheckDup -- Có --> Err3[Báo lỗi: Xe này đang gửi trong bãi!] --> End
    CheckDup -- Không --> GetPrice[Lấy đơn giá hiện hành từ bang_gia]
    GetPrice --> GenTicket[Sinh mã vé duy nhất: V-YYYYMMDD-XXX]
    GenTicket --> SaveDB[(Lưu vào ve_xe:<br>Snapshot don_gia_ap_dung, gio_vao=NOW)]
    SaveDB --> LogAudit[(Ghi nhật ký: TIEP_NHAN_XE)]
    LogAudit --> PopupSuccess[Hiển thị CyberDialog 2 lớp thành công]
    PopupSuccess --> RefreshUI[Cập nhật bảng xe đang gửi & KPI]
    RefreshUI --> End
```

---

### 3.2. Lưu đồ xe ra và xử lý thanh toán (Check-out Flowchart)
Mô tả nghiệp vụ khi xe rời bãi, áp dụng MySQL Transaction bảo toàn kế toán:

```mermaid
flowchart TD
    Start([Bắt đầu: Xe ra]) --> ScanTicket[Nhân viên nhập Mã vé hoặc chọn dòng trên bảng]
    ScanTicket --> FindTicket{Tìm thấy vé trong CSDL?}
    FindTicket -- Không --> Err1[Báo lỗi: Không tìm thấy mã vé!] --> End([Kết thúc])
    FindTicket -- Có --> CheckStatus{Trạng thái vé là 'Dang gui'?}
    CheckStatus -- Đã thanh toán --> Err2[Báo lỗi: Vé này đã thanh toán trước đó!] --> End
    CheckStatus -- Đã hủy --> Err3[Báo lỗi: Vé này đã bị hủy bỏ!] --> End
    CheckStatus -- Đúng --> Calc[Lấy don_gia_ap_dung từ vé<br>Tính số tiền = don_gia_ap_dung<br>Ghi nhận gio_ra = NOW]
    Calc --> ShowConfirm[Hiển thị Popup CyberDialog xác nhận chi tiết số tiền]
    ShowConfirm --> UserChoice{Người dùng bấm Xác nhận?}
    UserChoice -- Hủy bỏ --> End
    UserChoice -- Xác nhận --> BeginTrans[(Bắt đầu MySQL Transaction<br>autocommit = False)]
    BeginTrans --> UpdateTicket[Cập nhật ve_xe:<br>trang_thai = 'Da thanh toan',<br>gio_ra = NOW, id_nhan_vien_ra]
    UpdateTicket --> InsertPay[Chèn bản ghi vào thanh_toan:<br>ma_ve, so_tien, phuong_thuc, id_nhan_vien_thu]
    InsertPay --> TryCommit{Thực thi thành công?}
    TryCommit -- Lỗi ngoại lệ --> Rollback[(Rollback Transaction<br>Khôi phục dữ liệu gốc)]
    Rollback --> ErrTrans[Báo lỗi: Giao dịch thất bại!] --> End
    TryCommit -- Thành công --> Commit[(Commit Transaction<br>Lưu vĩnh viễn vào DB)]
    Commit --> LogAudit[(Ghi nhật ký: XE_RA_THANH_TOAN)]
    LogAudit --> OpenGate[Mở cổng bãi xe & Thông báo thành công]
    OpenGate --> RefreshUI[Cập nhật lại KPI và bảng xe đang gửi]
    RefreshUI --> End
```

---

### 3.3. Lưu đồ điều chỉnh cấu hình sức chứa an toàn (Capacity Settings Flowchart)
Minh chứng việc bảo vệ toàn vẹn nghiệp vụ (không thể giảm sức chứa dưới số xe đang đỗ):

```mermaid
flowchart TD
    Start([Admin điều chỉnh Sức chứa]) --> Input[Nhập tổng số chỗ mới cho Loại xe]
    Input --> CheckNeg{Số chỗ nhập vào >= 0?}
    CheckNeg -- Không --> Err1[Báo lỗi: Sức chứa không được là số âm!] --> End([Kết thúc])
    CheckNeg -- Có --> CountCurrent[Đếm số xe loại này đang có vé 'Dang gui']
    CountCurrent --> CheckValid{Số chỗ mới >= Số xe đang gửi?}
    CheckValid -- Không --> Err2[Báo lỗi: Không thể giảm sức chứa thấp hơn<br>số lượng xe đang thực tế gửi trong bãi!] --> End
    CheckValid -- Có --> UpdateDB[(Cập nhật bảng suc_chua trong MySQL)]
    UpdateDB --> LogAudit[(Ghi nhật ký: SUA_SUC_CHUA)]
    LogAudit --> Success[Báo thành công & Cập nhật thanh tiến trình]
    Success --> End
```

---

## 4. SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOP CLASS DIAGRAM)

*Căn cứ*: Chương 2 & 3 – Thể hiện nguyên lý Kế thừa, Đóng gói và Đa hình trong `models/`:

```mermaid
classDiagram
    class Xe {
        #str _bien_so
        #str _loai_xe
        #datetime _gio_vao
        #bool _da_thanh_toan
        +bien_so() str
        +loai_xe() str
        +gio_vao() datetime
        +da_thanh_toan() bool
        +tinh_tien(gio_ra) int*
        +__str__() str
    }

    class XeMay {
        -int _dung_tich
        +tinh_tien(gio_ra) int
        +__str__() str
    }

    class OTo {
        -int _so_cho_ngoi
        +tinh_tien(gio_ra) int
        +__str__() str
    }

    class XeDap {
        -str _ma_the
        +tinh_tien(gio_ra) int
        +__str__() str
    }

    class VeXe {
        -str _ma_ve
        -Xe _xe
        -int _don_gia
        -datetime _gio_vao
        -datetime _gio_ra
        -str _trang_thai
        +ma_ve() str
        +xe() Xe
        +xac_nhan_thanh_toan(gio_ra) int
    }

    class NguoiDung {
        +int id
        +str ten_dang_nhap
        +str mat_khau_hash
        +str ho_ten
        +str vai_tro
        +str trang_thai
        +la_admin() bool
        +dang_hoat_dong() bool
    }

    Xe <|-- XeMay : Kế thừa (Inheritance)
    Xe <|-- OTo : Kế thừa (Inheritance)
    Xe <|-- XeDap : Kế thừa (Inheritance)
    VeXe *-- Xe : Chứa đối tượng (Composition)
```

---

## 5. SƠ ĐỒ KIẾN TRÚC PHÂN TẦNG (TIER ARCHITECTURE DIAGRAM)

```mermaid
graph TD
    subgraph GUI_Layer["1. TẦNG GIAO DIỆN (GUI LAYER)"]
        app["app_desktop.py (Main Application Entry)"]
        mw["MainWindow (Controller & Router)"]
        sidebar["Sidebar Component"]
        header["Header Component"]
        dialog["CyberDialog System (Dual-Layer)"]
        views["9 Phân Hệ Nghiệp Vụ:<br>Dashboard, Vehicles, Tickets, Revenue,<br>Statistics, Users, Settings, Reports, Audit"]
        app --> mw
        mw --> sidebar
        mw --> header
        mw --> views
        views --> dialog
    end

    subgraph Service_Layer["2. TẦNG NGHIỆP VỤ & BẢO MẬT (SERVICE LAYER)"]
        auth_srv["AuthService<br>(Xác thực, Quản lý Session, Phân quyền)"]
        bx_srv["BaiXeDbService<br>(Tiếp nhận, Xe ra, Tính tiền, Sức chứa)"]
        user_srv["UserService<br>(CRUD Nhân viên, Chống tự khóa)"]
        setting_srv["SettingsService<br>(Bảng giá snapshot, Ràng buộc sức chứa)"]
        audit_srv["AuditService<br>(Bộ lọc đa tiêu chí, Phân trang)"]
        rep_srv["ReportService<br>(Định dạng bảng ASCII, Xuất tệp TXT UTF-8)"]
        hasher["Hasher (Argon2id Algorithm)"]
        auth_srv --> hasher
    end

    subgraph Repo_Layer["3. TẦNG TRUY VẤN CSDL (REPOSITORY LAYER)"]
        user_repo["UserRepository<br>(Truy vấn nguoi_dung, nhat_ky)"]
        veh_repo["VehicleRepository<br>(Truy vấn xe, ve_xe, bang_gia, suc_chua, thanh_toan)"]
    end

    subgraph DB_Layer["4. TẦNG CƠ SỞ DỮ LIỆU & FILE (DATABASE & STORAGE)"]
        db_conn["db_connection.py<br>(Context manager giao_dich() Transaction)"]
        mysql[("MySQL Server 9.7<br>neon_parking_db")]
        env[".env Config File"]
        txt_out["Báo cáo văn bản TXT"]
        txt_old["data/du_lieu_bai_xe.txt (Console)"]
    end

    %% Kết nối liên tầng
    views -->|"Gọi logic nghiệp vụ"| auth_srv
    views -->|"Gọi logic bãi xe"| bx_srv
    views -->|"Thao tác nhân viên"| user_srv
    views -->|"Cài đặt hệ thống"| setting_srv
    views -->|"Xem nhật ký"| audit_srv
    views -->|"Yêu cầu xuất tệp"| rep_srv

    auth_srv --> user_repo
    user_srv --> user_repo
    audit_srv --> user_repo
    bx_srv --> veh_repo
    setting_srv --> veh_repo
    rep_srv --> veh_repo
    rep_srv --> txt_out

    user_repo --> db_conn
    veh_repo --> db_conn
    db_conn --> env
    db_conn --> mysql
```
