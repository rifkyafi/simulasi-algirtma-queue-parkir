from structures.queue import Queue
from structures.stack import Stack
from structures.bst import BinarySearchTree
from structures.heap import MaxHeap
from models.kendaraan import Kendaraan


class ParkirSystem:
    def __init__(self):
        self.antrian_masuk = Queue()
        self.parkir_aktif = BinarySearchTree()
        self.prioritas_keluar = MaxHeap()
        self.riwayat = Stack()
        self.no_tiket_counter = 1

    def kendaraan_masuk(self, plat, jenis, vip, jam_masuk):
        k = Kendaraan(self.no_tiket_counter, plat, jenis, vip, jam_masuk)
        self.no_tiket_counter += 1
        self.antrian_masuk.enqueue(k)
        print(f"[QUEUE] Kendaraan {plat} masuk antrian. Tiket #{k.no_tiket:03d} | Prioritas: {k.prioritas}")

    def proses_antrian(self):
        if self.antrian_masuk.is_empty():
            print("[QUEUE] Antrian masuk kosong.")
            return
        k = self.antrian_masuk.dequeue()
        self.parkir_aktif.insert(k.no_tiket, k)
        self.prioritas_keluar.insert((k.prioritas, k.no_tiket))
        print(f"[QUEUE >> BST >> HEAP] Tiket#{k.no_tiket:03d} - {k.plat} diproses masuk area parkir.")

    def cari_kendaraan(self, no_tiket):
        node = self.parkir_aktif.search(no_tiket)
        if node:
            return node.data
        return None

    def proses_keluar(self):
        if self.prioritas_keluar.is_empty():
            print("[HEAP] Tidak ada kendaraan parkir.")
            return
        item = self.prioritas_keluar.extract_max()
        prioritas, no_tiket = item
        k = self.parkir_aktif.delete(no_tiket)
        if k:
            self.riwayat.push(k)
            print(f"[HEAP >> BST >> STACK] Tiket#{k.no_tiket:03d} - {k.plat} keluar (prioritas:{prioritas}). Disimpan ke riwayat.")
        else:
            print(f"[ERROR] Tiket#{no_tiket} tidak ditemukan di BST.")

    def undo_keluar(self):
        if self.riwayat.is_empty():
            print("[STACK] Tidak ada riwayat untuk di-undo.")
            return
        k = self.riwayat.pop()
        self.parkir_aktif.insert(k.no_tiket, k)
        self.prioritas_keluar.insert((k.prioritas, k.no_tiket))
        print(f"[STACK >> BST >> HEAP] Undo: Tiket#{k.no_tiket:03d} - {k.plat} dikembalikan ke parkir.")

    def lihat_antrian_masuk(self):
        items = self.antrian_masuk.display()
        print("\n" + "="*60)
        print("  ANTRIAN MASUK (QUEUE - FIFO)")
        print("="*60)
        if not items:
            print("  (kosong)")
            return
        for i, k in enumerate(items, 1):
            print(f"  {i:2d}. {k}")
        print(f"  Total: {len(items)} kendaraan menunggu")

    def lihat_parkir_aktif(self):
        items = self.parkir_aktif.inorder()
        print("\n" + "="*60)
        print("  KENDARAAN PARKIR (BST - Inorder)")
        print("="*60)
        if not items:
            print("  (kosong)")
            return
        for key, k in items:
            print(f"  {k}")
        print(f"  Total: {len(items)} kendaraan parkir")

    def lihat_prioritas(self):
        items = self.prioritas_keluar.display()
        print("\n" + "="*60)
        print("  PRIORITAS KELUAR (MAX HEAP)")
        print("="*60)
        if not items:
            print("  (kosong)")
            return
        sorted_items = sorted(items, key=lambda x: x[0], reverse=True)
        for i, (p, no_tiket) in enumerate(sorted_items, 1):
            node = self.parkir_aktif.search(no_tiket)
            k = node.data if node else f"Unknown #{no_tiket:03d}"
            print(f"  {i:2d}. Prioritas:{p:3d} | {k}")
        print(f"  Total: {len(items)} kendaraan antri keluar")

    def lihat_riwayat(self):
        items = self.riwayat.display()
        print("\n" + "="*60)
        print("  RIWAYAT TRANSAKSI (STACK - LIFO)")
        print("="*60)
        if not items:
            print("  (kosong)")
            return
        for i, k in enumerate(items, 1):
            print(f"  {i:2d}. {k}")
        print(f"  Total: {len(items)} transaksi tersimpan")

    def lihat_semua(self):
        print("\n" + "="*60)
        print("  STATUS SISTEM PARKIR")
        print("="*60)
        q_size = self.antrian_masuk.size()
        bst_size = len(self.parkir_aktif.inorder())
        h_size = self.prioritas_keluar.size()
        s_size = self.riwayat.size()
        print(f"  Queue (antrian masuk)     : {q_size} kendaraan")
        print(f"  BST   (parkir aktif)      : {bst_size} kendaraan")
        print(f"  Heap  (prioritas keluar)  : {h_size} kendaraan")
        print(f"  Stack (riwayat transaksi) : {s_size} kendaraan")
