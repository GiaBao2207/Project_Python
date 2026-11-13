"""
NEON PARKING MANAGER - VEHICLE REPOSITORY
Tầng tương tác CSDL cho xe, vé xe và thanh toán.
Tất cả SQL dùng parameterized query (%s) chống SQL Injection.
Transaction (commit/rollback) bảo toàn tính toàn vẹn dữ liệu.
"""

from typing import Optional, List, Dict, Any
from database.db_connection import quan_ly_ket_noi


class VehicleRepository:
    """
    Thực hiện các thao tác CRUD trên bảng xe, ve_xe và thanh_toan.
    """

    # ─────────────────────────── BẢNG GIÁ & SỨC CHỨA ───────────────────────────

    @staticmethod
    def lay_bang_gia() -> List[Dict[str, Any]]:
        """Trả về danh sách tất cả loại xe và đơn giá hiện hành."""
        sql = "SELECT loai_xe, ten_hien_thi, gia_ve FROM bang_gia"
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            return rows

    @staticmethod
    def lay_suc_chua() -> Dict[str, int]:
        """
        Trả về dict {loai_xe: tong_cho} cho toàn bộ các loại xe.
        Ví dụ: {'XeDap': 50, 'XeMay': 150, 'OTo': 30}
        """
        sql = "SELECT loai_xe, tong_cho FROM suc_chua"
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            return {row["loai_xe"]: row["tong_cho"] for row in rows}

    @staticmethod
    def dem_xe_dang_gui(loai_xe: str) -> int:
        """
        Đếm số phương tiện đang gửi (trạng thái 'Dang gui') theo loại xe.
        Dùng để kiểm tra sức chứa còn trống trước khi tiếp nhận.
        """
        sql = """
            SELECT COUNT(*) AS so_luong
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            WHERE x.loai_xe = %s AND vx.trang_thai = 'Dang gui'
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (loai_xe,))
            row = cur.fetchone()
            cur.close()
            return int(row["so_luong"]) if row else 0

    @staticmethod
    def lay_chi_tiet_bang_gia() -> List[Dict[str, Any]]:
        """Lấy danh sách đầy đủ thông tin bảng giá xe."""
        sql = "SELECT loai_xe, ten_hien_thi, gia_ve, ngay_cap_nhat FROM bang_gia ORDER BY gia_ve ASC"
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            return rows

    @staticmethod
    def cap_nhat_gia_ve(loai_xe: str, gia_moi: int, id_admin: Optional[int]) -> Tuple[bool, str]:
        """
        Cập nhật đơn giá gửi xe trong bảng bang_gia.
        Ghi nhật ký hệ thống. Không ảnh hưởng đến các vé đã được phát hành trước đó.
        """
        sql_update = "UPDATE bang_gia SET gia_ve = %s WHERE loai_xe = %s"
        sql_log = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, 'CAP_NHAT_GIA', %s)"

        with quan_ly_ket_noi() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql_update, (gia_moi, loai_xe))
                cur.execute(sql_log, (id_admin, f"Thay đổi giá vé {loai_xe} thành {gia_moi:,} VNĐ"))
                conn.commit()
                return True, f"Cập nhật giá vé cho {loai_xe} thành công!"
            except Exception as e:
                conn.rollback()
                return False, f"Lỗi cơ sở dữ liệu khi cập nhật giá: {e}"
            finally:
                cur.close()

    @staticmethod
    def lay_chi_tiet_suc_chua() -> List[Dict[str, Any]]:
        """
        Lấy thông tin sức chứa chi tiết: tổng chỗ, số xe đang gửi thực tế, chỗ trống còn lại.
        """
        sql = """
            SELECT 
                sc.loai_xe,
                bg.ten_hien_thi,
                sc.tong_cho,
                COALESCE(dg.so_luong, 0) AS dang_gui,
                GREATEST(0, sc.tong_cho - COALESCE(dg.so_luong, 0)) AS con_trong,
                sc.ngay_cap_nhat
            FROM suc_chua sc
            JOIN bang_gia bg ON sc.loai_xe = bg.loai_xe
            LEFT JOIN (
                SELECT x.loai_xe, COUNT(*) AS so_luong
                FROM ve_xe vx
                JOIN xe x ON vx.id_xe = x.id
                WHERE vx.trang_thai = 'Dang gui'
                GROUP BY x.loai_xe
            ) dg ON sc.loai_xe = dg.loai_xe
            ORDER BY sc.tong_cho DESC
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            return rows

    @staticmethod
    def cap_nhat_suc_chua(loai_xe: str, tong_cho_moi: int, id_admin: Optional[int]) -> Tuple[bool, str]:
        """
        Cập nhật tổng số chỗ gửi xe trong bảng suc_chua.
        Ghi nhật ký hệ thống.
        """
        sql_update = "UPDATE suc_chua SET tong_cho = %s WHERE loai_xe = %s"
        sql_log = "INSERT INTO nhat_ky (id_nguoi_dung, hanh_dong, chi_tiet) VALUES (%s, 'CAP_NHAT_SUC_CHUA', %s)"

        with quan_ly_ket_noi() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql_update, (tong_cho_moi, loai_xe))
                cur.execute(sql_log, (id_admin, f"Thay đổi sức chứa {loai_xe} thành {tong_cho_moi} chỗ"))
                conn.commit()
                return True, f"Cập nhật sức chứa cho {loai_xe} thành công!"
            except Exception as e:
                conn.rollback()
                return False, f"Lỗi cơ sở dữ liệu khi cập nhật sức chứa: {e}"
            finally:
                cur.close()

    # ─────────────────────────── BẢNG XE ───────────────────────────

    @staticmethod
    def tim_xe_theo_ma_dinh_danh(ma_dinh_danh: str) -> Optional[Dict[str, Any]]:
        """Tìm xe theo mã định danh duy nhất (biển số hoặc mã thẻ XeDap)."""
        sql = """
            SELECT id, ma_dinh_danh, bien_so, loai_xe, chu_xe, ngay_dang_ky
            FROM xe WHERE ma_dinh_danh = %s LIMIT 1
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (ma_dinh_danh.strip().upper(),))
            row = cur.fetchone()
            cur.close()
            return row

    @staticmethod
    def them_xe(ma_dinh_danh: str, bien_so: Optional[str],
                loai_xe: str, chu_xe: str) -> int:
        """
        Thêm xe mới vào bảng xe.
        Trả về id_xe vừa tạo.
        bien_so có thể là None đối với xe đạp.
        """
        sql = """
            INSERT INTO xe (ma_dinh_danh, bien_so, loai_xe, chu_xe)
            VALUES (%s, %s, %s, %s)
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (
                    ma_dinh_danh.strip().upper(),
                    bien_so.strip().upper() if bien_so else None,
                    loai_xe,
                    chu_xe.strip()
                ))
                new_id = cur.lastrowid
                conn.commit()
                return new_id
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()

    @staticmethod
    def lay_danh_sach_xe(loai_xe: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả xe, có thể lọc theo loại xe.
        Bao gồm thông tin trạng thái hiện tại (đang gửi hay không).
        """
        if loai_xe:
            sql = """
                SELECT x.id, x.ma_dinh_danh, x.bien_so, x.loai_xe,
                       x.chu_xe, x.ngay_dang_ky,
                       bg.ten_hien_thi AS ten_loai_xe,
                       (SELECT vx.ma_ve FROM ve_xe vx
                        WHERE vx.id_xe = x.id AND vx.trang_thai = 'Dang gui'
                        LIMIT 1) AS ma_ve_dang_gui
                FROM xe x
                JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
                WHERE x.loai_xe = %s
                ORDER BY x.ngay_dang_ky DESC
            """
            params = (loai_xe,)
        else:
            sql = """
                SELECT x.id, x.ma_dinh_danh, x.bien_so, x.loai_xe,
                       x.chu_xe, x.ngay_dang_ky,
                       bg.ten_hien_thi AS ten_loai_xe,
                       (SELECT vx.ma_ve FROM ve_xe vx
                        WHERE vx.id_xe = x.id AND vx.trang_thai = 'Dang gui'
                        LIMIT 1) AS ma_ve_dang_gui
                FROM xe x
                JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
                ORDER BY x.ngay_dang_ky DESC
            """
            params = ()

        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, params)
            rows = cur.fetchall()
            cur.close()
            return rows

    # ─────────────────────────── BẢNG VÉ XE ───────────────────────────

    @staticmethod
    def kiem_tra_xe_dang_gui(id_xe: int) -> bool:
        """Kiểm tra xem xe này có đang có vé trạng thái 'Dang gui' không."""
        sql = """
            SELECT COUNT(*) AS so_ve
            FROM ve_xe WHERE id_xe = %s AND trang_thai = 'Dang gui'
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (id_xe,))
            row = cur.fetchone()
            cur.close()
            return int(row["so_ve"]) > 0 if row else False

    @staticmethod
    def tao_ve_tiep_nhan(ma_ve: str, id_xe: int, don_gia_ap_dung: int,
                         id_nhan_vien: Optional[int]) -> bool:
        """
        Tạo vé tiếp nhận xe (INSERT vào ve_xe).
        Dùng trong MySQL Transaction cùng với cập nhật sức chứa nếu cần.
        Trả về True nếu thành công.
        """
        sql = """
            INSERT INTO ve_xe (ma_ve, id_xe, don_gia_ap_dung, id_nhan_vien_vao)
            VALUES (%s, %s, %s, %s)
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (ma_ve, id_xe, don_gia_ap_dung, id_nhan_vien))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()

    @staticmethod
    def lay_ve_dang_gui(id_xe: int) -> Optional[Dict[str, Any]]:
        """Lấy vé đang gửi hiện tại của một xe theo id_xe."""
        sql = """
            SELECT vx.ma_ve, vx.id_xe, vx.don_gia_ap_dung,
                   vx.gio_vao, vx.trang_thai,
                   x.ma_dinh_danh, x.bien_so, x.loai_xe, x.chu_xe,
                   bg.ten_hien_thi AS ten_loai_xe
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            WHERE vx.id_xe = %s AND vx.trang_thai = 'Dang gui'
            LIMIT 1
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (id_xe,))
            row = cur.fetchone()
            cur.close()
            return row

    @staticmethod
    def lay_ve_theo_ma(ma_ve: str) -> Optional[Dict[str, Any]]:
        """Lấy chi tiết vé theo mã vé kèm thông tin thanh toán và nhân viên."""
        sql = """
            SELECT vx.ma_ve, vx.id_xe, vx.don_gia_ap_dung,
                   vx.gio_vao, vx.gio_ra, vx.trang_thai,
                   vx.id_nhan_vien_vao, vx.id_nhan_vien_ra,
                   x.ma_dinh_danh, x.bien_so, x.loai_xe, x.chu_xe,
                   bg.ten_hien_thi AS ten_loai_xe,
                   tt.so_tien, tt.phuong_thuc, tt.thoi_gian_thanh_toan, tt.ghi_chu,
                   nv_vao.ho_ten AS ten_nv_vao,
                   nv_ra.ho_ten AS ten_nv_ra
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            LEFT JOIN thanh_toan tt ON tt.ma_ve = vx.ma_ve
            LEFT JOIN nguoi_dung nv_vao ON nv_vao.id = vx.id_nhan_vien_vao
            LEFT JOIN nguoi_dung nv_ra ON nv_ra.id = vx.id_nhan_vien_ra
            WHERE vx.ma_ve = %s
            LIMIT 1
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (ma_ve.strip().upper(),))
            row = cur.fetchone()
            cur.close()
            return row

    @staticmethod
    def lay_danh_sach_ve(
        trang_thai: Optional[str] = None,
        tu_khoa: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách vé xe kết hợp thông tin xe, bảng giá và thanh toán.
        Hỗ trợ lọc theo trạng thái và tìm kiếm theo từ khóa (biển số, mã vé, chủ xe).
        """
        conditions = []
        params = []

        if trang_thai and trang_thai not in ("Tat ca", "Tất cả", "ALL"):
            conditions.append("vx.trang_thai = %s")
            params.append(trang_thai)

        if tu_khoa and tu_khoa.strip():
            kw = f"%{tu_khoa.strip().upper()}%"
            conditions.append("(vx.ma_ve LIKE %s OR UPPER(x.ma_dinh_danh) LIKE %s OR UPPER(IFNULL(x.bien_so, '')) LIKE %s OR UPPER(x.chu_xe) LIKE %s)")
            params.extend([kw, kw, kw, kw])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        sql = f"""
            SELECT vx.ma_ve, vx.id_xe, vx.don_gia_ap_dung,
                   vx.gio_vao, vx.gio_ra, vx.trang_thai,
                   vx.id_nhan_vien_vao, vx.id_nhan_vien_ra,
                   x.ma_dinh_danh, x.bien_so, x.loai_xe, x.chu_xe,
                   bg.ten_hien_thi AS ten_loai_xe,
                   tt.so_tien, tt.phuong_thuc, tt.thoi_gian_thanh_toan, tt.ghi_chu,
                   nv_vao.ho_ten AS ten_nv_vao,
                   nv_ra.ho_ten AS ten_nv_ra
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            LEFT JOIN thanh_toan tt ON tt.ma_ve = vx.ma_ve
            LEFT JOIN nguoi_dung nv_vao ON nv_vao.id = vx.id_nhan_vien_vao
            LEFT JOIN nguoi_dung nv_ra ON nv_ra.id = vx.id_nhan_vien_ra
            {where_clause}
            ORDER BY vx.gio_vao DESC
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            cur.close()
            return rows

    @staticmethod
    def lay_danh_sach_xe_dang_gui(
        tu_khoa: Optional[str] = None,
        loai_xe: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách tất cả xe đang được gửi trong bãi (trạng thái 'Dang gui').
        Hỗ trợ tìm kiếm theo mã vé, biển số, mã định danh xe đạp, tên chủ xe.
        Hỗ trợ lọc theo loại xe và phân trang (limit, offset).
        Dùng cho bảng dữ liệu chính của module Quản lý Xe.
        """
        conditions = ["vx.trang_thai = 'Dang gui'"]
        params: List[Any] = []

        if loai_xe and loai_xe not in ("Tat ca", "Tất cả", "ALL"):
            conditions.append("x.loai_xe = %s")
            params.append(loai_xe)

        if tu_khoa and tu_khoa.strip():
            kw = f"%{tu_khoa.strip()}%"
            conditions.append(
                "(vx.ma_ve LIKE %s OR x.ma_dinh_danh LIKE %s OR IFNULL(x.bien_so, '') LIKE %s OR x.chu_xe LIKE %s)"
            )
            params.extend([kw, kw, kw, kw])

        where_clause = "WHERE " + " AND ".join(conditions)
        limit_clause = ""
        if limit is not None and limit > 0:
            if offset is not None and offset > 0:
                limit_clause = f" LIMIT {int(limit)} OFFSET {int(offset)}"
            else:
                limit_clause = f" LIMIT {int(limit)}"

        sql = f"""
            SELECT vx.ma_ve, vx.gio_vao, vx.don_gia_ap_dung,
                   x.id AS id_xe, x.ma_dinh_danh, x.bien_so,
                   x.loai_xe, x.chu_xe,
                   bg.ten_hien_thi AS ten_loai_xe
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            {where_clause}
            ORDER BY vx.gio_vao DESC
            {limit_clause}
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            cur.close()
            return rows

    @staticmethod
    def dem_so_luong_xe_dang_gui(
        tu_khoa: Optional[str] = None,
        loai_xe: Optional[str] = None
    ) -> int:
        """
        Đếm tổng số xe đang gửi thỏa mãn từ khóa tìm kiếm và bộ lọc loại xe (không phân trang).
        Phục vụ tính tổng số trang và hiển thị số lượng trên giao diện.
        """
        conditions = ["vx.trang_thai = 'Dang gui'"]
        params: List[Any] = []

        if loai_xe and loai_xe not in ("Tat ca", "Tất cả", "ALL"):
            conditions.append("x.loai_xe = %s")
            params.append(loai_xe)

        if tu_khoa and tu_khoa.strip():
            kw = f"%{tu_khoa.strip()}%"
            conditions.append(
                "(vx.ma_ve LIKE %s OR x.ma_dinh_danh LIKE %s OR IFNULL(x.bien_so, '') LIKE %s OR x.chu_xe LIKE %s)"
            )
            params.extend([kw, kw, kw, kw])

        where_clause = "WHERE " + " AND ".join(conditions)
        sql = f"""
            SELECT COUNT(*) AS tong_so
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            {where_clause}
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            cur.close()
            return int(row["tong_so"]) if row else 0

    @staticmethod
    def thuc_hien_cho_xe_ra_va_thanh_toan(
        ma_ve: str,
        so_tien: int,
        phuong_thuc: str,
        id_nhan_vien_ra: Optional[int],
        ghi_chu: Optional[str] = None
    ) -> bool:
        """
        Thực hiện toàn bộ quy trình cho xe ra + thanh toán trong 1 Transaction:
        1. Cập nhật ve_xe: gio_ra = NOW(), trang_thai = 'Da thanh toan', id_nhan_vien_ra
        2. INSERT vào thanh_toan với số tiền và phương thức
        Nếu bất kỳ bước nào lỗi -> rollback toàn bộ để bảo toàn tính nhất quán.
        """
        sql_cap_nhat_ve = """
            UPDATE ve_xe
            SET gio_ra = NOW(), trang_thai = 'Da thanh toan', id_nhan_vien_ra = %s
            WHERE ma_ve = %s AND trang_thai = 'Dang gui'
        """
        sql_tao_thanh_toan = """
            INSERT INTO thanh_toan (ma_ve, so_tien, phuong_thuc, id_nhan_vien_thu, ghi_chu)
            VALUES (%s, %s, %s, %s, %s)
        """

        with quan_ly_ket_noi() as conn:
            cur = conn.cursor()
            try:
                # Bước 1: Đóng vé xe
                cur.execute(sql_cap_nhat_ve, (id_nhan_vien_ra, ma_ve))
                if cur.rowcount == 0:
                    # Không có vé nào khớp -> vé đã thanh toán hoặc không tồn tại
                    raise ValueError(f"Không tìm thấy vé '{ma_ve}' đang hoạt động.")

                # Bước 2: Tạo bản ghi thanh toán
                cur.execute(sql_tao_thanh_toan, (
                    ma_ve, so_tien, phuong_thuc, id_nhan_vien_ra, ghi_chu
                ))

                conn.commit()
                return True
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()

    # ─────────────────────────── DASHBOARD – KPI TỔNG QUAN ───────────────────────────

    @staticmethod
    def lay_kpi_dashboard() -> dict:
        """
        Lấy bộ số liệu KPI tổng quan cho màn hình Dashboard:
        - Tổng xe đang gửi (toàn bãi).
        - Tổng sức chứa toàn bãi và số chỗ trống.
        - Lượt xe vào hôm nay (kể từ 00:00:00 hôm nay).
        - Doanh thu hôm nay (tổng từ bảng thanh_toan).
        - Lượt xe vào trong 7 ngày gần nhất (cho biểu đồ).
        """
        sql_xe_dang_gui = "SELECT COUNT(*) AS tong FROM ve_xe WHERE trang_thai = 'Dang gui'"
        sql_suc_chua = "SELECT SUM(tong_cho) AS tong_cho FROM suc_chua"
        sql_luot_vao = "SELECT COUNT(*) AS so_luot FROM ve_xe WHERE DATE(gio_vao) = CURDATE()"
        sql_luot_ra = """
            SELECT COUNT(*) AS so_luot FROM ve_xe
            WHERE DATE(gio_ra) = CURDATE() AND trang_thai = 'Da thanh toan'
        """
        sql_doanh_thu = """
            SELECT COALESCE(SUM(so_tien), 0) AS tong FROM thanh_toan
            WHERE DATE(thoi_gian_thanh_toan) = CURDATE()
        """
        sql_xe_theo_loai = """
            SELECT x.loai_xe, bg.ten_hien_thi, COUNT(*) AS dang_gui
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            WHERE vx.trang_thai = 'Dang gui'
            GROUP BY x.loai_xe, bg.ten_hien_thi
        """
        sql_7_ngay = """
            SELECT DATE(gio_vao) AS ngay, COUNT(*) AS so_luot
            FROM ve_xe
            WHERE gio_vao >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(gio_vao)
            ORDER BY ngay ASC
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql_xe_dang_gui)
            tong_dang_gui = int((cur.fetchone() or {}).get("tong", 0))

            cur.execute(sql_suc_chua)
            tong_cho = int((cur.fetchone() or {}).get("tong_cho", 0))

            cur.execute(sql_luot_vao)
            luot_vao = int((cur.fetchone() or {}).get("so_luot", 0))

            cur.execute(sql_luot_ra)
            luot_ra = int((cur.fetchone() or {}).get("so_luot", 0))

            cur.execute(sql_doanh_thu)
            doanh_thu_hom_nay = int((cur.fetchone() or {}).get("tong", 0))

            cur.execute(sql_xe_theo_loai)
            xe_theo_loai = cur.fetchall()

            cur.execute(sql_7_ngay)
            data_7_ngay = cur.fetchall()

            cur.close()

        return {
            "tong_dang_gui": tong_dang_gui,
            "tong_suc_chua": tong_cho,
            "cho_trong": max(0, tong_cho - tong_dang_gui),
            "luot_vao_hom_nay": luot_vao,
            "luot_ra_hom_nay": luot_ra,
            "doanh_thu_hom_nay": doanh_thu_hom_nay,
            "xe_theo_loai": xe_theo_loai,
            "data_7_ngay": data_7_ngay,
        }

    # ─────────────────────────── REVENUE – DOANH THU ───────────────────────────

    @staticmethod
    def lay_doanh_thu_theo_ngay(so_ngay: int = 30, tu_ngay: str = None, den_ngay: str = None) -> list:
        """
        Thống kê doanh thu từng ngày.
        Hỗ trợ lọc theo khoảng ngày (tu_ngay, den_ngay) hoặc N ngày gần nhất (so_ngay).
        Trả về list dict: ngay, tien_mat, chuyen_khoan, tong, tong_doanh_thu, so_giao_dich.
        """
        conditions = []
        params = []
        if tu_ngay:
            conditions.append("DATE(thoi_gian_thanh_toan) >= %s")
            params.append(tu_ngay)
        if den_ngay:
            conditions.append("DATE(thoi_gian_thanh_toan) <= %s")
            params.append(den_ngay)
        if not conditions:
            conditions.append("thoi_gian_thanh_toan >= DATE_SUB(CURDATE(), INTERVAL %s DAY)")
            params.append(max(0, so_ngay - 1))
        where = f"WHERE {' AND '.join(conditions)}"
        sql = f"""
            SELECT
                DATE(thoi_gian_thanh_toan) AS ngay,
                COALESCE(SUM(CASE WHEN phuong_thuc = 'TIEN_MAT' THEN so_tien ELSE 0 END), 0) AS tien_mat,
                COALESCE(SUM(CASE WHEN phuong_thuc = 'CHUYEN_KHOAN' THEN so_tien ELSE 0 END), 0) AS chuyen_khoan,
                COALESCE(SUM(so_tien), 0) AS tong_doanh_thu,
                COUNT(*) AS so_giao_dich
            FROM thanh_toan
            {where}
            GROUP BY DATE(thoi_gian_thanh_toan)
            ORDER BY ngay DESC
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            cur.close()
            return [
                {
                    "ngay": r.get("ngay"),
                    "tien_mat": int(r.get("tien_mat") or 0),
                    "chuyen_khoan": int(r.get("chuyen_khoan") or 0),
                    "tong": int(r.get("tong_doanh_thu") or 0),
                    "tong_doanh_thu": int(r.get("tong_doanh_thu") or 0),
                    "so_giao_dich": int(r.get("so_giao_dich") or 0)
                }
                for r in rows
            ]

    @staticmethod
    def lay_tong_doanh_thu(tu_ngay: str = None, den_ngay: str = None) -> dict:
        """
        Tổng hợp doanh thu (tổng, tiền mặt, chuyển khoản, số giao dịch) theo khoảng ngày.
        tu_ngay, den_ngay định dạng 'YYYY-MM-DD'. Nếu None thì tính toàn bộ.
        """
        conditions = []
        params = []
        if tu_ngay:
            conditions.append("DATE(thoi_gian_thanh_toan) >= %s")
            params.append(tu_ngay)
        if den_ngay:
            conditions.append("DATE(thoi_gian_thanh_toan) <= %s")
            params.append(den_ngay)
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"""
            SELECT
                COALESCE(SUM(so_tien), 0) AS tong_doanh_thu,
                COALESCE(SUM(CASE WHEN phuong_thuc = 'TIEN_MAT' THEN so_tien ELSE 0 END), 0) AS tien_mat,
                COALESCE(SUM(CASE WHEN phuong_thuc = 'CHUYEN_KHOAN' THEN so_tien ELSE 0 END), 0) AS chuyen_khoan,
                COUNT(*) AS so_giao_dich
            FROM thanh_toan {where}
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            row = cur.fetchone() or {}
            cur.close()
            tong_val = int(row.get("tong_doanh_thu") or 0)
            tm_val = int(row.get("tien_mat") or 0)
            ck_val = int(row.get("chuyen_khoan") or 0)
            so_gd = int(row.get("so_giao_dich") or 0)
            return {
                "tong_doanh_thu": tong_val,
                "tong": tong_val,
                "tien_mat": tm_val,
                "chuyen_khoan": ck_val,
                "so_giao_dich": so_gd,
                "so_luot_thu": so_gd
            }

    @staticmethod
    def lay_lich_su_thanh_toan(
        tu_ngay: str = None,
        den_ngay: str = None,
        phuong_thuc: str = None,
        limit: int = 200
    ) -> list:
        """
        Lấy lịch sử giao dịch thanh toán chi tiết, hỗ trợ lọc theo ngày và phương thức.
        Trả về list dict kèm thông tin xe, nhân viên thu tiền.
        Nếu limit <= 0 hoặc None thì lấy toàn bộ không phân trang.
        """
        conditions = []
        params = []
        if tu_ngay:
            conditions.append("DATE(tt.thoi_gian_thanh_toan) >= %s")
            params.append(tu_ngay)
        if den_ngay:
            conditions.append("DATE(tt.thoi_gian_thanh_toan) <= %s")
            params.append(den_ngay)
        if phuong_thuc and phuong_thuc not in ("TAT_CA", "Tất cả"):
            conditions.append("tt.phuong_thuc = %s")
            params.append(phuong_thuc)
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        limit_clause = ""
        if limit and limit > 0:
            limit_clause = "LIMIT %s"
            params.append(limit)
        sql = f"""
            SELECT
                tt.id, tt.ma_ve, tt.so_tien, tt.phuong_thuc,
                tt.thoi_gian_thanh_toan, tt.ghi_chu,
                x.ma_dinh_danh, x.bien_so, x.chu_xe, x.loai_xe,
                bg.ten_hien_thi AS ten_loai_xe,
                vx.gio_vao,
                nd.ho_ten AS ten_nhan_vien
            FROM thanh_toan tt
            JOIN ve_xe vx ON vx.ma_ve = tt.ma_ve
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            LEFT JOIN nguoi_dung nd ON nd.id = tt.id_nhan_vien_thu
            {where}
            ORDER BY tt.thoi_gian_thanh_toan DESC
            {limit_clause}
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            cur.close()
            for r in rows:
                r["so_tien"] = int(r.get("so_tien") or 0)
            return rows

    @staticmethod
    def lay_doanh_thu_theo_thang(nam: int = None) -> list:
        """
        Thống kê doanh thu theo từng tháng trong năm.
        Mặc định là năm hiện tại.
        Trả về list dict: thang, tien_mat, chuyen_khoan, tong, tong_doanh_thu, so_giao_dich.
        """
        import datetime as _dt
        nam_thuc_te = nam or _dt.datetime.now().year
        sql = """
            SELECT
                MONTH(thoi_gian_thanh_toan) AS thang,
                COALESCE(SUM(CASE WHEN phuong_thuc = 'TIEN_MAT' THEN so_tien ELSE 0 END), 0) AS tien_mat,
                COALESCE(SUM(CASE WHEN phuong_thuc = 'CHUYEN_KHOAN' THEN so_tien ELSE 0 END), 0) AS chuyen_khoan,
                COALESCE(SUM(so_tien), 0) AS tong_doanh_thu,
                COUNT(*) AS so_giao_dich
            FROM thanh_toan
            WHERE YEAR(thoi_gian_thanh_toan) = %s
            GROUP BY MONTH(thoi_gian_thanh_toan)
            ORDER BY thang ASC
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (nam_thuc_te,))
            rows = cur.fetchall()
            cur.close()
            return [
                {
                    "thang": int(r.get("thang") or 0),
                    "tien_mat": int(r.get("tien_mat") or 0),
                    "chuyen_khoan": int(r.get("chuyen_khoan") or 0),
                    "tong": int(r.get("tong_doanh_thu") or 0),
                    "tong_doanh_thu": int(r.get("tong_doanh_thu") or 0),
                    "so_giao_dich": int(r.get("so_giao_dich") or 0)
                }
                for r in rows
            ]

    # ─────────────────────────── STATISTICS – THỐNG KÊ ───────────────────────────

    @staticmethod
    def lay_thong_ke_tong_hop() -> dict:
        """
        Lấy bộ số liệu thống kê tổng hợp cho màn hình Statistics:
        - Tỷ lệ lấp đầy từng loại xe (đang gửi / sức chứa).
        - Phân bố số lượng xe theo loại.
        - Tổng lượt xe vào/ra tất cả thời gian.
        - Số liệu giờ cao điểm (giờ nào có nhiều xe vào nhất).
        """
        sql_lap_day = """
            SELECT
                sc.loai_xe,
                bg.ten_hien_thi,
                sc.tong_cho,
                COALESCE(
                    (SELECT COUNT(*) FROM ve_xe vx2
                     JOIN xe x2 ON x2.id = vx2.id_xe
                     WHERE x2.loai_xe = sc.loai_xe AND vx2.trang_thai = 'Dang gui'), 0
                ) AS dang_gui
            FROM suc_chua sc
            JOIN bang_gia bg ON bg.loai_xe = sc.loai_xe
            ORDER BY sc.loai_xe
        """
        sql_tong_luot = """
            SELECT
                COUNT(*) AS tong_ve,
                SUM(CASE WHEN trang_thai = 'Dang gui' THEN 1 ELSE 0 END) AS dang_gui,
                SUM(CASE WHEN trang_thai = 'Da thanh toan' THEN 1 ELSE 0 END) AS da_thanh_toan
            FROM ve_xe
        """
        sql_gio_cao_diem = """
            SELECT HOUR(gio_vao) AS gio, COUNT(*) AS so_luot
            FROM ve_xe
            WHERE gio_vao >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY HOUR(gio_vao)
            ORDER BY gio ASC
        """
        sql_luot_theo_loai = """
            SELECT bg.ten_hien_thi, x.loai_xe, COUNT(vx.ma_ve) AS tong_luot
            FROM ve_xe vx
            JOIN xe x ON x.id = vx.id_xe
            JOIN bang_gia bg ON bg.loai_xe = x.loai_xe
            GROUP BY x.loai_xe, bg.ten_hien_thi
            ORDER BY tong_luot DESC
        """
        with quan_ly_ket_noi() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql_lap_day)
            lap_day = cur.fetchall()

            cur.execute(sql_tong_luot)
            tong_luot = cur.fetchone() or {}

            cur.execute(sql_gio_cao_diem)
            gio_cao_diem = cur.fetchall()

            cur.execute(sql_luot_theo_loai)
            luot_theo_loai = cur.fetchall()

            cur.close()

        return {
            "lap_day": lap_day,
            "tong_ve": int(tong_luot.get("tong_ve", 0)),
            "dang_gui": int(tong_luot.get("dang_gui", 0)),
            "da_thanh_toan": int(tong_luot.get("da_thanh_toan", 0)),
            "gio_cao_diem": gio_cao_diem,
            "luot_theo_loai": luot_theo_loai,
        }
