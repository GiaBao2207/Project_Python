from models.xe import Xe


class XeMay(Xe):
    def __init__(self, bien_so, chu_xe):
        super().__init__(bien_so, chu_xe)

    def tinh_phi(self):
        return 5000

    def hien_thi(self):
        super().hien_thi()
        print("Loai xe: Xe may")