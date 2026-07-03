# Sistem Manajemen Parkir — Algoritma & Struktur Data

Program ini adalah simulasi sistem manajemen parkir yang mengimplementasikan empat struktur data fundamental: **Queue**, **Stack**, **Binary Search Tree (BST)**, dan **Max Heap**. Setiap kendaraan yang masuk diproses melalui antrian, disimpan di area parkir, diprioritaskan saat keluar, dan riwayat transaksinya dicatat.

## Struktur Data yang Digunakan

### 1. Node
Kelas dasar untuk linked list. Setiap node memiliki:
- `data` — nilai yang disimpan
- `next` — pointer ke node berikutnya

### 2. Queue (FIFO — First In, First Out)
Menggunakan linked list dengan pointer `front` (depan) dan `rear` (belakang).

| Method     | Deskripsi |
|------------|-----------|
| `enqueue`  | Tambah kendaraan ke belakang antrian |
| `dequeue`  | Ambil kendaraan dari depan antrian |
| `peek`     | Lihat kendaraan paling depan tanpa menghapus |
| `display`  | Kembalikan list seluruh antrian |
| `is_empty` | Cek apakah antrian kosong |
| `size`     | Hitung jumlah antrian |

**Digunakan untuk**: antrian kendaraan yang baru masuk.

### 3. Stack (LIFO — Last In, First Out)
Menggunakan linked list dengan pointer `top`.

| Method | Deskripsi |
|--------|-----------|
| `push`  | Tambah data ke atas stack |
| `pop`   | Ambil data dari atas stack |
| `peek`  | Lihat data paling atas |
| `display` | Kembalikan list seluruh stack |
| `is_empty` | Cek apakah stack kosong |
| `size`  | Hitung jumlah elemen |

**Digunakan untuk**: menyimpan riwayat transaksi keluar (untuk undo).

### 4. Binary Search Tree (BST)
Menyimpan data dengan key unik (nomor tiket). Setiap node BST (BSTNode) memiliki `key`, `data`, `left`, `right`.

| Method         | Deskripsi |
|----------------|-----------|
| `insert`       | Tambah node (rekursif) |
| `search`       | Cari node berdasarkan key |
| `delete`       | Hapus node (3 kasus: leaf, satu anak, dua anak) |
| `_min_value_node` | Cari node dengan key terkecil (inorder successor) |
| `inorder`      | Traversal kiri-akar-kanan, hasil list `(key, data)` |
| `is_empty`     | Cek apakah pohon kosong |

**Digunakan untuk**: menyimpan kendaraan yang sedang parkir, key = nomor tiket.

### 5. Max Heap
Implementasi heap dengan array. Elemen dengan prioritas tertinggi selalu di root (index 0). Elemen heap adalah tuple `(prioritas, no_tiket)`.

| Method         | Deskripsi |
|----------------|-----------|
| `insert`       | Tambah elemen lalu heapify up |
| `extract_max`  | Ambil elemen tertinggi lalu heapify down |
| `peek`         | Lihat elemen tertinggi tanpa menghapus |
| `_heapify_up`  | Bandingkan dengan parent, swap jika lebih besar |
| `_heapify_down`| Bandingkan dengan anak kiri/kanan, swap dengan yang terbesar |
| `display`      | Return salinan array heap |
| `is_empty`     | Cek apakah heap kosong |
| `size`         | Jumlah elemen di heap |

**Digunakan untuk**: prioritas keluar — kendaraan dengan prioritas tertinggi keluar lebih dulu.

### 6. Kelas Kendaraan
Menyimpan data kendaraan:
- `no_tiket`, `plat`, `jenis` (Mobil/Motor), `vip` (VIP/Reguler), `jam_masuk`
- `hitung_prioritas()`: rumus = skor_vip (120/20) + skor_jenis (50/25) + durasi (jam_masuk × 10)
- `__str__`: format output tabel

### 7. Kelas ParkirSystem — Integrasi Semua Struktur

| Method              | Alur Data |
|---------------------|-----------|
| `kendaraan_masuk`   | Input → **Queue** |
| `proses_antrian`    | **Queue** → dequeue → **BST** + **Heap** |
| `cari_kendaraan`    | Cari di **BST** |
| `proses_keluar`     | **Heap** (extract_max) → **BST** (delete) → **Stack** (push) |
| `undo_keluar`       | **Stack** (pop) → **BST** (insert) + **Heap** (insert) |
| `lihat_antrian_masuk` | Tampilkan **Queue** |
| `lihat_parkir_aktif` | Tampilkan **BST** (inorder) |
| `lihat_prioritas`   | Tampilkan **Heap** (urut descending) |
| `lihat_riwayat`     | Tampilkan **Stack** |
| `lihat_semua`       | Tampilkan ukuran semua struktur |

### Menu Program

```
 1. Kendaraan Masuk (>> Queue)
 2. Proses Antrian Masuk (Queue >> BST >> Heap)
 3. Lihat Antrian Masuk (Queue)
 4. Cari Kendaraan (BST)
 5. Proses Keluar (Heap >> BST >> Stack)
 6. Lihat Status Parkir (BST)
 7. Lihat Prioritas Keluar (Heap)
 8. Undo Transaksi Terakhir (Stack >> BST >> Heap)
 9. Lihat Riwayat Transaksi (Stack)
10. Status Semua Struktur Data
 0. Keluar
```

## Refactoring — SOLID Principles

Program ini telah di-refactor dari satu file `main.py` (441 baris) menjadi modul-modul terpisah yang mengikuti prinsip **SOLID**.

### Struktur Folder

```
algo/
├── main.py                         # Entry point (5 baris)
├── structures/                     # Data Structures
│   ├── __init__.py
│   ├── node.py                     # Node (linked list)
│   ├── bst_node.py                 # BSTNode (tree node)
│   ├── queue.py                    # Queue (FIFO)
│   ├── stack.py                    # Stack (LIFO)
│   ├── bst.py                      # BinarySearchTree
│   └── heap.py                     # MaxHeap
├── models/                         # Entity
│   ├── __init__.py
│   └── kendaraan.py                # Kendaraan + prioritas
└── services/                       # Business Logic
    ├── __init__.py
    ├── parkir_system.py            # Orchestrator
    └── menu.py                     # CLI Menu
```

### SOLID Mapping

| Prinsip | Penerapan |
|---------|-----------|
| **S**ingle Responsibility | Setiap file punya 1 tanggung jawab: `Queue` hanya urus queue, `Kendaraan` hanya data kendaraan, `Menu` hanya IO |
| **O**pen/Closed | Class seperti `Queue`, `Stack`, `BST`, `Heap` bisa di-extend tanpa memodifikasi class lain |
| **L**iskov | Semua struktur data bisa diganti implementasinya tanpa merusak `ParkirSystem` |
| **I**nterface Segregation | Method di tiap class spesifik sesuai kebutuhan masing-masing struktur data |
| **D**ependency Inversion | `ParkirSystem` tergantung pada abstraksi (`Queue`, `Stack`, `BST`, `Heap`), bukan implementasi detail |

## Cara Menjalankan

```bash
python main.py
```

## Contoh Alur

1. Input kendaraan (menu 1) → masuk **Queue**
2. Proses antrian (menu 2) → pindah ke **BST** & **Heap**
3. Proses keluar (menu 5) → **Heap** pilih prioritas tertinggi → hapus dari **BST** → simpan ke **Stack**
4. Undo (menu 8) → ambil dari **Stack** → kembalikan ke **BST** & **Heap**
5. Lihat status (menu 10) → tampilkan jumlah di tiap struktur
