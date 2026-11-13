"""
NEON PARKING MANAGER - DASHBOARD VIEW
Màn hình tổng quan hệ thống: Hiển thị KPI số liệu theo thời gian thực từ MySQL.
Tầng GUI chỉ nhận dữ liệu từ BaiXeDbService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
import datetime
from typing import Optional
from config.theme import CyberpunkTheme
from gui.components.stat_card import StatCard
from services.bai_xe_db_service import BaiXeDbService
from services.auth_service import AuthService


class DashboardView(ctk.CTkFrame):
    """
    Màn hình Dashboard tổng quan:
    - Hàng KPI: Xe đang gửi, Chỗ trống, Lượt vào hôm nay, Doanh thu (Admin only).
    - Bảng phân bố xe theo loại và tỷ lệ lấp đầy.
    - Biểu đồ dạng thanh (ASCII Neon) thể hiện lượt xe 7 ngày gần nhất.
    - Bảng hoạt động gần nhất.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)
        self._du_lieu_kpi: dict = {}
        self._xay_dung_giao_dien()
        # Tải dữ liệu ngay khi khởi tạo
        self.after(100, self.tai_lai_du_lieu)

    # ─────────────────────────────── XÂY DỰNG GIAO DIỆN ───────────────────────────────

    def _xay_dung_giao_dien(self) -> None:
        """Khởi tạo toàn bộ layout giao diện Dashboard."""
        # Vùng cuộn chính
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        self._scroll.pack(fill="both", expand=True, padx=24, pady=20)

        # ── Hàng 1: Tiêu đề + Nút Làm mới ──
        header_row = ctk.CTkFrame(self._scroll, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 16))

        lbl_title = ctk.CTkLabel(
            header_row,
            text="TỔNG QUAN BÃI XE",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            anchor="w"
        )
        lbl_title.pack(side="left")

        self._lbl_cap_nhat = ctk.CTkLabel(
            header_row,
            text="",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        )
        self._lbl_cap_nhat.pack(side="right", padx=(0, 12))

        btn_refresh = ctk.CTkButton(
            header_row,
            text="🔄 LÀM MỚI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_TEAL,
            text_color=CyberpunkTheme.TEXT_WHITE,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            corner_radius=8,
            height=34,
            width=120,
            command=self.tai_lai_du_lieu
        )
        btn_refresh.pack(side="right")

        # ── Hàng 2: 4 Thẻ KPI ──
        kpi_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 16))
        kpi_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="kpi")

        self._card_xe_gui = StatCard(
            kpi_frame, title="XE ĐANG GỬI", value="—",
            subtitle="Toàn bãi xe", neon_color=CyberpunkTheme.CYAN_NEON, icon="🚗"
        )
        self._card_xe_gui.grid(row=0, column=0, sticky="nsew", padx=5)

        self._card_cho_trong = StatCard(
            kpi_frame, title="CHỖ TRỐNG", value="—",
            subtitle="Còn nhận thêm", neon_color=CyberpunkTheme.GREEN_NEON, icon="🅿"
        )
        self._card_cho_trong.grid(row=0, column=1, sticky="nsew", padx=5)

        self._card_luot_vao = StatCard(
            kpi_frame, title="LƯỢT VÀO HÔM NAY", value="—",
            subtitle="Kể từ 00:00", neon_color=CyberpunkTheme.PURPLE_NEON, icon="📥"
        )
        self._card_luot_vao.grid(row=0, column=2, sticky="nsew", padx=5)

        self._card_doanh_thu = StatCard(
            kpi_frame, title="DOANH THU HÔM NAY", value="—",
            subtitle="Chỉ Admin xem được", neon_color=CyberpunkTheme.PINK_NEON, icon="💰"
        )
        self._card_doanh_thu.grid(row=0, column=3, sticky="nsew", padx=5)

        # ── Hàng 3: Phân bố loại xe (trái) + Biểu đồ 7 ngày (phải) ──
        row3 = ctk.CTkFrame(self._scroll, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 16))
        row3.columnconfigure(0, weight=1)
        row3.columnconfigure(1, weight=2)

        # Panel trái: Phân bố loại xe
        self._panel_phan_bo = self._tao_panel_card(
            row3, title="🚦  PHÂN BỐ THEO LOẠI XE", neon=CyberpunkTheme.GREEN_NEON, col=0
        )

        # Panel phải: Biểu đồ 7 ngày
        self._panel_bieu_do = self._tao_panel_card(
            row3, title="📈  LƯỢT XE VÀO – 7 NGÀY GẦN NHẤT", neon=CyberpunkTheme.CYAN_NEON, col=1
        )

        # ── Hàng 4: Thông tin lượt ra hôm nay ──
        self._panel_tong_hop = self._tao_panel_card(
            self._scroll, title="📊  TỔNG HỢP CA LÀM VIỆC HÔM NAY", neon=CyberpunkTheme.PURPLE_NEON
        )
        self._panel_tong_hop.pack_configure(padx=0)

    def _tao_panel_card(
        self, master, title: str, neon: str, col: Optional[int] = None
    ) -> ctk.CTkFrame:
        """Tạo một card panel với viền Neon và tiêu đề chuẩn giao diện Cyberpunk."""
        outer = ctk.CTkFrame(
            master,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=neon
        )
        if col is not None:
            outer.grid(row=0, column=col, sticky="nsew", padx=6, pady=0)
        else:
            outer.pack(fill="x", pady=6)

        lbl = ctk.CTkLabel(
            outer,
            text=title,
            font=CyberpunkTheme.FONT_BODY_BOLD,
            text_color=neon,
            anchor="w"
        )
        lbl.pack(fill="x", padx=16, pady=(12, 8))

        divider = ctk.CTkFrame(outer, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE)
        divider.pack(fill="x", padx=16, pady=(0, 8))

        # Vùng nội dung bên trong card (trả về để điền dữ liệu sau)
        content = ctk.CTkFrame(outer, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Gắn thuộc tính content vào outer để truy cập sau
        outer._content = content
        return outer

    # ─────────────────────────────── TẢI DỮ LIỆU ───────────────────────────────

    def tai_lai_du_lieu(self) -> None:
        """Gọi Service, cập nhật tất cả widget với dữ liệu mới từ MySQL."""
        thanh_cong, thong_bao, du_lieu = BaiXeDbService.lay_kpi_dashboard()
        if not thanh_cong:
            self._hien_loi(thong_bao)
            return

        self._du_lieu_kpi = du_lieu
        gio_cap_nhat = datetime.datetime.now().strftime("%H:%M:%S")
        self._lbl_cap_nhat.configure(text=f"Cập nhật lúc: {gio_cap_nhat}")

        # Cập nhật 4 thẻ KPI
        self._card_xe_gui.cap_nhat_gia_tri(
            str(du_lieu.get("tong_dang_gui", 0)),
            f"Sức chứa tối đa: {du_lieu.get('tong_suc_chua', 0)}"
        )
        self._card_cho_trong.cap_nhat_gia_tri(
            str(du_lieu.get("cho_trong", 0)),
            f"Đang gửi: {du_lieu.get('tong_dang_gui', 0)} / {du_lieu.get('tong_suc_chua', 0)}"
        )
        self._card_luot_vao.cap_nhat_gia_tri(
            str(du_lieu.get("luot_vao_hom_nay", 0)),
            f"Đã ra: {du_lieu.get('luot_ra_hom_nay', 0)} lượt"
        )

        # Doanh thu chỉ hiển thị với Admin
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if nguoi_dung and nguoi_dung.vai_tro == "ADMIN":
            tong_dt = du_lieu.get("doanh_thu_hom_nay", 0)
            self._card_doanh_thu.cap_nhat_gia_tri(
                f"{tong_dt:,.0f}đ",
                "Tổng thanh toán hôm nay"
            )
        else:
            self._card_doanh_thu.cap_nhat_gia_tri("🔒 Ẩn", "Chỉ Admin xem được")

        # Cập nhật panel phân bố loại xe
        self._cap_nhat_phan_bo(du_lieu.get("xe_theo_loai", []), du_lieu)

        # Cập nhật biểu đồ 7 ngày
        self._cap_nhat_bieu_do(du_lieu.get("data_7_ngay", []))

        # Cập nhật tổng hợp ca làm việc
        self._cap_nhat_tong_hop(du_lieu)

    def _hien_loi(self, thong_bao: str) -> None:
        """Hiển thị thông báo lỗi trong vùng KPI khi không tải được dữ liệu."""
        for card in (
            self._card_xe_gui, self._card_cho_trong,
            self._card_luot_vao, self._card_doanh_thu
        ):
            card.cap_nhat_gia_tri("Lỗi", thong_bao[:40])

    # ─────────────────────────────── CẬP NHẬT PANEL ───────────────────────────────

    def _cap_nhat_phan_bo(self, xe_theo_loai: list, du_lieu: dict) -> None:
        """Vẽ lại bảng phân bố xe theo loại trong panel trái."""
        content = self._panel_phan_bo._content
        for w in content.winfo_children():
            w.destroy()

        tong_dang_gui = du_lieu.get("tong_dang_gui", 0)
        tong_suc_chua = du_lieu.get("tong_suc_chua", 0)

        if not xe_theo_loai and tong_dang_gui == 0:
            lbl = ctk.CTkLabel(
                content, text="Bãi xe đang trống",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            )
            lbl.pack(pady=16)
            return

        # Màu Neon theo từng loại xe
        mau_loai = {
            "XeDap": CyberpunkTheme.GREEN_NEON,
            "XeMay": CyberpunkTheme.CYAN_NEON,
            "OTo": CyberpunkTheme.PINK_NEON
        }

        for item in xe_theo_loai:
            loai = item.get("loai_xe", "")
            ten = item.get("ten_hien_thi", loai)
            so_luong = item.get("dang_gui", 0)
            mau = mau_loai.get(loai, CyberpunkTheme.PURPLE_NEON)

            row = ctk.CTkFrame(content, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            row.pack(fill="x", pady=4)

            # Tên loại xe
            lbl_ten = ctk.CTkLabel(
                row, text=f"  {ten}",
                font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.TEXT_PRIMARY,
                anchor="w", width=110
            )
            lbl_ten.pack(side="left", padx=(8, 4), pady=8)

            # Thanh progress (vẽ thủ công bằng frame neon)
            bar_outer = ctk.CTkFrame(row, fg_color=CyberpunkTheme.SURFACE, corner_radius=4, height=16)
            bar_outer.pack(side="left", fill="x", expand=True, padx=6, pady=10)
            bar_outer.pack_propagate(False)

            # Tính tỷ lệ phần trăm so với sức chứa tương ứng
            # (Lấy từ xe_theo_loai, tong_cho sẽ truy vấn qua tổng; dùng xấp xỉ 1/3 tổng cho đơn giản)
            ty_le = min(so_luong / max(tong_suc_chua // 3 if tong_suc_chua else 1, 1), 1.0)
            if so_luong > 0:
                bar_fill = ctk.CTkFrame(bar_outer, fg_color=mau, corner_radius=4, height=16)
                bar_fill.place(relx=0, rely=0, relwidth=max(ty_le, 0.04), relheight=1.0)

            # Số lượng
            lbl_sl = ctk.CTkLabel(
                row, text=str(so_luong),
                font=CyberpunkTheme.FONT_BODY_BOLD, text_color=mau, width=36, anchor="e"
            )
            lbl_sl.pack(side="right", padx=(4, 10), pady=8)

    def _cap_nhat_bieu_do(self, data_7_ngay: list) -> None:
        """Vẽ biểu đồ cột ASCII Neon thể hiện lượt xe 7 ngày gần nhất."""
        content = self._panel_bieu_do._content
        for w in content.winfo_children():
            w.destroy()

        if not data_7_ngay:
            lbl = ctk.CTkLabel(
                content, text="Chưa có dữ liệu lượt xe trong 7 ngày gần nhất.",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            )
            lbl.pack(pady=16)
            return

        # Điền 7 ngày kể cả ngày không có dữ liệu
        ngay_co_du_lieu = {str(row["ngay"]): int(row["so_luot"]) for row in data_7_ngay}
        cac_ngay = []
        hom_nay = datetime.date.today()
        for i in range(6, -1, -1):
            ngay = hom_nay - datetime.timedelta(days=i)
            cac_ngay.append((ngay, ngay_co_du_lieu.get(str(ngay), 0)))

        # Nhúng biểu đồ Matplotlib Cyberpunk chuẩn
        from gui.components.cyber_chart import CyberChart
        if CyberChart.co_the_ve():
            CyberChart.ve_bieu_do_cot_7_ngay(content, cac_ngay)
            return

        max_luot = max(sl for _, sl in cac_ngay) if cac_ngay else 1
        if max_luot == 0:
            max_luot = 1  # Tránh chia cho 0

        # Khung biểu đồ fallback
        bieu_do_frame = ctk.CTkFrame(content, fg_color="transparent")
        bieu_do_frame.pack(fill="both", expand=True, pady=4)

        # Chiều cao tối đa của cột (pixel)
        cao_toi_da = 80

        for ngay, so_luot in cac_ngay:
            col_frame = ctk.CTkFrame(bieu_do_frame, fg_color="transparent")
            col_frame.pack(side="left", fill="both", expand=True, padx=3)

            # Số lượt (phía trên cột)
            lbl_so = ctk.CTkLabel(
                col_frame,
                text=str(so_luot) if so_luot > 0 else "",
                font=CyberpunkTheme.FONT_SMALL,
                text_color=CyberpunkTheme.CYAN_NEON
            )
            lbl_so.pack()

            # Vùng cột
            bar_container = ctk.CTkFrame(col_frame, fg_color="transparent", height=cao_toi_da)
            bar_container.pack(fill="x")
            bar_container.pack_propagate(False)

            ty_le = so_luot / max_luot
            cao_cot = max(int(ty_le * cao_toi_da), 2 if so_luot > 0 else 0)

            if cao_cot > 0:
                # Khoảng trống phía trên
                spacer = ctk.CTkFrame(bar_container, fg_color="transparent", height=cao_toi_da - cao_cot)
                spacer.pack(fill="x")

                # Cột màu Neon
                mau_cot = CyberpunkTheme.CYAN_NEON if ngay != hom_nay else CyberpunkTheme.GREEN_NEON
                bar = ctk.CTkFrame(bar_container, fg_color=mau_cot, corner_radius=3, height=cao_cot)
                bar.pack(fill="x")

            # Nhãn ngày phía dưới
            ten_ngay = "Hôm nay" if ngay == hom_nay else f"{ngay.day}/{ngay.month}"
            lbl_ngay = ctk.CTkLabel(
                col_frame,
                text=ten_ngay,
                font=("Segoe UI", 8),
                text_color=CyberpunkTheme.TEXT_MUTED if ngay != hom_nay else CyberpunkTheme.GREEN_NEON
            )
            lbl_ngay.pack(pady=(4, 0))

    def _cap_nhat_tong_hop(self, du_lieu: dict) -> None:
        """Cập nhật panel tổng hợp ca làm việc hôm nay."""
        content = self._panel_tong_hop._content
        for w in content.winfo_children():
            w.destroy()

        luot_vao = du_lieu.get("luot_vao_hom_nay", 0)
        luot_ra = du_lieu.get("luot_ra_hom_nay", 0)
        tong_dang_gui = du_lieu.get("tong_dang_gui", 0)
        doanh_thu = du_lieu.get("doanh_thu_hom_nay", 0)
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        la_admin = nguoi_dung and nguoi_dung.vai_tro == "ADMIN"

        thong_tin = [
            ("📥 Lượt xe vào hôm nay", str(luot_vao), CyberpunkTheme.CYAN_NEON),
            ("🚗 Xe đang gửi hiện tại", str(tong_dang_gui), CyberpunkTheme.GREEN_NEON),
            ("📤 Lượt xe ra hôm nay", str(luot_ra), CyberpunkTheme.PURPLE_NEON),
        ]
        if la_admin:
            thong_tin.append(
                ("💰 Doanh thu hôm nay", f"{doanh_thu:,.0f}đ", CyberpunkTheme.PINK_NEON)
            )

        row_frame = ctk.CTkFrame(content, fg_color="transparent")
        row_frame.pack(fill="x")

        for i, (ten, gia_tri, mau) in enumerate(thong_tin):
            item = ctk.CTkFrame(row_frame, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            item.pack(side="left", fill="both", expand=True, padx=5, pady=4)

            lbl_ten = ctk.CTkLabel(
                item, text=ten,
                font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w"
            )
            lbl_ten.pack(fill="x", padx=12, pady=(8, 2))

            lbl_gia_tri = ctk.CTkLabel(
                item, text=gia_tri,
                font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=mau, anchor="w"
            )
            lbl_gia_tri.pack(fill="x", padx=12, pady=(2, 8))
