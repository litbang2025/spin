import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import random
import time
from io import StringIO

st.set_page_config(page_title="🎡 Spin Nama Interaktif", layout="centered")

# --- Session State ---
if "daftar_nama" not in st.session_state:
    st.session_state.daftar_nama = []
if "nama_keluar" not in st.session_state:
    st.session_state.nama_keluar = []
if "terpilih" not in st.session_state:
    st.session_state.terpilih = None

# --- Sidebar Menu ---
with st.sidebar:
    selected = option_menu(
        menu_title="📋 Menu",
        options=["Input Nama", "Spin Nama", "Hasil", "Reset"],
        icons=["pencil", "shuffle", "list-task", "arrow-clockwise"],
        default_index=0,
    )

st.markdown("<h1 style='text-align: center;'>🎡 Spin Nama Interaktif</h1>", unsafe_allow_html=True)

# --- Input Nama ---
if selected == "Input Nama":
    st.subheader("📝 Masukkan Daftar Nama")

    input_nama = st.text_area("Atau ketik langsung (pisahkan dengan koma):", "Ali, Budi, Cici")

    uploaded_file = st.file_uploader("📁 Atau upload file .csv/.txt", type=['csv', 'txt'])
    daftar_file = []

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, header=None)
            daftar_file = df.iloc[:, 0].dropna().astype(str).tolist()
        elif uploaded_file.name.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8")
            daftar_file = [x.strip() for x in content.splitlines() if x.strip()]

    if st.button("✅ Muat Daftar"):
        manual_list = [n.strip() for n in input_nama.split(",") if n.strip()]
        all_names = list(set(manual_list + daftar_file))
        if len(all_names) < 2:
            st.error("Minimal 2 nama diperlukan.")
        else:
            st.session_state.daftar_nama = all_names
            st.session_state.nama_keluar = []
            st.session_state.terpilih = None
            st.success(f"{len(all_names)} nama dimuat!")

# --- Spin Nama ---
elif selected == "Spin Nama":
    st.subheader("🔄 Spin Sekarang")

    if not st.session_state.daftar_nama:
        st.warning("🚨 Belum ada nama. Silakan input di menu sebelumnya.")
    else:
        tersisa = list(set(st.session_state.daftar_nama) - set(st.session_state.nama_keluar))

        if tersisa:
            if st.button("🎰 Spin Sekarang"):
                with st.status("🎡 Sedang memutar roda...", expanded=True):
                    for i in range(25):  # Simulasi putaran
                        nama_acak = random.choice(tersisa)
                        st.write(f"🔁 {nama_acak}")
                        time.sleep(0.07)

                terpilih = random.choice(tersisa)
                st.session_state.nama_keluar.append(terpilih)
                st.session_state.terpilih = terpilih
                st.success(f"🎉 Nama yang keluar: **{terpilih}**")

                st.balloons()
        else:
            st.info("✅ Semua nama sudah keluar!")

# --- Hasil ---
elif selected == "Hasil":
    st.subheader("📊 Hasil Spin")

    if st.session_state.nama_keluar:
        st.markdown("### 🏁 Urutan Nama yang Keluar:")
        for i, nama in enumerate(st.session_state.nama_keluar, 1):
            st.markdown(f"{i}. **{nama}**")

        sisa = list(set(st.session_state.daftar_nama) - set(st.session_state.nama_keluar))
        if sisa:
            st.markdown("### 👥 Nama Belum Keluar:")
            st.write(", ".join(sorted(sisa)))

        hasil_str = "\n".join([f"{i}. {n}" for i, n in enumerate(st.session_state.nama_keluar, 1)])
        st.download_button("⬇️ Unduh Hasil", data=hasil_str, file_name="hasil_spin.txt", mime="text/plain")
    else:
        st.info("🚫 Belum ada hasil.")

# --- Reset ---
elif selected == "Reset":
    st.subheader("♻️ Reset Semua Data")
    if st.button("🔄 Reset Aplikasi"):
        st.session_state.daftar_nama = []
        st.session_state.nama_keluar = []
        st.session_state.terpilih = None
        st.success("✅ Data berhasil direset.")

# Footer
st.markdown("---")
st.caption("📁 More Apps: [Home Digital](https://www.stimulasi.my.id/apps-store)")
st.caption("📞 Hubungi kami di WhatsApp: [WhatsApp](https://wa.me/6285640375704)")  # Ganti dengan nomor WhatsApp yang sesuai
st.caption("© 2025 Home Digital - A3SA.")
