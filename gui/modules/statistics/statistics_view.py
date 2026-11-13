"""
NEON PARKING MANAGER - STATISTICS VIEW (THỐNG KÊ & BÁO CÁO)
Màn hình thống kê tổng hợp: Tỷ lệ lấp đầy, giờ cao điểm, phân bố loại xe.
Mọi nhân viên đã đăng nhập đều xem được (không giới hạn Admin).
Tầng GUI chỉ nhận dữ liệu từ BaiXeDbService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
from config.theme import CyberpunkTheme
from gui.components.stat_card import StatCard
from services.bai_xe_db_service import BaiXeDbService


class StatisticsView(ctk.CTkFrame):
    """
    Màn hình Thống kê tổng hợp:
    - 3 Thẻ KPI: Tổng vé, Đang gửi, Đã thanh toán.
    - Bảng tỷ lệ lấp đầy từng loại xe với thanh progress Neon.
    - Biểu đồ cột giờ cao điểm trong ngày (30 ngày gần nhất).
    - Bảng phân bố tổng lượt gửi xe theo loại phương tiện.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)
        self._xay_dung_giao_dien()
        self.after(100, self.tai_lai_du_lieu)

    # ─────────────────────────────── XÂY DỰNG GIAO DIỆN ───────────────────────────────

    def _xay_dung_giao_dien(self) -> None:
        """Khởi tạo toàn bộ layout giao diện Statistics."""
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.GREEN_NEON
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        # ── Tiêu đề + Nút làm mới ──
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="📊  THỐNG KÊ & BÁO CÁO BÃI GIỮ XE",
            font=CyberpunkTheme.FONT_TITLE_PAGE,
            text_color=CyberpunkTheme.GREEN_NEON,
            anchor="w"
        ).pack(side="left")

        self._lbl_cap_nhat = ctk.CTkLabel(
            header, text="",
            font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED
        )
        self._lbl_cap_nhat.pack(side="right", padx=(0, 12))

        ctk.CTkButton(
            header, text="🔄 LÀM MỚI",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.SURFACE_CARD, text_color=CyberpunkTheme.GREEN_NEON,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            border_width=1, border_color=CyberpunkTheme.GREEN_NEON,
            corner_radius=8, height=34, width=120,
            command=self.tai_lai_du_lieu
        ).pack(side="right")

        # ── 3 Thẻ KPI ──
        kpi_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 16))
        kpi_frame.columnconfigure((0, 1, 2), weight=1, uniform="stat_kpi")

        self._card_tong_ve = StatCard(
            kpi_frame, title="TỔNG VÉ XE", value="—",
            subtitle="Toàn bộ lịch sử", neon_color=CyberpunkTheme.GREEN_NEON, icon="🎫"
        )
        self._card_tong_ve.grid(row=0, column=0, sticky="nsew", padx=5)

        self._card_dang_gui = StatCard(
            kpi_frame, title="ĐANG GỬI", value="—",
            subtitle="Hiện tại trong bãi", neon_color=CyberpunkTheme.CYAN_NEON, icon="🚗"
        )
        self._card_dang_gui.grid(row=0, column=1, sticky="nsew", padx=5)

        self._card_da_thanh_toan = StatCard(
            kpi_frame, title="ĐÃ THANH TOÁN", value="—",
            subtitle="Tổng lượt đã hoàn thành", neon_color=CyberpunkTheme.PURPLE_NEON, icon="✅"
        )
        self._card_da_thanh_toan.grid(row=0, column=2, sticky="nsew", padx=5)

        # ── Hàng 2: Tỷ lệ lấp đầy (trái) + Phân bố loại xe (phải) ──
        row2 = ctk.CTkFrame(scroll, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 16))
        row2.columnconfigure(0, weight=1)
        row2.columnconfigure(1, weight=1)

        self._panel_lap_day = self._tao_panel(
            row2, "🅿  TỶ LỆ LẤP ĐẦY TỪNG KHU VỰC", CyberpunkTheme.GREEN_NEON, col=0
        )
        self._panel_phan_bo = self._tao_panel(
            row2, "🛵  PHÂN BỐ TỔNG LƯỢT GỬI THEO LOẠI XE", CyberpunkTheme.PURPLE_NEON, col=1
        )

        # ── Hàng 3: Biểu đồ giờ cao điểm ──
        self._panel_gio = self._tao_panel(
            scroll, "⏰  PHÂN TÍCH GIỜ CAO ĐIỂM (30 NGÀY GẦN NHẤT)", CyberpunkTheme.CYAN_NEON
        )
        self._panel_gio.pack_configure(pady=(0, 8))

    def _tao_panel(self, master, title: str, neon: str, col: int = None) -> ctk.CTkFrame:
        """Tạo card panel Cyberpunk với tiêu đề và vùng nội dung."""
        outer = ctk.CTkFrame(
            master,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=neon
        )
        if col is not None:
            outer.grid(row=0, column=col, sticky="nsew", padx=6)
        else:
            outer.pack(fill="x", pady=6)

        ctk.CTkLabel(
            outer, text=title,
            font=CyberpunkTheme.FONT_BODY_BOLD, text_color=neon, anchor="w"
        ).pack(fill="x", padx=16, pady=(12, 6))
        ctk.CTkFrame(outer, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=16, pady=(0, 8))

        content = ctk.CTkFrame(outer, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        outer._content = content
        return outer

    # ─────────────────────────────── TẢI DỮ LIỆU ───────────────────────────────

    def tai_lai_du_lieu(self) -> None:
        """Gọi Service, cập nhật toàn bộ widget thống kê."""
        import datetime
        thanh_cong, _, du_lieu = BaiXeDbService.lay_thong_ke_tong_hop()
        if not thanh_cong:
            return

        gio = datetime.datetime.now().strftime("%H:%M:%S")
        self._lbl_cap_nhat.configure(text=f"Cập nhật lúc: {gio}")

        # Cập nhật 3 KPI
        self._card_tong_ve.cap_nhat_gia_tri(
            str(du_lieu.get("tong_ve", 0)), "Toàn bộ lịch sử"
        )
        self._card_dang_gui.cap_nhat_gia_tri(
            str(du_lieu.get("dang_gui", 0)), "Đang trong bãi"
        )
        self._card_da_thanh_toan.cap_nhat_gia_tri(
            str(du_lieu.get("da_thanh_toan", 0)), "Đã hoàn thành"
        )

        # Cập nhật các panel
        self._cap_nhat_lap_day(du_lieu.get("lap_day", []))
        self._cap_nhat_phan_bo(du_lieu.get("luot_theo_loai", []))
        self._cap_nhat_gio_cao_diem(du_lieu.get("gio_cao_diem", []))

    # ─────────────────────────────── CẬP NHẬT PANEL ───────────────────────────────

    def _cap_nhat_lap_day(self, lap_day: list) -> None:
        """Vẽ lại bảng tỷ lệ lấp đầy từng loại xe với progress bar Neon."""
        content = self._panel_lap_day._content
        for w in content.winfo_children():
            w.destroy()

        if not lap_day:
            ctk.CTkLabel(
                content, text="Không có dữ liệu.",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(pady=16)
            return

        mau_loai = {
            "XeDap": CyberpunkTheme.GREEN_NEON,
            "XeMay": CyberpunkTheme.CYAN_NEON,
            "OTo": CyberpunkTheme.PINK_NEON
        }

        for item in lap_day:
            loai = item.get("loai_xe", "")
            ten = item.get("ten_hien_thi", loai)
            tong_cho = int(item.get("tong_cho", 0))
            dang_gui = int(item.get("dang_gui", 0))
            ty_le = dang_gui / max(tong_cho, 1)
            mau = mau_loai.get(loai, CyberpunkTheme.PURPLE_NEON)

            # Màu cảnh báo khi lấp đầy > 80%
            if ty_le >= 0.9:
                mau_bar = CyberpunkTheme.PINK_NEON
            elif ty_le >= 0.7:
                mau_bar = "#FF8C00"  # Cam cảnh báo
            else:
                mau_bar = mau

            row = ctk.CTkFrame(content, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            row.pack(fill="x", pady=5)

            # Hàng trên: Tên loại xe + tỷ lệ %
            top = ctk.CTkFrame(row, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(8, 4))

            ctk.CTkLabel(
                top, text=ten,
                font=CyberpunkTheme.FONT_BODY_BOLD, text_color=mau, anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                top, text=f"{dang_gui} / {tong_cho}  ({ty_le:.0%})",
                font=CyberpunkTheme.FONT_BODY_BOLD, text_color=mau_bar, anchor="e"
            ).pack(side="right")

            # Thanh progress
            bar_outer = ctk.CTkFrame(row, fg_color=CyberpunkTheme.SURFACE, corner_radius=6, height=14)
            bar_outer.pack(fill="x", padx=12, pady=(0, 10))
            bar_outer.pack_propagate(False)

            if dang_gui > 0:
                bar_fill = ctk.CTkFrame(bar_outer, fg_color=mau_bar, corner_radius=6, height=14)
                bar_fill.place(relx=0, rely=0, relwidth=min(ty_le, 1.0), relheight=1.0)

    def _cap_nhat_phan_bo(self, luot_theo_loai: list) -> None:
        """Vẽ lại bảng phân bố tổng lượt theo loại xe."""
        content = self._panel_phan_bo._content
        for w in content.winfo_children():
            w.destroy()

        if not luot_theo_loai:
            ctk.CTkLabel(
                content, text="Chưa có dữ liệu lượt gửi xe.",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(pady=16)
            return

        tong_tat_ca = sum(int(r.get("tong_luot", 0)) for r in luot_theo_loai)
        mau_loai = {
            "XeDap": CyberpunkTheme.GREEN_NEON,
            "XeMay": CyberpunkTheme.CYAN_NEON,
            "OTo": CyberpunkTheme.PINK_NEON
        }
        icons = {"XeDap": "🚲", "XeMay": "🛵", "OTo": "🚙"}

        for item in luot_theo_loai:
            loai = item.get("loai_xe", "")
            ten = item.get("ten_hien_thi", loai)
            tong_luot = int(item.get("tong_luot", 0))
            ty_le = tong_luot / max(tong_tat_ca, 1)
            mau = mau_loai.get(loai, CyberpunkTheme.PURPLE_NEON)
            icon = icons.get(loai, "🚗")

            row = ctk.CTkFrame(content, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            row.pack(fill="x", pady=5)

            top = ctk.CTkFrame(row, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(8, 4))

            ctk.CTkLabel(
                top, text=f"{icon}  {ten}",
                font=CyberpunkTheme.FONT_BODY_BOLD, text_color=mau, anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                top, text=f"{tong_luot:,} lượt  ({ty_le:.1%})",
                font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.TEXT_PRIMARY, anchor="e"
            ).pack(side="right")

            bar_outer = ctk.CTkFrame(row, fg_color=CyberpunkTheme.SURFACE, corner_radius=6, height=12)
            bar_outer.pack(fill="x", padx=12, pady=(0, 10))
            bar_outer.pack_propagate(False)

            if tong_luot > 0:
                bar_fill = ctk.CTkFrame(bar_outer, fg_color=mau, corner_radius=6, height=12)
                bar_fill.place(relx=0, rely=0, relwidth=min(ty_le, 1.0), relheight=1.0)

    def _cap_nhat_gio_cao_diem(self, gio_cao_diem: list) -> None:
        """Vẽ biểu đồ cột 24h giờ cao điểm dạng ASCII Neon."""
        content = self._panel_gio._content
        for w in content.winfo_children():
            w.destroy()

        if not gio_cao_diem:
            ctk.CTkLabel(
                content,
                text="Chưa có dữ liệu giờ cao điểm (cần ít nhất 1 lượt xe vào trong 30 ngày gần nhất).",
                font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(pady=16)
            return

        # Nhúng biểu đồ Matplotlib Cyberpunk
        from gui.components.cyber_chart import CyberChart
        if CyberChart.co_the_ve():
            CyberChart.ve_bieu_do_gio_cao_diem(content, gio_cao_diem)
            return

        # Lấp đầy tất cả 24 giờ
        gio_dict = {int(r["gio"]): int(r["so_luot"]) for r in gio_cao_diem}
        all_gio = [(gio, gio_dict.get(gio, 0)) for gio in range(24)]
        max_luot = max(sl for _, sl in all_gio) if all_gio else 1
        if max_luot == 0:
            max_luot = 1

        # Tìm giờ cao điểm nhất
        gio_dinh, sl_dinh = max(all_gio, key=lambda x: x[1])
        import datetime as _dt
        gio_hien_tai = _dt.datetime.now().hour

        # Nhãn thông tin
        info_row = ctk.CTkFrame(content, fg_color="transparent")
        info_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            info_row,
            text=f"⏰ Giờ cao điểm: {gio_dinh:02d}h – {sl_dinh} lượt xe",
            font=CyberpunkTheme.FONT_BODY_BOLD,
            text_color=CyberpunkTheme.CYAN_NEON
        ).pack(side="left")

        ctk.CTkLabel(
            info_row,
            text=f"(Thống kê 30 ngày gần nhất)",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.TEXT_MUTED
        ).pack(side="right")

        # Khung biểu đồ
        bieu_do = ctk.CTkFrame(content, fg_color="transparent")
        bieu_do.pack(fill="x", pady=4)

        cao_toi_da = 70

        for gio, so_luot in all_gio:
            col = ctk.CTkFrame(bieu_do, fg_color="transparent")
            col.pack(side="left", fill="both", expand=True)

            # Số lượt (bỏ qua nếu = 0)
            lbl_so = ctk.CTkLabel(
                col,
                text=str(so_luot) if so_luot > 0 else "",
                font=("Segoe UI", 7),
                text_color=CyberpunkTheme.CYAN_NEON
            )
            lbl_so.pack()

            # Vùng cột
            bar_area = ctk.CTkFrame(col, fg_color="transparent", height=cao_toi_da)
            bar_area.pack(fill="x")
            bar_area.pack_propagate(False)

            ty_le = so_luot / max_luot
            cao_cot = max(int(ty_le * cao_toi_da), 2 if so_luot > 0 else 0)

            if cao_cot > 0:
                spacer = ctk.CTkFrame(bar_area, fg_color="transparent", height=cao_toi_da - cao_cot)
                spacer.pack(fill="x")

                # Màu: Cyan bình thường, Vàng neon cho cao điểm, Xanh cho giờ hiện tại
                if gio == gio_dinh:
                    mau_cot = CyberpunkTheme.PINK_NEON
                elif gio == gio_hien_tai:
                    mau_cot = CyberpunkTheme.GREEN_NEON
                else:
                    mau_cot = CyberpunkTheme.CYAN_NEON

                bar = ctk.CTkFrame(bar_area, fg_color=mau_cot, corner_radius=2, height=cao_cot)
                bar.pack(fill="x")

            # Nhãn giờ phía dưới
            lbl_gio = ctk.CTkLabel(
                col,
                text=f"{gio}h",
                font=("Segoe UI", 7),
                text_color=CyberpunkTheme.PINK_NEON if gio == gio_dinh else CyberpunkTheme.TEXT_MUTED
            )
            lbl_gio.pack(pady=(2, 0))

        # Chú thích màu
        legend = ctk.CTkFrame(content, fg_color="transparent")
        legend.pack(fill="x", pady=(8, 0))

        for mau, nhan in [
            (CyberpunkTheme.PINK_NEON, "Giờ cao điểm"),
            (CyberpunkTheme.GREEN_NEON, "Giờ hiện tại"),
            (CyberpunkTheme.CYAN_NEON, "Bình thường"),
        ]:
            dot = ctk.CTkFrame(legend, fg_color=mau, corner_radius=3, width=10, height=10)
            dot.pack(side="left", padx=(8, 4))
            ctk.CTkLabel(
                legend, text=nhan,
                font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(side="left", padx=(0, 16))
