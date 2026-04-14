import streamlit as st
from datetime import datetime
import math
import base64
import os
import json

# --- 1. KONFIGURACIJA I AKTIVACIJA ---
st.set_page_config(page_title="Rakija Master Pro", page_icon="🥃", layout="centered")

DATUM_ISTEKA = datetime(2026, 12, 31) 
if datetime.now() > DATUM_ISTEKA:
    st.error("PROBNI PERIOD ISTEKAO")
    st.stop()

# --- 2. ČUVANJE PODATAKA (DNEVNIK) ---
FILE_PATH = "dnevnik_podaci.json"

def ucitaj_podatke():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return[]

def sacuvaj_podatke(lista):
    with open(FILE_PATH, "w", encoding="utf-8") as f: json.dump(lista, f, indent=4, ensure_ascii=False)

# --- 3. INICIJALIZACIJA SESIJE ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'
if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik = ucitaj_podatke()

# Boje tačno kao u Flet-u
if st.session_state.theme_mode == 'dark':
    GOLD = "#D4AF37"
    BG = "#121212"
    TXT = "white"
    CARD = "#1e1e1e"
else:
    GOLD = "#996515"
    BG = "#f8f9fa"
    TXT = "black"
    CARD = "white"

# --- 4. CSS STILIZACIJA (Kloniranje Flet izgleda) ---
st.markdown(f"""
    <style>
    /* Sakrivanje Streamlit UI elemenata */
    [data-testid="stHeader"],[data-testid="stFooter"], [data-testid="stToolbar"] {{display: none !important;}}
    #MainMenu {{visibility: hidden;}}
    
    /* Globalno */
    .stApp {{ background-color: {BG}; color: {TXT}; }}
    .block-container {{ padding: 0 !important; max-width: 450px !important; margin: auto; padding-bottom: 30px !important; }}

    /* Flet Header Klon */
    .flet-header {{
        background-color: {GOLD};
        padding: 20px 15px 20px 20px;
        text-align: center;
        border-radius: 0 0 35px 35px;
        box-shadow: 0px 1px 10px rgba(0,0,0,0.4);
        position: relative;
        margin-bottom: 20px;
    }}
    .header-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 0px;
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
        padding: 10px 0;
    }}

    /* Dugme za promenu teme */
    .theme-btn-container {{ position: absolute; top: 15px; right: 15px; z-index: 1000; }}
    .theme-btn-container button {{
        background: transparent !important;
        border: none !important;
        font-size: 24px !important;
        color: white !important;
        box-shadow: none !important;
    }}

    /* Kolone kod Početne strane - fiksiran 2 po redu grid */
    .pocetna-grid [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        padding: 0 15px !important;
    }}
    .pocetna-grid [data-testid="column"] {{
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
    }}

    /* Grid tasteri alata */
    div.stButton > button[data-testid="baseButton-secondary"] {{
        width: 100% !important;
        height: 90px !important;
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
        box-shadow: none !important;
        padding: 0 !important;
    }}
    div.stButton > button[data-testid="baseButton-secondary"] p {{
        margin: 0 !important; line-height: 1.2 !important; text-align: center !important;
    }}

    /* Akcijski tasteri unutar Alata (Izračunaj / Sačuvaj) */
    div.stButton > button[data-testid="baseButton-primary"] {{
        background-color: {GOLD} !important;
        color: black !important;
        border: none !important;
        border-radius: 10px !important;
        height: 50px !important;
        font-weight: bold !important;
        width: 100% !important;
    }}

    /* Dugme Nazad i Zatvori */
    .nazad-box div.stButton > button {{
        background-color: transparent !important;
        color: {GOLD} !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 14px !important;
        font-weight: bold !important;
        justify-content: flex-start !important;
        padding-left: 0 !important;
        margin-top: 20px !important;
    }}
    .zatvori-box div.stButton > button {{
        background-color: transparent !important;
        color: red !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 20px !important;
    }}

    /* Brisanje iz dnevnika dugme */
    .delete-btn div.stButton > button {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 20px !important;
        padding: 0 !important;
    }}

    /* Naslovi sekcija */
    .section-label {{ color: {GOLD}; font-size: 14px; font-weight: bold; margin: 15px 0 5px 20px; }}

    /* Inputi */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {{
        background-color: {CARD} !important;
        color: {TXT} !important;
        border: 1px solid {GOLD} !important;
        border-radius: 10px !important;
    }}
    label {{ color: {GOLD} !important; font-weight: bold !important; font-size: 11px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

# ==========================================
# --- POČETNA STRANA (DASHBOARD) ---
# ==========================================
if st.session_state.stranica == 'pocetna':
    st.markdown('<div class="pocetna-grid">', unsafe_allow_html=True)

    img_b64 = get_base64_img("kazan.png")
    slika_html = f'<img src="data:image/png;base64,{img_b64}" width="160">' if img_b64 else '<div style="font-size:80px;">⚗️</div>'
    ikona_teme = "☀️" if st.session_state.theme_mode == "dark" else "🌙"

    # Header okruženje
    st.markdown(f"""
        <div class="flet-header">
            <div class="header-top">
                <p class="flet-title">RAKIJA MASTER PRO</p>
            </div>
            <div class="header-img-box">{slika_html}</div>
        </div>
    """, unsafe_allow_html=True)

    # Theme Toggle dugme pozicionirano CSS-om preko headera
    st.markdown('<div class="theme-btn-container">', unsafe_allow_html=True)
    if st.button(ikona_teme, key="theme_toggle"):
        st.session_state.theme_mode = 'light' if st.session_state.theme_mode == 'dark' else 'dark'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Funkcija za crtanje grid tastera
    def draw_btn(label, icon, key, target):
        if st.button(f"{icon}\n{label}", key=key): idi_na(target)

    # --- GLAVNI MENI ---
    st.markdown('<p class="section-label"> 🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: draw_btn("Komina", "🍇", "k1", "komina")
    with c2: draw_btn("Kvasci", "🦠", "k2", "kvasci")

    st.markdown('<p class="section-label"> 🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3: draw_btn("Prvenac", "✂️", "d1", "prvenac")
    with c4: draw_btn("Patoka", "🏁", "d2", "patoka")
    
    c3b, c4b = st.columns(2)
    with c3b: draw_btn("Razblaživanje", "💧", "d3", "razblazivanje")
    with c4b: draw_btn("Temperatura", "🌡️", "d4", "temperatura")

    st.markdown('<p class="section-label"> ⚖️ KUPAŽA I ODLEŽAVANJE</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5: draw_btn("Kupaža", "⚖️", "b1", "kupaza")
    with c6: draw_btn("Bure", "🪵", "b2", "bure")

    st.markdown('<p class="section-label"> 📖 ARHIVA I LINKOVI</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7: draw_btn("Dnevnik", "📖", "a1", "dnevnik")
    with c8: draw_btn("Linkovi", "🔗", "a2", "linkovi")

    st.divider()
    st.markdown('<div class="zatvori-box">', unsafe_allow_html=True)
    if st.button("ZATVORI APLIKACIJU", key="izlaz"):
        os._exit(0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Zatvaranje grid CSS-a

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    # --- POMOĆNA FUNKCIJA ZA ISPIS NASLOVA ALATA ---
    def naslov_alata(tekst, podnaslov=""):
        st.markdown(f"<h2 style='color:{GOLD}; font-size:22px; font-weight:bold; margin-bottom: 0px;'>{tekst}</h2>", unsafe_allow_html=True)
        if podnaslov:
            st.markdown(f"<p style='color:{TXT}; font-size:12px; font-style:italic;'>{podnaslov}</p>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # PADDING KONTEJNER ZA ALATE
    with st.container():
        
        if st.session_state.stranica == 'komina':
            naslov_alata("🍇 ANALIZA KOMINE", "Brix meri šećer. Babo i Oechsle mere gustinu šire.")
            u = st.number_input("Šećer u komini (% Brix)", value=18.0, step=0.1)
            if st.button("IZRAČUNAJ", type="primary"):
                st.markdown(f"<p style='color:{TXT}; font-size:15px; font-weight:bold;'>Babo: {u*0.85:.1f}° | Oechsle: {u*4.25:.0f}°<br>Potencijalni alkohol: {u*0.55:.1f}% vol</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'kvasci':
            naslov_alata("🦠 KVASCI I ENZIMI", "Enzimi, kvasci i hrana osiguravaju čisto vrenje.")
            u = st.number_input("Količina voća (kg)", value=100.0, step=1.0)
            if st.button("IZRAČUNAJ", type="primary"):
                st.markdown(f"<p style='color:{TXT}; font-size:15px; font-weight:bold;'>Enzim: {(u/100)*2:.1f}g<br>Kvasac: {(u/100)*25:.1f}g<br>Hrana: {(u/100)*25:.1f}g</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'prvenac':
            naslov_alata("✂️ PRVENAC", "Odvajanje metila na početku prepeka.")
            v = st.selectbox("Voće",["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
            u = st.number_input("Meka rakija (L)", value=100.0, step=1.0)
            if st.button("IZRAČUNAJ", type="primary"):
                p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
                st.markdown(f"<p style='color:red; font-size:16px; font-weight:bold;'>ODVOJITI: {u*p:.2f} L</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'razblazivanje':
            naslov_alata("💧 RAZBLAŽIVANJE", "Postepeno dodavanje destilovane vode u rakiju.")
            v = st.number_input("Litraža (L)", value=10.0, step=0.5)
            j1 = st.number_input("Trenutna %", value=65.0, step=0.5)
            j2 = st.number_input("Željena %", value=42.0, step=0.5)
            if st.button("IZRAČUNAJ", type="primary"):
                vd = v * (j1/j2 - 1)
                st.markdown(f"<p style='color:green; font-size:16px; font-weight:bold;'>DODATI VODE: {vd:.2f} L</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'temperatura':
            naslov_alata("🌡️ TEMPERATURA", "Korekcija očitane jačine na standardnih 20°C.")
            j = st.number_input("Jačina %", value=45.0, step=0.5)
            t = st.number_input("Temp °C", value=15.0, step=1.0)
            if st.button("IZRAČUNAJ", type="primary"):
                s = j + (20 - t) * 0.3
                st.markdown(f"<p style='color:{GOLD}; font-size:16px; font-weight:bold;'>STVARNA JAČINA: {s:.1f}%</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'patoka':
            naslov_alata("🏁 PATOKA", "Trenutak kada se prekida hvatanje srca rakije.")
            v = st.selectbox("Voće", ["Šljiva", "Dunja", "Jabuka"])
            if st.button("SAVET", type="primary"):
                s = {"Šljiva": "Prekidaj na 40-45% na luli.", "Dunja": "Prekidaj na 45-50% na luli.", "Jabuka": "Prekidaj na oko 42%."}
                st.markdown(f"<p style='color:{TXT}; font-size:15px;'>{s[v]}</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'kupaza':
            naslov_alata("⚖️ KUPAŽA", "Mešanje dve različite rakije radi ujednačavanja.")
            c1, c2 = st.columns(2)
            with c1: v1 = st.number_input("L1 (Litri)", value=10.0, step=1.0)
            with c2: j1 = st.number_input("Jačina 1 (%)", value=60.0, step=1.0)
            c3, c4 = st.columns(2)
            with c3: v2 = st.number_input("L2 (Litri)", value=5.0, step=1.0)
            with c4: j2 = st.number_input("Jačina 2 (%)", value=40.0, step=1.0)
            if st.button("IZRAČUNAJ", type="primary"):
                uk = v1 + v2
                n = (v1*j1 + v2*j2) / uk if uk > 0 else 0
                st.markdown(f"<p style='color:{TXT}; font-size:15px;'>Ukupno: {uk}L | Jačina: {n:.1f}%</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'bure':
            naslov_alata("🪵 BURE", "Proračun zapremine drvenog bureta.")
            h = st.number_input("Visina (cm)", value=70.0, step=1.0)
            ds = st.number_input("Sredina (cm)", value=60.0, step=1.0)
            dk = st.number_input("Dno (cm)", value=50.0, step=1.0)
            if st.button("IZRAČUNAJ", type="primary"):
                vol = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
                st.markdown(f"<p style='color:{TXT}; font-size:15px;'>Zapremina: oko {vol:.1f} L</p>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'dnevnik':
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
            
            if st.button("SAČUVAJ U ARHIVU", type="primary"):
                if f_i:
                    st.session_state.dnevnik.append({"ime": f_i, "godina": f_g, "kg": f_k, "datum": f_dat, "litara": f_l, "jacina": f_j})
                    sacuvaj_podatke(st.session_state.dnevnik)
                    st.rerun()
            
            st.divider()

            # Prikaz dnevnika sa opcijom brisanja (klonirano ponašanje Flet liste)
            for i, s in enumerate(reversed(st.session_state.dnevnik)):
                idx = len(st.session_state.dnevnik) - 1 - i
                rc1, rc2 = st.columns([8, 2], vertical_alignment="center")
                with rc1:
                    st.markdown(f"""
                    <div style="background-color:{CARD}; padding:10px; border-radius:10px; border:1px solid {GOLD}; line-height:1.2;">
                        <strong style="color:{GOLD}; font-size:14px;">{s.get('ime','-')} ({s.get('godina','-')})</strong><br>
                        <span style="color:{TXT}; font-size:12px;">{s.get('kg','-')}kg | {s.get('datum','-')} | {s.get('litara','-')}L | {s.get('jacina','-')}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                with rc2:
                    st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.dnevnik.pop(idx)
                        sacuvaj_podatke(st.session_state.dnevnik)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)

        elif st.session_state.stranica == 'linkovi':
            naslov_alata("🔗 KORISNI LINKOVI", "Preporučeni sajtovi, prodavnice i udruženja.")
            
            def link_dugme(tekst, ikona, url):
                st.markdown(f'''
                <a href="{url}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:{GOLD}; color:black; padding:15px; border-radius:10px; display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:5px; font-weight:bold;">
                        <span style="font-size:24px;">{ikona}</span>
                        <span style="font-size:14px;">{tekst}</span>
                    </div>
                </a>
                ''', unsafe_allow_html=True)
                
            def dogadjaj_dugme(naslov, opis, url):
                st.markdown(f'''
                <a href="{url}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:{GOLD}; color:black; padding:15px; border-radius:10px; text-align:center; margin-bottom:5px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                        <span style="font-size:14px; font-weight:bold;">{naslov}</span>
                        <span style="font-size:11px; font-style:italic;">{opis}</span>
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
            
            dogadjaj_dugme("18.04.2024. Prvi Hajdučki festival rakije", "Klikni za Facebook stranicu", "https://www.facebook.com/p/Хајдучки-фестивал-ракије-Богатић-Hajdučki-festival-rakije-Bogatić-61584019897579/")
            dogadjaj_dugme("📍 Lokacija: Mike Vitomirovića 3, Bogatić", "Klikni da otvoriš mapu", "https://www.google.com/maps/search/?api=1&query=44.834296,19.480729")

        # --- DUGME ZA POVRATAK NAZAD ---
        st.markdown('<div class="nazad-box">', unsafe_allow_html=True)
        if st.button("⬅ NAZAD NA MENI", key="back"): idi_na('pocetna')
        st.markdown('</div>', unsafe_allow_html=True)
