
from datetime import datetime


class VeXe:
    def __init__(self, ma_ve, xe):
        self.ma_ve = ma_ve
        self.xe = xe
        self.gio_vao = datetime.now()
        self.gio_ra = None
        self.phi_gui_xe = 0
        self.trang_thai = "Dang gui"

    def hoan_thanh(self, phi):
        self.gio_ra = datetime.now()
        self.phi_gui_xe = phi
        self.trang_thai = "Da thanh toan"

    def hien_thi(self):
        print("\n===== THONG TIN VE =====")
        print("Ma ve:", self.ma_ve)
        print("Bien so:", self.xe.bien_so)
        print("Chu xe:", self.xe.chu_xe)

        print("Gio vao:",
              self.gio_vao.strftime("%d/%m/%Y %H:%M:%S"))

        if self.gio_ra is not None:
            print("Gio ra:",
                  self.gio_ra.strftime("%d/%m/%Y %H:%M:%S"))

        print("Trang thai:", self.trang_thai)

        if self.trang_thai == "Da thanh toan":
            print("Phi gui xe:", self.phi_gui_xe, "VND")
