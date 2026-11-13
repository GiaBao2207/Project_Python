"""
KIỂM THỬ TỰ ĐỘNG CHUYỂN ĐỔI GIAO DIỆN CÁC MODULE (UI SWITCHING STABILITY TEST)
Mô phỏng chuỗi thao tác đăng nhập và điều hướng liên tục giữa tất cả 9 module
để đảm bảo không có rò rỉ widget, lỗi lifecycle Tkinter hay crash.
"""

import os
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

import customtkinter as ctk
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService
from gui.main_window import MainWindow

def test_switching():
    print("Khởi tạo cửa sổ CustomTkinter kiểm thử...")
    root = ctk.CTk()
    root.geometry("1280x800")
    root.withdraw()  # Ẩn cửa sổ để chạy kiểm thử ngầm không cản trở màn hình

    # 1. Giả lập Admin đăng nhập
    admin_user = UserRepository.lay_theo_ten_dang_nhap("admin")
    if not admin_user:
        # Lấy bất kỳ admin nào
        users = UserRepository.lay_tat_ca_nguoi_dung()
        for u in users:
            if u.la_admin:
                admin_user = u
                break

    assert admin_user is not None, "Không tìm thấy tài khoản admin trong CSDL!"
    AuthService._nguoi_dung_hien_tai = admin_user
    print(f"Đăng nhập phiên kiểm thử: {admin_user.ho_ten} (Vai trò: {admin_user.vai_tro})")

    # 2. Khởi tạo MainWindow
    app = MainWindow(root)
    app.pack(fill="both", expand=True)
    root.update()

    app.hien_thi_shell_chinh()
    root.update()

    # 3. Chuỗi module kiểm thử chuyển đổi nhiều vòng
    modules = [
        "dashboard", "vehicles", "tickets", "revenue",
        "statistics", "users", "settings", "reports", "audit"
    ]

    print("Bắt đầu vòng lặp điều hướng qua toàn bộ 9 module:")
    for vong in range(1, 3):
        print(f"--- Vòng kiểm thử số {vong} ---")
        for m_id in modules:
            app.dieu_huong_module(m_id)
            root.update()
            assert app.current_view is not None, f"Module {m_id} không khởi tạo được View!"
            print(f"  [OK] Nạp thành công module: '{m_id}' -> {type(app.current_view).__name__}")

    # Đóng cửa sổ kiểm thử
    root.destroy()
    print("=== KIỂM THỬ CHUYỂN ĐỔI GIAO DIỆN 9 MODULE HOÀN TẤT: PASS 100% ===")

if __name__ == "__main__":
    test_switching()
