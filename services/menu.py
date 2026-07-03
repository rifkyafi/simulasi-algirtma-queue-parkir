from services.parkir_system import ParkirSystem


class Menu:
    def __init__(self):
        self.system = ParkirSystem()

    def run(self):
        while True:
            print("\n" + "="*60)
            print("  SISTEM MANAJEMEN PARKIR - ALGORITMA & STRUKTUR DATA")
            print("="*60)
            print("  1.  Kendaraan Masuk (>> Queue)")
            print("  2.  Proses Antrian Masuk (Queue >> BST >> Heap)")
            print("  3.  Lihat Antrian Masuk (Queue)")
            print("  4.  Cari Kendaraan (BST)")
            print("  5.  Proses Keluar (Heap >> BST >> Stack)")
            print("  6.  Lihat Status Parkir (BST)")
            print("  7.  Lihat Prioritas Keluar (Heap)")
            print("  8.  Undo Transaksi Terakhir (Stack >> BST >> Heap)")
            print("  9.  Lihat Riwayat Transaksi (Stack)")
            print("  10. Status Semua Struktur Data")
            print("  0.  Keluar")
            print("-"*60)
            pilihan = input("  Pilih menu (0-10): ").strip()

            if pilihan == '1':
                plat = input("  Plat nomor: ").strip().upper()
                print("  Jenis: 1. Mobil  2. Motor")
                j = input("  Pilih (1/2): ").strip()
                jenis = "Mobil" if j == '1' else "Motor"
                print("  Status: 1. VIP  2. Reguler")
                v = input("  Pilih (1/2): ").strip()
                vip = "VIP" if v == '1' else "Reguler"
                jam = int(input("  Jam masuk (0-23): ").strip())
                self.system.kendaraan_masuk(plat, jenis, vip, jam)

            elif pilihan == '2':
                self.system.proses_antrian()

            elif pilihan == '3':
                self.system.lihat_antrian_masuk()

            elif pilihan == '4':
                no = int(input("  Nomor tiket: ").strip())
                k = self.system.cari_kendaraan(no)
                if k:
                    print(f"  [BST] Ditemukan >> {k}")
                else:
                    print(f"  [BST] Tiket#{no:03d} tidak ditemukan.")

            elif pilihan == '5':
                self.system.proses_keluar()

            elif pilihan == '6':
                self.system.lihat_parkir_aktif()

            elif pilihan == '7':
                self.system.lihat_prioritas()

            elif pilihan == '8':
                self.system.undo_keluar()

            elif pilihan == '9':
                self.system.lihat_riwayat()

            elif pilihan == '10':
                self.system.lihat_semua()

            elif pilihan == '0':
                print("\n  Terima kasih telah menggunakan sistem parkir.")
                break
            else:
                print("  Pilihan tidak valid.")
