import streamlit as st
from groq import Groq
from gtts import gTTS
import tempfile
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Tools Affiliate AI", layout="wide")

# Sidebar untuk API Key
with st.sidebar:
    st.header("⚙️ Pengaturan")
    api_key = st.text_input("Masukkan Groq API Key:", type="password")
    st.markdown("[Dapatkan API Key di sini](https://console.groq.com/keys)")
    st.info("Tips: Gunakan model 'Llama 3.3' untuk hasil terbaik.")

st.title("Tools Affiliate Gratis 🚀")

# --- BAGIAN 1: SCRIPT GENERATOR ---
st.header("1. Buat Script Jualan")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Nama Produk", placeholder="Contoh: Jaket Trucker Canvas")
    style = st.selectbox(
        "Gaya Bahasa", 
        ["Santai & Gaul (TikTok)", "Profesional & Elegan", "Storytelling (Bercerita)", "Hard Selling (To the point)"]
    )

with col2:
    features = st.text_area("Fitur/Kelebihan Produk", placeholder="Contoh: Bahan tebal, warna earth tone, cocok untuk outfit casual...", height=100)

if st.button("✨ Buat Script"):
    if not api_key:
        st.error("⚠️ Harap masukkan Groq API Key di menu sebelah kiri!")
    elif not product_name or not features:
        st.warning("⚠️ Harap isi Nama Produk dan Fitur terlebih dahulu.")
    else:
        try:
            # Inisialisasi Client Groq
            client = Groq(api_key=api_key)

            # Prompt untuk AI
            prompt_content = f"""
            Buatkan script konten video pendek (TikTok/Reels) untuk produk ini:
            Nama Produk: {product_name}
            Kelebihan: {features}
            
            Gaya Bahasa: {style}
            
            Pastikan scriptnya:
            1. Ada Hook yang menarik di awal.
            2. Menjelaskan manfaat produk.
            3. Ada Call to Action (CTA) yang jelas di akhir.
            4. Gunakan Bahasa Indonesia yang natural.
            """

            # Request ke API Groq (MENGGUNAKAN MODEL TERBARU)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt_content,
                    }
                ],
                model="llama-3.3-70b-versatile", # <--- INI BAGIAN YANG DIPERBAIKI
                temperature=0.7,
            )

            # Ambil hasil
            result_script = chat_completion.choices[0].message.content
            
            # Simpan ke session state agar tidak hilang saat reload
            st.session_state['generated_script'] = result_script
            
            st.success("Script berhasil dibuat!")

        except Exception as e:
            st.error(f"Terjadi Error: {e}")

# Tampilkan Hasil Script jika ada
if 'generated_script' in st.session_state:
    script_text = st.text_area("Hasil Script (Bisa diedit):", value=st.session_state['generated_script'], height=250)

    # --- BAGIAN 2: VOICE OVER (TTS) ---
    st.markdown("---")
    st.header("2. Buat Suara (Voice Over)")
    st.write("Ubah teks di atas menjadi suara natural.")
    
    lang_option = st.selectbox("Pilih Bahasa Suara:", ["Indonesia (id)", "Inggris (en)"])
    lang_code = "id" if "Indonesia" in lang_option else "en"

    if st.button("🔊 Generate Suara"):
        if script_text:
            try:
                # Menggunakan gTTS (Google Text-to-Speech)
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                
                # Simpan ke file sementara
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, format="audio/mp3")
                    st.success("Suara berhasil dibuat! Silakan putar atau download.")
            except Exception as e:
                st.error(f"Gagal membuat suara: {e}")
        else:
            st.warning("Belum ada script untuk diubah menjadi suara.")
