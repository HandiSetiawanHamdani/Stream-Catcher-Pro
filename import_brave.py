import os
import json
import re

def ekstrak_bookmark_brave():
    # Mengambil path profil user Windows kamu
    user_profile = os.environ.get('USERPROFILE')
    # Path default file bookmark Brave di Windows 10
    brave_path = os.path.join(user_profile, 'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Bookmarks')
    
    file_tujuan = "hosts_data.json"
    
    if not os.path.exists(brave_path):
        print(f"[ERROR] File bookmark Brave tidak ditemukan di: {brave_path}")
        return

    print("[INFO] Membaca file bookmark Brave...")
    with open(brave_path, 'r', encoding='utf-8') as f:
        brave_data = json.load(f)

    # Fungsi untuk mencari folder "bg" secara rekursif
    def cari_folder_bg(nodes):
        for node in nodes:
            if node['type'] == 'folder' and node['name'] == 'bg':
                return node.get('children', [])
            if node['type'] == 'folder' and 'children' in node:
                hasil = cari_folder_bg(node['children'])
                if hasil: return hasil
        return []

    # Mulai pencarian dari Bookmark Bar
    bookmark_bar = brave_data['roots']['bookmark_bar']['children']
    bg_children = cari_folder_bg(bookmark_bar)

    if not bg_children:
        print("[ERROR] Folder bernama 'bg' tidak ditemukan di Bookmark Bar Brave.")
        return

    # Load data host kita yang sudah ada (kalau ada)
    hosts_kita = []
    if os.path.exists(file_tujuan):
        with open(file_tujuan, 'r', encoding='utf-8') as f:
            try:
                hosts_kita = json.load(f)
            except json.JSONDecodeError:
                hosts_kita = []

    id_yang_sudah_ada = [h['id'] for h in hosts_kita]
    jumlah_ditambah = 0

    print(f"[INFO] Ditemukan {len(bg_children)} item di folder 'bg'. Memproses...\n")

    for item in bg_children:
        if item['type'] == 'url':
            url = item['url']
            raw_name = item['name']
            
            # Cek apakah ini link Bigo
            if 'bigo.tv' in url:
                # Membersihkan nama: Hapus "Watch ", " Live Stream on BIGO LIVE", dsb
                nama_bersih = re.sub(r'^Watch\s+', '', raw_name)
                nama_bersih = re.sub(r'\s+Live Stream on BIGO LIVE$', '', nama_bersih)
                nama_bersih = nama_bersih.strip()
                
                # Mengambil ID dari URL (biasanya setelah bigo.tv/)
                # Contoh: https://www.bigo.tv/syfaa98 -> syfaa98
                id_match = re.search(r'bigo\.tv/([^/?]+)', url)
                host_id = id_match.group(1) if id_match else "ID_Tidak_Diketahui"
                
                # Masukkan ke list kalau ID-nya belum ada di sistem kita
                if host_id not in id_yang_sudah_ada:
                    host_baru = {
                        "nama": nama_bersih,
                        "id": host_id,
                        "link": url,
                        "platform": "Bigo"
                    }
                    hosts_kita.append(host_baru)
                    id_yang_sudah_ada.append(host_id)
                    jumlah_ditambah += 1
                    print(f" [+] Ditambahkan: {nama_bersih} (@{host_id})")

    # Simpan kembali ke file JSON kita
    with open(file_tujuan, 'w', encoding='utf-8') as f:
        json.dump(hosts_kita, f, indent=4, ensure_ascii=False)

    print(f"\n[SUKSES] Proses selesai! {jumlah_ditambah} host baru berhasil diimpor.")

if __name__ == "__main__":
    ekstrak_bookmark_brave()