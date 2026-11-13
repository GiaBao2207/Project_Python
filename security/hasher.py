"""
NEON PARKING MANAGER - PASSWORD SECURITY MODULE
Băm và xác thực mật khẩu an toàn theo chuẩn Argon2id (sử dụng thư viện argon2-cffi).
"""

import argon2
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError


class MatKhauHasher:
    """
    Tiện ích băm và xác minh mật khẩu bằng thuật toán Argon2id hàng đầu hiện nay.
    Chống tấn công vét cạn brute-force và tăng tốc phần cứng GPU/ASIC.
    """
    # Khởi tạo đối tượng PasswordHasher với các tham số chuẩn bảo mật cao
    _hasher = argon2.PasswordHasher(
        time_cost=2,        # Số vòng tính toán (iterations)
        memory_cost=65536,  # Dung lượng RAM sử dụng: 64 MB
        parallelism=1,      # Số luồng xử lý
        hash_len=32,        # Độ dài chuỗi hash đầu ra
        type=argon2.Type.ID # Sử dụng chuẩn Argon2id
    )

    @classmethod
    def bam_mat_khau(cls, mat_khau_tho: str) -> str:
        """
        Nhận mật khẩu văn bản thô và trả về chuỗi hash an toàn chuẩn Argon2id.
        :param mat_khau_tho: Chuỗi mật khẩu gốc do người dùng nhập.
        :return: Chuỗi hash dạng $argon2id$v=19$m=65536,t=2,p=1$...
        """
        if not mat_khau_tho:
            raise ValueError("Mật khẩu không được để trống khi băm!")
        return cls._hasher.hash(mat_khau_tho)

    @classmethod
    def kiem_tra_mat_khau(cls, chuoi_hash: str, mat_khau_tho: str) -> bool:
        """
        Xác minh mật khẩu thô có khớp với chuỗi hash đã lưu trong CSDL hay không.
        :param chuoi_hash: Chuỗi băm đã lưu trong MySQL.
        :param mat_khau_tho: Mật khẩu người dùng nhập lúc đăng nhập.
        :return: True nếu khớp, False nếu sai hoặc chuỗi hash không hợp lệ.
        """
        if not chuoi_hash or not mat_khau_tho:
            return False
        try:
            return cls._hasher.verify(chuoi_hash, mat_khau_tho)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False

    @classmethod
    def can_bam_lai(cls, chuoi_hash: str) -> bool:
        """
        Kiểm tra chuỗi hash có cần nâng cấp lên tham số mới hơn hay không.
        """
        try:
            return cls._hasher.check_needs_rehash(chuoi_hash)
        except Exception:
            return False
