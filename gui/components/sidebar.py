"""
NEON PARKING MANAGER - SIDEBAR NAVIGATION COMPONENT
Thanh điều hướng bên trái giao diện: Menu động theo quyền (ADMIN / NHÂN VIÊN),
thông tin người dùng hiện tại và nút đăng xuất.
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict
from config.theme import CyberpunkTheme
from services.auth_service import AuthService


class Sidebar(ctk.CTkFrame):
    """
    Sidebar cố định bên trái, tự động lọc menu theo vai trò người dùng.
    """
    # Danh sách đầy đủ 9 module nghiệp vụ với tiêu đề chuẩn hóa tiếng Việt
    MENU_ITEMS = [
        {"id": "dashboard", "title": "Tổng quan bãi xe", "icon": "⚡", "admin_only": False},
        {"id": "vehicles", "title": "Quản lý phương tiện", "icon": "🚗", "admin_only": False},
        {"id": "tickets", "title": "Quản lý vé xe", "icon": "🎫", "admin_only": False},
        {"id": "revenue", "title": "Quản lý doanh thu", "icon": "💰", "admin_only": True},
        {"id": "statistics", "title": "Thống kê hoạt động", "icon": "📊", "admin_only": False},
        {"id": "users", "title": "Quản lý nhân viên", "icon": "👥", "admin_only": True},
        {"id": "settings", "title": "Cấu hình hệ thống", "icon": "⚙️", "admin_only": True},
        {"id": "reports", "title": "Xuất báo cáo", "icon": "📄", "admin_only": False},
        {"id": "audit", "title": "Nhật ký hệ thống", "icon": "🛡️", "admin_only": True},
    ]

    def __init__(
        self,
        master,
        on_navigate: Callable[[str], None],
        on_logout: Callable[[], None],
        on_exit: Callable[[], None],
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=CyberpunkTheme.SIDEBAR,
            width=252,
            corner_radius=0,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            **kwargs
        )
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self.on_exit = on_exit
        self.buttons: Dict[str, ctk.CTkButton] = {}
        self.active_module_id = "dashboard"

        # 1. Header Logo Sidebar
        self._build_logo()

        # 2. Vùng danh sách các nút điều hướng (Scrollable Frame)
        self.nav_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.PRIMARY_TEAL
        )
        self.nav_scroll.pack(fill="both", expand=True, padx=10, pady=(6, 10))

        # 3. Footer người dùng, Đăng xuất & Thoát
        self._build_user_footer()

        # Khởi tạo các nút menu
        self.refresh_menu()

    def _build_logo(self) -> None:
        """Logo Cyberpunk Premium đồng bộ nhận diện mới ở đầu Sidebar."""
        from gui.components.branding import lay_logo_ctk_image
        
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(16, 10))

        # Hiển thị icon logo thương hiệu đã được duyệt (Option 3 Vector Monogram)
        self.logo_img = lay_logo_ctk_image((38, 38))
        
        row_box = ctk.CTkFrame(logo_frame, fg_color="transparent")
        row_box.pack(fill="x")

        if self.logo_img:
            lbl_icon = ctk.CTkLabel(row_box, image=self.logo_img, text="")
            lbl_icon.pack(side="left", padx=(0, 10))

        text_box = ctk.CTkFrame(row_box, fg_color="transparent")
        text_box.pack(side="left", fill="both", expand=True)

        lbl_app_name = ctk.CTkLabel(
            text_box,
            text="NEON PARKING",
            font=("Segoe UI", 13, "bold"),
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            anchor="w"
        )
        lbl_app_name.pack(fill="x")

        lbl_subtitle = ctk.CTkLabel(
            text_box,
            text="MANAGER",
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.CHAMPAGNE_GOLD,
            anchor="w"
        )
        lbl_subtitle.pack(fill="x")

        # Đường viền phân cách mỏng công nghiệp
        divider = ctk.CTkFrame(self, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE)
        divider.pack(fill="x", padx=14, pady=(10, 8))

    def _build_user_footer(self) -> None:
        """Khung hiển thị thông tin ca trực và nút Đăng xuất dưới chân Sidebar."""
        # Đường viền phân cách
        divider = ctk.CTkFrame(self, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE)
        divider.pack(fill="x", padx=14, pady=(6, 10))

        user_frame = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            corner_radius=10,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        user_frame.pack(fill="x", padx=12, pady=(0, 12))

        user = AuthService.lay_nguoi_dung_hien_tai()
        ho_ten = user.ho_ten if user else "Người dùng"
        vai_tro = user.vai_tro if user else "NHAN_VIEN"
        is_admin = user.la_admin if user else False

        badge_color = CyberpunkTheme.CHAMPAGNE_GOLD if is_admin else CyberpunkTheme.SUCCESS
        badge_text = "ADMINISTRATOR" if is_admin else "NHÂN VIÊN TRỰC"

        lbl_name = ctk.CTkLabel(
            user_frame,
            text=ho_ten,
            font=CyberpunkTheme.FONT_BODY_BOLD,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            anchor="w"
        )
        lbl_name.pack(fill="x", padx=12, pady=(10, 2))

        lbl_role = ctk.CTkLabel(
            user_frame,
            text=badge_text,
            font=("Segoe UI", 8, "bold"),
            text_color=badge_color,
            anchor="w"
        )
        lbl_role.pack(fill="x", padx=12, pady=(0, 10))

        # Nút Đăng xuất ca trực
        btn_logout = ctk.CTkButton(
            self,
            text="↩  ĐĂNG XUẤT",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            height=34,
            command=self.on_logout
        )
        btn_logout.pack(fill="x", padx=12, pady=(0, 6))

        # Nút Thoát chương trình với icon Power
        btn_exit = ctk.CTkButton(
            self,
            text="⏻  THOÁT CHƯƠNG TRÌNH",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            text_color=CyberpunkTheme.ERROR,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            height=34,
            command=self.on_exit
        )
        btn_exit.pack(fill="x", padx=12, pady=(0, 14))

    def refresh_menu(self) -> None:
        """
        Vẽ lại danh sách các nút menu dựa trên quyền của người dùng đang đăng nhập.
        """
        # Xóa các nút cũ
        for widget in self.nav_scroll.winfo_children():
            widget.destroy()
        self.buttons.clear()

        is_admin = AuthService.la_admin()

        for item in self.MENU_ITEMS:
            # Nếu mục yêu cầu quyền Admin mà người dùng hiện tại không phải Admin thì bỏ qua
            if item["admin_only"] and not is_admin:
                continue

            btn = ctk.CTkButton(
                self.nav_scroll,
                text=f"{item['icon']}  {item['title']}",
                font=CyberpunkTheme.FONT_BUTTON,
                anchor="w",
                corner_radius=8,
                height=40,
                command=lambda m_id=item["id"]: self._handle_click(m_id)
            )
            btn.pack(fill="x", pady=3)
            self.buttons[item["id"]] = btn

        # Khôi phục trạng thái active
        self.set_active(self.active_module_id)

    def set_active(self, module_id: str) -> None:
        """Tô sáng nút menu đang được chọn với phong cách Light Premium Teal."""
        self.active_module_id = module_id
        for m_id, btn in self.buttons.items():
            if m_id == module_id:
                btn.configure(
                    fg_color=CyberpunkTheme.PRIMARY_TEAL,
                    text_color=CyberpunkTheme.TEXT_WHITE,
                    border_width=0,
                    hover_color=CyberpunkTheme.PRIMARY_HOVER
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=CyberpunkTheme.TEXT_MUTED,
                    border_width=0,
                    hover_color=CyberpunkTheme.SURFACE_HOVER
                )

    def _handle_click(self, module_id: str) -> None:
        self.set_active(module_id)
        if self.on_navigate:
            self.on_navigate(module_id)
