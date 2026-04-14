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

# --- 3. BRUTALAN CSS ZA IDENTIČAN IZGLED KAO FLET VERZIJA ---
st.markdown("""
    <style>
    /* SAKRIVANJE SVEGA OD STREAMLIT-A */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stFooter"] {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    
    /* Pozadina i fontovi */
    .stApp { background-color: #121212; color: #ffffff; font-family: 'sans-serif'; }
    .block-container { padding-top: 0rem; padding-bottom: 5rem; max-width: 450px; }

    /* ZLATNI HEADER (Kao u Fletu) */
    .header-container {
        text-align: center;
        padding: 30px 10px;
        background-color: #D4AF37;
        margin: -1rem -1rem 1rem -1rem;
        border-radius: 0 0 35px 35px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
    }
    .header-title {
        color: white;
        font-size: 24px;
        font-weight: 900;
        margin: 0;
        letter-spacing: 1px;
    }

    /* SEKCIJE (Naslovi) */
    .section-label {
        color: #D4AF37;
        font-size: 14px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* DUGMIĆI (Kvadratni, identični Fletu) */
    div[data-testid="stButton"] > button {
        background-color: #1e1e1e !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 15px !important;
        height: 100px !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px !important;
        transition: 0.3s !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        border-color: #ffffff !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stButton"] > button:active {
        background-color: #D4AF37 !important;
        color: #121212 !important;
        transform: scale(0.95) !important;
    }

    /* Tekst unutar dugmeta */
    .btn-text {
        font-size: 12px;
        font-weight: bold;
        margin-top: 5px;
    }
    .btn-icon {
        font-size: 30px;
    }

    /* Dugme NAZAD */
    .btn-nazad div[data-testid="stButton"] > button {
        height: 45px !important;
        background-color: transparent !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
        font-size: 14px !important;
    }

    /* Input polja */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    label { color: #D4AF37 !important; font-size: 13px !important; }
    
    /* Rezultati */
    .stAlert { background-color: #1e1e1e !important; border: 1px solid #D4AF37 !important; color: white !important; }
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
    # Header sa slikom (ako postoji) ili emojijem
    img_b64 = get_image_base64("kazan.png")
    if img_b64:
        header_content = f'<img src="data:image/png;base64,{img_b64}" width="120" style="margin-bottom:10px;">'
    else:
        header_content = '<div style="font-size: 70px; margin-bottom: 10px;">⚗️</div>'

    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-title">RAKIJA MASTER PRO</h1>
            <div style="margin-top:15px;">{header_content}</div>
        </div>
    """, unsafe_allow_html=True)

    # Sekcije i dugmići
    st.markdown('<p class="section-label">🟢 UKOMLJAVANJE</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇\nKomina", key="btn_komina"): idi_na('komina')
    with c2:
        if st.button("🦠\nKvasci", key="btn_kvasci"): idi_na('kvasci')

    st.markdown('<p class="section-label">🔥 DESTILACIJA</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️\nPrvenac", key="btn_prvenac"): idi_na('prvenac')
        if st.button("💧\nRazblaživanje", key="btn_razblaz"): idi_na('razblazivanje')
    with c4:
        if st.button("🏁\nPatoka", key="btn_patoka"): idi_na('patoka')
        if st.button("🌡️\nTemperatura", key="btn_temp"): idi_na('temperatura')

    st.markdown('<p class="section-label">⚖️ KUPAŽA I BURE</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("⚖️\nKupaža", key="btn_kupaza"): idi_na('kupaza')
    with c6:
        if st.button("🪵\nBure", key="btn_bure"): idi_na('bure')

    st.markdown('<p class="section-label">📖 ARHIVA</p>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📖\nDnevnik", key="btn_dnevnik"): idi_na('dnevnik')
    with c8:
        if st.button("🔗\nLinkovi", key="btn_linkovi"): idi_na('linkovi')

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI"):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)

    # 1. KOMINA
    if st.session_state.stranica == 'komina':
        st.markdown("<h2 style='color:#D4AF37;'>🍇 ANALIZA KOMINE</h2>", unsafe_allow_html=True)
        st.write("*Brix meri šećer. Babo i Oechsle mere gustinu šire.*")
        brix = st.number_input("Šećer u komini (% Brix):", value=18.0, step=0.1)
        st.info(f"**Babo:** {brix*0.85:.1f}° | **Oechsle:** {brix*4.25:.0f}°")
        st.success(f"**Potencijalni alkohol:** {brix*0.55:.1f}% vol")

    # 2. KVASCI
    elif st.session_state.stranica == 'kvasci':
        st.markdown("<h2 style='color:#D4AF37;'>🦠 KVASCI I ENZIMI</h2>", unsafe_allow_html=True)
        st.write("*Enzimi, kvasci i hrana osiguravaju čisto vrenje.*")
        kg = st.number_input("Količina voća (kg):", value=100)
        st.warning(f"**Receptura:**\n\n- Enzim: {(kg/100)*2:.1f}g\n- Kvasac: {(kg/100)*25:.1f}g\n- Hrana: {(kg/100)*25:.1f}g")

    # 3. PRVENAC
    elif st.session_state.stranica == 'prvenac':
        st.markdown("<h2 style='color:#D4AF37;'>✂️ PRVENAC</h2>", unsafe_allow_html=True)
        st.write("*Odvajanje metila na početku prepeka.*")
        v = st.selectbox("Voće:", ["Šljiva (1%)", "Dunja (1.5%)", "Ostalo (1.2%)"])
        l = st.number_input("Meka rakija (L):", value=100)
        p = 0.015 if "Dunja" in v else (0.012 if "Ostalo" in v else 0.01)
        st.error(f"**ODVOJITI: {l*p:.2f} L**")

    # 4. RAZBLAŽIVANJE
    elif st.session_state.stranica == 'razblazivanje':
        st.markdown("<h2 style='color:#D4AF37;'>💧 RAZBLAŽIVANJE</h2>", unsafe_allow_html=True)
        st.write("*Postepeno dodavanje destilovane vode u rakiju.*")
        v = st.number_input("Litraža (L):", value=10.0)
        j1 = st.number_input("Trenutna jačina (%):", value=65.0)
        j2 = st.number_input("Željena jačina (%):", value=42.0)
        if j1 > j2:
            vd = v * (j1/j2 - 1)
            st.success(f"**DODATI VODE: {vd:.2f} L**")

    # 5. TEMPERATURA
    elif st.session_state.stranica == 'temperatura':
        st.markdown("<h2 style='color:#D4AF37;'>🌡️ TEMPERATURA</h2>", unsafe_allow_html=True)
        st.write("*Korekcija očitane jačine na standardnih 20°C.*")
        j = st.number_input("Jačina %:", value=45.0)
        t = st.number_input("Temp °C:", value=15.0)
        s = j + (20 - t) * 0.3
        st.warning(f"**STVARNA JAČINA: {s:.1f}%**")

    # 6. PATOKA
    elif st.session_state.stranica == 'patoka':
        st.markdown("<h2 style='color:#D4AF37;'>🏁 PATOKA</h2>", unsafe_allow_html=True)
        st.write("*Trenutak kada se prekida hvatanje srca rakije.*")
        v = st.selectbox("Voće:", ["Šljiva", "Dunja", "Jabuka", "Kajsija / Breskva", "Grožđe"])
        saveti = {
            "Šljiva": "Prekidaj na 40-45% na luli. Ispod 40% izlaze teški alkoholi.",
            "Dunja": "Prekidaj na 45-50% na luli. Aromatično voće brzo gubi fine arome.",
            "Kajsija / Breskva": "Prekidaj na 45-50% na luli. Reži ranije!",
            "Jabuka": "Prekidaj na oko 40-42%. Pazi na miris 'na vosak'.",
            "Grožđe": "Prekidaj na 35-40% na luli."
        }
        st.info(saveti[v])

    # 7. KUPAŽA
    elif st.session_state.stranica == 'kupaza':
        st.markdown("<h2 style='color:#D4AF37;'>⚖️ KUPAŽA</h2>", unsafe_allow_html=True)
        st.write("*Mešanje dve različite rakije radi ujednačavanja.*")
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
            st.success(f"**Ukupno: {uk}L | Jačina: {n:.1f}%**")

    # 8. BURE
    elif st.session_state.stranica == 'bure':
        st.markdown("<h2 style='color:#D4AF37;'>🪵 BURE</h2>", unsafe_allow_html=True)
        st.write("*Proračun zapremine drvenog bureta.*")
        h = st.number_input("Visina (cm):", value=70.0)
        ds = st.number_input("Sredina (cm):", value=60.0)
        dk = st.number_input("Dno (cm):", value=50.0)
        v = (math.pi * h / 12 * (2 * ds**2 + dk**2)) / 1000
        st.success(f"**Zapremina: oko {v:.1f} L**")

    # 9. DNEVNIK
    elif st.session_state.stranica == 'dnevnik':
        st.markdown("<h2 style='color:#D4AF37;'>📖 DNEVNIK RADA</h2>", unsafe_allow_html=True)
        with st.expander("➕ DODAJ NOVI UNOS", expanded=True):
            f_ime = st.text_input("Voće", "Šljiva")
            f_god = st.text_input("Godina", "2024")
            f_kg = st.number_input("Količina (kg)", value=500)
            f_dat = st.text_input("Datum", datetime.now().strftime("%d.%m"))
            f_lit = st.number_input("Dobijeno litara", value=50)
            f_jac = st.number_input("Jačina (%)", value=42)
            if st.button("SAČUVAJ U ARHIVU"):
                st.session_state.dnevnik.append({
                    "ime": f_ime, "godina": f_god, "kg": f_kg, 
                    "datum": f_dat, "litara": f_lit, "jacina": f_jac
                })
                st.success("Uspešno sačuvano!")

        st.write("---")
        for i, s in enumerate(reversed(st.session_state.dnevnik)):
            st.markdown(f"""
            <div style='background-color:#1e1e1e; padding:15px; border-radius:15px; margin-bottom:10px; border:1px solid #D4AF37;'>
                <strong style='color:#D4AF37; font-size:16px;'>{s['ime']} ({s['godina']})</strong><br>
                <span style='color:#ccc; font-size:13px;'>{s['kg']}kg | {s['datum']} | {s['litara']}L | {s['jacina']}%</span>
            </div>
            """, unsafe_allow_html=True)

    # 10. LINKOVI
    elif st.session_state.stranica == 'linkovi':
        st.markdown("<h2 style='color:#D4AF37;'>🔗 LINKOVI I DOGAĐAJI</h2>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background-color:#1e1e1e; padding:20px; border-radius:15px; border:1px solid #D4AF37;'>
                <p><a href='https://www.facebook.com/rakijskikod/' style='color:#D4AF37; text-decoration:none; font-weight:bold;'>📘 Knjiga: Rakijski kod</a></p>
                <p><a href='https://www.rakijaizrakije.com' style='color:#D4AF37; text-decoration:none; font-weight:bold;'>🥂 Rakija iz rakije</a></p>
                <p><a href='https://savezrakija.rs' style='color:#D4AF37; text-decoration:none; font-weight:bold;'>🤝 Savez proizvođača rakija</a></p>
                <hr style='border-color:#444;'>
                <p style='color:#D4AF37; font-weight:bold;'>📅 DOGAĐAJI</p>
                <p style='font-size:14px;'>18.04.2024. Prvi Hajdučki festival rakije - Bogatić</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #555; font-size:10px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
