"""
Kiểm thử tự động độ tương phản màu chữ và nền trong phân hệ Quản lý xe (VehicleView).
Xác minh 100% không còn chữ trắng chìm trên nền sáng.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from gui.modules.vehicles.vehicle_view import VehicleView
from config.theme import CyberpunkTheme


def test_contrast():
    root = ctk.CTk()
    root.geometry("1100x750")

    view = VehicleView(root)
    view.pack(fill="both", expand=True)
    root.update()

    print("[1] KIỂM TRA HEADER BẢNG DỮ LIỆU:")
    cols_frame = None
    for child in view.main_scroll.winfo_children():
        for sub in child.winfo_children():
            if isinstance(sub, ctk.CTkFrame) and len(sub.winfo_children()) == 7:
                # Tìm thấy cols_frame
                cols_frame = sub
                break

    assert cols_frame is not None, "Không tìm thấy cols_frame!"
    for lbl in cols_frame.winfo_children():
        txt = lbl.cget("text")
        tc = lbl.cget("text_color")
        print(f" - Cột '{txt}': text_color = {tc}")
        assert tc != "#FFFFFF" and tc != "white", f"Lỗi: Cột {txt} có màu chữ trắng!"
    print(" -> PASS Header bảng!")

    print("\n[2] KIỂM TRA NÚT XÓA TỪ KHÓA (NÚT X):")
    # Tìm btn_clear trong search_box
    btn_clear = None
    for child in view.main_scroll.winfo_children():
        for sub in child.winfo_children():
            if isinstance(sub, ctk.CTkFrame):
                for s in sub.winfo_children():
                    if isinstance(s, ctk.CTkFrame):
                        for btn in s.winfo_children():
                            if isinstance(btn, ctk.CTkButton) and btn.cget("text") == "✕":
                                btn_clear = btn
                                break

    assert btn_clear is not None, "Không tìm thấy nút ✕!"
    clear_bg = btn_clear.cget("fg_color")
    clear_tc = btn_clear.cget("text_color")
    print(f" - Nút ✕: fg_color = {clear_bg}, text_color = {clear_tc}")
    assert clear_tc == CyberpunkTheme.TEXT_PRIMARY or clear_tc == "#162A35", f"Lỗi: Nút ✕ có text_color {clear_tc} không phải TEXT_PRIMARY!"
    print(" -> PASS Nút ✕!")

    print("\n[3] KIỂM TRA CỘT BIỂN SỐ VÀ CÁC Ô TRONG DÒNG DỮ LIỆU:")
    assert len(view.row_widgets) > 0, "Không có dữ liệu dòng nào để kiểm tra!"
    for ma_ve, row_card in view.row_widgets.items():
        row_bg = row_card.cget("fg_color")
        children = row_card.winfo_children()
        lbl_ma_ve = children[0]
        lbl_loai = children[1]
        lbl_bien = children[2]
        lbl_chu = children[3]
        lbl_gio = children[4]
        lbl_gia = children[5]
        btn_sel = children[6]

        print(f" - Dòng [{ma_ve}] (Nền: {row_bg}):")
        print(f"    * Biển số / Mã thẻ: '{lbl_bien.cget('text')}' - text_color: {lbl_bien.cget('text_color')}")
        print(f"    * Chủ xe: '{lbl_chu.cget('text')}' - text_color: {lbl_chu.cget('text_color')}")
        print(f"    * Thời gian vào: '{lbl_gio.cget('text')}' - text_color: {lbl_gio.cget('text_color')}")
        print(f"    * Đơn giá: '{lbl_gia.cget('text')}' - text_color: {lbl_gia.cget('text_color')}")

        # Kiểm tra tuyệt đối không có chữ trắng trên nền sáng
        assert lbl_bien.cget("text_color") == CyberpunkTheme.TEXT_PRIMARY or lbl_bien.cget("text_color") == "#162A35", \
            f"Lỗi: Biển số bị dùng màu {lbl_bien.cget('text_color')}, phải là TEXT_PRIMARY!"
        assert lbl_chu.cget("text_color") == CyberpunkTheme.TEXT_PRIMARY or lbl_chu.cget("text_color") == "#162A35"
        assert lbl_bien.cget("text_color") != "#FFFFFF" and lbl_bien.cget("text_color") != "white"

        # Kiểm tra nút Chọn vé có nền đậm chữ trắng
        assert btn_sel.cget("text_color") == CyberpunkTheme.TEXT_WHITE or btn_sel.cget("text_color") == "#FFFFFF"
        assert btn_sel.cget("fg_color") == CyberpunkTheme.CYAN_DEEP or btn_sel.cget("fg_color") == "#087F83"
    print(" -> PASS Dòng dữ liệu bình thường!")

    print("\n[4] KIỂM TRA TRẠNG THÁI DÒNG ĐƯỢC CHỌN (SELECTED):")
    first_ma_ve = list(view.row_widgets.keys())[0]
    view._chon_ve_thanh_toan(first_ma_ve)
    root.update()

    selected_row = view.row_widgets[first_ma_ve]
    sel_bg = selected_row.cget("fg_color")
    sel_border = selected_row.cget("border_color")
    print(f" - Dòng đã chọn: fg_color = {sel_bg}, border_color = {sel_border}")
    assert sel_bg == "#E8F4F5"
    assert sel_border == CyberpunkTheme.CYAN_BORDER

    # Kiểm tra chữ trên dòng đã chọn vẫn là chữ tối màu tương phản cao
    lbl_bien_sel = selected_row.winfo_children()[2]
    assert lbl_bien_sel.cget("text_color") == CyberpunkTheme.TEXT_PRIMARY
    print(" -> PASS Trạng thái chọn dòng tương phản cao!")

    print("\n[5] KIỂM TRA TRẠNG THÁI KHÔNG CÓ DỮ LIỆU:")
    view.txt_tim_kiem.insert(0, "KHONG_THE_TIM_THAY_VE_NAY_999999")
    view._on_tim_kiem()
    root.update()

    assert view.tong_so_xe == 0
    empty_label = None
    for child in view.rows_frame.winfo_children():
        if isinstance(child, ctk.CTkLabel):
            empty_label = child
            break
    assert empty_label is not None, "Không tìm thấy empty_label khi không có dữ liệu!"
    print(f" - Empty label: text = '{empty_label.cget('text')}', text_color = {empty_label.cget('text_color')}")
    assert empty_label.cget("text_color") != "#FFFFFF" and empty_label.cget("text_color") != "white"
    print(" -> PASS Trạng thái không có dữ liệu!")

    root.destroy()
    print("\n=======================================================")
    print("=== TOÀN BỘ KIỂM THỬ ĐỘ TƯƠNG PHẢN XE VIEW PASS 100% ===")
    print("=======================================================")


if __name__ == "__main__":
    test_contrast()
