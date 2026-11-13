import sys
from pathlib import Path

# Đảm bảo đường dẫn gốc của project có trong sys.path để import các module
GOC_DU_AN = Path(__file__).resolve().parent.parent
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from config.database import DatabaseConfig
from database.db_connection import quan_ly_ket_noi


def kiem_tra_ket_noi_va_cau_truc():
    """
    Kiểm tra toàn diện trạng thái kết nối, 7 bảng và các khóa ngoại trong neon_parking_db.
    """
    print("==================================================")
    print("    KIỂM TRA CƠ SỞ DỮ LIỆU: NEON_PARKING_DB       ")
    print("==================================================")
    print(f"- Host: {DatabaseConfig.HOST}:{DatabaseConfig.PORT}")
    print(f"- User: {DatabaseConfig.USER}")
    print(f"- Database: {DatabaseConfig.DATABASE}")
    print("--------------------------------------------------")

    try:
        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)

            # 1. Kiểm tra phiên bản MySQL
            cursor.execute("SELECT VERSION() AS phien_ban")
            phien_ban = cursor.fetchone()["phien_ban"]
            print(f"[OK] Đã kết nối thành công tới MySQL Server: {phien_ban}")

            # 2. Kiểm tra danh sách 7 bảng bắt buộc
            cursor.execute("SHOW TABLES")
            cac_bang = [list(b.values())[0] for b in cursor.fetchall()]
            bang_yeu_cau = ["nguoi_dung", "bang_gia", "suc_chua", "xe", "ve_xe", "thanh_toan", "nhat_ky"]
            
            print(f"\n[DANH SÁCH BẢNG ({len(cac_bang)} bảng)]: {', '.join(cac_bang)}")
            tat_ca_co_du = True
            for b in bang_yeu_cau:
                co_mat = b in cac_bang
                bieu_tuong = "✓" if co_mat else "✗"
                print(f"  [{bieu_tuong}] Bảng: {b}")
                if not co_mat:
                    tat_ca_co_du = False

            if not tat_ca_co_du:
                print("\n[CẢNH BÁO] Chưa đủ 7 bảng! Hãy chạy: python database/init_db.py")
                return False

            # 3. Kiểm tra danh sách khóa ngoại (Foreign Keys)
            cursor.execute("""
                SELECT 
                    TABLE_NAME, 
                    CONSTRAINT_NAME, 
                    REFERENCED_TABLE_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
                ORDER BY TABLE_NAME
            """, (DatabaseConfig.DATABASE,))
            khoa_ngoai = cursor.fetchall()
            print(f"\n[QUAN HỆ KHÓA NGOẠI ({len(khoa_ngoai)} khóa ngoại)]: ")
            for kn in khoa_ngoai:
                print(f"  • {kn['TABLE_NAME']} -> {kn['REFERENCED_TABLE_NAME']} ({kn['CONSTRAINT_NAME']})")

            # 4. Kiểm tra dữ liệu bảng giá mặc định
            cursor.execute("SELECT loai_xe, ten_hien_thi, gia_ve FROM bang_gia")
            bang_gia = cursor.fetchall()
            print("\n[BẢNG GIÁ HIỆN TẠI]:")
            for item in bang_gia:
                print(f"  • {item['ten_hien_thi']} ({item['loai_xe']}): {item['gia_ve']:,} VNĐ")

            # 5. Kiểm tra sức chứa hiện tại
            cursor.execute("SELECT loai_xe, tong_cho FROM suc_chua")
            suc_chua = cursor.fetchall()
            print("\n[SỨC CHỨA BÃI XE]:")
            for item in suc_chua:
                print(f"  • {item['loai_xe']}: {item['tong_cho']} chỗ đỗ")

            # 6. Kiểm tra số lượng tài khoản Admin
            cursor.execute("SELECT COUNT(*) AS so_admin FROM nguoi_dung WHERE vai_tro = 'ADMIN'")
            so_admin = cursor.fetchone()["so_admin"]
            print(f"\n[TÀI KHOẢN ADMIN HIỆN TẠI]: {so_admin} tài khoản.")
            if so_admin == 0:
                print("  => Chưa có Admin nào. Chuẩn bị sẵn sàng cho bước tạo Admin đầu tiên!")

            cursor.close()
            print("\n==================================================")
            print("  TOÀN BỘ 7 BẢNG VÀ QUAN HỆ ĐÃ ĐƯỢC THIẾT KẾ ĐẠT CHUẨN!")
            print("==================================================")
            return True

    except Exception as e:
        print(f"\n[THẤT BẠI] Lỗi kết nối hoặc kiểm tra database: {e}")
        return False


if __name__ == "__main__":
    kiem_tra_ket_noi_va_cau_truc()
