import streamlit as st
from datetime import datetime
import math
import base64
import os
import json

# --- 1. KONFIGURACIJA ---
st.set_page_config(
    page_title="Rakija Master Pro",
    page_icon="🥃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DATUM_ISTEKA = datetime(2026, 12, 31)
if datetime.now() > DATUM_ISTEKA:
    st.error("PROBNI PERIOD ISTEKAO")
    st.stop()

# --- 2. ČUVANJE PODATAKA (DNEVNIK) ---
FILE_PATH = "dnevnik_podaci.json"

def ucitaj_podatke():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def sacuvaj_podatke(lista):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

# --- 3. INICIJALIZACIJA SESIJE ---
if "stranica" not in st.session_state:
    st.session_state.stranica = "pocetna"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"
if "dnevnik" not in st.session_state:
    st.session_state.dnevnik = ucitaj_podatke()

# Boje
if st.session_state.theme_mode == "dark":
    GOLD = "#D4AF37"
    BG = "#121212"
    TXT = "white"
    CARD = "#1e1e1e"
else:
    GOLD = "#996515"
    BG = "#f8f9fa"
    TXT = "black"
    CARD = "white"

# --- 4. CSS (ISPRAVLJEN / STABILNIJI) ---
st.markdown(f"""
<style>
/* =========================================================
   STREAMLIT UI (ikonice, toolbar, status, deploy, footer)
   ========================================================= */

/* Top bar / toolbar / deploy dugmad */
[data-testid="stHeader"],
[data-testid="stToolbar"],
.stDeployButton,
.stAppDeployButton,
[data-testid="stAppDeployButton"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

/* Running/Stop status widget (često je "dole desno") */
[data-testid="stStatusWidget"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

/* Footer */
footer,
[data-testid="stFooter"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

/* Stari glavni meni (nekad se pojavi u nekim režimima) */
#MainMenu {{
    visibility: hidden !important;
}}

/* =========================================================
   TVOJ THEME / UI STIL
   ========================================================= */

.stApp {{
    background-color: {BG};
    color: {TXT};
}}

.block-container {{
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
    max-width: 500px !important;
}}

/* Flet Header Klon */
.flet-header {{
    background-color: {GOLD};
    padding: 20px;
    text-align: center;
    border-radius: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    margin-bottom: 20px;
    position: relative;
}}

.flet-title {{
    color: white;
    font-size: 24px;
    font-weight: 900;
    margin: 0;
}}

/* Stilizacija svih dugmića da izgledaju kao kartice */
div.stButton > button {{
    background-color: {CARD} !important;
    color: {GOLD} !important;
    border: 1px solid {GOLD} !important;
    border-radius: 15px !important;
    height: 80px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    transition: 0.3s;
}}

div.stButton > button:hover {{
    background-color: {GOLD} !important;
    color: {BG} !important;
}}

/* Primarna dugmad (Izračunaj, Sačuvaj) */
div.stButton > button[data-testid="baseButton-primary"] {{
    background-color: {GOLD} !important;
    color: black !important;
    height: 50px !important;
}}

/* Dugme za brisanje iz dnevnika */
.del-btn div.stButton > button {{
    height: 40px !important;
    border: none !important;
    background: transparent !important;
    font-size: 20px !important;
}}

/* Naslovi sekcija */
.section-label {{
    color: {GOLD};
    font-size: 14px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
    text-transform: uppercase;
}}

/* =========================================
   POPRAVKA ZA POLJA ZA UNOS I TEKST IZNAD NJIH
   ========================================= */

/* Boja teksta iznad polja (Labele) */
label p, label div {{
    color: {GOLD} !important;
    font-weight: bold !important;
    font-size: 14px !important;
}}

/* Pozadina i ivice samog polja za unos */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {{
    background-color: {CARD} !important;
    border: 1px solid {GOLD} !important;
    border-radius: 10px !important;
}}

/* Tekst unutar polja za unos i plus/minus dugmići */
input, div[data-baseweb="input"] button {{
    color: {TXT} !important;
    background-color: transparent !important;
}}

/* Tekst u padajućem meniju (Selectbox) */
div[data-baseweb="select"] span {{
    color: {TXT} !important;
}}
</style>
""", unsafe_allow_html=True)

# --- 5. POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ==========================================
# --- POČETNA STRANA (DASHBOARD) ---
# ==========================================
if st.session_state.stranica == "pocetna":

    img_b64 = get_base64_img("kazan.png")

    # POPRAVKA: ovde mora biti <img> tag, ne samo "data:image..."
    slika_html = (
        f'data:image/png;base64,{img_b64}'
        if img_b64
        else '<div style="font-size:60px;">⚗️</div>'
    )

    ikona_teme = "☀️" if st.session_state.theme_mode == "dark" else "🌙"

    # Header
    st.markdown(f"""
        <div class="flet-header">
            <p class="flet-title">RAKIJA MASTER PRO</p>
            {slika_html}
        </div>
    """, unsafe_allow_html=True)

    # Dugme za temu
    if st.button(f"{ikona_teme} Promeni temu", use_container_width=True):
        st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"
        st.rerun()

    # --- GLAVNI MENI ---
    st.markdown('<p class="section-label">🟢 Ukomljavanje</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇 Komina", use_container_width=True):
            idi_na("komina")
    with c2:
        if st.button("🦠 Kvasci", use_container_width=True):
            idi_na("kvasci")

    st.markdown('<p class="section-label">🔥 Destilacija</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️ Prvenac", use_container_width=True):
            idi_na("prvenac")
    with c4:
        if st.button("🏁 Patoka", use_container_width=True):
            idi_na("patoka")

    c5, c6 = st.columns(2)
    with c5:
        if st.button("💧 Razblaživanje", use_container_width=True):
            idi_na("razblazivanje")
    with c6:
        if st.button("🌡️ Temperatura", use_container_width=True):
            idi_na("temperatura")

    st.markdown('<p class="section-label">⚖️ Kupaža i odležavanje</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if st.button("⚖️ Kupaža", use_container_width=True):
            idi_na("kupaza")
    with c8:
        if st.button("🪵 Bure", use_container_width=True):
            idi_na("bure")

    st.markdown('<p class="section-label">📖 Arhiva i linkovi</p>', unsafe_allow_html=True)
    c9, c10 = st.columns(2)
    with c9:
        if st.button("📖 Dnevnik", use_container_width=True):
            idi_na("dnevnik")
    with c10:
        if st.button("🔗 Linkovi", use_container_width=True):
            idi_na("linkovi")

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:

    def naslov_alata(tekst, podnaslov=""):
        st.markdown(
            f"<h2 style='color:{GOLD}; font-size:24px; font-weight:bold; margin-bottom: 0px;'>{tekst}</h2>",
            unsafe_allow_html=True
        )
        if podnaslov:
            st.markdown(
                f"<p style='color:{TXT}; font-size:14px; font-style:italic;'>{podnaslov}</p>",
                unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.stranica == "komina":
        naslov_alata("🍇 ANALIZA KOMINE", "Brix meri šećer. Babo i Oechsle mere gustinu šire.")
        u = st.number_input("Šećer u komini (% Brix)", value=18.0, step=0.1)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            st.success(f"Babo: {u*0.85:.1f}° | Oechsle: {u*4.25:.0f}°\n\nPotencijalni alkohol: {u*0.55:.1f}% vol")

    elif st.session_state.stranica == "kvasci":
        naslov_alata("🦠 KVASCI I ENZIMI", "Enzimi, kvasci i hrana osiguravaju čisto vrenje.")
        u = st.number_input("Količina voća (kg)", value=100.0, step=1.0)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            st.success(f"Enzim: {(u/100)*2:.1f}g\n\nKvasac: {(u/100)*25:.1f}g\n\nHrana: {(u/100)*25:.1f}g")

    elif st.session_state.stranica == "prvenac":
        naslov_alata("✂️ PRVENAC", "Odvajanje metila na početku prepeka.")
        v = st.selectbox("Voće", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        u = st.number_input("Meka rakija (L)", value=100.0, step=1.0)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=Truerakija.py
