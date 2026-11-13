"""
NEON PARKING MANAGER - USER MODEL
Mô hình đối tượng Người dùng (Admin / Nhân viên) theo chuẩn OOP.
"""

from datetime import datetime
from typing import Optional


class NguoiDung:
    """
    Đại diện cho một tài khoản người dùng trong hệ thống bãi giữ xe.
    """
    def __init__(
        self,
        id: Optional[int],
        ten_dang_nhap: str,
        ho_ten: str,
        vai_tro: str = "NHAN_VIEN",
        trang_thai: str = "HOAT_DONG",
        mat_khau_hash: str = "",
        ngay_tao: Optional[datetime] = None
    ):
        self.id = id
        self.ten_dang_nhap = ten_dang_nhap
        self.ho_ten = ho_ten
        self.vai_tro = vai_tro          # 'ADMIN' hoặc 'NHAN_VIEN'
        self.trang_thai = trang_thai    # 'HOAT_DONG' hoặc 'KHOA'
        self.mat_khau_hash = mat_khau_hash
        self.ngay_tao = ngay_tao or datetime.now()

    @property
    def la_admin(self) -> bool:
        """Kiểm tra xem người dùng có phải là Quản trị viên (ADMIN) không."""
        return self.vai_tro == "ADMIN"

    @property
    def dang_hoat_dong(self) -> bool:
        """Kiểm tra xem tài khoản có đang hoạt động hay đã bị khóa."""
        return self.trang_thai == "HOAT_DONG"

    @property
    def vai_tro_tieng_viet(self) -> str:
        """Trả về tên vai trò tiếng Việt thân thiện."""
        return "Quản Trị Viên" if self.la_admin else "Nhân Viên Trực"

    def __repr__(self) -> str:
        return f"<NguoiDung id={self.id} user='{self.ten_dang_nhap}' role='{self.vai_tro}'>"
