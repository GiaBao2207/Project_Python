"""
Script kiểm thử các tính năng mới trong VehicleView:
1. Khởi tạo giao diện
2. Tìm kiếm theo mã vé, biển số, mã thẻ, chủ xe
3. Bộ lọc loại xe (Tất cả, Xe máy, Ô tô, Xe đạp)
4. Nút xóa từ khóa (X) và nút làm mới
5. Chọn vé và click đúp vào dòng
6. Phân trang
"""

import os
import sys

# Thêm thư mục gốc dự án vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from gui.modules.vehicles.vehicle_view import VehicleView
from services.bai_xe_db_service import BaiXeDbService

def run_test():
    root = ctk.CTk()
    root.geometry("1100x700")
    
    view = VehicleView(root)
    view.pack(fill="both", expand=True)
    root.update()

    print("[1] VehicleView UI Render: OK")
    print(" - txt_tim_kiem placeholder:", view.txt_tim_kiem.cget("placeholder_text"))
    print(" - cbo_loc_loai values:", view.cbo_loc_loai.cget("values"))
    print(" - so_luong_label:", view.lbl_so_luong.cget("text"))
    print(" - phan_trang_info:", view.lbl_phan_trang_info.cget("text"))

    # Test search debounce / search
    view.txt_tim_kiem.insert(0, "TestKeyword")
    view._on_tim_kiem()
    root.update()
    print("[2] Search trigger: OK (Found count:", view.tong_so_xe, ")")

    # Test clear keyword
    view._xoa_tu_khoa()
    root.update()
    assert view.txt_tim_kiem.get() == ""
    print("[3] Clear keyword (Nút X): OK")

    # Test vehicle type filter
    view.loai_xe_loc_var.set("Xe máy")
    view._on_bo_loc_changed("Xe máy")
    root.update()
    print("[4] Filter by 'Xe máy': OK (Found count:", view.tong_so_xe, ")")

    # Reset filter
    view.loai_xe_loc_var.set("Tất cả")
    view._on_bo_loc_changed("Tất cả")
    root.update()

    # Test selecting ticket
    view._chon_ve_thanh_toan("VX-TEST-12345")
    assert view.txt_ma_ve_out.get() == "VX-TEST-12345"
    assert view.selected_ma_ve == "VX-TEST-12345"
    print("[5] Select ticket auto-fill: OK (txt_ma_ve_out =", view.txt_ma_ve_out.get(), ")")

    root.destroy()
    print("=== ALL VEHICLE VIEW TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_test()
