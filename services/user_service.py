"""
NEON PARKING MANAGER - USER SERVICE
Tầng nghiệp vụ Quản lý người dùng: Tạo nhân viên, Sửa thông tin, Khóa/Mở khóa, Đặt lại mật khẩu.
Kiểm tra phân quyền Admin tại Service Layer theo nguyên tắc AGENTS.md.
"""

from typing import List, Tuple, Optional
from models.nguoi_dung import NguoiDung
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService
from security.hasher import MatKhauHasher


class UserService:
    """
    Dịch vụ quản trị tài khoản nhân viên (ADMIN ONLY).
    """

    @classmethod
    def lay_danh_sach_nhan_vien(cls, tu_khoa: Optional[str] = None) -> List[NguoiDung]:
        """
        Lấy danh sách tất cả người dùng trong hệ thống (Chỉ ADMIN).
        """
        AuthService.kiem_tra_quyen_admin()
        return UserRepository.lay_tat_ca_nguoi_dung(tu_khoa=tu_khoa)

    @classmethod
    def tao_nhan_vien(
        cls,
        ten_dang_nhap: str,
        ho_ten: str,
        mat_khau: str,
        xac_nhan_mat_khau: str
    ) -> Tuple[bool, str]:
        """
        Tạo tài khoản nhân viên mới (Chỉ ADMIN).
        """
        AuthService.kiem_tra_quyen_admin()
        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        ten_dang_nhap = (ten_dang_nhap or "").strip()
        ho_ten = (ho_ten or "").strip()

        if not ten_dang_nhap:
            return False, "Vui lòng nhập tên đăng nhập!"
        if len(ten_dang_nhap) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự!"
        if " " in ten_dang_nhap:
            return False, "Tên đăng nhập không được chứa khoảng trắng!"
        if not ho_ten:
            return False, "Vui lòng nhập họ tên nhân viên!"
        if not mat_khau:
            return False, "Vui lòng nhập mật khẩu khởi tạo!"
        if len(mat_khau) < 6:
            return False, "Mật khẩu phải có độ dài tối thiểu từ 6 ký tự trở lên!"
        if mat_khau != xac_nhan_mat_khau:
            return False, "Mật khẩu xác nhận không trùng khớp!"

        # Băm mật khẩu bằng Argon2id
        try:
            mat_khau_hash = MatKhauHasher.bam_mat_khau(mat_khau)
        except Exception as e:
            return False, f"Lỗi băm mật khẩu: {e}"

        ok, msg, _ = UserRepository.tao_nhan_vien(
            ten_dang_nhap=ten_dang_nhap,
            ho_ten=ho_ten,
            mat_khau_hash=mat_khau_hash,
            id_admin=admin_hien_tai.id if admin_hien_tai else None
        )
        return ok, msg

    @classmethod
    def sua_thong_tin_nhan_vien(
        cls,
        user_id: int,
        ho_ten: str,
        ten_dang_nhap: str
    ) -> Tuple[bool, str]:
        """
        Sửa họ tên và tên đăng nhập của tài khoản (Chỉ ADMIN).
        """
        AuthService.kiem_tra_quyen_admin()
        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        ten_dang_nhap = (ten_dang_nhap or "").strip()
        ho_ten = (ho_ten or "").strip()

        if not ten_dang_nhap:
            return False, "Tên đăng nhập không được để trống!"
        if len(ten_dang_nhap) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự!"
        if " " in ten_dang_nhap:
            return False, "Tên đăng nhập không được chứa khoảng trắng!"
        if not ho_ten:
            return False, "Họ và tên không được để trống!"

        return UserRepository.cap_nhat_thong_tin(
            user_id=user_id,
            ho_ten=ho_ten,
            ten_dang_nhap=ten_dang_nhap,
            id_admin=admin_hien_tai.id if admin_hien_tai else None
        )

    @classmethod
    def thay_doi_trang_thai_khoa(
        cls,
        user_id: int,
        khoa: bool
    ) -> Tuple[bool, str]:
        """
        Khóa hoặc Mở khóa tài khoản nhân viên (Chỉ ADMIN).
        Quy tắc an toàn: Không cho phép Admin tự khóa chính mình!
        """
        AuthService.kiem_tra_quyen_admin()
        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        # Kiểm tra không cho phép tự khóa tài khoản đang sử dụng
        if admin_hien_tai and admin_hien_tai.id == user_id:
            return False, "Bạn không thể tự khóa tài khoản Admin đang sử dụng của chính mình!"

        # Kiểm tra người dùng mục tiêu
        muc_tieu = UserRepository.lay_theo_id(user_id)
        if not muc_tieu:
            return False, "Không tìm thấy người dùng trong hệ thống!"

        if muc_tieu.la_admin and khoa:
            # Kiểm tra nếu là Admin duy nhất thì không được khóa
            so_admin = UserRepository.dem_so_luong_admin()
            if so_admin <= 1:
                return False, "Không thể khóa Quản trị viên duy nhất của hệ thống!"

        trang_thai_moi = "KHOA" if khoa else "HOAT_DONG"
        return UserRepository.cap_nhat_trang_thai(
            user_id=user_id,
            trang_thai=trang_thai_moi,
            id_admin=admin_hien_tai.id if admin_hien_tai else None
        )

    @classmethod
    def dat_lai_mat_khau(
        cls,
        user_id: int,
        mat_khau_moi: str,
        xac_nhan_mat_khau: str
    ) -> Tuple[bool, str]:
        """
        Admin đặt lại mật khẩu cho nhân viên bằng quy trình an toàn Argon2id (Chỉ ADMIN).
        """
        AuthService.kiem_tra_quyen_admin()
        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        if not mat_khau_moi:
            return False, "Vui lòng nhập mật khẩu mới!"
        if len(mat_khau_moi) < 6:
            return False, "Mật khẩu mới phải có tối thiểu 6 ký tự!"
        if mat_khau_moi != xac_nhan_mat_khau:
            return False, "Mật khẩu xác nhận không trùng khớp!"

        # Băm mật khẩu mới bằng Argon2id
        try:
            mat_khau_hash = MatKhauHasher.bam_mat_khau(mat_khau_moi)
        except Exception as e:
            return False, f"Lỗi mã hóa mật khẩu: {e}"

        return UserRepository.dat_lai_mat_khau_nhan_vien(
            user_id=user_id,
            mat_khau_hash_moi=mat_khau_hash,
            id_admin=admin_hien_tai.id if admin_hien_tai else None
        )
