import mysql.connector
from mysql.connector import Error, errorcode
from typing import Optional
from contextlib import contextmanager
from config.database import DatabaseConfig


def lay_ket_noi(include_database: bool = True):
    """
    Tạo và trả về một kết nối MySQL mới dựa trên cấu hình trong .env.
    :param include_database: True để chọn database quan_ly_bai_giu_xe, False để kết nối Server chung.
    :return: mysql.connector.connection_cext.CMySQLConnection
    :raises: ConnectionError với thông báo tiếng Việt chi tiết nếu kết nối thất bại.
    """
    thong_so = DatabaseConfig.lay_thong_so_ket_noi(include_database=include_database)
    try:
        connection = mysql.connector.connect(**thong_so)
        return connection
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            thong_bao = f"Sai tên tài khoản hoặc mật khẩu MySQL ({thong_so['user']}@{thong_so['host']}). Vui lòng kiểm tra lại file .env!"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            thong_bao = f"Cơ sở dữ liệu '{thong_so.get('database')}' chưa tồn tại. Hãy chạy script khởi tạo init_db.py!"
        elif err.errno == errorcode.CR_CONN_HOST_ERROR or err.errno == 2003:
            thong_bao = f"Không thể kết nối tới MySQL Server tại {thong_so['host']}:{thong_so['port']}. Hãy kiểm tra xem dịch vụ MySQL đã bật chưa!"
        else:
            thong_bao = f"Lỗi kết nối MySQL [{err.errno}]: {err.msg}"
        raise ConnectionError(thong_bao) from err


@contextmanager
def quan_ly_ket_noi(include_database: bool = True, tu_dong_commit: bool = False):
    """
    Context manager giúp mở và tự động đóng kết nối MySQL an toàn.
    Ví dụ sử dụng:
        with quan_ly_ket_noi() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bang_gia")
            data = cursor.fetchall()
    """
    conn = lay_ket_noi(include_database=include_database)
    try:
        yield conn
        if tu_dong_commit:
            conn.commit()
    except Exception:
        if conn.is_connected():
            conn.rollback()
        raise
    finally:
        if conn.is_connected():
            conn.close()
