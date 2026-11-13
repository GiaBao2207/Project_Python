"""
NEON PARKING MANAGER - BÃI XE DB SERVICE
Tầng Nghiệp vụ: Xử lý toàn bộ logic kinh doanh bãi xe với MySQL.
Tách biệt hoàn toàn khỏi tầng Giao diện (GUI).

Nguyên tắc phân tầng:
- GUI chỉ gọi các method của BaiXeDbService.
- BaiXeDbService kiểm tra nghiệp vụ, phân quyền, gọi VehicleRepository.
- VehicleRepository chỉ biết SQL, không biết nghiệp vụ.
"""

import uuid
import datetime
from typing import Optional, Tuple, List, Dict, Any

from database.repositories.vehicle_repository import VehicleRepository
from database.repositories.user_repository import UserRepository
from services.auth_service import AuthService


class BaiXeDbService:
    """
    Service xử lý nghiệp vụ bãi xe kết hợp MySQL:
    - Tiếp nhận xe (check-in): Kiểm tra biển số, sức chứa, chống vé trùng.
    - Cho xe ra (check-out): Tính tiền, thanh toán Transaction MySQL.
    - Truy vấn danh sách xe đang gửi.

    Mọi thao tác ghi đều dùng MySQL Transaction để đảm bảo tính toàn vẹn.
    """

    # ─────────────────────────── TIẾP NHẬN XE (CHECK-IN) ───────────────────────────

    @staticmethod
    def tiep_nhan_xe(
        loai_xe: str,
        ma_dinh_danh: str,
        bien_so: Optional[str],
        chu_xe: str
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Tiếp nhận một phương tiện vào bãi giữ xe.

        Quy trình:
        1. Kiểm tra quyền người dùng (phải đang đăng nhập).
        2. Xác thực dữ liệu đầu vào (loại xe hợp lệ, biển số bắt buộc với XeMay/OTo).
        3. Kiểm tra sức chứa còn trống.
        4. Tìm xe trong CSDL:
           - Nếu đã có: kiểm tra xe có đang được gửi không (chống vé trùng).
           - Nếu chưa có: tạo xe mới.
        5. Tạo mã vé duy nhất, lưu vé vào MySQL.

        Args:
            loai_xe: 'XeDap', 'XeMay', hoặc 'OTo'
            ma_dinh_danh: Biển số (XeMay/OTo) hoặc mã thẻ (XeDap), upper-case
            bien_so: Biển số xe (None với XeDap được phép)
            chu_xe: Tên chủ xe / người gửi

        Returns:
            Tuple(thanh_cong: bool, thong_bao: str, ma_ve: Optional[str])
        """
        # BƯỚC 1: Xác thực người dùng đang đăng nhập
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn. Vui lòng đăng nhập lại.", None

        # BƯỚC 2: Xác thực dữ liệu đầu vào
        loai_xe_hop_le = ["XeDap", "XeMay", "OTo"]
        if loai_xe not in loai_xe_hop_le:
            return False, f"Loại xe không hợp lệ. Chỉ chấp nhận: {', '.join(loai_xe_hop_le)}", None

        ma_dinh_danh = ma_dinh_danh.strip().upper()
        if not ma_dinh_danh:
            return False, "Mã định danh xe không được để trống.", None

        chu_xe = chu_xe.strip()
        if not chu_xe:
            return False, "Tên chủ xe không được để trống.", None

        # Kiểm tra biển số bắt buộc với XeMay và OTo (Service Layer Validation)
        # - Thay thế cho CHECK constraint MySQL bị lỗi 3823 (AGENTS.md - Quyết định kỹ thuật #3)
        if loai_xe in ("XeMay", "OTo"):
            if not bien_so or not bien_so.strip():
                return False, (
                    f"Xe {loai_xe} bắt buộc phải có biển số đăng ký. "
                    "XeDap mới được phép không có biển số."
                ), None
            bien_so = bien_so.strip().upper()
        else:
            # XeDap: biển số là tùy chọn
            bien_so = bien_so.strip().upper() if bien_so and bien_so.strip() else None

        # BƯỚC 3: Kiểm tra sức chứa còn trống (concurrency-safe)
        try:
            suc_chua = VehicleRepository.lay_suc_chua()
            tong_cho = suc_chua.get(loai_xe, 0)
            dang_gui = VehicleRepository.dem_xe_dang_gui(loai_xe)
            if dang_gui >= tong_cho:
                return False, (
                    f"Bãi xe đã hết chỗ cho {loai_xe}! "
                    f"Sức chứa: {tong_cho}, Đang gửi: {dang_gui}."
                ), None
        except Exception as e:
            return False, f"Lỗi kiểm tra sức chứa: {e}", None

        # BƯỚC 4: Tìm hoặc tạo xe trong CSDL
        try:
            xe = VehicleRepository.tim_xe_theo_ma_dinh_danh(ma_dinh_danh)
            if xe:
                id_xe = xe["id"]
                # Kiểm tra xe này có đang được gửi không
                if VehicleRepository.kiem_tra_xe_dang_gui(id_xe):
                    return False, (
                        f"Phương tiện '{ma_dinh_danh}' hiện đang được gửi trong bãi. "
                        "Vui lòng làm thủ tục trả xe trước."
                    ), None
            else:
                # Xe chưa từng đăng ký -> tạo mới
                id_xe = VehicleRepository.them_xe(ma_dinh_danh, bien_so, loai_xe, chu_xe)
        except Exception as e:
            return False, f"Lỗi tra cứu / đăng ký xe: {e}", None

        # BƯỚC 5: Lấy đơn giá hiện hành và tạo vé
        try:
            bang_gia_list = VehicleRepository.lay_bang_gia()
            gia_dict = {row["loai_xe"]: row["gia_ve"] for row in bang_gia_list}
            don_gia = gia_dict.get(loai_xe, 0)

            # Sinh mã vé duy nhất: VX-YYYYMMDD-XXXX (dạng ngắn gọn)
            ngay_hom_nay = datetime.datetime.now().strftime("%Y%m%d")
            ma_ve = f"VX-{ngay_hom_nay}-{uuid.uuid4().hex[:6].upper()}"

            VehicleRepository.tao_ve_tiep_nhan(
                ma_ve=ma_ve,
                id_xe=id_xe,
                don_gia_ap_dung=don_gia,
                id_nhan_vien=nguoi_dung.id
            )

            # Ghi nhật ký hoạt động
            UserRepository.ghi_nhat_ky(
                id_nguoi_dung=nguoi_dung.id,
                hanh_dong="TIEP_NHAN_XE",
                chi_tiet=f"Tiếp nhận {loai_xe} '{ma_dinh_danh}' - Vé: {ma_ve}"
            )

            return True, f"Tiếp nhận thành công! Mã vé: {ma_ve}", ma_ve

        except Exception as e:
            return False, f"Lỗi tạo vé xe: {e}", None

    # ─────────────────────────── CHO XE RA + THANH TOÁN (CHECK-OUT) ───────────────────────────

    @staticmethod
    def cho_xe_ra_va_tinh_tien(
        ma_ve: str,
        phuong_thuc: str = "TIEN_MAT",
        ghi_chu: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Thực hiện cho xe ra và tính tiền thanh toán.

        Logic tính tiền:
        - Số tiền = don_gia_ap_dung lưu trong vé (snapshot giá tại thời điểm nhận xe).
        - Dự án này dùng giá cố định theo lượt (không tính theo giờ gửi).

        Dùng MySQL Transaction: cập nhật ve_xe + INSERT thanh_toan trong 1 transaction.

        Returns:
            Tuple(thanh_cong, thong_bao, chi_tiet_thanh_toan)
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", None

        if not ma_ve or not ma_ve.strip():
            return False, "Mã vé không được để trống.", None

        ma_ve = ma_ve.strip().upper()
        phuong_thuc_hop_le = ["TIEN_MAT", "CHUYEN_KHOAN"]
        if phuong_thuc not in phuong_thuc_hop_le:
            return False, f"Phương thức thanh toán không hợp lệ: {phuong_thuc}", None

        try:
            # Lấy thông tin vé đang gửi
            ve = VehicleRepository.lay_ve_theo_ma(ma_ve)
            if not ve:
                return False, f"Không tìm thấy vé '{ma_ve}'.", None
            if ve["trang_thai"] != "Dang gui":
                return False, (
                    f"Vé '{ma_ve}' đã được thanh toán hoặc đã hủy. "
                    f"Trạng thái hiện tại: {ve['trang_thai']}."
                ), None

            so_tien = ve["don_gia_ap_dung"]

            # Thực hiện transaction: đóng vé + tạo thanh toán
            VehicleRepository.thuc_hien_cho_xe_ra_va_thanh_toan(
                ma_ve=ma_ve,
                so_tien=so_tien,
                phuong_thuc=phuong_thuc,
                id_nhan_vien_ra=nguoi_dung.id,
                ghi_chu=ghi_chu
            )

            # Ghi nhật ký
            UserRepository.ghi_nhat_ky(
                id_nguoi_dung=nguoi_dung.id,
                hanh_dong="XE_RA",
                chi_tiet=(
                    f"Xe ra: {ve['loai_xe']} '{ve['ma_dinh_danh']}' - "
                    f"Vé: {ma_ve} - Tiền: {so_tien:,}đ"
                )
            )

            chi_tiet = {
                "ma_ve": ma_ve,
                "ma_dinh_danh": ve["ma_dinh_danh"],
                "loai_xe": ve["ten_loai_xe"],
                "chu_xe": ve["chu_xe"],
                "gio_vao": ve["gio_vao"],
                "so_tien": so_tien,
                "phuong_thuc": phuong_thuc
            }
            return True, (
                f"Thanh toán thành công! Số tiền: {so_tien:,}đ"
            ), chi_tiet

        except Exception as e:
            return False, f"Lỗi xử lý cho xe ra: {e}", None

    # ─────────────────────────── TRUY VẤN ───────────────────────────

    @staticmethod
    def lay_danh_sach_xe_dang_gui(
        tu_khoa: Optional[str] = None,
        loai_xe: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Lấy danh sách tất cả xe đang gửi trong bãi (trạng thái 'Dang gui').
        Hỗ trợ tìm kiếm theo mã vé, biển số, mã định danh xe đạp, tên chủ xe.
        Hỗ trợ lọc theo loại xe và phân trang (limit, offset).
        """
        try:
            danh_sach = VehicleRepository.lay_danh_sach_xe_dang_gui(
                tu_khoa=tu_khoa,
                loai_xe=loai_xe,
                limit=limit,
                offset=offset
            )
            return True, "Tải dữ liệu thành công.", danh_sach
        except Exception as e:
            return False, f"Lỗi truy vấn CSDL: {e}", []

    @staticmethod
    def dem_so_luong_xe_dang_gui(
        tu_khoa: Optional[str] = None,
        loai_xe: Optional[str] = None
    ) -> int:
        """Đếm tổng số xe đang gửi thỏa mãn từ khóa tìm kiếm và loại xe (không phân trang)."""
        try:
            return VehicleRepository.dem_so_luong_xe_dang_gui(tu_khoa=tu_khoa, loai_xe=loai_xe)
        except Exception:
            return 0

    @staticmethod
    def lay_danh_sach_ve(
        trang_thai: Optional[str] = None,
        tu_khoa: Optional[str] = None
    ) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Lấy danh sách vé xe kết hợp thông tin xe và thanh toán.
        Dùng chung cho cả Module Vé Xe và tìm kiếm.
        """
        try:
            danh_sach = VehicleRepository.lay_danh_sach_ve(
                trang_thai=trang_thai,
                tu_khoa=tu_khoa
            )
            return True, f"Tìm thấy {len(danh_sach)} vé.", danh_sach
        except Exception as e:
            return False, f"Lỗi truy vấn danh sách vé: {e}", []

    @staticmethod
    def lay_chi_tiet_ve(ma_ve: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Lấy chi tiết toàn diện của một vé xe theo mã vé."""
        if not ma_ve or not ma_ve.strip():
            return False, "Mã vé không được để trống.", None
        try:
            ve = VehicleRepository.lay_ve_theo_ma(ma_ve.strip())
            if not ve:
                return False, f"Không tìm thấy vé '{ma_ve}'.", None
            return True, "Thành công", ve
        except Exception as e:
            return False, f"Lỗi truy vấn chi tiết vé: {e}", None

    @staticmethod
    def tao_doi_tuong_xe_oop(loai_xe: str, bien_so: str, chu_xe: str):
        """
        Adapter method minh họa tính Đa hình và Kế thừa của các class OOP:
        XeMay, OTo, XeDap (kế thừa từ Xe).
        Giữ nguyên 100% các class Console models.
        """
        from models.XeMay import XeMay
        from models.Oto import OTo
        from models.XeDap import XeDap

        if loai_xe == "XeMay":
            return XeMay(bien_so, chu_xe)
        elif loai_xe == "OTo":
            return OTo(bien_so, chu_xe)
        else:
            return XeDap(bien_so, chu_xe)

    # ─────────────────────────── DASHBOARD – KPI TỔNG QUAN ───────────────────────────

    @staticmethod
    def lay_kpi_dashboard() -> Tuple[bool, str, Dict[str, Any]]:
        """
        Lấy bộ KPI tổng quan cho màn hình Dashboard.
        Không yêu cầu quyền Admin – mọi nhân viên đã đăng nhập đều xem được.

        Returns:
            Tuple(thanh_cong, thong_bao, du_lieu_kpi)
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", {}
        try:
            du_lieu = VehicleRepository.lay_kpi_dashboard()
            return True, "Tải KPI Dashboard thành công.", du_lieu
        except Exception as e:
            return False, f"Lỗi tải dữ liệu Dashboard: {e}", {}

    # ─────────────────────────── REVENUE – DOANH THU ───────────────────────────

    @staticmethod
    def lay_tong_doanh_thu(tu_ngay: str = None, den_ngay: str = None) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Tổng hợp doanh thu theo khoảng ngày.
        Chỉ ADMIN được truy cập (kiểm tra tại tầng Service).
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", {}
        if nguoi_dung.vai_tro != "ADMIN":
            return False, "Chỉ Quản trị viên (ADMIN) mới được xem doanh thu.", {}
        try:
            du_lieu = VehicleRepository.lay_tong_doanh_thu(tu_ngay, den_ngay)
            return True, "Tải doanh thu tổng hợp thành công.", du_lieu
        except Exception as e:
            return False, f"Lỗi tải dữ liệu doanh thu: {e}", {}

    @staticmethod
    def lay_doanh_thu_theo_ngay(
        so_ngay: int = 30,
        tu_ngay: str = None,
        den_ngay: str = None
    ) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Thống kê doanh thu từng ngày trong N ngày gần nhất hoặc theo khoảng ngày lọc.
        Chỉ ADMIN được truy cập.
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", []
        if nguoi_dung.vai_tro != "ADMIN":
            return False, "Chỉ Quản trị viên (ADMIN) mới được xem doanh thu.", []
        try:
            du_lieu = VehicleRepository.lay_doanh_thu_theo_ngay(so_ngay=so_ngay, tu_ngay=tu_ngay, den_ngay=den_ngay)
            return True, f"Tải {len(du_lieu)} ngày có doanh thu thành công.", du_lieu
        except Exception as e:
            return False, f"Lỗi tải doanh thu theo ngày: {e}", []

    @staticmethod
    def lay_doanh_thu_theo_thang(nam: int = None) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Thống kê doanh thu từng tháng trong năm.
        Chỉ ADMIN được truy cập.
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", []
        if nguoi_dung.vai_tro != "ADMIN":
            return False, "Chỉ Quản trị viên (ADMIN) mới được xem doanh thu.", []
        try:
            du_lieu = VehicleRepository.lay_doanh_thu_theo_thang(nam)
            return True, "Tải doanh thu theo tháng thành công.", du_lieu
        except Exception as e:
            return False, f"Lỗi tải doanh thu theo tháng: {e}", []

    @staticmethod
    def lay_lich_su_thanh_toan(
        tu_ngay: str = None,
        den_ngay: str = None,
        phuong_thuc: str = None,
        limit: int = 200
    ) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Lịch sử chi tiết giao dịch thanh toán.
        Chỉ ADMIN được truy cập.
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", []
        if nguoi_dung.vai_tro != "ADMIN":
            return False, "Chỉ Quản trị viên (ADMIN) mới được xem lịch sử thanh toán.", []
        try:
            du_lieu = VehicleRepository.lay_lich_su_thanh_toan(tu_ngay, den_ngay, phuong_thuc, limit)
            return True, f"Tìm thấy {len(du_lieu)} giao dịch.", du_lieu
        except Exception as e:
            return False, f"Lỗi tải lịch sử thanh toán: {e}", []

    # ─────────────────────────── STATISTICS – THỐNG KÊ ───────────────────────────

    @staticmethod
    def lay_thong_ke_tong_hop() -> Tuple[bool, str, Dict[str, Any]]:
        """
        Lấy bộ thống kê tổng hợp: tỷ lệ lấp đầy, giờ cao điểm, phân bố loại xe.
        Mọi nhân viên đã đăng nhập đều xem được (không giới hạn Admin).
        """
        nguoi_dung = AuthService.lay_nguoi_dung_hien_tai()
        if not nguoi_dung:
            return False, "Phiên làm việc đã hết hạn.", {}
        try:
            du_lieu = VehicleRepository.lay_thong_ke_tong_hop()
            return True, "Tải thống kê tổng hợp thành công.", du_lieu
        except Exception as e:
            return False, f"Lỗi tải thống kê: {e}", {}
