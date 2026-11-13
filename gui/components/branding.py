"""
NEON PARKING MANAGER - BRANDING & ASSETS HELPER
Cung cấp tiện ích nạp Logo, Icon cửa sổ đồng bộ cho toàn bộ giao diện CustomTkinter.
Đảm bảo giữ tham chiếu đối tượng ảnh (Image Reference) chống Garbage Collection trong Tkinter.
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import customtkinter as ctk

# Thư mục gốc chứa tài nguyên branding
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "branding"
LOGO_PNG_PATH = ASSETS_DIR / "logo.png"
LOGO_SMALL_PATH = ASSETS_DIR / "logo_small.png"
APP_ICO_PATH = ASSETS_DIR / "app.ico"


def lay_logo_ctk_image(size: Tuple[int, int] = (64, 64)) -> Optional[ctk.CTkImage]:
    """
    Trả về đối tượng CTkImage của Logo ứng dụng với kích thước yêu cầu.
    """
    try:
        target_path = LOGO_PNG_PATH if size[0] > 64 else LOGO_SMALL_PATH
        if not target_path.exists():
            target_path = LOGO_PNG_PATH
            
        if not target_path.exists():
            return None

        pil_img = Image.open(str(target_path))
        return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
    except Exception as e:
        print(f"[Cảnh báo Branding] Không thể nạp ảnh logo: {e}")
        return None


def cai_dat_icon_cua_so(root_window) -> None:
    """
    Thiết lập Icon cho cửa sổ Tkinter / CustomTkinter bằng file app.ico.
    Tương thích chuẩn Windows Desktop.
    """
    if not APP_ICO_PATH.exists():
        return

    try:
        # Cách 1: iconbitmap (tối ưu nhất trên Windows cho file .ico)
        root_window.iconbitmap(str(APP_ICO_PATH))
    except Exception:
        try:
            # Cách 2: wm_iconphoto fallback
            from PIL import ImageTk
            img = Image.open(str(LOGO_SMALL_PATH))
            photo = ImageTk.PhotoImage(img)
            root_window.wm_iconphoto(True, photo)
            # Lưu tham chiếu để chống GC
            root_window._app_icon_ref = photo
        except Exception as e:
            print(f"[Cảnh báo Branding] Không thể cài icon cửa sổ: {e}")
