"""
NEON PARKING MANAGER - USERS VIEW (QUẢN LÝ NHÂN VIÊN)
Màn hình quản trị tài khoản người dùng và nhân viên bãi xe.
Chỉ dành riêng cho ADMIN - Tầng GUI gọi UserService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
from typing import Optional, List
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from services.user_service import UserService
from models.nguoi_dung import NguoiDung
from gui.components.dialog import show_confirm, show_info, show_error
from gui.utils.window_helper import center_window


class UsersView(ctk.CTkFrame):
    """
    Giao diện Quản lý Nhân viên: Danh sách, Thêm mới, Sửa thông tin, Khóa/Mở khóa, Đặt lại mật khẩu.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        self.users: List[NguoiDung] = []

        # Kiểm tra quyền Admin
        if not AuthService.la_admin():
            self._build_access_denied()
            return

        self._build_ui()
        self.tai_du_lieu()

    def _build_access_denied(self) -> None:
        """Hiển thị thông báo từ chối truy cập nếu không phải Admin."""
        card = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.PINK_NEON,
            width=500,
            height=260
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text="⛔ TRUY CẬP BỊ TỪ CHỐI",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.PINK_NEON
        ).pack(pady=(36, 12))

        ctk.CTkLabel(
            card,
            text="Phân hệ Quản Lý Nhân Viên chỉ dành riêng cho Quản trị viên (ADMIN).\nTài khoản của bạn không có đủ thẩm quyền truy cập màn hình này.",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="center"
        ).pack(padx=24, pady=(0, 20))

    def _build_ui(self) -> None:
        """Xây dựng bố cục giao diện quản lý nhân viên."""
        # 1. Thanh công cụ phía trên (Search, Add, Refresh)
        toolbar = ctk.CTkFrame(self, fg_color=CyberpunkTheme.SURFACE, height=60, corner_radius=10)
        toolbar.pack(fill="x", padx=16, pady=(12, 10))

        # Ô tìm kiếm
        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Tìm theo tên đăng nhập hoặc họ tên...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=320,
            height=36
        )
        self.search_entry.pack(side="left", padx=(16, 10), pady=12)
        self.search_entry.bind("<Return>", lambda e: self.tai_du_lieu())

        btn_search = ctk.CTkButton(
            toolbar,
            text="🔍 TÌM KIẾM",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_DEEP,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            text_color=CyberpunkTheme.TEXT_WHITE,
            border_width=1,
            border_color=CyberpunkTheme.CYAN_BORDER,
            width=110,
            height=36,
            command=self.tai_du_lieu
        )
        btn_search.pack(side="left", padx=(0, 10))

        btn_refresh = ctk.CTkButton(
            toolbar,
            text="🔄 LÀM MỚI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=100,
            height=36,
            command=self.lam_moi
        )
        btn_refresh.pack(side="left", padx=(0, 10))

        # Nút Thêm nhân viên
        btn_add = ctk.CTkButton(
            toolbar,
            text="+ THÊM NHÂN VIÊN",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_DEEP,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            border_color=CyberpunkTheme.CYAN_BORDER,
            border_width=1,
            text_color=CyberpunkTheme.TEXT_WHITE,
            width=160,
            height=36,
            command=self._mo_dialog_them_nhan_vien
        )
        btn_add.pack(side="right", padx=16)

        # 2. Khung Bảng Danh Sách Người Dùng
        table_container = ctk.CTkFrame(self, fg_color=CyberpunkTheme.SURFACE, corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Header bảng
        tbl_header = ctk.CTkFrame(table_container, fg_color=CyberpunkTheme.SURFACE_CARD, height=40, corner_radius=6)
        tbl_header.pack(fill="x", padx=10, pady=(10, 6))

        cols = [
            ("ID", 50),
            ("TÊN ĐĂNG NHẬP", 150),
            ("HỌ VÀ TÊN", 200),
            ("VAI TRÒ", 120),
            ("TRẠNG THÁI", 130),
            ("NGÀY TẠO", 150),
            ("THAO TÁC", 240)
        ]
        for title, w in cols:
            lbl = ctk.CTkLabel(
                tbl_header,
                text=title,
                font=CyberpunkTheme.FONT_BODY_BOLD,
                text_color=CyberpunkTheme.CYAN_NEON if title != "THAO TÁC" else CyberpunkTheme.PINK_NEON,
                width=w,
                anchor="center" if title in ("ID", "VAI TRÒ", "TRẠNG THÁI") else ("w" if title != "THAO TÁC" else "center")
            )
            lbl.pack(side="left", padx=4)

        # Scrollable Frame chứa các dòng dữ liệu
        self.rows_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        self.rows_frame.pack(fill="both", expand=True, padx=6, pady=(0, 10))

    def lam_moi(self) -> None:
        """Đặt lại bộ lọc và nạp lại dữ liệu."""
        self.search_entry.delete(0, "end")
        self.tai_du_lieu()

    def tai_du_lieu(self) -> None:
        """Tải danh sách người dùng từ UserService và render bảng."""
        # Xóa dòng cũ
        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        kw = self.search_entry.get().strip()
        try:
            self.users = UserService.lay_danh_sach_nhan_vien(tu_khoa=kw if kw else None)
        except Exception as e:
            show_error(self, "Lỗi nạp dữ liệu", f"Không thể tải danh sách tài khoản: {e}")
            return

        if not self.users:
            lbl_empty = ctk.CTkLabel(
                self.rows_frame,
                text="Không tìm thấy tài khoản nhân viên nào.",
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_MUTED
            )
            lbl_empty.pack(pady=40)
            return

        admin_hien_tai = AuthService.lay_nguoi_dung_hien_tai()

        for u in self.users:
            self._render_row(u, admin_hien_tai)

    def _render_row(self, u: NguoiDung, admin_hien_tai: Optional[NguoiDung]) -> None:
        """Vẽ một dòng tài khoản người dùng."""
        row_bg = CyberpunkTheme.SURFACE_INPUT if u.id % 2 == 0 else CyberpunkTheme.SURFACE
        row = ctk.CTkFrame(self.rows_frame, fg_color=row_bg, height=44, corner_radius=4)
        row.pack(fill="x", pady=2, padx=4)

        # ID
        ctk.CTkLabel(row, text=str(u.id), font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, width=50, anchor="center").pack(side="left", padx=4)

        # Tên đăng nhập
        ctk.CTkLabel(row, text=u.ten_dang_nhap, font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.TEXT_PRIMARY, width=150, anchor="w").pack(side="left", padx=4)

        # Họ và tên
        ctk.CTkLabel(row, text=u.ho_ten, font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_PRIMARY, width=200, anchor="w").pack(side="left", padx=4)

        # Vai trò
        is_admin = u.la_admin
        lbl_vaitro = ctk.CTkLabel(
            row,
            text="ADMIN" if is_admin else "NHÂN VIÊN",
            font=CyberpunkTheme.FONT_SMALL,
            text_color="#9B1C1C" if is_admin else CyberpunkTheme.PRIMARY_CYAN,
            fg_color="#FDE8E8" if is_admin else "#E3F2F1",
            corner_radius=4,
            width=100,
            height=24
        )
        lbl_vaitro.pack(side="left", padx=14)

        # Trạng thái
        is_active = u.dang_hoat_dong
        lbl_status = ctk.CTkLabel(
            row,
            text="● HOẠT ĐỘNG" if is_active else "■ BỊ KHÓA",
            font=CyberpunkTheme.FONT_SMALL,
            text_color="#03543F" if is_active else "#9B1C1C",
            fg_color="#DEF7EC" if is_active else "#FDE8E8",
            corner_radius=4,
            width=110,
            height=24
        )
        lbl_status.pack(side="left", padx=10)

        # Ngày tạo
        ngay_tao_str = str(u.ngay_tao)[:16] if u.ngay_tao else ""
        ctk.CTkLabel(row, text=ngay_tao_str, font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED, width=150, anchor="w").pack(side="left", padx=4)

        # Thao tác
        actions_box = ctk.CTkFrame(row, fg_color="transparent", width=240)
        actions_box.pack(side="left", padx=4)

        # Nút Sửa
        btn_edit = ctk.CTkButton(
            actions_box,
            text="✏️ Sửa",
            font=CyberpunkTheme.FONT_SMALL,
            width=65,
            height=26,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.PRIMARY_CYAN,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            command=lambda user=u: self._mo_dialog_sua_nhan_vien(user)
        )
        btn_edit.pack(side="left", padx=2)

        # Nút Khóa / Mở khóa
        la_chinh_minh = (admin_hien_tai is not None and admin_hien_tai.id == u.id)
        if not la_chinh_minh:
            btn_lock = ctk.CTkButton(
                actions_box,
                text="🔓 Mở" if not is_active else "🔒 Khóa",
                font=CyberpunkTheme.FONT_SMALL,
                width=65,
                height=26,
                fg_color="#DEF7EC" if not is_active else "#FDE8E8",
                hover_color="#BCF0DA" if not is_active else "#FBD5D5",
                text_color="#03543F" if not is_active else "#9B1C1C",
                border_width=1,
                border_color="#99E7C0" if not is_active else "#F9B4B4",
                command=lambda user=u: self._xac_nhan_doi_trang_thai(user)
            )
            btn_lock.pack(side="left", padx=2)
        else:
            lbl_self = ctk.CTkLabel(actions_box, text="(Đang dùng)", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED, width=65)
            lbl_self.pack(side="left", padx=2)

        # Nút Đặt lại MK
        btn_reset = ctk.CTkButton(
            actions_box,
            text="🔑 Đổi MK",
            font=CyberpunkTheme.FONT_SMALL,
            width=70,
            height=26,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            command=lambda user=u: self._mo_dialog_dat_lai_mk(user)
        )
        btn_reset.pack(side="left", padx=2)

    # ─────────────────────────── DIALOGS XỬ LÝ ───────────────────────────

    def _mo_dialog_them_nhan_vien(self) -> None:
        """Mở modal dialog tạo tài khoản nhân viên mới."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("THÊM NHÂN VIÊN MỚI")
        dialog.minsize(460, 480)
        dialog.resizable(False, False)
        dialog.configure(fg_color=CyberpunkTheme.BG_DARK)
        dialog.grab_set()

        # Căn giữa popup so với cửa sổ cha
        center_window(dialog, width=460, height=480, parent=self)

        card = ctk.CTkFrame(dialog, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.PRIMARY_TEAL)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(card, text="TẠO TÀI KHOẢN NHÂN VIÊN", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.PRIMARY_TEAL).pack(pady=(16, 14))

        # Họ và tên
        ctk.CTkLabel(card, text="Họ và tên nhân viên *", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_name = ctk.CTkEntry(card, height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_name.pack(fill="x", padx=24, pady=(0, 8))

        # Tên đăng nhập
        ctk.CTkLabel(card, text="Tên đăng nhập * (viết liền không dấu)", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_user = ctk.CTkEntry(card, height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_user.pack(fill="x", padx=24, pady=(0, 8))

        # Mật khẩu
        ctk.CTkLabel(card, text="Mật khẩu khởi tạo * (tối thiểu 6 ký tự)", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_pass = ctk.CTkEntry(card, show="*", height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_pass.pack(fill="x", padx=24, pady=(0, 8))

        # Xác nhận mật khẩu
        ctk.CTkLabel(card, text="Xác nhận mật khẩu *", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_confirm = ctk.CTkEntry(card, show="*", height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_confirm.pack(fill="x", padx=24, pady=(0, 16))

        def _luu():
            ho_ten = txt_name.get().strip()
            ten_dang_nhap = txt_user.get().strip()
            mk = txt_pass.get()
            xac_nhan = txt_confirm.get()

            ok, msg = UserService.tao_nhan_vien(
                ten_dang_nhap=ten_dang_nhap,
                ho_ten=ho_ten,
                mat_khau=mk,
                xac_nhan_mat_khau=xac_nhan
            )
            if ok:
                show_info(dialog, "Thành công", msg)
                dialog.destroy()
                self.tai_du_lieu()
            else:
                show_error(dialog, "Lỗi nhập liệu", msg)

        FONT_BTN = ("Segoe UI", 13, "bold")
        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=24, pady=(0, 16))

        ctk.CTkButton(
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
            command=dialog.destroy
        ).pack(side="left")

        ctk.CTkButton(
            btn_box,
            text="LƯU TÀI KHOẢN",
            font=FONT_BTN,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=44,
            command=_luu
        ).pack(side="right", fill="x", expand=True, padx=(14, 0))

    def _mo_dialog_sua_nhan_vien(self, u: NguoiDung) -> None:
        """Mở modal dialog cập nhật thông tin nhân viên."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"SỬA TÀI KHOẢN: {u.ten_dang_nhap}")
        dialog.minsize(460, 350)
        dialog.resizable(False, False)
        dialog.configure(fg_color=CyberpunkTheme.BG_DARK)
        dialog.grab_set()

        # Căn giữa popup so với cửa sổ cha
        center_window(dialog, width=460, height=350, parent=self)

        card = ctk.CTkFrame(dialog, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.PRIMARY_TEAL)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(card, text=f"CẬP NHẬT: {u.ten_dang_nhap}", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.PRIMARY_TEAL).pack(pady=(16, 14))

        # Họ và tên
        ctk.CTkLabel(card, text="Họ và tên *", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_name = ctk.CTkEntry(card, height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_name.insert(0, u.ho_ten)
        txt_name.pack(fill="x", padx=24, pady=(0, 8))

        # Tên đăng nhập
        ctk.CTkLabel(card, text="Tên đăng nhập *", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_user = ctk.CTkEntry(card, height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_user.insert(0, u.ten_dang_nhap)
        txt_user.pack(fill="x", padx=24, pady=(0, 20))

        def _luu():
            ho_ten = txt_name.get().strip()
            ten_dang_nhap = txt_user.get().strip()

            ok, msg = UserService.sua_thong_tin_nhan_vien(
                user_id=u.id,
                ho_ten=ho_ten,
                ten_dang_nhap=ten_dang_nhap
            )
            if ok:
                show_info(dialog, "Thành công", msg)
                dialog.destroy()
                self.tai_du_lieu()
            else:
                show_error(dialog, "Lỗi cập nhật", msg)

        FONT_BTN = ("Segoe UI", 13, "bold")
        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=24, pady=(0, 16))

        ctk.CTkButton(
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
            command=dialog.destroy
        ).pack(side="left")

        ctk.CTkButton(
            btn_box,
            text="LƯU THAY ĐỔI",
            font=FONT_BTN,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=44,
            command=_luu
        ).pack(side="right", fill="x", expand=True, padx=(14, 0))

    def _xac_nhan_doi_trang_thai(self, u: NguoiDung) -> None:
        """Xác nhận và đổi trạng thái Khóa / Mở khóa."""
        hanh_dong = "khóa" if u.dang_hoat_dong else "mở khóa"
        msg = f"Bạn có chắc chắn muốn {hanh_dong} tài khoản '{u.ten_dang_nhap}'?"
        
        if show_confirm(self, f"Xác nhận {hanh_dong} tài khoản", msg):
            ok, res_msg = UserService.thay_doi_trang_thai_khoa(
                user_id=u.id,
                khoa=u.dang_hoat_dong  # Nếu đang hoạt động thì chuyển sang khóa
            )
            if ok:
                show_info(self, "Thành công", res_msg)
                self.tai_du_lieu()
            else:
                show_error(self, "Thao tác thất bại", res_msg)

    def _mo_dialog_dat_lai_mk(self, u: NguoiDung) -> None:
        """Mở modal dialog đặt lại mật khẩu cho nhân viên."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"ĐẶT LẠI MẬT KHẨU: {u.ten_dang_nhap}")
        dialog.minsize(460, 340)
        dialog.resizable(False, False)
        dialog.configure(fg_color=CyberpunkTheme.BG_DARK)
        dialog.grab_set()

        # Căn giữa popup so với cửa sổ cha
        center_window(dialog, width=460, height=340, parent=self)

        card = ctk.CTkFrame(dialog, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.PRIMARY_TEAL)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(card, text=f"ĐẶT LẠI MK: {u.ten_dang_nhap}", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.PRIMARY_TEAL).pack(pady=(16, 12))

        # Mật khẩu mới
        ctk.CTkLabel(card, text="Mật khẩu mới * (tối thiểu 6 ký tự)", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_pass = ctk.CTkEntry(card, show="*", height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_pass.pack(fill="x", padx=24, pady=(0, 8))

        # Xác nhận
        ctk.CTkLabel(card, text="Xác nhận mật khẩu mới *", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
        txt_confirm = ctk.CTkEntry(card, show="*", height=36, fg_color=CyberpunkTheme.SURFACE_INPUT)
        txt_confirm.pack(fill="x", padx=24, pady=(0, 18))

        def _luu():
            mk = txt_pass.get()
            xac_nhan = txt_confirm.get()

            ok, msg = UserService.dat_lai_mat_khau(
                user_id=u.id,
                mat_khau_moi=mk,
                xac_nhan_mat_khau=xac_nhan
            )
            if ok:
                show_info(dialog, "Thành công", msg)
                dialog.destroy()
                self.tai_du_lieu()
            else:
                show_error(dialog, "Lỗi đặt mật khẩu", msg)

        FONT_BTN = ("Segoe UI", 13, "bold")
        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=24, pady=(0, 16))

        ctk.CTkButton(
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
            command=dialog.destroy
        ).pack(side="left")

        ctk.CTkButton(
            btn_box,
            text="XÁC NHẬN ĐỔI",
            font=FONT_BTN,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=44,
            command=_luu
        ).pack(side="right", fill="x", expand=True, padx=(14, 0))
