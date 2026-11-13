"""
NEON PARKING MANAGER - MAIN WINDOW CONTROLLER
Quản lý luồng hiển thị chính: First Admin Setup -> Login -> Desktop Dashboard Shell.
Điều phối Sidebar, Header, Phân quyền và Chuyển đổi giữa các phân hệ nghiệp vụ.
"""

import customtkinter as ctk
from typing import Optional
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from models.nguoi_dung import NguoiDung

from gui.components.sidebar import Sidebar
from gui.components.header import Header
from gui.components.dialog import show_confirm
from gui.modules.auth.setup_admin_view import SetupAdminView
from gui.modules.auth.login_view import LoginView
from gui.modules.auth.change_password_dialog import ChangePasswordDialog
from gui.modules.placeholder_view import PlaceholderView, MODULE_INFO


class MainWindow(ctk.CTkFrame):
    """
    Frame điều phối toàn bộ các màn hình chính của ứng dụng Desktop.
    Được gắn trực tiếp vào cửa sổ gốc CTk.
    """
    def __init__(self, master: ctk.CTk, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)
        self.root = master
        self.sidebar: Optional[Sidebar] = None
        self.header: Optional[Header] = None
        self.content_frame: Optional[ctk.CTkFrame] = None
        self.current_view: Optional[ctk.CTkFrame] = None

        # Bắt đầu kiểm tra trạng thái khởi động
        self.kiem_tra_khoi_dong()

    def kiem_tra_khoi_dong(self) -> None:
        """
        Kiểm tra trạng thái hệ thống:
        - Nếu chưa có Admin -> Hiển thị SetupAdminView.
        - Nếu đã có Admin -> Hiển thị LoginView.
        """
        try:
            can_setup = AuthService.kiem_tra_can_setup_admin()
            if can_setup:
                self.hien_thi_setup_admin()
            else:
                self.hien_thi_login()
        except Exception as e:
            # Nếu có lỗi kết nối MySQL, hiển thị màn hình báo lỗi trực quan
            self.hien_thi_loi_ket_noi(str(e))

    def _xoa_tat_ca_giao_dien_hien_tai(self) -> None:
        """Xóa sạch các widget con trước khi chuyển trạng thái màn hình lớn."""
        for widget in self.winfo_children():
            widget.destroy()
        self.sidebar = None
        self.header = None
        self.content_frame = None
        self.current_view = None

    def hien_thi_setup_admin(self) -> None:
        """Chuyển sang màn hình First Admin Setup."""
        self._xoa_tat_ca_giao_dien_hien_tai()
        view = SetupAdminView(
            self,
            on_setup_success=self.hien_thi_login,
            on_exit=self.xac_nhan_thoat_chuong_trinh
        )
        view.pack(fill="both", expand=True)

    def hien_thi_login(self) -> None:
        """Chuyển sang màn hình Đăng nhập."""
        self._xoa_tat_ca_giao_dien_hien_tai()
        view = LoginView(
            self,
            on_login_success=self._on_login_thanh_cong,
            on_exit=self.xac_nhan_thoat_chuong_trinh
        )
        view.pack(fill="both", expand=True)

    def _on_login_thanh_cong(self, nguoi_dung: NguoiDung) -> None:
        """Khi đăng nhập thành công, khởi tạo giao diện Desktop Shell chính."""
        self.hien_thi_shell_chinh()

    def hien_thi_shell_chinh(self) -> None:
        """
        Khởi tạo giao diện làm việc chính gồm Sidebar bên trái,
        Header bên trên và Content Area bên phải.
        """
        self._xoa_tat_ca_giao_dien_hien_tai()

        # 1. Sidebar bên trái
        self.sidebar = Sidebar(
            self,
            on_navigate=self.dieu_huong_module,
            on_logout=self._xac_nhan_dang_xuat,
            on_exit=self.xac_nhan_thoat_chuong_trinh
        )
        self.sidebar.pack(side="left", fill="y")

        # 2. Khung làm việc bên phải (Header + Content Area)
        right_container = ctk.CTkFrame(self, fg_color="transparent")
        right_container.pack(side="left", fill="both", expand=True)

        # 3. Header bên trên
        self.header = Header(
            right_container,
            on_change_password_clicked=self._mo_dialog_doi_mat_khau
        )
        self.header.pack(fill="x")

        # Phân cách Header và Content Area
        divider = ctk.CTkFrame(right_container, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE)
        divider.pack(fill="x")

        # 4. Content Area
        self.content_frame = ctk.CTkFrame(right_container, fg_color=CyberpunkTheme.BG_DARK)
        self.content_frame.pack(fill="both", expand=True)

        # Điều hướng mặc định tới module Quản lý xe hoặc Dashboard
        self.dieu_huong_module("vehicles")

    def dieu_huong_module(self, module_id: str) -> None:
        """Chuyển đổi màn hình làm việc giữa các phân hệ nghiệp vụ."""
        if not self.content_frame:
            return

        # Xóa view đang mở hiện tại
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

        # Cập nhật thông tin trên Header
        info = MODULE_INFO.get(module_id, {
            "title": module_id.title(),
            "subtitle": "",
            "icon": ""
        })
        self.header.set_title(
            title=info.get("title", module_id.title()),
            subtitle=info.get("subtitle", ""),
            icon=info.get("icon", "")
        )

        # Tải view tương ứng: Toàn bộ các module nghiệp vụ kết nối MySQL
        if module_id == "vehicles":
            from gui.modules.vehicles.vehicle_view import VehicleView
            self.current_view = VehicleView(self.content_frame)
        elif module_id == "tickets":
            from gui.modules.tickets.ticket_view import TicketView
            self.current_view = TicketView(self.content_frame)
        elif module_id in ("dashboard", "parking"):
            from gui.modules.dashboard.dashboard_view import DashboardView
            self.current_view = DashboardView(self.content_frame)
        elif module_id == "revenue":
            from gui.modules.revenue.revenue_view import RevenueView
            self.current_view = RevenueView(self.content_frame)
        elif module_id == "statistics":
            from gui.modules.statistics.statistics_view import StatisticsView
            self.current_view = StatisticsView(self.content_frame)
        elif module_id == "users":
            from gui.modules.users.users_view import UsersView
            self.current_view = UsersView(self.content_frame)
        elif module_id == "settings":
            from gui.modules.settings.settings_view import SettingsView
            self.current_view = SettingsView(self.content_frame)
        elif module_id == "reports":
            from gui.modules.reports.reports_view import ReportsView
            self.current_view = ReportsView(self.content_frame)
        elif module_id == "audit":
            from gui.modules.audit.audit_view import AuditView
            self.current_view = AuditView(self.content_frame)
        else:
            self.current_view = PlaceholderView(self.content_frame, module_id=module_id)

        self.current_view.pack(fill="both", expand=True)

        # Đồng bộ trạng thái active trên Sidebar
        if self.sidebar:
            self.sidebar.set_active(module_id)

    def _xac_nhan_dang_xuat(self) -> None:
        """Hiển thị popup hỏi xác nhận trước khi đăng xuất."""
        show_confirm(
            self.root,
            title="Đăng Xuất",
            message="Bạn có chắc chắn muốn đăng xuất khỏi ca làm việc hiện tại không?",
            on_confirm=self._thuc_hien_dang_xuat
        )

    def _thuc_hien_dang_xuat(self) -> None:
        """Xóa phiên làm việc và trở về màn hình đăng nhập."""
        AuthService.dang_xuat()
        self.hien_thi_login()

    def xac_nhan_thoat_chuong_trinh(self) -> None:
        """
        Hiển thị hộp thoại CyberDialog xác nhận thoát chương trình.
        Dùng chung cho nút Thoát tại Sidebar, nút Thoát tại Login và nút X của Windows.
        """
        show_confirm(
            self.root,
            title="Thoát Chương Trình",
            message="Bạn có chắc chắn muốn thoát chương trình không?",
            on_confirm=self._thuc_hien_thoat
        )

    def _thuc_hien_thoat(self) -> None:
        """
        Đóng ứng dụng và giải phóng tài nguyên một cách an toàn.
        Không tắt dịch vụ MySQL Server.
        """
        try:
            AuthService.dang_xuat()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def _mo_dialog_doi_mat_khau(self) -> None:
        """Mở popup đổi mật khẩu."""
        ChangePasswordDialog(self.root)

    def hien_thi_loi_ket_noi(self, loi_chi_tiet: str) -> None:
        """
        Hiển thị màn hình cảnh báo lỗi kết nối MySQL trực quan kèm nút Thử lại kết nối.
        """
        self._xoa_tat_ca_giao_dien_hien_tai()

        card = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=16,
            border_width=2,
            border_color=CyberpunkTheme.PINK_NEON,
            width=580
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=36, pady=32)

        lbl_icon = ctk.CTkLabel(
            content,
            text="⚠️",
            font=("Segoe UI", 36),
            text_color=CyberpunkTheme.PINK_NEON
        )
        lbl_icon.pack(anchor="center", pady=(0, 6))

        lbl_title = ctk.CTkLabel(
            content,
            text="KHÔNG THỂ KẾT NỐI TỚI MYSQL SERVER",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.PINK_NEON
        )
        lbl_title.pack(anchor="center", pady=(0, 8))

        lbl_msg = ctk.CTkLabel(
            content,
            text=(
                f"{loi_chi_tiet}\n\n"
                "GỢI Ý KHẮC PHỤC:\n"
                "1. Kiểm tra lại thông tin máy chủ và mật khẩu trong file '.env'.\n"
                "2. Đảm bảo dịch vụ MySQL đang chạy (Dịch vụ MySQLGiaBao trong Windows Services).\n"
                "3. Đảm bảo cơ sở dữ liệu 'neon_parking_db' đã được thực thi bằng file schema.sql."
            ),
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            justify="left",
            wraplength=500
        )
        lbl_msg.pack(fill="x", pady=(0, 20))

        btn_retry = ctk.CTkButton(
            content,
            text="🔄 THỬ LẠI KẾT NỐI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_NEON,
            text_color=CyberpunkTheme.TEXT_DARK,
            hover_color=CyberpunkTheme.CYAN_HOVER,
            corner_radius=8,
            height=40,
            command=self.kiem_tra_khoi_dong
        )
        btn_retry.pack(fill="x")
