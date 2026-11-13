"""
NEON PARKING MANAGER - SETTINGS SERVICE
Tầng nghiệp vụ Quản lý Cài đặt: Bảng giá dịch vụ và Sức chứa bãi xe.
Tuân thủ nghiêm ngặt:
- Chỉ Admin có quyền thay đổi.
- Không cho phép nhập giá hoặc sức chứa âm.
- Không cho phép giảm sức chứa xuống thấp hơn số xe đang gửi thực tế.
- Việc đổi bảng giá không làm thay đổi giá vé đã tạo (bảo toàn snapshot).
- Ghi nhật ký đầy đủ cho mọi thao tác.
"""

from typing import List, Dict, Any, Tuple
from database.repositories.vehicle_repository import VehicleRepository
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService


class SettingsService:
    """
    Dịch vụ quản trị Cấu hình Hệ thống (ADMIN ONLY).
    """

    @classmethod
    def lay_bang_gia(cls) -> List[Dict[str, Any]]:
        """Lấy danh sách bảng giá hiện tại (Chỉ ADMIN)."""
        AuthService.kiem_tra_quyen_admin()
        return VehicleRepository.lay_chi_tiet_bang_gia()

    @classmethod
    def lay_suc_chua(cls) -> List[Dict[str, Any]]:
        """Lấy danh sách sức chứa và tình trạng chiếm chỗ hiện tại (Chỉ ADMIN)."""
        AuthService.kiem_tra_quyen_admin()
        return VehicleRepository.lay_chi_tiet_suc_chua()

    @classmethod
    def cap_nhat_bang_gia(cls, loai_xe: str, gia_moi: int) -> Tuple[bool, str]:
        """
        Cập nhật đơn giá vé gửi xe (Chỉ ADMIN).
        """
        AuthService.kiem_tra_quyen_admin()
        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        loai_xe_hop_le = ["XeDap", "XeMay", "OTo"]
        if loai_xe not in loai_xe_hop_le:
            return False, f"Loại xe không hợp lệ! Chỉ chấp nhận: {', '.join(loai_xe_hop_le)}"

        if gia_moi < 0:
            return False, "Đơn giá vé gửi xe không được là số âm!"

        return VehicleRepository.cap_nhat_gia_ve(
            loai_xe=loai_xe,
            gia_moi=gia_moi,
            id_admin=admin_hien_tai.id if admin_hien_tai else None
        )

    @classmethod
    def cap_nhat_suc_chua(cls, loai_xe: str, suc_chua_moi: int) -> Tuple[bool, str]:
        """
        Cập nhật tổng số chỗ đỗ quy định cho từng loại xe (Chỉ ADMIN).
        Kiểm tra nghiệp vụ: Sức chứa mới không được nhỏ hơn số xe đang gửi thực tế!
        """
        AuthService.kiem_tra_quyen_admin()
        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        loai_xe_hop_le = ["XeDap", "XeMay", "OTo"]
        if loai_xe not in loai_xe_hop_le:
            return False, f"Loại xe không hợp lệ! Chỉ chấp nhận: {', '.join(loai_xe_hop_le)}"

        if suc_chua_moi < 0:
            return False, "Sức chứa không được là số âm!"

        # Ràng buộc nghiệp vụ: Không được giảm sức chứa xuống dưới số xe đang gửi
        dang_gui = VehicleRepository.dem_xe_dang_gui(loai_xe)
        if suc_chua_moi < dang_gui:
            return False, (
                f"Không thể giảm sức chứa {loai_xe} xuống {suc_chua_moi} chỗ! "
                f"Hiện tại đang có {dang_gui} xe đang gửi trong bãi."
            )

        return VehicleRepository.cap_nhat_suc_chua(
            loai_xe=loai_xe,
            tong_cho_moi=suc_chua_moi,
            id_admin=admin_hien_tai.id if admin_hien_tai else None
        )
