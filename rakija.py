import streamlit as st
from datetime import datetime
import math
import base64
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Rakija Master Pro", page_icon="🥃", layout="centered")

# --- INICIJALIZACIJA SESIJE ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'
if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik = []

# --- CSS FIX ZA SAKRIVANJE IKONICA I ANDROID IZGLED ---
st.markdown("""
    <style>
    /* SAKRIVANJE STREAMLIT IKONICA (Dole desno i gore desno) */
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stFooter"] {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .st-emotion-cache-1cvow4s {display: none !important;} 
    a[href^="https://streamlit.io"] {display: none !important; opacity: 0 !important; pointer-events: none !important;}
    
    /* Tamna tema i Android stil */
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
    .stApp { background-color: #121212; color: #ffffff; }
    .header-box {
        text-align: center;
        padding: 40px 10px 20px 10px;
        background: linear-gradient(to bottom, #D4AF37, #8B6E02);
        margin: -20px -20px 20px -20px;
        border-radius: 0 0 40px 40px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
    }
    div[data-testid="stButton"] > button {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a) !important;
        color: #D4AF37 !important;
        border: 1px solid #444 !important;
        border-radius: 15px !important;
        height: 80px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.3) !important;
    }
    .btn-nazad div[data-testid="stButton"] > button {
        height: 50px !important;
        background: transparent !important;
        border: 1px solid #D4AF37 !important;
        color: white !important;
    }
    label, .stMarkdown p { color: #eeeeee !important; }
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return ""

# --- POČETNA STRANA ---
if st.session_state.stranica == 'pocetna':
    img_src = get_image_base64("kazan.png")
    image_html = f'<img src="{img_src}" width="150">' if img_src else '<div style="font-size: 70px;">⚗️</div>'
    st.markdown(f'<div class="header-box">{image_html}<h1 style="color: white; margin:0;">RAKIJA MASTER PRO</h1><p style="color: #eee;">Distillery Tools</p></div>', unsafe_allow_html=True)

    st.markdown("<p style='color:#D4AF37; font-weight:bold;'> 🟢 UKOMLJAVANJE</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🍇 Komina", use_container_width=True): idi_na('secer')
    with c2: 
        if st.button("🦠 Kvasci", use_container_width=True): idi_na('kvasci')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:10px;'> 🔥 DESTILACIJA</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️ Prvenac", use_container_width=True): idi_na('prvenac')
        if st.button("💧 Razblaživanje", use_container_width=True): idi_na('razblazivanje')
        if st.button("⚖️ Kupaža", use_container_width=True): idi_na('kupaza')
    with c4:
        if st.button("🏁 Patoka", use_container_width=True): idi_na('patoka')
        if st.button("🌡️ Temperatura", use_container_width=True): idi_na('temperatura')
        if st.button("🪵 Bure", use_container_width=True): idi_na('bure')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:10px;'> 📖 ARHIVA</p>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5: 
        if st.button("📖 Dnevnik", use_container_width=True): idi_na('dnevnik')
    with c6: 
        if st.button("🔗 Linkovi", use_container_width=True): idi_na('linkovi')

else:
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI", use_container_width=True): idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.stranica == 'secer':
        st.subheader("🍇 Analiza komine")
        brix = st.slider("Brix (%):", 0.0, 30.0, 18.0, 0.5)
        st.info(f"Babo: {brix*0.85:.1f}° | Oechsle: {brix*4.25:.0f}°")
        st.success(f"Potencijalni alkohol: {brix*0.55:.1f}% vol")

    elif st.session_state.stranica == 'kvasci':
        st.subheader("🦠 Kvasci i Enzimi")
        kg = st.number_input("Količina voća (kg):", value=100)
        st.warning(f"Enzim: {(kg/100)*2:.1f}g | Kvasac: {(kg/100)*25:.1f}g | Hrana: {(kg/100)*25:.1f}g")

    elif st.session_state.stranica == 'prvenac':
        st.subheader("✂️ Odvajanje prvenca")
        v = st.selectbox("Voće:", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        l = st.number_input("Meka rakija (L):", value=100)
        p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
        st.error(f"ODVOJITI: {l*p:.2f} L")

    elif st.session_state.stranica == 'patoka':
        st.subheader("🏁 Odvajanje patoke")
        voce = st.selectbox("Voće:", ["Šljiva", "Dunja", "Jabuka"])
        savet = {"Šljiva": "40-45% na luli", "Dunja": "45-50% na luli", "Jabuka": "oko 42% na luli"}
        st.info(f"Prekidaj hvatanje srca kada na luli padne na: **{savet[voce]}**")

    elif st.session_state.stranica == 'razblazivanje':
        st.subheader("💧 Razblaživanje")
        v, j1, j2 = st.number_input("Litraža (L):", value=10.0), st.number_input("Trenutna %:", value=65.0), st.number_input("Željena %:", value=42.0)
        if j1 > j2: st.success(f"DODATI VODE: {v*(j1/j2-1):.2f} L")

    elif st.session_state.stranica == 'temperatura':
        st.subheader("🌡️ Korekcija temperature")
        j, t = st.number_input("Jačina %:", value=45.0), st.number_input("Temp °C:", value=15.0)
        st.warning(f"Stvarna jačina (na 20°C): {j + (20-t)*0.3:.1f}%")

    elif st.session_state.stranica == 'kupaza':
        st.subheader("⚖️ Kupaža")
        v1, j1 = st.number_input("L1:", value=10.0), st.number_input("J1 %:", value=60.0)
        v2, j2 = st.number_input("L2:", value=5.0), st.number_input("J2 %:", value=40.0)
        if (v1+v2) > 0: st.success(f"Ukupno: {v1+v2}L | Jačina: {(v1*j1+v2*j2)/(v1+v2):.1f}%")

    elif st.session_state.stranica == 'bure':
        st.subheader("🪵 Zapremina bureta")
        h, ds, dk = st.number_input("Visina (cm):", value=70.0), st.number_input("Sredina (cm):", value=60.0), st.number_input("Dno (cm):", value=50.0)
        v = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
        st.success(f"Zapremina: oko {v:.1f} L")

    elif st.session_state.stranica == 'dnevnik':
        st.subheader("📖 Dnevnik rada")
        with st.expander("Dodaj novi unos"):
            f_ime = st.text_input("Voće", "Šljiva")
            f_god = st.text_input("Godina", "2024")
            f_kg = st.number_input("Kg", value=500)
            f_lit = st.number_input("Litri", value=50)
            f_jac = st.number_input("Jačina %", value=42)
            if st.button("SAČUVAJ"):
                st.session_state.dnevnik.append({"ime": f_ime, "godina": f_god, "kg": f_kg, "litara": f_lit, "jacina": f_jac, "datum": datetime.now().strftime("%d.%m")})
                st.success("Sačuvano!")
        for i, s in enumerate(reversed(st.session_state.dnevnik)):
            st.markdown(f"**{s['ime']} ({s['godina']})** - {s['kg']}kg | {s['datum']} | {s['litara']}L | {s['jacina']}%")

    elif st.session_state.stranica == 'linkovi':
        st.subheader("🔗 Linkovi i Događaji")
        st.markdown("[📘 Knjiga: Rakijski kod](https://www.facebook.com/rakijskikod/)")
        st.markdown("[🥂 Rakija iz rakije](https://www.rakijaizrakije.com)")
        st.markdown("[🤝 Savez proizvođača rakija](https://savezrakija.rs)")
        st.divider()
        st.write("**📅 DOGAĐAJI:**")
        st.write("18.04.2024. Prvi Hajdučki festival rakije - Bogatić")
        st.markdown("[📍 Lokacija na mapi](https://www.google.com/maps/search/?api=1&query=44.834296,19.480729)")

st.markdown("<br><p style='text-align: center; color: #555; font-size:12px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
