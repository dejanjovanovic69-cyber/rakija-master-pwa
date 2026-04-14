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
    st.error("PROBNI PERIOD ISTEKAO. Kontaktirajte administratora.")
    st.stop()

# --- 3. INICIJALIZACIJA SESIJE I PODATAKA ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'

if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik = []

# --- 4. TEŠKA ARTILJERIJA CSS-a (BRIŠE IKONICE I SREĐUJE IZGLED) ---
st.markdown("""
    <style>
    /* POTPUNO SAKRIVANJE STREAMLIT BRENDINGA I IKONICA */
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
    .st-emotion-cache-15zrgzn {display: none !important;}
    a[href^="https://streamlit.io"] {display: none !important; opacity: 0 !important; pointer-events: none !important;}
    
    /* Margine ekrana za mobilni */
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
    
    /* Tamna tema */
    .stApp { background-color: #121212; color: #ffffff; }

    /* Naslovni blok (Zlatni Header) */
    .header-box {
        text-align: center;
        padding: 40px 10px 20px 10px;
        background: linear-gradient(to bottom, #D4AF37, #8B6E02);
        margin: -20px -20px 20px -20px;
        border-radius: 0 0 40px 40px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
    }
    
    /* Dizajn dugmića (Android stil) */
    div[data-testid="stButton"] > button {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a) !important;
        color: #D4AF37 !important;
        border: 1px solid #444 !important;
        border-radius: 15px !important;
        height: 80px !important;
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
        font-size: 14px !important;
    }

    label, .stMarkdown p { color: #eeeeee !important; }
    
    /* Input polja */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. POMOĆNE FUNKCIJE ---
def idi_na(strana):
    st.session_state.stranica = strana
    st.rerun()

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    return ""

# ==========================================
# --- POČETNI EKRAN (DASHBOARD) ---
# ==========================================
if st.session_state.stranica == 'pocetna':
    img_src = get_image_base64("kazan.png")
    image_html = f'<img src="{img_src}" width="140" style="margin-bottom: 15px;">' if img_src else '<div style="font-size: 60px; margin-bottom: 10px;">⚗️</div>'

    st.markdown(f"""
        <div class="header-box">
            {image_html}
            <h1 style='color: white; margin:0; font-size: 28px;'>RAKIJA MASTER PRO</h1>
            <p style='color: #eee; font-style: italic; font-size: 14px;'>Premium Distillery Tools</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-bottom:5px;'>🟢 UKOMLJAVANJE</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇 Šećer i Alk.", key="btn_secer"): idi_na('secer')
    with c2:
        if st.button("🦠 Kvasci", key="btn_kvasci"): idi_na('kvasci')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>🔥 DESTILACIJA</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️ Prvenac", key="btn_prvenac"): idi_na('prvenac')
        if st.button("💧 Razblaživanje", key="btn_razblaz"): idi_na('razblazivanje')
        if st.button("⚖️ Kupažiranje", key="btn_kupaza"): idi_na('kupaza')
    with c4:
        if st.button("🏁 Patoka (Srce)", key="btn_patoka"): idi_na('patoka')
        if st.button("🌡️ Temperatura", key="btn_temp"): idi_na('temperatura')
        if st.button("🪵 Bure (Litri)", key="btn_bure"): idi_na('bure')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>🏺 EVIDENCIJA & LINKOVI</p>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("📖 Dnevnik", key="btn_dnevnik"): idi_na('dnevnik')
    with c6:
        if st.button("🔗 Linkovi", key="btn_linkovi"): idi_na('linkovi')

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI", key="btn_back"):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")

    # 1. ŠEĆER
    if st.session_state.stranica == 'secer':
        st.subheader("🍇 Analiza komine")
        brix = st.slider("Izmeren šećer (% Brix):", 0.0, 30.0, 18.0, 0.5)
        st.info(f"**Babo:** {brix*0.85:.1f}° | **Oechsle:** {brix*4.25:.0f}°")
        st.success(f"**Potencijalni alkohol:** oko {brix*0.55:.1f} % vol")

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
        st.info("💡 Pravilo majstora: Prekidaj hvatanje srca čim osetiš tupi miris na vosak ili travu.")

    # 5. RAZBLAŽIVANJE
    elif st.session_state.stranica == 'razblazivanje':
        st.subheader("💧 Razblaživanje")
        v_r = st.number_input("Litraža rakije (L):", value=10.0)
        j1 = st.number_input("Trenutna jačina (%):", value=65.0)
        j2 = st.number_input("Željena jačina (%):", value=42.0)
        if j1 > j2:
            voda = v_r * (j1 / j2 - 1)
            st.success(f"**DODATI DESTILOVANE VODE: {voda:.2f} L**")
        else:
            st.warning("Željena jačina mora biti manja od trenutne.")

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
                    "ime": f_ime, 
                    "godina": f_god, 
                    "kg": f_kg, 
                    "litara": f_lit, 
                    "jacina": f_jac, 
                    "datum": datetime.now().strftime("%d.%m")
                })
                st.success("Uspešno sačuvano!")
        
        st.write("### 🗄️ Arhiva")
        if not st.session_state.dnevnik:
            st.info("Dnevnik je prazan.")
        else:
            for s in reversed(st.session_state.dnevnik):
                st.markdown(f"""
                <div style='background-color:#1e1e1e; padding:15px; border-radius:10px; margin-bottom:10px; border-left:5px solid #D4AF37;'>
                    <strong style='color:#D4AF37;'>{s['ime']} ({s['godina']})</strong><br>
                    Voće: {s['kg']}kg | Litara: {s['litara']}L | Jačina: {s['jacina']}% | Datum: {s['datum']}
                </div>
                """, unsafe_allow_html=True)

    # 10. LINKOVI
    elif st.session_state.stranica == 'linkovi':
        st.subheader("🔗 Korisni Linkovi")
        st.markdown("[📘 Knjiga: Rakijski kod](https://www.facebook.com/rakijskikod/)")
        st.markdown("[🥂 Rakija iz rakije](https://www.rakijaizrakije.com)")
        st.markdown("[🤝 Savez proizvođača rakija](https://savezrakija.rs)")
        st.markdown("[🛒 Rakija Shop](https://rakijashop.eu/srb/)")
        st.divider()
        st.write("**📅 DOGAĐAJI:**")
        st.write("18.04.2024. Prvi Hajdučki festival rakije - Bogatić")
        st.markdown("[📍 Lokacija na mapi](https://www.google.com/maps/search/?api=1&query=44.834296,19.480729)")

st.markdown("<br><p style='text-align: center; color: #555; font-size:12px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
