import os
from pathlib import Path
from dotenv import load_dotenv

# Xác định đường dẫn file .env nằm ở thư mục gốc của project
GOC_DU_AN = Path(__file__).resolve().parent.parent
DUONG_DAN_ENV = GOC_DU_AN / ".env"

# Nạp các biến môi trường từ file .env (nếu file tồn tại)
if DUONG_DAN_ENV.exists():
    load_dotenv(dotenv_path=DUONG_DAN_ENV)
else:
    # Nếu chưa có .env, nạp mặc định từ môi trường hệ thống
    load_dotenv()


class DatabaseConfig:
    """
    Class quản lý thông tin cấu hình kết nối MySQL.
    Các giá trị được ưu tiên đọc từ biến môi trường (.env),
    nếu không có sẽ sử dụng giá trị mặc định an toàn.
    """
    HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("DB_PORT", "3306"))
    USER: str = os.getenv("DB_USER", "root")
    PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DATABASE: str = os.getenv("DB_NAME", "neon_parking_db")
    CHARSET: str = os.getenv("DB_CHARSET", "utf8mb4")

    @classmethod
    def lay_thong_so_ket_noi(cls, include_database: bool = True) -> dict:
        """
        Trả về dictionary chứa tham số kết nối cho mysql.connector.
        :param include_database: True nếu muốn kết nối trực tiếp vào database chỉ định,
                                  False nếu muốn kết nối vào MySQL Server chung (để tạo database).
        """
        cau_hinh = {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "charset": cls.CHARSET,
            "use_pure": True,
            "autocommit": False,
        }
        if include_database:
            cau_hinh["database"] = cls.DATABASE

        return cau_hinh
