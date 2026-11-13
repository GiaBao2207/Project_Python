"""
NEON PARKING MANAGER - STAT KPI CARD COMPONENT
Thành phần thẻ KPI phát sáng phong cách Cyberpunk dùng chung cho Dashboard và Thống kê.
"""

import customtkinter as ctk
from config.theme import CyberpunkTheme


class StatCard(ctk.CTkFrame):
    """
    Thẻ hiển thị chỉ số KPI phát sáng Neon.
    """
    def __init__(
        self,
        master,
        title: str,
        value: str,
        subtitle: str = "",
        neon_color: str = CyberpunkTheme.CYAN_NEON,
        icon: str = "⚡",
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            **kwargs
        )
        self.neon_color = neon_color

        # Padding bên trong
        inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=16, pady=14)

        # Hàng trên: Tiêu đề + Icon
        top_row = ctk.CTkFrame(inner_frame, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 6))

        self.lbl_title = ctk.CTkLabel(
            top_row,
            text=title.upper(),
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        )
        self.lbl_title.pack(side="left")

        # Icon tròn nhỏ
        icon_badge = ctk.CTkLabel(
            top_row,
            text=icon,
            font=("Segoe UI", 12),
            text_color=neon_color,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            corner_radius=6,
            width=26,
            height=26
        )
        icon_badge.pack(side="right")

        # Hàng giữa: Giá trị số liệu lớn phát sáng
        self.lbl_value = ctk.CTkLabel(
            inner_frame,
            text=value,
            font=CyberpunkTheme.FONT_STAT_NUMBER,
            text_color=neon_color,
            anchor="w"
        )
        self.lbl_value.pack(fill="x", pady=(2, 4))

        # Hàng dưới: Ghi chú phụ
        self.lbl_sub = ctk.CTkLabel(
            inner_frame,
            text=subtitle,
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_sub.pack(fill="x")

        # Hiệu ứng hover nhẹ làm nổi bật viền
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def cap_nhat_gia_tri(self, value: str, subtitle: str = None) -> None:
        """Cập nhật giá trị hiển thị mới cho thẻ KPI."""
        self.lbl_value.configure(text=value)
        if subtitle is not None:
            self.lbl_sub.configure(text=subtitle)

    def _on_enter(self, event=None):
        self.configure(border_color=self.neon_color, border_width=1)

    def _on_leave(self, event=None):
        self.configure(border_color=CyberpunkTheme.BORDER_SUBTLE, border_width=1)
