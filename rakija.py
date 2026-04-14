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

# --- 3. CSS ZA IDENTIČAN IZGLED KAO NA SLICI (ŠIROKI TASTERI, TAMNA TEMA) ---
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
    .block-container { padding: 0 !important; max-width: 500px !important; margin: auto; }

    /* ZLATNI GRADIENT HEADER (IDENTIČAN SLICI) */
    .header-box {
        text-align: center;
        padding: 60px 20px 40px 20px;
        background: linear-gradient(to bottom, #D4AF37, #8B6E02);
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 60px 60px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.6);
    }
    .header-title {
        color: white;
        font-size: 38px;
        font-weight: 900;
        margin: 15px 0 5px 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .header-subtitle {
        color: #f0f0f0;
        font-style: italic;
        font-size: 15px;
        opacity: 0.9;
    }

    /* SEKCIJE (Naslovi sa emojijima) */
    .section-label {
        color: #ffffff;
        font-size: 16px;
        font-weight: bold;
        margin: 30px 0 15px 15px;
        display: flex;
        align-items: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* TASTERI (Široki, tamno sivi, zaobljeni - KAO NA SLICI) */
    div[data-testid="stButton"] > button {
        background-color: #262626 !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        height: 70px !important;
        width: 100% !important;
        font-size: 17px !important;
        font-weight: 500 !important;
        transition: 0.2s !important;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.3) !important;
        margin-bottom: 5px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        border-color: #D4AF37 !important;
        background-color: #2d2d2d !important;
    }

    div[data-testid="stButton"] > button:active {
        background-color: #D4AF37 !important;
        color: #121212 !important;
        transform: scale(0.97) !important;
    }

    /* Dugme za NAZAD */
    .btn-nazad div[data-testid="stButton"] > button {
        height: 50px !important;
        background-color: transparent !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
        font-size: 15px !important;
        margin: 15px !important;
        width: calc(100% - 30px) !important;
    }

    /* Input polja i forme */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 12px !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    label { color: #D4AF37 !important; font-weight: bold !important; margin-left: 5px; }
    
    /* Razmak između kolona */
    [data-testid="column"] {
        padding: 0 8px !important;
    }
    
    /* Alert poruke */
    .stAlert { background-color: #1e1e1e !important; border: 1px solid #D4AF37 !important; color: white !important; border-radius: 15px !important; }
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
    # Header sa slikom i gradijentom (TAČNO KAO NA SLICI)
    img_b64 = get_image_base64("kazan.png")
    img_html = f'<img src="data:image/png;base64,{img_b64}" width="160">' if img_b64 else '<div style="font-size: 90px;">⚗️</div>'

    st.markdown(f"""
        <div class="header-box">
            {img_html}
            <h1 class="header-title">RAKIJA MASTER</h1>
            <p class="header-subtitle">Premium Distillery Tools</p>
        </div>
    """, unsafe_allow_html=True)

    # 🟢 UKOMLJAVANJE
    st.markdown('<p class="section-label">🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇 Šećer i Alk.", key="d_secer"): idi_na('secer')
    with c2:
        if st.button("🦠 Kvasci", key="d_kvasci"): idi_na('kvasci')

    # 🔥 DESTILACIJA
    st.markdown('<p class="section-label">🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️ Prvenac", key="d_prvenac"): idi_na('prvenac')
        if st.button("💧 Razblaživanje", key="d_razblaz"): idi_na('razblazivanje')
        if st.button("⚖️ Kupažiranje", key="d_kupaza"): idi_na('kupaza')
    with c4:
        if st.button("🏁 Patoka (Srce)", key="d_patoka"): idi_na('patoka')
        if st.button("🌡️ Temperatura", key="d_temp"): idi_na('temperatura')

    # 🏺 ODLEŽAVANJE & EVIDENCIJA
    st.markdown('<p class="section-label">🏺 ODLEŽAVANJE & EVIDENCIJA</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("🪵 Bure (Litri)", key="d_bure"): idi_na('bure')
        if st.button("🔗 Korisni Linkovi", key="d_linkovi"): idi_na('linkovi')
    with c6:
        if st.button("📖 Dnevnik", key="d_dnevnik"): idi_na('dnevnik')

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI"):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")

    # 1. ŠEĆER (Brix -> Babo/Oechsle)
    if st.session_state.stranica == 'secer':
        st.subheader("🍇 Analiza komine")
        brix = st.number_input("Šećer u komini (% Brix):", value=18.0, step=0.1)
        st.info(f"**Babo:** {brix*0.85:.1f}° | **Oechsle:** {brix*4.25:.0f}°")
        st.success(f"**Potencijalni alkohol:** {brix*0.55:.1f}% vol")

    # 2. KVASCI
    elif st.session_state.stranica == 'kvasci':
        st.subheader("🦠 Kvasci i Enzimi")
        kg = st.number_input("Količina voća (kg):", value=100)
        st.warning(f"**Receptura:**\n- Enzim: {(kg/100)*2:.1f}g\n- Kvasac: {(kg/100)*25:.1f}g\n- Hrana: {(kg/100)*25:.1f}g")

    # 3. PRVENAC
    elif st.session_state.stranica == 'prvenac':
        st.subheader("✂️ Odvajanje prvenca")
        v = st.selectbox("Voće:", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        l = st.number_input("Meka rakija (L):", value=100)
        p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
        st.error(f"**ODVOJITI PRVENCA: {l*p:.2f} L**")

    # 4. PATOKA
    elif st.session_state.stranica == 'patoka':
        st.subheader("🏁 Presek: Odvajanje Patoke")
        voce = st.selectbox("Vrsta voća:", ["Šljiva", "Kajsija / Breskva", "Dunja", "Jabuka / Kruška", "Grožđe"])
        savet = {"Šljiva": "40-45% na luli", "Kajsija / Breskva": "45-50% na luli", "Dunja": "45-50% na luli", "Jabuka / Kruška": "40-42% na luli", "Grožđe": "35-40% na luli"}
        st.error(f"Kada jačina **NA LULI** padne na: **{savet[voce]}**")

    # 5. RAZBLAŽIVANJE
    elif st.session_state.stranica == 'razblazivanje':
        st.subheader("💧 Razblaživanje")
        v_r = st.number_input("Litraža rakije (L):", value=10.0)
        j1 = st.number_input("Trenutna jačina (%):", value=65.0)
        j2 = st.number_input("Željena jačina (%):", value=42.0)
        if j1 > j2:
            voda = v_r * (j1 / j2 - 1)
            st.success(f"**DODATI DESTILOVANE VODE: {voda:.2f} L**")

    # 6. TEMPERATURA
    elif st.session_state.stranica == 'temperatura':
        st.subheader("🌡️ Korekcija temperature")
        j_izm = st.number_input("Očitana jačina %:", value=45.0)
        t_izm = st.number_input("Temperatura destilata °C:", value=15.0)
        stvarna = j_izm + (20 - t_izm) * 0.3
        st.warning(f"**Stvarna jačina (na 20°C): {stvarna:.1f}% vol**")

    # 7. KUPAŽA
    elif st.session_state.stranica == 'kupaza':
        st.subheader("⚖️ Kupažiranje")
        v1, j1 = st.number_input("Rakija 1 (L):", value=10.0), st.number_input("Jačina 1 (%):", value=60.0)
        v2, j2 = st.number_input("Rakija 2 (L):", value=5.0), st.number_input("Jačina 2 (%):", value=40.0)
        if (v1 + v2) > 0:
            nova = (v1 * j1 + v2 * j2) / (v1 + v2)
            st.success(f"**Ukupno: {v1+v2}L | Jačina kupaže: {nova:.1f}%**")

    # 8. BURE
    elif st.session_state.stranica == 'bure':
        st.subheader("🪵 Zapremina bureta")
        h_b = st.number_input("Visina (cm):", value=70.0)
        ds_b = st.number_input("Prečnik sredina (cm):", value=60.0)
        dk_b = st.number_input("Prečnik dno (cm):", value=50.0)
        zapremina = (math.pi * h_b / 12 * (2 * ds_b**2 + dk_b**2)) / 1000
        st.success(f"**Zapremina: oko {zapremina:.1f} Litara**")

    # 9. DNEVNIK
    elif st.session_state.stranica == 'dnevnik':
        st.subheader("📖 Digitalni Dnevnik")
        with st.expander("➕ Dodaj novi unos", expanded=True):
            f_ime = st.text_input("Voće", "Šljiva")
            f_god = st.text_input("Godina", "2024")
            f_kg = st.number_input("Količina (kg)", value=500)
            f_lit = st.number_input("Dobijeno litara", value=50)
            f_jac = st.number_input("Jačina (%)", value=42)
            if st.button("💾 SAČUVAJ U ARHIVU"):
                st.session_state.dnevnik.append({
                    "ime": f_ime, "godina": f_god, "kg": f_kg, 
                    "litara": f_lit, "jacina": f_jac, 
                    "datum": datetime.now().strftime("%d.%m")
                })
                st.success("Uspešno sačuvano!")
        
        for s in reversed(st.session_state.dnevnik):
            st.markdown(f"""
            <div style='background-color:#1e1e1e; padding:15px; border-radius:12px; margin-bottom:10px; border-left:5px solid #D4AF37;'>
                <strong style='color:#D4AF37;'>{s['ime']} ({s['godina']})</strong><br>
                {s['kg']}kg | {s['litara']}L | {s['jacina']}% | {s['datum']}
            </div>
            """, unsafe_allow_html=True)

    # 10. LINKOVI
    elif st.session_state.stranica == 'linkovi':
        st.subheader("🔗 Korisni Linkovi")
        st.markdown("[📘 Knjiga: Rakijski kod](https://www.facebook.com/rakijskikod/)")
        st.markdown("[🥂 Rakija iz rakije](https://www.rakijaizrakije.com)")
        st.markdown("[🤝 Savez proizvođača rakija](https://savezrakija.rs)")
        st.divider()
        st.write("**📅 DOGAĐAJI:**")
        st.write("18.04.2024. Prvi Hajdučki festival rakije - Bogatić")

st.markdown("<br><p style='text-align: center; color: #555; font-size:12px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
