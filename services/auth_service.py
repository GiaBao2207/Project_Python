"""
NEON PARKING MANAGER - AUTHENTICATION SERVICE
Tầng nghiệp vụ xử lý: Thiết lập Admin đầu tiên, Đăng nhập, Đổi mật khẩu, 
Kiểm tra tài khoản khóa, Quản lý phiên làm việc (Session) và Phân quyền.
"""

from typing import Optional, Tuple
from models.nguoi_dung import NguoiDung
from database.repositories.user_repository import UserRepository
from security.hasher import MatKhauHasher


class AuthService:
    """
    Dịch vụ xác thực và phân quyền người dùng.
    Đảm bảo kiểm tra quyền chặt chẽ ở tầng Service trước khi thực thi.
    """
    _nguoi_dung_hien_tai: Optional[NguoiDung] = None

    @classmethod
    def lay_nguoi_dung_hien_tai(cls) -> Optional[NguoiDung]:
        """Trả về thông tin người dùng đang đăng nhập trong phiên làm việc hiện tại."""
        return cls._nguoi_dung_hien_tai

    @classmethod
    def kiem_tra_da_dang_nhap(cls) -> bool:
        """Kiểm tra xem hiện tại đã có ai đăng nhập hay chưa."""
        return cls._nguoi_dung_hien_tai is not None

    @classmethod
    def la_admin(cls) -> bool:
        """Kiểm tra người dùng hiện tại có vai trò Quản trị viên (ADMIN) không."""
        return cls._nguoi_dung_hien_tai is not None and cls._nguoi_dung_hien_tai.la_admin

    @classmethod
    def kiem_tra_quyen_admin(cls) -> None:
        """
        Ném PermissionError nếu người dùng hiện tại không phải ADMIN.
        Bảo vệ nghiệp vụ quản trị không phụ thuộc vào việc ẩn/hiện nút GUI.
        """
        if not cls.la_admin():
            raise PermissionError("Quyền hạn bị từ chối: Thao tác này chỉ dành riêng cho Quản trị viên (ADMIN)!")

    @classmethod
    def kiem_tra_can_setup_admin(cls) -> bool:
        """
        Kiểm tra xem hệ thống có cần hiển thị màn hình 'First Admin Setup' không.
        Trả về True nếu chưa có bất kỳ Admin nào trong MySQL.
        """
        try:
            so_admin = UserRepository.dem_so_luong_admin()
            return so_admin == 0
        except Exception as e:
            # Nếu có lỗi kết nối, chuyển tiếp ngoại lệ để tầng GUI hiển thị cảnh báo kết nối
            raise e

    @classmethod
    def thiet_lap_admin_dau_tien(
        cls,
        ten_dang_nhap: str,
        ho_ten: str,
        mat_khau: str,
        xac_nhan_mat_khau: str
    ) -> Tuple[bool, str]:
        """
        Thiết lập tài khoản Quản trị viên đầu tiên cho hệ sinh thái bãi xe.
        :return: (Thành_công: bool, Thông_báo_kết_quả: str)
        """
        # 1. Kiểm tra tính hợp lệ của dữ liệu đầu vào
        ten_dang_nhap = (ten_dang_nhap or "").strip()
        ho_ten = (ho_ten or "").strip()

        if not ten_dang_nhap:
            return False, "Vui lòng nhập tên đăng nhập cho Quản trị viên!"
        if len(ten_dang_nhap) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự!"
        if " " in ten_dang_nhap:
            return False, "Tên đăng nhập không được chứa khoảng trắng!"
        if not ho_ten:
            return False, "Vui lòng nhập họ và tên của Quản trị viên!"
        if not mat_khau:
            return False, "Vui lòng nhập mật khẩu!"
        if len(mat_khau) < 6:
            return False, "Mật khẩu phải có độ dài tối thiểu từ 6 ký tự trở lên!"
        if mat_khau != xac_nhan_mat_khau:
            return False, "Mật khẩu xác nhận không trùng khớp!"

        # 2. Băm mật khẩu bằng Argon2id
        try:
            mat_khau_hash = MatKhauHasher.bam_mat_khau(mat_khau)
        except Exception as e:
            return False, f"Lỗi trong quá trình mã hóa mật khẩu: {e}"

        # 3. Ghi vào CSDL với cơ chế an toàn concurrency
        try:
            thanh_cong = UserRepository.tao_admin_dau_tien(
                ten_dang_nhap=ten_dang_nhap,
                ho_ten=ho_ten,
                mat_khau_hash=mat_khau_hash
            )
            if thanh_cong:
                return True, "Khởi tạo Quản trị viên đầu tiên thành công! Vui lòng đăng nhập."
            else:
                return False, "Hệ thống đã có tài khoản Quản trị viên. Không thể tạo thêm bằng quy trình này!"
        except Exception as e:
            return False, f"Lỗi cơ sở dữ liệu khi tạo Admin: {e}"

    @classmethod
    def dang_nhap(cls, ten_dang_nhap: str, mat_khau: str) -> Tuple[bool, str, Optional[NguoiDung]]:
        """
        Xác thực đăng nhập người dùng bằng tên tài khoản và mật khẩu.
        :return: (Thành_công: bool, Thông_báo: str, NguoiDung_nếu_thành_công)
        """
        ten_dang_nhap = (ten_dang_nhap or "").strip()
        if not ten_dang_nhap:
            return False, "Vui lòng nhập tên đăng nhập!", None
        if not mat_khau:
            return False, "Vui lòng nhập mật khẩu!", None

        # 1. Tìm tài khoản trong MySQL
        try:
            nguoi_dung = UserRepository.lay_theo_ten_dang_nhap(ten_dang_nhap)
        except Exception as e:
            return False, f"Không thể kết nối cơ sở dữ liệu để đăng nhập: {e}", None

        if not nguoi_dung:
            return False, "Tên đăng nhập hoặc mật khẩu không chính xác!", None

        # 2. Kiểm tra trạng thái tài khoản
        if not nguoi_dung.dang_hoat_dong:
            UserRepository.ghi_nhat_ky(
                nguoi_dung.id,
                "DANG_NHAP_THAT_BAI",
                "Cố gắng đăng nhập vào tài khoản đã bị khóa"
            )
            return False, "Tài khoản của bạn đã bị KHÓA. Vui lòng liên hệ Quản trị viên!", None

        # 3. Xác minh mật khẩu bằng Argon2id
        mat_khau_dung = MatKhauHasher.kiem_tra_mat_khau(nguoi_dung.mat_khau_hash, mat_khau)
        if not mat_khau_dung:
            UserRepository.ghi_nhat_ky(
                nguoi_dung.id,
                "DANG_NHAP_THAT_BAI",
                "Nhập sai mật khẩu"
            )
            return False, "Tên đăng nhập hoặc mật khẩu không chính xác!", None

        # 4. Đăng nhập thành công -> Lưu vào Session
        cls._nguoi_dung_hien_tai = nguoi_dung
        UserRepository.ghi_nhat_ky(
            nguoi_dung.id,
            "DANG_NHAP_THANH_CONG",
            f"Đăng nhập thành công với vai trò {nguoi_dung.vai_tro}"
        )
        return True, "Đăng nhập thành công!", nguoi_dung

    @classmethod
    def dang_xuat(cls) -> None:
        """Đăng xuất người dùng hiện tại và xóa phiên làm việc."""
        if cls._nguoi_dung_hien_tai:
            UserRepository.ghi_nhat_ky(
                cls._nguoi_dung_hien_tai.id,
                "DANG_XUAT",
                "Đăng xuất khỏi hệ thống"
            )
        cls._nguoi_dung_hien_tai = None

    @classmethod
    def doi_mat_khau(
        cls,
        mat_khau_cu: str,
        mat_khau_moi: str,
        xac_nhan_moi: str
    ) -> Tuple[bool, str]:
        """
        Đổi mật khẩu cho người dùng đang đăng nhập trong phiên hiện tại.
        """
        if not cls._nguoi_dung_hien_tai:
            return False, "Bạn chưa đăng nhập vào hệ thống!"

        user_id = cls._nguoi_dung_hien_tai.id
        if not mat_khau_cu:
            return False, "Vui lòng nhập mật khẩu hiện tại!"
        if not mat_khau_moi:
            return False, "Vui lòng nhập mật khẩu mới!"
        if len(mat_khau_moi) < 6:
            return False, "Mật khẩu mới phải có tối thiểu từ 6 ký tự!"
        if mat_khau_moi != xac_nhan_moi:
            return False, "Xác nhận mật khẩu mới không trùng khớp!"
        if mat_khau_cu == mat_khau_moi:
            return False, "Mật khẩu mới không được trùng với mật khẩu cũ!"

        # Lấy lại bản ghi mới nhất từ DB
        user_db = UserRepository.lay_theo_id(user_id)
        if not user_db:
            return False, "Không tìm thấy thông tin tài khoản trong cơ sở dữ liệu!"

        # Xác thực mật khẩu cũ
        if not MatKhauHasher.kiem_tra_mat_khau(user_db.mat_khau_hash, mat_khau_cu):
            return False, "Mật khẩu hiện tại không chính xác!"

        # Băm mật khẩu mới và lưu
        mat_khau_hash_moi = MatKhauHasher.bam_mat_khau(mat_khau_moi)
        thanh_cong = UserRepository.doi_mat_khau(user_id, mat_khau_hash_moi)
        if thanh_cong:
            cls._nguoi_dung_hien_tai.mat_khau_hash = mat_khau_hash_moi
            return True, "Đổi mật khẩu thành công!"
        return False, "Không thể cập nhật mật khẩu mới vào cơ sở dữ liệu!"
