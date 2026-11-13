"""
NEON PARKING MANAGER - REPORTS VIEW (XUẤT BÁO CÁO TXT)
Màn hình xuất báo cáo chuẩn văn bản tiếng Việt UTF-8:
1. Danh sách xe đang gửi trong bãi
2. Lịch sử vé xe (toàn bộ hoặc theo trạng thái)
3. Tổng hợp doanh thu & giao dịch (Chỉ ADMIN)
Tầng GUI gọi ReportService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime, date
from typing import Optional
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from services.report_service import ReportService
from gui.components.dialog import show_info, show_error
from gui.components.segmented_control import SegmentedControl


class ReportsView(ctk.CTkFrame):
    """
    Giao diện Xuất Báo cáo dạng TXT hỗ trợ lưu file qua hộp thoại Windows.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        self._build_ui()

    def _build_ui(self) -> None:
        """Xây dựng 3 Card báo cáo nghiệp vụ."""
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=CyberpunkTheme.SURFACE_HOVER,
            scrollbar_button_hover_color=CyberpunkTheme.CYAN_NEON
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=16)

        # ─── BÁO CÁO 1: XE ĐANG GỬI ───
        self._build_card_xe_dang_gui(scroll)

        # ─── BÁO CÁO 2: LỊCH SỬ VÉ ───
        self._build_card_lich_su_ve(scroll)

        # ─── BÁO CÁO 3: DOANH THU TỔNG HỢP ───
        self._build_card_doanh_thu(scroll)

        # ─── BÁO CÁO 4: LỊCH SỬ GIAO DỊCH THANH TOÁN ───
        self._build_card_lich_su_thanh_toan(scroll)

    def _build_card_xe_dang_gui(self, parent) -> None:
        """Card báo cáo danh sách phương tiện hiện diện trong bãi."""
        card = ctk.CTkFrame(parent, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.BORDER_SUBTLE)
        card.pack(fill="x", pady=(0, 16))

        # Tiêu đề Card
        title_box = ctk.CTkFrame(card, fg_color="transparent")
        title_box.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(title_box, text="🚗 BÁO CÁO PHƯƠNG TIỆN HIỆN DIỆN TRONG BÃI", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.CYAN_NEON).pack(side="left")
        ctk.CTkLabel(title_box, text="Mọi nhân viên", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.GREEN_NEON, fg_color="#0F2D20", corner_radius=4, padx=8, pady=2).pack(side="right")

        ctk.CTkLabel(
            card,
            text="Xuất toàn bộ danh sách các phương tiện hiện đang đỗ trong bãi giữ xe, phân loại xe đạp, xe máy, ô tô, biển số/mã thẻ, giờ tiếp nhận và đơn giá tạm tính.",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="left",
            wraplength=900
        ).pack(fill="x", padx=20, pady=(0, 14))

        # Thanh nút bấm
        action_bar = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
        action_bar.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(action_bar, text="Định dạng xuất: Văn bản chuẩn UTF-8 (.txt) hỗ trợ tiếng Việt", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=16, pady=12)

        btn_export = ctk.CTkButton(
            action_bar,
            text="📄 XUẤT BÁO CÁO (.TXT)",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.CYAN_DEEP,
            hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
            border_color=CyberpunkTheme.CYAN_BORDER,
            border_width=1,
            text_color=CyberpunkTheme.TEXT_WHITE,
            height=36,
            command=self._xuat_xe_dang_gui
        )
        btn_export.pack(side="right", padx=16, pady=8)

    def _build_card_lich_su_ve(self, parent) -> None:
        """Card báo cáo lịch sử các vé xe."""
        card = ctk.CTkFrame(parent, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.BORDER_SUBTLE)
        card.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(card, fg_color="transparent")
        title_box.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(title_box, text="🎫 BÁO CÁO LỊCH SỬ VÉ XE", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.GREEN_NEON).pack(side="left")
        ctk.CTkLabel(title_box, text="Mọi nhân viên", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.GREEN_NEON, fg_color="#0F2D20", corner_radius=4, padx=8, pady=2).pack(side="right")

        ctk.CTkLabel(
            card,
            text="Xuất danh sách vé xe đã phát hành trong hệ thống, bao gồm giờ vào, giờ ra, thông tin phương tiện và trạng thái vé (Đang gửi, Đã thanh toán, Đã hủy).",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="left",
            wraplength=900
        ).pack(fill="x", padx=20, pady=(0, 14))

        # Tùy chọn lọc trạng thái vé
        action_bar = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
        action_bar.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(action_bar, text="Trạng thái vé:", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_PRIMARY).pack(side="left", padx=(16, 8), pady=12)

        self.cbo_trang_thai_ve = SegmentedControl(
            action_bar,
            values=["Tất cả", "Đang gửi", "Đã thanh toán", "Đã hủy"],
            default_value="Tất cả",
            height=34,
            corner_radius=8
        )
        self.cbo_trang_thai_ve.pack(side="left", padx=(0, 16))

        btn_export = ctk.CTkButton(
            action_bar,
            text="📄 XUẤT LỊCH SỬ VÉ (.TXT)",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_CYAN,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            text_color=CyberpunkTheme.TEXT_WHITE,
            height=36,
            command=self._xuat_lich_su_ve
        )
        btn_export.pack(side="right", padx=16, pady=8)

    def _build_card_doanh_thu(self, parent) -> None:
        """Card báo cáo tổng hợp doanh thu hoạt động."""
        is_admin = AuthService.la_admin()

        card = ctk.CTkFrame(parent, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.PINK_NEON if is_admin else CyberpunkTheme.BORDER_SUBTLE)
        card.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(card, fg_color="transparent")
        title_box.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(title_box, text="💰 BÁO CÁO TỔNG HỢP DOANH THU", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.PINK_NEON).pack(side="left")
        ctk.CTkLabel(title_box, text="ADMIN ONLY", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.PINK_NEON, fg_color="#2D1225", corner_radius=4, padx=8, pady=2).pack(side="right")

        ctk.CTkLabel(
            card,
            text="Tổng hợp tổng doanh thu hoạt động của bãi xe theo khoảng ngày, phân tích chi tiết dòng tiền theo ngày và theo tháng, tỷ trọng tiền mặt / chuyển khoản (chỉ tính các vé đã thanh toán thực thu).",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="left",
            wraplength=900
        ).pack(fill="x", padx=20, pady=(0, 14))

        if not is_admin:
            # Ẩn form lọc nếu không phải Admin
            lock_box = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            lock_box.pack(fill="x", padx=20, pady=(0, 16))
            ctk.CTkLabel(lock_box, text="🔒 Báo cáo doanh thu là thông tin tài chính mật, chỉ dành riêng cho tài khoản Quản trị viên (ADMIN).", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.PINK_NEON).pack(padx=16, pady=12)
            return

        # Tùy chọn lọc khoảng ngày cho Admin
        action_bar = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
        action_bar.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(action_bar, text="Từ ngày:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(16, 4), pady=12)
        self.entry_dt_tu = ctk.CTkEntry(action_bar, placeholder_text="YYYY-MM-DD", width=110, height=34, fg_color=CyberpunkTheme.SURFACE_INPUT)
        self.entry_dt_tu.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(action_bar, text="Đến ngày:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.entry_dt_den = ctk.CTkEntry(action_bar, placeholder_text="YYYY-MM-DD", width=110, height=34, fg_color=CyberpunkTheme.SURFACE_INPUT)
        self.entry_dt_den.pack(side="left", padx=(0, 14))

        # Nút nạp hôm nay nhanh
        btn_today = ctk.CTkButton(
            action_bar,
            text="Hôm nay",
            font=CyberpunkTheme.FONT_SMALL,
            width=70,
            height=30,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            command=self._chon_hom_nay
        )
        btn_today.pack(side="left", padx=(0, 14))

        btn_export = ctk.CTkButton(
            action_bar,
            text="📄 XUẤT BÁO CÁO DOANH THU (.TXT)",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.ACCENT_GOLD,
            hover_color=CyberpunkTheme.GOLD_HOVER,
            text_color=CyberpunkTheme.TEXT_WHITE,
            height=36,
            command=self._xuat_doanh_thu
        )
        btn_export.pack(side="right", padx=16, pady=8)

    def _build_card_lich_su_thanh_toan(self, parent) -> None:
        """Card báo cáo lịch sử giao dịch thanh toán chi tiết."""
        is_admin = AuthService.la_admin()

        card = ctk.CTkFrame(parent, fg_color=CyberpunkTheme.SURFACE, corner_radius=12, border_width=1, border_color=CyberpunkTheme.PRIMARY_CYAN if is_admin else CyberpunkTheme.BORDER_SUBTLE)
        card.pack(fill="x", pady=(0, 16))

        title_box = ctk.CTkFrame(card, fg_color="transparent")
        title_box.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(title_box, text="📋 BÁO CÁO LỊCH SỬ GIAO DỊCH THANH TOÁN", font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=CyberpunkTheme.CYAN_NEON).pack(side="left")
        ctk.CTkLabel(title_box, text="ADMIN ONLY", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.CYAN_NEON, fg_color="#0F2D30", corner_radius=4, padx=8, pady=2).pack(side="right")

        ctk.CTkLabel(
            card,
            text="Bảng kê chi tiết từng hóa đơn giao dịch thanh toán trong hệ thống: mã vé, thông tin xe, số tiền thu, phương thức thanh toán, thời gian thu tiền và nhân viên thu ngân phụ trách.",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="left",
            wraplength=900
        ).pack(fill="x", padx=20, pady=(0, 14))

        if not is_admin:
            lock_box = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            lock_box.pack(fill="x", padx=20, pady=(0, 16))
            ctk.CTkLabel(lock_box, text="🔒 Lịch sử giao dịch thanh toán là thông tin tài chính mật, chỉ dành riêng cho tài khoản Quản trị viên (ADMIN).", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.PINK_NEON).pack(padx=16, pady=12)
            return

        action_bar = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
        action_bar.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(action_bar, text="Từ ngày:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(16, 4), pady=12)
        self.entry_gd_tu = ctk.CTkEntry(action_bar, placeholder_text="YYYY-MM-DD", width=110, height=34, fg_color=CyberpunkTheme.SURFACE_INPUT)
        self.entry_gd_tu.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(action_bar, text="Đến ngày:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.entry_gd_den = ctk.CTkEntry(action_bar, placeholder_text="YYYY-MM-DD", width=110, height=34, fg_color=CyberpunkTheme.SURFACE_INPUT)
        self.entry_gd_den.pack(side="left", padx=(0, 10))

        btn_today_gd = ctk.CTkButton(
            action_bar,
            text="Hôm nay",
            font=CyberpunkTheme.FONT_SMALL,
            width=70,
            height=30,
            fg_color=CyberpunkTheme.SURFACE_CARD,
            hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=CyberpunkTheme.BORDER_SUBTLE,
            command=self._chon_hom_nay_gd
        )
        btn_today_gd.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(action_bar, text="Hình thức:", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.cbo_phuong_thuc_gd = SegmentedControl(
            action_bar,
            values=["Tất cả", "Tiền mặt", "Chuyển khoản"],
            default_value="Tất cả",
            height=32,
            corner_radius=8
        )
        self.cbo_phuong_thuc_gd.pack(side="left", padx=(0, 16))

        btn_export = ctk.CTkButton(
            action_bar,
            text="📄 XUẤT LỊCH SỬ GIAO DỊCH (.TXT)",
            font=CyberpunkTheme.FONT_BUTTON,
            fg_color=CyberpunkTheme.PRIMARY_CYAN,
            hover_color=CyberpunkTheme.PRIMARY_HOVER,
            text_color=CyberpunkTheme.TEXT_WHITE,
            height=36,
            command=self._xuat_lich_su_giao_dich
        )
        btn_export.pack(side="right", padx=16, pady=8)

    def _chon_hom_nay(self) -> None:
        """Điền ngày hôm nay vào bộ lọc ngày báo cáo doanh thu."""
        hom_nay = date.today().strftime("%Y-%m-%d")
        self.entry_dt_tu.delete(0, "end")
        self.entry_dt_tu.insert(0, hom_nay)
        self.entry_dt_den.delete(0, "end")
        self.entry_dt_den.insert(0, hom_nay)

    def _chon_hom_nay_gd(self) -> None:
        """Điền ngày hôm nay vào bộ lọc ngày lịch sử giao dịch."""
        hom_nay = date.today().strftime("%Y-%m-%d")
        self.entry_gd_tu.delete(0, "end")
        self.entry_gd_tu.insert(0, hom_nay)
        self.entry_gd_den.delete(0, "end")
        self.entry_gd_den.insert(0, hom_nay)

    # ─────────────────────────── THỰC THI XUẤT FILE ───────────────────────────

    def _xuat_xe_dang_gui(self) -> None:
        """Mở hộp thoại chọn vị trí lưu và xuất báo cáo xe đang gửi."""
        mac_dinh = f"BaoCao_XeDangGui_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=mac_dinh,
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            title="Chọn nơi lưu Báo Cáo Xe Đang Gửi"
        )
        if not path:
            return

        ok, msg = ReportService.xuat_bao_cao_xe_dang_gui(path)
        if ok:
            show_info(self, "Xuất thành công", f"{msg}\nĐường dẫn: {path}")
        else:
            show_error(self, "Lỗi xuất báo cáo", msg)

    def _xuat_lich_su_ve(self) -> None:
        """Mở hộp thoại chọn vị trí lưu và xuất báo cáo lịch sử vé."""
        tt = self.cbo_trang_thai_ve.get()
        mapping = {
            "Tất cả": None,
            "Đang gửi": "Dang gui",
            "Đã thanh toán": "Da thanh toan",
            "Đã hủy": "Da huy"
        }
        tt_param = mapping.get(tt, None if tt in ("Tất cả", "ALL") else tt)

        mac_dinh = f"BaoCao_LichSuVe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=mac_dinh,
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            title="Chọn nơi lưu Báo Cáo Lịch Sử Vé"
        )
        if not path:
            return

        ok, msg = ReportService.xuat_bao_cao_lich_su_ve(path, trang_thai=tt_param)
        if ok:
            show_info(self, "Xuất thành công", f"{msg}\nĐường dẫn: {path}")
        else:
            show_error(self, "Lỗi xuất báo cáo", msg)

    def _xuat_doanh_thu(self) -> None:
        """Mở hộp thoại chọn vị trí lưu và xuất báo cáo doanh thu tổng hợp."""
        tu_ngay = self.entry_dt_tu.get().strip()
        den_ngay = self.entry_dt_den.get().strip()

        # Kiểm tra tính hợp lệ của định dạng ngày nếu người dùng có nhập
        if tu_ngay:
            try:
                date.fromisoformat(tu_ngay)
            except ValueError:
                show_error(self, "Lỗi ngày", f"Định dạng 'Từ ngày' không hợp lệ: {tu_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return
        if den_ngay:
            try:
                date.fromisoformat(den_ngay)
            except ValueError:
                show_error(self, "Lỗi ngày", f"Định dạng 'Đến ngày' không hợp lệ: {den_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return

        mac_dinh = f"BaoCao_DoanhThu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=mac_dinh,
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            title="Chọn nơi lưu Báo Cáo Doanh Thu Tổng Hợp"
        )
        if not path:
            return

        ok, msg = ReportService.xuat_bao_cao_doanh_thu(
            path,
            tu_ngay=tu_ngay if tu_ngay else None,
            den_ngay=den_ngay if den_ngay else None
        )
        if ok:
            show_info(self, "Xuất thành công", f"{msg}\nĐường dẫn: {path}")
        else:
            show_error(self, "Lỗi xuất báo cáo", msg)

    def _xuat_lich_su_giao_dich(self) -> None:
        """Mở hộp thoại chọn vị trí lưu và xuất báo cáo lịch sử giao dịch thanh toán."""
        tu_ngay = self.entry_gd_tu.get().strip()
        den_ngay = self.entry_gd_den.get().strip()
        pt_chon = self.cbo_phuong_thuc_gd.get()
        pt_mapping = {
            "Tất cả": None,
            "Tiền mặt": "TIEN_MAT",
            "Chuyển khoản": "CHUYEN_KHOAN"
        }
        pt_db = pt_mapping.get(pt_chon, None)

        if tu_ngay:
            try:
                date.fromisoformat(tu_ngay)
            except ValueError:
                show_error(self, "Lỗi ngày", f"Định dạng 'Từ ngày' không hợp lệ: {tu_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return
        if den_ngay:
            try:
                date.fromisoformat(den_ngay)
            except ValueError:
                show_error(self, "Lỗi ngày", f"Định dạng 'Đến ngày' không hợp lệ: {den_ngay}\nVui lòng nhập đúng định dạng YYYY-MM-DD.")
                return

        mac_dinh = f"BaoCao_LichSuGiaoDich_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
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
            tu_ngay=tu_ngay if tu_ngay else None,
            den_ngay=den_ngay if den_ngay else None,
            phuong_thuc=pt_db
        )
        if ok:
            show_info(self, "Xuất thành công", f"{msg}\nĐường dẫn: {path}")
        else:
            show_error(self, "Lỗi xuất báo cáo", msg)
