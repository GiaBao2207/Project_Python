"""
NEON PARKING MANAGER - USER REPOSITORY
Tầng tương tác CSDL cho đối tượng Người dùng và Ghi nhật ký hoạt động.
Tách bạch hoàn toàn SQL khỏi tầng Giao diện và Nghiệp vụ.
"""

from typing import Optional, List
from database.db_connection import quan_ly_ket_noi
from models.nguoi_dung import NguoiDung


class UserRepository:
    """
    Thực hiện các thao tác CRUD trên bảng nguoi_dung và nhat_ky trong MySQL.
    Sử dụng parameterized query (%s) để chống SQL Injection 100%.
    """

    @staticmethod
    def dem_so_luong_admin() -> int:
        """
        Đếm tổng số tài khoản có vai trò ADMIN đang tồn tại trong hệ thống.
        """
        sql = "SELECT COUNT(*) AS so_admin FROM nguoi_dung WHERE vai_tro = 'ADMIN'"
        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()
            cursor.close()
            return int(row["so_admin"]) if row else 0

    @staticmethod
    def lay_theo_ten_dang_nhap(ten_dang_nhap: str) -> Optional[NguoiDung]:
        """
        Tìm kiếm người dùng theo tên đăng nhập duy nhất.
        """
        sql = """
            SELECT id, ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro, trang_thai, ngay_tao
            FROM nguoi_dung
            WHERE ten_dang_nhap = %s
            LIMIT 1
        """
        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (ten_dang_nhap.strip(),))
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return None
            return NguoiDung(
                id=row["id"],
                ten_dang_nhap=row["ten_dang_nhap"],
                mat_khau_hash=row["mat_khau_hash"],
                ho_ten=row["ho_ten"],
                vai_tro=row["vai_tro"],
                trang_thai=row["trang_thai"],
                ngay_tao=row["ngay_tao"]
            )

    @staticmethod
    def lay_theo_id(user_id: int) -> Optional[NguoiDung]:
        """
        Tìm kiếm người dùng theo ID khóa chính.
        """
        sql = """
            SELECT id, ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro, trang_thai, ngay_tao
            FROM nguoi_dung
            WHERE id = %s
            LIMIT 1
        """
        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return None
            return NguoiDung(
                id=row["id"],
                ten_dang_nhap=row["ten_dang_nhap"],
                mat_khau_hash=row["mat_khau_hash"],
                ho_ten=row["ho_ten"],
                vai_tro=row["vai_tro"],
                trang_thai=row["trang_thai"],
                ngay_tao=row["ngay_tao"]
            )

    @staticmethod
    def tao_admin_dau_tien(ten_dang_nhap: str, ho_ten: str, mat_khau_hash: str) -> bool:
        """
        Thiết lập Quản trị viên đầu tiên cho hệ thống.
        Đảm bảo an toàn đồng thời (concurrency-safe): khóa bảng trong transaction,
        chỉ cho phép tạo nếu chưa có bất kỳ Admin nào trước đó.
        """
        sql_check = "SELECT COUNT(*) AS so_admin FROM nguoi_dung WHERE vai_tro = 'ADMIN' FOR UPDATE"
        sql_insert = """
            INSERT INTO nguoi_dung (ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro, trang_thai)
            VALUES (%s, %s, %s, 'ADMIN', 'HOAT_DONG')
        """
        sql_log = """
            INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet)
            VALUES (%s, 'SETUP_ADMIN', %s)
        """

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                # 1. Khóa và kiểm tra xem đã có admin nào chưa
                cursor.execute(sql_check)
                row = cursor.fetchone()
                if row and row["so_admin"] > 0:
                    conn.rollback()
                    return False  # Đã có admin, từ chối tạo thêm bằng luồng first-setup

                # 2. Thêm admin mới
                cursor.execute(sql_insert, (ten_dang_nhap.strip(), mat_khau_hash, ho_ten.strip()))
                new_admin_id = cursor.lastrowid

                # 3. Ghi audit log
                cursor.execute(sql_log, (new_admin_id, f"Khởi tạo Quản trị viên đầu tiên: {ten_dang_nhap.strip()}"))

                conn.commit()
                return True
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    @staticmethod
    def doi_mat_khau(user_id: int, mat_khau_hash_moi: str) -> bool:
        """
        Cập nhật mật khẩu băm mới cho người dùng.
        """
        sql_update = "UPDATE nguoi_dung SET mat_khau_hash = %s WHERE id = %s"
        sql_log = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, 'DOI_MAT_KHAU', 'Đổi mật khẩu tài khoản')"

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_update, (mat_khau_hash_moi, user_id))
                cursor.execute(sql_log, (user_id,))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    @staticmethod
    def ghi_nhat_ky(id_nguoi_dung: Optional[int], hanh_dong: str, chi_tiet: str) -> None:
        """
        Ghi một sự kiện vào bảng nhat_ky phục vụ Audit trail.
        """
        sql = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, %s, %s)"
        try:
            with quan_ly_ket_noi(include_database=True, tu_dong_commit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (id_nguoi_dung, hanh_dong, chi_tiet))
                cursor.close()
        except Exception:
            # Ghi log không được làm sập luồng nghiệp vụ chính
            pass

    @staticmethod
    def lay_tat_ca_nguoi_dung(tu_khoa: Optional[str] = None) -> List[NguoiDung]:
        """
        Lấy danh sách tất cả tài khoản người dùng, hỗ trợ tìm kiếm theo tên đăng nhập hoặc họ tên.
        """
        sql = """
            SELECT id, ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro, trang_thai, ngay_tao
            FROM nguoi_dung
        """
        params = []
        if tu_khoa and tu_khoa.strip():
            sql += " WHERE ten_dang_nhap LIKE %s OR ho_ten LIKE %s"
            kw = f"%{tu_khoa.strip()}%"
            params.extend([kw, kw])

        sql += " ORDER BY id DESC"

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
            cursor.close()

            danh_sach = []
            for r in rows:
                danh_sach.append(NguoiDung(
                    id=r["id"],
                    ten_dang_nhap=r["ten_dang_nhap"],
                    mat_khau_hash=r["mat_khau_hash"],
                    ho_ten=r["ho_ten"],
                    vai_tro=r["vai_tro"],
                    trang_thai=r["trang_thai"],
                    ngay_tao=r["ngay_tao"]
                ))
            return danh_sach

    @staticmethod
    def tao_nhan_vien(
        ten_dang_nhap: str,
        ho_ten: str,
        mat_khau_hash: str,
        id_admin: Optional[int]
    ) -> Tuple[bool, str, Optional[int]]:
        """
        Tạo tài khoản Nhân viên mới trong MySQL bằng Transaction.
        """
        sql_check = "SELECT id FROM nguoi_dung WHERE ten_dang_nhap = %s LIMIT 1"
        sql_insert = """
            INSERT INTO nguoi_dung (ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro, trang_thai)
            VALUES (%s, %s, %s, 'NHAN_VIEN', 'HOAT_DONG')
        """
        sql_log = """
            INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet)
            VALUES (%s, 'TAO_NHAN_VIEN', %s)
        """
        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql_check, (ten_dang_nhap.strip(),))
                if cursor.fetchone():
                    conn.rollback()
                    return False, f"Tên đăng nhập '{ten_dang_nhap}' đã tồn tại trong hệ thống!", None

                cursor.execute(sql_insert, (ten_dang_nhap.strip(), mat_khau_hash, ho_ten.strip()))
                new_id = cursor.lastrowid

                cursor.execute(sql_log, (id_admin, f"Tạo tài khoản nhân viên mới: {ten_dang_nhap.strip()} (ID: {new_id})"))
                conn.commit()
                return True, "Tạo tài khoản nhân viên thành công!", new_id
            except Exception as e:
                conn.rollback()
                return False, f"Lỗi cơ sở dữ liệu khi tạo nhân viên: {e}", None
            finally:
                cursor.close()

    @staticmethod
    def cap_nhat_thong_tin(
        user_id: int,
        ho_ten: str,
        ten_dang_nhap: str,
        id_admin: Optional[int]
    ) -> Tuple[bool, str]:
        """
        Cập nhật họ tên và tên đăng nhập của người dùng.
        """
        sql_check = "SELECT id FROM nguoi_dung WHERE ten_dang_nhap = %s AND id != %s LIMIT 1"
        sql_update = "UPDATE nguoi_dung SET ho_ten = %s, ten_dang_nhap = %s WHERE id = %s"
        sql_log = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, 'CAP_NHAT_NHAN_VIEN', %s)"

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql_check, (ten_dang_nhap.strip(), user_id))
                if cursor.fetchone():
                    conn.rollback()
                    return False, f"Tên đăng nhập '{ten_dang_nhap}' đã được sử dụng bởi tài khoản khác!"

                cursor.execute(sql_update, (ho_ten.strip(), ten_dang_nhap.strip(), user_id))
                cursor.execute(sql_log, (id_admin, f"Cập nhật thông tin tài khoản ID {user_id}: {ten_dang_nhap.strip()} - {ho_ten.strip()}"))
                conn.commit()
                return True, "Cập nhật thông tin tài khoản thành công!"
            except Exception as e:
                conn.rollback()
                return False, f"Lỗi cơ sở dữ liệu khi cập nhật: {e}"
            finally:
                cursor.close()

    @staticmethod
    def cap_nhat_trang_thai(
        user_id: int,
        trang_thai: str,
        id_admin: Optional[int]
    ) -> Tuple[bool, str]:
        """
        Khóa hoặc Mở khóa tài khoản người dùng ('HOAT_DONG' hoặc 'KHOA').
        """
        sql_update = "UPDATE nguoi_dung SET trang_thai = %s WHERE id = %s"
        sql_log = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, %s, %s)"

        hanh_dong = "KHOA_TAI_KHOAN" if trang_thai == "KHOA" else "MO_KHOA_TAI_KHOAN"
        mo_ta = f"{'Khóa' if trang_thai == 'KHOA' else 'Mở khóa'} tài khoản ID {user_id}"

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_update, (trang_thai, user_id))
                cursor.execute(sql_log, (id_admin, hanh_dong, mo_ta))
                conn.commit()
                return True, f"{mo_ta} thành công!"
            except Exception as e:
                conn.rollback()
                return False, f"Lỗi cơ sở dữ liệu khi đổi trạng thái: {e}"
            finally:
                cursor.close()

    @staticmethod
    def dat_lai_mat_khau_nhan_vien(
        user_id: int,
        mat_khau_hash_moi: str,
        id_admin: Optional[int]
    ) -> Tuple[bool, str]:
        """
        Admin đặt lại mật khẩu cho nhân viên.
        """
        sql_update = "UPDATE nguoi_dung SET mat_khau_hash = %s WHERE id = %s"
        sql_log = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, 'RESET_MAT_KHAU', %s)"

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_update, (mat_khau_hash_moi, user_id))
                cursor.execute(sql_log, (id_admin, f"Admin đặt lại mật khẩu cho tài khoản ID {user_id}"))
                conn.commit()
                return True, "Đặt lại mật khẩu cho nhân viên thành công!"
            except Exception as e:
                conn.rollback()
                return False, f"Lỗi cơ sở dữ liệu khi đặt lại mật khẩu: {e}"
            finally:
                cursor.close()

    @staticmethod
    def lay_nhat_ky(
        tu_ngay: Optional[str] = None,
        den_ngay: Optional[str] = None,
        id_nguoi_dung: Optional[int] = None,
        hanh_dong: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[dict], int]:
        """
        Truy vấn danh sách nhật ký hoạt động có bộ lọc và phân trang.
        Trả về Tuple(danh_sach_nhat_ky, tong_so_dong).
        """
        where_clauses = ["1=1"]
        params = []

        if tu_ngay and tu_ngay.strip():
            where_clauses.append("nk.thoi_gian >= %s")
            params.append(f"{tu_ngay.strip()} 00:00:00")

        if den_ngay and den_ngay.strip():
            where_clauses.append("nk.thoi_gian <= %s")
            params.append(f"{den_ngay.strip()} 23:59:59")

        if id_nguoi_dung is not None and id_nguoi_dung > 0:
            where_clauses.append("nk.id_nguoi_dung = %s")
            params.append(id_nguoi_dung)

        if hanh_dong and hanh_dong.strip() and hanh_dong != "ALL":
            where_clauses.append("nk.hanh_dong = %s")
            params.append(hanh_dong.strip())

        where_sql = " AND ".join(where_clauses)

        sql_count = f"SELECT COUNT(*) AS tong FROM nhat_ky nk WHERE {where_sql}"
        sql_data = f"""
            SELECT 
                nk.id,
                nk.id_nguoi_dung,
                nd.ten_dang_nhap,
                nd.ho_ten,
                nd.vai_tro,
                nk.hanh_dong,
                nk.chi_tiet,
                nk.thoi_gian
            FROM nhat_ky nk
            LEFT JOIN nguoi_dung nd ON nk.id_nguoi_dung = nd.id
            WHERE {where_sql}
            ORDER BY nk.id DESC
            LIMIT %s OFFSET %s
        """

        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            # 1. Đếm tổng số
            cursor.execute(sql_count, tuple(params))
            total_row = cursor.fetchone()
            total = int(total_row["tong"]) if total_row else 0

            # 2. Lấy dữ liệu phân trang
            data_params = list(params) + [limit, offset]
            cursor.execute(sql_data, tuple(data_params))
            rows = cursor.fetchall()
            cursor.close()
            return rows, total

    @staticmethod
    def lay_danh_sach_loai_hanh_dong() -> List[str]:
        """
        Lấy danh sách các loại hành động độc nhất trong bảng nhat_ky để hiển thị vào Combobox lọc.
        """
        sql = "SELECT DISTINCT hanh_dong FROM nhat_ky WHERE hanh_dong IS NOT NULL ORDER BY hanh_dong ASC"
        with quan_ly_ket_noi(include_database=True) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return [r["hanh_dong"] for r in rows if r["hanh_dong"]]
