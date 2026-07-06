# Sistem Manajemen Parkir — Algoritma & Struktur Data

Program ini adalah simulasi sistem manajemen parkir yang mengimplementasikan empat struktur data fundamental: **Queue**, **Stack**, **Binary Search Tree (BST)**, dan **Max Heap**. Setiap kendaraan yang masuk diproses melalui antrian, disimpan di area parkir, diprioritaskan saat keluar, dan riwayat transaksinya dicatat. Program ditulis dengan prinsip **clean code** agar mudah dipahami.

---

## Struktur Data yang Digunakan

### 1. `Node`
Kelas dasar untuk linked list yang dipakai oleh `Queue` dan `Stack`.

| Atribut | Deskripsi |
|---------|-----------|
| `data`  | Nilai/muatan yang disimpan di dalam node |
| `next`  | Penunjuk ke node berikutnya (`None` = node terakhir) |

---

### 2. `Queue` — Antrian (FIFO: First In, First Out)
Menggunakan linked list dengan pointer `front` (depan) dan `rear` (belakang).
Kendaraan yang **pertama masuk** akan **pertama diproses**.

| Method                | Deskripsi |
|-----------------------|-----------|
| `tambah_ke_antrian`   | Tambah kendaraan ke belakang antrian |
| `ambil_dari_depan`    | Ambil & hapus kendaraan paling depan |
| `lihat_depan`         | Lihat kendaraan paling depan tanpa menghapus |
| `tampilkan_semua`     | Kembalikan list seluruh isi antrian |
| `kosong`              | Cek apakah antrian kosong |
| `hitung_isi`          | Hitung jumlah kendaraan dalam antrian |

**Digunakan untuk**: antrian kendaraan yang baru datang dan menunggu masuk area parkir.

---

### 3. `Stack` — Tumpukan (LIFO: Last In, First Out)
Menggunakan linked list dengan pointer `puncak`.
Data yang **terakhir dimasukkan** akan **pertama diambil**.

| Method         | Deskripsi |
|----------------|-----------|
| `simpan`       | Simpan data baru ke puncak tumpukan |
| `ambil_teratas`| Ambil & hapus data dari puncak tumpukan |
| `lihat_teratas`| Lihat data puncak tanpa menghapus |
| `tampilkan_semua` | Kembalikan list seluruh isi tumpukan |
| `kosong`       | Cek apakah tumpukan kosong |
| `hitung_isi`   | Hitung jumlah elemen dalam tumpukan |

**Digunakan untuk**: menyimpan riwayat transaksi keluar, sehingga bisa di-*undo*.

---

### 4. `BinarySearchTree` (BST)
Pohon pencarian biner yang menyimpan kendaraan dengan key unik (nomor tiket).
Setiap node (`BSTNode`) memiliki atribut: `key`, `data`, `left`, `right`.

```
Contoh BST dengan tiket [5, 3, 7, 1, 4]:
      5
     / \
    3   7
   / \
  1   4
```

| Method                  | Deskripsi |
|-------------------------|-----------|
| `sisipkan`              | Tambah node baru (rekursif) |
| `cari`                  | Cari node berdasarkan key (nomor tiket) |
| `hapus`                 | Hapus node (3 kasus: tanpa anak, satu anak, dua anak) |
| `_cari_node_terkecil`   | Cari node dengan key terkecil (inorder successor) |
| `tampilkan_inorder`     | Traversal kiri→akar→kanan, hasil terurut menaik |
| `kosong`                | Cek apakah pohon kosong |
| `hitung_tinggi`         | Hitung tinggi pohon secara rekursif |
| `hitung_node`           | Hitung total jumlah node secara rekursif |

**Digunakan untuk**: menyimpan kendaraan yang sedang parkir, dengan key = nomor tiket.

---

### 5. `MaxHeap`
Implementasi heap dengan Python list. Elemen dengan **prioritas tertinggi** selalu berada di posisi pertama (index 0). Setiap elemen berupa tuple `(prioritas, no_tiket)`.

| Method          | Deskripsi |
|-----------------|-----------|
| `tambahkan`     | Tambah elemen lalu jalankan `_naikkan` |
| `ambil_terbesar`| Ambil elemen prioritas tertinggi lalu jalankan `_turunkan` |
| `lihat_terbesar`| Lihat elemen tertinggi tanpa menghapus |
| `_naikkan`      | Proses internal: naikkan elemen sampai heap valid |
| `_turunkan`     | Proses internal: turunkan elemen sampai heap valid |
| `tampilkan_semua` | Kembalikan salinan list heap |
| `kosong`        | Cek apakah heap kosong |
| `hitung_isi`    | Hitung jumlah elemen di heap |

**Digunakan untuk**: menentukan urutan prioritas keluar — kendaraan dengan skor tertinggi keluar lebih dulu.

---

### 6. Kelas `Kendaraan`
Merepresentasikan satu kendaraan dalam sistem parkir.

| Atribut     | Deskripsi |
|-------------|-----------|
| `no_tiket`  | Nomor tiket unik (otomatis dari counter) |
| `plat`      | Plat nomor kendaraan |
| `jenis`     | `"Mobil"` atau `"Motor"` |
| `status`    | `"VIP"` atau `"Reguler"` |
| `jam_masuk` | Jam kedatangan (0–23) |
| `prioritas` | Skor prioritas (dihitung otomatis) |

**Rumus prioritas:**
```
prioritas = skor_status + skor_jenis + (jam_masuk × 10)

skor_status : VIP = 120, Reguler = 20
skor_jenis  : Mobil = 50, Motor = 25
```

> Semua angka skor disimpan sebagai **konstanta bernama** (`SKOR_STATUS_VIP`, `SKOR_JENIS_MOBIL`, dst.) agar mudah diubah.

---

### 7. Kelas `SistemParkir` — Integrasi Semua Struktur

| Method                       | Alur Data |
|------------------------------|-----------|
| `daftarkan_kendaraan`        | Input → **Queue** |
| `proses_kendaraan_masuk`     | **Queue** → ambil dari depan → **BST** + **Heap** |
| `cari_kendaraan`             | Cari di **BST** berdasarkan nomor tiket |
| `proses_kendaraan_keluar`    | **Heap** (ambil terbesar) → **BST** (hapus) → **Stack** (simpan) |
| `batalkan_transaksi_terakhir`| **Stack** (ambil teratas) → **BST** (sisipkan) + **Heap** (tambahkan) |
| `tampilkan_antrian_masuk`    | Tampilkan isi **Queue** |
| `tampilkan_parkir_aktif`     | Tampilkan isi **BST** (inorder, urut tiket) |
| `tampilkan_urutan_prioritas` | Tampilkan isi **Heap** (urut prioritas tertinggi) |
| `tampilkan_riwayat_transaksi`| Tampilkan isi **Stack** (terbaru ke terlama) |
| `tampilkan_ringkasan_sistem` | Tampilkan jumlah kendaraan di tiap struktur |
| `tampilkan_semua_kendaraan`  | Tampilkan **semua kendaraan** dalam tabel, dikelompokkan VIP & Reguler |

---

## Menu Program

Menu utama ditampilkan dalam **format tabel dua kolom**:

```
+------------------------------------------------------------------------------+
|                    SISTEM MANAJEMEN PARKIR                                   |
|             Algoritma & Struktur Data - Menu Utama                           |
+--------------------------------------+--------------------------------------+
|  No  Aksi                           |  No  Aksi                            |
+--------------------------------------+--------------------------------------+
|  1.  Kendaraan Masuk (-> Queue)     |  6.  Lihat Status Parkir (BST)       |
|  2.  Proses Antrian (Queue->BST->.. |  7.  Lihat Prioritas Keluar (Heap)   |
|  3.  Lihat Antrian Masuk (Queue)    |  8.  Undo Transaksi (Stack->BST->..  |
|  4.  Cari Kendaraan (BST)           |  9.  Lihat Riwayat Transaksi (Stack) |
|  5.  Proses Keluar (Heap->BST->..   |  10. Ringkasan Struktur Data         |
+--------------------------------------+--------------------------------------+
|  11.  Lihat Semua Kendaraan (Tabel VIP & Reguler)                           |
|  0.   Keluar                                                                 |
+------------------------------------------------------------------------------+
```

| No  | Fungsi |
|-----|--------|
| 1   | Daftarkan kendaraan baru ke antrian masuk |
| 2   | Proses satu kendaraan dari antrian ke area parkir |
| 3   | Lihat antrian masuk (Queue) |
| 4   | Cari kendaraan berdasarkan nomor tiket (BST) |
| 5   | Proses kendaraan prioritas tertinggi keluar |
| 6   | Lihat kendaraan yang sedang parkir (BST inorder) |
| 7   | Lihat urutan prioritas keluar (MaxHeap) |
| 8   | Batalkan transaksi keluar terakhir (Undo via Stack) |
| 9   | Lihat riwayat transaksi keluar (Stack) |
| 10  | Ringkasan jumlah kendaraan di setiap struktur data |
| 11  | **Lihat semua kendaraan dalam tabel, dikelompokkan VIP & Reguler** |
| 0   | Keluar dari program |

---

## Struktur Kode

Semua kode program digabung dalam satu file `main.py`. Urutan definisi kelas:

| Lapisan | Kelas | Peran |
|---------|-------|-------|
| Struktur Data | `Node`, `BSTNode` | Blok dasar linked list & BST |
| Struktur Data | `Queue`, `Stack`, `MaxHeap`, `BinarySearchTree` | Implementasi struktur data |
| Model | `Kendaraan` | Representasi entitas kendaraan |
| Logika | `SistemParkir` | Mengintegrasikan semua struktur data |
| Antarmuka | `Menu` | Tampilan CLI & routing input pengguna |

---

## Cara Menjalankan

```bash
python main.py
```

---

## Contoh Alur Penggunaan

1. **Daftarkan kendaraan** (menu `1`) → kendaraan masuk ke **Queue**
2. **Proses antrian** (menu `2`) → kendaraan pindah dari **Queue** ke **BST** & **Heap**
3. **Cari kendaraan** (menu `4`) → BST mencari berdasarkan nomor tiket
4. **Proses keluar** (menu `5`) → **Heap** memilih prioritas tertinggi → hapus dari **BST** → simpan ke **Stack**
5. **Undo** (menu `8`) → ambil dari **Stack** → kembalikan ke **BST** & **Heap**
6. **Lihat semua** (menu `11`) → tabel lengkap semua kendaraan, dikelompokkan **VIP** dan **Reguler**
