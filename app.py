import streamlit as st
import json
import os
import subprocess
import shutil
import unicodedata
import requests
import math
import time
from datetime import datetime

# Import fungsi auto-import dari file sebelah
try:
    from import_brave import ekstrak_bookmark_brave
except ImportError:
    def ekstrak_bookmark_brave(): pass

# ==========================================
# 1. SETUP & THEME (CYBER-GLASS V8.8)
# ==========================================
st.set_page_config(page_title="Recorder Pro v8.8", page_icon="📡", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: radial-gradient(circle at top right, #0d1117, #161b22, #010409); color: #c9d1d9; }
    header[data-testid="stHeader"] {
        background-color: rgba(1, 4, 9, 0.95) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 3.5rem !important;
    }
    header[data-testid="stHeader"] svg { fill: #c9d1d9 !important; }
    header[data-testid="stHeader"] button[data-testid="stDeployButton"] {
        color: #c9d1d9 !important; background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; margin-right: 1.5rem !important;
    }
    header[data-testid="stHeader"] button[data-testid="stDeployButton"]:hover {
        border-color: #58a6ff !important; color: #58a6ff !important;
    }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 2rem !important; }
    [data-testid="stSidebar"] { background-color: rgba(1, 4, 9, 0.95) !important; border-right: 1px solid rgba(255, 255, 255, 0.1); }
    div[data-baseweb="input"] > div, .stSelectbox div[data-baseweb="select"] { 
        background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #30363d !important; 
    }
    input { color: #58a6ff !important; }
    .stButton > button {
        background-color: #21262d !important; color: #c9d1d9 !important;
        border: 1px solid #30363d !important; border-radius: 8px !important; transition: 0.3s;
    }
    .stButton > button:hover { border-color: #58a6ff !important; color: #58a6ff !important; }
    .btn-stop > button { background-color: #da3633 !important; color: white !important; font-weight: bold; border: none !important; }
    .btn-stop > button:hover { background-color: #ff5555 !important; color: white !important; }
    .host-card { 
        background: rgba(22, 27, 34, 0.8); border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; text-align: center; margin-bottom: 15px; position: relative; height: 160px;
    }
    .status-live { position: absolute; top: 8px; right: 8px; background: #238636; color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: bold; }
    .status-off { position: absolute; top: 8px; right: 8px; background: #444; color: #888; padding: 2px 6px; border-radius: 8px; font-size: 9px; }
    .avatar-circle {
        width: 50px; height: 50px; background: linear-gradient(135deg, #58a6ff, #21262d);
        color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        margin: 0 auto 10px auto; font-weight: bold; font-size: 18px; border: 2px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "hosts_data.json"
REC_FOLDER = "Hasil_Rekaman"

ekstrak_bookmark_brave()

# --- STATE MANAGEMENT ---
if 'is_any_recording' not in st.session_state: st.session_state.is_any_recording = False
if 'live_status' not in st.session_state: st.session_state.live_status = {}
if 'm3u8_val' not in st.session_state: st.session_state.m3u8_val = ""
if 'page_number' not in st.session_state: st.session_state.page_number = 0
if 'last_search' not in st.session_state: st.session_state.last_search = ""

# ==========================================
# 2. LOGIKA CORE
# ==========================================

def load_hosts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_hosts(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

def get_storage_free_gb():
    total, used, free = shutil.disk_usage("/")
    return free / (1024**3) 

def bersihkan_teks(teks):
    return unicodedata.normalize('NFKD', str(teks)).encode('ascii', 'ignore').decode('utf-8').lower()

def fetch_m3u8(url):
    if not url or not url.startswith("http"):
        return None
    try:
        res = subprocess.run(["streamlink", url, "best", "--stream-url"], capture_output=True, text=True, timeout=10)
        output = res.stdout.strip()
        if res.returncode == 0 and output.startswith("http"):
            return output
        return None
    except: return None

def check_link_status(url):
    try:
        r = requests.head(url, timeout=5)
        return "ONLINE" if r.status_code == 200 else "OFFLINE"
    except: return "ERROR"

def start_rec(host, link):
    if not os.path.exists(REC_FOLDER): os.makedirs(REC_FOLDER)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{REC_FOLDER}/[{host.get('platform', 'Bigo')}]_{host['id']}_{ts}.ts"
    cmd = f'ffmpeg -hide_banner -nostdin -i "{link}" -c copy "{filename}"'
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    st.session_state.is_any_recording = True
    return filename

def stop_recording():
    try:
        subprocess.run(["taskkill", "/IM", "ffmpeg.exe", "/T", "/F"], capture_output=True)
    except Exception as e:
        pass
    st.session_state.is_any_recording = False

def is_ffmpeg_running():
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq ffmpeg.exe" /NH', shell=True, text=True)
        return "ffmpeg.exe" in output
    except:
        return False

# ==========================================
# 3. INTERFACE (UI)
# ==========================================

st.sidebar.title("🎥 Recorder Pro v8.8")
menu = st.sidebar.radio("Navigasi", ["🏠 Dashboard", "🔴 Recording Studio", "⚙️ Kelola Host"])

st.sidebar.markdown("---")
free_space = get_storage_free_gb()
st.sidebar.metric("Sisa SSD", f"{free_space:.2f} GB")
st.sidebar.warning("⚠️ RAM 4GB detected. Tutup aplikasi lain saat recording aktif!")

if st.session_state.is_any_recording:
    if not is_ffmpeg_running():
        st.session_state.is_any_recording = False
        st.sidebar.success("✅ Rekaman telah selesai/terputus otomatis dari pusat.")
        time.sleep(2)
        st.rerun()
    else:
        st.sidebar.error("🔴 RECORDING ACTIVE")
        st.sidebar.markdown('<div class="btn-stop">', unsafe_allow_html=True)
        if st.sidebar.button("⏹️ STOP RECORDING", use_container_width=True):
            stop_recording()
            st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        if st.sidebar.button("🔄 Sinkronkan Status"):
            st.rerun()

hosts = load_hosts()

# --- MENU 1: DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("Main Radar")
    
    col_search, col_scan = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Cari Host (Nama atau ID)...", "")
        if search != st.session_state.last_search:
            st.session_state.page_number = 0
            st.session_state.last_search = search

    with col_scan:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Scan Status Live", use_container_width=True):
            with st.spinner("Scanning..."):
                for h in hosts:
                    try:
                        check = subprocess.run(["streamlink", h.get('link', ''), "--json"], capture_output=True, text=True, timeout=7)
                        st.session_state.live_status[h['id']] = "LIVE" if "streams" in check.stdout else "OFFLINE"
                    except: st.session_state.live_status[h['id']] = "OFFLINE"
            st.rerun()

    filtered_hosts = hosts
    if search:
        q = bersihkan_teks(search)
        filtered_hosts = [h for h in hosts if q in bersihkan_teks(h.get('nama', '')) or q in bersihkan_teks(h['id'])]

    items_per_page = 10
    total_pages = math.ceil(len(filtered_hosts) / items_per_page) if len(filtered_hosts) > 0 else 1
    
    if total_pages > 1:
        st.write(f"Halaman {st.session_state.page_number + 1} dari {total_pages}")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.session_state.page_number > 0:
                if st.button("⬅️ Sebelumnya", use_container_width=True):
                    st.session_state.page_number -= 1
                    st.rerun()
        with col_next:
            if st.session_state.page_number < total_pages - 1:
                if st.button("Berikutnya ➡️", use_container_width=True):
                    st.session_state.page_number += 1
                    st.rerun()

    start_idx = st.session_state.page_number * items_per_page
    end_idx = start_idx + items_per_page
    current_page_hosts = filtered_hosts[start_idx:end_idx]

    if not current_page_hosts:
        st.info("Host tidak ditemukan.")
    else:
        cols = st.columns(5)
        for i, h in enumerate(current_page_hosts):
            stts = st.session_state.live_status.get(h['id'], "OFFLINE")
            initial = h.get('nama', h['id'])[0].upper()
            with cols[i % 5]:
                st.markdown(f"""
                <div class="host-card">
                    <span class="{'status-live' if stts == 'LIVE' else 'status-off'}">{stts}</span>
                    <div class="avatar-circle">{initial}</div>
                    <div style="font-weight:bold; font-size:12px; overflow:hidden;">{h.get('nama', h['id'])}</div>
                    <div style="color:#8b949e; font-size:10px;">@{h['id']}</div>
                </div>
                """, unsafe_allow_html=True)

# --- MENU 2: RECORDING STUDIO ---
elif menu == "🔴 Recording Studio":
    st.title("Studio")
    if not hosts: st.error("Database Kosong!")
    else:
        col_input, col_info = st.columns([2, 1])
        
        with col_input:
            sel_host = st.selectbox("Pilih Target Host:", hosts, format_func=lambda h: f"{h.get('nama', h['id'])} (@{h['id']})")
            
            st.markdown(f"<div style='display:flex; align-items:center; gap:15px; background:rgba(255,255,255,0.05); padding:10px; border-radius:10px;'>"
                        f"<div class='avatar-circle' style='margin:0;'>{sel_host.get('nama', sel_host['id'])[0].upper()}</div>"
                        f"<div><b>{sel_host.get('nama', 'Unknown')}</b><br><small>@{sel_host['id']}</small><br>"
                        f"<a href='{sel_host.get('link', '#')}' target='_blank' style='color:#58a6ff; font-size:12px; text-decoration:none;'>🌐 Buka Profil di Browser</a></div></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            is_auto = st.toggle("🔄 Auto Fetch m3u8 via Streamlink", value=True)
            
            if st.button("🔗 Fetch / Ambil Link m3u8", use_container_width=True):
                with st.spinner("Fetching..."):
                    res = fetch_m3u8(sel_host.get('link', ''))
                    if res: 
                        st.session_state.m3u8_val = res
                        st.success("✅ Link didapatkan!")
                    else: 
                        st.error("❌ Gagal Fetch. Pastikan Link Profil terisi dan formatnya benar.")

            m3u8_input = st.text_input("Link m3u8:", value=st.session_state.m3u8_val)
            
            if not st.session_state.is_any_recording:
                if st.button("▶️ START RECORDING", type="primary", use_container_width=True, disabled=(not m3u8_input)):
                    with st.spinner("Memverifikasi link & storage..."):
                        if get_storage_free_gb() < 1.0:
                            st.error("⚠️ GAGAL: Sisa SSD di bawah 1GB! Harap kosongkan ruang terlebih dahulu.")
                        else:
                            link_status = check_link_status(m3u8_input)
                            if link_status != "ONLINE":
                                st.error(f"❌ GAGAL: Link mati atau error (Status: {link_status}). Host mungkin offline.")
                            else:
                                f = start_rec(sel_host, m3u8_input)
                                if f: 
                                    st.success(f"Berhasil! Merekam ke: {f}")
                                    st.rerun()
            else:
                st.warning("⚠️ Proses FFmpeg sedang merekam video di latar belakang.")
                st.markdown('<div class="btn-stop">', unsafe_allow_html=True)
                if st.button("⏹️ STOP RECORDING & SIMPAN VIDEO", use_container_width=True):
                    with st.spinner("Memutuskan koneksi dan menyimpan file video..."):
                        stop_recording()
                        time.sleep(1)
                        st.success("✅ Rekaman berhasil dihentikan! File video aman di folder Hasil_Rekaman.")
                        time.sleep(2)
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        with col_info:
            st.subheader("Opsi Cepat")
            if st.button("✅ Cek Link Nyala"):
                if m3u8_input:
                    s = check_link_status(m3u8_input)
                    st.write(f"Status: **{s}**")
                else: st.warning("Isi link dulu!")
            
            if st.button("📋 Copy untuk VLC"):
                if m3u8_input: st.code(m3u8_input); st.caption("Copy link di atas ke VLC.")

# --- MENU 3: KELOLA Host ---
elif menu == "⚙️ Kelola Host":
    st.title("Database")
    t1, t2, t3 = st.tabs(["➕ Tambah", "✏️ Edit", "🗑️ Hapus"])
    
    # ---------------- TAB TAMBAH ----------------
    with t1:
        with st.form("add"):
            n = st.text_input("Nama")
            i = st.text_input("ID")
            l = st.text_input("Link Profil (*Wajib)")
            
            # Tambahan Platform di form Tambah
            platforms = ["Bigo", "Tiktok", "YouTube", "Lainnya"]
            p = st.selectbox("Platform", platforms)
            av = st.text_input("Avatar URL (Optional)")
            
            if st.form_submit_button("Simpan"):
                if not n or not i or not l:
                    st.error("⚠️ Nama, ID, dan Link Profil WAJIB diisi!")
                else:
                    hosts.append({"nama": n, "id": i, "link": l, "platform": p, "avatar": av})
                    save_hosts(hosts)
                    st.success(f"✅ Host '{n}' berhasil ditambahkan ke database!")
                    time.sleep(1.5)
                    st.rerun()
                    
    # ---------------- TAB EDIT (SUPER LENGKAP) ----------------
    with t2:
        if hosts:
            h_ed = st.selectbox("Pilih Host yang mau diedit:", hosts, format_func=lambda x: f"{x.get('nama', x['id'])} (@{x['id']})", key="ed")
            with st.form("edit"):
                st.caption(f"Mengedit data milik: **{h_ed['id']}**")
                
                # Semua field dimunculkan dengan nilai default dari database
                en = st.text_input("Nama", h_ed.get('nama', ''))
                ei = st.text_input("ID", h_ed.get('id', ''))
                el = st.text_input("Link Profil", h_ed.get('link', ''))
                
                # Logic untuk menampilkan platform saat ini
                curr_plat = h_ed.get('platform', 'Bigo')
                platforms_edit = ["Bigo", "Tiktok", "YouTube", "Lainnya"]
                try:
                    plat_idx = platforms_edit.index(curr_plat)
                except ValueError:
                    plat_idx = 0
                    
                e_plat = st.selectbox("Platform", platforms_edit, index=plat_idx)
                e_av = st.text_input("Avatar URL (Optional)", h_ed.get('avatar', ''))
                
                if st.form_submit_button("Update Data"):
                    if not en or not ei or not el:
                        st.error("⚠️ Nama, ID, dan Link Profil tidak boleh kosong!")
                    else:
                        idx = hosts.index(h_ed)
                        hosts[idx].update({
                            "nama": en, 
                            "id": ei, 
                            "link": el,
                            "platform": e_plat,
                            "avatar": e_av
                        })
                        save_hosts(hosts)
                        st.success("✅ Data berhasil diupdate ke database!")
                        time.sleep(1)
                        st.rerun()
                        
    # ---------------- TAB HAPUS ----------------
    with t3:
        if hosts:
            h_dl = st.selectbox("Pilih Host yang mau dihapus:", hosts, format_func=lambda x: f"{x.get('nama', x['id'])} (@{x['id']})", key="dl")
            if st.button("❌ KONFIRMASI DELETE"):
                hosts.remove(h_dl)
                save_hosts(hosts)
                st.success("✅ Host berhasil dihapus dari sistem!")
                time.sleep(1)
                st.rerun()

st.markdown("---")
with st.expander("📝 Catatan Penting (v8.8 Complete Editor)"):
    st.write("**Workflow Terbaik:** Gunakan Auto Fetch dulu. Jika gagal, klik link profil untuk buka Brave, lalu ambil link m3u8 manual.")
    st.write("**Editor Lengkap:** Di menu Kelola Host -> Edit, kamu sekarang bisa memodifikasi semua data termasuk Platform dan Avatar.")