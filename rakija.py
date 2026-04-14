import streamlit as st
from datetime import datetime
import math
import base64
import os

# --- 1. KONFIGURACIJA STRANICE ---
st.set_page_config(page_title="Rakija Master Pro", page_icon="🥃", layout="centered")

# --- 2. INICIJALIZACIJA SESIJE ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'
if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik = []

# --- 3. NAPREDNI CSS ZA IDENTIČAN FLET IZGLED ---
st.markdown("""
    <style>
    /* SAKRIVANJE STREAMLIT ELEMENATA */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stFooter"] {display: none !important;}
    [data-testid="manage-app-button"], .viewerBadge_container__1QSob {display: none !important;}
    
    /* Globalni stilovi */
    .stApp { background-color: #121212; color: #ffffff; }
    .block-container { padding: 0 !important; max-width: 400px !important; margin: auto; }

    /* ZLATNI HEADER */
    .header-container {
        text-align: center;
        padding: 40px 20px;
        background-color: #D4AF37;
        border-radius: 0 0 35px 35px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .header-title {
        color: white;
        font-size: 26px;
        font-weight: 900;
        margin: 0 0 15px 0;
        text-transform: uppercase;
    }

    /* SEKCIJE */
    .section-label {
        color: #D4AF37;
        font-size: 13px;
        font-weight: bold;
        margin: 20px 0 10px 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* DUGMIĆI - MAGIJA ZA CENTRIRANJE IKONE I TEKSTA */
    div[data-testid="stButton"] > button {
        background-color: #1e1e1e !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 15px !important;
        height: 110px !important;
        width: 100% !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.2s !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3) !important;
        white-space: pre-wrap !important; /* Omogućava novi red */
        line-height: 1.2 !important;
    }
    
    /* Hover i Active efekti */
    div[data-testid="stButton"] > button:hover {
        border-color: white !important;
        background-color: #252525 !important;
    }
    div[data-testid="stButton"] > button:active {
        background-color: #D4AF37 !important;
        color: #121212 !important;
        transform: scale(0.95) !important;
    }

    /* Dugme NAZAD */
    .btn-nazad div[data-testid="stButton"] > button {
        height: 45px !important;
        background-color: transparent !important;
        border: 1px solid #D4AF37 !important;
        color: white !important;
        margin: 10px 15px !important;
        width: calc(100% - 30px) !important;
    }

    /* Input polja */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    label { color: #D4AF37 !important; font-weight: bold !important; margin-left: 5px; }

    /* Uklanjanje razmaka između kolona */
    [data-testid="stHorizontalBlock"] { gap: 10px !important; padding: 0 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# ==========================================
# --- POČETNA STRANA (DASHBOARD) ---
# ==========================================
if st.session_state.stranica == 'pocetna':
    img_b64 = get_image_base64("kazan.png")
    header_img = f'<img src="data:image/png;base64,{img_b64}" width="130">' if img_b64 else '<div style="font-size: 70px;">⚗️</div>'

    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-title">RAKIJA MASTER PRO</h1>
            {header_img}
        </div>
    """, unsafe_allow_html=True)

    # Grid sistem
    st.markdown('<p class="section-label">🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇\nKomina", key="k1"): idi_na('komina')
    with c2:
        if st.button("🦠\nKvasci", key="k2"): idi_na('kvasci')

    st.markdown('<p class="section-label">🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️\nPrvenac", key="d1"): idi_na('prvenac')
        if st.button("💧\nRazblaživanje", key="d2"): idi_na('razblazivanje')
    with c4:
        if st.button("🏁\nPatoka", key="d3"): idi_na('patoka')
        if st.button("🌡️\nTemperatura", key="d4"): idi_na('temperatura')

    st.markdown('<p class="section-label">⚖️ KUPAŽA I BURE</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("⚖️\nKupaža", key="b1"): idi_na('kupaza')
    with c6:
        if st.button("🪵\nBure", key="b2"): idi_na('bure')

    st.markdown('<p class="section-label">📖 ARHIVA</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📖\nDnevnik", key="a1"): idi_na('dnevnik')
    with c8:
        if st.button("🔗\nLinkovi", key="a2"): idi_na('linkovi')

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI"):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)

    # Sadržaj stranica (Komina, Kvasci, itd.) ostaje isti kao u prethodnom kodu
    if st.session_state.stranica == 'komina':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>🍇 ANALIZA KOMINE</h2>", unsafe_allow_html=True)
        brix = st.number_input("Šećer u komini (% Brix):", value=18.0, step=0.1)
        st.info(f"Babo: {brix*0.85:.1f}° | Oechsle: {brix*4.25:.0f}°")
        st.success(f"Potencijalni alkohol: {brix*0.55:.1f}% vol")

    elif st.session_state.stranica == 'kvasci':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>🦠 KVASCI I ENZIMI</h2>", unsafe_allow_html=True)
        kg = st.number_input("Količina voća (kg):", value=100)
        st.warning(f"Enzim: {(kg/100)*2:.1f}g\n\nKvasac: {(kg/100)*25:.1f}g\n\nHrana: {(kg/100)*25:.1f}g")

    elif st.session_state.stranica == 'prvenac':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>✂️ PRVENAC</h2>", unsafe_allow_html=True)
        v = st.selectbox("Voće:", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        l = st.number_input("Meka rakija (L):", value=100)
        p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
        st.error(f"ODVOJITI: {l*p:.2f} L")

    elif st.session_state.stranica == 'razblazivanje':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>💧 RAZBLAŽIVANJE</h2>", unsafe_allow_html=True)
        v = st.number_input("Litraža (L):", value=10.0)
        j1 = st.number_input("Trenutna %:", value=65.0)
        j2 = st.number_input("Željena %:", value=42.0)
        if j1 > j2:
            vd = v * (j1/j2 - 1)
            st.success(f"DODATI VODE: {vd:.2f} L")

    elif st.session_state.stranica == 'temperatura':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>🌡️ TEMPERATURA</h2>", unsafe_allow_html=True)
        j = st.number_input("Jačina %:", value=45.0)
        t = st.number_input("Temp °C:", value=15.0)
        s = j + (20 - t) * 0.3
        st.warning(f"STVARNA JAČINA: {s:.1f}%")

    elif st.session_state.stranica == 'patoka':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>🏁 PATOKA</h2>", unsafe_allow_html=True)
        v = st.selectbox("Voće:", ["Šljiva", "Dunja", "Jabuka", "Kajsija / Breskva", "Grožđe"])
        saveti = {"Šljiva": "40-45% na luli", "Dunja": "45-50% na luli", "Kajsija / Breskva": "45-50% na luli", "Jabuka": "40-42% na luli", "Grožđe": "35-40% na luli"}
        st.info(f"Prekidaj na: {saveti[v]}")

    elif st.session_state.stranica == 'kupaza':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>⚖️ KUPAŽA</h2>", unsafe_allow_html=True)
        v1 = st.number_input("L1 (Litri):", value=10.0)
        j1 = st.number_input("Jačina 1 (%):", value=60.0)
        v2 = st.number_input("L2 (Litri):", value=5.0)
        j2 = st.number_input("Jačina 2 (%):", value=40.0)
        if (v1 + v2) > 0:
            n = (v1*j1 + v2*j2) / (v1+v2)
            st.success(f"Ukupno: {v1+v2}L | Jačina: {n:.1f}%")

    elif st.session_state.stranica == 'bure':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>🪵 BURE</h2>", unsafe_allow_html=True)
        h = st.number_input("Visina (cm):", value=70.0)
        ds = st.number_input("Sredina (cm):", value=60.0)
        dk = st.number_input("Dno (cm):", value=50.0)
        v = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
        st.success(f"Zapremina: oko {v:.1f} L")

    elif st.session_state.stranica == 'dnevnik':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>📖 DNEVNIK RADA</h2>", unsafe_allow_html=True)
        with st.expander("➕ NOVI UNOS", expanded=True):
            f_ime = st.text_input("Voće", "Šljiva")
            f_god = st.text_input("Godina", "2024")
            f_kg = st.number_input("Kg", value=500)
            f_dat = st.text_input("Datum", datetime.now().strftime("%d.%m"))
            f_lit = st.number_input("Litri", value=50)
            f_jac = st.number_input("Jačina %", value=42)
            if st.button("SAČUVAJ U ARHIVU"):
                st.session_state.dnevnik.append({"ime": f_ime, "godina": f_god, "kg": f_kg, "datum": f_dat, "litara": f_lit, "jacina": f_jac})
                st.success("Sačuvano!")
        for s in reversed(st.session_state.dnevnik):
            st.markdown(f"<div style='background-color:#1e1e1e; padding:15px; border-radius:15px; margin:10px; border:1px solid #D4AF37;'><strong style='color:#D4AF37;'>{s['ime']} ({s['godina']})</strong><br>{s['kg']}kg | {s['datum']} | {s['litara']}L | {s['jacina']}%</div>", unsafe_allow_html=True)

    elif st.session_state.stranica == 'linkovi':
        st.markdown("<h2 style='color:#D4AF37; margin-left:15px;'>🔗 LINKOVI</h2>", unsafe_allow_html=True)
        st.markdown("[📘 Knjiga: Rakijski kod](https://www.facebook.com/rakijskikod/)")
        st.markdown("[🥂 Rakija iz rakije](https://www.rakijaizrakije.com)")
        st.markdown("[🤝 Savez proizvođača rakija](https://savezrakija.rs)")

st.markdown("<p style='text-align: center; color: #555; font-size:10px; margin-top:50px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
