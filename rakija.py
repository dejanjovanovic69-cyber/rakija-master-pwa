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

# --- 3. CSS ZA SAKRIVANJE STREAMLIT BRENDINGA I IKONICA ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stFooter"] {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .st-emotion-cache-1cvow4s {display: none !important;} 
    .st-emotion-cache-zq5wms {display: none !important;}
    
    .stApp { background-color: #121212; color: #ffffff; }
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }

    /* Naslovni blok */
    .header-box {
        text-align: center;
        padding: 40px 10px 20px 10px;
        background: linear-gradient(to bottom, #D4AF37, #8B6E02);
        margin: -20px -20px 20px -20px;
        border-radius: 0 0 40px 40px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
    }
    
    /* Dugmići na dashboardu */
    div[data-testid="stButton"] > button {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a) !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 15px !important;
        height: 100px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.3) !important;
        transition: 0.2s !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: scale(0.95) !important;
        background: #D4AF37 !important;
        color: #121212 !important;
    }
    
    /* Dugme za NAZAD */
    .btn-nazad div[data-testid="stButton"] > button {
        height: 50px !important;
        background: transparent !important;
        border: 1px solid #D4AF37 !important;
        color: white !important;
    }

    /* Input polja */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    label { color: #D4AF37 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def dugme_nazad():
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI"):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")

# ==========================================
# --- POČETNA STRANA (DASHBOARD) ---
# ==========================================
if st.session_state.stranica == 'pocetna':
    st.markdown("""
        <div class="header-box">
            <div style="font-size: 60px; margin-bottom: 10px;">⚗️</div>
            <h1 style='color: white; margin:0; font-size: 28px;'>RAKIJA MASTER PRO</h1>
            <p style='color: #eee; font-style: italic; font-size: 14px;'>Premium Distillery Tools</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:10px;'> 🟢 UKOMLJAVANJE</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇\nKomina"): idi_na('komina')
    with c2:
        if st.button("🦠\nKvasci"): idi_na('kvasci')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:10px;'> 🔥 DESTILACIJA</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️\nPrvenac"): idi_na('prvenac')
        if st.button("💧\nRazblaživanje"): idi_na('razblazivanje')
    with c4:
        if st.button("🏁\nPatoka"): idi_na('patoka')
        if st.button("🌡️\nTemperatura"): idi_na('temperatura')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:10px;'> ⚖️ KUPAŽA I BURE</p>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("⚖️\nKupaža"): idi_na('kupaza')
    with c6:
        if st.button("🪵\nBure"): idi_na('bure')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:10px;'> 📖 ARHIVA</p>", unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📖\nDnevnik"): idi_na('dnevnik')
    with c8:
        if st.button("🔗\nLinkovi"): idi_na('linkovi')

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    dugme_nazad()

    if st.session_state.stranica == 'komina':
        st.subheader("🍇 ANALIZA KOMINE")
        brix = st.number_input("Šećer u komini (% Brix):", value=18.0)
        st.info(f"Babo: {brix*0.85:.1f}° | Oechsle: {brix*4.25:.0f}°")
        st.success(f"Potencijalni alkohol: {brix*0.55:.1f}% vol")

    elif st.session_state.stranica == 'kvasci':
        st.subheader("🦠 KVASCI I ENZIMI")
        kg = st.number_input("Količina voća (kg):", value=100)
        st.warning(f"Enzim: {(kg/100)*2:.1f}g\n\nKvasac: {(kg/100)*25:.1f}g\n\nHrana: {(kg/100)*25:.1f}g")

    elif st.session_state.stranica == 'prvenac':
        st.subheader("✂️ PRVENAC")
        v = st.selectbox("Voće:", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        l = st.number_input("Meka rakija (L):", value=100)
        p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
        st.error(f"ODVOJITI: {l*p:.2f} L")

    elif st.session_state.stranica == 'razblazivanje':
        st.subheader("💧 RAZBLAŽIVANJE")
        v = st.number_input("Litraža (L):", value=10.0)
        j1 = st.number_input("Trenutna %:", value=65.0)
        j2 = st.number_input("Željena %:", value=42.0)
        if j1 > j2:
            vd = v * (j1/j2 - 1)
            st.success(f"DODATI VODE: {vd:.2f} L")

    elif st.session_state.stranica == 'temperatura':
        st.subheader("🌡️ TEMPERATURA")
        j = st.number_input("Jačina %:", value=45.0)
        t = st.number_input("Temp °C:", value=15.0)
        s = j + (20 - t) * 0.3
        st.warning(f"STVARNA JAČINA: {s:.1f}%")

    elif st.session_state.stranica == 'patoka':
        st.subheader("🏁 PATOKA")
        v = st.selectbox("Voće:", ["Šljiva", "Dunja", "Jabuka", "Kajsija / Breskva", "Grožđe"])
        saveti = {
            "Šljiva": "Prekidaj na 40-45% na luli. Ispod 40% izlaze teški alkoholi.",
            "Dunja": "Prekidaj na 45-50% na luli. Aromatično voće brzo gubi fine arome.",
            "Kajsija / Breskva": "Prekidaj na 45-50% na luli. Reži ranije!",
            "Jabuka": "Prekidaj na oko 40-42%. Pazi na miris 'na vosak'.",
            "Grožđe": "Prekidaj na 35-40% na luli."
        }
        st.info(saveti[v])

    elif st.session_state.stranica == 'kupaza':
        st.subheader("⚖️ KUPAŽA")
        c1, c2 = st.columns(2)
        with c1:
            v1 = st.number_input("L1 (Litri):", value=10.0)
            j1 = st.number_input("Jačina 1 (%):", value=60.0)
        with c2:
            v2 = st.number_input("L2 (Litri):", value=5.0)
            j2 = st.number_input("Jačina 2 (%):", value=40.0)
        if (v1 + v2) > 0:
            uk = v1 + v2
            n = (v1*j1 + v2*j2) / uk
            st.success(f"Ukupno: {uk}L | Jačina: {n:.1f}%")

    elif st.session_state.stranica == 'bure':
        st.subheader("🪵 BURE")
        h = st.number_input("Visina (cm):", value=70.0)
        ds = st.number_input("Sredina (cm):", value=60.0)
        dk = st.number_input("Dno (cm):", value=50.0)
        v = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
        st.success(f"Zapremina: oko {v:.1f} L")

    elif st.session_state.stranica == 'dnevnik':
        st.subheader("📖 DNEVNIK RADA")
        with st.expander("➕ NOVI UNOS", expanded=True):
            f_ime = st.text_input("Voće", "Šljiva")
            f_god = st.text_input("Godina", "2024")
            f_kg = st.number_input("Kg", value=500)
            f_dat = st.text_input("Datum", datetime.now().strftime("%d.%m"))
            f_lit = st.number_input("Litri", value=50)
            f_jac = st.number_input("Jačina %", value=42)
            if st.button("SAČUVAJ U ARHIVU"):
                st.session_state.dnevnik.append({
                    "ime": f_ime, "godina": f_god, "kg": f_kg, 
                    "datum": f_dat, "litara": f_lit, "jacina": f_jac
                })
                st.success("Sačuvano!")

        for i, s in enumerate(reversed(st.session_state.dnevnik)):
            st.markdown(f"""
            <div style='background-color:#1e1e1e; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #D4AF37;'>
                <strong style='color:#D4AF37;'>{s['ime']} ({s['godina']})</strong><br>
                {s['kg']}kg | {s['datum']} | {s['litara']}L | {s['jacina']}%
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.stranica == 'linkovi':
        st.subheader("🔗 LINKOVI I DOGAĐAJI")
        st.markdown("[📘 Knjiga: Rakijski kod](https://www.facebook.com/rakijskikod/)")
        st.markdown("[🥂 Rakija iz rakije](https://www.rakijaizrakije.com)")
        st.markdown("[🤝 Savez proizvođača rakija](https://savezrakija.rs)")
        st.write("---")
        st.write("**📅 DOGAĐAJI**")
        st.write("18.04.2024. Prvi Hajdučki festival rakije - Bogatić")

st.markdown("<p style='text-align: center; color: #555; font-size:10px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
