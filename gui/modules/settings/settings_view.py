"""
NEON PARKING MANAGER - SETTINGS VIEW (CÀI ĐẶT BẢNG GIÁ & SỨC CHỨA)
Màn hình quản trị cấu hình hệ thống: Bảng giá vé và Sức chứa bãi xe.
Chỉ dành riêng cho ADMIN - Tầng GUI gọi SettingsService, không viết SQL trực tiếp.
"""

import customtkinter as ctk
from typing import Dict, Any, List
from config.theme import CyberpunkTheme
from services.auth_service import AuthService
from services.settings_service import SettingsService
from gui.components.dialog import show_confirm, show_info, show_error


class SettingsView(ctk.CTkFrame):
    """
    Giao diện Quản lý Cài đặt: 2 Tabs riêng biệt cho Bảng Giá và Sức Chứa.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CyberpunkTheme.BG_DARK, **kwargs)

        if not AuthService.la_admin():
            self._build_access_denied()
            return

        self._build_ui()
        self.tai_du_lieu_bang_gia()
        self.tai_du_lieu_suc_chua()

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
            text="Phân hệ Cài Đặt Hệ Thống chỉ dành riêng cho Quản trị viên (ADMIN).\nTài khoản của bạn không có đủ thẩm quyền truy cập màn hình này.",
            font=CyberpunkTheme.FONT_BODY,
            text_color=CyberpunkTheme.TEXT_MUTED,
            justify="center"
        ).pack(padx=24, pady=(0, 20))

    def _build_ui(self) -> None:
        """Xây dựng giao diện với 2 Tabs: Bảng Giá và Sức Chứa."""
        # Tabview CustomTkinter hiện đại
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=CyberpunkTheme.BG_DARK,
            segmented_button_fg_color=CyberpunkTheme.SURFACE,
            segmented_button_selected_color=CyberpunkTheme.CYAN_NEON,
            segmented_button_selected_hover_color=CyberpunkTheme.CYAN_HOVER,
            segmented_button_unselected_color=CyberpunkTheme.SURFACE_CARD,
            segmented_button_unselected_hover_color=CyberpunkTheme.SURFACE_HOVER,
            text_color=CyberpunkTheme.TEXT_DARK
        )
        self.tabview.pack(fill="both", expand=True, padx=16, pady=10)

        # Tạo 2 Tabs
        self.tab_gia = self.tabview.add("💰 BẢNG GIÁ DỊCH VỤ")
        self.tab_succhua = self.tabview.add("🅿️ SỨC CHỨA BÃI XE")

        # Thiết lập màu chữ cho tabview headers
        self.tabview._segmented_button.configure(font=CyberpunkTheme.FONT_BUTTON)

        # Xây dựng nội dung từng Tab
        self._build_tab_bang_gia()
        self._build_tab_suc_chua()

    # ─────────────────────────── TAB 1: BẢNG GIÁ ───────────────────────────

    def _build_tab_bang_gia(self) -> None:
        """Xây dựng giao diện tab Bảng Giá."""
        # Khung giải thích nguyên tắc kế toán snapshot
        note_card = ctk.CTkFrame(self.tab_gia, fg_color=CyberpunkTheme.SURFACE, corner_radius=8, border_width=1, border_color=CyberpunkTheme.BORDER_SUBTLE)
        note_card.pack(fill="x", padx=10, pady=(6, 12))

        lbl_note = ctk.CTkLabel(
            note_card,
            text="ℹ️ LƯU Ý BẢO TOÀN DỮ LIỆU KẾ TOÁN: Khi thay đổi đơn giá, mức giá mới chỉ áp dụng cho các xe vào bãi sau thời điểm đổi. Toàn bộ vé xe đã tạo trước đó vẫn giữ nguyên đơn giá snapshot tại thời điểm check-in để đảm bảo tính nhất quán doanh thu.",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.CYAN_NEON,
            justify="left",
            wraplength=850
        )
        lbl_note.pack(padx=16, pady=10, anchor="w")

        # Khung chứa các Card giá của 3 loại xe
        self.cards_gia_frame = ctk.CTkFrame(self.tab_gia, fg_color="transparent")
        self.cards_gia_frame.pack(fill="both", expand=True, padx=6, pady=4)

    def tai_du_lieu_bang_gia(self) -> None:
        """Nạp danh sách giá vé từ SettingsService và render giao diện."""
        for w in self.cards_gia_frame.winfo_children():
            w.destroy()

        try:
            danh_sach = SettingsService.lay_bang_gia()
        except Exception as e:
            show_error(self, "Lỗi nạp bảng giá", f"Không thể lấy bảng giá: {e}")
            return

        icon_map = {
            "XeDap": ("🚲", CyberpunkTheme.GREEN_NEON),
            "XeMay": ("🛵", CyberpunkTheme.CYAN_NEON),
            "OTo": ("🚗", CyberpunkTheme.PINK_NEON)
        }

        # Grid 3 cột cho 3 loại xe
        self.cards_gia_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="col_gia")

        for idx, item in enumerate(danh_sach):
            lx = item["loai_xe"]
            ten = item["ten_hien_thi"]
            gia = int(item["gia_ve"])
            ngay_up = str(item.get("ngay_cap_nhat", ""))[:16]

            icon, color = icon_map.get(lx, ("🚘", CyberpunkTheme.CYAN_NEON))

            card = ctk.CTkFrame(
                self.cards_gia_frame,
                fg_color=CyberpunkTheme.SURFACE,
                corner_radius=12,
                border_width=1,
                border_color=CyberpunkTheme.BORDER_SUBTLE
            )
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")

            # Icon & Tên loại xe
            header_box = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            header_box.pack(fill="x", padx=16, pady=(16, 12))

            ctk.CTkLabel(header_box, text=icon, font=("Segoe UI", 32)).pack(pady=(10, 2))
            ctk.CTkLabel(header_box, text=ten.upper(), font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=color).pack(pady=(0, 10))

            # Giá hiện tại
            ctk.CTkLabel(card, text="ĐƠN GIÁ ÁP DỤNG HIỆN TẠI", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(pady=(6, 2))
            lbl_cur_price = ctk.CTkLabel(
                card,
                text=f"{gia:,.0f} VNĐ",
                font=("Segoe UI", 24, "bold"),
                text_color=CyberpunkTheme.TEXT_PRIMARY
            )
            lbl_cur_price.pack(pady=(0, 12))

            # Ô nhập giá mới
            ctk.CTkLabel(card, text="Thiết lập đơn giá mới (VNĐ):", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(4, 2))
            entry_new_price = ctk.CTkEntry(
                card,
                placeholder_text=str(gia),
                font=CyberpunkTheme.FONT_BODY,
                fg_color=CyberpunkTheme.SURFACE_INPUT,
                height=38
            )
            entry_new_price.insert(0, str(gia))
            entry_new_price.pack(fill="x", padx=24, pady=(0, 14))

            # Nút Lưu
            def _luu_gia(loai=lx, entry=entry_new_price, ten_xe=ten):
                val = entry.get().strip().replace(",", "").replace(".", "")
                if not val.isdigit():
                    show_error(self, "Lỗi nhập liệu", "Vui lòng nhập đơn giá là số nguyên hợp lệ!")
                    return
                gia_moi = int(val)
                if not show_confirm(self, "Xác nhận cập nhật giá", f"Bạn có chắc muốn đổi đơn giá {ten_xe} thành {gia_moi:,.0f} VNĐ?"):
                    return
                ok, msg = SettingsService.cap_nhat_bang_gia(loai, gia_moi)
                if ok:
                    show_info(self, "Thành công", msg)
                    self.tai_du_lieu_bang_gia()
                else:
                    show_error(self, "Thao tác thất bại", msg)

            btn_save = ctk.CTkButton(
                card,
                text="💾 CẬP NHẬT GIÁ",
                font=CyberpunkTheme.FONT_BUTTON,
                fg_color=CyberpunkTheme.CYAN_DEEP,
                hover_color=CyberpunkTheme.CYAN_DEEP_HOVER,
                border_color=CyberpunkTheme.CYAN_BORDER,
                border_width=1,
                text_color=CyberpunkTheme.TEXT_WHITE,
                height=38,
                command=_luu_gia
            )
            btn_save.pack(fill="x", padx=24, pady=(0, 10))

            if ngay_up:
                ctk.CTkLabel(card, text=f"Cập nhật: {ngay_up}", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(pady=(0, 12))

    # ─────────────────────────── TAB 2: SỨC CHỨA ───────────────────────────

    def _build_tab_suc_chua(self) -> None:
        """Xây dựng giao diện tab Sức Chứa."""
        # Khung lưu ý nghiệp vụ
        note_card = ctk.CTkFrame(self.tab_succhua, fg_color=CyberpunkTheme.SURFACE, corner_radius=8, border_width=1, border_color=CyberpunkTheme.BORDER_SUBTLE)
        note_card.pack(fill="x", padx=10, pady=(6, 12))

        lbl_note = ctk.CTkLabel(
            note_card,
            text="⚠️ RÀNG BUỘC SỨC CHỨA: Không được giảm tổng sức chứa xuống thấp hơn số lượng xe đang thực tế gửi trong bãi. Hệ thống tự động kiểm tra và từ chối nếu vi phạm điều kiện này.",
            font=CyberpunkTheme.FONT_SMALL,
            text_color=CyberpunkTheme.PINK_NEON,
            justify="left",
            wraplength=850
        )
        lbl_note.pack(padx=16, pady=10, anchor="w")

        # Khung chứa các Card sức chứa của 3 loại xe
        self.cards_succhua_frame = ctk.CTkFrame(self.tab_succhua, fg_color="transparent")
        self.cards_succhua_frame.pack(fill="both", expand=True, padx=6, pady=4)

    def tai_du_lieu_suc_chua(self) -> None:
        """Nạp thông tin sức chứa từ SettingsService và render giao diện."""
        for w in self.cards_succhua_frame.winfo_children():
            w.destroy()

        try:
            danh_sach = SettingsService.lay_suc_chua()
        except Exception as e:
            show_error(self, "Lỗi nạp sức chứa", f"Không thể lấy dữ liệu sức chứa: {e}")
            return

        icon_map = {
            "XeDap": ("🚲", CyberpunkTheme.GREEN_NEON),
            "XeMay": ("🛵", CyberpunkTheme.CYAN_NEON),
            "OTo": ("🚗", CyberpunkTheme.PINK_NEON)
        }

        self.cards_succhua_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="col_sc")

        for idx, item in enumerate(danh_sach):
            lx = item["loai_xe"]
            ten = item["ten_hien_thi"]
            tong_cho = int(item["tong_cho"])
            dang_gui = int(item.get("dang_gui", 0))
            con_trong = int(item.get("con_trong", max(0, tong_cho - dang_gui)))
            ngay_up = str(item.get("ngay_cap_nhat", ""))[:16]

            icon, color = icon_map.get(lx, ("🚘", CyberpunkTheme.CYAN_NEON))

            card = ctk.CTkFrame(
                self.cards_succhua_frame,
                fg_color=CyberpunkTheme.SURFACE,
                corner_radius=12,
                border_width=1,
                border_color=CyberpunkTheme.BORDER_SUBTLE
            )
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")

            # Header Card
            header_box = ctk.CTkFrame(card, fg_color=CyberpunkTheme.SURFACE_CARD, corner_radius=8)
            header_box.pack(fill="x", padx=16, pady=(16, 12))

            ctk.CTkLabel(header_box, text=icon, font=("Segoe UI", 32)).pack(pady=(10, 2))
            ctk.CTkLabel(header_box, text=ten.upper(), font=CyberpunkTheme.FONT_TITLE_SECTION, text_color=color).pack(pady=(0, 10))

            # Thống kê hiện trạng
            stats_box = ctk.CTkFrame(card, fg_color="transparent")
            stats_box.pack(fill="x", padx=20, pady=(4, 10))

            # Hàng 1: Tổng chỗ
            r1 = ctk.CTkFrame(stats_box, fg_color="transparent")
            r1.pack(fill="x", pady=2)
            ctk.CTkLabel(r1, text="Tổng sức chứa:", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(r1, text=f"{tong_cho} chỗ", font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.TEXT_PRIMARY).pack(side="right")

            # Hàng 2: Đang gửi
            r2 = ctk.CTkFrame(stats_box, fg_color="transparent")
            r2.pack(fill="x", pady=2)
            ctk.CTkLabel(r2, text="Đang gửi thực tế:", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(r2, text=f"{dang_gui} xe", font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.PINK_NEON if dang_gui >= tong_cho else CyberpunkTheme.CYAN_NEON).pack(side="right")

            # Hàng 3: Còn trống
            r3 = ctk.CTkFrame(stats_box, fg_color="transparent")
            r3.pack(fill="x", pady=2)
            ctk.CTkLabel(r3, text="Chỗ trống còn lại:", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(r3, text=f"{con_trong} chỗ", font=CyberpunkTheme.FONT_BODY_BOLD, text_color=CyberpunkTheme.GREEN_NEON).pack(side="right")

            # Progress Bar tỷ lệ chiếm chỗ
            ratio = (dang_gui / tong_cho) if tong_cho > 0 else 0
            prog = ctk.CTkProgressBar(
                card,
                height=8,
                fg_color=CyberpunkTheme.SURFACE_INPUT,
                progress_color=CyberpunkTheme.PINK_NEON if ratio > 0.9 else (CyberpunkTheme.CYAN_NEON if ratio > 0.6 else CyberpunkTheme.GREEN_NEON)
            )
            prog.set(min(1.0, ratio))
            prog.pack(fill="x", padx=20, pady=(6, 12))

            # Ô nhập sức chứa mới
            ctk.CTkLabel(card, text="Thiết lập sức chứa mới (số chỗ):", font=CyberpunkTheme.FONT_BODY, text_color=CyberpunkTheme.TEXT_MUTED, anchor="w").pack(fill="x", padx=24, pady=(2, 2))
            entry_sc = ctk.CTkEntry(
                card,
                placeholder_text=str(tong_cho),
                font=CyberpunkTheme.FONT_BODY,
                fg_color=CyberpunkTheme.SURFACE_INPUT,
                height=38
            )
            entry_sc.insert(0, str(tong_cho))
            entry_sc.pack(fill="x", padx=24, pady=(0, 14))

            # Nút Lưu sức chứa
            def _luu_sc(loai=lx, entry=entry_sc, ten_xe=ten, hien_tai=dang_gui):
                val = entry.get().strip()
                if not val.isdigit():
                    show_error(self, "Lỗi nhập liệu", "Vui lòng nhập số chỗ là số nguyên không âm!")
                    return
                sc_moi = int(val)
                if sc_moi < hien_tai:
                    show_error(self, "Vi phạm ràng buộc", f"Không thể giảm sức chứa xuống {sc_moi} chỗ vì đang có {hien_tai} xe đang gửi!")
                    return
                if not show_confirm(self, "Xác nhận cập nhật sức chứa", f"Bạn có chắc muốn đổi sức chứa {ten_xe} thành {sc_moi} chỗ?"):
                    return
                ok, msg = SettingsService.cap_nhat_suc_chua(loai, sc_moi)
                if ok:
                    show_info(self, "Thành công", msg)
                    self.tai_du_lieu_suc_chua()
                else:
                    show_error(self, "Thao tác thất bại", msg)

            btn_save = ctk.CTkButton(
                card,
                text="💾 CẬP NHẬT SỨC CHỨA",
                font=CyberpunkTheme.FONT_BUTTON,
                fg_color=CyberpunkTheme.PURPLE_NEON,
                hover_color=CyberpunkTheme.PURPLE_HOVER,
                text_color=CyberpunkTheme.TEXT_PRIMARY,
                height=38,
                command=_luu_sc
            )
            btn_save.pack(fill="x", padx=24, pady=(0, 10))

            if ngay_up:
                ctk.CTkLabel(card, text=f"Cập nhật: {ngay_up}", font=CyberpunkTheme.FONT_SMALL, text_color=CyberpunkTheme.TEXT_MUTED).pack(pady=(0, 12))
