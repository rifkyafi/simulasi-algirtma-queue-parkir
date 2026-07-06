"""
Sistem Manajemen Parkir
=======================
Program ini mensimulasikan sistem parkir menggunakan empat struktur data utama:
  - Queue  (Antrian FIFO) : kendaraan yang menunggu masuk
  - BST    (Binary Search Tree) : kendaraan yang sedang parkir
  - MaxHeap               : menentukan prioritas kendaraan keluar
  - Stack  (Tumpukan LIFO): riwayat transaksi (bisa di-undo)

Dibuat untuk keperluan pembelajaran Algoritma & Struktur Data.
"""

# =============================================================================
# KONSTANTA
# Angka-angka di sini diberi nama agar mudah dipahami dan mudah diubah.
# =============================================================================

SKOR_STATUS_VIP = 120       # Poin tambahan untuk kendaraan VIP
SKOR_STATUS_REGULER = 20    # Poin tambahan untuk kendaraan Reguler
SKOR_JENIS_MOBIL = 50       # Poin tambahan untuk jenis Mobil
SKOR_JENIS_MOTOR = 25       # Poin tambahan untuk jenis Motor
SKOR_PER_JAM_MASUK = 10     # Poin per jam masuk (semakin pagi = semakin lama parkir = prioritas lebih tinggi)

SEPARATOR  = "=" * 78       # Garis pembatas utama


# Lebar setiap kolom pada tabel kendaraan
LEBAR_NO     = 4
LEBAR_TIKET  = 9
LEBAR_PLAT   = 12
LEBAR_JENIS  = 8
LEBAR_STATUS = 9
LEBAR_JAM    = 12
LEBAR_PRIORITAS = 11


# =============================================================================
# STRUKTUR DATA DASAR: NODE
# Node adalah "kotak" yang menyimpan satu data dan penunjuk ke kotak berikutnya.
# Digunakan oleh Queue dan Stack.
# =============================================================================

class Node:
    """
    Satu simpul (node) dalam linked list.

    Bayangkan Node seperti satu gerbong kereta:
      - 'data'  -> muatan/isi gerbong
      - 'next'  -> sambungan ke gerbong berikutnya (None = gerbong terakhir)
    """

    def __init__(self, data):
        self.data = data    # Data yang disimpan di dalam node ini
        self.next = None    # Penunjuk ke node berikutnya; None berarti belum ada


# =============================================================================
# STRUKTUR DATA DASAR: BST NODE
# BSTNode adalah "kotak" khusus untuk Binary Search Tree.
# Setiap node punya dua cabang: kiri (nilai lebih kecil) dan kanan (nilai lebih besar).
# =============================================================================

class BSTNode:
    """
    Satu simpul (node) dalam Binary Search Tree (BST).

    Bayangkan BSTNode seperti simpul di pohon:
      - 'key'   -> nomor unik untuk mengurutkan dan mencari
      - 'data'  -> data asli yang disimpan
      - 'left'  -> cabang kiri (node dengan key lebih kecil)
      - 'right' -> cabang kanan (node dengan key lebih besar)
    """

    def __init__(self, key, data):
        self.key = key      # Kunci unik untuk pencarian (misalnya: nomor tiket)
        self.data = data    # Data asli yang disimpan (misalnya: objek Kendaraan)
        self.left = None    # Cabang kiri  -> node dengan key lebih kecil
        self.right = None   # Cabang kanan -> node dengan key lebih besar


# =============================================================================
# STRUKTUR DATA: QUEUE (ANTRIAN)
# Prinsip: FIFO (First In, First Out) — yang pertama masuk, pertama keluar.
# Contoh nyata: antrian kasir di supermarket.
# =============================================================================

class Queue:
    """
    Antrian (Queue) dengan prinsip FIFO.

    FIFO = First In, First Out:
      Kendaraan yang PERTAMA masuk antrian akan PERTAMA diproses.

    Visualisasi:
      Masuk -> [C] [B] [A] -> Keluar
                ^               ^
             rear (belakang)  front (depan)
    """

    def __init__(self):
        self.front = None   # Penunjuk ke node paling depan (yang akan diproses duluan)
        self.rear = None    # Penunjuk ke node paling belakang (yang baru saja masuk)

    def tambah_ke_antrian(self, data):
        """
        Menambahkan data baru ke BELAKANG antrian (enqueue).

        Contoh: kendaraan baru datang -> langsung ke ujung antrian.
        """
        node_baru = Node(data)

        # Jika antrian kosong, node baru menjadi satu-satunya node (depan sekaligus belakang)
        if self.rear is None:
            self.front = self.rear = node_baru
            return

        # Sambungkan node terakhir ke node baru, lalu geser penunjuk belakang
        self.rear.next = node_baru
        self.rear = node_baru

    def ambil_dari_depan(self):
        """
        Mengambil dan menghapus data dari DEPAN antrian (dequeue).

        Contoh: kendaraan paling depan selesai diproses -> keluar dari antrian.
        Mengembalikan None jika antrian kosong.
        """
        # Jika antrian kosong, tidak ada yang bisa diambil
        if self.front is None:
            return None

        node_depan = self.front             # Simpan referensi ke node depan
        self.front = node_depan.next        # Geser penunjuk depan ke node berikutnya

        # Jika antrian sekarang kosong, rear juga harus di-reset ke None
        if self.front is None:
            self.rear = None

        return node_depan.data

    def lihat_depan(self):
        """
        Melihat data di depan antrian TANPA menghapusnya (peek).

        Berguna untuk cek siapa yang berikutnya, tanpa memproses dulu.
        """
        if self.front is None:
            return None
        return self.front.data

    def tampilkan_semua(self):
        """
        Mengembalikan semua isi antrian sebagai list, dari depan ke belakang.
        """
        daftar_isi = []
        node_sekarang = self.front

        # Telusuri semua node dari depan ke belakang
        while node_sekarang is not None:
            daftar_isi.append(node_sekarang.data)
            node_sekarang = node_sekarang.next  # Pindah ke node berikutnya

        return daftar_isi

    def kosong(self):
        """Mengembalikan True jika antrian kosong, False jika ada isinya."""
        return self.front is None

    def hitung_isi(self):
        """Menghitung berapa banyak item di dalam antrian."""
        jumlah = 0
        node_sekarang = self.front

        while node_sekarang is not None:
            jumlah += 1
            node_sekarang = node_sekarang.next

        return jumlah


# =============================================================================
# STRUKTUR DATA: STACK (TUMPUKAN)
# Prinsip: LIFO (Last In, First Out) — yang terakhir masuk, pertama keluar.
# Contoh nyata: tumpukan piring; piring teratas diambil duluan.
# =============================================================================

class Stack:
    """
    Tumpukan (Stack) dengan prinsip LIFO.

    LIFO = Last In, First Out:
      Data yang TERAKHIR dimasukkan akan PERTAMA diambil kembali.

    Visualisasi (puncak = paling atas):
      <- masuk/keluar
      [C]  <- puncak (diambil duluan)
      [B]
      [A]  <- paling bawah
    """

    def __init__(self):
        self.puncak = None  # Penunjuk ke node paling atas (yang akan diambil duluan)

    def simpan(self, data):
        """
        Menyimpan data baru ke PUNCAK tumpukan (push).

        Contoh: kendaraan keluar -> transaksinya disimpan ke atas tumpukan riwayat.
        """
        node_baru = Node(data)
        node_baru.next = self.puncak    # Node baru menunjuk ke node yang tadinya di puncak
        self.puncak = node_baru         # Node baru sekarang menjadi puncak baru

    def ambil_teratas(self):
        """
        Mengambil dan menghapus data dari PUNCAK tumpukan (pop).

        Contoh: undo -> ambil transaksi terakhir dari tumpukan riwayat.
        Mengembalikan None jika tumpukan kosong.
        """
        if self.puncak is None:
            return None

        node_puncak = self.puncak          # Simpan referensi ke puncak sekarang
        self.puncak = self.puncak.next     # Geser puncak ke node di bawahnya
        return node_puncak.data

    def lihat_teratas(self):
        """
        Melihat data di puncak tumpukan TANPA menghapusnya (peek).
        """
        if self.puncak is None:
            return None
        return self.puncak.data

    def tampilkan_semua(self):
        """
        Mengembalikan semua isi tumpukan sebagai list, dari atas ke bawah.
        """
        daftar_isi = []
        node_sekarang = self.puncak

        while node_sekarang is not None:
            daftar_isi.append(node_sekarang.data)
            node_sekarang = node_sekarang.next

        return daftar_isi

    def kosong(self):
        """Mengembalikan True jika tumpukan kosong."""
        return self.puncak is None

    def hitung_isi(self):
        """Menghitung berapa banyak item di dalam tumpukan."""
        jumlah = 0
        node_sekarang = self.puncak

        while node_sekarang is not None:
            jumlah += 1
            node_sekarang = node_sekarang.next

        return jumlah


# =============================================================================
# STRUKTUR DATA: MAX HEAP
# Prinsip: Nilai terbesar selalu berada di paling atas (root).
# Digunakan untuk menentukan kendaraan mana yang PALING PRIORITAS keluar duluan.
# =============================================================================

class MaxHeap:
    """
    Max Heap — struktur data untuk mengelola prioritas.

    Aturan utama:
      Elemen dengan nilai TERBESAR selalu berada di posisi pertama (index 0).

    Contoh penggunaan di sini:
      Kendaraan dengan skor prioritas tertinggi akan keluar duluan.

    Implementasi menggunakan list Python biasa (bukan linked list).
    """

    def __init__(self):
        self.data = []  # List yang menyimpan semua elemen heap

    def tambahkan(self, item):
        """
        Menambahkan item baru ke dalam heap.

        Setelah ditambahkan, heap akan merapikan diri agar nilai terbesar
        tetap di posisi paling atas (_naikkan).
        """
        self.data.append(item)
        self._naikkan(len(self.data) - 1)   # Rapikan dari posisi terakhir ke atas

    def ambil_terbesar(self):
        """
        Mengambil dan menghapus item dengan nilai TERBESAR dari heap.

        Setelah diambil, heap akan merapikan diri lagi (_turunkan).
        Mengembalikan None jika heap kosong.
        """
        if not self.data:
            return None

        # Jika hanya ada satu item, langsung keluarkan
        if len(self.data) == 1:
            return self.data.pop()

        item_terbesar = self.data[0]        # Simpan item terbesar (selalu di index 0)
        self.data[0] = self.data.pop()      # Pindahkan item terakhir ke posisi 0
        self._turunkan(0)                   # Rapikan dari atas ke bawah

        return item_terbesar

    def lihat_terbesar(self):
        """Melihat item terbesar TANPA menghapusnya."""
        if not self.data:
            return None
        return self.data[0]

    def _naikkan(self, posisi_anak):
        """
        Proses internal: naikkan item ke atas sampai heap kembali valid.

        Heap dikatakan valid jika setiap node lebih besar dari anak-anaknya.
        Rumus posisi parent: (posisi_anak - 1) // 2
        """
        posisi_parent = (posisi_anak - 1) // 2

        # Selama masih ada parent dan nilai anak lebih besar dari parent, tukar posisi
        if posisi_anak > 0 and self.data[posisi_anak][0] > self.data[posisi_parent][0]:
            self.data[posisi_anak], self.data[posisi_parent] = (
                self.data[posisi_parent], self.data[posisi_anak]
            )
            self._naikkan(posisi_parent)    # Lanjutkan proses naik dari posisi parent

    def _turunkan(self, posisi_parent):
        """
        Proses internal: turunkan item ke bawah sampai heap kembali valid.

        Bandingkan dengan anak kiri dan anak kanan, tukar dengan yang terbesar.
        Rumus posisi anak kiri : 2 * posisi_parent + 1
        Rumus posisi anak kanan: 2 * posisi_parent + 2
        """
        posisi_terbesar = posisi_parent
        posisi_kiri = 2 * posisi_parent + 1
        posisi_kanan = 2 * posisi_parent + 2

        # Cek apakah anak kiri lebih besar dari parent saat ini
        if posisi_kiri < len(self.data) and self.data[posisi_kiri][0] > self.data[posisi_terbesar][0]:
            posisi_terbesar = posisi_kiri

        # Cek apakah anak kanan lebih besar dari node terbesar saat ini
        if posisi_kanan < len(self.data) and self.data[posisi_kanan][0] > self.data[posisi_terbesar][0]:
            posisi_terbesar = posisi_kanan

        # Jika ada yang lebih besar dari parent, tukar dan lanjutkan proses turun
        if posisi_terbesar != posisi_parent:
            self.data[posisi_parent], self.data[posisi_terbesar] = (
                self.data[posisi_terbesar], self.data[posisi_parent]
            )
            self._turunkan(posisi_terbesar)

    def tampilkan_semua(self):
        """Mengembalikan salinan semua isi heap sebagai list."""
        return self.data[:]     # Pakai [:] agar yang dikembalikan adalah salinan, bukan referensi asli

    def kosong(self):
        """Mengembalikan True jika heap kosong."""
        return len(self.data) == 0

    def hitung_isi(self):
        """Menghitung berapa banyak item di dalam heap."""
        return len(self.data)


# =============================================================================
# STRUKTUR DATA: BINARY SEARCH TREE (BST)
# BST adalah pohon biner di mana:
#   - Semua node di KIRI memiliki key LEBIH KECIL dari node parent
#   - Semua node di KANAN memiliki key LEBIH BESAR dari node parent
# Keunggulan: pencarian, penyisipan, dan penghapusan lebih cepat dari list biasa.
# =============================================================================

class BinarySearchTree:
    """
    Binary Search Tree (BST) — pohon pencarian biner.

    Digunakan untuk menyimpan kendaraan yang sedang parkir.
    Key yang digunakan adalah nomor tiket kendaraan.

    Contoh struktur BST dengan key [5, 3, 7, 1, 4]:
              5
             / \\
            3   7
           / \\
          1   4
    """

    def __init__(self):
        self.akar = None    # Akar pohon (root); None berarti pohon masih kosong

    def sisipkan(self, key, data):
        """
        Menyisipkan data baru ke dalam BST berdasarkan key.

        Jika key sudah ada, data lama akan diganti dengan data baru.
        """
        if self.akar is None:
            # Pohon kosong -> node baru langsung jadi akar
            self.akar = BSTNode(key, data)
            return

        # Pohon sudah ada -> cari posisi yang tepat secara rekursif
        self._sisipkan_rekursif(self.akar, key, data)

    def _sisipkan_rekursif(self, node_sekarang, key, data):
        """
        Proses internal: rekursif mencari posisi yang benar untuk node baru.

        Aturan:
          - Jika key baru < key node sekarang -> pergi ke KIRI
          - Jika key baru > key node sekarang -> pergi ke KANAN
          - Jika key sama -> update data (tidak boleh duplikat key)
        """
        if key < node_sekarang.key:
            # Key lebih kecil -> cari tempat di cabang kiri
            if node_sekarang.left is None:
                node_sekarang.left = BSTNode(key, data)     # Posisi kosong, langsung taruh
            else:
                self._sisipkan_rekursif(node_sekarang.left, key, data)  # Terus cari ke bawah

        elif key > node_sekarang.key:
            # Key lebih besar -> cari tempat di cabang kanan
            if node_sekarang.right is None:
                node_sekarang.right = BSTNode(key, data)
            else:
                self._sisipkan_rekursif(node_sekarang.right, key, data)

        else:
            # Key sama -> update saja datanya
            node_sekarang.data = data

    def cari(self, key):
        """
        Mencari node berdasarkan key.

        Mengembalikan node jika ditemukan, atau None jika tidak ada.
        """
        return self._cari_rekursif(self.akar, key)

    def _cari_rekursif(self, node_sekarang, key):
        """
        Proses internal: rekursif mencari node dengan key tertentu.
        """
        # Tidak ditemukan (sudah sampai ujung pohon)
        if node_sekarang is None:
            return None

        # Ditemukan!
        if key == node_sekarang.key:
            return node_sekarang

        # Cari ke kiri atau kanan berdasarkan perbandingan key
        if key < node_sekarang.key:
            return self._cari_rekursif(node_sekarang.left, key)
        else:
            return self._cari_rekursif(node_sekarang.right, key)

    def hapus(self, key):
        """
        Menghapus node dengan key tertentu dari BST.

        Mengembalikan data node yang dihapus, atau None jika tidak ditemukan.
        """
        self.akar, data_terhapus = self._hapus_rekursif(self.akar, key)
        return data_terhapus

    def _hapus_rekursif(self, node_sekarang, key):
        """
        Proses internal: rekursif menghapus node dan menjaga struktur BST tetap valid.

        Ada tiga kasus saat menghapus:
          1. Node tidak punya anak -> langsung hapus
          2. Node punya satu anak  -> ganti node dengan anaknya
          3. Node punya dua anak   -> ganti dengan node terkecil dari cabang kanan (successor)
        """
        if node_sekarang is None:
            return None, None   # Key tidak ditemukan

        if key < node_sekarang.key:
            # Key yang dicari ada di cabang kiri
            node_sekarang.left, data_terhapus = self._hapus_rekursif(node_sekarang.left, key)
            return node_sekarang, data_terhapus

        if key > node_sekarang.key:
            # Key yang dicari ada di cabang kanan
            node_sekarang.right, data_terhapus = self._hapus_rekursif(node_sekarang.right, key)
            return node_sekarang, data_terhapus

        # === Key ditemukan di node ini ===
        data_terhapus = node_sekarang.data

        # Kasus 1: Tidak punya anak kiri -> ganti dengan anak kanan (atau None)
        if node_sekarang.left is None:
            return node_sekarang.right, data_terhapus

        # Kasus 2: Tidak punya anak kanan -> ganti dengan anak kiri
        if node_sekarang.right is None:
            return node_sekarang.left, data_terhapus

        # Kasus 3: Punya dua anak -> cari node TERKECIL di cabang kanan (in-order successor)
        node_pengganti = self._cari_node_terkecil(node_sekarang.right)
        node_sekarang.key = node_pengganti.key
        node_sekarang.data = node_pengganti.data
        # Hapus node pengganti dari cabang kanan
        node_sekarang.right, _ = self._hapus_rekursif(node_sekarang.right, node_pengganti.key)

        return node_sekarang, data_terhapus

    def _cari_node_terkecil(self, node):
        """
        Proses internal: mencari node dengan key terkecil.

        Caranya: terus ke kiri sampai tidak ada lagi anak kiri.
        """
        node_sekarang = node
        while node_sekarang.left is not None:
            node_sekarang = node_sekarang.left
        return node_sekarang

    def tampilkan_inorder(self):
        """
        Mengembalikan semua isi BST dalam urutan MENAIK (inorder traversal).

        Inorder = kunjungi kiri -> root -> kanan.
        Hasilnya selalu terurut dari key terkecil ke terbesar.
        """
        hasil = []
        self._inorder_rekursif(self.akar, hasil)
        return hasil

    def _inorder_rekursif(self, node, hasil):
        """Proses internal: rekursif inorder traversal."""
        if node is not None:
            self._inorder_rekursif(node.left, hasil)    # Kunjungi kiri dulu
            hasil.append((node.key, node.data))         # Catat node ini
            self._inorder_rekursif(node.right, hasil)   # Kunjungi kanan

    def kosong(self):
        """Mengembalikan True jika BST kosong."""
        return self.akar is None

    def hitung_tinggi(self):
        """
        Menghitung tinggi pohon BST.

        Tinggi = jumlah level dari akar ke daun paling dalam.
        """
        return self._hitung_tinggi_rekursif(self.akar)

    def _hitung_tinggi_rekursif(self, node):
        """Proses internal: rekursif menghitung tinggi pohon."""
        if node is None:
            return 0
        tinggi_kiri = self._hitung_tinggi_rekursif(node.left)
        tinggi_kanan = self._hitung_tinggi_rekursif(node.right)
        return 1 + max(tinggi_kiri, tinggi_kanan)

    def hitung_node(self):
        """Menghitung total jumlah node dalam BST."""
        return self._hitung_node_rekursif(self.akar)

    def _hitung_node_rekursif(self, node):
        """Proses internal: rekursif menghitung jumlah node."""
        if node is None:
            return 0
        return 1 + self._hitung_node_rekursif(node.left) + self._hitung_node_rekursif(node.right)


# =============================================================================
# MODEL DATA: KENDARAAN
# Merepresentasikan satu kendaraan yang menggunakan sistem parkir.
# =============================================================================

class Kendaraan:
    """
    Merepresentasikan satu kendaraan di sistem parkir.

    Setiap kendaraan punya:
      - Nomor tiket unik
      - Plat nomor kendaraan
      - Jenis kendaraan (Mobil / Motor)
      - Status (VIP / Reguler)
      - Jam masuk parkir
      - Skor prioritas (dihitung otomatis)

    Kendaraan dengan skor prioritas LEBIH TINGGI akan diproses keluar lebih dulu.
    """

    def __init__(self, no_tiket: int, plat: str, jenis: str, status: str, jam_masuk: int):
        self.no_tiket = no_tiket
        self.plat = plat
        self.jenis = jenis
        self.status = status        # "VIP" atau "Reguler"
        self.jam_masuk = jam_masuk
        self.prioritas = self._hitung_prioritas()   # Dihitung otomatis saat kendaraan dibuat

    def _hitung_prioritas(self) -> int:
        """
        Menghitung skor prioritas kendaraan.

        Skor = skor_status + skor_jenis + skor_durasi

        Contoh perhitungan:
          Mobil VIP masuk jam 8    -> 120 + 50 + (8  x 10) = 250
          Motor Reguler masuk jam 14 -> 20 + 25 + (14 x 10) = 185
        """
        skor_status = SKOR_STATUS_VIP if self.status == "VIP" else SKOR_STATUS_REGULER
        skor_jenis = SKOR_JENIS_MOBIL if self.jenis == "Mobil" else SKOR_JENIS_MOTOR
        skor_durasi = self.jam_masuk * SKOR_PER_JAM_MASUK

        return skor_status + skor_jenis + skor_durasi

    def __str__(self) -> str:
        """Representasi teks kendaraan untuk ditampilkan di layar."""
        return (
            f"Tiket#{self.no_tiket:03d} | {self.plat:<10} | {self.jenis:<6} | "
            f"{self.status:<7} | Masuk:{self.jam_masuk:02d}:00 | Prioritas:{self.prioritas}"
        )


# =============================================================================
# LOGIKA UTAMA: SISTEM PARKIR
# Mengatur semua operasi parkir menggunakan keempat struktur data di atas.
# =============================================================================

class SistemParkir:
    """
    Pusat kendali sistem parkir.

    Menggabungkan Queue, BST, MaxHeap, dan Stack untuk:
      1. Mendaftarkan kendaraan yang datang    -> Queue
      2. Memproses kendaraan masuk parkir      -> Queue -> BST + Heap
      3. Mencari kendaraan berdasarkan tiket   -> BST
      4. Memproses kendaraan keluar            -> Heap -> BST -> Stack
      5. Membatalkan (undo) transaksi keluar   -> Stack -> BST + Heap
    """

    def __init__(self):
        self.antrian_masuk = Queue()            # Kendaraan yang menunggu giliran masuk
        self.parkir_aktif = BinarySearchTree()  # Kendaraan yang sedang parkir (dicari pakai tiket)
        self.antrian_keluar = MaxHeap()         # Urutan prioritas kendaraan yang akan keluar
        self.riwayat_transaksi = Stack()        # Histori transaksi (untuk fitur undo)
        self.nomor_tiket_berikutnya = 1         # Counter otomatis untuk nomor tiket

    def daftarkan_kendaraan(self, plat: str, jenis: str, status: str, jam_masuk: int):
        """
        Mendaftarkan kendaraan baru ke antrian masuk (Queue).

        Langkah:
          1. Buat objek Kendaraan baru dengan tiket unik
          2. Masukkan ke antrian (Queue)
          3. Tampilkan konfirmasi
        """
        kendaraan_baru = Kendaraan(
            no_tiket=self.nomor_tiket_berikutnya,
            plat=plat,
            jenis=jenis,
            status=status,
            jam_masuk=jam_masuk
        )
        self.nomor_tiket_berikutnya += 1    # Siapkan nomor tiket berikutnya

        self.antrian_masuk.tambah_ke_antrian(kendaraan_baru)
        print(
            f"[QUEUE] Kendaraan {plat} masuk antrian. "
            f"Tiket #{kendaraan_baru.no_tiket:03d} | Prioritas: {kendaraan_baru.prioritas}"
        )

    def proses_kendaraan_masuk(self):
        """
        Memproses kendaraan paling depan dari antrian masuk ke area parkir.

        Alur: Queue -> BST (simpan) + MaxHeap (catat prioritas)
        """
        if self.antrian_masuk.kosong():
            print("[QUEUE] Antrian masuk kosong. Tidak ada yang diproses.")
            return

        kendaraan = self.antrian_masuk.ambil_dari_depan()                        # Ambil dari depan antrian
        self.parkir_aktif.sisipkan(kendaraan.no_tiket, kendaraan)                # Simpan ke BST
        self.antrian_keluar.tambahkan((kendaraan.prioritas, kendaraan.no_tiket)) # Daftarkan ke Heap

        print(
            f"[QUEUE -> BST -> HEAP] Tiket#{kendaraan.no_tiket:03d} - "
            f"{kendaraan.plat} diproses masuk area parkir."
        )

    def cari_kendaraan(self, no_tiket: int):
        """
        Mencari kendaraan yang sedang parkir berdasarkan nomor tiket.

        Memanfaatkan BST untuk pencarian cepat.
        Mengembalikan objek Kendaraan jika ditemukan, atau None jika tidak ada.
        """
        node = self.parkir_aktif.cari(no_tiket)
        if node is not None:
            return node.data
        return None

    def proses_kendaraan_keluar(self):
        """
        Memproses kendaraan dengan PRIORITAS TERTINGGI untuk keluar dari parkir.

        Alur: MaxHeap (ambil prioritas tertinggi) -> BST (hapus) -> Stack (simpan ke riwayat)
        """
        if self.antrian_keluar.kosong():
            print("[HEAP] Tidak ada kendaraan yang sedang parkir.")
            return

        # Ambil kendaraan dengan prioritas tertinggi dari Heap
        prioritas, no_tiket = self.antrian_keluar.ambil_terbesar()

        # Hapus kendaraan dari BST (area parkir aktif)
        kendaraan = self.parkir_aktif.hapus(no_tiket)

        if kendaraan is not None:
            # Simpan ke riwayat transaksi (Stack) untuk keperluan undo
            self.riwayat_transaksi.simpan(kendaraan)
            print(
                f"[HEAP -> BST -> STACK] Tiket#{kendaraan.no_tiket:03d} - "
                f"{kendaraan.plat} keluar (prioritas:{prioritas}). Disimpan ke riwayat."
            )
        else:
            print(f"[ERROR] Tiket#{no_tiket} tidak ditemukan di area parkir.")

    def batalkan_transaksi_terakhir(self):
        """
        Membatalkan transaksi keluar terakhir (undo).

        Mengambil kendaraan terakhir dari riwayat (Stack),
        lalu mengembalikannya ke BST dan MaxHeap.

        Alur: Stack -> BST + MaxHeap
        """
        if self.riwayat_transaksi.kosong():
            print("[STACK] Tidak ada transaksi untuk dibatalkan.")
            return

        kendaraan = self.riwayat_transaksi.ambil_teratas()
        self.parkir_aktif.sisipkan(kendaraan.no_tiket, kendaraan)
        self.antrian_keluar.tambahkan((kendaraan.prioritas, kendaraan.no_tiket))

        print(
            f"[STACK -> BST -> HEAP] Undo berhasil: Tiket#{kendaraan.no_tiket:03d} - "
            f"{kendaraan.plat} dikembalikan ke area parkir."
        )

    # =========================================================================
    # METODE TAMPILAN — menampilkan isi masing-masing struktur data
    # =========================================================================

    def tampilkan_antrian_masuk(self):
        """Menampilkan semua kendaraan yang sedang menunggu di antrian masuk."""
        daftar_kendaraan = self.antrian_masuk.tampilkan_semua()

        print(f"\n{SEPARATOR}")
        print("  ANTRIAN MASUK (QUEUE - FIFO)")
        print(SEPARATOR)

        if not daftar_kendaraan:
            print("  (kosong)")
            return

        for nomor_urut, kendaraan in enumerate(daftar_kendaraan, start=1):
            print(f"  {nomor_urut:2d}. {kendaraan}")

        print(f"  Total: {len(daftar_kendaraan)} kendaraan menunggu")

    def tampilkan_parkir_aktif(self):
        """Menampilkan semua kendaraan yang sedang parkir, diurutkan berdasarkan nomor tiket."""
        daftar_kendaraan = self.parkir_aktif.tampilkan_inorder()

        print(f"\n{SEPARATOR}")
        print("  KENDARAAN PARKIR (BST - Inorder / Urut Tiket)")
        print(SEPARATOR)

        if not daftar_kendaraan:
            print("  (kosong)")
            return

        for _key, kendaraan in daftar_kendaraan:
            print(f"  {kendaraan}")

        print(f"  Total: {len(daftar_kendaraan)} kendaraan parkir")

    def tampilkan_urutan_prioritas(self):
        """Menampilkan urutan kendaraan berdasarkan prioritas keluar (tertinggi lebih dulu)."""
        semua_item = self.antrian_keluar.tampilkan_semua()

        print(f"\n{SEPARATOR}")
        print("  PRIORITAS KELUAR (MAX HEAP - Tertinggi Duluan)")
        print(SEPARATOR)

        if not semua_item:
            print("  (kosong)")
            return

        # Urutkan dari prioritas tertinggi ke terendah untuk tampilan
        terurut = sorted(semua_item, key=lambda item: item[0], reverse=True)

        for nomor_urut, (prioritas, no_tiket) in enumerate(terurut, start=1):
            node = self.parkir_aktif.cari(no_tiket)
            kendaraan = node.data if node else f"Unknown (Tiket #{no_tiket:03d})"
            print(f"  {nomor_urut:2d}. Prioritas:{prioritas:3d} | {kendaraan}")

        print(f"  Total: {len(semua_item)} kendaraan antri keluar")

    def tampilkan_riwayat_transaksi(self):
        """Menampilkan riwayat kendaraan yang sudah keluar (dari yang terbaru ke terlama)."""
        daftar_riwayat = self.riwayat_transaksi.tampilkan_semua()

        print(f"\n{SEPARATOR}")
        print("  RIWAYAT TRANSAKSI (STACK - LIFO / Terbaru Dulu)")
        print(SEPARATOR)

        if not daftar_riwayat:
            print("  (kosong)")
            return

        for nomor_urut, kendaraan in enumerate(daftar_riwayat, start=1):
            print(f"  {nomor_urut:2d}. {kendaraan}")

        print(f"  Total: {len(daftar_riwayat)} transaksi tersimpan")

    def tampilkan_ringkasan_sistem(self):
        """Menampilkan ringkasan jumlah kendaraan di setiap struktur data."""
        print(f"\n{SEPARATOR}")
        print("  RINGKASAN STATUS SISTEM PARKIR")
        print(SEPARATOR)
        print(f"  Queue (antrian masuk)      : {self.antrian_masuk.hitung_isi()} kendaraan")
        print(f"  BST   (parkir aktif)       : {self.parkir_aktif.hitung_node()} kendaraan")
        print(f"  Heap  (antrian keluar)     : {self.antrian_keluar.hitung_isi()} kendaraan")
        print(f"  Stack (riwayat transaksi)  : {self.riwayat_transaksi.hitung_isi()} kendaraan")

    def tampilkan_semua_kendaraan(self):
        """
        Menampilkan SEMUA kendaraan (antrian + parkir aktif + riwayat) dalam format tabel.

        Kendaraan dikelompokkan berdasarkan status (VIP / Reguler) agar mudah dibaca.
        """
        # Kumpulkan semua kendaraan dari ketiga sumber
        antrian    = self.antrian_masuk.tampilkan_semua()               # List Kendaraan
        parkir     = [k for _, k in self.parkir_aktif.tampilkan_inorder()]  # List Kendaraan
        riwayat    = self.riwayat_transaksi.tampilkan_semua()           # List Kendaraan

        # Tandai setiap kendaraan dengan lokasi saat ini
        semua = (
            [(k, "Antrian Masuk") for k in antrian] +
            [(k, "Parkir Aktif") for k in parkir]  +
            [(k, "Riwayat Keluar") for k in riwayat]
        )

        print(f"\n{SEPARATOR}")
        print("  SEMUA KENDARAAN — REKAP LENGKAP")
        print(SEPARATOR)

        if not semua:
            print("  (Belum ada kendaraan yang terdaftar di sistem)")
            return

        # Pisahkan ke dua kelompok: VIP dan Reguler
        kendaraan_vip     = [(k, lok) for k, lok in semua if k.status == "VIP"]
        kendaraan_reguler = [(k, lok) for k, lok in semua if k.status == "Reguler"]

        # Tampilkan masing-masing kelompok
        self._cetak_tabel_kendaraan("VIP", kendaraan_vip)
        self._cetak_tabel_kendaraan("REGULER", kendaraan_reguler)

        print(f"  Total keseluruhan: {len(semua)} kendaraan")
        print(f"  (VIP: {len(kendaraan_vip)} | Reguler: {len(kendaraan_reguler)})")

    @staticmethod
    def _cetak_tabel_kendaraan(label_kelompok: str, daftar: list):
        """
        Mencetak satu kelompok kendaraan dalam format tabel ASCII.

        Parameter:
          label_kelompok : judul grup, contoh 'VIP' atau 'REGULER'
          daftar         : list of tuple (Kendaraan, lokasi_string)
        """
        # Header kelompok
        print(f"\n  [ {label_kelompok} ]")

        # Baris header tabel
        header = (
            f"  {'No':>{LEBAR_NO}} "
            f"{'Tiket':<{LEBAR_TIKET}} "
            f"{'Plat':<{LEBAR_PLAT}} "
            f"{'Jenis':<{LEBAR_JENIS}} "
            f"{'Status':<{LEBAR_STATUS}} "
            f"{'Jam Masuk':<{LEBAR_JAM}} "
            f"{'Prioritas':>{LEBAR_PRIORITAS}} "
            f"{'Lokasi'}"
        )
        garis_tabel = "  " + "-" * (len(header) - 2)

        print(garis_tabel)
        print(header)
        print(garis_tabel)

        if not daftar:
            print(f"  {'(tidak ada)'}")
            print(garis_tabel)
            return

        # Baris data
        for nomor_urut, (kendaraan, lokasi) in enumerate(daftar, start=1):
            baris = (
                f"  {nomor_urut:>{LEBAR_NO}} "
                f"#{kendaraan.no_tiket:03d}{'':<{LEBAR_TIKET - 4}} "
                f"{kendaraan.plat:<{LEBAR_PLAT}} "
                f"{kendaraan.jenis:<{LEBAR_JENIS}} "
                f"{kendaraan.status:<{LEBAR_STATUS}} "
                f"{kendaraan.jam_masuk:02d}:00{'':<{LEBAR_JAM - 5}} "
                f"{kendaraan.prioritas:>{LEBAR_PRIORITAS}} "
                f"{lokasi}"
            )
            print(baris)

        print(garis_tabel)


# =============================================================================
# ANTARMUKA PENGGUNA: MENU
# Menampilkan menu interaktif dan menghubungkan pilihan pengguna ke SistemParkir.
# =============================================================================

class Menu:
    """
    Antarmuka teks (CLI) untuk berinteraksi dengan SistemParkir.

    Bertanggung jawab untuk:
      - Menampilkan menu
      - Membaca input pengguna
      - Memanggil metode yang sesuai di SistemParkir
    """

    def __init__(self):
        self.sistem = SistemParkir()    # Inisialisasi sistem parkir
        self._isi_data_dummy()          # Tambahkan 8 data dummy

    def _isi_data_dummy(self):
        """Mengisi sistem dengan 8 data kendaraan secara otomatis untuk demonstrasi."""
        data_awal = [
            # (Plat, Jenis, Status, Jam)
            ("B 1111 VIP", "Mobil", "VIP", 8),
            ("B 2222 REG", "Mobil", "Reguler", 9),
            ("B 3333 REG", "Motor", "Reguler", 10),
            ("B 4444 VIP", "Motor", "VIP", 7),
            ("D 5555 VIP", "Mobil", "VIP", 6),
            ("D 6666 REG", "Motor", "Reguler", 11),
            ("F 7777 REG", "Mobil", "Reguler", 12),
            ("L 8888 VIP", "Motor", "VIP", 8),
        ]
        
        # 1. Masukkan semua ke antrian (Queue)
        print("  [SYSTEM] Menambahkan 8 data dummy kendaraan...")
        for plat, jenis, status, jam in data_awal:
            # cukup panggil daftarkan_kendaraan (sudah include print)
            self.sistem.daftarkan_kendaraan(plat, jenis, status, jam)
            
        print("  [SYSTEM] Memproses beberapa kendaraan masuk dan keluar...")
        # 2. Pindahkan 6 dari 8 kendaraan ke area parkir (BST & Heap)
        for _ in range(6):
            self.sistem.proses_kendaraan_masuk()
            
        # 3. Keluarkan 2 kendaraan terprioritas agar masuk riwayat (Stack)
        for _ in range(2):
            self.sistem.proses_kendaraan_keluar()
            
        print("  [SYSTEM] Data dummy selesai disiapkan.\n")

    def jalankan(self):
        """Menjalankan loop utama program hingga pengguna memilih keluar."""
        while True:
            self._tampilkan_menu()

            pilihan = input("  Pilih menu (0-11): ").strip()

            if pilihan == '1':
                self._input_kendaraan_baru()

            elif pilihan == '2':
                self.sistem.proses_kendaraan_masuk()

            elif pilihan == '3':
                self.sistem.tampilkan_antrian_masuk()

            elif pilihan == '4':
                self._input_cari_kendaraan()

            elif pilihan == '5':
                self.sistem.proses_kendaraan_keluar()

            elif pilihan == '6':
                self.sistem.tampilkan_parkir_aktif()

            elif pilihan == '7':
                self.sistem.tampilkan_urutan_prioritas()

            elif pilihan == '8':
                self.sistem.batalkan_transaksi_terakhir()

            elif pilihan == '9':
                self.sistem.tampilkan_riwayat_transaksi()

            elif pilihan == '10':
                self.sistem.tampilkan_ringkasan_sistem()

            elif pilihan == '11':
                self.sistem.tampilkan_semua_kendaraan()

            elif pilihan == '0':
                print("\n  Terima kasih telah menggunakan sistem parkir. Sampai jumpa!")
                break

            else:
                print("  [!] Pilihan tidak valid. Masukkan angka 0-11.")

    def _tampilkan_menu(self):
        """
        Menampilkan menu utama dalam format tabel satu kolom agar rapi.
        """
        lebar_tabel = 76
        garis_menu = "+" + "-" * lebar_tabel + "+"
        
        def baris_satu(no, teks):
            """Membuat satu baris tabel yang rapi."""
            return f"|  {no:<4} | {teks:<66} |"

        print(f"\n{garis_menu}")
        print(f"|{'SISTEM MANAJEMEN PARKIR':^76}|")
        print(f"|{'Algoritma & Struktur Data - Menu Utama':^76}|")
        print(garis_menu)
        print(f"|  {'No':<4} | {'Aksi':<66} |")
        print(garis_menu)
        print(baris_satu('1.', 'Kendaraan Masuk (-> Queue)'))
        print(baris_satu('2.', 'Proses Antrian (Queue -> BST -> Heap)'))
        print(baris_satu('3.', 'Lihat Antrian Masuk (Queue)'))
        print(baris_satu('4.', 'Cari Kendaraan (BST)'))
        print(baris_satu('5.', 'Proses Keluar (Heap -> BST -> Stack)'))
        print(baris_satu('6.', 'Lihat Status Parkir (BST)'))
        print(baris_satu('7.', 'Lihat Prioritas Keluar (Heap)'))
        print(baris_satu('8.', 'Undo Transaksi Terakhir (Stack -> BST -> Heap)'))
        print(baris_satu('9.', 'Lihat Riwayat Transaksi (Stack)'))
        print(baris_satu('10.', 'Ringkasan Semua Struktur Data'))
        print(garis_menu)
        print(baris_satu('11.', 'Lihat Semua Kendaraan (Tabel VIP & Reguler)'))
        print(baris_satu('0.', 'Keluar'))
        print(garis_menu)

    @staticmethod
    def _input_angka(prompt, min_val=None, max_val=None):
        while True:
            try:
                nilai = int(input(f"  {prompt}").strip())
                if min_val is not None and nilai < min_val:
                    print(f"  [!] Nilai minimal {min_val}.")
                    continue
                if max_val is not None and nilai > max_val:
                    print(f"  [!] Nilai maksimal {max_val}.")
                    continue
                return nilai
            except ValueError:
                print("  [!] Masukkan angka yang valid.")

    @staticmethod
    def _input_pilihan(prompt, pilihan1, pilihan2):
        while True:
            pilihan = input(f"  {prompt}").strip()
            if pilihan == '1':
                return pilihan1
            if pilihan == '2':
                return pilihan2
            print(f"  [!] Pilih 1 untuk {pilihan1} atau 2 untuk {pilihan2}.")

    @staticmethod
    def _input_plat():
        while True:
            plat = input("  Plat nomor: ").strip().upper()
            if plat:
                return plat
            print("  [!] Plat nomor tidak boleh kosong.")

    def _input_kendaraan_baru(self):
        """Memandu pengguna memasukkan data kendaraan baru."""
        plat = self._input_plat()
        jenis = self._input_pilihan("Jenis kendaraan (1. Mobil / 2. Motor): ", "Mobil", "Motor")
        status = self._input_pilihan("Status kendaraan (1. VIP / 2. Reguler): ", "VIP", "Reguler")
        jam_masuk = self._input_angka("Jam masuk (0-23): ", 0, 23)

        self.sistem.daftarkan_kendaraan(plat, jenis, status, jam_masuk)

    def _input_cari_kendaraan(self):
        """Memandu pengguna mencari kendaraan berdasarkan nomor tiket."""
        no_tiket = self._input_angka("Nomor tiket yang dicari: ", 1)
        kendaraan = self.sistem.cari_kendaraan(no_tiket)

        if kendaraan is not None:
            print(f"  [BST] Ditemukan >> {kendaraan}")
        else:
            print(f"  [BST] Tiket#{no_tiket:03d} tidak ditemukan di area parkir.")


# =============================================================================
# ENTRY POINT
# Titik awal program. Hanya berjalan jika file ini dieksekusi langsung
# (bukan diimport oleh file lain).
# =============================================================================

if __name__ == "__main__":
    menu = Menu()
    menu.jalankan()
