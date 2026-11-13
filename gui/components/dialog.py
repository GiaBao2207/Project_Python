"""
NEON PARKING MANAGER - CYBERPUNK DIALOG SYSTEM
Hộp thoại Popup 2 lớp (Dual-layer Dialog) mang phong cách Cyberpunk Neon:
- Khung ngoài (Outer Modal Window): Viền phát sáng Neon, Icon & Tiêu đề chính.
- Khung nội dung bên trong (Inner Content Box / Detail Card): Nền tối sâu tách biệt,
  viền riêng, bo góc, phân cấp thị giác rõ ràng giữa Label và Value.
"""

import customtkinter as ctk
from typing import Callable, Optional, List, Tuple, Any
from config.theme import CyberpunkTheme
from gui.utils.window_helper import center_window


def _parse_message_lines(raw_message: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Tự động phân tách chuỗi message thành:
    - intro_text: Đoạn văn bản mở đầu (nếu có).
    - pairs: Danh sách các cặp (Label, Value) nếu dòng có định dạng 'Nhãn: Giá trị' hoặc '• Nhãn: Giá trị'.
    """
    if not raw_message or not raw_message.strip():
        return "", []

    lines = [line.strip() for line in raw_message.strip().split("\n") if line.strip()]
    intro_lines = []
    pairs = []

    for line in lines:
        cleaned = line.lstrip("•-*▫> ").strip()
        if ":" in cleaned:
            parts = cleaned.split(":", 1)
            k = parts[0].strip()
            v = parts[1].strip()
            # Nếu phần label ngắn gọn (<= 35 ký tự), coi là cặp label: value
            if 1 <= len(k) <= 35 and v:
                pairs.append((k, v))
                continue
        intro_lines.append(line)

    intro_text = "\n".join(intro_lines)
    return intro_text, pairs


class CyberDialog(ctk.CTkToplevel):
    """
    Cửa sổ popup 2 lớp cao cấp phong cách Cyberpunk Neon.
    Tự động co giãn kích thước, căn giữa cửa sổ cha và hỗ trợ cả callback lẫn return boolean.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        title: str,
        message: str = "",
        details: Optional[List[Tuple[str, Any]]] = None,
        card_title: Optional[str] = None,
        dialog_type: str = "INFO",  # 'INFO', 'SUCCESS', 'ERROR', 'CONFIRM'
        on_confirm: Optional[Callable[[], None]] = None,
        confirm_text: str = "XÁC NHẬN",
        cancel_text: str = "HỦY BỎ"
    ):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()  # Chế độ modal chặn tương tác với cửa sổ cha
        self.result = False  # Kết quả trả về cho show_confirm synchronous
        self.title(title)

        # 1. Phân loại cấu hình màu sắc theo dialog_type
        if dialog_type == "SUCCESS":
            neon_color = CyberpunkTheme.SUCCESS
            icon_char = "✔"
            btn_bg = CyberpunkTheme.SUCCESS
            btn_hover = CyberpunkTheme.SUCCESS_HOVER
            btn_border = CyberpunkTheme.SUCCESS
            default_card_title = "THÔNG TIN GIAO DỊCH"
            card_title_color = CyberpunkTheme.SUCCESS
            card_border_color = CyberpunkTheme.BORDER_SUBTLE
        elif dialog_type == "ERROR":
            neon_color = CyberpunkTheme.ERROR
            icon_char = "✖"
            btn_bg = CyberpunkTheme.ERROR
            btn_hover = CyberpunkTheme.ERROR_HOVER
            btn_border = CyberpunkTheme.ERROR
            default_card_title = "CHI TIẾT LỖI / CẢNH BÁO"
            card_title_color = CyberpunkTheme.ERROR
            card_border_color = CyberpunkTheme.BORDER_SUBTLE
        elif dialog_type == "CONFIRM":
            neon_color = CyberpunkTheme.PRIMARY_TEAL
            icon_char = "❓"
            btn_bg = CyberpunkTheme.PRIMARY_TEAL
            btn_hover = CyberpunkTheme.PRIMARY_HOVER
            btn_border = CyberpunkTheme.PRIMARY_TEAL
            default_card_title = "THÔNG TIN XÁC NHẬN"
            card_title_color = CyberpunkTheme.PRIMARY_TEAL
            card_border_color = CyberpunkTheme.BORDER_SUBTLE
        else:
            neon_color = CyberpunkTheme.PRIMARY_TEAL
            icon_char = "ℹ"
            btn_bg = CyberpunkTheme.PRIMARY_TEAL
            btn_hover = CyberpunkTheme.PRIMARY_HOVER
            btn_border = CyberpunkTheme.PRIMARY_TEAL
            default_card_title = "CHI TIẾT THÔNG BÁO"
            card_title_color = CyberpunkTheme.PRIMARY_TEAL
            card_border_color = CyberpunkTheme.BORDER_SUBTLE

        card_title_final = card_title if card_title else default_card_title

        # 2. Xử lý dữ liệu: Tách intro text và danh sách cặp Label-Value
        if details is not None:
            final_details = details
            intro_text = message.strip()
            free_text = ""
        else:
            intro_text, parsed_pairs = _parse_message_lines(message)
            if parsed_pairs:
                final_details = parsed_pairs
                free_text = ""
            else:
                final_details = []
                free_text = message.strip()

        # 3. Tính toán kích thước cửa sổ linh hoạt theo nội dung
        win_w = 540
        num_rows = len(final_details)
        if num_rows > 0:
            base_h = 270
            if intro_text:
                base_h += 38
            win_h = base_h + (num_rows * 30)
        else:
            text_lines = len(free_text.split("\n"))
            win_h = max(290, 240 + text_lines * 24)

        win_h = max(290, min(620, win_h))

        self.minsize(500, 280)
        self.resizable(False, False)
        self.configure(fg_color=CyberpunkTheme.BG_DARK)

        # Căn giữa cửa sổ con so với cửa sổ cha hoặc màn hình bằng center_window
        center_window(self, width=win_w, height=win_h, parent=parent)

        # ─── LỚP 1: KHUNG NGOÀI (POPUP TỔNG CÓ VIỀN NEON PHÁT SÁNG) ───
        main_frame = ctk.CTkFrame(
            self,
            fg_color=CyberpunkTheme.SURFACE,
            corner_radius=12,
            border_width=2,
            border_color=neon_color
        )
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Header với Icon và Tiêu đề chính
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=18, pady=(16, 8))

        lbl_icon = ctk.CTkLabel(
            header_frame,
            text=icon_char,
            font=("Segoe UI", 20, "bold"),
            text_color=neon_color,
            width=32
        )
        lbl_icon.pack(side="left", padx=(0, 10))

        lbl_title = ctk.CTkLabel(
            header_frame,
            text=title.upper(),
            font=CyberpunkTheme.FONT_TITLE_SECTION,
            text_color=CyberpunkTheme.TEXT_PRIMARY
        )
        lbl_title.pack(side="left")

        # Đường kẻ phân cách mỏng
        divider = ctk.CTkFrame(main_frame, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE)
        divider.pack(fill="x", padx=18, pady=4)

        # Đoạn văn bản tóm tắt phía trên khung chi tiết (nếu có)
        if intro_text:
            lbl_intro = ctk.CTkLabel(
                main_frame,
                text=intro_text,
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_PRIMARY,
                wraplength=470,
                justify="left",
                anchor="w"
            )
            lbl_intro.pack(fill="x", padx=20, pady=(6, 4))

        # ─── LỚP 2: KHUNG THÔNG TIN BÊN TRONG (INNER CONTENT BOX / DETAIL CARD) ───
        # Nền tách biệt (SURFACE_INPUT = #0F1220), có viền riêng, bo góc, có khoảng cách với khung ngoài
        inner_card = ctk.CTkFrame(
            main_frame,
            fg_color=CyberpunkTheme.SURFACE_INPUT,
            corner_radius=8,
            border_width=1,
            border_color=card_border_color
        )
        inner_card.pack(fill="both", expand=True, padx=18, pady=(4, 12))

        # Tiêu đề nhỏ bên trong khung nội dung
        card_head = ctk.CTkFrame(inner_card, fg_color="transparent")
        card_head.pack(fill="x", padx=16, pady=(10, 4))

        ctk.CTkLabel(
            card_head,
            text=f"▫ {card_title_final.upper()}",
            font=("Segoe UI", 9, "bold"),
            text_color=card_title_color,
            anchor="w"
        ).pack(side="left")

        # Đường gạch chân tiêu đề khung
        ctk.CTkFrame(inner_card, height=1, fg_color=CyberpunkTheme.BORDER_SUBTLE).pack(fill="x", padx=14, pady=(2, 6))

        # Trình bày nội dung chi tiết
        if final_details:
            # Dạng bảng phân cấp thị giác Label (nhạt) + Value (nổi bật)
            rows_box = ctk.CTkFrame(inner_card, fg_color="transparent")
            rows_box.pack(fill="both", expand=True, padx=16, pady=(2, 10))

            for label_text, val_text in final_details:
                row = ctk.CTkFrame(rows_box, fg_color="transparent", height=24)
                row.pack(fill="x", pady=2)

                lbl = ctk.CTkLabel(
                    row,
                    text=str(label_text),
                    font=("Segoe UI", 10),
                    text_color=CyberpunkTheme.TEXT_MUTED,
                    anchor="w"
                )
                lbl.pack(side="left")

                val_str = str(val_text)
                lbl_up = str(label_text).upper()

                # Phân cấp màu sắc và font chữ cho Value (mặc định là chữ tối màu tương phản cao)
                val_color = CyberpunkTheme.TEXT_PRIMARY
                val_font = ("Segoe UI", 10, "bold")

                if "MÃ VÉ" in lbl_up or lbl_up.endswith("VÉ"):
                    val_color = CyberpunkTheme.CYAN_BORDER
                    val_font = ("Consolas", 10, "bold")
                elif any(k in lbl_up for k in ("TIỀN", "PHÍ", "GIÁ", "DOANH THU", "ĐƠN GIÁ")):
                    val_color = CyberpunkTheme.GREEN_NEON
                    val_font = ("Segoe UI", 10, "bold")
                elif any(k in lbl_up for k in ("LỖI", "CẢNH BÁO", "NGUYÊN NHÂN", "TỪ CHỐI")):
                    val_color = CyberpunkTheme.PINK_NEON
                    val_font = ("Segoe UI", 10, "bold")
                elif any(k in lbl_up for k in ("THỜI GIAN", "NGÀY")):
                    val_color = CyberpunkTheme.TEXT_PRIMARY
                    val_font = ("Segoe UI", 10)

                val = ctk.CTkLabel(
                    row,
                    text=val_str,
                    font=val_font,
                    text_color=val_color,
                    anchor="e"
                )
                val.pack(side="right")
        else:
            # Dạng văn bản tự do nằm gọn gàng trong khung nội dung
            lbl_body = ctk.CTkLabel(
                inner_card,
                text=free_text,
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_PRIMARY,
                wraplength=460,
                justify="left",
                anchor="w"
            )
            lbl_body.pack(fill="both", expand=True, padx=16, pady=(4, 12))

        # ─── NÚT BẤM DƯỚI CHÂN POPUP (CHIỀU CAO 44PX, RỘNG TỐI THIỂU 135PX, FONT SEGOE UI 13 BOLD) ───
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=18, pady=(4, 18))

        FONT_DIALOG_BTN = ("Segoe UI", 13, "bold")

        if dialog_type == "CONFIRM":
            def handle_confirm():
                self.result = True
                self.destroy()
                if on_confirm:
                    on_confirm()

            def handle_cancel():
                self.result = False
                self.destroy()

            # Nút Xác nhận (Nền Teal đậm #087F83, chữ trắng, cao 44px, rộng 135px, bo góc 8px)
            btn_ok = ctk.CTkButton(
                btn_frame,
                text=confirm_text,
                font=FONT_DIALOG_BTN,
                fg_color=btn_bg,
                text_color=CyberpunkTheme.TEXT_WHITE,
                hover_color=btn_hover,
                border_width=1,
                border_color=btn_border,
                corner_radius=8,
                width=135,
                height=44,
                command=handle_confirm
            )
            btn_ok.pack(side="right", padx=(14, 0))

            # Nút Hủy (Nền trắng #FFFFFF, viền xám, chữ xanh đen #162A35, hover #F0F4F7, cao 44px, rộng 135px)
            btn_cancel = ctk.CTkButton(
                btn_frame,
                text=cancel_text,
                font=FONT_DIALOG_BTN,
                fg_color=CyberpunkTheme.SURFACE_CARD,
                text_color=CyberpunkTheme.TEXT_PRIMARY,
                hover_color=CyberpunkTheme.SURFACE_HOVER,
                border_width=1,
                border_color=CyberpunkTheme.BORDER_SUBTLE,
                corner_radius=8,
                width=135,
                height=44,
                command=handle_cancel
            )
            btn_cancel.pack(side="right")
        else:
            # Nút Đóng đơn giản (Cao 44px, rộng 135px, bo góc 8px, font Segoe UI 13 Bold)
            btn_close = ctk.CTkButton(
                btn_frame,
                text="ĐÓNG",
                font=FONT_DIALOG_BTN,
                fg_color=btn_bg,
                text_color=CyberpunkTheme.TEXT_WHITE,
                hover_color=btn_hover,
                border_width=1,
                border_color=btn_border,
                corner_radius=8,
                width=135,
                height=44,
                command=self.destroy
            )
            btn_close.pack(side="right")


# ──────────────────────────────────────────────────────────────────────────
# CÁC TIỆN ÍCH POPUP DÙNG CHUNG TOÀN HỆ THỐNG
# ──────────────────────────────────────────────────────────────────────────

def show_error(
    parent: ctk.CTk,
    title: str,
    message: str = "",
    details: Optional[List[Tuple[str, Any]]] = None,
    card_title: Optional[str] = None
) -> None:
    """Hiển thị popup cảnh báo lỗi phong cách Cyberpunk Pink Neon với khung chi tiết lỗi."""
    CyberDialog(
        parent,
        title=title,
        message=message,
        details=details,
        card_title=card_title,
        dialog_type="ERROR"
    )


def show_success(
    parent: ctk.CTk,
    title: str,
    message: str = "",
    details: Optional[List[Tuple[str, Any]]] = None,
    card_title: Optional[str] = None
) -> None:
    """Hiển thị popup thông báo thành công phong cách Cyberpunk Green Neon với khung chi tiết."""
    CyberDialog(
        parent,
        title=title,
        message=message,
        details=details,
        card_title=card_title,
        dialog_type="SUCCESS"
    )


def show_info(
    parent: ctk.CTk,
    title: str,
    message: str = "",
    details: Optional[List[Tuple[str, Any]]] = None,
    card_title: Optional[str] = None
) -> None:
    """Hiển thị popup thông tin phong cách Cyberpunk Cyan Neon với khung chi tiết."""
    CyberDialog(
        parent,
        title=title,
        message=message,
        details=details,
        card_title=card_title,
        dialog_type="INFO"
    )


def show_confirm(
    parent: ctk.CTk,
    title: str,
    message: str = "",
    on_confirm: Optional[Callable[[], None]] = None,
    details: Optional[List[Tuple[str, Any]]] = None,
    card_title: Optional[str] = None,
    confirm_text: str = "XÁC NHẬN",
    cancel_text: str = "HỦY BỎ"
) -> bool:
    """
    Hiển thị popup yêu cầu xác nhận thao tác quan trọng.
    Hỗ trợ cả cơ chế callback (on_confirm) lẫn cơ chế synchronous trả về True/False.
    """
    diag = CyberDialog(
        parent,
        title=title,
        message=message,
        details=details,
        card_title=card_title,
        dialog_type="CONFIRM",
        on_confirm=on_confirm,
        confirm_text=confirm_text,
        cancel_text=cancel_text
    )
    diag.wait_window()
    return diag.result
