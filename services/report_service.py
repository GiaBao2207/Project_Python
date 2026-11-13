"""
NEON PARKING MANAGER - REPORT SERVICE
Tầng nghiệp vụ Xuất Báo cáo dạng TXT (UTF-8 tiếng Việt chuẩn).
Không xuất mật khẩu, hash mật khẩu hoặc dữ liệu bí mật.
Mọi hành động xuất báo cáo đều được ghi nhận vào nhật ký Audit trail.
"""

import os
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any

from database.repositories.vehicle_repository import VehicleRepository
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService


class ReportService:
    """
    Dịch vụ tạo và xuất các mẫu báo cáo chuẩn hóa ra file văn bản TXT.
    """

    @classmethod
    def _tao_tieu_de_chung(cls, ten_bao_cao: str) -> str:
        """Tạo phần đầu tiêu đề đồng bộ cho mọi văn bản báo cáo."""
        user = AuthService.lay_nguoi_dung_hien_tai()
        ten_nv = f"{user.ho_ten} ({user.ten_dang_nhap})" if user else "Hệ thống"
        bay_gio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        lines = [
            "=" * 92,
            "                   HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH - NEON PARKING",
            f"                               {ten_bao_cao.upper()}",
            "=" * 92,
            f"  Thời gian xuất báo cáo : {bay_gio}",
            f"  Nhân viên thực hiện    : {ten_nv}",
            "-" * 92,
            ""
        ]
        return "\n".join(lines)

    @classmethod
    def xuat_bao_cao_xe_dang_gui(cls, file_path: str) -> Tuple[bool, str]:
        """
        Xuất danh sách phương tiện hiện đang gửi trong bãi ra file TXT.
        """
        user = AuthService.lay_nguoi_dung_hien_tai()
        if not user:
            return False, "Yêu cầu đăng nhập trước khi xuất báo cáo!"

        try:
            danh_sach = VehicleRepository.lay_danh_sach_xe_dang_gui()
            
            # Thống kê sơ bộ
            thong_ke_loai = {"XeDap": 0, "XeMay": 0, "OTo": 0}
            tong_tien_tam_tinh = 0
            for xe in danh_sach:
                lx = xe.get("loai_xe", "")
                thong_ke_loai[lx] = thong_ke_loai.get(lx, 0) + 1
                tong_tien_tam_tinh += int(xe.get("don_gia_ap_dung", 0))

            content = cls._tao_tieu_de_chung("BÁO CÁO PHƯƠNG TIỆN HIỆN DIỆN TRONG BÃI")
            content += f"  TỔNG SỐ XE ĐANG GỬI: {len(danh_sach)} phương tiện\n"
            content += f"  - Xe đạp: {thong_ke_loai.get('XeDap', 0)} xe  |  "
            content += f"Xe máy: {thong_ke_loai.get('XeMay', 0)} xe  |  "
            content += f"Ô tô: {thong_ke_loai.get('OTo', 0)} xe\n"
            content += f"  - Doanh thu dự kiến khi xe ra: {tong_tien_tam_tinh:,.0f} VNĐ\n"
            content += "=" * 92 + "\n\n"

            # Header bảng
            content += f"{'STT':<4} | {'MÃ VÉ':<10} | {'LOẠI XE':<10} | {'BIỂN SỐ / ĐỊNH DANH':<20} | {'CHỦ XE':<18} | {'GIỜ VÀO':<16}\n"
            content += "-" * 92 + "\n"

            for i, xe in enumerate(danh_sach, start=1):
                ma_ve = xe.get("ma_ve", "")
                loai_xe = xe.get("ten_loai_xe", xe.get("loai_xe", ""))
                dinh_danh = xe.get("bien_so") or xe.get("ma_dinh_danh", "")
                chu_xe = xe.get("chu_xe", "")
                gio_vao = str(xe.get("gio_vao", ""))[:19]
                content += f"{i:<4} | {ma_ve:<10} | {loai_xe:<10} | {dinh_danh:<20} | {chu_xe:<18} | {gio_vao:<16}\n"

            content += "-" * 92 + "\n"
            content += f"Tổng cộng: {len(danh_sach)} phương tiện.\n"
            content += "\n               --- HẾT BÁO CÁO (NEON PARKING MANAGER) ---\n"

            # Ghi file chuẩn UTF-8
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            # Ghi nhật ký Audit trail
            UserRepository.ghi_nhat_ky(
                user.id,
                "XUAT_BAO_CAO",
                f"Xuất báo cáo xe đang gửi ra file: {os.path.basename(file_path)} ({len(danh_sach)} xe)"
            )
            return True, f"Xuất báo cáo xe đang gửi thành công ({len(danh_sach)} bản ghi)!"
        except Exception as e:
            return False, f"Lỗi khi xuất file báo cáo: {e}"

    @classmethod
    def xuat_bao_cao_lich_su_ve(
        cls,
        file_path: str,
        trang_thai: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Xuất lịch sử vé xe ra file TXT.
        """
        user = AuthService.lay_nguoi_dung_hien_tai()
        if not user:
            return False, "Yêu cầu đăng nhập trước khi xuất báo cáo!"

        try:
            danh_sach = VehicleRepository.lay_danh_sach_ve(trang_thai=trang_thai)

            content = cls._tao_tieu_de_chung("BÁO CÁO LỊCH SỬ VÉ XE")
            content += f"  Trạng thái lọc: {trang_thai or 'Tất cả'}\n"
            content += f"  Tổng số vé tìm thấy: {len(danh_sach)} vé\n"
            content += "=" * 105 + "\n\n"

            content += f"{'STT':<4} | {'MÃ VÉ':<10} | {'LOẠI XE':<9} | {'BIỂN SỐ':<15} | {'CHỦ XE':<16} | {'GIỜ VÀO':<16} | {'GIỜ RA':<16} | {'TRẠNG THÁI':<14}\n"
            content += "-" * 105 + "\n"

            for i, ve in enumerate(danh_sach, start=1):
                ma_ve = ve.get("ma_ve", "")
                loai_xe = ve.get("ten_loai_xe", ve.get("loai_xe", ""))
                bien_so = ve.get("bien_so") or ve.get("ma_dinh_danh", "")
                chu_xe = ve.get("chu_xe", "")
                gio_vao = str(ve.get("gio_vao", ""))[:19]
                gio_ra = str(ve.get("gio_ra", "") or "Chưa ra")[:19]
                tt = ve.get("trang_thai", "")
                content += f"{i:<4} | {ma_ve:<10} | {loai_xe:<9} | {bien_so:<15} | {chu_xe:<16} | {gio_vao:<16} | {gio_ra:<16} | {tt:<14}\n"

            content += "-" * 105 + "\n"
            content += f"Tổng cộng: {len(danh_sach)} vé xe.\n"
            content += "\n               --- HẾT BÁO CÁO (NEON PARKING MANAGER) ---\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            UserRepository.ghi_nhat_ky(
                user.id,
                "XUAT_BAO_CAO",
                f"Xuất báo cáo lịch sử vé ra file: {os.path.basename(file_path)} ({len(danh_sach)} vé)"
            )
            return True, f"Xuất báo cáo lịch sử vé thành công ({len(danh_sach)} bản ghi)!"
        except Exception as e:
            return False, f"Lỗi khi xuất file báo cáo vé: {e}"

    @classmethod
    def xuat_bao_cao_doanh_thu(
        cls,
        file_path: str,
        tu_ngay: Optional[str] = None,
        den_ngay: Optional[str] = None,
        nam: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Xuất báo cáo tổng hợp doanh thu hoạt động ra file TXT (Chỉ ADMIN).
        Báo cáo bao gồm:
        - Tổng doanh thu thực thu, tiền mặt, chuyển khoản, số giao dịch.
        - Doanh thu chi tiết theo ngày.
        - Doanh thu chi tiết theo tháng trong năm.
        - Tổng hợp tiền đã thu, không cộng vé chưa thanh toán.
        """
        AuthService.kiem_tra_quyen_admin()
        user = AuthService.lay_nguoi_dung_hien_tai()

        try:
            nam_thuc_te = nam or datetime.now().year
            tong_hop = VehicleRepository.lay_tong_doanh_thu(tu_ngay=tu_ngay, den_ngay=den_ngay)
            danh_sach_ngay = VehicleRepository.lay_doanh_thu_theo_ngay(so_ngay=30, tu_ngay=tu_ngay, den_ngay=den_ngay)
            danh_sach_thang = VehicleRepository.lay_doanh_thu_theo_thang(nam=nam_thuc_te)

            tong_doanh_thu = tong_hop["tong_doanh_thu"]
            tien_mat = tong_hop["tien_mat"]
            chuyen_khoan = tong_hop["chuyen_khoan"]
            so_giao_dich = tong_hop["so_giao_dich"]

            pt_tm = (tien_mat / tong_doanh_thu * 100) if tong_doanh_thu > 0 else 0.0
            pt_ck = (chuyen_khoan / tong_doanh_thu * 100) if tong_doanh_thu > 0 else 0.0
            tb_luot = (tong_doanh_thu / so_giao_dich) if so_giao_dich > 0 else 0.0

            content = cls._tao_tieu_de_chung("BÁO CÁO TỔNG HỢP DOANH THU HOẠT ĐỘNG")
            content += f"  Khoảng thời gian thống kê : {tu_ngay or 'Toàn bộ lịch sử'} -> {den_ngay or 'Hiện tại'}\n"
            content += f"  Năm thống kê theo tháng   : {nam_thuc_te}\n"
            content += "=" * 105 + "\n\n"

            # ── Mục I: Tổng hợp ──
            content += "I. TỔNG HỢP DOANH THU & DÒNG TIỀN\n"
            content += "-" * 105 + "\n"
            content += f"  * TỔNG DOANH THU THỰC THU : {tong_doanh_thu:,.0f} VNĐ\n"
            content += f"    - Tiền mặt              : {tien_mat:,.0f} VNĐ ({pt_tm:.1f}%)\n"
            content += f"    - Chuyển khoản ngân hàng: {chuyen_khoan:,.0f} VNĐ ({pt_ck:.1f}%)\n"
            content += f"  * Tổng số lượt giao dịch  : {so_giao_dich} giao dịch đã hoàn tất\n"
            content += f"  * Doanh thu bình quân/lượt: {tb_luot:,.0f} VNĐ/giao dịch\n"
            content += "  (Ghi chú: Số liệu tổng hợp từ các giao dịch thanh toán thực thu (bảng thanh_toan), không tính các vé chưa xuất bãi hoặc chưa thanh toán)\n\n"

            # ── Mục II: Doanh thu theo ngày ──
            content += "II. DOANH THU CHI TIẾT THEO NGÀY\n"
            content += "-" * 105 + "\n"
            content += f"{'STT':<4} | {'NGÀY':<12} | {'TIỀN MẶT (VNĐ)':<18} | {'CHUYỂN KHOẢN (VNĐ)':<20} | {'TỔNG CỘNG (VNĐ)':<18} | {'SỐ GD':<8}\n"
            content += "-" * 105 + "\n"

            if not danh_sach_ngay:
                content += "  (Không có dữ liệu giao dịch phát sinh theo ngày trong khoảng thời gian này)\n"
            else:
                for i, row in enumerate(danh_sach_ngay, start=1):
                    ngay_str = str(row.get("ngay", ""))
                    tm_str = f"{row.get('tien_mat', 0):,}"
                    ck_str = f"{row.get('chuyen_khoan', 0):,}"
                    tong_str = f"{row.get('tong_doanh_thu', 0):,}"
                    sgd = row.get("so_giao_dich", 0)
                    content += f"{i:<4} | {ngay_str:<12} | {tm_str:<18} | {ck_str:<20} | {tong_str:<18} | {sgd:<8}\n"

            content += "-" * 105 + "\n\n"

            # ── Mục III: Doanh thu theo tháng ──
            content += f"III. DOANH THU THEO TỪNG THÁNG (NĂM {nam_thuc_te})\n"
            content += "-" * 105 + "\n"
            content += f"{'THÁNG':<10} | {'TIỀN MẶT (VNĐ)':<18} | {'CHUYỂN KHOẢN (VNĐ)':<20} | {'TỔNG CỘNG (VNĐ)':<18} | {'SỐ GD':<8}\n"
            content += "-" * 105 + "\n"

            if not danh_sach_thang:
                content += f"  (Không có dữ liệu giao dịch phát sinh trong năm {nam_thuc_te})\n"
            else:
                for row in danh_sach_thang:
                    thang_str = f"Tháng {row.get('thang', 0):02d}"
                    tm_str = f"{row.get('tien_mat', 0):,}"
                    ck_str = f"{row.get('chuyen_khoan', 0):,}"
                    tong_str = f"{row.get('tong_doanh_thu', 0):,}"
                    sgd = row.get("so_giao_dich", 0)
                    content += f"{thang_str:<10} | {tm_str:<18} | {ck_str:<20} | {tong_str:<18} | {sgd:<8}\n"

            content += "-" * 105 + "\n\n"
            content += f"Tổng kết: {so_giao_dich} giao dịch thực thu. Tổng doanh thu: {tong_doanh_thu:,.0f} VNĐ.\n"
            content += "\n               --- HẾT BÁO CÁO (NEON PARKING MANAGER) ---\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            UserRepository.ghi_nhat_ky(
                user.id,
                "XUAT_BAO_CAO",
                f"Xuất báo cáo doanh thu ra file: {os.path.basename(file_path)} (Tổng: {tong_doanh_thu:,.0f} VNĐ)"
            )
            return True, f"Xuất báo cáo doanh thu thành công ({so_giao_dich} giao dịch, tổng {tong_doanh_thu:,.0f} VNĐ)!"
        except Exception as e:
            return False, f"Lỗi khi xuất file báo cáo doanh thu: {e}"

    @classmethod
    def xuat_bao_cao_lich_su_giao_dich(
        cls,
        file_path: str,
        tu_ngay: Optional[str] = None,
        den_ngay: Optional[str] = None,
        phuong_thuc: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Xuất danh sách lịch sử giao dịch thanh toán chi tiết ra file TXT (Chỉ ADMIN).
        Hỗ trợ lọc theo khoảng ngày và phương thức thanh toán (TIEN_MAT / CHUYEN_KHOAN / Tất cả).
        """
        AuthService.kiem_tra_quyen_admin()
        user = AuthService.lay_nguoi_dung_hien_tai()

        try:
            pt_filter = phuong_thuc if phuong_thuc not in ("TAT_CA", "Tất cả", None) else None
            giao_dich = VehicleRepository.lay_lich_su_thanh_toan(
                tu_ngay=tu_ngay,
                den_ngay=den_ngay,
                phuong_thuc=pt_filter,
                limit=None
            )

            tong_so_gd = len(giao_dich)
            tong_tien = sum(int(gd.get("so_tien", 0)) for gd in giao_dich)
            tien_mat = sum(int(gd.get("so_tien", 0)) for gd in giao_dich if gd.get("phuong_thuc") == "TIEN_MAT")
            chuyen_khoan = sum(int(gd.get("so_tien", 0)) for gd in giao_dich if gd.get("phuong_thuc") == "CHUYEN_KHOAN")

            pt_hien_thi = "Tất cả"
            if pt_filter == "TIEN_MAT":
                pt_hien_thi = "Tiền mặt"
            elif pt_filter == "CHUYEN_KHOAN":
                pt_hien_thi = "Chuyển khoản"

            content = cls._tao_tieu_de_chung("BÁO CÁO LỊCH SỬ GIAO DỊCH THANH TOÁN")
            content += f"  Khoảng thời gian: {tu_ngay or 'Toàn bộ lịch sử'} -> {den_ngay or 'Hiện tại'}\n"
            content += f"  Hình thức lọc   : {pt_hien_thi}\n"
            content += f"  Tổng số hóa đơn : {tong_so_gd} giao dịch  |  Tổng tiền thực thu: {tong_tien:,.0f} VNĐ\n"
            content += f"  - Tiền mặt      : {tien_mat:,.0f} VNĐ  |  Chuyển khoản: {chuyen_khoan:,.0f} VNĐ\n"
            content += "=" * 125 + "\n\n"

            content += f"{'STT':<4} | {'MÃ VÉ':<10} | {'LOẠI XE':<9} | {'BIỂN SỐ / ĐỊNH DANH':<20} | {'CHỦ XE':<16} | {'SỐ TIỀN (VNĐ)':<14} | {'HÌNH THỨC':<13} | {'THỜI GIAN THU':<19} | {'THU NGÂN':<15}\n"
            content += "-" * 125 + "\n"

            if not giao_dich:
                content += "  (Không có giao dịch thanh toán nào phù hợp với điều kiện lọc)\n"
            else:
                for i, gd in enumerate(giao_dich, start=1):
                    ma_ve = str(gd.get("ma_ve") or "")
                    loai_xe = str(gd.get("ten_loai_xe") or gd.get("loai_xe") or "")
                    bien_so = str(gd.get("bien_so") or gd.get("ma_dinh_danh") or "")
                    chu_xe = str(gd.get("chu_xe") or "—")
                    so_tien = f"{int(gd.get('so_tien', 0)):,}"
                    pt = "Tiền mặt" if gd.get("phuong_thuc") == "TIEN_MAT" else "Chuyển khoản"
                    tg = str(gd.get("thoi_gian_thanh_toan", ""))[:19]
                    nv = str(gd.get("ten_nhan_vien") or "N/A")
                    content += f"{i:<4} | {ma_ve:<10} | {loai_xe:<9} | {bien_so:<20} | {chu_xe:<16} | {so_tien:<14} | {pt:<13} | {tg:<19} | {nv:<15}\n"

            content += "-" * 125 + "\n"
            content += f"Tổng cộng: {tong_so_gd} giao dịch thanh toán. Tổng tiền: {tong_tien:,.0f} VNĐ.\n"
            content += "\n               --- HẾT BÁO CÁO (NEON PARKING MANAGER) ---\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            UserRepository.ghi_nhat_ky(
                user.id,
                "XUAT_BAO_CAO",
                f"Xuất báo cáo lịch sử giao dịch ra file: {os.path.basename(file_path)} ({tong_so_gd} giao dịch, Tổng: {tong_tien:,.0f} VNĐ)"
            )
            return True, f"Xuất báo cáo lịch sử giao dịch thành công ({tong_so_gd} giao dịch)!"
        except Exception as e:
            return False, f"Lỗi khi xuất file báo cáo lịch sử giao dịch: {e}"

    # Alias tương thích
    xuat_bao_cao_lich_su_thanh_toan = xuat_bao_cao_lich_su_giao_dich
