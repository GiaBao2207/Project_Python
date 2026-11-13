
import json
from pathlib import Path
from datetime import datetime
from models.XeDap import XeDap
from models.XeMay import XeMay
from models.Oto import OTo
from models.ve_xe import VeXe


# Duong dan file TXT
DUONG_DAN = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "du_lieu_bai_xe.txt"
)


def luu_du_lieu(bai_xe):
    du_lieu = {
        "so_ve_tiep_theo": bai_xe.so_ve_tiep_theo,
        "danh_sach_ve": []
    }

    for ve in bai_xe.danh_sach_ve:

        if isinstance(ve.xe, XeDap):
            loai_xe = "XeDap"
        elif isinstance(ve.xe, XeMay):
            loai_xe = "XeMay"
        elif isinstance(ve.xe, OTo):
            loai_xe = "OTo"
        else:
            raise ValueError("Loai xe khong duoc ho tro")

        thong_tin_ve = {
            "ma_ve": ve.ma_ve,
            "bien_so": ve.xe.bien_so,
            "chu_xe": ve.xe.chu_xe,
            "loai_xe": loai_xe,
            "gio_vao": ve.gio_vao.isoformat(),
            "gio_ra": (
                ve.gio_ra.isoformat()
                if ve.gio_ra is not None else None
            ),
            "phi_gui_xe": ve.phi_gui_xe,
            "trang_thai": ve.trang_thai
        }

        du_lieu["danh_sach_ve"].append(thong_tin_ve)

    DUONG_DAN.parent.mkdir(parents=True, exist_ok=True)

    with open(DUONG_DAN, "w", encoding="utf-8") as file:
        json.dump(du_lieu, file, ensure_ascii=False, indent=4)

    print("Da luu du lieu thanh cong!")


def doc_du_lieu(bai_xe):
    if not DUONG_DAN.exists():
        print("Chua co file du lieu. Bat dau voi bai xe trong.")
        return

    with open(DUONG_DAN, "r", encoding="utf-8") as file:
        du_lieu = json.load(file)

    danh_sach_xe_moi = []
    danh_sach_ve_moi = []
    ma_ve_lon_nhat = 0

    for thong_tin in du_lieu["danh_sach_ve"]:

        bien_so = thong_tin["bien_so"]
        chu_xe = thong_tin["chu_xe"]

        if thong_tin["loai_xe"] == "XeDap":
            xe = XeDap(bien_so, chu_xe)
        elif thong_tin["loai_xe"] == "XeMay":
            xe = XeMay(bien_so, chu_xe)
        elif thong_tin["loai_xe"] == "OTo":
            xe = OTo(bien_so, chu_xe)
        else:
            raise ValueError("Loai xe khong hop le")

        ve = VeXe(thong_tin["ma_ve"], xe)

        ve.gio_vao = datetime.fromisoformat(
            thong_tin["gio_vao"]
        )

        if thong_tin["gio_ra"] is not None:
            ve.gio_ra = datetime.fromisoformat(
                thong_tin["gio_ra"]
            )
        else:
            ve.gio_ra = None

        ve.phi_gui_xe = thong_tin["phi_gui_xe"]
        ve.trang_thai = thong_tin["trang_thai"]

        danh_sach_ve_moi.append(ve)

        if ve.trang_thai == "Dang gui":
            danh_sach_xe_moi.append(xe)

        so_ve = int(ve.ma_ve[2:])
        ma_ve_lon_nhat = max(ma_ve_lon_nhat, so_ve)

    # Chi cap nhat khi doc xong toan bo du lieu
    bai_xe.danh_sach_xe = danh_sach_xe_moi
    bai_xe.danh_sach_ve = danh_sach_ve_moi

    bai_xe.so_ve_tiep_theo = max(
        du_lieu["so_ve_tiep_theo"],
        ma_ve_lon_nhat + 1
    )

    print("Da doc du lieu TXT thanh cong!")
