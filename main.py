import json
from storage.file_txt import luu_du_lieu, doc_du_lieu
from models.XeMay import XeMay
from models.Oto import OTo
from services.quan_ly_bai_xe import QuanLyBaiXe
from datetime import datetime
from models.XeDap import XeDap
# Tao doi tuong quan ly bai xe
bai_xe = QuanLyBaiXe()


# ==================================
# MENU CHINH
# ==================================
def menu_chinh():
    while True:
        print("\n====== QUAN LY BAI GIU XE ======")
        print("1. Quan ly xe")
        print("2. Quan ly ve xe")
        print("3. Doanh thu")
        print("4. Thong ke")
        print("5. Tim kiem")
        print("6. Xuat TXT")
        print("0. Thoat")

        chon = input("Chon chuc nang: ").strip()

        if chon == "1":
            menu_quan_ly_xe()

        elif chon == "2":
            menu_quan_ly_ve()

        elif chon == "3":
            menu_doanh_thu()

        elif chon == "4":
            menu_thong_ke()

        elif chon == "5":
            tim_kiem_xe()


        elif chon == "6":
            luu_du_lieu(bai_xe)
            input("\nNhan Enter de quay lai...")

        elif chon == "0":
            print("Tam biet!")
            break

        else:
            print("Lua chon khong hop le!")


def menu_doanh_thu():
    while True:
        print("\n===== QUAN LY DOANH THU =====")
        print("1. Xem tong doanh thu")
        print("2. Doanh thu hom nay")
        print("3. Doanh thu theo ngay")
        print("4. Lich su thanh toan")
        print("0. Quay lai")

        chon = input("Chon chuc nang: ").strip()

        if chon == "1":
            tong = bai_xe.tinh_doanh_thu()
            print("Tong doanh thu:", tong, "VND")

        elif chon == "2":
            hom_nay = datetime.now().date()
            tong = bai_xe.doanh_thu_theo_ngay(hom_nay)
            print("Doanh thu hom nay:", tong, "VND")

        elif chon == "3":
            ngay_nhap = input(
                "Nhap ngay (dd/mm/yyyy, 0 de quay lai): "
            ).strip()

            if ngay_nhap == "0":
                continue

            try:
                ngay = datetime.strptime(
                    ngay_nhap, "%d/%m/%Y"
                ).date()

                tong = bai_xe.doanh_thu_theo_ngay(ngay)
                print("Doanh thu:", tong, "VND")

            except ValueError:
                print("Ngay khong hop le!")

        elif chon == "4":
            bai_xe.lich_su_thanh_toan()

        elif chon == "0":
            break

        else:
            print("Lua chon khong hop le!")

        input("\nNhan Enter de tiep tuc...")



def menu_thong_ke():
    while True:
        print("\n===== THONG KE BAI XE =====")
        print("1. Tong so xe dang gui")
        print("2. Thong ke theo loai xe")
        print("3. Tong so luot xe vao")
        print("4. Tong so luot xe da ra")
        print("5. Bao cao tong hop")
        print("6. Thong ke theo ngay")
        print("0. Quay lai")

        chon = input("Chon chuc nang: ").strip()

        if chon == "1":
            print("Xe dang gui:", len(bai_xe.danh_sach_xe))

        elif chon == "2":
            so_xe_dap = 0
            so_xe_may = 0
            so_o_to = 0

            for xe in bai_xe.danh_sach_xe:
                if isinstance(xe, XeDap):
                    so_xe_dap += 1
                elif isinstance(xe, XeMay):
                    so_xe_may += 1
                elif isinstance(xe, OTo):
                    so_o_to += 1

            print("\n===== THONG KE THEO LOAI XE =====")
            print("Xe dap:", so_xe_dap)
            print("Xe may:", so_xe_may)
            print("O to:", so_o_to)

        elif chon == "3":
            print("Tong luot xe vao:", len(bai_xe.danh_sach_ve))

        elif chon == "4":
            so_xe_ra = 0

            for ve in bai_xe.danh_sach_ve:
                if ve.trang_thai == "Da thanh toan":
                    so_xe_ra += 1

            print("Tong luot xe da ra:", so_xe_ra)

        elif chon == "5":
            bai_xe.thong_ke_tong_hop()

        elif chon == "6":
            ngay_nhap = input(
                "Nhap ngay (dd/mm/yyyy, 0 de quay lai): "
            ).strip()

            if ngay_nhap == "0":
                continue

            try:
                ngay = datetime.strptime(
                    ngay_nhap, "%d/%m/%Y"
                ).date()

                bai_xe.thong_ke_theo_ngay(ngay)

            except ValueError:
                print("Ngay khong hop le!")

        elif chon == "0":
            break

        else:
            print("Lua chon khong hop le!")

        input("\nNhan Enter de tiep tuc...")

# ==================================
# MENU QUAN LY XE
# ==================================
def menu_quan_ly_xe():
    while True:
        print("\n===== QUAN LY XE =====")
        print("1. Tiep nhan xe")
        print("2. Xe ra bai")
        print("3. Danh sach xe")
        print("0. Quay lai")

        chon = input("Chon chuc nang: ").strip()

        if chon == "1":
            nhap_xe()


        elif chon == "2":
           xu_ly_xe_ra()

        elif chon == "3":
            bai_xe.xem_danh_sach()
            input("\nNhan Enter de quay lai...")

        elif chon == "0":
            break

        else:
            print("Lua chon khong hop le!")


# ==================================
# TIEP NHAN XE
# ==================================
def nhap_xe():
    print("\n===== TIEP NHAN XE =====")

    # Nhap va kiem tra bien so
    while True:
        bien_so = input("Nhap bien so (0 de quay lai): ").strip().upper()

        if bien_so == "0":
            return

        if bien_so == "":
            print("Bien so khong duoc de trong!")
            continue

        if bai_xe.tim_xe(bien_so) is not None:
            print("Bien so da ton tai! Vui long nhap lai.")
            continue

        break

    # Nhap va kiem tra chu xe
    while True:
        chu_xe = input("Nhap ten chu xe: ").strip()

        if chu_xe == "":
            print("Ten chu xe khong duoc de trong!")
            continue

        break

    # Chon loai xe
    while True:
        print("\n===== CHON LOAI XE =====")
        print("1. Xe dap")
        print("2. Xe may")
        print("3. O to")

        loai_xe = input("Chon loai xe: ").strip()

        if loai_xe == "1":
            xe = XeDap(bien_so, chu_xe)
            break

        elif loai_xe == "2":
            xe = XeMay(bien_so, chu_xe)
            break

        elif loai_xe == "3":
            xe = OTo(bien_so, chu_xe)
            break

        else:
            print("Loai xe khong hop le!")
    # Them xe vao bai va tu dong tao ve
    ket_qua = bai_xe.them_xe(xe)

    if ket_qua:
        luu_du_lieu(bai_xe)
    if not ket_qua:
        print("Tiep nhan xe that bai!")

    input("\nNhan Enter de quay lai...")


# ==================================
# TIM KIEM XE
# ==================================
def tim_kiem_xe():
    print("\n===== TIM KIEM XE =====")

    bien_so = input("Nhap bien so can tim: ").strip()

    if bien_so == "":
        print("Bien so khong duoc de trong!")
        input("\nNhan Enter de quay lai...")
        return

    xe = bai_xe.tim_xe(bien_so)

    if xe is not None:
        print("\nTim thay xe!")
        xe.hien_thi()
        print("Phi gui xe du kien:", xe.tinh_phi(), "VND")
    else:
        print("Khong tim thay xe trong bai!")

    input("\nNhan Enter de quay lai...")


# ==================================
# MENU QUAN LY VE XE
# ==================================
def menu_quan_ly_ve():
    while True:
        print("\n===== QUAN LY VE XE =====")
        print("1. Danh sach ve")
        print("2. Tim ve theo ma")
        print("0. Quay lai")

        chon = input("Chon chuc nang: ").strip()

        if chon == "1":
            print("\n===== DANH SACH VE =====")

            if len(bai_xe.danh_sach_ve) == 0:
                print("Chua co ve xe nao!")
            else:
                for ve in bai_xe.danh_sach_ve:
                    ve.hien_thi()

            input("\nNhan Enter de quay lai...")

        elif chon == "2":
            print("\n===== TIM KIEM VE =====")

            ma_ve = input("Nhap ma ve: ").strip()
            ve = bai_xe.tim_ve(ma_ve)

            if ve is not None:
                print("Tim thay ve!")
                ve.hien_thi()
            else:
                print("Khong tim thay ve!")

            input("\nNhan Enter de quay lai...")

        elif chon == "0":
            break

        else:
            print("Lua chon khong hop le!")

    # ==================================
    # XU LY XE RA
    # ==================================
def xu_ly_xe_ra():
    print("\n===== XE RA BAI =====")

    while True:
        bien_so = input("Nhap bien so xe ra (0 de quay lai): ").strip()

        if bien_so == "0":
            print("Da quay lai menu quan ly xe!")
            return

        if bien_so == "":
            print("Bien so khong duoc de trong!")
            continue

        ket_qua = bai_xe.xe_ra(bien_so)

        if ket_qua:
            luu_du_lieu(bai_xe)

        input("\nNhan Enter de quay lai...")
        return


# ==================================
# CHAY CHUONG TRINH
# ==================================
if __name__ == "__main__":
    try:
        doc_du_lieu(bai_xe)
    except (OSError, ValueError, KeyError, TypeError) as loi:
        print("Khong the doc du lieu:", loi)
        print("Chuong trinh dung de tranh ghi de du lieu cu.")
    else:
        menu_chinh()
