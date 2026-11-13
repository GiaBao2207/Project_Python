"""
NEON PARKING MANAGER - TICKET MANAGEMENT VIEW
Form quản lý vé xe: Tra cứu, lọc trạng thái, xem chi tiết vé và thanh toán vé đang gửi.
Sử dụng chung BaiXeDbService với Module Quản lý xe, không sao chép nghiệp vụ.
Bảo toàn dữ liệu: Tuyệt đối không xóa cứng vé đã thanh toán khỏi CSDL.
"""

import customtkinter as ctk
from typing import Optional, List, Dict, Any
from config.theme import CyberpunkTheme
from services.bai_xe_db_service import BaiXeDbService
from gui.components.dialog import show_error, show_success, show_confirm, show_info
from gui.components.segmented_control import SegmentedControl


class TicketView(ctk.CTkFrame):
    """
    Màn hình Quản Lý Vé Xe:
    - Tìm kiếm và lọc vé theo nhiều tiêu chí
    - Bảng danh sách vé đang gửi và vé đã thanh toán
    - Xem chi tiết toàn diện thông tin vé và lịch sử thanh toán
    - Thanh toán vé trực tiếp từ danh sách vé đang gửi
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        self.danh_sach_hien_tai: List[Dict[str, Any]] = []

        # Container cuộn toàn màn hình
        self.main_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=16)

        # 1. Thanh tìm kiếm và bộ lọc trên cùng
        self._build_filter_bar()

        # 2. Hàng thống kê nhanh số lượng vé
        self._build_stats_summary()

        # 3. Bảng danh sách vé
        self._build_tickets_table()

        # Nạp dữ liệu ban đầu
        self.tai_danh_sach_ve()

    # ──────────────────────────────────────────────────────────────────────────
    # 1. THANH TÌM KIẾM VÀ BỘ LỌC
    # ──────────────────────────────────────────────────────────────────────────

    def _build_filter_bar(self) -> None:
        """Thanh công cụ tìm kiếm và lọc trạng thái vé."""
        filter_card = ctk.CTkFrame(
            self.main_scroll,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        filter_card.pack(fill="x", pady=(0, 14))

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        # Ô nhập từ khóa tìm kiếm
        lbl_search = ctk.CTkLabel(
            inner,
            text="TÌM KIẾM:",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.CYAN_NEON
        )
        lbl_search.pack(side="left", padx=(0, 8))

        self.txt_search = ctk.CTkEntry(
            inner,
            placeholder_text="Nhập biển số, mã vé, mã định danh hoặc tên chủ xe...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=36,
            width=360,
            corner_radius=8
        )
        self.txt_search.pack(side="left", padx=(0, 14))
        self.txt_search.bind("<Return>", lambda e: self.tai_danh_sach_ve())

        # Bộ lọc trạng thái vé
        lbl_filter = ctk.CTkLabel(
            inner,
            text="TRẠNG THÁI:",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.PURPLE_NEON
        )
        lbl_filter.pack(side="left", padx=(0, 8))

        self.status_var = ctk.StringVar(value="Tất cả")
        self.cbo_status = SegmentedControl(
            inner,
            values=["Tất cả", "Đang gửi", "Đã thanh toán"],
            variable=self.status_var,
            command=lambda v: self.tai_danh_sach_ve(),
            height=36
        )
        self.cbo_status.pack(side="left", padx=(0, 14))

        # Nút Tìm kiếm
        btn_search = ctk.CTkButton(
            inner,
            text="🔍 TÌM KIẾM",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            width=100,
            height=36,
            command=self.tai_danh_sach_ve
        )
        btn_search.pack(side="left", padx=(0, 8))

        # Nút Làm mới
        btn_reset = ctk.CTkButton(
            inner,
            text="🔄 LÀM MỚI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            width=80,
            height=36,
            command=self._reset_filters
        )
        btn_reset.pack(side="left")

    def _reset_filters(self) -> None:
        """Xóa trắng ô tìm kiếm và đặt lại bộ lọc trạng thái."""
        self.txt_search.delete(0, "end")
        self.cbo_status.set("Tất cả")
        self.tai_danh_sach_ve()

    # ──────────────────────────────────────────────────────────────────────────
    # 2. HÀNG THỐNG KÊ NHANH
    # ──────────────────────────────────────────────────────────────────────────

    def _build_stats_summary(self) -> None:
        """Hiển thị tổng số vé theo từng trạng thái."""
        summary_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        summary_frame.pack(fill="x", pady=(0, 14))

        self.lbl_stat_total = self._create_mini_badge(summary_frame, "TỔNG VÉ:", "0", CyberpunkTheme.TEXT_PRIMARY)
        self.lbl_stat_active = self._create_mini_badge(summary_frame, "ĐANG GỬI:", "0", CyberpunkTheme.CYAN_NEON)
        self.lbl_stat_paid = self._create_mini_badge(summary_frame, "ĐÃ THANH TOÁN:", "0", CyberpunkTheme.GREEN_NEON)

    def _create_mini_badge(self, parent, label: str, value: str, color: str) -> ctk.CTkLabel:
        """Tạo badge nhỏ hiển thị thống kê."""
        card = ctk.CTkFrame(parent, fg_color=CyberpunkTheme.SURFACE, corner_radius=8, height=36)
        card.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            card,
            text=label,
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.TEXT_MUTED
        ).pack(side="left", padx=(12, 4), pady=6)

        val_lbl = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 10, "bold"),
            text_color=color
        )
        val_lbl.pack(side="left", padx=(0, 12), pady=6)
        return val_lbl

    # ──────────────────────────────────────────────────────────────────────────
    # 3. BẢNG DANH SÁCH VÉ
    # ──────────────────────────────────────────────────────────────────────────

    def _build_tickets_table(self) -> None:
        """Tạo cấu trúc bảng danh sách vé."""
        table_card = ctk.CTkFrame(
            self.main_scroll,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        table_card.pack(fill="both", expand=True)

        # Header cột
        cols_frame = ctk.CTkFrame(table_card, fg_color=CyberpunkTheme.SURFACE_CARD, height=36, corner_radius=6)
        cols_frame.pack(fill="x", padx=16, pady=(14, 6))

        columns = [
            ("MÃ VÉ", 160),
            ("LOẠI XE", 90),
            ("BIỂN SỐ / ĐỊNH DANH", 160),
            ("CHỦ XE", 160),
            ("GIỜ VÀO", 140),
            ("GIỜ RA", 140),
            ("SỐ TIỀN", 100),
            ("TRẠNG THÁI", 120),
            ("THAO TÁC", 110)
        ]
        for title, width in columns:
            lbl = ctk.CTkLabel(
                cols_frame,
                text=title,
                font=("Segoe UI", 9, "bold"),
                text_color=CyberpunkTheme.TEXT_MUTED,
                width=width,
                anchor="center"
            )
            lbl.pack(side="left", padx=3)

        # Vùng chứa các dòng
        self.rows_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        self.rows_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # ──────────────────────────────────────────────────────────────────────────
    # 4. TRUY VẤN VÀ VẼ BẢNG
    # ──────────────────────────────────────────────────────────────────────────

    def tai_danh_sach_ve(self) -> None:
        """Truy vấn CSDL qua BaiXeDbService và hiển thị danh sách vé."""
        tu_khoa = self.txt_search.get().strip()
        trang_thai_raw = self.status_var.get()
        map_trang_thai = {
            "Tất cả": None,
            "Tat ca": None,
            "Đang gửi": "Dang gui",
            "Dang gui": "Dang gui",
            "Đã thanh toán": "Da thanh toan",
            "Da thanh toan": "Da thanh toan"
        }
        trang_thai = map_trang_thai.get(trang_thai_raw, None)

        ok, msg, danh_sach = BaiXeDbService.lay_danh_sach_ve(
            trang_thai=trang_thai,
            tu_khoa=tu_khoa if tu_khoa else None
        )
        if not ok:
            show_error(self.winfo_toplevel(), "Lỗi Truy Vấn", msg)
            return

        self.danh_sach_hien_tai = danh_sach

        # Cập nhật số liệu thống kê
        total = len(danh_sach)
        active = sum(1 for v in danh_sach if v.get("trang_thai") == "Dang gui")
        paid = sum(1 for v in danh_sach if v.get("trang_thai") == "Da thanh toan")

        self.lbl_stat_total.configure(text=str(total))
        self.lbl_stat_active.configure(text=str(active))
        self.lbl_stat_paid.configure(text=str(paid))

        # Xóa các dòng cũ
        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        if not danh_sach:
            lbl_empty = ctk.CTkLabel(
                self.rows_frame,
                text="Không tìm thấy vé xe nào phù hợp với điều kiện tìm kiếm.",
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_MUTED,
                pady=24
            )
            lbl_empty.pack(fill="x")
            return

        for item in danh_sach:
            self._render_row(item)

    def _render_row(self, item: Dict[str, Any]) -> None:
        """Vẽ một dòng vé xe."""
        row_card = ctk.CTkFrame(
            self.rows_frame,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            corner_radius=6,
            height=42
        )
        row_card.pack(fill="x", pady=2)

        # 1. Mã vé
        ctk.CTkLabel(
            row_card,
            text=item["ma_ve"],
            font=("Consolas", 9, "bold"),
            text_color=CyberpunkTheme.CYAN_NEON,
            width=160,
            anchor="center"
        ).pack(side="left", padx=3)

        # 2. Loại xe
        loai_text = item.get("ten_loai_xe", item.get("loai_xe", "—"))
        badge_color = (
            CyberpunkTheme.CYAN_NEON if item.get("loai_xe") == "XeMay"
            else CyberpunkTheme.PINK_NEON if item.get("loai_xe") == "OTo"
            else CyberpunkTheme.GREEN_NEON
        )
        ctk.CTkLabel(
            row_card,
            text=loai_text,
            font=CyberpunkTheme.FONT_SMALL,
            text_color=badge_color,
            width=90,
            anchor="center"
        ).pack(side="left", padx=3)

        # 3. Biển số / Định danh
        dinh_danh = item.get("bien_so") or item.get("ma_dinh_danh", "—")
        ctk.CTkLabel(
            row_card,
            text=dinh_danh,
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=160,
            anchor="center"
        ).pack(side="left", padx=3)

        # 4. Chủ xe
        ctk.CTkLabel(
            row_card,
            text=item.get("chu_xe", "—"),
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=160,
            anchor="center"
        ).pack(side="left", padx=3)

        # 5. Giờ vào
        gio_vao_str = str(item.get("gio_vao", "—"))[:16]
        ctk.CTkLabel(
            row_card,
            text=gio_vao_str,
            font=("Segoe UI", 8),
            text_color=CyberpunkTheme.TEXT_MUTED,
            width=140,
            anchor="center"
        ).pack(side="left", padx=3)

        # 6. Giờ ra
        gio_ra_str = str(item.get("gio_ra", "—"))[:16] if item.get("gio_ra") else "—"
        ctk.CTkLabel(
            row_card,
            text=gio_ra_str,
            font=("Segoe UI", 8),
            text_color=CyberpunkTheme.TEXT_MUTED,
            width=140,
            anchor="center"
        ).pack(side="left", padx=3)

        # 7. Số tiền
        so_tien = item.get("so_tien") or item.get("don_gia_ap_dung", 0)
        so_tien_str = f"{so_tien:,} đ" if so_tien else "0 đ"
        ctk.CTkLabel(
            row_card,
            text=so_tien_str,
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.GREEN_NEON,
            width=100,
            anchor="center"
        ).pack(side="left", padx=3)

        # 8. Trạng thái badge
        trang_thai = item.get("trang_thai", "")
        if trang_thai == "Dang gui":
            st_text = "ĐANG GỬI"
            st_color = CyberpunkTheme.CYAN_NEON
        elif trang_thai == "Da thanh toan":
            st_text = "ĐÃ THU TIỀN"
            st_color = CyberpunkTheme.GREEN_NEON
        else:
            st_text = "ĐÃ HỦY"
            st_color = CyberpunkTheme.PINK_NEON

        ctk.CTkLabel(
            row_card,
            text=st_text,
            font=("Segoe UI", 8, "bold"),
            text_color=st_color,
            width=120,
            anchor="center"
        ).pack(side="left", padx=3)

        # 9. Nút Thao tác: Chi tiết
        btn_detail = ctk.CTkButton(
            row_card,
            text="CHI TIẾT 👁",
            font=("Segoe UI", 8, "bold"),
            fg_color=CyberpunkTheme.SURFACE,
            text_color=CyberpunkTheme.PURPLE_NEON,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.PURPLE_NEON,
            corner_radius=6,
            width=96,
            height=26,
            command=lambda mv=item["ma_ve"]: self._xem_chi_tiet_ve(mv)
        )
        btn_detail.pack(side="left", padx=4)

    # ──────────────────────────────────────────────────────────────────────────
    # 5. CHI TIẾT VÉ & THANH TOÁN
    # ──────────────────────────────────────────────────────────────────────────

    def _xem_chi_tiet_ve(self, ma_ve: str) -> None:
        """Mở popup hiển thị toàn diện thông tin vé xe."""
        ok, msg, ve = BaiXeDbService.lay_chi_tiet_ve(ma_ve)
        if not ok or not ve:
            show_error(self.winfo_toplevel(), "Lỗi", msg)
            return

        dialog = ctk.CTkToplevel(self.winfo_toplevel())
        dialog.title(f"CHI TIẾT VÉ: {ma_ve}")
        dialog.geometry("540x500")
        dialog.resizable(False, False)
        dialog.configure(fg_color=CyberpunkTheme.BG_DARK)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Nội dung chi tiết
        content = ctk.CTkFrame(dialog, fg_color=CyberpunkTheme.SURFACE, corner_radius=12)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề
        ctk.CTkLabel(
            content,
            text=f"🎫 THÔNG TIN VÉ XE: {ma_ve}",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.CYAN_NEON,
            anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 12))

        ctk.CTkFrame(content, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=16, pady=(0, 12))

        # Các dòng thông tin
        details = [
            ("Mã vé:", ve["ma_ve"]),
            ("Loại phương tiện:", f"{ve.get('ten_loai_xe', ve['loai_xe'])} ({ve['loai_xe']})"),
            ("Biển số / Mã định danh:", ve.get("bien_so") or ve["ma_dinh_danh"]),
            ("Chủ phương tiện:", ve.get("chu_xe", "—")),
            ("Đơn giá snapshot:", f"{ve.get('don_gia_ap_dung', 0):,} VNĐ"),
            ("Thời gian vào:", str(ve.get("gio_vao", "—"))),
            ("Nhân viên tiếp nhận:", ve.get("ten_nv_vao") or "—"),
            ("Trạng thái vé:", ve.get("trang_thai", "—")),
            ("Thời gian ra:", str(ve.get("gio_ra", "—")) if ve.get("gio_ra") else "Chưa xuất bãi"),
            ("Nhân viên trả xe:", ve.get("ten_nv_ra") or "—"),
            ("Số tiền thanh toán:", f"{ve.get('so_tien', 0):,} VNĐ" if ve.get("so_tien") is not None else "Chưa thanh toán"),
            ("Phương thức:", ve.get("phuong_thuc") or "—"),
            ("Ghi chú:", ve.get("ghi_chu") or "—")
        ]

        for label, val in details:
            r = ctk.CTkFrame(content, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(r, text=label, font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED, width=170, anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=str(val), font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.TEXT_PRIMARY, anchor="w").pack(side="left")

        # Nút Đóng & Nút Thanh toán nhanh nếu vé đang gửi
        btn_box = ctk.CTkFrame(content, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(20, 16))

        if ve.get("trang_thai") == "Dang gui":
            btn_pay = ctk.CTkButton(
                btn_box,
                text="💳 THANH TOÁN VÉ NÀY",
                font=CyberpunkTheme.FONT_BUTTON,
                fg_color=CyberpunkTheme.PINK_NEON,
                text_color=CyberpunkTheme.TEXT_DARK,
                hover_color=CyberpunkTheme.PINK_HOVER,
                corner_radius=8,
                height=36,
                command=lambda: self._thanh_toan_tu_chi_tiet(dialog, ma_ve)
            )
            btn_pay.pack(side="left", padx=(0, 10))

        btn_close = ctk.CTkButton(
            btn_box,
            text="ĐÓNG",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            text_color=CyberpunkTheme.TEXT_MUTED,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            corner_radius=8,
            height=36,
            command=dialog.destroy
        )
        btn_close.pack(side="right")

    def _thanh_toan_tu_chi_tiet(self, parent_dialog, ma_ve: str) -> None:
        """Thực hiện thanh toán nhanh khi đang xem chi tiết vé."""
        parent_dialog.destroy()
        show_confirm(
            self.winfo_toplevel(),
            title="Xác Nhận Thanh Toán",
            message="Xác nhận thanh toán và mở cổng cho xe ra đối với vé này:",
            card_title="THÔNG TIN XÁC NHẬN",
            details=[
                ("Mã vé", ma_ve),
                ("Phương thức", "Tiền mặt")
            ],
            on_confirm=lambda: self._thuc_hien_thanh_toan(ma_ve)
        )

    def _thuc_hien_thanh_toan(self, ma_ve: str) -> None:
        """Gọi BaiXeDbService thực hiện thanh toán an toàn."""
        ok, msg, chi_tiet = BaiXeDbService.cho_xe_ra_va_tinh_tien(
            ma_ve=ma_ve,
            phuong_thuc="TIEN_MAT"
        )
        if not ok:
            show_error(
                self.winfo_toplevel(),
                title="Lỗi Thanh Toán",
                message=msg,
                card_title="CHI TIẾT LỖI GIAO DỊCH"
            )
            return

        so_tien_str = f"{chi_tiet.get('so_tien', 0):,} VNĐ" if chi_tiet else ""
        loai_hien_thi = chi_tiet.get('loai_xe', '')
        show_success(
            self.winfo_toplevel(),
            title="Thanh Toán Thành Công",
            message="Đã hoàn tất thủ tục thanh toán cho vé xe.",
            card_title="CHI TIẾT GIAO DỊCH",
            details=[
                ("Mã vé", ma_ve),
                ("Phương tiện", loai_hien_thi),
                ("Biển số / Mã thẻ", chi_tiet.get('ma_dinh_danh', '—')),
                ("Chủ xe", chi_tiet.get('chu_xe') or "Khách vãng lai"),
                ("Số tiền thu", so_tien_str),
                ("Phương thức", "Tiền mặt")
            ]
        )
        self.tai_danh_sach_ve()
