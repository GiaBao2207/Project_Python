"""
NEON PARKING MANAGER - HEADER COMPONENT
Thanh điều khiển phía trên cùng: Tiêu đề trang, đồng hồ thời gian thực,
trạng thái kết nối CSDL và nút đổi mật khẩu nhanh.
"""

import time
import customtkinter as ctk
from typing import Callable, Optional
from config.theme import CyberpunkTheme
from services.auth_service import AuthService


class Header(ctk.CTkFrame):
    """
    Header cố định phía trên cùng của giao diện ứng dụng.
    """
    def __init__(
        self,
        master,
        on_change_password_clicked: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=CyberpunkTheme.SURFACE,
            height=68,
            corner_radius=0,
            border_width=0,
            **kwargs
        )
        self.pack_propagate(False)
        self.on_change_password_clicked = on_change_password_clicked

        # Khung bên trái: Icon + Tiêu đề trang & Phụ đề
        left_box = ctk.CTkFrame(self, fg_color="transparent")
        left_box.pack(side="left", padx=24, pady=10)

        title_row = ctk.CTkFrame(left_box, fg_color="transparent")
        title_row.pack(anchor="w")

        self.lbl_icon = ctk.CTkLabel(
            title_row,
            text="⚡",
            font=("Segoe UI", 16, "bold"),
            text_color=CyberpunkTheme.PRIMARY_TEAL,
            width=28
        )
        self.lbl_icon.pack(side="left", padx=(0, 6))

        self.lbl_title = ctk.CTkLabel(
            title_row,
            text="TỔNG QUAN BÃI XE",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_title.pack(side="left")

        self.lbl_subtitle = ctk.CTkLabel(
            left_box,
            text="Theo dõi hoạt động và tình trạng bãi đỗ theo thời gian thực.",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_subtitle.pack(anchor="w", padx=(34, 0))

        # Khung bên phải: Đồng hồ + Trạng thái MySQL + Nút Đổi mật khẩu
        right_box = ctk.CTkFrame(self, fg_color="transparent")
        right_box.pack(side="right", padx=24, pady=12)

        # Nút Đổi mật khẩu
        btn_key = ctk.CTkButton(
            right_box,
            text="🔑 ĐỔI MẬT KHẨU",
            font=CyberpunkTheme.FONT_SMALL,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            height=32,
            command=self._handle_change_password
        )
        btn_key.pack(side="right", padx=(12, 0))

        # Badge trạng thái MySQL
        db_badge = ctk.CTkFrame(
            right_box,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            height=32
        )
        db_badge.pack(side="right", padx=(12, 0))

        lbl_db_dot = ctk.CTkLabel(
            db_badge,
            text="●",
            font=("Segoe UI", 12, "bold"),
            text_color=CyberpunkTheme.SUCCESS
        )
        lbl_db_dot.pack(side="left", padx=(10, 4), pady=4)

        lbl_db_text = ctk.CTkLabel(
            db_badge,
            text="MYSQL ONLINE",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        )
        lbl_db_text.pack(side="left", padx=(0, 10), pady=4)

        # Đồng hồ thời gian thực
        self.lbl_clock = ctk.CTkLabel(
            right_box,
            text="",
            font=("Consolas", 12, "bold"),
            text_color=CyberpunkTheme.PRIMARY_TEAL
        )
        self.lbl_clock.pack(side="right", padx=(0, 8))

        # Bắt đầu vòng lặp cập nhật đồng hồ
        self._update_clock()

    def set_title(self, title: str, subtitle: str = "", icon: str = "") -> None:
        """Cập nhật tiêu đề hiển thị trên Header khi người dùng chuyển trang."""
        if icon:
            self.lbl_icon.configure(text=icon)
            self.lbl_icon.pack(side="left", padx=(0, 6))
        else:
            self.lbl_icon.pack_forget()

        self.lbl_title.configure(text=title)
        self.lbl_subtitle.configure(text=subtitle)

    def _update_clock(self) -> None:
        """Cập nhật đồng hồ mỗi giây một lần."""
        hien_tai = time.strftime("%H:%M:%S  |  %d/%m/%Y")
        self.lbl_clock.configure(text=hien_tai)
        self.after(1000, self._update_clock)

    def _handle_change_password(self) -> None:
        if self.on_change_password_clicked:
            self.on_change_password_clicked()
