"""
NEON PARKING MANAGER - AUDIT VIEW (NHẬT KÝ HOẠT ĐỘNG HỆ THỐNG)
Màn hình truy vết Audit trail: lọc theo ngày, tài khoản, loại hành động.
Hỗ trợ phân trang để chống giật lag - Chỉ dành riêng cho ADMIN.
Tầng GUI gọi AuditService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from services.audit_service import AuditService
from gui.components.dialog import show_error


class AuditView(ctk.CTkFrame):
    """
    Giao diện Nhật ký Hoạt động hệ thống với bộ lọc nâng cao và phân trang.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        if not AuthService.la_admin():
            self._build_access_denied()
            return

        self.current_page = 1
        self.page_size = 50
        self.total_records = 0
        self.total_pages = 1
        self.user_filter_map: Dict[str, Optional[int]] = {"Tất cả người dùng": None}

        self._build_ui()
        self._nap_du_lieu_combobox()
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
            text="Phân hệ Nhật Ký Hoạt Động chỉ dành riêng cho Quản trị viên (ADMIN).\nTài khoản của bạn không có đủ thẩm quyền truy cập màn hình này.",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="center"
        ).pack(padx=24, pady=(0, 20))

    def _build_ui(self) -> None:
        """Xây dựng thanh công cụ lọc, bảng hiển thị và thanh phân trang."""
        # 1. Thanh Lọc Nâng Cao (Filter Toolbar)
        filter_card = ctk.CTkFrame(self, fg_color=CyberpunkTheme.SURFACE, corner_radius=10)
        filter_card.pack(fill="x", padx=16, pady=(12, 10))

        # Hàng 1: Bộ lọc
        row_filter = ctk.CTkFrame(filter_card, fg_color="transparent")
        row_filter.pack(fill="x", padx=14, pady=12)

        # Từ ngày
        ctk.CTkLabel(row_filter, text="Từ ngày:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.entry_tu_ngay = ctk.CTkEntry(
            row_filter,
            placeholder_text="YYYY-MM-DD",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            width=110,
            height=34
        )
        self.entry_tu_ngay.pack(side="left", padx=(0, 14))

        # Đến ngày
        ctk.CTkLabel(row_filter, text="Đến ngày:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.entry_den_ngay = ctk.CTkEntry(
            row_filter,
            placeholder_text="YYYY-MM-DD",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            width=110,
            height=34
        )
        self.entry_den_ngay.pack(side="left", padx=(0, 14))

        # Người dùng
        ctk.CTkLabel(row_filter, text="Người dùng:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.cbo_user = ctk.CTkComboBox(
            row_filter,
            values=["Tất cả người dùng"],
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            button_color=CyberpunkTheme.SURFACE_HOVER,
            button_hover_color=CyberpunkTheme.PRIMARY_CYAN,
            dropdown_fg_color=CyberpunkTheme.SURFACE,
            dropdown_text_color=CyberpunkTheme.TEXT_PRIMARY,
            dropdown_hover_color=CyberpunkTheme.SURFACE_HOVER,
            width=180,
            height=34
        )
        self.cbo_user.pack(side="left", padx=(0, 14))

        # Loại hành động
        ctk.CTkLabel(row_filter, text="Hành động:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.cbo_action = ctk.CTkComboBox(
            row_filter,
            values=["Tất cả hành động"],
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            button_color=CyberpunkTheme.SURFACE_HOVER,
            button_hover_color=CyberpunkTheme.PRIMARY_CYAN,
            dropdown_fg_color=CyberpunkTheme.SURFACE,
            dropdown_text_color=CyberpunkTheme.TEXT_PRIMARY,
            dropdown_hover_color=CyberpunkTheme.SURFACE_HOVER,
            width=180,
            height=34
        )
        self.cbo_action.pack(side="left", padx=(0, 14))

        # Nút Lọc
        btn_filter = ctk.CTkButton(
            row_filter,
            text="🔍 LỌC",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_DEEP,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            border_color=CyberpunkTheme.CYAN_BORDER,
            border_width=1,
            text_color=CyberpunkTheme.TEXT_WHITE,
            width=90,
            height=34,
            command=self._ap_dung_loc
        )
        btn_filter.pack(side="left", padx=(0, 8))

        # Nút Đặt lại
        btn_reset = ctk.CTkButton(
            row_filter,
            text="🔄 ĐẶT LẠI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=90,
            height=34,
            command=self._dat_lai_bo_loc
        )
        btn_reset.pack(side="left")

        # 2. Khung Bảng Dữ Liệu
        table_container = ctk.CTkFrame(self, fg_color=CyberpunkTheme.SURFACE, corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        # Header bảng
        tbl_header = ctk.CTkFrame(table_container, fg_color=CyberpunkTheme.SURFACE_CARD, height=38, corner_radius=6)
        tbl_header.pack(fill="x", padx=10, pady=(10, 6))

        cols = [
            ("ID", 50, "center"),
            ("THỜI GIAN", 160, "w"),
            ("NGƯỜI THỰC HIỆN", 180, "w"),
            ("LOẠI HÀNH ĐỘNG", 190, "center"),
            ("CHI TIẾT HOẠT ĐỘNG", 0, "w")
        ]
        for title, w, anchor in cols:
            if w > 0:
                lbl = ctk.CTkLabel(
                    tbl_header,
                    text=title,
                    font=CyberpunkTheme.FONT_BODY_BOLD,
                    text_color=CyberpunkTheme.CYAN_NEON,
                    width=w,
                    anchor=anchor
                )
                lbl.pack(side="left", padx=4)
            else:
                lbl = ctk.CTkLabel(
                    tbl_header,
                    text=title,
                    font=CyberpunkTheme.FONT_BODY_BOLD,
                    text_color=CyberpunkTheme.CYAN_NEON,
                    anchor=anchor
                )
                lbl.pack(side="left", fill="x", expand=True, padx=4)

        # Scrollable rows frame
        self.rows_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        self.rows_frame.pack(fill="both", expand=True, padx=6, pady=(0, 8))

        # 3. Thanh Phân Trang (Pagination Footer)
        footer = ctk.CTkFrame(self, fg_color=CyberpunkTheme.SURFACE, height=44, corner_radius=8)
        footer.pack(fill="x", padx=16, pady=(0, 10))

        self.lbl_total = ctk.CTkLabel(
            footer,
            text="Tổng số: 0 bản ghi",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        )
        self.lbl_total.pack(side="left", padx=16)

        self.btn_next = ctk.CTkButton(
            footer,
            text="TRANG SAU ▶",
            font=CyberpunkTheme.FONT_SMALL,
            width=100,
            height=28,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            command=self._trang_sau
        )
        self.btn_next.pack(side="right", padx=(6, 16))

        self.lbl_page = ctk.CTkLabel(
            footer,
            text="Trang 1 / 1",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.CYAN_NEON
        )
        self.lbl_page.pack(side="right", padx=10)

        self.btn_prev = ctk.CTkButton(
            footer,
            text="◀ TRANG TRƯỚC",
            font=CyberpunkTheme.FONT_SMALL,
            width=100,
            height=28,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            command=self._trang_truoc
        )
        self.btn_prev.pack(side="right", padx=(10, 6))

    def _nap_du_lieu_combobox(self) -> None:
        """Nạp danh sách người dùng và các loại hành động vào Combobox."""
        try:
            users = AuditService.lay_danh_sach_nguoi_dung_filter()
            u_values = ["Tất cả người dùng"]
            for u in users:
                display_str = f"{u['ho_ten']} ({u['ten_dang_nhap']})"
                u_values.append(display_str)
                self.user_filter_map[display_str] = u["id"]
            self.cbo_user.configure(values=u_values)

            actions = AuditService.lay_danh_sach_loai_hanh_dong()
            act_values = ["Tất cả hành động"] + actions
            self.cbo_action.configure(values=act_values)
        except Exception:
            pass

    def _ap_dung_loc(self) -> None:
        """Áp dụng bộ lọc và reset về trang 1."""
        self.current_page = 1
        self.tai_du_lieu()

    def _dat_lai_bo_loc(self) -> None:
        """Đặt lại toàn bộ tiêu chí lọc về mặc định."""
        self.entry_tu_ngay.delete(0, "end")
        self.entry_den_ngay.delete(0, "end")
        self.cbo_user.set("Tất cả người dùng")
        self.cbo_action.set("Tất cả hành động")
        self.current_page = 1
        self.tai_du_lieu()

    def _trang_truoc(self) -> None:
        if self.current_page > 1:
            self.current_page -= 1
            self.tai_du_lieu()

    def _trang_sau(self) -> None:
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.tai_du_lieu()

    def tai_du_lieu(self) -> None:
        """Truy vấn dữ liệu nhật ký từ AuditService và render dòng."""
        for w in self.rows_frame.winfo_children():
            w.destroy()

        tu_ngay = self.entry_tu_ngay.get().strip()
        den_ngay = self.entry_den_ngay.get().strip()

        u_sel = self.cbo_user.get()
        user_id = self.user_filter_map.get(u_sel, None)

        act_sel = self.cbo_action.get()
        hanh_dong = None if act_sel == "Tất cả hành động" else act_sel

        try:
            records, total, pages = AuditService.lay_nhat_ky(
                tu_ngay=tu_ngay if tu_ngay else None,
                den_ngay=den_ngay if den_ngay else None,
                id_nguoi_dung=user_id,
                hanh_dong=hanh_dong,
                trang=self.current_page,
                so_dong_moi_trang=self.page_size
            )
            self.total_records = total
            self.total_pages = pages
        except Exception as e:
            show_error(self, "Lỗi nạp nhật ký", f"Không thể lấy dữ liệu nhật ký: {e}")
            return

        # Cập nhật thanh phân trang
        self.lbl_total.configure(text=f"Tổng số: {self.total_records} sự kiện ghi nhận")
        self.lbl_page.configure(text=f"Trang {self.current_page} / {self.total_pages}")
        self.btn_prev.configure(state="normal" if self.current_page > 1 else "disabled")
        self.btn_next.configure(state="normal" if self.current_page < self.total_pages else "disabled")

        if not records:
            lbl_empty = ctk.CTkLabel(
                self.rows_frame,
                text="Không có bản ghi nhật ký nào thỏa mãn điều kiện lọc.",
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_MUTED
            )
            lbl_empty.pack(pady=40)
            return

        # Color map cho từng loại hành động
        action_colors = {
            "DANG_NHAP_THANH_CONG": ("#0F2D20", CyberpunkTheme.GREEN_NEON),
            "DANG_NHAP_THAT_BAI": ("#2D1218", CyberpunkTheme.PINK_NEON),
            "DANG_XUAT": ("#1E2338", CyberpunkTheme.TEXT_MUTED),
            "TIEP_NHAN_XE": ("#0D2530", CyberpunkTheme.CYAN_NEON),
            "XE_RA": ("#2A1835", CyberpunkTheme.PURPLE_NEON),
            "TAO_NHAN_VIEN": ("#0D2530", CyberpunkTheme.CYAN_NEON),
            "CAP_NHAT_NHAN_VIEN": ("#1E2338", CyberpunkTheme.TEXT_PRIMARY),
            "KHOA_TAI_KHOAN": ("#2D1218", CyberpunkTheme.PINK_NEON),
            "MO_KHOA_TAI_KHOAN": ("#0F2D20", CyberpunkTheme.GREEN_NEON),
            "CAP_NHAT_GIA": ("#2B2410", "#FFD700"),
            "CAP_NHAT_SUC_CHUA": ("#2A1835", CyberpunkTheme.PURPLE_NEON),
            "XUAT_BAO_CAO": ("#0D2530", CyberpunkTheme.CYAN_NEON),
            "RESET_MAT_KHAU": ("#2D1225", CyberpunkTheme.PINK_NEON)
        }

        for r in records:
            row_bg = CyberpunkTheme.SURFACE_INPUT if r["id"] % 2 == 0 else CyberpunkTheme.SURFACE
            row = ctk.CTkFrame(self.rows_frame, fg_color=row_bg, height=40, corner_radius=4)
            row.pack(fill="x", pady=2, padx=4)

            # ID
            ctk.CTkLabel(row, text=str(r["id"]), font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, width=50, anchor="center").pack(side="left", padx=4)

            # Thời gian
            tg = str(r.get("thoi_gian", ""))[:19]
            ctk.CTkLabel(row, text=tg, font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED, width=160, anchor="w").pack(side="left", padx=4)

            # Người thực hiện
            ten_nv = r.get("ho_ten") or r.get("ten_dang_nhap") or "Hệ thống"
            ctk.CTkLabel(row, text=ten_nv, font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_PRIMARY, width=180, anchor="w").pack(side="left", padx=4)

            # Loại hành động (Badge)
            act = r.get("hanh_dong", "")
            bg_c, text_c = action_colors.get(act, ("#1E2338", CyberpunkTheme.CYAN_NEON))

            lbl_act = ctk.CTkLabel(
                row,
                text=act,
                font=("Segoe UI", 9, "bold"),
                text_color=text_c,
                fg_color=bg_c,
                corner_radius=4,
                width=180,
                height=24
            )
            lbl_act.pack(side="left", padx=8)

            # Chi tiết hoạt động
            ctk.CTkLabel(row, text=r.get("chi_tiet") or "", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_PRIMARY, anchor="w").pack(side="left", fill="x", expand=True, padx=8)
