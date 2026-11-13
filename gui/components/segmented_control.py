"""
NEON PARKING MANAGER - LIGHT PREMIUM SEGMENTED CONTROL COMPONENT
Thành phần chuyển đổi tùy chọn (Segmented Control) tùy biến cao cấp:
- Khắc phục triệt để lỗi màu chữ biến mất của CTkSegmentedButton trên nền sáng.
- Trạng thái Đang chọn (Selected): Nền Teal #087F83, Chữ trắng #FFFFFF.
- Trạng thái Chưa chọn (Unselected): Nền trắng #FFFFFF, Chữ đậm #162A35.
- Trạng thái Di chuột (Hover): Nền #E3F2F1, Chữ #075E63.
- Trạng thái Vô hiệu (Disabled): Nền #E5E9ED, Chữ #657786.
- Đầy đủ API tương thích ngược với CTkSegmentedButton (get, set, configure, command, variable).
"""

from typing import List, Callable, Optional, Dict, Any
import customtkinter as ctk
from config.theme import CyberpunkTheme


class SegmentedControl(ctk.CTkFrame):
    """
    Component lựa chọn nhiều trạng thái chuẩn Light Premium Automotive:
    Tự động quản lý màu nền và màu chữ tương phản hoàn hảo theo từng nút riêng biệt.
    """

    COLOR_SELECTED_BG = "#087F83"       # Primary Teal đậm
    COLOR_SELECTED_TEXT = "#FFFFFF"     # Chữ trắng tinh khiết
    COLOR_SELECTED_HOVER = "#096B70"    # Hover nút đang chọn

    COLOR_UNSELECTED_BG = "#FFFFFF"     # Nền trắng tinh khôi
    COLOR_UNSELECTED_TEXT = "#162A35"   # Chữ đen ánh xanh đậm tương phản cao
    COLOR_UNSELECTED_HOVER_BG = "#E3F2F1"   # Nền hover xanh ngọc nhạt cao cấp
    COLOR_UNSELECTED_HOVER_TEXT = "#075E63" # Chữ hover teal đậm

    COLOR_DISABLED_BG = "#E5E9ED"       # Nền vô hiệu hóa
    COLOR_DISABLED_TEXT = "#657786"     # Chữ vô hiệu hóa
    COLOR_BORDER = "#D8E1E6"            # Viền phân cách mỏng

    def __init__(
        self,
        master,
        values: List[str],
        variable: Optional[ctk.StringVar] = None,
        command: Optional[Callable[[str], None]] = None,
        selected_value: Optional[str] = None,
        default_value: Optional[str] = None,
        height: int = 36,
        corner_radius: int = 8,
        font: Optional[Any] = None,
        state: str = "normal",
        **kwargs
    ):
        # Hỗ trợ cả default_value và selected_value
        ban_dau = selected_value or default_value

        super().__init__(
            master,
            fg_color="#F8FAFB",
            border_width=1,
            border_color=self.COLOR_BORDER,
            corner_radius=corner_radius,
            height=height,
            **kwargs
        )
        self.values = list(values)
        self.variable = variable
        self.command = command
        self.control_font = font if font is not None else CyberpunkTheme.FONT_BUTTON
        self.btn_height = max(28, height - 6)
        self.btn_corner_radius = max(4, corner_radius - 2)
        self.state = state

        # Xác định giá trị được chọn ban đầu
        if ban_dau and ban_dau in self.values:
            self._current_value = ban_dau
        elif self.variable and self.variable.get() in self.values:
            self._current_value = self.variable.get()
        elif self.values:
            self._current_value = self.values[0]
        else:
            self._current_value = ""

        if self.variable and self._current_value:
            self.variable.set(self._current_value)

        self.buttons: Dict[str, ctk.CTkButton] = {}
        self._build_buttons()

    def _build_buttons(self) -> None:
        """Khởi tạo danh sách các nút bấm bên trong khung điều khiển."""
        # Xóa các nút cũ nếu có
        for w in self.winfo_children():
            w.destroy()
        self.buttons.clear()

        # Cấu hình grid đồng đều cho các cột
        for col_idx in range(len(self.values)):
            self.columnconfigure(col_idx, weight=1, uniform="seg_btn")
        self.rowconfigure(0, weight=1)

        for col_idx, val in enumerate(self.values):
            is_sel = (val == self._current_value)
            btn = ctk.CTkButton(
                self,
                text=val,
                font=self.control_font,
                height=self.btn_height,
                corner_radius=self.btn_corner_radius,
                border_width=1 if not is_sel else 0,
                border_color=self.COLOR_BORDER if not is_sel else self.COLOR_SELECTED_BG,
                command=lambda v=val: self._on_button_click(v)
            )
            btn.grid(row=0, column=col_idx, padx=2, pady=2, sticky="nsew")

            # Gán sự kiện hover động để đổi màu chữ tinh xảo
            btn.bind("<Enter>", lambda e, v=val: self._on_button_enter(v))
            btn.bind("<Leave>", lambda e, v=val: self._on_button_leave(v))

            self.buttons[val] = btn

        self._cap_nhat_giao_dien()

    def _on_button_click(self, value: str) -> None:
        """Xử lý khi người dùng click chọn một giá trị."""
        if self.state == "disabled":
            return
        if self._current_value == value:
            return  # Đã chọn rồi thì không cần làm lại

        self._current_value = value
        if self.variable:
            self.variable.set(value)

        self._cap_nhat_giao_dien()

        if self.command:
            try:
                self.command(value)
            except Exception as e:
                print(f"[SegmentedControl] Lỗi thực thi callback command: {e}")

    def _on_button_enter(self, value: str) -> None:
        """Hiệu ứng khi di chuột vào nút chưa chọn: Đổi chữ sang teal đậm #075E63."""
        if self.state == "disabled":
            return
        if value != self._current_value and value in self.buttons:
            self.buttons[value].configure(
                text_color=self.COLOR_UNSELECTED_HOVER_TEXT,
                fg_color=self.COLOR_UNSELECTED_HOVER_BG
            )

    def _on_button_leave(self, value: str) -> None:
        """Khôi phục trạng thái khi rời chuột khỏi nút."""
        if self.state == "disabled":
            return
        if value != self._current_value and value in self.buttons:
            self.buttons[value].configure(
                text_color=self.COLOR_UNSELECTED_TEXT,
                fg_color=self.COLOR_UNSELECTED_BG
            )

    def _cap_nhat_giao_dien(self) -> None:
        """Cập nhật màu sắc của toàn bộ các nút theo trạng thái hiện thời."""
        is_disabled = (self.state == "disabled")

        for val, btn in self.buttons.items():
            if is_disabled:
                btn.configure(
                    state="disabled",
                    fg_color=self.COLOR_DISABLED_BG,
                    text_color=self.COLOR_DISABLED_TEXT,
                    border_width=1,
                    border_color=self.COLOR_BORDER
                )
            elif val == self._current_value:
                # Nút đang được chọn (Selected)
                btn.configure(
                    state="normal",
                    fg_color=self.COLOR_SELECTED_BG,
                    text_color=self.COLOR_SELECTED_TEXT,
                    hover_color=self.COLOR_SELECTED_HOVER,
                    border_width=0
                )
            else:
                # Nút chưa chọn (Unselected)
                btn.configure(
                    state="normal",
                    fg_color=self.COLOR_UNSELECTED_BG,
                    text_color=self.COLOR_UNSELECTED_TEXT,
                    hover_color=self.COLOR_UNSELECTED_HOVER_BG,
                    border_width=1,
                    border_color=self.COLOR_BORDER
                )

    def get(self) -> str:
        """Trả về giá trị đang được chọn."""
        return self._current_value

    def set(self, value: str) -> None:
        """Đặt giá trị được chọn theo lập trình."""
        if value in self.buttons and value != self._current_value:
            self._current_value = value
            if self.variable:
                self.variable.set(value)
            self._cap_nhat_giao_dien()

    def configure(self, **kwargs) -> None:
        """Cấu hình lại các thuộc tính."""
        if "state" in kwargs:
            self.state = kwargs.pop("state")
            self._cap_nhat_giao_dien()
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "values" in kwargs:
            self.values = list(kwargs.pop("values"))
            if self._current_value not in self.values and self.values:
                self._current_value = self.values[0]
                if self.variable:
                    self.variable.set(self._current_value)
            self._build_buttons()
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> Any:
        """Lấy giá trị thuộc tính tương thích ngược với CTkSegmentedButton."""
        if attribute_name == "values":
            return self.values
        if attribute_name == "variable":
            return self.variable
        if attribute_name == "state":
            return self.state
        return super().cget(attribute_name)
