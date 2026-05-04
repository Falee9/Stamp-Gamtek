import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
import os
import shutil

# --- FILE COPY WORKAROUND ---
impranet_src = r"C:\Users\naufa\.gemini\antigravity\brain\d0504333-3300-46f6-9b74-5df0686651a9\media__1776880913262.png"
impranet_dst = "Logo_Impranet.png"
if os.path.exists(impranet_src) and not os.path.exists(impranet_dst):
    try:
        shutil.copy(impranet_src, impranet_dst)
    except Exception:
        pass
# ----------------------------

# Set konfigurasi halaman Streamlit
st.set_page_config(page_title="Sistem Stamp Gamtek", page_icon="✨", layout="centered")

# --- CUSTOM CSS ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* TEMA GELAP BERBINTANG (Antigravity Style) */
        
        /* Background dasar dikosongkan karena canvas JS akan menggantikannya */
        .stApp {
            background-color: transparent !important;
        }
        
        /* Ubah semua teks default menjadi putih/terang */
        .stMarkdown, p, span, label, div[data-testid="stMarkdownContainer"] {
            color: #E0F2FE !important;
        }

        .header-container {
            background: linear-gradient(135deg, rgba(0,31,63,0.8) 0%, rgba(0,168,232,0.4) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px 20px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
            text-align: center;
        }
        .header-title {
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            margin-bottom: 5px;
            padding-bottom: 0;
            font-size: 2.2rem;
            text-shadow: 0 2px 10px rgba(0,168,232,0.5);
        }
        .header-subtitle {
            color: #87CEFA !important;
            font-weight: 600;
            font-size: 1.1rem;
            margin-top: 0;
        }
        
        /* Glassmorphism Form */
        div[data-testid="stForm"] {
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            background: rgba(255, 255, 255, 0.05); /* Transparan */
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        div[data-testid="stForm"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(0, 168, 232, 0.2);
            border: 1px solid rgba(0, 168, 232, 0.3);
        }
        
        .stButton>button, .stFormSubmitButton>button {
            background: linear-gradient(90deg, #001F3F 0%, #00A8E8 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0, 168, 232, 0.3);
        }
        .stButton>button:hover, .stFormSubmitButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 168, 232, 0.6);
            background: linear-gradient(90deg, #003366 0%, #00BFFF 100%);
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

def inject_wave_animation():
    components.html("""
    <script>
        const parentWindow = window.parent;
        const parentDoc = parentWindow.document;

        if (!parentDoc.getElementById('star-wave-canvas')) {
            // Hapus canvas lama jika ada
            let oldCanvas1 = parentDoc.getElementById('star-canvas');
            if (oldCanvas1) oldCanvas1.remove();
            let oldCanvas2 = parentDoc.getElementById('wave-canvas');
            if (oldCanvas2) oldCanvas2.remove();

            const canvas = parentDoc.createElement('canvas');
            canvas.id = 'star-wave-canvas';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '-999';
            canvas.style.pointerEvents = 'none';
            parentDoc.body.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            let w = canvas.width = parentWindow.innerWidth;
            let h = canvas.height = parentWindow.innerHeight;

            // Bintang-bintang
            const stars = [];
            const numStars = 1200; // Sangat banyak bintang bertabur

            for(let i = 0; i < numStars; i++) {
                stars.push({
                    x: Math.random() * w,
                    y: Math.random() * h,
                    baseY: Math.random() * h, // Posisi dasar Y
                    r: Math.random() * 1.5 + 0.5,
                    z: Math.random() * 0.8 + 0.2, // Kedalaman untuk efek parallax
                    phase: Math.random() * Math.PI * 2
                });
            }

            let mouseX = w / 2;
            let mouseY = h / 2;
            let targetMouseX = w / 2;
            let targetMouseY = h / 2;

            parentDoc.addEventListener('mousemove', (e) => {
                targetMouseX = e.clientX;
                targetMouseY = e.clientY;
            });

            let time = 0;

            function draw() {
                // Background gelap
                ctx.fillStyle = '#020b18';
                ctx.fillRect(0, 0, w, h);
                
                // Mouse lerp (Pergerakan kursor yang mulus)
                mouseX += (targetMouseX - mouseX) * 0.05;
                mouseY += (targetMouseY - mouseY) * 0.05;
                
                // Kecepatan dan tinggi ombak dipengaruhi oleh posisi Y kursor
                let waveSpeed = 0.02 + ((h - mouseY) / h) * 0.05; 
                let waveAmp = 20 + ((h - mouseY) / h) * 50;
                
                time += waveSpeed;

                stars.forEach(star => {
                    // Gerakan ombak (sine wave) utama
                    let waveOffset = Math.sin(star.x * 0.005 + time * star.z) * waveAmp * star.z;
                    
                    // Riak (ripple) tambahan yang berpusat di mouse kursor
                    let dx = mouseX - star.x;
                    let dy = mouseY - star.baseY; // hitung jarak ke base Y
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    let ripple = 0;
                    if (dist < 250) {
                        ripple = Math.sin(dist * 0.05 - time * 5) * (250 - dist) * 0.15;
                    }

                    // Bintang mengalir perlahan ke kiri seperti arus
                    let currentSpeedX = 0.2 + ((mouseX / w) * 1.5); // Kecepatan arus bergantung posisi X kursor
                    star.x -= currentSpeedX * star.z;
                    if (star.x < 0) {
                        star.x = w;
                        star.baseY = Math.random() * h; // Reset tinggi secara acak di sebelah kanan
                    }

                    let drawY = star.baseY + waveOffset + ripple;
                    
                    // Efek wrap around untuk Y jika melewati batas layar
                    if (drawY < -50) drawY += h + 100;
                    if (drawY > h + 50) drawY -= h + 100;

                    // Efek kelap-kelip dinamis
                    star.phase += 0.03;
                    let alpha = 0.3 + Math.sin(star.phase) * 0.5;
                    
                    ctx.beginPath();
                    ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                    ctx.arc(star.x, drawY, star.r, 0, Math.PI * 2);
                    ctx.fill();
                });
                
                requestAnimationFrame(draw);
            }
            draw();

            parentWindow.addEventListener('resize', () => {
                w = canvas.width = parentWindow.innerWidth;
                h = canvas.height = parentWindow.innerHeight;
            });
        }
    </script>
    """, height=0)

# Fungsi untuk membaca data Excel
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Data_Stamp.xlsx")
        # Bersihkan nama kolom dari spasi berlebih
        df.columns = df.columns.str.strip()
        
        # Pastikan kolom Kode dibaca sebagai string untuk mempermudah pencocokan
        if 'Kode' in df.columns:
            def clean_kode(x):
                if pd.isna(x): return ""
                s = str(x).strip()
                if s.endswith(".0"): s = s[:-2]
                return s
            df['Kode'] = df['Kode'].apply(clean_kode)
            
        return df
    except Exception as e:
        st.error(f"Gagal membaca file Data_Stamp.xlsx: {e}")
        return None

# Fungsi untuk membaca gambar sebagai base64 agar bisa digunakan di HTML/CSS
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

def main():
    inject_custom_css()
    inject_wave_animation()
    df = load_data()
    if df is None:
        return

    # Inisialisasi state untuk login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_data'] = None

    # --- LOGO SECTION ---
    logo_col1, logo_col2, logo_col3 = st.columns([1, 1.5, 1])
    with logo_col1:
        if os.path.exists("Logo_Impranet.png"):
            logo_impranet_b64 = get_image_base64("Logo_Impranet.png")
            if logo_impranet_b64:
                st.markdown(
                    f'<div style="background-color: white; padding: 10px; border-radius: 10px; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2); height: 120px;">'
                    f'<img src="data:image/png;base64,{logo_impranet_b64}" style="width: 100%; height: 100%; object-fit: contain;">'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            else:
                st.image("Logo_Impranet.png", use_container_width=True)
    with logo_col3:
        if os.path.exists("Logo Gamtek.png"):
            logo_gamtek_b64 = get_image_base64("Logo Gamtek.png")
            if logo_gamtek_b64:
                st.markdown(
                    f'<div style="background-color: white; padding: 10px; border-radius: 10px; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2); height: 120px;">'
                    f'<img src="data:image/png;base64,{logo_gamtek_b64}" style="width: 100%; height: 100%; object-fit: contain;">'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            else:
                st.image("Logo Gamtek.png", use_container_width=True)
            
    st.markdown("<hr style='border: 1px solid #E0F2FE; margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

    # --- HALAMAN LOGIN ---
    if not st.session_state['logged_in']:
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🔐 Portal Pengecekan Stamp</h1>
            <p class="header-subtitle">Laboratorium Gambar Teknik</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #001F3F; margin-bottom: 20px;'>Silakan masukkan <b>Kode</b> Anda untuk melihat progres stamp.</p>", unsafe_allow_html=True)
        
        # Form Login
        with st.form("login_form"):
            input_kode = st.text_input("Masukkan Kode", placeholder="Contoh: KODE123")
            submit_btn = st.form_submit_button("Login")
            
            if submit_btn:
                if input_kode:
                    input_kode = input_kode.strip()
                    # Cari user berdasarkan Kode
                    user_match = df[df['Kode'] == input_kode]
                    
                    if not user_match.empty:
                        st.session_state['logged_in'] = True
                        st.session_state['user_data'] = user_match.iloc[0]
                        st.rerun()
                    else:
                        st.error("❌ Kode tidak ditemukan. Pastikan Anda memasukkan kode yang benar.")
                else:
                    st.warning("⚠️ Harap masukkan Kode terlebih dahulu.")
                    
    # --- HALAMAN UTAMA (SETELAH LOGIN) ---
    else:
        user_data = st.session_state['user_data']
        
        # Ambil data Nama dan NPM (Gunakan .get() dengan default value jika kolom tidak ada)
        nama = user_data.get('Nama', 'Tidak Diketahui')
        npm = user_data.get('NPM', 'Tidak Diketahui')
        
        # Deteksi otomatis kolom untuk jumlah stamp (Total Stamp / Jumlah Stamp)
        stamp_col = None
        for col in df.columns:
            if 'stamp' in col.lower() or 'total' in col.lower() or 'jumlah' in col.lower():
                stamp_col = col
                if col.lower() == 'total stamp':
                    break # Prioritaskan jika namanya persis 'Total Stamp'
        
        total_stamp = 0
        if stamp_col and pd.notna(user_data[stamp_col]):
            try:
                total_stamp = int(user_data[stamp_col])
            except ValueError:
                total_stamp = 0

        # Header Profile
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🎉 Stamp Gamtek Anda</h1>
            <p class="header-subtitle">Dashboard Peserta Praktikum</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Nama:** {nama}")
            st.markdown(f"**NPM:** {npm}")
            st.markdown(f"**Total Stamp Terkumpul:** {total_stamp}")
        with col2:
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['user_data'] = None
                st.rerun()

        st.divider()
        st.subheader("Kartu Koleksi Stamp (5x6)")
        
        # Konversi logo ke base64
        logo_base64 = get_image_base64("Logo Gamtek.png")
        
        # Generate Tabel HTML (5 kolom x 6 baris)
        # Menggunakan HTML/CSS agar grid rapi dan stabil meskipun ukuran window berubah
        table_html = """
        <style>
            .stamp-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .stamp-cell {
                border: 2px dashed #00A8E8;
                width: 20%;
                height: 100px;
                text-align: center;
                vertical-align: middle;
                background-color: #F0F8FF;
                border-radius: 12px;
                transition: all 0.3s ease;
            }
            .stamp-cell:hover {
                background-color: #E0F2FE;
                border-color: #001F3F;
                box-shadow: 0 4px 8px rgba(0,168,232,0.2);
            }
            .stamp-image {
                max-width: 80%;
                max-height: 80px;
                object-fit: contain;
                animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            @keyframes popIn {
                0% { transform: scale(0); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }
            .empty-cell-number {
                color: #e0e0e0;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        <table class="stamp-table">
        """
        
        MAX_ROWS = 6
        MAX_COLS = 5
        MAX_CELLS = MAX_ROWS * MAX_COLS # 30 cells
        
        # Batasi jumlah stamp yang ditampilkan maksimal sebesar kapasitas tabel (30)
        stamps_to_show = min(total_stamp, MAX_CELLS)
        
        cell_count = 0
        for r in range(MAX_ROWS):
            table_html += "<tr>"
            for c in range(MAX_COLS):
                cell_count += 1
                table_html += "<td class='stamp-cell'>"
                
                if cell_count <= stamps_to_show:
                    if logo_base64:
                        img_src = f"data:image/png;base64,{logo_base64}"
                        table_html += f"<img src='{img_src}' class='stamp-image'>"
                    else:
                        table_html += "<b>✔️ Stamp</b>" # Fallback jika gambar tidak ada
                else:
                    # Sel kosong
                    table_html += f"<span class='empty-cell-number'>{cell_count}</span>"
                    
                table_html += "</td>"
            table_html += "</tr>"
            
        table_html += "</table>"
        
        # Render HTML ke dalam Streamlit
        st.markdown(table_html, unsafe_allow_html=True)
        
        if total_stamp > MAX_CELLS:
             st.info(f"Anda memiliki total {total_stamp} stamp. Tabel ini hanya menampilkan maksimum {MAX_CELLS} stamp.")

if __name__ == '__main__':
    main()
