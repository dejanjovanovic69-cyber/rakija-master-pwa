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

# === NAJJAČI CSS ===
st.markdown(f"""
<style>
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stAppDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], footer, [data-testid="stFooter"], 
    #MainMenu, [data-testid="stDecoration"], button[title="View app in new tab"],
    div[class*="Hosted"], div[style*="Hosted with Streamlit"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
    }}
    .stApp {{
        background-color: {BG} !important;
    }}
    .block-container {{
        padding-top: 0.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 520px !important;
    }}
    .flet-header {{
        background-color: {GOLD};
        padding: 20px;
        text-align: center;
        border-radius: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }}
    .flet-title {{
        color: white;
        font-size: 24px;
        font-weight: 900;
        margin: 0;
    }}
    div.stButton > button {{
        background-color: {CARD} !important;
        color: {GOLD} !important;
        border: 1px solid {GOLD} !important;
        border-radius: 15px !important;
        height: 80px !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }}
    div.stButton > button:hover {{
        background-color: {GOLD} !important;
        color: {BG} !important;
    }}
    div.stButton > button[data-testid="baseButton-primary"] {{
        background-color: {GOLD} !important;
        color: black !important;
    }}
    label p, label div {{
        color: {GOLD} !important;
        font-weight: bold !important;
    }}
    .section-label {{
        color: {GOLD};
        font-size: 14px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }}
</style>
""", unsafe_allow_html=True)

# --- POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ==========================================
# POČETNA STRANA
# ==========================================
if st.session_state.stranica == "pocetna":
    img_b64 = get_base64_img("kazan.png")
    slika_html = (
        f'<img src="data:image/png;base64,{img_b64}" width="120" style="margin-top:10px;" />'
        if img_b64 else '<div style="font-size:60px;">⚗️</div>'
    )
    ikona_teme = "☀️" if st.session_state.theme_mode == "dark" else "🌙"

    st.markdown(f"""
        <div class="flet-header">
            <p class="flet-title">RAKIJA MASTER PRO</p>
            {slika_html}
        </div>
    """, unsafe_allow_html=True)

    if st.button(f"{ikona_teme} Promeni temu", use_container_width=True):
        st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"
        st.rerun()

    st.markdown('<p class="section-label">🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇 Komina", use_container_width=True): idi_na("komina")
    with c2:
        if st.button("🦠 Kvasci", use_container_width=True): idi_na("kvasci")

    st.markdown('<p class="section-label">🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️ Prvenac", use_container_width=True): idi_na("prvenac")
    with c4:
        if st.button("🏁 Patoka", use_container_width=True): idi_na("patoka")

    c5, c6 = st.columns(2)
    with c5:
        if st.button("💧 Razblaživanje", use_container_width=True): idi_na("razblazivanje")
    with c6:
        if st.button("🌡️ Temperatura", use_container_width=True): idi_na("temperatura")

    st.markdown('<p class="section-label">⚖️ KUPAŽA I ODLEŽAVANJE</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if st.button("⚖️ Kupaža", use_container_width=True): idi_na("kupaza")
    with c8:
        if st.button("🪵 Bure", use_container_width=True): idi_na("bure")

    st.markdown('<p class="section-label">📖 ARHIVA I LINKOVI</p>', unsafe_allow_html=True)
    c9, c10 = st.columns(2)
    with c9:
        if st.button("📖 Dnevnik", use_container_width=True): idi_na("dnevnik")
    with c10:
        if st.button("🔗 Linkovi", use_container_width=True): idi_na("linkovi")

# ==========================================
# OSTALE STRANICE
# ==========================================
else:
    def naslov_alata(tekst, podnaslov=""):
        st.markdown(f"<h2 style='color:{GOLD}; font-size:24px; font-weight:bold; margin-bottom:0;'>{tekst}</h2>", unsafe_allow_html=True)
        if podnaslov:
            st.markdown(f"<p style='color:{TXT}; font-size:14px; font-style:italic;'>{podnaslov}</p>", unsafe_allow_html=True)
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
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
            st.error(f"ODVOJITI: {u*p:.2f} L")

    elif st.session_state.stranica == "razblazivanje":
        naslov_alata("💧 RAZBLAŽIVANJE", "Postepeno dodavanje destilovane vode u rakiju.")
        v = st.number_input("Litraža (L)", value=10.0, step=0.5)
        j1 = st.number_input("Trenutna %", value=65.0, step=0.5)
        j2 = st.number_input("Željena %", value=42.0, step=0.5)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            vd = v * (j1/j2 - 1)
            st.success(f"DODATI VODE: {vd:.2f} L")

    elif st.session_state.stranica == "temperatura":
        naslov_alata("🌡️ TEMPERATURA", "Korekcija očitane jačine na standardnih 20°C.")
        j = st.number_input("Jačina %", value=45.0, step=0.5)
        t = st.number_input("Temp °C", value=15.0, step=1.0)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            s = j + (20 - t) * 0.3
            st.warning(f"STVARNA JAČINA: {s:.1f}%")

    elif st.session_state.stranica == "patoka":
        naslov_alata("🏁 PATOKA", "Trenutak kada se prekida hvatanje srca rakije.")
        v = st.selectbox("Voće", ["Šljiva", "Dunja", "Jabuka"])
        if st.button("SAVET", type="primary", use_container_width=True):
            s = {
                "Šljiva": "Prekidaj na 40-45% na luli.",
                "Dunja": "Prekidaj na 45-50% na luli.",
                "Jabuka": "Prekidaj na oko 42%."
            }
            st.info(s[v])

    elif st.session_state.stranica == "kupaza":
        naslov_alata("⚖️ KUPAŽA", "Mešanje dve različite rakije radi ujednačavanja.")
        c1, c2 = st.columns(2)
        with c1: v1 = st.number_input("L1 (Litri)", value=10.0, step=1.0)
        with c2: j1 = st.number_input("Jačina 1 (%)", value=60.0, step=1.0)
        c3, c4 = st.columns(2)
        with c3: v2 = st.number_input("L2 (Litri)", value=5.0, step=1.0)
        with c4: j2 = st.number_input("Jačina 2 (%)", value=40.0, step=1.0)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            uk = v1 + v2
            n = (v1*j1 + v2*j2) / uk if uk > 0 else 0
            st.success(f"Ukupno: {uk}L | Jačina: {n:.1f}%")

    elif st.session_state.stranica == "bure":
        naslov_alata("🪵 BURE", "Proračun zapremine drvenog bureta.")
        h = st.number_input("Visina (cm)", value=70.0, step=1.0)
        ds = st.number_input("Sredina (cm)", value=60.0, step=1.0)
        dk = st.number_input("Dno (cm)", value=50.0, step=1.0)
        if st.button("IZRAČUNAJ", type="primary", use_container_width=True):
            vol = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
            st.info(f"Zapremina: oko {vol:.1f} L")

    elif st.session_state.stranica == "dnevnik":
        naslov_alata("📖 DNEVNIK RADA")
        c1, c2 = st.columns(2)
        with c1: f_i = st.text_input("Voće", "Šljiva")
        with c2: f_g = st.text_input("Godina", "2024")
        c3, c4 = st.columns(2)
        with c3: f_k = st.text_input("Kg", "500")
        with c4: f_dat = st.text_input("Datum", datetime.now().strftime("%d.%m"))
        c5, c6 = st.columns(2)
        with c5: f_l = st.text_input("Litri", "50")
        with c6: f_j = st.text_input("Jačina %", "42")
        if st.button("SAČUVAJ U ARHIVU", type="primary", use_container_width=True):
            if f_i:
                st.session_state.dnevnik.append({
                    "ime": f_i, "godina": f_g, "kg": f_k,
                    "datum": f_dat, "litara": f_l, "jacina": f_j
                })
                sacuvaj_podatke(st.session_state.dnevnik)
                st.rerun()
        st.divider()
        for i, s in enumerate(reversed(st.session_state.dnevnik)):
            idx = len(st.session_state.dnevnik) - 1 - i
            rc1, rc2 = st.columns([8, 2])
            with rc1:
                st.markdown(f"""
                <div style="background-color:{CARD}; padding:15px; border-radius:10px; border:1px solid {GOLD};">
                    <strong style="color:{GOLD};">{s.get('ime','-')} ({s.get('godina','-')})</strong><br>
                    <span style="color:{TXT};">{s.get('kg','-')}kg | {s.get('datum','-')} | {s.get('litara','-')}L | {s.get('jacina','-')}%</span>
                </div>
                """, unsafe_allow_html=True)
            with rc2:
                st.markdown('<div class="del-btn">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.dnevnik.pop(idx)
                    sacuvaj_podatke(st.session_state.dnevnik)
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif st.session_state.stranica == "linkovi":
        naslov_alata("🔗 KORISNI LINKOVI", "Preporučeni sajtovi, prodavnice i udruženja.")
        def link_dugme(tekst, ikona, url):
            st.markdown(f'''
            <a href="{url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:{GOLD}; color:black; padding:15px; border-radius:10px; 
                display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:10px; font-weight:bold;">
                    <span style="font-size:24px;">{ikona}</span>
                    <span style="font-size:16px;">{tekst}</span>
                </div>
            </a>
            ''', unsafe_allow_html=True)
        link_dugme("Knjiga: Rakijski kod", "📘", "https://www.facebook.com/rakijskikod/?locale=sr_RS")
        link_dugme("Rakija iz rakije", "🥂", "https://www.rakijaizrakije.com")
        link_dugme("Savez proizvođača rakija", "🤝", "https://savezrakija.rs")
        link_dugme("Rakija Shop", "🛒", "https://rakijashop.eu/srb/")
        link_dugme("Čiča Zlajina Rakija", "🏺", "https://cicazlajinarakija.rs")
        
        st.divider()
        st.markdown(f"<p style='color:{GOLD}; font-size:18px; font-weight:bold;'>📅 DOGAĐAJI</p>", unsafe_allow_html=True)
        link_dugme("18.04.2024. Hajdučki festival", "📍", "https://www.facebook.com/p/Хајдучки-фестивал-ракије-Богатић-Hajdučki-festival-rakije-Bogatić-61584019897579/")

    st.divider()
    if st.button("⬅ NAZAD NA MENI", use_container_width=True):
        idi_na("pocetna")
