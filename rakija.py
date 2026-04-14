import streamlit as st
from datetime import datetime
import math
import base64
import os
import json

# --- 1. KONFIGURACIJA STRANICE ---
st.set_page_config(page_title="Rakija Master Pro", page_icon="🥃", layout="centered")

# --- 2. AKTIVACIJA DO 31. DECEMBRA 2026. ---
DATUM_ISTEKA = datetime(2026, 12, 31)
if datetime.now() > DATUM_ISTEKA:
    st.error("PROBNI PERIOD ISTEKAO")
    st.stop()

# --- 3. INICIJALIZACIJA SESIJE (IDENTIČNO KAO FLET) ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'
if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik = []

GOLD_DARK = "#D4AF37"
GOLD_LIGHT = "#996515"

def get_gold(): return GOLD_DARK if st.session_state.theme_mode == 'dark' else GOLD_LIGHT
def get_bg(): return "#121212" if st.session_state.theme_mode == 'dark' else "#f8f9fa"
def get_txt(): return "white" if st.session_state.theme_mode == 'dark' else "black"
def get_card(): return "#1e1e1e" if st.session_state.theme_mode == 'dark' else "white"

# --- 4. BRUTALAN CSS ZA REPLIKACIJU FLET UI ---
st.markdown(f"""
    <style>
    /* SAKRIVANJE STREAMLIT ELEMENATA */
    #MainMenu {{visibility: hidden !important;}}
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stFooter"] {{display: none !important;}}
    [data-testid="manage-app-button"], .viewerBadge_container__1QSob {{display: none !important;}}
    
    /* Globalni stilovi */
    .stApp {{ background-color: {get_bg()}; color: {get_txt()}; }}
    .block-container {{ padding: 0 !important; max-width: 450px !important; margin: auto; }}

    /* ZLATNI HEADER (Kao u Fletu) */
    .flet-header {{
        background-color: {GOLD_DARK};
        padding: 20px 15px 30px 20px;
        border-radius: 0 0 35px 35px;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.4);
        margin-bottom: 20px;
        position: relative;
    }}
    .header-title {{
        color: white;
        font-size: 22px;
        font-weight: 900;
        margin: 0;
        text-align: left;
    }}
    .header-img-container {{
        text-align: center;
        margin-top: 15px;
    }}

    /* FIKSIRANJE KOLONA NA MOBILNOM (Da ne budu pilule) */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        padding: 0 15px !important;
    }}
    [data-testid="stHorizontalBlock"] > div {{
        width: 50% !important;
        min-width: 50% !important;
    }}

    /* SEKCIJE (Naslovi) */
    .section-title {{
        color: {get_gold()};
        font-size: 14px;
        font-weight: bold;
        margin: 25px 0 10px 15px;
        text-transform: uppercase;
    }}

    /* DUGMIĆI (Kvadratni stavka stil iz Fleta) */
    div[data-testid="stButton"] > button {{
        background-color: {get_card()} !important;
        color: {get_gold()} !important;
        border: 1px solid {get_gold()} !important;
        border-radius: 15px !important;
        height: 100px !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 5px !important;
        transition: 0.2s !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2) !important;
        line-height: 1.2 !important;
    }}
    
    /* Ikona i tekst unutar dugmeta */
    div[data-testid="stButton"] > button p {{
        font-size: 14px !important;
        font-weight: bold !important;
        margin: 0 !important;
        text-align: center !important;
    }}

    div[data-testid="stButton"] > button:active {{
        background-color: {get_gold()} !important;
        color: #121212 !important;
    }}

    /* Dugme za temu u headeru */
    .theme-btn-pos {{
        position: absolute;
        top: 15px;
        right: 15px;
        z-index: 1000;
    }}
    .theme-btn-pos button {{
        background: transparent !important;
        border: none !important;
        font-size: 24px !important;
        color: white !important;
        padding: 0 !important;
        width: 40px !important;
        height: 40px !important;
    }}

    /* Dugme NAZAD */
    .back-btn div[data-testid="stButton"] > button {{
        height: 45px !important;
        background-color: transparent !important;
        border: 1px solid {get_gold()} !important;
        color: {get_gold()} !important;
        font-size: 14px !important;
        margin: 10px 15px !important;
        width: calc(100% - 30px) !important;
    }}

    /* Input polja */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {{
        background-color: {get_card()} !important;
        border-radius: 10px !important;
        color: {get_txt()} !important;
        border: 1px solid {get_gold()} !important;
    }}
    label {{ color: {get_gold()} !important; font-size: 11px !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. POMOĆNE FUNKCIJE ---
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
    header_img = f'<img src="data:image/png;base64,{img_b64}" width="160">' if img_b64 else '<div style="font-size: 80px;">⚗️</div>'
    ikona_teme = "☀️" if st.session_state.theme_mode == "dark" else "🌙"

    # Header sa naslovom i slikom
    st.markdown(f"""
        <div class="flet-header">
            <p class="header-title">RAKIJA MASTER PRO</p>
            <div class="header-img-container">
                {header_img}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Dugme za temu pozicionirano preko CSS-a
    st.markdown('<div class="theme-btn-pos">', unsafe_allow_html=True)
    if st.button(ikona_teme, key="theme_toggle"):
        st.session_state.theme_mode = 'light' if st.session_state.theme_mode == 'dark' else 'dark'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SEKCIJE ---
    st.markdown('<p class="section-title"> 🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇\nKomina", key="k1"): idi_na('komina')
    with c2:
        if st.button("🦠\nKvasci", key="k2"): idi_na('kvasci')

    st.markdown('<p class="section-title"> 🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️\nPrvenac", key="d1"): idi_na('prvenac')
        if st.button("💧\nRazblaživanje", key="d2"): idi_na('razblazivanje')
    with c4:
        if st.button("🏁\nPatoka", key="d3"): idi_na('patoka')
        if st.button("🌡️\nTemperatura", key="d4"): idi_na('temperatura')

    st.markdown('<p class="section-title"> ⚖️ KUPAŽA I ODLEŽAVANJE</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("⚖️\nKupaža", key="b1"): idi_na('kupaza')
    with c6:
        if st.button("🪵\nBure", key="b2"): idi_na('bure')

    st.markdown('<p class="section-title"> 📖 ARHIVA I LINKOVI</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📖\nDnevnik", key="a1"): idi_na('dnevnik')
    with c8:
        if st.button("🔗\nLinkovi", key="a2"): idi_na('linkovi')

    st.divider()
    if st.button("ZATVORI APLIKACIJU", key="exit_btn"):
        st.warning("Osvežite stranicu za izlaz.")

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI", key="back_btn"):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)

    # 1. KOMINA
    if st.session_state.stranica == 'komina':
        st.markdown(f"<h2 style='color:{get_gold()};'>🍇 ANALIZA KOMINE</h2>", unsafe_allow_html=True)
        st.write("*Brix meri šećer. Babo i Oechsle mere gustinu šire.*")
        u = st.number_input("Šećer u komini (% Brix)", value=18.0)
        if st.button("IZRAČUNAJ", key="calc_komina"):
            st.info(f"Babo: {u*0.85:.1f}° | Oechsle: {u*4.25:.0f}°\n\nPotencijalni alkohol: {u*0.55:.1f}% vol")

    # 2. KVASCI
    elif st.session_state.stranica == 'kvasci':
        st.markdown(f"<h2 style='color:{get_gold()};'>🦠 KVASCI I ENZIMI</h2>", unsafe_allow_html=True)
        u = st.number_input("Količina voća (kg)", value=100)
        if st.button("IZRAČUNAJ", key="calc_kvasci"):
            st.info(f"Enzim: {(u/100)*2:.1f}g\n\nKvasac: {(u/100)*25:.1f}g\n\nHrana: {(u/100)*25:.1f}g")

    # 3. PRVENAC
    elif st.session_state.stranica == 'prvenac':
        st.markdown(f"<h2 style='color:{get_gold()};'>✂️ PRVENAC</h2>", unsafe_allow_html=True)
        v = st.selectbox("Voće", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        u = st.number_input("Meka rakija (L)", value=100)
        if st.button("IZRAČUNAJ", key="calc_prvenac"):
            p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
            st.error(f"ODVOJITI: {u*p:.2f} L")

    # 4. RAZBLAŽIVANJE
    elif st.session_state.stranica == 'razblazivanje':
        st.markdown(f"<h2 style='color:{get_gold()};'>💧 RAZBLAŽIVANJE</h2>", unsafe_allow_html=True)
        v = st.number_input("Litraža (L)", value=10.0)
        j1 = st.number_input("Trenutna %", value=65.0)
        j2 = st.number_input("Željena %", value=42.0)
        if st.button("IZRAČUNAJ", key="calc_razblaz"):
            vd = v * (j1/j2 - 1)
            st.success(f"DODATI VODE: {vd:.2f} L")

    # 5. TEMPERATURA
    elif st.session_state.stranica == 'temperatura':
        st.markdown(f"<h2 style='color:{get_gold()};'>🌡️ TEMPERATURA</h2>", unsafe_allow_html=True)
        j = st.number_input("Jačina %", value=45.0)
        t = st.number_input("Temp °C", value=15.0)
        if st.button("IZRAČUNAJ", key="calc_temp"):
            s = j + (20 - t) * 0.3
            st.warning(f"STVARNA JAČINA: {s:.1f}%")

    # 6. PATOKA
    elif st.session_state.stranica == 'patoka':
        st.markdown(f"<h2 style='color:{get_gold()};'>🏁 PATOKA</h2>", unsafe_allow_html=True)
        v = st.selectbox("Voće", ["Šljiva", "Dunja", "Jabuka"])
        if st.button("SAVET", key="calc_patoka"):
            s = {"Šljiva": "Prekidaj na 40-45% na luli.", "Dunja": "Prekidaj na 45-50% na luli.", "Jabuka": "Prekidaj na oko 42%."}
            st.info(s[v])

    # 7. KUPAŽA
    elif st.session_state.stranica == 'kupaza':
        st.markdown(f"<h2 style='color:{get_gold()};'>⚖️ KUPAŽA</h2>", unsafe_allow_html=True)
        v1 = st.number_input("L1 (Litri)", value=10.0)
        j1 = st.number_input("Jačina 1 (%)", value=60.0)
        v2 = st.number_input("L2 (Litri)", value=5.0)
        j2 = st.number_input("Jačina 2 (%)", value=40.0)
        if st.button("IZRAČUNAJ", key="calc_kupaza"):
            uk = v1 + v2
            n = (v1*j1 + v2*j2) / uk
            st.success(f"Ukupno: {uk}L | Jačina: {n:.1f}%")

    # 8. BURE
    elif st.session_state.stranica == 'bure':
        st.markdown(f"<h2 style='color:{get_gold()};'>🪵 BURE</h2>", unsafe_allow_html=True)
        h = st.number_input("Visina (cm)", value=70.0)
        ds = st.number_input("Sredina (cm)", value=60.0)
        dk = st.number_input("Dno (cm)", value=50.0)
        if st.button("IZRAČUNAJ", key="calc_bure"):
            vol = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
            st.info(f"Zapremina: oko {vol:.1f} L")

    # 9. DNEVNIK
    elif st.session_state.stranica == 'dnevnik':
        st.markdown(f"<h2 style='color:{get_gold()};'>📖 DNEVNIK RADA</h2>", unsafe_allow_html=True)
        f_ime = st.text_input("Voće", "Šljiva")
        f_god = st.text_input("Godina", "2024")
        c1, c2 = st.columns(2)
        with c1:
            f_kg = st.number_input("Kg", value=500)
            f_lit = st.number_input("Litri", value=50)
        with c2:
            f_dat = st.text_input("Datum", datetime.now().strftime("%d.%m"))
            f_jac = st.number_input("Jačina %", value=42)
        
        if st.button("SAČUVAJ U ARHIVU", key="save_dnevnik"):
            st.session_state.dnevnik.append({"ime": f_ime, "godina": f_god, "kg": f_kg, "datum": f_dat, "litara": f_lit, "jacina": f_jac})
            st.success("Sačuvano!")

        st.write("---")
        for s in reversed(st.session_state.dnevnik):
            st.markdown(f"<div style='background-color:{get_card()}; padding:15px; border-radius:15px; margin-bottom:10px; border:1px solid {get_gold()};'><strong style='color:{get_gold()};'>{s['ime']} ({s['godina']})</strong><br>{s['kg']}kg | {s['datum']} | {s['litara']}L | {s['jacina']}%</div>", unsafe_allow_html=True)

    # 10. LINKOVI
    elif st.session_state.stranica == 'linkovi':
        st.markdown(f"<h2 style='color:{get_gold()};'>🔗 KORISNI LINKOVI</h2>", unsafe_allow_html=True)
        def link_box(t, url):
            st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><div style="background-color:{get_gold()}; color:black; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:10px;">{t}</div></a>', unsafe_allow_html=True)
        link_box("📘 Knjiga: Rakijski kod", "https://www.facebook.com/rakijskikod/?locale=sr_RS")
        link_box("🥂 Rakija iz rakije", "https://www.rakijaizrakije.com")
        link_box("🤝 Savez proizvođača rakija", "https://savezrakija.rs")
        link_box("🛒 Rakija Shop", "https://rakijashop.eu/srb/")
        link_box("🏺 Čiča Zlajina Rakija", "https://cicazlajinarakija.rs")
        st.write("---")
        st.info("**18.04.2024. Prvi Hajdučki festival rakije**\n\nLokacija: Mike Vitomirovića 3, Bogatić")

st.markdown("<br><p style='text-align: center; color: #555; font-size:10px; margin-top:50px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
