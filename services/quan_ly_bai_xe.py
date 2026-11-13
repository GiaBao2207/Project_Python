from models.XeMay import XeMay
from models.Oto import OTo
from models.ve_xe import VeXe
from models.XeDap import XeDap
from datetime import datetime

class QuanLyBaiXe:

    def __init__(self):
        self.danh_sach_xe = []
        self.danh_sach_ve = []
        self.so_ve_tiep_theo = 1

    # Them xe va tao ve
    def them_xe(self, xe):
        xe.bien_so = xe.bien_so.strip().upper()

        xe_da_co = self.tim_xe(xe.bien_so)

        if xe_da_co is not None:
            print("Xe nay da co trong bai!")
            return False

        ma_ve = "VE" + str(self.so_ve_tiep_theo).zfill(4)
        ve = VeXe(ma_ve, xe)

        self.danh_sach_xe.append(xe)
        self.danh_sach_ve.append(ve)

        self.so_ve_tiep_theo += 1

        print("Tiep nhan xe thanh cong!")
        ve.hien_thi()

        return True

    # Tim xe theo bien so
    def tim_xe(self, bien_so):
        bien_so = bien_so.strip().upper()

        for xe in self.danh_sach_xe:
            if xe.bien_so == bien_so:
                return xe

        return None

    # Hien thi danh sach xe
    def xem_danh_sach(self):
        print("\n===== DANH SACH XE =====")

        if len(self.danh_sach_xe) == 0:
            print("Bai xe dang trong!")
            return

        for xe in self.danh_sach_xe:
            xe.hien_thi()
            print("--------------------")

    # Tim ve theo ma
    def tim_ve(self, ma_ve):
        ma_ve = ma_ve.strip().upper()

        for ve in self.danh_sach_ve:
            if ve.ma_ve == ma_ve:
                return ve

        return None

    def tim_ve_theo_bien_so(self, bien_so):
        for ve in self.danh_sach_ve:
            if (ve.xe.bien_so == bien_so.strip().upper()
                    and ve.trang_thai == "Dang gui"):
                return ve

        return None
    def xe_ra(self, bien_so):
        xe = self.tim_xe(bien_so)

        if xe is None:
            print("Khong tim thay xe trong bai!")
            return False

        ve = self.tim_ve_theo_bien_so(bien_so)

        if ve is None:
            print("Khong tim thay ve dang gui!")
            return False

        phi = xe.tinh_phi()

        print("\n===== THONG TIN THANH TOAN =====")
        ve.hien_thi()
        print("Phi can thanh toan:", phi, "VND")

        xac_nhan = input("Xac nhan xe ra? (y/n): ").strip().lower()

        if xac_nhan != "y":
            print("Da huy giao dich!")
            return False

        ve.hoan_thanh(phi)
        self.danh_sach_xe.remove(xe)

        print("Thanh toan thanh cong!")
        print("Xe da roi khoi bai!")
        return True

    def tinh_doanh_thu(self):
        tong_tien = 0

        for ve in self.danh_sach_ve:
            if ve.trang_thai == "Da thanh toan":
                tong_tien += ve.phi_gui_xe

        return tong_tien

    def doanh_thu_theo_ngay(self, ngay):
        tong_tien = 0

        for ve in self.danh_sach_ve:
            if ve.trang_thai == "Da thanh toan":
                if ve.gio_ra is not None:
                    if ve.gio_ra.date() == ngay:
                        tong_tien += ve.phi_gui_xe

        return tong_tien

    def lich_su_thanh_toan(self):
        print("\n===== LICH SU THANH TOAN =====")
        so_giao_dich = 0

        for ve in self.danh_sach_ve:
            if ve.trang_thai == "Da thanh toan":
                ve.hien_thi()
                so_giao_dich += 1

        if so_giao_dich == 0:
            print("Chua co giao dich thanh toan!")


    # ==================================
    # BAO CAO THONG KE TONG HOP
    # ==================================
    def thong_ke_tong_hop(self):
        so_xe_dap = 0
        so_xe_may = 0
        so_o_to = 0
        so_xe_da_ra = 0

        # Dem cac xe dang gui
        for xe in self.danh_sach_xe:
            if isinstance(xe, XeDap):
                so_xe_dap += 1

            elif isinstance(xe, XeMay):
                so_xe_may += 1

            elif isinstance(xe, OTo):
                so_o_to += 1

        # Dem cac ve da thanh toan
        for ve in self.danh_sach_ve:
            if ve.trang_thai == "Da thanh toan":
                so_xe_da_ra += 1

        print("\n===== BAO CAO TONG HOP =====")
        print("Tong xe dang gui:", len(self.danh_sach_xe))
        print("Xe dap dang gui:", so_xe_dap)
        print("Xe may dang gui:", so_xe_may)
        print("O to dang gui:", so_o_to)
        print("Tong luot xe vao:", len(self.danh_sach_ve))
        print("Tong luot xe da ra:", so_xe_da_ra)

    def thong_ke_theo_ngay(self, ngay):
        xe_vao = 0
        xe_ra = 0

        xe_dap_vao = 0
        xe_may_vao = 0
        o_to_vao = 0

        for ve in self.danh_sach_ve:

            if ve.gio_vao.date() == ngay:
                xe_vao += 1

                if isinstance(ve.xe, XeDap):
                    xe_dap_vao += 1

                elif isinstance(ve.xe, XeMay):
                    xe_may_vao += 1

                elif isinstance(ve.xe, OTo):
                    o_to_vao += 1

            if ve.gio_ra is not None:
                if ve.gio_ra.date() == ngay:
                    xe_ra += 1

        print("\n===== THONG KE THEO NGAY =====")
        print("Ngay:", ngay.strftime("%d/%m/%Y"))
        print("Tong luot xe vao:", xe_vao)
        print("Tong luot xe ra:", xe_ra)
        print("Xe dap vao:", xe_dap_vao)
        print("Xe may vao:", xe_may_vao)
        print("O to vao:", o_to_vao)