class Kendaraan:
    def __init__(self, no_tiket, plat, jenis, vip, jam_masuk):
        self.no_tiket = no_tiket
        self.plat = plat
        self.jenis = jenis
        self.vip = vip
        self.jam_masuk = jam_masuk
        self.prioritas = self.hitung_prioritas()

    def hitung_prioritas(self):
        skor_vip = 120 if self.vip == "VIP" else 20
        skor_jenis = 50 if self.jenis == "Mobil" else 25
        skor_durasi = self.jam_masuk * 10
        return skor_vip + skor_jenis + skor_durasi

    def __str__(self):
        return (f"Tiket#{self.no_tiket:03d} | {self.plat:<10} | {self.jenis:<6} | "
                f"{self.vip:<7} | Masuk:{self.jam_masuk:02d}:00 | Prioritas:{self.prioritas}")
