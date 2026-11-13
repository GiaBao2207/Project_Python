"""
NEON PARKING MANAGER - FIRST ADMIN SETUP VIEW
Màn hình thiết lập Quản trị viên đầu tiên khi cơ sở dữ liệu chưa có Admin.
Không cho phép đăng ký công khai và không hardcode mật khẩu mặc định.
"""

import customtkinter as ctk
from typing import Callable
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from gui.components.dialog import show_success, show_error


class SetupAdminView(ctk.CTkFrame):
    """
    Giao diện khởi tạo tài khoản Quản trị viên đầu tiên (First Admin Setup).
    """
    def __init__(
        self,
        master,
        on_setup_success: Callable[[], None],
        on_exit: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)
        self.on_setup_success = on_setup_success
        self.on_exit = on_exit

        # Container căn giữa màn hình
        center_card = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            width=520
        )
        center_card.place(relx=0.5, rely=0.5, anchor="center")

        # Nội dung bên trong Card
        content_frame = ctk.CTkFrame(center_card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=36)

        # 1. Badge & Tiêu đề
        from gui.components.branding import lay_logo_ctk_image
        self.logo_img = lay_logo_ctk_image((68, 68))
        if self.logo_img:
            lbl_logo = ctk.CTkLabel(content_frame, image=self.logo_img, text="")
            lbl_logo.pack(anchor="center", pady=(0, 10))

        badge = ctk.CTkLabel(
            content_frame,
            text="THIẾT LẬP QUẢN TRỊ VIÊN ĐẦU TIÊN",
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.CHAMPAGNE_GOLD,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            corner_radius=6,
            padx=12,
            pady=4
        )
        badge.pack(anchor="center", pady=(0, 8))

        lbl_title = ctk.CTkLabel(
            content_frame,
            text="KHỞI TẠO TÀI KHOẢN ADMIN",
            font=CyberpunkTheme.FONT_TITLE_HERO,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        )
        lbl_title.pack(anchor="center", pady=(0, 4))

        lbl_desc = ctk.CTkLabel(
            content_frame,
            text="Hệ thống bãi xe chưa có tài khoản Quản trị viên (ADMIN).\nVui lòng khởi tạo tài khoản quản trị đầu tiên để tiếp tục.",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="center"
        )
        lbl_desc.pack(anchor="center", pady=(0, 24))

        # 2. Form Nhập liệu
        # Trường 1: Tên đăng nhập
        ctk.CTkLabel(
            content_frame,
            text="TÊN ĐĂNG NHẬP",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        self.txt_username = ctk.CTkEntry(
            content_frame,
            placeholder_text="Ví dụ: admin",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=40,
            corner_radius=8
        )
        self.txt_username.pack(fill="x", pady=(0, 14))
        self.txt_username.insert(0, "admin")

        # Trường 2: Họ và tên
        ctk.CTkLabel(
            content_frame,
            text="HỌ VÀ TÊN QUẢN TRỊ VIÊN",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        self.txt_fullname = ctk.CTkEntry(
            content_frame,
            placeholder_text="Ví dụ: Quản Trị Viên Hệ Thống",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=40,
            corner_radius=8
        )
        self.txt_fullname.pack(fill="x", pady=(0, 14))

        # Trường 3: Mật khẩu
        ctk.CTkLabel(
            content_frame,
            text="MẬT KHẨU (TỐI THIỂU 6 KÝ TỰ)",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        self.txt_password = ctk.CTkEntry(
            content_frame,
            placeholder_text="Nhập mật khẩu an toàn...",
            font=CyberpunkTheme.FONT_BODY,
            show="•",
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=40,
            corner_radius=8
        )
        self.txt_password.pack(fill="x", pady=(0, 14))

        # Trường 4: Xác nhận mật khẩu
        ctk.CTkLabel(
            content_frame,
            text="XÁC NHẬN MẬT KHẨU",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        self.txt_confirm_password = ctk.CTkEntry(
            content_frame,
            placeholder_text="Nhập lại mật khẩu để xác nhận...",
            font=CyberpunkTheme.FONT_BODY,
            show="•",
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=40,
            corner_radius=8
        )
        self.txt_confirm_password.pack(fill="x", pady=(0, 10))

        # Checkbox Hiện/Ẩn mật khẩu
        self.show_pass_var = ctk.BooleanVar(value=False)
        chk_show = ctk.CTkCheckBox(
            content_frame,
            text="Hiển thị mật khẩu",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            variable=self.show_pass_var,
            command=self._toggle_show_pass,
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            fg_color=CyberpunkTheme.CYAN_NEON,
            hover_color=CyberpunkTheme.CYAN_HOVER
        )
        chk_show.pack(anchor="w", pady=(0, 16))

        # Nhãn báo lỗi
        self.lbl_error = ctk.CTkLabel(
            content_frame,
            text="",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.PINK_NEON
        )
        self.lbl_error.pack(fill="x", pady=(0, 10))

        # Nút Xác nhận (Nền Teal đậm, chữ trắng rõ ràng)
        self.btn_submit = ctk.CTkButton(
            content_frame,
            text="⚡ HOÀN TẤT THIẾT LẬP ADMIN",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=44,
            command=self._handle_submit
        )
        self.btn_submit.pack(fill="x", pady=(0, 10))

        # Nút Thoát chương trình
        if self.on_exit:
            self.btn_exit = ctk.CTkButton(
                content_frame,
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
            self.btn_exit.pack(fill="x")

        # Nhấn Enter để gửi
        self.txt_confirm_password.bind("<Return>", lambda e: self._handle_submit())

    def _toggle_show_pass(self) -> None:
        """Ẩn hoặc hiện ký tự mật khẩu."""
        is_show = self.show_pass_var.get()
        show_char = "" if is_show else "•"
        self.txt_password.configure(show=show_char)
        self.txt_confirm_password.configure(show=show_char)

    def _handle_submit(self) -> None:
        """Xử lý sự kiện bấm nút hoàn tất thiết lập Admin."""
        username = self.txt_username.get()
        fullname = self.txt_fullname.get()
        password = self.txt_password.get()
        confirm_pwd = self.txt_confirm_password.get()

        self.lbl_error.configure(text="")

        ok, msg = AuthService.thiet_lap_admin_dau_tien(
            ten_dang_nhap=username,
            ho_ten=fullname,
            mat_khau=password,
            xac_nhan_mat_khau=confirm_pwd
        )

        if not ok:
            self.lbl_error.configure(text=msg)
            return

        # Hiển thị thông báo thành công và chuyển sang màn hình đăng nhập
        show_success(
            self.winfo_toplevel(),
            title="Khởi Tạo Thành Công",
            message=f"Đã thiết lập tài khoản Quản trị viên '{username}' thành công!\nMật khẩu đã được mã hóa an toàn bằng Argon2id. Vui lòng đăng nhập."
        )
        if self.on_setup_success:
            self.on_setup_success()
