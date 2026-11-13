"""
NEON PARKING MANAGER - CYBERPUNK DESKTOP APPLICATION
Điểm khởi chạy ứng dụng Desktop chính (CustomTkinter + MySQL Server 9.7.1).
"""

import sys
from pathlib import Path

# Đảm bảo đường dẫn gốc của project có trong sys.path
GOC_DU_AN = Path(__file__).resolve().parent
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

import customtkinter as ctk
from config.theme import CyberpunkTheme
from gui.components.branding import cai_dat_icon_cua_so
from gui.utils.window_helper import center_window
from gui.main_window import MainWindow


def main():
    """Khởi động ứng dụng Desktop."""
    # Cấu hình giao diện CustomTkinter sang phong cách Light Premium
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # Tạo cửa sổ gốc CTk duy nhất
    root = ctk.CTk()
    root.title("NEON PARKING MANAGER - Hệ Thống Quản Lý Bãi Giữ Xe Thông Minh")

    # Tính toán kích thước tối ưu theo độ phân giải màn hình thực tế
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Kích thước tiêu chuẩn thiết kế là 1280x800
    app_w = 1280
    app_h = 800

    # Nếu màn hình nhỏ (ví dụ laptop 1366x768 hoặc tương đương), tự co lại an toàn
    if screen_w < 1360 or screen_h < 820:
        app_w = min(1200, int(screen_w * 0.92))
        app_h = min(680, int(screen_h * 0.88))

    root.minsize(1000, 560)
    root.configure(fg_color=CyberpunkTheme.BG_DARK)

    # Căn giữa cửa sổ chính một lần duy nhất lúc khởi động
    center_window(root, width=app_w, height=app_h)

    # Cài đặt biểu tượng icon cửa sổ Windows từ bộ nhận diện branding
    cai_dat_icon_cua_so(root)

    # Khởi tạo Main Window Controller
    app = MainWindow(root)
    app.pack(fill="both", expand=True)

    # Bắt sự kiện bấm nút X trên thanh tiêu đề Windows để hiển thị CyberDialog xác nhận thoát
    root.protocol("WM_DELETE_WINDOW", app.xac_nhan_thoat_chuong_trinh)

    # Chạy vòng lặp sự kiện chính của giao diện
    root.mainloop()


if __name__ == "__main__":
    main()
