import sys
from pathlib import Path

# Đảm bảo đường dẫn gốc của project có trong sys.path để import các module
GOC_DU_AN = Path(__file__).resolve().parent.parent
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from config.database import DatabaseConfig
from database.db_connection import lay_ket_noi


def khoi_tao_database():
    """
    Đọc file schema.sql và thực thi trên MySQL Server.
    Tự động tạo cơ sở dữ liệu neon_parking_db và 7 bảng liên quan.
    Tuân thủ an toàn: KHÔNG DROP DATABASE, KHÔNG DROP TABLE.
    """
    duong_dan_sql = Path(__file__).resolve().parent / "schema.sql"
    if not duong_dan_sql.exists():
        print(f"[LỖI] Không tìm thấy file schema tại: {duong_dan_sql}")
        return False

    with open(duong_dan_sql, "r", encoding="utf-8") as f:
        noi_dung_sql = f.read()

    print("==================================================")
    print("  KHỞI TẠO CƠ SỞ DỮ LIỆU MYSQL: NEON_PARKING_DB  ")
    print("==================================================")
    print(f"- Máy chủ: {DatabaseConfig.HOST}:{DatabaseConfig.PORT}")
    print(f"- Người dùng: {DatabaseConfig.USER}")
    print(f"- Tên CSDL: {DatabaseConfig.DATABASE}")
    print("--------------------------------------------------")

    try:
        # Bước 1: Kết nối server chung (include_database=False để có thể CREATE DATABASE)
        conn = lay_ket_noi(include_database=False)
        cursor = conn.cursor()

        # Bước 2: Tách và chạy từng câu lệnh SQL từ schema.sql
        cau_lenh_list = [
            cau.strip() for cau in noi_dung_sql.split(";")
            if cau.strip() and not cau.strip().startswith("--")
        ]

        for cau_lenh in cau_lenh_list:
            cursor.execute(cau_lenh)

        conn.commit()
        cursor.close()
        conn.close()

        print("[THÀNH CÔNG] Đã khởi tạo hoàn tất CSDL và 7 bảng chuẩn:")
        print("  1. 'nguoi_dung'  : Tài khoản, phân quyền, mật khẩu Argon2id")
        print("  2. 'bang_gia'    : Đơn giá từng loại xe (XeDap, XeMay, OTo)")
        print("  3. 'suc_chua'    : Sức chứa tối đa từng loại xe")
        print("  4. 'xe'          : Danh mục phương tiện (mã định danh xe đạp / biển số)")
        print("  5. 've_xe'       : Vé xe, snapshot đơn giá, chống 1 xe 2 vé đang gửi")
        print("  6. 'thanh_toan'  : Tách dữ liệu thanh toán 1-1, chống trùng thanh toán")
        print("  7. 'nhat_ky'     : Lịch sử thao tác (Audit trail)")
        print("==================================================")
        return True

    except Exception as e:
        print(f"\n[THẤT BẠI] Lỗi trong quá trình khởi tạo database: {e}")
        print("\nGợi ý khắc phục:")
        print("1. Kiểm tra lại mật khẩu MySQL trong file .env")
        print("2. Đảm bảo dịch vụ MySQL đang chạy (VD: MySQLGiaBao trong Windows Services)")
        return False


if __name__ == "__main__":
    khoi_tao_database()
