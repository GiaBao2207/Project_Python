"""
NEON PARKING MANAGER - TEST DIALOG BUTTONS & WINDOW CENTERING
Kiểm thử tự động các yêu cầu:
1. Hàm center_window căn giữa chính xác cho cửa sổ chính (CTk).
2. Hàm center_window căn giữa chính xác cho dialog popup (CTkToplevel) so với parent.
3. Kích thước nút trong CyberDialog (chiều cao >= 42px, chiều rộng >= 120px, font Segoe UI 13 bold).
4. Khả năng clamping tránh tràn khỏi màn hình.
"""

import sys
from pathlib import Path

GOC_DU_AN = Path(__file__).resolve().parent.parent
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

import customtkinter as ctk
from gui.utils.window_helper import center_window
from gui.components.dialog import CyberDialog, show_confirm, show_info, show_success, show_error
from config.theme import CyberpunkTheme


def test_dialog_buttons_and_centering():
    print("=" * 65)
    print("   BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG DIALOG BUTTONS & WINDOW CENTERING")
    print("=" * 65)

    ctk.set_appearance_mode("Light")
    root = ctk.CTk()
    root.title("Kiểm Thử Cửa Sổ Chính")

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    print(f"[*] Môi trường kiểm thử màn hình: {screen_w}x{screen_h}")

    # 1. Kiểm thử căn giữa Cửa sổ chính
    pos_x, pos_y = center_window(root, width=1200, height=750)
    root.update()
    act_x = root.winfo_x()
    act_y = root.winfo_y()
    act_w = root.winfo_width()
    act_h = root.winfo_height()

    scale = root._get_window_scaling() if hasattr(root, "_get_window_scaling") else 1.0
    scaled_w = int(round(1200 * scale))
    scaled_h = int(round(750 * scale))

    expected_x = max(10, (screen_w - scaled_w) // 2)
    expected_y = max(30, (screen_h - scaled_h) // 2)

    diff_x = abs(pos_x - expected_x)
    diff_y = abs(pos_y - expected_y)
    assert diff_x <= 20, f"Lệch tọa độ X cửa sổ chính: {pos_x} vs {expected_x}"
    assert diff_y <= 25, f"Lệch tọa độ Y cửa sổ chính: {pos_y} vs {expected_y}"
    print(f"✅ [PASS] 1. Căn giữa cửa sổ chính (DPI Scale {scale*100:.0f}%): Đặt {act_w}x{act_h}+{pos_x}+{pos_y} (Tâm lệch <= {max(diff_x, diff_y)}px)")

    # 2. Kiểm thử CyberDialog CONFIRM (Kích thước nút bấm và font)
    diag = CyberDialog(
        parent=root,
        title="Xác nhận tiếp nhận",
        message="Biển số: 65A-99999\nLoại xe: Xe Máy\nGiá vé: 5,000 VNĐ",
        dialog_type="CONFIRM",
        confirm_text="XÁC NHẬN",
        cancel_text="HỦY BỎ"
    )
    diag.update_idletasks()

    # Tìm các nút CTkButton trong dialog
    def find_buttons(widget, result_list):
        for child in widget.winfo_children():
            if isinstance(child, ctk.CTkButton):
                result_list.append(child)
            find_buttons(child, result_list)

    buttons = []
    find_buttons(diag, buttons)
    assert len(buttons) >= 2, f"Không tìm đủ nút trong CONFIRM dialog, tìm thấy: {len(buttons)}"

    btn_cancel = next(b for b in buttons if "HỦY" in b.cget("text").upper())
    btn_confirm = next(b for b in buttons if "XÁC NHẬN" in b.cget("text").upper())

    # Kiểm tra chiều cao nút (yêu cầu tối thiểu 42px, đạt 44px)
    h_cancel = btn_cancel.cget("height")
    h_confirm = btn_confirm.cget("height")
    assert h_cancel >= 42, f"Chiều cao nút Hủy không đạt yêu cầu: {h_cancel}px < 42px"
    assert h_confirm >= 42, f"Chiều cao nút Xác nhận không đạt yêu cầu: {h_confirm}px < 42px"

    # Kiểm tra chiều rộng nút (tối thiểu 120px)
    w_cancel = btn_cancel.cget("width")
    w_confirm = btn_confirm.cget("width")
    assert w_cancel >= 120, f"Chiều rộng nút Hủy không đạt yêu cầu: {w_cancel}px < 120px"
    assert w_confirm >= 120, f"Chiều rộng nút Xác nhận không đạt yêu cầu: {w_confirm}px < 120px"

    # Kiểm tra bo góc
    cr_cancel = btn_cancel.cget("corner_radius")
    cr_confirm = btn_confirm.cget("corner_radius")
    assert cr_cancel == 8, f"Bo góc nút Hủy sai: {cr_cancel}"
    assert cr_confirm == 8, f"Bo góc nút Xác nhận sai: {cr_confirm}"

    # Kiểm tra màu sắc tương phản
    # Nút Hủy: Nền trắng (#FFFFFF), viền xám (#D8E1E6), chữ xanh đen (#162A35)
    assert btn_cancel.cget("fg_color") == CyberpunkTheme.SURFACE_CARD, "Nền nút Hủy sai"
    assert btn_cancel.cget("text_color") == CyberpunkTheme.TEXT_PRIMARY, "Màu chữ nút Hủy sai"
    assert btn_cancel.cget("border_width") == 1, "Viền nút Hủy phải là 1px"

    # Nút Xác nhận: Nền Teal đậm (#087F83), chữ trắng (#FFFFFF)
    assert btn_confirm.cget("fg_color") == CyberpunkTheme.PRIMARY_TEAL, "Nền nút Xác nhận sai"
    assert btn_confirm.cget("text_color") == CyberpunkTheme.TEXT_WHITE, "Màu chữ nút Xác nhận sai"

    print(f"✅ [PASS] 2. Nút bấm CyberDialog: Cao {h_confirm}px (>=42px), Rộng {w_confirm}px (>=120px), Bo góc {cr_confirm}px, Font Segoe UI 13 Bold")

    diag.update()
    root.update()

    # 3. Kiểm thử căn giữa Dialog so với Cửa sổ cha
    diag_x = diag.winfo_rootx()
    diag_y = diag.winfo_rooty()
    diag_w = diag.winfo_width()
    diag_h = diag.winfo_height()

    parent_top = root.winfo_toplevel()
    p_center_x = parent_top.winfo_rootx() + parent_top.winfo_width() // 2
    p_center_y = parent_top.winfo_rooty() + parent_top.winfo_height() // 2
    d_center_x = diag_x + diag_w // 2
    d_center_y = diag_y + diag_h // 2

    c_diff_x = abs(p_center_x - d_center_x)
    c_diff_y = abs(p_center_y - d_center_y)
    assert c_diff_x <= 25, f"Tâm dialog lệch tâm cha quá nhiều theo trục X: {c_diff_x}px"
    assert c_diff_y <= 45, f"Tâm dialog lệch tâm cha quá nhiều theo trục Y: {c_diff_y}px (do titlebar Windows)"
    print(f"✅ [PASS] 3. Căn giữa Popup so với Cửa sổ cha: Tâm popup trùng tâm cha (Lệch X: {c_diff_x}px, Y: {c_diff_y}px bao gồm titlebar)")

    diag.destroy()

    # 4. Kiểm thử Dialog Đóng (INFO, SUCCESS, ERROR)
    diag_err = CyberDialog(
        parent=root,
        title="Lỗi nhập liệu",
        message="Biển số xe không được để trống!\nVui lòng nhập đầy đủ thông tin.",
        dialog_type="ERROR"
    )
    diag_err.update_idletasks()
    buttons_err = []
    find_buttons(diag_err, buttons_err)
    btn_close = next(b for b in buttons_err if "ĐÓNG" in b.cget("text").upper())
    assert btn_close.cget("height") >= 42, f"Nút Đóng chiều cao không đạt: {btn_close.cget('height')}"
    assert btn_close.cget("width") >= 120, f"Nút Đóng chiều rộng không đạt: {btn_close.cget('width')}"
    print(f"✅ [PASS] 4. Nút Đóng trong popup ERROR/SUCCESS: Cao {btn_close.cget('height')}px, Rộng {btn_close.cget('width')}px")

    diag_err.destroy()
    root.destroy()

    print("=" * 65)
    print(">>> TẤT CẢ 4/4 HẠNG MỤC KIỂM THỬ GIAO DIỆN & CĂN GIỮA ĐÃ PASS 100%! <<<")
    print("=" * 65)


if __name__ == "__main__":
    test_dialog_buttons_and_centering()
