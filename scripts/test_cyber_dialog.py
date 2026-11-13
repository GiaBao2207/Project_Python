"""
Script kiểm thử tự động toàn diện hệ thống Popup 2 lớp (Dual-layer Dialog) CyberDialog:
1. Tiếp nhận thành công (Card THÔNG TIN TIẾP NHẬN với 6 trường chi tiết)
2. Thanh toán thành công (Card CHI TIẾT GIAO DỊCH)
3. Cảnh báo / Lỗi (Card CHI TIẾT LỖI)
4. Xác nhận thao tác (Card THÔNG TIN XÁC NHẬN)
5. Bộ giải mã tự động (Auto-parser) cho các thông điệp có định dạng key: value
"""

import os
import sys

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from gui.components.dialog import (
    CyberDialog,
    show_success,
    show_error,
    show_info,
    show_confirm,
    _parse_message_lines
)

def run_tests():
    root = ctk.CTk()
    root.geometry("400x300")
    root.withdraw()  # Ẩn cửa sổ gốc khi test logic

    print("[1] Kiểm tra bộ phân tách tự động _parse_message_lines:")
    raw = (
        "Đã hoàn tất thanh toán cho vé: VX-20261015-123456\n"
        "Phương tiện: Xe máy (29A-123.45)\n"
        "Chủ xe: Nguyễn Văn A\n"
        "Số tiền thu: 5,000 đ (Tiền mặt)"
    )
    intro, pairs = _parse_message_lines(raw)
    print(" - Intro:", intro)
    print(" - Pairs count:", len(pairs))
    assert len(pairs) >= 3
    print(" -> PASS auto-parser")

    print("[2] Khởi tạo CyberDialog - Tiếp nhận thành công:")
    diag_tiep_nhan = CyberDialog(
        root,
        title="Tiếp Nhận Thành Công",
        message="Phương tiện đã được tiếp nhận vào bãi và cấp vé điện tử thành công.",
        card_title="THÔNG TIN TIẾP NHẬN",
        details=[
            ("Mã vé", "VX-20261015-ABC123"),
            ("Phương tiện", "Xe máy"),
            ("Biển số xe", "29A-123.45"),
            ("Chủ xe", "Nguyễn Văn A"),
            ("Thời gian vào", "15/10/2026 01:45"),
            ("Phí gửi xe", "5,000 VNĐ")
        ],
        dialog_type="SUCCESS"
    )
    root.update()
    print(" - Kích thước:", diag_tiep_nhan.geometry())
    diag_tiep_nhan.destroy()
    root.update()
    print(" -> PASS Tiếp nhận thành công")

    print("[3] Khởi tạo CyberDialog - Thanh toán thành công:")
    diag_thanh_toan = CyberDialog(
        root,
        title="Thanh Toán Thành Công",
        message="Đã hoàn tất thanh toán và mở cổng cho phương tiện xuất bãi.",
        card_title="CHI TIẾT GIAO DỊCH",
        details=[
            ("Mã vé", "VX-20261015-ABC123"),
            ("Phương tiện", "Ô tô"),
            ("Biển số xe", "30H-999.88"),
            ("Chủ xe", "Trần Thị B"),
            ("Thời gian vào", "15/10/2026 00:30"),
            ("Thời gian ra", "15/10/2026 01:45"),
            ("Số tiền thu", "20,000 VNĐ"),
            ("Phương thức", "Chuyển khoản")
        ],
        dialog_type="SUCCESS"
    )
    root.update()
    diag_thanh_toan.destroy()
    root.update()
    print(" -> PASS Thanh toán thành công")

    print("[4] Khởi tạo CyberDialog - Cảnh báo lỗi:")
    diag_error = CyberDialog(
        root,
        title="Không Thể Thanh Toán",
        message="Vé xe không ở trạng thái hợp lệ để thực hiện thanh toán.",
        card_title="CHI TIẾT TRẠNG THÁI VÉ",
        details=[
            ("Mã vé", "VX-20261015-OLD"),
            ("Trạng thái hiện tại", "Da thanh toan"),
            ("Lý do từ chối", "Vé đã được thanh toán hoặc đã bị hủy trước đó")
        ],
        dialog_type="ERROR"
    )
    root.update()
    diag_error.destroy()
    root.update()
    print(" -> PASS Cảnh báo lỗi")

    print("[5] Khởi tạo CyberDialog - Xác nhận (Confirm):")
    diag_confirm = CyberDialog(
        root,
        title="Xác Nhận Cho Xe Ra",
        message="Vui lòng kiểm tra kỹ thông tin phương tiện trước khi thanh toán:",
        card_title="THÔNG TIN XÁC NHẬN THANH TOÁN",
        details=[
            ("Mã vé", "VX-20261015-999"),
            ("Phương tiện", "Xe đạp"),
            ("Mã thẻ xe đạp", "XD-012"),
            ("Số tiền phải trả", "2,000 VNĐ")
        ],
        dialog_type="CONFIRM"
    )
    root.update()
    diag_confirm.destroy()
    root.update()
    print(" -> PASS Xác nhận thanh toán")

    root.destroy()
    print("=== TOÀN BỘ KIỂM THỬ CYBERDIALOG PASS 100% ===")

if __name__ == "__main__":
    run_tests()
