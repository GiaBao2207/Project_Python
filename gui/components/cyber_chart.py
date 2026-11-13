"""
NEON PARKING MANAGER - CYBERPUNK MATPLOTLIB CHART COMPONENT
Cung cấp tiện ích vẽ và nhúng biểu đồ Matplotlib với phong cách Cyberpunk Neon
vào các màn hình CustomTkinter (Dashboard, Doanh thu, Thống kê).
"""

from typing import List, Tuple, Optional, Dict, Any
import tkinter as tk
import customtkinter as ctk
from config.theme import CyberpunkTheme

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_SAN_SANG = True
except ImportError:
    MATPLOTLIB_SAN_SANG = False


class CyberChart:
    """Tiện ích tạo và nhúng biểu đồ Matplotlib chuẩn phong cách Light Premium."""

    BG_CANVAS = "#FFFFFF"
    BG_PLOT = "#F8FAFB"
    GRID_COLOR = "#D8E1E6"
    TEXT_COLOR = "#617482"
    CYAN = "#087F83"       # Primary Teal
    PINK = "#C34F5C"       # Error / Cao điểm
    GREEN = "#268667"      # Success
    PURPLE = "#C5A46D"     # Gold Accent

    @classmethod
    def co_the_ve(cls) -> bool:
        """Kiểm tra môi trường có sẵn thư viện Matplotlib hay không."""
        return MATPLOTLIB_SAN_SANG

    @classmethod
    def tao_figure_chuan(cls, figsize=(6, 2.8), dpi=100) -> Tuple[Any, Any]:
        """Tạo Figure và Axes với theme Cyberpunk tối màu."""
        fig = Figure(figsize=figsize, dpi=dpi, facecolor=cls.BG_CANVAS)
        ax = fig.add_subplot(111)
        ax.set_facecolor(cls.BG_PLOT)

        # Viền đồ thị
        for spine in ax.spines.values():
            spine.set_color(cls.GRID_COLOR)
            spine.set_linewidth(1)

        # Lưới
        ax.grid(True, linestyle="--", alpha=0.3, color=cls.GRID_COLOR)

        # Ticks
        ax.tick_params(colors=cls.TEXT_COLOR, labelsize=8)
        return fig, ax

    @classmethod
    def nhung_vao_container(cls, fig, container) -> Optional[Any]:
        """
        Nhúng Figure vào CTkFrame/TkFrame và trả về canvas widget.
        Tự động đóng figure cũ để tránh rò rỉ bộ nhớ.
        """
        if not MATPLOTLIB_SAN_SANG:
            return None

        # Xóa các widget cũ trong container
        for w in container.winfo_children():
            w.destroy()

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        return canvas

    @classmethod
    def ve_bieu_do_cot_7_ngay(cls, container, cac_ngay: List[Tuple[Any, int]]) -> None:
        """
        Vẽ biểu đồ cột 7 ngày gần nhất cho Dashboard.
        cac_ngay: List[(ngay, so_luot)]
        """
        if not MATPLOTLIB_SAN_SANG:
            return

        fig, ax = cls.tao_figure_chuan(figsize=(5.5, 2.2))

        labels = []
        values = []
        colors = []
        for i, (ngay, sl) in enumerate(cac_ngay):
            is_today = (i == len(cac_ngay) - 1)
            ten = "Hôm nay" if is_today else f"{ngay.day}/{ngay.month}"
            labels.append(ten)
            values.append(sl)
            colors.append(cls.GREEN if is_today else cls.CYAN)

        bars = ax.bar(labels, values, color=colors, width=0.55, edgecolor=cls.BG_CANVAS, linewidth=1)

        # Hiển thị số lượt trên đầu cột nếu > 0
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.annotate(
                    f"{int(h)}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 2),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=8, color=cls.CYAN, fontweight="bold"
                )

        ax.set_ylabel("Lượt xe", color=cls.TEXT_COLOR, fontsize=8)
        max_v = max(values) if values else 1
        ax.set_ylim(0, max(max_v * 1.25, 5))
        fig.tight_layout(pad=1.0)
        cls.nhung_vao_container(fig, container)

    @classmethod
    def ve_bieu_do_gio_cao_diem(cls, container, gio_cao_diem: List[Dict[str, Any]]) -> None:
        """
        Vẽ biểu đồ phân tích 24h giờ cao điểm cho StatisticsView.
        """
        if not MATPLOTLIB_SAN_SANG:
            return

        fig, ax = cls.tao_figure_chuan(figsize=(8, 2.6))

        gio_dict = {int(r["gio"]): int(r["so_luot"]) for r in gio_cao_diem}
        hours = list(range(24))
        counts = [gio_dict.get(h, 0) for h in hours]
        max_count = max(counts) if counts else 1

        colors = [cls.PINK if c == max_count and c > 0 else cls.CYAN for c in counts]

        bars = ax.bar(hours, counts, color=colors, width=0.68)

        ax.set_xticks(hours[::2])  # 0h, 2h, 4h, ...
        ax.set_xticklabels([f"{h}h" for h in hours[::2]], fontsize=8)
        ax.set_ylabel("Lượt xe", color=cls.TEXT_COLOR, fontsize=8)
        ax.set_title("PHÂN BỐ LƯỢT XE VÀO THEO KHUNG GIỜ (30 NGÀY GẦN NHẤT)", color=cls.CYAN, fontsize=9, fontweight="bold")
        ax.set_ylim(0, max(max_count * 1.25, 4))

        fig.tight_layout(pad=1.0)
        cls.nhung_vao_container(fig, container)

    @classmethod
    def ve_bieu_do_doanh_thu_ngay(cls, container, data_ngay: List[Dict[str, Any]]) -> None:
        """
        Vẽ biểu đồ đường/cột doanh thu theo ngày cho RevenueView.
        data_ngay: List[{'ngay': ..., 'tien_mat': ..., 'chuyen_khoan': ..., 'tong_cong': ...}]
        """
        if not MATPLOTLIB_SAN_SANG:
            return

        if not data_ngay:
            # Container rỗng
            for w in container.winfo_children():
                w.destroy()
            ctk.CTkLabel(
                container,
                text="Chưa có dữ liệu doanh thu trong khoảng ngày này.",
                font=CyberpunkTheme.FONT_BODY,
                text_color=CyberpunkTheme.TEXT_MUTED
            ).pack(pady=30)
            return

        fig, ax = cls.tao_figure_chuan(figsize=(8, 2.6))

        # Đảo ngược lại theo thứ tự thời gian tăng dần
        items = list(reversed(data_ngay[-15:]))  # Tối đa 15 ngày gần nhất
        labels = [str(r["ngay"])[5:] for r in items]  # MM-DD
        tien_mat = [int(r.get("tien_mat", 0)) / 1000 for r in items]  # k VNĐ
        chuyen_khoan = [int(r.get("chuyen_khoan", 0)) / 1000 for r in items]

        # Stacked bar
        w = 0.55
        bars1 = ax.bar(labels, tien_mat, width=w, label="Tiền mặt", color=cls.GREEN)
        bars2 = ax.bar(labels, chuyen_khoan, width=w, bottom=tien_mat, label="Chuyển khoản", color=cls.CYAN)

        ax.set_ylabel("Nghìn VNĐ", color=cls.TEXT_COLOR, fontsize=8)
        ax.set_title("XU HƯỚNG DOANH THU CÁC NGÀY GẦN NHẤT", color=cls.CYAN, fontsize=9, fontweight="bold")
        ax.legend(facecolor=cls.BG_PLOT, edgecolor=cls.GRID_COLOR, labelcolor=cls.TEXT_COLOR, fontsize=8)

        fig.tight_layout(pad=1.0)
        cls.nhung_vao_container(fig, container)
