import streamlit as st
import os
from groq import Groq
import asyncio
import edge_tts

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tools Affiliate Gratis", page_icon="🚀")

# --- JUDUL & TAMPILAN ---
st.title("🚀 AI Content Generator (Versi Gratis)")
st.write("Buat Script & Voice Over untuk Affiliate TikTok/Shopee tanpa biaya bulanan.")

# --- SIDEBAR: PENGATURAN ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    api_key = st.text_input("Masukkan Groq API Key:", type="password", help="Dapatkan gratis di console.groq.com")
    st.info("Tips: Gunakan model 'Llama3' untuk hasil terbaik.")

# --- FUNGSI 1: GENERATE SCRIPT ---
st.header("1. Buat Script Jualan")
produk = st.text_input("Nama Produk:", placeholder="Contoh: Botol Minum Viral 2 Liter")
fitur = st.text_area("Fitur/Kelebihan Produk:", placeholder="Contoh: Tahan dingin, anti tumpah, ada sedotan, warna pastel")
gaya_bahasa = st.selectbox("Gaya Bahasa:", ["Santai & Gaul (TikTok)", "Formal & Elegan", "Hard Selling (To the point)"])

if st.button("✨ Buat Script"):
    if not api_key:
        st.error("Harap masukkan API Key Groq di sidebar dulu ya!")
    else:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        Buatkan script video pendek (durasi 15-30 detik) untuk mempromosikan produk: {produk}.
        Fitur utamanya: {fitur}.
        Gunakan gaya bahasa: {gaya_bahasa}.
        Buat formatnya langsung siap baca (Voice Over) tanpa instruksi scene visual yang rumit.
        Gunakan Bahasa Indonesia yang natural.
        """
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192", # Model gratis dari Groq
            )
            script_hasil = chat_completion.choices[0].message.content
            st.session_state['script_final'] = script_hasil # Simpan hasil
            st.success("Script berhasil dibuat!")
        except Exception as e:
            st.error(f"Error: {e}")

# Tampilkan Script jika sudah ada
script_text = st.text_area("Hasil Script (Bisa diedit):", value=st.session_state.get('script_final', ""), height=200)

# --- FUNGSI 2: VOICE OVER (TTS) ---
st.header("2. Buat Suara (Voice Over)")
st.write("Ubah teks di atas menjadi suara natural.")

voice_option = st.selectbox("Pilih Suara:", [
    "id-ID-GadisNeural-Female", # Suara Cewek Indonesia
    "id-ID-ArdiNeural-Male"     # Suara Cowok Indonesia
])

async def generate_voice(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

if st.button("🔊 Generate Audio"):
    if not script_text:
        st.warning("Script masih kosong. Buat dulu di atas atau ketik manual.")
    else:
        with st.spinner("Sedang memproses suara..."):
            output_file = "voiceover.mp3"
            try:
                asyncio.run(generate_voice(script_text, voice_option, output_file))
                st.audio(output_file)
                st.success("Audio selesai! Klik titik tiga di player untuk download.")
            except Exception as e:
                st.error(f"Gagal membuat suara: {e}")

# --- CREDIT ---
st.markdown("---")
st.caption("Dibuat dengan Streamlit, Groq, & Edge-TTS. 100% Gratis.")
