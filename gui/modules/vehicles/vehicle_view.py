"""
NEON PARKING MANAGER - VEHICLE MANAGEMENT VIEW
Form quản lý tiếp nhận xe, xử lý xe ra và danh sách xe đang gửi trong bãi.
Tuân thủ chuẩn phân tầng: Tương tác 100% qua BaiXeDbService, không viết SQL trực tiếp.
Giao diện tối ưu độ tương phản Cyberpunk Neon: chữ trắng (#FFFFFF) trên nền cyan đậm (#009FB3).
"""

import math
import datetime
import customtkinter as ctk
from typing import Optional, List, Dict, Any
from config.theme import CyberpunkTheme
from services.bai_xe_db_service import BaiXeDbService
from gui.components.dialog import show_error, show_success, show_confirm, show_info
from gui.components.segmented_control import SegmentedControl

# Ánh xạ tên tiếng Việt hiển thị sang mã nghiệp vụ backend và ngược lại
MAP_HIEN_THI_LOAI_XE = {
    "Xe máy": "XeMay",
    "Ô tô": "OTo",
    "Xe đạp": "XeDap"
}

MAP_MA_SANG_HIEN_THI = {
    "XeMay": "Xe máy",
    "OTo": "Ô tô",
    "XeDap": "Xe đạp"
}

MAP_HIEN_THI_LOC = {
    "Tất cả": None,
    "Xe máy": "XeMay",
    "Ô tô": "OTo",
    "Xe đạp": "XeDap"
}

MAP_HIEN_THI_PHUONG_THUC = {
    "Tiền mặt": "TIEN_MAT",
    "Chuyển khoản": "CHUYEN_KHOAN"
}

MAP_MA_SANG_PT = {
    "TIEN_MAT": "Tiền mặt",
    "CHUYEN_KHOAN": "Chuyển khoản"
}


class VehicleView(ctk.CTkFrame):
    """
    Màn hình Quản Lý Xe:
    - Bảng thông tin xe đang gửi theo thời gian thực (hỗ trợ tìm kiếm, lọc loại xe, phân trang)
    - Form tiếp nhận xe vào bãi (Check-in)
    - Form xử lý xe ra & thanh toán (Check-out)
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        # Trạng thái phân trang và tìm kiếm
        self.so_dong_moi_trang = 10
        self.trang_hien_tai = 1
        self.tong_so_xe = 0
        self.tong_so_trang = 1
        self.selected_ma_ve: Optional[str] = None
        self.row_widgets: Dict[str, ctk.CTkFrame] = {}
        self._search_timer: Optional[str] = None

        # Container cuộn toàn màn hình
        self.main_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_BORDER
        )
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=16)

        # 1. Hàng trên: 2 Form thao tác (Tiếp nhận xe & Cho xe ra)
        self._build_forms_section()

        # 2. Hàng dưới: Bảng danh sách xe đang gửi trong bãi (có thanh tìm kiếm và phân trang)
        self._build_table_section()

        # Nạp dữ liệu ban đầu
        self.tai_lai_danh_sach()

    # ──────────────────────────────────────────────────────────────────────────
    # 1. KHU VỰC CÁC FORM THAO TÁC
    # ──────────────────────────────────────────────────────────────────────────

    def _build_forms_section(self) -> None:
        """Tạo 2 thẻ Card: Form Tiếp nhận xe (trái) và Form Xe ra (phải)."""
        forms_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        forms_container.pack(fill="x", pady=(0, 20))

        # ─── FORM 1: TIẾP NHẬN XE VÀO BÃI ───
        in_card = ctk.CTkFrame(
            forms_container,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.CYAN_BORDER
        )
        in_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        in_inner = ctk.CTkFrame(in_card, fg_color="transparent")
        in_inner.pack(fill="both", expand=True, padx=20, pady=18)

        # Tiêu đề Form
        ctk.CTkLabel(
            in_inner,
            text="TIẾP NHẬN PHƯƠNG TIỆN",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.PRIMARY_TEAL,
            anchor="w"
        ).pack(fill="x", pady=(0, 12))

        # Chọn Loại xe (tiếng Việt có dấu, chữ trắng, nền cyan đậm tương phản cao)
        ctk.CTkLabel(
            in_inner,
            text="LOẠI PHƯƠNG TIỆN",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.loai_xe_hien_thi_var = ctk.StringVar(value="Xe máy")
        self.cbo_loai_xe = SegmentedControl(
            in_inner,
            values=["Xe máy", "Ô tô", "Xe đạp"],
            variable=self.loai_xe_hien_thi_var,
            command=self._on_loai_xe_changed,
            height=38
        )
        self.cbo_loai_xe.pack(fill="x", pady=(0, 10))

        # Nhập Biển số / Mã định danh
        self.lbl_bien_so = ctk.CTkLabel(
            in_inner,
            text="BIỂN SỐ XE (BẮT BUỘC CHO XE MÁY / Ô TÔ)",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_bien_so.pack(fill="x", pady=(0, 4))

        self.txt_ma_dinh_danh = ctk.CTkEntry(
            in_inner,
            placeholder_text="Nhập biển số xe (VD: 29A-123.45)...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=8
        )
        self.txt_ma_dinh_danh.pack(fill="x", pady=(0, 10))

        # Nhập Tên chủ xe
        ctk.CTkLabel(
            in_inner,
            text="HỌ TÊN CHỦ XE / NGƯỜI GỬI",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.txt_chu_xe = ctk.CTkEntry(
            in_inner,
            placeholder_text="Họ và tên chủ xe (VD: Nguyễn Văn A)...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=8
        )
        self.txt_chu_xe.pack(fill="x", pady=(0, 14))

        # Nút bấm Tiếp nhận (Nền Teal #087F83, hover #096B70, chữ trắng #FFFFFF)
        self.btn_tiep_nhan = ctk.CTkButton(
            in_inner,
            text="📥 TIẾP NHẬN PHƯƠNG TIỆN",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=40,
            command=self._handle_tiep_nhan
        )
        self.btn_tiep_nhan.pack(fill="x")

        # ─── FORM 2: XE RA & THANH TOÁN ───
        out_card = ctk.CTkFrame(
            forms_container,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        out_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        out_inner = ctk.CTkFrame(out_card, fg_color="transparent")
        out_inner.pack(fill="both", expand=True, padx=20, pady=18)

        # Tiêu đề Form
        ctk.CTkLabel(
            out_inner,
            text="XỬ LÝ XE RA & THANH TOÁN",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.SUCCESS,
            anchor="w"
        ).pack(fill="x", pady=(0, 12))

        # Nhập Mã vé cần thanh toán (Không thêm thanh tìm kiếm thứ 2 vào form này)
        ctk.CTkLabel(
            out_inner,
            text="MÃ VÉ CẦN THANH TOÁN (HOẶC CHỌN TỪ BẢNG DƯỚI)",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.txt_ma_ve_out = ctk.CTkEntry(
            out_inner,
            placeholder_text="Mã vé (VD: VX-20261014-A1B2C3)...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=8
        )
        self.txt_ma_ve_out.pack(fill="x", pady=(0, 10))

        # Phương thức thanh toán (Tiếng Việt có dấu, chữ trắng, tương phản cao)
        ctk.CTkLabel(
            out_inner,
            text="PHƯƠNG THỨC THANH TOÁN",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.phuong_thuc_hien_thi_var = ctk.StringVar(value="Tiền mặt")
        self.cbo_phuong_thuc = SegmentedControl(
            out_inner,
            values=["Tiền mặt", "Chuyển khoản"],
            variable=self.phuong_thuc_hien_thi_var,
            height=38
        )
        self.cbo_phuong_thuc.pack(fill="x", pady=(0, 10))

        # Ghi chú tùy chọn
        ctk.CTkLabel(
            out_inner,
            text="GHI CHÚ THANH TOÁN (TÙY CHỌN)",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.txt_ghi_chu = ctk.CTkEntry(
            out_inner,
            placeholder_text="Ghi chú thêm nếu có...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=8
        )
        self.txt_ghi_chu.pack(fill="x", pady=(0, 14))

        # Nút bấm Xác nhận trả xe (Chữ trắng #FFFFFF trên nền Success #268667)
        self.btn_xe_ra = ctk.CTkButton(
            out_inner,
            text="💳 XÁC NHẬN THANH TOÁN & CHO XE RA",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SUCCESS,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.SUCCESS_HOVER,
            corner_radius=8,
            height=40,
            command=self._handle_xe_ra
        )
        self.btn_xe_ra.pack(fill="x")

    def _on_loai_xe_changed(self, value: str) -> None:
        """Cập nhật gợi ý placeholder linh hoạt theo loại xe."""
        loai_ma = MAP_HIEN_THI_LOAI_XE.get(value, "XeMay")
        if loai_ma == "XeDap":
            self.lbl_bien_so.configure(text="MÃ THẺ XE ĐẠP (MÃ ĐỊNH DANH)")
            self.txt_ma_dinh_danh.configure(placeholder_text="Mã thẻ xe đạp (VD: XD-001)...")
        else:
            self.lbl_bien_so.configure(text="BIỂN SỐ XE (BẮT BUỘC CHO XE MÁY / Ô TÔ)")
            self.txt_ma_dinh_danh.configure(placeholder_text="Biển số xe (VD: 29A-123.45)...")

    # ──────────────────────────────────────────────────────────────────────────
    # 2. BẢNG DANH SÁCH XE ĐANG GỬI (KÈM THANH TÌM KIẾM, BỘ LỌC VÀ PHÂN TRANG)
    # ──────────────────────────────────────────────────────────────────────────

    def _build_table_section(self) -> None:
        """Tạo Card chứa bảng danh sách xe đang gửi theo thời gian thực."""
        table_card = ctk.CTkFrame(
            self.main_scroll,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        table_card.pack(fill="both", expand=True)

        header_bar = ctk.CTkFrame(table_card, fg_color="transparent")
        header_bar.pack(fill="x", padx=20, pady=(16, 10))

        # Tiêu đề bảng & Badge đếm số lượng
        left_head = ctk.CTkFrame(header_bar, fg_color="transparent")
        left_head.pack(side="left")

        ctk.CTkLabel(
            left_head,
            text="🚗 DANH SÁCH PHƯƠNG TIỆN ĐANG GỬI TRONG BÃI",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 10))

        self.lbl_so_luong = ctk.CTkLabel(
            left_head,
            text="0 XE",
            font=("Segoe UI", 10, "bold"),
            text_color=CyberpunkTheme.CYAN_BORDER,
            fg_color="#E3F2F1",
            corner_radius=6,
            padx=10,
            pady=3
        )
        self.lbl_so_luong.pack(side="left")

        # ─── THANH TÌM KIẾM & BỘ LỌC LOẠI XE (PHÍA TRÊN BẢNG) ───
        search_filter_bar = ctk.CTkFrame(table_card, fg_color="transparent")
        search_filter_bar.pack(fill="x", padx=20, pady=(0, 12))

        # Khung nhập tìm kiếm với nút X xóa nhanh
        search_box = ctk.CTkFrame(search_filter_bar, fg_color="transparent")
        search_box.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.txt_tim_kiem = ctk.CTkEntry(
            search_box,
            placeholder_text="🔍 Tìm kiếm theo mã vé, biển số, mã thẻ hoặc tên chủ xe...",
            font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            height=36,
            corner_radius=8
        )
        self.txt_tim_kiem.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.txt_tim_kiem.bind("<Return>", lambda e: self._on_tim_kiem())
        self.txt_tim_kiem.bind("<KeyRelease>", lambda e: self._on_tim_kiem_debounce())

        # Nút X để xóa từ khóa tìm kiếm (chữ màu tối tương phản cao)
        btn_clear = ctk.CTkButton(
            search_box,
            text="✕",
            font=("Segoe UI", 11, "bold"),
            fg_color=CyberpunkTheme.SURFACE_CARD,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=8,
            width=36,
            height=36,
            command=self._xoa_tu_khoa
        )
        btn_clear.pack(side="left")

        # Bộ lọc loại xe (Tất cả, Xe máy, Ô tô, Xe đạp)
        self.loai_xe_loc_var = ctk.StringVar(value="Tất cả")
        self.cbo_loc_loai = SegmentedControl(
            search_filter_bar,
            values=["Tất cả", "Xe máy", "Ô tô", "Xe đạp"],
            variable=self.loai_xe_loc_var,
            command=self._on_bo_loc_changed,
            height=36
        )
        self.cbo_loc_loai.pack(side="left", padx=(0, 10))

        # Nút Làm mới dữ liệu (Chữ trắng, nền Teal #087F83)
        btn_refresh = ctk.CTkButton(
            search_filter_bar,
            text="🔄 LÀM MỚI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=36,
            width=110,
            command=self.tai_lai_danh_sach
        )
        btn_refresh.pack(side="right")

        # Phân cách
        ctk.CTkFrame(table_card, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=16, pady=(0, 8))

        # Tiêu đề các cột trong bảng bằng tiếng Việt chuẩn
        cols_frame = ctk.CTkFrame(table_card, fg_color=CyberpunkTheme.SURFACE_CARD, height=36, corner_radius=6)
        cols_frame.pack(fill="x", padx=16, pady=(0, 6))

        columns = [
            ("MÃ VÉ", 160),
            ("LOẠI XE", 110),
            ("BIỂN SỐ / MÃ THẺ", 170),
            ("CHỦ XE", 180),
            ("THỜI GIAN VÀO", 160),
            ("ĐƠN GIÁ", 110),
            ("THAO TÁC", 110)
        ]
        for title, width in columns:
            lbl = ctk.CTkLabel(
                cols_frame,
                text=title,
                font=("Segoe UI", 9, "bold"),
                text_color="#526579",
                width=width,
                anchor="center"
            )
            lbl.pack(side="left", padx=4)

        # Khung chứa các dòng dữ liệu (Rows container)
        self.rows_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        self.rows_frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        # ─── THANH PHÂN TRANG (PAGINATION BAR) ───
        self.pagination_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        self.pagination_frame.pack(fill="x", padx=20, pady=(0, 16))

        # Thông tin số lượng hiển thị
        self.lbl_phan_trang_info = ctk.CTkLabel(
            self.pagination_frame,
            text="Đang tải dữ liệu...",
            font=CyberpunkTheme.FONT_SMALL,
            text_color="#526579"
        )
        self.lbl_phan_trang_info.pack(side="left")

        # Nút chuyển trang bên phải
        pagi_controls = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        pagi_controls.pack(side="right")

        self.btn_trang_truoc = ctk.CTkButton(
            pagi_controls,
            text="◀ Trang trước",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_DEEP,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.CYAN_BORDER,
            corner_radius=6,
            width=100,
            height=30,
            command=lambda: self._chuyen_trang(-1)
        )
        self.btn_trang_truoc.pack(side="left", padx=(0, 8))

        self.lbl_trang_hien_tai = ctk.CTkLabel(
            pagi_controls,
            text="Trang 1 / 1",
            font=CyberpunkTheme.FONT_BODY_BOLD,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=90,
            anchor="center"
        )
        self.lbl_trang_hien_tai.pack(side="left", padx=(0, 8))

        self.btn_trang_sau = ctk.CTkButton(
            pagi_controls,
            text="Trang sau ▶",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_DEEP,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.CYAN_BORDER,
            corner_radius=6,
            width=100,
            height=30,
            command=lambda: self._chuyen_trang(1)
        )
        self.btn_trang_sau.pack(side="left")

    # ──────────────────────────────────────────────────────────────────────────
    # 3. TÌM KIẾM, BỘ LỌC & PHÂN TRANG
    # ──────────────────────────────────────────────────────────────────────────

    def _on_tim_kiem_debounce(self) -> None:
        """Debounce 300ms khi người dùng gõ từ khóa tìm kiếm."""
        if self._search_timer:
            self.after_cancel(self._search_timer)
        self._search_timer = self.after(300, self._on_tim_kiem)

    def _on_tim_kiem(self) -> None:
        """Kích hoạt tìm kiếm, đưa về trang 1."""
        self._search_timer = None
        self.trang_hien_tai = 1
        self.tai_lai_danh_sach()

    def _xoa_tu_khoa(self) -> None:
        """Xóa trắng ô tìm kiếm và tải lại danh sách phương tiện."""
        self.txt_tim_kiem.delete(0, "end")
        self.trang_hien_tai = 1
        self.tai_lai_danh_sach()

    def _on_bo_loc_changed(self, value: str) -> None:
        """Xử lý khi người dùng chọn lọc loại xe khác."""
        self.trang_hien_tai = 1
        self.tai_lai_danh_sach()

    def _chuyen_trang(self, huong: int) -> None:
        """Chuyển sang trang trước (-1) hoặc trang kế tiếp (+1)."""
        self.trang_hien_tai += huong
        self.tai_lai_danh_sach()

    # ──────────────────────────────────────────────────────────────────────────
    # 4. XỬ LÝ SỰ KIỆN & KẾT NỐI SERVICE
    # ──────────────────────────────────────────────────────────────────────────

    def tai_lai_danh_sach(self) -> None:
        """Đọc danh sách xe đang gửi từ MySQL qua BaiXeDbService và hiển thị."""
        # Xóa các dòng cũ và reset bộ nhớ widget dòng
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        self.row_widgets.clear()

        # Lấy từ khóa và bộ lọc loại xe
        tu_khoa = self.txt_tim_kiem.get().strip() if hasattr(self, "txt_tim_kiem") else ""
        loai_hien_thi = self.loai_xe_loc_var.get() if hasattr(self, "loai_xe_loc_var") else "Tất cả"
        loai_ma = MAP_HIEN_THI_LOC.get(loai_hien_thi, None)

        # Tính tổng số xe thỏa mãn điều kiện
        self.tong_so_xe = BaiXeDbService.dem_so_luong_xe_dang_gui(tu_khoa=tu_khoa, loai_xe=loai_ma)
        self.tong_so_trang = max(1, math.ceil(self.tong_so_xe / self.so_dong_moi_trang))

        # Đảm bảo trang hiện tại hợp lệ
        if self.trang_hien_tai > self.tong_so_trang:
            self.trang_hien_tai = self.tong_so_trang
        if self.trang_hien_tai < 1:
            self.trang_hien_tai = 1

        offset = (self.trang_hien_tai - 1) * self.so_dong_moi_trang

        # Lấy dữ liệu phân trang từ Service
        ok, msg, danh_sach = BaiXeDbService.lay_danh_sach_xe_dang_gui(
            tu_khoa=tu_khoa,
            loai_xe=loai_ma,
            limit=self.so_dong_moi_trang,
            offset=offset
        )

        if not ok:
            show_error(self.winfo_toplevel(), "Lỗi Tải Dữ Liệu", msg)
            return

        # Cập nhật Badge số lượng tổng
        self.lbl_so_luong.configure(text=f"{self.tong_so_xe} XE")

        # Cập nhật thanh phân trang
        if self.tong_so_xe == 0:
            self.lbl_phan_trang_info.configure(text="Không có phương tiện nào phù hợp với bộ lọc hiện tại.")
            self.lbl_trang_hien_tai.configure(text="Trang 1 / 1")
            self.btn_trang_truoc.configure(state="disabled")
            self.btn_trang_sau.configure(state="disabled")
        else:
            bat_dau = offset + 1
            ket_thuc = min(offset + len(danh_sach), self.tong_so_xe)
            self.lbl_phan_trang_info.configure(
                text=f"Hiển thị {bat_dau} - {ket_thuc} trên tổng số {self.tong_so_xe} xe đang gửi"
            )
            self.lbl_trang_hien_tai.configure(text=f"Trang {self.trang_hien_tai} / {self.tong_so_trang}")
            self.btn_trang_truoc.configure(state="normal" if self.trang_hien_tai > 1 else "disabled")
            self.btn_trang_sau.configure(state="normal" if self.trang_hien_tai < self.tong_so_trang else "disabled")

        if not danh_sach:
            lbl_empty = ctk.CTkLabel(
                self.rows_frame,
                text="Không tìm thấy phương tiện nào đang gửi trong bãi thỏa mãn điều kiện.",
                font=CyberpunkTheme.FONT_BODY,
                text_color="#526579",
                pady=24
            )
            lbl_empty.pack(fill="x")
            return

        for item in danh_sach:
            self._render_row(item)

    def _render_row(self, item: Dict[str, Any]) -> None:
        """Vẽ một dòng thông tin xe đang gửi với nút bấm thao tác nhanh và bắt sự kiện click / double-click."""
        ma_ve = item["ma_ve"]
        is_selected = (self.selected_ma_ve == ma_ve)

        row_card = ctk.CTkFrame(
            self.rows_frame,
            fg_color="#E8F4F5" if is_selected else CyberpunkTheme.SURFACE_CARD,
            border_width=1 if is_selected else 0,
            border_color=CyberpunkTheme.CYAN_BORDER if is_selected else CyberpunkTheme.BORDER_SUBTLE,
            corner_radius=6,
            height=42
        )
        row_card.pack(fill="x", pady=2)
        self.row_widgets[ma_ve] = row_card

        # 1. Mã vé
        lbl_ma_ve = ctk.CTkLabel(
            row_card,
            text=ma_ve,
            font=("Consolas", 10, "bold"),
            text_color=CyberpunkTheme.CYAN_BORDER,
            width=160,
            anchor="center"
        )
        lbl_ma_ve.pack(side="left", padx=4)

        # 2. Loại xe
        loai_ma = item["loai_xe"]
        loai_text = MAP_MA_SANG_HIEN_THI.get(loai_ma, item.get("ten_loai_xe", loai_ma))
        badge_color = (
            CyberpunkTheme.CYAN_BORDER if loai_ma == "XeMay"
            else CyberpunkTheme.PINK_NEON if loai_ma == "OTo"
            else CyberpunkTheme.GREEN_NEON
        )
        lbl_loai = ctk.CTkLabel(
            row_card,
            text=loai_text,
            font=CyberpunkTheme.FONT_BODY_BOLD,
            text_color=badge_color,
            width=110,
            anchor="center"
        )
        lbl_loai.pack(side="left", padx=4)

        # 3. Biển số / Mã định danh (Chữ đậm màu tối #162A35 tương phản cao trên nền sáng)
        dinh_danh = item.get("bien_so") or item["ma_dinh_danh"]
        lbl_bien = ctk.CTkLabel(
            row_card,
            text=dinh_danh,
            font=("Segoe UI", 10, "bold"),
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=170,
            anchor="center"
        )
        lbl_bien.pack(side="left", padx=4)

        # 4. Chủ xe
        lbl_chu = ctk.CTkLabel(
            row_card,
            text=item.get("chu_xe", "—"),
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            width=180,
            anchor="center"
        )
        lbl_chu.pack(side="left", padx=4)

        # 5. Giờ vào
        gio_vao_str = "—"
        if item.get("gio_vao"):
            gio_vao_str = str(item["gio_vao"])[:16]
        lbl_gio = ctk.CTkLabel(
            row_card,
            text=gio_vao_str,
            font=CyberpunkTheme.FONT_SMALL,
            text_color="#526579",
            width=160,
            anchor="center"
        )
        lbl_gio.pack(side="left", padx=4)

        # 6. Đơn giá
        gia_str = f"{item.get('don_gia_ap_dung', 0):,} đ"
        lbl_gia = ctk.CTkLabel(
            row_card,
            text=gia_str,
            font=("Segoe UI", 10, "bold"),
            text_color=CyberpunkTheme.GREEN_NEON,
            width=110,
            anchor="center"
        )
        lbl_gia.pack(side="left", padx=4)

        # 7. Nút Chọn vé (Nền cyan đậm #087F83, chữ trắng #FFFFFF sắc nét)
        btn_select = ctk.CTkButton(
            row_card,
            text="Chọn vé ➔",
            font=("Segoe UI", 9, "bold"),
            fg_color=CyberpunkTheme.CYAN_DEEP,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            border_width=1,
            border_color=CyberpunkTheme.CYAN_BORDER,
            corner_radius=6,
            width=90,
            height=28,
            command=lambda mv=ma_ve: self._chon_ve_thanh_toan(mv)
        )
        btn_select.pack(side="left", padx=8)

        # Bắt sự kiện hover đổi nền nhẹ và click chọn dòng
        def _on_enter(e, r_mv=ma_ve):
            if self.selected_ma_ve != r_mv and r_mv in self.row_widgets:
                self.row_widgets[r_mv].configure(fg_color=CyberpunkTheme.SURFACE_HOVER)

        def _on_leave(e, r_mv=ma_ve):
            if self.selected_ma_ve != r_mv and r_mv in self.row_widgets:
                self.row_widgets[r_mv].configure(fg_color=CyberpunkTheme.SURFACE_CARD)

        for widget in (row_card, lbl_ma_ve, lbl_loai, lbl_bien, lbl_chu, lbl_gio, lbl_gia):
            widget.bind("<Enter>", _on_enter)
            widget.bind("<Leave>", _on_leave)
            widget.bind("<Button-1>", lambda e, mv=ma_ve: self._chon_ve_thanh_toan(mv))
            widget.bind("<Double-Button-1>", lambda e, mv=ma_ve: self._chon_ve_thanh_toan(mv))

    def _chon_ve_thanh_toan(self, ma_ve: str) -> None:
        """Tự động điền mã vé vào ô thanh toán và đổi màu viền dòng được chọn."""
        self.selected_ma_ve = ma_ve

        # Cập nhật viền và nền tương phản cho tất cả các dòng hiện tại
        for mv, frame in self.row_widgets.items():
            if mv == ma_ve:
                frame.configure(
                    fg_color="#E8F4F5",
                    border_width=1,
                    border_color=CyberpunkTheme.CYAN_BORDER
                )
            else:
                frame.configure(
                    fg_color=CyberpunkTheme.SURFACE_CARD,
                    border_width=0,
                    border_color=CyberpunkTheme.BORDER_SUBTLE
                )

        self.txt_ma_ve_out.delete(0, "end")
        self.txt_ma_ve_out.insert(0, ma_ve)
        self.txt_ma_ve_out.focus()

    def _handle_tiep_nhan(self) -> None:
        """Xử lý sự kiện bấm nút Tiếp nhận xe."""
        loai_hien_thi = self.loai_xe_hien_thi_var.get()
        loai_xe = MAP_HIEN_THI_LOAI_XE.get(loai_hien_thi, "XeMay")
        ma_dinh_danh = self.txt_ma_dinh_danh.get().strip()
        chu_xe = self.txt_chu_xe.get().strip()

        # Với xe đạp, biển số có thể là None
        bien_so = ma_dinh_danh if loai_xe in ("XeMay", "OTo") else None

        ok, msg, ma_ve = BaiXeDbService.tiep_nhan_xe(
            loai_xe=loai_xe,
            ma_dinh_danh=ma_dinh_danh,
            bien_so=bien_so,
            chu_xe=chu_xe
        )

        if not ok:
            show_error(
                self.winfo_toplevel(),
                title="Không Thể Tiếp Nhận",
                message="Quá trình đăng ký tiếp nhận phương tiện không thành công.",
                card_title="CHI TIẾT LỖI TIẾP NHẬN",
                details=[
                    ("Phương tiện", loai_hien_thi),
                    ("Định danh", ma_dinh_danh if ma_dinh_danh else "Chưa nhập"),
                    ("Lý do từ chối", msg)
                ]
            )
            return

        # Lấy thông tin chi tiết vé vừa tạo để hiển thị giờ vào và đơn giá chính xác
        gio_vao_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        don_gia_str = "—"
        ok_ve, _, ve = BaiXeDbService.lay_chi_tiet_ve(ma_ve)
        if ok_ve and ve:
            if ve.get("gio_vao"):
                gio_vao_str = str(ve["gio_vao"])[:16]
            if ve.get("don_gia_ap_dung") is not None:
                don_gia_str = f"{ve['don_gia_ap_dung']:,} VNĐ"

        bien_so_label = "Mã thẻ xe đạp" if loai_xe == "XeDap" else "Biển số xe"
        details = [
            ("Mã vé", ma_ve),
            ("Phương tiện", loai_hien_thi),
            (bien_so_label, ma_dinh_danh),
            ("Chủ xe", chu_xe if chu_xe else "Khách vãng lai"),
            ("Thời gian vào", gio_vao_str),
            ("Phí gửi xe", don_gia_str)
        ]

        # Thành công: Hiển thị popup 2 lớp với khung thông tin chi tiết
        show_success(
            self.winfo_toplevel(),
            title="Tiếp Nhận Thành Công",
            message="Phương tiện đã được tiếp nhận vào bãi và cấp vé điện tử thành công.",
            card_title="THÔNG TIN TIẾP NHẬN",
            details=details
        )

        # Xóa trắng form nhập
        self.txt_ma_dinh_danh.delete(0, "end")
        self.txt_chu_xe.delete(0, "end")

        # Tải lại bảng dữ liệu và cập nhật số lượng
        self.tai_lai_danh_sach()

    def _handle_xe_ra(self) -> None:
        """Xử lý sự kiện bấm nút Cho xe ra và thanh toán."""
        ma_ve = self.txt_ma_ve_out.get().strip().upper()
        if not ma_ve:
            show_error(
                self.winfo_toplevel(),
                title="Lỗi Nhập Liệu",
                message="Vui lòng nhập hoặc chọn một vé từ danh sách để thanh toán.",
                card_title="CHI TIẾT LỖI"
            )
            return

        # Yêu cầu 10 & 9: Kiểm tra thông tin vé từ CSDL trước khi xác nhận thanh toán
        ok, msg, ve = BaiXeDbService.lay_chi_tiet_ve(ma_ve)
        if not ok or not ve:
            show_error(
                self.winfo_toplevel(),
                title="Không Tìm Thấy Vé",
                message="Hệ thống không tìm thấy mã vé yêu cầu trong cơ sở dữ liệu.",
                card_title="CHI TIẾT TRA CỨU",
                details=[
                    ("Mã vé tra cứu", ma_ve),
                    ("Nguyên nhân", "Vé không tồn tại hoặc đã nhập sai ký tự")
                ]
            )
            return

        # Yêu cầu 10: Không cho thanh toán vé đã được thanh toán hoặc đã hủy
        if ve.get("trang_thai") != "Dang gui":
            trang_thai_str = ve.get("trang_thai", "Không rõ")
            show_error(
                self.winfo_toplevel(),
                title="Không Thể Thanh Toán",
                message="Vé xe không ở trạng thái hợp lệ để thực hiện thanh toán.",
                card_title="CHI TIẾT TRẠNG THÁI VÉ",
                details=[
                    ("Mã vé", ma_ve),
                    ("Trạng thái hiện tại", trang_thai_str),
                    ("Lý do từ chối", "Vé đã được thanh toán hoặc đã bị hủy trước đó")
                ]
            )
            return

        pt_hien_thi = self.phuong_thuc_hien_thi_var.get()
        phuong_thuc = MAP_HIEN_THI_PHUONG_THUC.get(pt_hien_thi, "TIEN_MAT")
        ghi_chu = self.txt_ghi_chu.get().strip()

        # Yêu cầu 9: Hiển thị xác nhận gồm mã vé, loại xe, biển số hoặc mã thẻ, giờ vào và số tiền phải trả
        loai_hien_thi = ve.get("ten_loai_xe") or MAP_MA_SANG_HIEN_THI.get(ve.get("loai_xe"), ve.get("loai_xe", "—"))
        dinh_danh = ve.get("bien_so") or ve.get("ma_dinh_danh") or "—"
        dinh_danh_label = "Mã thẻ xe đạp" if ve.get("loai_xe") == "XeDap" else "Biển số xe"
        gio_vao_str = str(ve.get("gio_vao", ""))[:16] if ve.get("gio_vao") else "—"
        so_tien = ve.get("don_gia_ap_dung", 0)

        confirm_details = [
            ("Mã vé", ve['ma_ve']),
            ("Phương tiện", loai_hien_thi),
            (dinh_danh_label, dinh_danh),
            ("Chủ xe", ve.get("chu_xe") or "Khách vãng lai"),
            ("Thời gian vào", gio_vao_str),
            ("Số tiền phải trả", f"{so_tien:,} VNĐ"),
            ("Phương thức", pt_hien_thi)
        ]

        show_confirm(
            self.winfo_toplevel(),
            title="Xác Nhận Cho Xe Ra",
            message="Vui lòng kiểm tra kỹ thông tin phương tiện trước khi thanh toán:",
            card_title="THÔNG TIN XÁC NHẬN THANH TOÁN",
            details=confirm_details,
            on_confirm=lambda: self._thuc_hien_xe_ra(ma_ve, phuong_thuc, pt_hien_thi, ghi_chu)
        )

    def _thuc_hien_xe_ra(self, ma_ve: str, phuong_thuc: str, pt_hien_thi: str, ghi_chu: str) -> None:
        """Thực thi nghiệp vụ thanh toán qua BaiXeDbService."""
        ok, msg, chi_tiet = BaiXeDbService.cho_xe_ra_va_tinh_tien(
            ma_ve=ma_ve,
            phuong_thuc=phuong_thuc,
            ghi_chu=ghi_chu if ghi_chu else None
        )

        if not ok:
            show_error(
                self.winfo_toplevel(),
                title="Thất Bại",
                message="Giao dịch thanh toán xe ra không thể hoàn tất.",
                card_title="CHI TIẾT LỖI GIAO DỊCH",
                details=[
                    ("Mã vé", ma_ve),
                    ("Lý do thất bại", msg)
                ]
            )
            return

        # Thông báo thành công và biên lai với khung thông tin chi tiết 2 lớp
        so_tien_str = f"{chi_tiet.get('so_tien', 0):,} VNĐ" if chi_tiet else ""
        loai_hien_thi = MAP_MA_SANG_HIEN_THI.get(chi_tiet.get('loai_xe', ''), chi_tiet.get('loai_xe', ''))
        dinh_danh_lbl = "Mã thẻ xe đạp" if chi_tiet.get('loai_xe') == "XeDap" else "Biển số xe"
        gio_vao_str = str(chi_tiet.get("gio_vao", ""))[:16] if chi_tiet.get("gio_vao") else "—"
        gio_ra_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        details = [
            ("Mã vé", ma_ve),
            ("Phương tiện", loai_hien_thi),
            (dinh_danh_lbl, chi_tiet.get('ma_dinh_danh', '—')),
            ("Chủ xe", chi_tiet.get('chu_xe') or "Khách vãng lai"),
            ("Thời gian vào", gio_vao_str),
            ("Thời gian ra", gio_ra_str),
            ("Số tiền thu", so_tien_str),
            ("Phương thức", pt_hien_thi)
        ]

        show_success(
            self.winfo_toplevel(),
            title="Thanh Toán Thành Công",
            message="Đã hoàn tất thanh toán và mở cổng cho phương tiện xuất bãi an toàn.",
            card_title="CHI TIẾT GIAO DỊCH",
            details=details
        )

        # Xóa trắng form thanh toán và bỏ chọn dòng
        self.txt_ma_ve_out.delete(0, "end")
        self.txt_ghi_chu.delete(0, "end")
        self.selected_ma_ve = None

        # Yêu cầu 11: Sau khi thanh toán thành công, tự động cập nhật danh sách xe và số lượng đang gửi
        self.tai_lai_danh_sach()
