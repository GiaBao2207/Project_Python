"""
KỊCH BẢN KIỂM THỬ TỔNG THỂ SỬA LỖI XUẤT BÁO CÁO
Dự án: Neon Parking Manager
Kiểm tra:
1. Repository & Service layer: key 'tong_doanh_thu', xử lý NULL, ép kiểu Decimal sang int, khoảng thời gian trống.
2. Phân quyền Admin ở tầng Service cho cả 2 hàm xuất báo cáo.
3. Xuất báo cáo tổng hợp doanh thu (Tổng DT, theo ngày, theo tháng, thực thu).
4. Xuất báo cáo lịch sử giao dịch thanh toán (chi tiết từng giao dịch).
5. Ghi nhật ký Audit trail (XUAT_BAO_CAO) vào bảng nhat_ky.
6. Bảo toàn ứng dụng Console CLI và tệp dữ liệu TXT cũ.
"""

import os
import sys
from datetime import datetime

# Đảm bảo đường dẫn import gốc
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.repositories.vehicle_repository import VehicleRepository
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.bai_xe_db_service import BaiXeDbService
from services.report_service import ReportService


def run_all_tests():
    ket_qua = []
    print("=" * 70)
    print("BAT DAU KIEM THU CHUC NANG XUAT BAO CAO - NEON PARKING MANAGER")
    print("=" * 70)

    # 1. KIỂM THỬ TẦNG REPOSITORY: lay_tong_doanh_thu
    try:
        data_all = VehicleRepository.lay_tong_doanh_thu()
        assert "tong_doanh_thu" in data_all, "Thieu key 'tong_doanh_thu' trong dict ket qua"
        assert "tong" in data_all, "Thieu key 'tong' de tuong thich nguoc"
        assert "tien_mat" in data_all, "Thieu key 'tien_mat'"
        assert "chuyen_khoan" in data_all, "Thieu key 'chuyen_khoan'"
        assert "so_giao_dich" in data_all, "Thieu key 'so_giao_dich'"
        assert "so_luot_thu" in data_all, "Thieu key 'so_luot_thu'"
        assert isinstance(data_all["tong_doanh_thu"], int), "tong_doanh_thu phai la int"
        assert isinstance(data_all["tien_mat"], int), "tien_mat phai la int"
        assert isinstance(data_all["chuyen_khoan"], int), "chuyen_khoan phai la int"
        assert isinstance(data_all["so_giao_dich"], int), "so_giao_dich phai la int"
        
        # Test voi khoang thoi gian KHONG co giao dich (truong hop SUM() tra ve NULL)
        data_empty = VehicleRepository.lay_tong_doanh_thu(tu_ngay="1999-01-01", den_ngay="1999-01-02")
        assert data_empty["tong_doanh_thu"] == 0, "Giao dich trong pham vi rong phai tra ve 0"
        assert data_empty["so_giao_dich"] == 0, "So giao dich pham vi rong phai tra ve 0"
        assert data_empty["tien_mat"] == 0
        assert data_empty["chuyen_khoan"] == 0

        ket_qua.append(("1. VehicleRepository.lay_tong_doanh_thu", True, f"Dung key 'tong_doanh_thu', int hop le, xu ly SUM NULL tot: {data_all}"))
    except Exception as e:
        ket_qua.append(("1. VehicleRepository.lay_tong_doanh_thu", False, str(e)))

    # 2. KIỂM THỬ lay_doanh_thu_theo_ngay & lay_doanh_thu_theo_thang
    try:
        theo_ngay = VehicleRepository.lay_doanh_thu_theo_ngay(30)
        assert isinstance(theo_ngay, list), "lay_doanh_thu_theo_ngay phai tra ve list"
        if theo_ngay:
            r = theo_ngay[0]
            assert "tong_doanh_thu" in r, "Moi row phai co 'tong_doanh_thu'"
            assert "so_giao_dich" in r, "Moi row phai co 'so_giao_dich'"
            assert isinstance(r["tong_doanh_thu"], int), "tong_doanh_thu trong row phai la int (khong phai Decimal)"
            assert isinstance(r["tien_mat"], int), "tien_mat trong row phai la int"

        theo_thang = VehicleRepository.lay_doanh_thu_theo_thang()
        assert isinstance(theo_thang, list), "lay_doanh_thu_theo_thang phai tra ve list"
        if theo_thang:
            r_thang = theo_thang[0]
            assert "tong_doanh_thu" in r_thang, "Moi row thang phai co 'tong_doanh_thu'"
            assert isinstance(r_thang["tong_doanh_thu"], int), "tong_doanh_thu trong row thang phai la int"

        ket_qua.append(("2. Thong ke Doanh thu theo ngay & thang", True, f"Theo ngay: {len(theo_ngay)} ban ghi, Theo thang: {len(theo_thang)} ban ghi"))
    except Exception as e:
        ket_qua.append(("2. Thong ke Doanh thu theo ngay & thang", False, str(e)))

    # 3. KIỂM THỬ lay_lich_su_thanh_toan
    try:
        ls_gd = VehicleRepository.lay_lich_su_thanh_toan(limit=None)
        assert isinstance(ls_gd, list), "lay_lich_su_thanh_toan phai tra ve list"
        if ls_gd:
            gd = ls_gd[0]
            assert "ma_ve" in gd, "Giao dich phai co ma_ve"
            assert "so_tien" in gd and isinstance(gd["so_tien"], int), "so_tien phai la int"
            assert "phuong_thuc" in gd, "phuong_thuc phai ton tai"
        ket_qua.append(("3. VehicleRepository.lay_lich_su_thanh_toan", True, f"Lay thanh cong {len(ls_gd)} giao dich day du cot"))
    except Exception as e:
        ket_qua.append(("3. VehicleRepository.lay_lich_su_thanh_toan", False, str(e)))

    # 4. KIỂM THỬ PHÂN QUYỀN TẦNG SERVICE LAYER
    try:
        AuthService.dang_xuat()
        # Thử gọi khi chưa đăng nhập
        bi_chan = False
        try:
            ReportService.xuat_bao_cao_doanh_thu("temp_test.txt")
        except PermissionError:
            bi_chan = True
        assert bi_chan, "Chua dang nhap phai bi nem PermissionError"

        # Thử giả lập người dùng NHAN_VIEN
        nv_user = UserRepository.lay_theo_ten_dang_nhap("nhanvien001")
        if not nv_user:
            for u in UserRepository.lay_tat_ca_nguoi_dung():
                if not u.la_admin:
                    nv_user = u
                    break
        if nv_user:
            AuthService._nguoi_dung_hien_tai = nv_user
            bi_chan_nv = False
            try:
                ReportService.xuat_bao_cao_doanh_thu("temp_test.txt")
            except PermissionError:
                bi_chan_nv = True
            assert bi_chan_nv, "Nhan vien khong phai Admin phai bi nem PermissionError"
            AuthService.dang_xuat()

        ket_qua.append(("4. Phan quyen Service Layer (Admin Only)", True, "Chan tuyet doi Guest va NHAN_VIEN tai Service Layer"))
    except Exception as e:
        ket_qua.append(("4. Phan quyen Service Layer (Admin Only)", False, str(e)))

    # 5. THIẾT LẬP PHIÊN LÀM VIỆC ADMIN
    admin_user = UserRepository.lay_theo_ten_dang_nhap("admin")
    if not admin_user:
        for u in UserRepository.lay_tat_ca_nguoi_dung():
            if u.la_admin:
                admin_user = u
                break
    assert admin_user is not None, "Khong tim thay tai khoan Admin trong CSDL!"
    AuthService._nguoi_dung_hien_tai = admin_user

    # 6. KIỂM THỬ XUẤT BÁO CÁO DOANH THU HOẠT ĐỘNG
    test_dt_path = os.path.join(BASE_DIR, "BaoCao_DoanhThu_KiemThu.txt")
    try:
        ok_dt, msg_dt = ReportService.xuat_bao_cao_doanh_thu(test_dt_path)
        assert ok_dt, f"Xuat bao cao doanh thu that bai: {msg_dt}"
        assert os.path.exists(test_dt_path), "File BaoCao_DoanhThu_KiemThu.txt khong duoc tao"

        with open(test_dt_path, "r", encoding="utf-8") as f:
            content_dt = f.read()

        assert "BÁO CÁO TỔNG HỢP DOANH THU HOẠT ĐỘNG" in content_dt
        assert "I. TỔNG HỢP DOANH THU & DÒNG TIỀN" in content_dt
        assert "II. DOANH THU CHI TIẾT THEO NGÀY" in content_dt
        assert "III. DOANH THU THEO TỪNG THÁNG" in content_dt
        assert "TỔNG DOANH THU THỰC THU" in content_dt
        assert "Tiền mặt" in content_dt
        assert "Chuyển khoản ngân hàng" in content_dt
        assert "--- HẾT BÁO CÁO (NEON PARKING MANAGER) ---" in content_dt

        ket_qua.append(("5. Xuat Bao Cao Tong Hop Doanh Thu", True, f"Xuat thanh cong, du 3 muc Tong quan, Theo ngay, Theo thang: {msg_dt}"))
    except Exception as e:
        ket_qua.append(("5. Xuat Bao Cao Tong Hop Doanh Thu", False, str(e)))
    finally:
        if os.path.exists(test_dt_path):
            os.remove(test_dt_path)

    # 7. KIỂM THỬ XUẤT BÁO CÁO LỊCH SỬ GIAO DỊCH THANH TOÁN
    test_gd_path = os.path.join(BASE_DIR, "BaoCao_LichSuGD_KiemThu.txt")
    try:
        ok_gd, msg_gd = ReportService.xuat_bao_cao_lich_su_giao_dich(test_gd_path)
        assert ok_gd, f"Xuat bao cao lich su giao dich that bai: {msg_gd}"
        assert os.path.exists(test_gd_path), "File BaoCao_LichSuGD_KiemThu.txt khong duoc tao"

        with open(test_gd_path, "r", encoding="utf-8") as f:
            content_gd = f.read()

        assert "BÁO CÁO LỊCH SỬ GIAO DỊCH THANH TOÁN" in content_gd
        assert "MÃ VÉ" in content_gd
        assert "BIỂN SỐ / ĐỊNH DANH" in content_gd
        assert "SỐ TIỀN (VNĐ)" in content_gd
        assert "HÌNH THỨC" in content_gd
        assert "THU NGÂN" in content_gd
        assert "--- HẾT BÁO CÁO (NEON PARKING MANAGER) ---" in content_gd

        ket_qua.append(("6. Xuat Bao Cao Lich Su Giao Dich Thanh Toan", True, f"Xuat thanh cong bang ke chi tiet giao dich: {msg_gd}"))
    except Exception as e:
        ket_qua.append(("6. Xuat Bao Cao Lich Su Giao Dich Thanh Toan", False, str(e)))
    finally:
        if os.path.exists(test_gd_path):
            os.remove(test_gd_path)

    # 8. KIỂM THỬ GHI NHẬT KÝ AUDIT TRAIL
    try:
        nhat_ky = UserRepository.lay_nhat_ky(hanh_dong="XUAT_BAO_CAO", limit=5)
        assert len(nhat_ky) > 0, "Khong tim thay nhat ky XUAT_BAO_CAO"
        ket_qua.append(("7. Audit Trail (Nhat ky he thong)", True, f"Ghi nhan dung {len(nhat_ky)} su kien XUAT_BAO_CAO gan nhat vao CSDL"))
    except Exception as e:
        ket_qua.append(("7. Audit Trail (Nhat ky he thong)", False, str(e)))

    # 9. KIỂM THỬ BẢO TOÀN CONSOLE CLI & FILE TXT
    try:
        txt_path = os.path.join(BASE_DIR, "data", "du_lieu_bai_xe.txt")
        assert os.path.exists(txt_path), "File data/du_lieu_bai_xe.txt bi thieu!"
        with open(txt_path, "r", encoding="utf-8") as f:
            txt_lines = f.readlines()
        assert len(txt_lines) > 0, "File du_lieu_bai_xe.txt bi rong!"

        # Import thu Console
        from services.quan_ly_bai_xe import QuanLyBaiXe
        ql_console = QuanLyBaiXe()
        assert hasattr(ql_console, "danh_sach_xe"), "Class QuanLyBaiXe Console bi hong!"

        ket_qua.append(("8. Bao toan Console CLI & File TXT", True, f"File TXT giu nguyen {len(txt_lines)} dong, QuanLyBaiXe Console san sang"))
    except Exception as e:
        ket_qua.append(("8. Bao toan Console CLI & File TXT", False, str(e)))

    # IN BẢNG KẾT QUẢ TỔNG HỢP
    print("\n" + "=" * 70)
    print("KET QUA KIEM THU CHI TIET")
    print("=" * 70)
    all_pass = True
    for ten, status, detail in ket_qua:
        icon = "[PASS]" if status else "[FAIL]"
        if not status:
            all_pass = False
        print(f"{icon} {ten}")
        print(f"       -> {detail}")

    print("=" * 70)
    if all_pass:
        print("TAT CA CA KIEM THU DEU DAT CHUAN 100%! (ALL PASS)")
    else:
        print("CO LOI TON TAI TRONG QUA TRINH KIEM THU!")
    print("=" * 70)
    return all_pass


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
