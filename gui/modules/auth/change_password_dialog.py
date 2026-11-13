"""
NEON PARKING MANAGER - CHANGE PASSWORD DIALOG
Hộp thoại đổi mật khẩu tài khoản người dùng hiện tại (CTkToplevel).
"""

import customtkinter as ctk
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from gui.components.dialog import show_success
from gui.utils.window_helper import center_window


class ChangePasswordDialog(ctk.CTkToplevel):
    """
    Cửa sổ popup đổi mật khẩu phong cách Cyberpunk Neon.
    """
    def __init__(self, parent: ctk.CTk):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()

        self.title("Đổi Mật Khẩu Tài Khoản")
        self.minsize(440, 420)
        self.resizable(False, False)
        self.configure(fg_color=CyberpunkTheme.BG_DARK)

        # Căn giữa so với parent bằng tiện ích center_window
        center_window(self, width=460, height=430, parent=parent)

        # Frame chính
        card = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.CYAN_NEON
        )
        card.pack(fill="both", expand=True, padx=14, pady=14)

        # Tiêu đề
        lbl_head = ctk.CTkLabel(
            card,
            text="🔑 ĐỔI MẬT KHẨU TÀI KHOẢN",
            font=CyberpunkTheme.FONT_TITLE_SECTION,
            text_color=CyberpunkTheme.CYAN_NEON
        )
        lbl_head.pack(anchor="w", padx=20, pady=(16, 4))

        user = AuthService.lay_nguoi_dung_hien_tai()
        user_info = f"Tài khoản: {user.ten_dang_nhap} ({user.vai_tro_tieng_viet})" if user else ""
        ctk.CTkLabel(
            card,
            text=user_info,
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        ).pack(anchor="w", padx=20, pady=(0, 14))

        # Phân cách
        ctk.CTkFrame(card, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=20, pady=(0, 12))

        # 1. Mật khẩu cũ
        ctk.CTkLabel(
            card,
            text="MẬT KHẨU HIỆN TẠI",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=20, pady=(0, 2))

        self.txt_old_pwd = ctk.CTkEntry(
            card,
            placeholder_text="Nhập mật khẩu hiện tại...",
            font=CyberpunkTheme.FONT_BODY,
            show="•",
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            height=36
        )
        self.txt_old_pwd.pack(fill="x", padx=20, pady=(0, 10))

        # 2. Mật khẩu mới
        ctk.CTkLabel(
            card,
            text="MẬT KHẨU MỚI (TỐI THIỂU 6 KÝ TỰ)",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=20, pady=(0, 2))

        self.txt_new_pwd = ctk.CTkEntry(
            card,
            placeholder_text="Nhập mật khẩu mới...",
            font=CyberpunkTheme.FONT_BODY,
            show="•",
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            height=36
        )
        self.txt_new_pwd.pack(fill="x", padx=20, pady=(0, 10))

        # 3. Xác nhận mật khẩu mới
        ctk.CTkLabel(
            card,
            text="XÁC NHẬN MẬT KHẨU MỚI",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=20, pady=(0, 2))

        self.txt_confirm_pwd = ctk.CTkEntry(
            card,
            placeholder_text="Nhập lại mật khẩu mới...",
            font=CyberpunkTheme.FONT_BODY,
            show="•",
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            height=36
        )
        self.txt_confirm_pwd.pack(fill="x", padx=20, pady=(0, 8))

        # Nhãn báo lỗi
        self.lbl_error = ctk.CTkLabel(
            card,
            text="",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.PINK_NEON
        )
        self.lbl_error.pack(fill="x", padx=20, pady=(0, 8))

        # Nút bấm Xác nhận / Hủy
        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(6, 18))

        FONT_BTN = ("Segoe UI", 13, "bold")

        btn_save = ctk.CTkButton(
            btn_box,
            text="CẬP NHẬT MẬT KHẨU",
            font=FONT_BTN,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            width=180,
            height=44,
            command=self._handle_change
        )
        btn_save.pack(side="right", padx=(14, 0))

        btn_cancel = ctk.CTkButton(
            btn_box,
            text="HỦY BỎ",
            font=FONT_BTN,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            width=120,
            height=44,
            command=self.destroy
        )
        btn_cancel.pack(side="right")

    def _handle_change(self) -> None:
        old_pwd = self.txt_old_pwd.get()
        new_pwd = self.txt_new_pwd.get()
        confirm_pwd = self.txt_confirm_pwd.get()

        self.lbl_error.configure(text="")

        ok, msg = AuthService.doi_mat_khau(old_pwd, new_pwd, confirm_pwd)
        if not ok:
            self.lbl_error.configure(text=msg)
            return

        self.destroy()
        show_success(
            self.master,
            title="Thành Công",
            message="Đã cập nhật mật khẩu mới thành công!\nVui lòng ghi nhớ mật khẩu mới cho những lần đăng nhập sau."
        )
