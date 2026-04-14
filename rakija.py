import streamlit as st
from datetime import datetime
import math
import base64
import os
import json

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="Rakija Master Pro", page_icon="🥃", layout="centered")

# --- 2. INICIJALIZACIJA SESIJE ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'
if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik = []

GOLD = "#D4AF37"
BG = "#121212" if st.session_state.theme_mode == 'dark' else "#f8f9fa"
TXT = "white" if st.session_state.theme_mode == 'dark' else "black"
CARD = "#1e1e1e" if st.session_state.theme_mode == 'dark' else "white"

# --- 3. BRUTALAN CSS ZA IDENTIČAN FLET IZGLED NA MOBILNOM ---
st.markdown(f"""
    <style>
    /* SAKRIVANJE SVEGA OD STREAMLIT-A */
    [data-testid="stHeader"], [data-testid="stFooter"], [data-testid="stToolbar"] {{display: none !important;}}
    #MainMenu {{visibility: hidden;}}
    
    /* GLOBALNI STIL */
    .stApp {{ background-color: {BG}; color: {TXT}; }}
    .block-container {{ padding: 0 !important; max-width: 450px !important; margin: auto; }}

    /* ZAGLAVLJE (Identicno Fletu) */
    .flet-header {{
        background-color: {GOLD};
        padding: 30px 20px 40px 20px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
        position: relative;
        margin-bottom: 20px;
    }}
    .header-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 10px;
    }}
    .flet-title {{
        color: white;
        font-size: 22px;
        font-weight: 900;
        margin: 0;
        text-align: left;
    }}
    .header-img-box {{
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }}

    /* SILOVANJE KOLONA DA OSTANU 2 U REDU (Sprečava pilule) */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        padding: 0 15px !important;
    }}
    [data-testid="column"] {{
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }}

    /* STIL DUGMIĆA (Kvadratni, centrirani) */
    div.stButton > button {{
        width: 100% !important;
        height: 110px !important;
        background-color: {CARD} !important;
        color: {GOLD} !important;
        border: 1px solid {GOLD} !important;
        border-radius: 15px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
        transition: 0.2s !important;
        padding: 0 !important;
    }}
    
    div.stButton > button p {{
        margin: 0 !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }}

    div.stButton > button:active {{
        background-color: {GOLD} !important;
        color: #121212 !important;
    }}

    /* DUGME ZA TEMU U HEADERU */
    .theme-btn-container {{
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }}
    .theme-btn-container button {{
        background: transparent !important;
        border: none !important;
        font-size: 24px !important;
        color: white !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        box-shadow: none !important;
    }}

    /* NASLOVI SEKCIJA */
    .section-label {{
        color: {GOLD};
        font-size: 14px;
        font-weight: bold;
        margin: 25px 0 10px 20px;
        text-transform: uppercase;
    }}

    /* DUGME NAZAD */
    .back-btn-box div.stButton > button {{
        height: 50px !important;
        background-color: transparent !important;
        margin: 10px 15px !important;
        width: calc(100% - 30px) !important;
    }}

    /* INPUTI */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {{
        background-color: {CARD} !important;
        color: {TXT} !important;
        border: 1px solid {GOLD} !important;
    }}
    label {{ color: {GOLD} !important; font-weight: bold !important; font-size: 12px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

# ==========================================
# --- POČETNA (DASHBOARD) ---
# ==========================================
if st.session_state.stranica == 'pocetna':
    img_b64 = get_base64_img("kazan.png")
    slika_html = f'<img src="data:image/png;base64,{img_b64}" width="160">' if img_b64 else '<div style="font-size:80px;">⚗️</div>'
    ikona_teme = "☀️" if st.session_state.theme_mode == "dark" else "🌙"

    # Header
    st.markdown(f"""
        <div class="flet-header">
            <div class="header-top">
                <p class="flet-title">RAKIJA MASTER PRO</p>
            </div>
            <div class="header-img-box">{slika_html}</div>
        </div>
    """, unsafe_allow_html=True)

    # Theme Toggle (Pozicioniran preko CSS-a)
    st.markdown('<div class="theme-btn-container">', unsafe_allow_html=True)
    if st.button(ikona_teme, key="theme_toggle"):
        st.session_state.theme_mode = 'light' if st.session_state.theme_mode == 'dark' else 'dark'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # GRID TASTERA
    def draw_btn(label, icon, key, target):
        if st.button(f"{icon}\n{label}", key=key): idi_na(target)

    st.markdown('<p class="section-label"> 🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: draw_btn("Komina", "🍇", "k1", "komina")
    with c2: draw_btn("Kvasci", "🦠", "k2", "kvasci")

    st.markdown('<p class="section-label"> 🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3: 
        draw_btn("Prvenac", "✂️", "d1", "prvenac")
        draw_btn("Razblaživanje", "💧", "d2", "razblazivanje")
    with c4: 
        draw_btn("Patoka", "🏁", "d3", "patoka")
        draw_btn("Temperatura", "🌡️", "d4", "temperatura")

    st.markdown('<p class="section-label"> ⚖️ KUPAŽA I ODLEŽAVANJE</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5: draw_btn("Kupaža", "⚖️", "b1", "kupaza")
    with c6: draw_btn("Bure", "🪵", "b2", "bure")

    st.markdown('<p class="section-label"> 📖 ARHIVA I LINKOVI</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7: draw_btn("Dnevnik", "📖", "a1", "dnevnik")
    with c8: draw_btn("Linkovi", "🔗", "a2", "linkovi")

# ==========================================
# --- ALATI ---
# ==========================================
else:
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI", key="back"): idi_na('pocetna')
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.stranica == 'komina':
        st.markdown(f"<h2 style='color:{GOLD};'>🍇 ANALIZA KOMINE</h2>", unsafe_allow_html=True)
        u = st.number_input("Šećer u komini (% Brix)", value=18.0)
        if st.button("IZRAČUNAJ"):
            st.info(f"Babo: {u*0.85:.1f}° | Oechsle: {u*4.25:.0f}°\n\nPotencijalni alkohol: {u*0.55:.1f}% vol")

    elif st.session_state.stranica == 'kvasci':
        st.markdown(f"<h2 style='color:{GOLD};'>🦠 KVASCI I ENZIMI</h2>", unsafe_allow_html=True)
        u = st.number_input("Količina voća (kg)", value=100)
        if st.button("IZRAČUNAJ"):
            st.info(f"Enzim: {(u/100)*2:.1f}g\n\nKvasac: {(u/100)*25:.1f}g\n\nHrana: {(u/100)*25:.1f}g")

    elif st.session_state.stranica == 'prvenac':
        st.markdown(f"<h2 style='color:{GOLD};'>✂️ PRVENAC</h2>", unsafe_allow_html=True)
        v = st.selectbox("Voće", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        u = st.number_input("Meka rakija (L)", value=100)
        if st.button("IZRAČUNAJ"):
            p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
            st.error(f"ODVOJITI: {u*p:.2f} L")

    elif st.session_state.stranica == 'razblazivanje':
        st.markdown(f"<h2 style='color:{GOLD};'>💧 RAZBLAŽIVANJE</h2>", unsafe_allow_html=True)
        v = st.number_input("Litraža (L)", value=10.0)
        j1 = st.number_input("Trenutna %", value=65.0)
        j2 = st.number_input("Željena %", value=42.0)
        if st.button("IZRAČUNAJ"):
            vd = v * (j1/j2 - 1)
            st.success(f"DODATI VODE: {vd:.2f} L")

    elif st.session_state.stranica == 'temperatura':
        st.markdown(f"<h2 style='color:{GOLD};'>🌡️ TEMPERATURA</h2>", unsafe_allow_html=True)
        j = st.number_input("Jačina %", value=45.0)
        t = st.number_input("Temp °C", value=15.0)
        if st.button("IZRAČUNAJ"):
            s = j + (20 - t) * 0.3
            st.warning(f"STVARNA JAČINA: {s:.1f}%")

    elif st.session_state.stranica == 'patoka':
        st.markdown(f"<h2 style='color:{GOLD};'>🏁 PATOKA</h2>", unsafe_allow_html=True)
        v = st.selectbox("Voće", ["Šljiva", "Dunja", "Jabuka"])
        if st.button("SAVET"):
            s = {"Šljiva": "Prekidaj na 40-45% na luli.", "Dunja": "Prekidaj na 45-50% na luli.", "Jabuka": "Prekidaj na oko 42%."}
            st.info(s[v])

    elif st.session_state.stranica == 'kupaza':
        st.markdown(f"<h2 style='color:{GOLD};'>⚖️ KUPAŽA</h2>", unsafe_allow_html=True)
        v1, j1 = st.number_input("L1 (L)", value=10.0), st.number_input("J1 (%)", value=60.0)
        v2, j2 = st.number_input("L2 (L)", value=5.0), st.number_input("J2 (%)", value=40.0)
        if st.button("IZRAČUNAJ"):
            n = (v1*j1 + v2*j2) / (v1+v2)
            st.success(f"Ukupno: {v1+v2}L | Jačina: {n:.1f}%")

    elif st.session_state.stranica == 'bure':
        st.markdown(f"<h2 style='color:{GOLD};'>🪵 BURE</h2>", unsafe_allow_html=True)
        h, ds, dk = st.number_input("Visina (cm)", 70.0), st.number_input("Sredina (cm)", 60.0), st.number_input("Dno (cm)", 50.0)
        if st.button("IZRAČUNAJ"):
            vol = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
            st.info(f"Zapremina: oko {vol:.1f} L")

    elif st.session_state.stranica == 'dnevnik':
        st.markdown(f"<h2 style='color:{GOLD};'>📖 DNEVNIK RADA</h2>", unsafe_allow_html=True)
        f_i, f_g = st.text_input("Voće", "Šljiva"), st.text_input("Godina", "2024")
        c1, c2 = st.columns(2)
        with c1:
            f_k, f_l = st.number_input("Kg", 500), st.number_input("Litri", 50)
        with c2:
            f_dat, f_j = st.text_input("Datum", datetime.now().strftime("%d.%m")), st.number_input("Jačina %", 42)
        if st.button("SAČUVAJ"):
            st.session_state.dnevnik.append({"ime": f_i, "godina": f_g, "kg": f_k, "datum": f_dat, "litara": f_l, "jacina": f_j})
            st.success("Sačuvano!")
        for s in reversed(st.session_state.dnevnik):
            st.markdown(f"<div style='background-color:{CARD}; padding:15px; border-radius:15px; margin-bottom:10px; border:1px solid {GOLD};'><strong style='color:{GOLD};'>{s['ime']} ({s['godina']})</strong><br>{s['kg']}kg | {s['datum']} | {s['litara']}L | {s['jacina']}%</div>", unsafe_allow_html=True)

    elif st.session_state.stranica == 'linkovi':
        st.markdown(f"<h2 style='color:{GOLD};'>🔗 LINKOVI</h2>", unsafe_allow_html=True)
        def link_box(t, url):
            st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><div style="background-color:{GOLD}; color:black; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:10px;">{t}</div></a>', unsafe_allow_html=True)
        link_box("📘 Knjiga: Rakijski kod", "https://www.facebook.com/rakijskikod/")
        link_box("🥂 Rakija iz rakije", "https://www.rakijaizrakije.com")
        link_box("🤝 Savez proizvođača rakija", "https://savezrakija.rs")
        link_box("🛒 Rakija Shop", "https://rakijashop.eu/srb/")
        link_box("🏺 Čiča Zlajina Rakija", "https://cicazlajinarakija.rs")
        st.divider()
        st.info("**18.04.2024. Prvi Hajdučki festival rakije**\n\nLokacija: Mike Vitomirovića 3, Bogatić")

st.markdown("<p style='text-align: center; color: #555; font-size:10px; margin-top:50px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
