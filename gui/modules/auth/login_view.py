"""
NEON PARKING MANAGER - LOGIN VIEW
Giao diện Đăng nhập Cyberpunk Neon hiện đại, kết nối AuthService và Argon2id.
"""

import customtkinter as ctk
from typing import Callable
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from models.nguoi_dung import NguoiDung


class LoginView(ctk.CTkFrame):
    """
    Màn hình Đăng nhập phong cách Cyberpunk Neon cho Desktop.
    """
    def __init__(
        self,
        master,
        on_login_success: Callable[[NguoiDung], None],
        on_exit: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)
        self.on_login_success = on_login_success
        self.on_exit = on_exit

        # Card căn giữa màn hình
        center_card = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            width=480
        )
        center_card.place(relx=0.5, rely=0.5, anchor="center")

        content = ctk.CTkFrame(center_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=36)

        # 1. Logo & Tiêu đề
        from gui.components.branding import lay_logo_ctk_image
        self.logo_img = lay_logo_ctk_image((72, 72))
        if self.logo_img:
            lbl_logo = ctk.CTkLabel(content, image=self.logo_img, text="")
            lbl_logo.pack(anchor="center", pady=(0, 12))

        badge = ctk.CTkLabel(
            content,
            text="HỆ THỐNG XÁC THỰC BẢO MẬT",
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.PRIMARY_TEAL,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            corner_radius=6,
            padx=12,
            pady=4
        )
        badge.pack(anchor="center", pady=(0, 8))

        lbl_app = ctk.CTkLabel(
            content,
            text="NEON PARKING MANAGER",
            font=CyberpunkTheme.FONT_TITLE_HERO,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        )
        lbl_app.pack(anchor="center", pady=(0, 2))

        lbl_sub = ctk.CTkLabel(
            content,
            text="Hệ thống Quản lý Bãi xe Thông minh & Cao cấp",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        )
        lbl_sub.pack(anchor="center", pady=(0, 24))

        # 2. Form Nhập liệu
        ctk.CTkLabel(
            content,
            text="TÊN ĐĂNG NHẬP",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        self.txt_username = ctk.CTkEntry(
            content,
            placeholder_text="Nhập tên tài khoản của bạn...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=42,
            corner_radius=8
        )
        self.txt_username.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            content,
            text="MẬT KHẨU",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        self.txt_password = ctk.CTkEntry(
            content,
            placeholder_text="Nhập mật khẩu...",
            font=CyberpunkTheme.FONT_BODY,
            show="•",
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=42,
            corner_radius=8
        )
        self.txt_password.pack(fill="x", pady=(0, 10))

        # Checkbox Hiện/Ẩn mật khẩu
        self.show_pass_var = ctk.BooleanVar(value=False)
        chk_show = ctk.CTkCheckBox(
            content,
            text="Hiển thị mật khẩu",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            variable=self.show_pass_var,
            command=self._toggle_show_pass,
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            hover_color=CyberpunkTheme.PRIMARY_HOVER
        )
        chk_show.pack(anchor="w", pady=(0, 16))

        # Nhãn báo lỗi
        self.lbl_error = ctk.CTkLabel(
            content,
            text="",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.ERROR,
            wraplength=380
        )
        self.lbl_error.pack(fill="x", pady=(0, 10))

        # Nút Đăng nhập (Nền Teal đậm, chữ trắng rõ ràng)
        self.btn_login = ctk.CTkButton(
            content,
            text="ĐĂNG NHẬP HỆ THỐNG  ➔",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=44,
            command=self._handle_login
        )
        self.btn_login.pack(fill="x", pady=(0, 10))

        # Nút Thoát chương trình
        if self.on_exit:
            self.btn_exit = ctk.CTkButton(
                content,
                text="⏻  THOÁT CHƯƠNG TRÌNH",
                font=CyberpunkTheme.FONT_BUTTON,
                fg_color=CyberpunkTheme.SURFACE_CARD,
                text_color=CyberpunkTheme.ERROR,
                hover_color=CyberpunkTheme.SURFACE_HOVER,
                border_width=1,
                border_color=CyberpunkTheme.BORDER_SUBTLE,
                corner_radius=8,
                height=38,
                command=self.on_exit
            )
            self.btn_exit.pack(fill="x", pady=(0, 16))

        # Ghi chú bảo mật dưới chân
        lbl_footer = ctk.CTkLabel(
            content,
            text="Bảo mật chuẩn Argon2id • Phân quyền Admin & Nhân viên",
            font=("Segoe UI", 8),
            text_color=CyberpunkTheme.TEXT_MUTED
        )
        lbl_footer.pack(anchor="center")

        # Phím tắt Enter để đăng nhập nhanh
        self.txt_username.bind("<Return>", lambda e: self.txt_password.focus())
        self.txt_password.bind("<Return>", lambda e: self._handle_login())

        # Focus sẵn vào ô tên đăng nhập
        self.txt_username.focus()

    def _toggle_show_pass(self) -> None:
        is_show = self.show_pass_var.get()
        self.txt_password.configure(show="" if is_show else "•")

    def _handle_login(self) -> None:
        """Xử lý đăng nhập và chuyển hướng sang Dashboard."""
        username = self.txt_username.get().strip()
        password = self.txt_password.get()

        self.lbl_error.configure(text="")

        ok, msg, user = AuthService.dang_nhap(username, password)
        if not ok or not user:
            self.lbl_error.configure(text=msg)
            return

        # Gọi callback thông báo đăng nhập thành công
        if self.on_login_success:
            self.on_login_success(user)
