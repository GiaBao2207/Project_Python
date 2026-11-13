"""
NEON PARKING MANAGER - REVENUE VIEW (QUẢN LÝ DOANH THU)
Màn hình thống kê doanh thu chi tiết – Chỉ dành cho ADMIN.
Tầng GUI chỉ nhận dữ liệu từ BaiXeDbService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
import datetime
from tkinter import filedialog
from config.theme import CyberpunkTheme
from gui.components.stat_card import StatCard
from gui.components.dialog import show_error, show_info
from gui.components.segmented_control import SegmentedControl
from services.bai_xe_db_service import BaiXeDbService
from services.auth_service import AuthService
from services.report_service import ReportService


class RevenueView(ctk.CTkFrame):
    """
    Màn hình Quản lý Doanh thu (Admin Only):
    - 3 thẻ KPI: Tổng doanh thu trong khoảng ngày, Tiền mặt, Chuyển khoản.
    - Bộ lọc: Từ ngày – Đến ngày, Phương thức thanh toán.
    - Bảng lịch sử giao dịch chi tiết kết hợp thông tin xe.
    - Tổng hợp doanh thu theo ngày (30 ngày gần nhất).
    """

    # Cột bảng lịch sử
    _COLS = [
        ("Thời gian", 150),
        ("Mã vé", 130),
        ("Phương tiện", 90),
        ("Biển số / Mã ĐD", 130),
        ("Phương thức", 110),
        ("Số tiền (đ)", 100),
        ("Nhân viên thu", 140),
        ("Ghi chú", 160),
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        # Kiểm tra quyền Admin ngay khi khởi tạo
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung or nguoi_dung.vai_tro != "ADMIN":
            self._hien_khong_co_quyen()
            return

        # Bộ lọc mặc định: 30 ngày gần nhất
        hom_nay = datetime.date.today()
        self._ngay_bat_dau = str(hom_nay - datetime.timedelta(days=29))
        self._ngay_ket_thuc = str(hom_nay)
        self._phuong_thuc = "TAT_CA"

        self._xay_dung_giao_dien()
        self.after(100, self.tai_lai_du_lieu)

    # ─────────────────────────────── QUYỀN TRUY CẬP ───────────────────────────────

    def _hien_khong_co_quyen(self) -> None:
        """Hiển thị thông báo không đủ quyền truy cập."""
        frame = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=16,
            border_width=2,
            border_color=CyberpunkTheme.PINK_NEON
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            frame, text="🔒", font=("Segoe UI", 48)
        ).pack(pady=(28, 8))

        ctk.CTkLabel(
            frame,
            text="TRUY CẬP BỊ TỪ CHỐI",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.PINK_NEON
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            frame,
            text="Chỉ Quản trị viên (ADMIN) mới được xem dữ liệu doanh thu.\nVui lòng liên hệ Admin để được cấp quyền.",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="center"
        ).pack(padx=32, pady=(0, 28))

    # ─────────────────────────────── XÂY DỰNG GIAO DIỆN ───────────────────────────────

    def _xay_dung_giao_dien(self) -> None:
        """Khởi tạo toàn bộ layout giao diện Revenue."""
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.PINK_NEON
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        # ── Tiêu đề ──
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="💰  QUẢN LÝ DOANH THU",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.PINK_NEON,
            anchor="w"
        ).pack(side="left")

        # Badge Admin
        ctk.CTkLabel(
            header,
            text="👑 ADMIN ONLY",
            font=("Segoe UI", 9, "bold"),
            text_color=CyberpunkTheme.PINK_NEON,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            corner_radius=6, padx=8, pady=3
        ).pack(side="right")

        # ── Bộ lọc ──
        self._xay_dung_bo_loc(scroll)

        # ── 3 Thẻ KPI ──
        kpi_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 16))
        kpi_frame.columnconfigure((0, 1, 2), weight=1, uniform="rev_kpi")

        self._card_tong = StatCard(
            kpi_frame, title="TỔNG DOANH THU", value="—",
            subtitle="Trong khoảng ngày chọn", neon_color=CyberpunkTheme.PINK_NEON, icon="💎"
        )
        self._card_tong.grid(row=0, column=0, sticky="nsew", padx=5)

        self._card_tien_mat = StatCard(
            kpi_frame, title="TIỀN MẶT", value="—",
            subtitle="Cash payment", neon_color=CyberpunkTheme.GREEN_NEON, icon="💵"
        )
        self._card_tien_mat.grid(row=0, column=1, sticky="nsew", padx=5)

        self._card_chuyen_khoan = StatCard(
            kpi_frame, title="CHUYỂN KHOẢN", value="—",
            subtitle="Bank transfer", neon_color=CyberpunkTheme.CYAN_NEON, icon="💳"
        )
        self._card_chuyen_khoan.grid(row=0, column=2, sticky="nsew", padx=5)

        # ── Bảng tổng hợp theo ngày ──
        self._xay_dung_bang_theo_ngay(scroll)

        # ── Bảng lịch sử giao dịch chi tiết ──
        self._xay_dung_bang_giao_dich(scroll)

    def _xay_dung_bo_loc(self, parent) -> None:
        """Khối bộ lọc: Từ ngày, Đến ngày, Phương thức, Nút Tìm."""
        card = ctk.CTkFrame(
            parent, fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12, border_width=1, border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        card.pack(fill="x", pady=(0, 16))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=12)

        # Từ ngày
        ctk.CTkLabel(
            inner, text="Từ ngày:", font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        ).pack(side="left")

        self._entry_tu_ngay = ctk.CTkEntry(
            inner, width=110, font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT, text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_color=CyberpunkTheme.BORDER_SUBTLE, corner_radius=6, placeholder_text="YYYY-MM-DD"
        )
        self._entry_tu_ngay.insert(0, self._ngay_bat_dau)
        self._entry_tu_ngay.pack(side="left", padx=(6, 16))

        # Đến ngày
        ctk.CTkLabel(
            inner, text="Đến ngày:", font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        ).pack(side="left")

        self._entry_den_ngay = ctk.CTkEntry(
            inner, width=110, font=CyberpunkTheme.FONT_BODY,
            fg_color=CyberpunkTheme.SURFACE_INPUT, text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_color=CyberpunkTheme.BORDER_SUBTLE, corner_radius=6, placeholder_text="YYYY-MM-DD"
        )
        self._entry_den_ngay.insert(0, self._ngay_ket_thuc)
        self._entry_den_ngay.pack(side="left", padx=(6, 16))

        # Phương thức
        ctk.CTkLabel(
            inner, text="Phương thức:", font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        ).pack(side="left")

        self._cbb_phuong_thuc = SegmentedControl(
            inner,
            values=["Tất cả", "Tiền mặt", "Chuyển khoản"],
            default_value="Tất cả",
            height=32,
            corner_radius=8
        )
        self._cbb_phuong_thuc.pack(side="left", padx=(6, 16))

        # Nút Tìm
        btn_tim = ctk.CTkButton(
            inner, text="🔍 LỌC KẾT QUẢ",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PINK_DEEP,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PINK_DEEP_HOVER,
            border_color=CyberpunkTheme.PINK_NEON,
            border_width=1,
            corner_radius=8, height=34,
            command=self.tai_lai_du_lieu
        )
        btn_tim.pack(side="left", padx=(0, 8))

        # Nút Hôm nay
        btn_hom_nay = ctk.CTkButton(
            inner, text="📅 Hôm nay",
            font=CyberpunkTheme.FONT_SMALL,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            text_color=CyberpunkTheme.TEXT_MUTED,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            corner_radius=8, height=34,
            command=self._loc_hom_nay
        )
        btn_hom_nay.pack(side="left")

        # Nút Xuất file trực tiếp từ màn hình Doanh thu
        btn_xuat_gd = ctk.CTkButton(
            inner,
            text="📄 LỊCH SỬ GD (.TXT)",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_CYAN,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            text_color=CyberpunkTheme.TEXT_WHITE,
            corner_radius=8, height=34,
            command=self._xuat_lich_su_giao_dich
        )
        btn_xuat_gd.pack(side="right", padx=(8, 0))

        btn_xuat_dt = ctk.CTkButton(
            inner,
            text="📄 BÁO CÁO DT (.TXT)",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.ACCENT_GOLD,
            hover_color=CyberpunkTheme.GOLD_HOVER,
            text_color=CyberpunkTheme.TEXT_WHITE,
            corner_radius=8, height=34,
            command=self._xuat_bao_cao_doanh_thu
        )
        btn_xuat_dt.pack(side="right", padx=(8, 0))

        # Nhãn thông báo trạng thái
        self._lbl_trang_thai = ctk.CTkLabel(
            card, text="", font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        )
        self._lbl_trang_thai.pack(padx=16, pady=(0, 8))

    def _xay_dung_bang_theo_ngay(self, parent) -> None:
        """Card bảng tổng hợp doanh thu từng ngày."""
        card = ctk.CTkFrame(
            parent, fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12, border_width=1, border_color=CyberpunkTheme.PINK_NEON
        )
        card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            card, text="📅  DOANH THU THEO NGÀY (30 NGÀY GẦN NHẤT)",
            font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.PINK_NEON, anchor="w"
        ).pack(fill="x", padx=16, pady=(12, 4))
        ctk.CTkFrame(card, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=16, pady=(0, 8))

        # Vùng biểu đồ doanh thu trực quan Matplotlib
        self._chart_container = ctk.CTkFrame(card, fg_color="transparent", height=200)
        self._chart_container.pack(fill="x", padx=16, pady=(0, 10))

        # Header cột
        header = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=0)
        header.pack(fill="x", padx=16, pady=(0, 4))
        for ten_col, do_rong in [("Ngày", 120), ("Tiền mặt (đ)", 150), ("Chuyển khoản (đ)", 160), ("Tổng (đ)", 130)]:
            ctk.CTkLabel(
                header, text=ten_col, font=CyberpunkTheme.FONT_SMALL,
                text_color=CyberpunkTheme.TEXT_MUTED, width=do_rong, anchor="w"
            ).pack(side="left", padx=8, pady=6)

        # Vùng cuộn cho bảng ngày
        self._scroll_ngay = ctk.CTkScrollableFrame(
            card, fg_color="transparent", height=160,
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.PINK_NEON
        )
        self._scroll_ngay.pack(fill="x", padx=16, pady=(0, 12))

    def _xay_dung_bang_giao_dich(self, parent) -> None:
        """Card bảng lịch sử giao dịch chi tiết."""
        card = ctk.CTkFrame(
            parent, fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12, border_width=1, border_color=CyberpunkTheme.BORDER_SUBTLE
        )
        card.pack(fill="both", expand=True, pady=(0, 8))

        self._lbl_so_giao_dich = ctk.CTkLabel(
            card, text="📋  LỊCH SỬ GIAO DỊCH CHI TIẾT",
            font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.TEXT_PRIMARY, anchor="w"
        )
        self._lbl_so_giao_dich.pack(fill="x", padx=16, pady=(12, 4))
        ctk.CTkFrame(card, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=16, pady=(0, 8))

        # Header bảng giao dịch
        header = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=0)
        header.pack(fill="x", padx=16, pady=(0, 4))
        for ten_col, do_rong in self._COLS:
            ctk.CTkLabel(
                header, text=ten_col, font=CyberpunkTheme.FONT_SMALL,
                text_color=CyberpunkTheme.CYAN_NEON, width=do_rong, anchor="w"
            ).pack(side="left", padx=6, pady=6)

        # Vùng cuộn cho bảng giao dịch
        self._scroll_gd = ctk.CTkScrollableFrame(
            card, fg_color="transparent", height=280,
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        self._scroll_gd.pack(fill="both", expand=True, padx=16, pady=(0, 12))

    # ─────────────────────────────── TẢI DỮ LIỆU ───────────────────────────────

    def tai_lai_du_lieu(self) -> None:
        """Đọc bộ lọc, gọi Service và cập nhật giao diện."""
        tu_ngay = self._entry_tu_ngay.get().strip() or None
        den_ngay = self._entry_den_ngay.get().strip() or None
        phuong_thuc_hien_thi = self._cbb_phuong_thuc.get()
        # Chuyển đổi hiển thị → mã DB
        phuong_thuc_db = {
            "Tất cả": "TAT_CA",
            "Tiền mặt": "TIEN_MAT",
            "Chuyển khoản": "CHUYEN_KHOAN"
        }.get(phuong_thuc_hien_thi, "TAT_CA")

        # Validate ngày
        if tu_ngay:
            try:
                datetime.date.fromisoformat(tu_ngay)
            except ValueError:
                show_error(self.winfo_toplevel(), "Lỗi ngày", f"Định dạng 'Từ ngày' không hợp lệ: {tu_ngay}\nHãy dùng định dạng YYYY-MM-DD.")
                return
        if den_ngay:
            try:
                datetime.date.fromisoformat(den_ngay)
            except ValueError:
                show_error(self.winfo_toplevel(), "Lỗi ngày", f"Định dạng 'Đến ngày' không hợp lệ: {den_ngay}\nHãy dùng định dạng YYYY-MM-DD.")
                return

        # Tải KPI tổng hợp theo khoảng ngày đã lọc
        ok1, _, tong_hop = BaiXeDbService.lay_tong_doanh_thu(tu_ngay, den_ngay)
        if ok1:
            self._cap_nhat_kpi(tong_hop)

        # Tải lịch sử giao dịch chi tiết
        ok2, msg2, giao_dich = BaiXeDbService.lay_lich_su_thanh_toan(
            tu_ngay, den_ngay,
            phuong_thuc_db if phuong_thuc_db != "TAT_CA" else None
        )
        self._lbl_trang_thai.configure(text=msg2)
        if ok2:
            self._cap_nhat_bang_giao_dich(giao_dich)

        # Tải bảng theo ngày (luôn 30 ngày gần nhất)
        ok3, _, theo_ngay = BaiXeDbService.lay_doanh_thu_theo_ngay(30)
        if ok3:
            self._cap_nhat_bang_theo_ngay(theo_ngay)

    def _loc_hom_nay(self) -> None:
        """Đặt lại bộ lọc về ngày hôm nay rồi tải lại."""
        hom_nay = str(datetime.date.today())
        self._entry_tu_ngay.delete(0, "end")
        self._entry_tu_ngay.insert(0, hom_nay)
        self._entry_den_ngay.delete(0, "end")
        self._entry_den_ngay.insert(0, hom_nay)
        self.tai_lai_du_lieu()

    # ─────────────────────────────── CẬP NHẬT WIDGET ───────────────────────────────

    def _cap_nhat_kpi(self, tong_hop: dict) -> None:
        """Cập nhật 3 thẻ KPI với số liệu tổng hợp."""
        tong_val = tong_hop.get('tong_doanh_thu', tong_hop.get('tong', 0))
        so_gd = tong_hop.get('so_giao_dich', tong_hop.get('so_luot_thu', 0))
        self._card_tong.cap_nhat_gia_tri(
            f"{tong_val:,.0f}đ",
            f"{so_gd} giao dịch"
        )
        self._card_tien_mat.cap_nhat_gia_tri(
            f"{tong_hop.get('tien_mat', 0):,.0f}đ",
            "TIEN_MAT"
        )
        self._card_chuyen_khoan.cap_nhat_gia_tri(
            f"{tong_hop.get('chuyen_khoan', 0):,.0f}đ",
            "CHUYEN_KHOAN"
        )

    def _cap_nhat_bang_theo_ngay(self, danh_sach: list) -> None:
        """Vẽ lại bảng tổng hợp doanh thu từng ngày và biểu đồ trực quan."""
        # Cập nhật biểu đồ Matplotlib
        from gui.components.cyber_chart import CyberChart
        if CyberChart.co_the_ve() and hasattr(self, "_chart_container"):
            CyberChart.ve_bieu_do_doanh_thu_ngay(self._chart_container, danh_sach)

        for w in self._scroll_ngay.winfo_children():
            w.destroy()

        if not danh_sach:
            ctk.CTkLabel(
                self._scroll_ngay,
                text="Không có dữ liệu doanh thu trong khoảng thời gian này.",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(pady=12)
            return

        for i, row in enumerate(danh_sach):
            mau_nen = CyberpunkTheme.SURFACE_CARD if i % 2 == 0 else "transparent"
            row_frame = ctk.CTkFrame(self._scroll_ngay, fg_color=mau_nen, corner_radius=4)
            row_frame.pack(fill="x", pady=1)

            ngay_str = str(row.get("ngay", ""))
            tien_mat = int(row.get("tien_mat", 0))
            chuyen_khoan = int(row.get("chuyen_khoan", 0))
            tong = int(row.get("tong", 0))

            for gia_tri, do_rong, mau in [
                (ngay_str, 120, CyberpunkTheme.TEXT_PRIMARY),
                (f"{tien_mat:,}", 150, CyberpunkTheme.GREEN_NEON),
                (f"{chuyen_khoan:,}", 160, CyberpunkTheme.CYAN_NEON),
                (f"{tong:,}", 130, CyberpunkTheme.PINK_NEON),
            ]:
                ctk.CTkLabel(
                    row_frame, text=gia_tri,
                    font=CyberpunkTheme.FONT_SMALL, text_color=mau,
                    width=do_rong, anchor="w"
                ).pack(side="left", padx=8, pady=5)

    def _cap_nhat_bang_giao_dich(self, danh_sach: list) -> None:
        """Vẽ lại bảng lịch sử giao dịch chi tiết."""
        for w in self._scroll_gd.winfo_children():
            w.destroy()

        self._lbl_so_giao_dich.configure(
            text=f"📋  LỊCH SỬ GIAO DỊCH CHI TIẾT  ({len(danh_sach)} bản ghi)"
        )

        if not danh_sach:
            ctk.CTkLabel(
                self._scroll_gd,
                text="Không có giao dịch nào trong khoảng thời gian đã chọn.",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(pady=20)
            return

        for i, gd in enumerate(danh_sach):
            mau_nen = CyberpunkTheme.SURFACE_CARD if i % 2 == 0 else "transparent"
            row_frame = ctk.CTkFrame(self._scroll_gd, fg_color=mau_nen, corner_radius=4)
            row_frame.pack(fill="x", pady=1)

            # Chuẩn bị dữ liệu hiển thị
            thoi_gian = gd.get("thoi_gian_thanh_toan")
            thoi_gian_str = thoi_gian.strftime("%d/%m/%Y %H:%M") if thoi_gian else "—"
            ma_ve = str(gd.get("ma_ve", "—"))
            ten_loai_xe = str(gd.get("ten_loai_xe", "—"))
            ma_dd = str(gd.get("ma_dinh_danh", "—"))
            phuong_thuc = gd.get("phuong_thuc", "—")
            phuong_thuc_hien = "Tiền mặt" if phuong_thuc == "TIEN_MAT" else "Chuyển khoản"
            so_tien = int(gd.get("so_tien", 0))
            nhan_vien = str(gd.get("ten_nhan_vien") or "—")
            ghi_chu = str(gd.get("ghi_chu") or "")

            # Màu phương thức
            mau_pt = CyberpunkTheme.GREEN_NEON if phuong_thuc == "TIEN_MAT" else CyberpunkTheme.CYAN_NEON

            du_lieu_cols = [
                (thoi_gian_str, 150, CyberpunkTheme.TEXT_MUTED),
                (ma_ve, 130, CyberpunkTheme.TEXT_PRIMARY),
                (ten_loai_xe, 90, CyberpunkTheme.PURPLE_NEON),
                (ma_dd, 130, CyberpunkTheme.TEXT_PRIMARY),
                (phuong_thuc_hien, 110, mau_pt),
                (f"{so_tien:,}", 100, CyberpunkTheme.PINK_NEON),
                (nhan_vien, 140, CyberpunkTheme.TEXT_MUTED),
                (ghi_chu[:20] if ghi_chu else "—", 160, CyberpunkTheme.TEXT_MUTED),
            ]
            for gia_tri, do_rong, mau in du_lieu_cols:
                ctk.CTkLabel(
                    row_frame, text=gia_tri,
                    font=CyberpunkTheme.FONT_SMALL, text_color=mau,
                    width=do_rong, anchor="w"
                ).pack(side="left", padx=6, pady=5)

    # ─────────────────────────── XUẤT BÁO CÁO TỪ REVENUE ───────────────────────────

    def _xuat_bao_cao_doanh_thu(self) -> None:
        """Xuất file báo cáo tổng hợp doanh thu theo bộ lọc ngày hiện tại."""
        tu_ngay = self._entry_tu_ngay.get().strip() or None
        den_ngay = self._entry_den_ngay.get().strip() or None

        if tu_ngay:
            try:
                datetime.date.fromisoformat(tu_ngay)
            except ValueError:
                show_error(self.winfo_toplevel(), "Lỗi ngày", f"Định dạng 'Từ ngày' không hợp lệ: {tu_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return
        if den_ngay:
            try:
                datetime.date.fromisoformat(den_ngay)
            except ValueError:
                show_error(self.winfo_toplevel(), "Lỗi ngày", f"Định dạng 'Đến ngày' không hợp lệ: {den_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return

        mac_dinh = f"BaoCao_DoanhThu_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=mac_dinh,
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            title="Chọn nơi lưu Báo Cáo Doanh Thu Tổng Hợp"
        )
        if not path:
            return

        ok, msg = ReportService.xuat_bao_cao_doanh_thu(path, tu_ngay=tu_ngay, den_ngay=den_ngay)
        if ok:
            show_info(self.winfo_toplevel(), "Xuất thành công", f"{msg}\nĐường dẫn: {path}")
        else:
            show_error(self.winfo_toplevel(), "Lỗi xuất báo cáo", msg)

    def _xuat_lich_su_giao_dich(self) -> None:
        """Xuất file báo cáo chi tiết lịch sử giao dịch thanh toán theo bộ lọc hiện tại."""
        tu_ngay = self._entry_tu_ngay.get().strip() or None
        den_ngay = self._entry_den_ngay.get().strip() or None
        phuong_thuc_hien_thi = self._cbb_phuong_thuc.get()
        phuong_thuc_db = {
            "Tất cả": None,
            "Tiền mặt": "TIEN_MAT",
            "Chuyển khoản": "CHUYEN_KHOAN"
        }.get(phuong_thuc_hien_thi, None)

        if tu_ngay:
            try:
                datetime.date.fromisoformat(tu_ngay)
            except ValueError:
                show_error(self.winfo_toplevel(), "Lỗi ngày", f"Định dạng 'Từ ngày' không hợp lệ: {tu_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return
        if den_ngay:
            try:
                datetime.date.fromisoformat(den_ngay)
            except ValueError:
                show_error(self.winfo_toplevel(), "Lỗi ngày", f"Định dạng 'Đến ngày' không hợp lệ: {den_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return

        mac_dinh = f"BaoCao_LichSuGiaoDich_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=mac_dinh,
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            title="Chọn nơi lưu Báo Cáo Lịch Sử Giao Dịch"
        )
        if not path:
            return

        ok, msg = ReportService.xuat_bao_cao_lich_su_giao_dich(
            path,
            tu_ngay=tu_ngay,
            den_ngay=den_ngay,
            phuong_thuc=phuong_thuc_db
        )
        if ok:
            show_info(self.winfo_toplevel(), "Xuất thành công", f"{msg}\nĐường dẫn: {path}")
        else:
            show_error(self.winfo_toplevel(), "Lỗi xuất báo cáo", msg)
