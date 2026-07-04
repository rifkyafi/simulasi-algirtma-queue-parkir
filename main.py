class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class BSTNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def peek(self):
        if self.front is None:
            return None
        return self.front.data

    def display(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        return self.front is None

    def size(self):
        count = 0
        current = self.front
        while current:
            count += 1
            current = current.next
        return count


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        temp = self.top
        self.top = self.top.next
        return temp.data

    def peek(self):
        if self.top is None:
            return None
        return self.top.data

    def display(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        return self.top is None

    def size(self):
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count


class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        max_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_item

    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]

    def _heapify_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx][0] > self.heap[parent][0]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._heapify_up(parent)

    def _heapify_down(self, idx):
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
            largest = left
        if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
            largest = right
        if largest != idx:
            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            self._heapify_down(largest)

    def display(self):
        return self.heap[:]

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = BSTNode(key, data)
            return
        self._insert_rec(self.root, key, data)

    def _insert_rec(self, node, key, data):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, data)
            else:
                self._insert_rec(node.left, key, data)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, data)
            else:
                self._insert_rec(node.right, key, data)
        else:
            node.data = data

    def search(self, key):
        return self._search_rec(self.root, key)

    def _search_rec(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._search_rec(node.left, key)
        return self._search_rec(node.right, key)

    def delete(self, key):
        self.root, deleted = self._delete_rec(self.root, key)
        return deleted

    def _delete_rec(self, node, key):
        if node is None:
            return None, None
        if key < node.key:
            node.left, deleted = self._delete_rec(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete_rec(node.right, key)
            return node, deleted
        deleted = node.data
        if node.left is None:
            return node.right, deleted
        if node.right is None:
            return node.left, deleted
        min_node = self._min_value_node(node.right)
        node.key = min_node.key
        node.data = min_node.data
        node.right, _ = self._delete_rec(node.right, min_node.key)
        return node, deleted

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        result = []
        self._inorder_rec(self.root, result)
        return result

    def _inorder_rec(self, node, result):
        if node:
            self._inorder_rec(node.left, result)
            result.append((node.key, node.data))
            self._inorder_rec(node.right, result)

    def is_empty(self):
        return self.root is None

    def height(self):
        return self._height_rec(self.root)

    def _height_rec(self, node):
        if node is None:
            return 0
        left_height = self._height_rec(node.left)
        right_height = self._height_rec(node.right)
        return 1 + max(left_height, right_height)

    def node_count(self):
        return self._node_count_rec(self.root)

    def _node_count_rec(self, node):
        if node is None:
            return 0
        return 1 + self._node_count_rec(node.left) + self._node_count_rec(node.right)


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
        bst_size = self.parkir_aktif.node_count()
        h_size = self.prioritas_keluar.size()
        s_size = self.riwayat.size()
        print(f"  Queue (antrian masuk)     : {q_size} kendaraan")
        print(f"  BST   (parkir aktif)      : {bst_size} kendaraan")
        print(f"  Heap  (prioritas keluar)  : {h_size} kendaraan")
        print(f"  Stack (riwayat transaksi) : {s_size} kendaraan")


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


if __name__ == "__main__":
    menu = Menu()
    menu.run()
