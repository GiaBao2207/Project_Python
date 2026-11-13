-- ====================================================================
-- DỰ ÁN: NEON PARKING MANAGER - HỆ THỐNG QUẢN LÝ BÃI GIỮ XE
-- PHÂN HỆ: CƠ SỞ DỮ LIỆU MYSQL (GIAI ĐOẠN 1)
-- TƯƠNG THÍCH: MySQL 8.x / MySQL 9.x (Đã tối ưu cho MySQL Server 9.7.1)
-- NGUYÊN TẮC: AN TOÀN DỮ LIỆU - KHÔNG DROP DATABASE / KHÔNG DROP TABLE
-- BẢNG MÃ: utf8mb4_unicode_ci (Hỗ trợ tiếng Việt đầy đủ)
-- ====================================================================

-- 1. Tạo Database nếu chưa tồn tại
CREATE DATABASE IF NOT EXISTS neon_parking_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE neon_parking_db;

-- ====================================================================
-- BẢNG 1: nguoi_dung (Quản lý tài khoản, mật khẩu Argon2id & phân quyền)
-- ====================================================================
CREATE TABLE IF NOT EXISTS nguoi_dung (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_dang_nhap VARCHAR(50) NOT NULL UNIQUE,
    mat_khau_hash VARCHAR(255) NOT NULL COMMENT 'Chuỗi băm an toàn chuẩn Argon2id',
    ho_ten VARCHAR(100) NOT NULL,
    vai_tro ENUM('ADMIN', 'NHAN_VIEN') NOT NULL DEFAULT 'NHAN_VIEN',
    trang_thai ENUM('HOAT_DONG', 'KHOA') NOT NULL DEFAULT 'HOAT_DONG',
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nguoi_dung_vai_tro (vai_tro),
    INDEX idx_nguoi_dung_trang_thai (trang_thai)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ghi chú: Tuyệt đối KHÔNG INSERT tài khoản Admin mặc định để đảm bảo an toàn.
-- Quy trình thiết lập Admin đầu tiên sẽ được thực hiện an toàn qua ứng dụng.

-- ====================================================================
-- BẢNG 2: bang_gia (Đơn giá gửi xe theo từng loại phương tiện)
-- ====================================================================
CREATE TABLE IF NOT EXISTS bang_gia (
    loai_xe VARCHAR(20) PRIMARY KEY COMMENT 'Mã loại xe: XeDap, XeMay, OTo',
    ten_hien_thi VARCHAR(50) NOT NULL COMMENT 'Tên tiếng Việt hiển thị',
    gia_ve INT NOT NULL CHECK (gia_ve >= 0) COMMENT 'Đơn giá gửi xe (VNĐ)',
    ngay_cap_nhat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu bảng giá mặc định ban đầu (Chỉ thêm nếu chưa có, không ghi đè giá đã sửa)
-- Cú pháp MySQL 8.0.20+ và MySQL 9.x: Sử dụng row alias `AS hang_moi` 
-- thay thế cho hàm VALUES() đã bị deprecated trong MySQL 9.7.1.
INSERT INTO bang_gia (loai_xe, ten_hien_thi, gia_ve)
VALUES
    ('XeDap', 'Xe đạp', 2000),
    ('XeMay', 'Xe máy', 5000),
    ('OTo', 'Ô tô', 20000) AS hang_moi
ON DUPLICATE KEY UPDATE ten_hien_thi = hang_moi.ten_hien_thi;

-- ====================================================================
-- BẢNG 3: suc_chua (Tổng số chỗ đỗ quy định cho từng loại phương tiện)
-- ====================================================================
CREATE TABLE IF NOT EXISTS suc_chua (
    loai_xe VARCHAR(20) PRIMARY KEY,
    tong_cho INT NOT NULL CHECK (tong_cho >= 0) COMMENT 'Tổng sức chứa tối đa',
    ngay_cap_nhat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_suc_chua_bang_gia FOREIGN KEY (loai_xe) 
        REFERENCES bang_gia (loai_xe) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu sức chứa mặc định ban đầu (Chỉ thêm nếu chưa có, không ghi đè sức chứa đã sửa)
INSERT INTO suc_chua (loai_xe, tong_cho)
VALUES
    ('XeDap', 50),
    ('XeMay', 150),
    ('OTo', 30) AS hang_moi
ON DUPLICATE KEY UPDATE loai_xe = hang_moi.loai_xe;

-- ====================================================================
-- BẢNG 4: xe (Danh mục phương tiện & chủ xe)
-- ====================================================================
-- Quy định:
-- - bien_so: Cho phép NULL đối với XeDap (không yêu cầu biển số).
--            Với XeMay và OTo, tính hợp lệ (bắt buộc, không rỗng) được kiểm soát chặt chẽ ở tầng Service Python.
-- - ma_dinh_danh: Khóa duy nhất. Với XeMay/OTo là biển số, với XeDap là mã thẻ riêng (VD: XD-001).
CREATE TABLE IF NOT EXISTS xe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_dinh_danh VARCHAR(50) NOT NULL UNIQUE COMMENT 'Biển số xe hoặc mã định danh xe đạp',
    bien_so VARCHAR(30) NULL COMMENT 'Biển số xe (kiểm tra bắt buộc với XeMay/OTo ở Service Layer; NULL với XeDap)',
    loai_xe VARCHAR(20) NOT NULL,
    chu_xe VARCHAR(100) NOT NULL,
    ngay_dang_ky DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_xe_loai_xe FOREIGN KEY (loai_xe) 
        REFERENCES bang_gia (loai_xe) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_xe_bien_so (bien_so),
    INDEX idx_xe_loai_xe (loai_xe)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- BẢNG 5: ve_xe (Quản lý lượt vào/ra của phương tiện)
-- ====================================================================
-- Thiết kế tối ưu & chuẩn hóa (3NF):
-- 1. Loại bỏ lưu trùng ma_dinh_danh và loai_xe: Thông tin định danh và loại xe được
--    quản lý tập trung tại bảng 'xe', truy vấn qua khóa ngoại id_xe để bảo đảm tính nhất quán.
-- 2. don_gia_ap_dung: Chụp ảnh đơn giá tại thời điểm tiếp nhận (snapshot bảo toàn kế toán).
-- 3. id_xe_dang_gui (Generated Column + UNIQUE): Chống một xe có 2 vé trạng thái 'Dang gui' cùng lúc.
CREATE TABLE IF NOT EXISTS ve_xe (
    ma_ve VARCHAR(20) PRIMARY KEY,
    id_xe INT NOT NULL,
    don_gia_ap_dung INT NOT NULL CHECK (don_gia_ap_dung >= 0) COMMENT 'Snapshot giá tại thời điểm nhận xe',
    gio_vao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    gio_ra DATETIME NULL,
    trang_thai ENUM('Dang gui', 'Da thanh toan', 'Da huy') NOT NULL DEFAULT 'Dang gui',
    id_nhan_vien_vao INT NULL COMMENT 'Nhân viên phụ trách tiếp nhận xe',
    id_nhan_vien_ra INT NULL COMMENT 'Nhân viên phụ trách lúc xe ra',
    
    -- Cột sinh tự động (Virtual Generated Column) để chống 1 id_xe có 2 vé 'Dang gui' cùng lúc
    id_xe_dang_gui INT GENERATED ALWAYS AS (
        CASE WHEN trang_thai = 'Dang gui' THEN id_xe ELSE NULL END
    ) VIRTUAL,
    CONSTRAINT uq_xe_dang_gui UNIQUE (id_xe_dang_gui),

    CONSTRAINT fk_ve_xe_xe FOREIGN KEY (id_xe) 
        REFERENCES xe (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ve_xe_nv_vao FOREIGN KEY (id_nhan_vien_vao) 
        REFERENCES nguoi_dung (id) ON DELETE SET NULL,
    CONSTRAINT fk_ve_xe_nv_ra FOREIGN KEY (id_nhan_vien_ra) 
        REFERENCES nguoi_dung (id) ON DELETE SET NULL,
        
    INDEX idx_ve_xe_id_xe (id_xe),
    INDEX idx_ve_xe_trang_thai (trang_thai),
    INDEX idx_ve_xe_gio_vao (gio_vao),
    INDEX idx_ve_xe_gio_ra (gio_ra)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- BẢNG 6: thanh_toan (Dữ liệu thanh toán tách riêng, quan hệ 1-1 với vé)
-- ====================================================================
-- Ràng buộc:
-- - ma_ve là UNIQUE để CHỐNG TẠO TRÙNG THANH TOÁN cho cùng 1 vé xe.
CREATE TABLE IF NOT EXISTS thanh_toan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_ve VARCHAR(20) NOT NULL UNIQUE COMMENT 'Khóa ngoại liên kết 1-1 với ve_xe',
    so_tien INT NOT NULL CHECK (so_tien >= 0) COMMENT 'Số tiền thực tế thanh toán',
    phuong_thuc ENUM('TIEN_MAT', 'CHUYEN_KHOAN') NOT NULL DEFAULT 'TIEN_MAT',
    thoi_gian_thanh_toan DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_nhan_vien_thu INT NULL COMMENT 'Nhân viên trực tiếp thu tiền',
    ghi_chu VARCHAR(255) NULL,
    CONSTRAINT fk_thanh_toan_ve FOREIGN KEY (ma_ve) 
        REFERENCES ve_xe (ma_ve) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_thanh_toan_nv FOREIGN KEY (id_nhan_vien_thu) 
        REFERENCES nguoi_dung (id) ON DELETE SET NULL,
    INDEX idx_thanh_toan_thoi_gian (thoi_gian_thanh_toan),
    INDEX idx_thanh_toan_phuong_thuc (phuong_thuc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- BẢNG 7: nhat_ky (Audit trail - Ghi nhận lịch sử hoạt động hệ thống)
-- ====================================================================
CREATE TABLE IF NOT EXISTS nhat_ky (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_nguoi_dung INT NULL,
    hanh_dong VARCHAR(100) NOT NULL COMMENT 'Hành động: TIEP_NHAN_XE, XE_RA, CAP_NHAT_GIA...',
    chi_tiet TEXT NULL,
    thoi_gian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_nhat_ky_nguoi_dung FOREIGN KEY (id_nguoi_dung) 
        REFERENCES nguoi_dung (id) ON DELETE SET NULL,
    INDEX idx_nhat_ky_thoi_gian (thoi_gian)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
