"""
NEON PARKING MANAGER - WINDOW HELPER UTILITIES
Module cung cấp tiện ích tính toán và căn giữa cửa sổ (Center Window).
Hỗ trợ cả cửa sổ chính (CTk) và cửa sổ con/popup (CTkToplevel).
Tương thích với các độ phân giải màn hình khác nhau (1366x768, 1920x1080...)
và xử lý an toàn giới hạn hiển thị (clamping) tránh tràn khỏi màn hình.
"""

import customtkinter as ctk
from typing import Optional, Tuple, Any


def center_window(
    window: Any,
    width: Optional[int] = None,
    height: Optional[int] = None,
    parent: Optional[Any] = None
) -> Tuple[int, int]:
    """
    Căn giữa cửa sổ (CTk hoặc CTkToplevel) trên màn hình hoặc so với cửa sổ cha.

    Tham số:
        window: Cửa sổ cần căn giữa (CTk hoặc CTkToplevel).
        width: Chiều rộng mong muốn (nếu None sẽ lấy từ window hoặc reqwidth).
        height: Chiều cao mong muốn (nếu None sẽ lấy từ window hoặc reqheight).
        parent: Cửa sổ cha để căn giữa theo (nếu có). Nếu None, căn giữa màn hình.

    Trả về:
        Tuple[int, int]: Tọa độ (pos_x, pos_y) sau khi căn giữa.
    """
    # 1. Cập nhật kích thước widget để đọc thông số chính xác
    try:
        window.update_idletasks()
    except Exception:
        pass

    # 2. Lấy kích thước màn hình
    try:
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
    except Exception:
        screen_w, screen_h = 1920, 1080

    # 3. Xác định kích thước mong muốn (width x height)
    target_w = width
    target_h = height

    if target_w is None or target_w <= 0:
        w_cur = window.winfo_width()
        w_req = window.winfo_reqwidth()
        target_w = w_cur if w_cur > 10 else (w_req if w_req > 10 else 520)

    if target_h is None or target_h <= 0:
        h_cur = window.winfo_height()
        h_req = window.winfo_reqheight()
        target_h = h_cur if h_cur > 10 else (h_req if h_req > 10 else 320)

    # 4. Xác định hệ số DPI Scaling của CustomTkinter (ví dụ 1.25 trên màn hình 125%)
    scale_factor = 1.0
    if hasattr(window, "_get_window_scaling"):
        try:
            scale_factor = float(window._get_window_scaling())
        except Exception:
            scale_factor = 1.0

    # Kích thước thực tế mà CustomTkinter sẽ hiển thị trên màn hình hệ điều hành
    scaled_w = int(round(target_w * scale_factor))
    scaled_h = int(round(target_h * scale_factor))

    # Điều chỉnh kích thước an toàn nếu vượt quá vùng làm việc của màn hình
    # Dành tối thiểu 4% chiều rộng và 10% chiều cao cho Taskbar và viền hệ thống
    if scaled_w > int(screen_w * 0.96):
        scaled_w = int(screen_w * 0.96)
        target_w = int(round(scaled_w / scale_factor))

    if scaled_h > int(screen_h * 0.90):
        scaled_h = int(screen_h * 0.90)
        target_h = int(round(scaled_h / scale_factor))

    # 5. Tính toán tọa độ vị trí X và Y (Pixel thực tế trên màn hình)
    pos_x = 0
    pos_y = 0

    if parent is not None:
        try:
            # Tìm cửa sổ cấp cao nhất của parent (nếu parent là Frame hoặc Widget con)
            top_parent = parent.winfo_toplevel() if hasattr(parent, "winfo_toplevel") else parent
            top_parent.update_idletasks()

            # Lấy tọa độ tuyệt đối trên màn hình của cửa sổ cha
            px = top_parent.winfo_rootx()
            py = top_parent.winfo_rooty()
            pw = top_parent.winfo_width()
            ph = top_parent.winfo_height()

            # Trích xuất thêm từ geometry() nếu Tkinter chưa kịp cập nhật event Configure
            import re
            geom_match = re.match(r"^(\d+)x(\d+)(?:([+-]\d+))?(?:([+-]\d+))?", top_parent.geometry())
            if geom_match:
                gw = int(geom_match.group(1))
                gh = int(geom_match.group(2))
                gx = int(geom_match.group(3)) if geom_match.group(3) is not None else None
                gy = int(geom_match.group(4)) if geom_match.group(4) is not None else None

                parent_scale = top_parent._get_window_scaling() if hasattr(top_parent, "_get_window_scaling") else scale_factor
                gw_scaled = int(round(gw * parent_scale))
                gh_scaled = int(round(gh * parent_scale))

                if pw <= 200 or pw < gw_scaled:
                    pw = gw_scaled
                if ph <= 200 or ph < gh_scaled:
                    ph = gh_scaled
                if px <= 0 and gx is not None and gx > 0:
                    px = gx
                if py <= 0 and gy is not None and gy > 0:
                    py = gy

            # Căn giữa tâm popup trùng với tâm cửa sổ cha (theo pixel thực tế)
            pos_x = px + (pw - scaled_w) // 2
            pos_y = py + (ph - scaled_h) // 2
        except Exception:
            # Dự phòng: Căn giữa màn hình nếu không lấy được thông tin parent
            pos_x = (screen_w - scaled_w) // 2
            pos_y = (screen_h - scaled_h) // 2
    else:
        # Căn giữa hoàn toàn trên màn hình chính (theo pixel thực tế)
        pos_x = max(0, (screen_w - scaled_w) // 2)
        pos_y = max(0, (screen_h - scaled_h) // 2)

    # 6. Clamping an toàn: Đảm bảo cửa sổ không bị lọt ra ngoài mép màn hình
    # Chừa 10px lề ngang và 40px lề dọc (tránh Taskbar Windows)
    pos_x = max(10, min(pos_x, max(10, screen_w - scaled_w - 10)))
    pos_y = max(30, min(pos_y, max(30, screen_h - scaled_h - 45)))

    # 7. Áp dụng geometry một lần duy nhất
    window.geometry(f"{target_w}x{target_h}+{pos_x}+{pos_y}")

    return pos_x, pos_y
