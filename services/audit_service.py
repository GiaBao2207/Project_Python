"""
NEON PARKING MANAGER - AUDIT SERVICE
Tầng nghiệp vụ Nhật ký Hoạt động (Audit Trail).
Quản lý lịch sử truy vết hệ thống: lọc theo ngày, nhân viên, loại thao tác.
Chỉ dành riêng cho ADMIN.
"""

from typing import List, Dict, Any, Tuple, Optional
import math
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService


class AuditService:
    """
    Dịch vụ truy vết hoạt động hệ thống (ADMIN ONLY).
    """

    @classmethod
    def lay_nhat_ky(
        cls,
        tu_ngay: Optional[str] = None,
        den_ngay: Optional[str] = None,
        id_nguoi_dung: Optional[int] = None,
        hanh_dong: Optional[str] = None,
        trang: int = 1,
        so_dong_moi_trang: int = 50
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Lấy danh sách nhật ký có bộ lọc và phân trang.
        :return: (danh_sach_nhat_ky, tong_so_ban_ghi, tong_so_trang)
        """
        AuthService.kiem_tra_quyen_admin()

        if trang < 1:
            trang = 1
        if so_dong_moi_trang < 10:
            so_dong_moi_trang = 10

        offset = (trang - 1) * so_dong_moi_trang
        rows, tong_so = UserRepository.lay_nhat_ky(
            tu_ngay=tu_ngay,
            den_ngay=den_ngay,
            id_nguoi_dung=id_nguoi_dung,
            hanh_dong=hanh_dong,
            limit=so_dong_moi_trang,
            offset=offset
        )

        tong_trang = max(1, math.ceil(tong_so / so_dong_moi_trang))
        return rows, tong_so, tong_trang

    @classmethod
    def lay_danh_sach_loai_hanh_dong(cls) -> List[str]:
        """Lấy danh sách các loại hành động để lọc (Chỉ ADMIN)."""
        AuthService.kiem_tra_quyen_admin()
        return UserRepository.lay_danh_sach_loai_hanh_dong()

    @classmethod
    def lay_danh_sach_nguoi_dung_filter(cls) -> List[Dict[str, Any]]:
        """Lấy danh sách người dùng phục vụ bộ lọc combobox (Chỉ ADMIN)."""
        AuthService.kiem_tra_quyen_admin()
        users = UserRepository.lay_tat_ca_nguoi_dung()
        return [{"id": u.id, "ten_dang_nhap": u.ten_dang_nhap, "ho_ten": u.ho_ten} for u in users]
