import streamlit as st
from datetime import datetime
import math
import base64
import os

# --- KONFIGURACIJA ---
st.set_page_config(page_title="Rakija Master Pro", page_icon="🥃", layout="centered")

# --- INICIJALIZACIJA SESIJE (NAVIGACIJA I DNEVNIK) ---
if 'stranica' not in st.session_state:
    st.session_state.stranica = 'pocetna'
if 'dnevnik' not in st.session_state:
    st.session_state.dnevnik =[]

# --- BRUTALAN CSS ZA ANDROID IZGLED (SA TEŠKOM ARTILJERIJOM ZA STREAMLIT) ---
st.markdown("""
    <style>
    /* TOTALNO SAKRIVANJE STREAMLIT BRENDINGA I MENIJA */
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}[data-testid="stToolbar"] {display: none !important;}

    /* SAKRIVANJE STREAMLIT FOOTER-A I BEDŽEVA NA DNU */
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stFooter"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .st-emotion-cache-1cvow4s {display: none !important;} 
    div[data-testid="manage-app-button"] {display: none !important;}
    a[href^="https://streamlit.io"] {display: none !important; opacity: 0 !important; pointer-events: none !important;}
    
    /* Margine ekrana */
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
    
    /* Tamna tema */
    .stApp { background-color: #121212; color: #ffffff; }

    /* Naslovni blok */
    .header-box {
        text-align: center;
        padding: 40px 10px 20px 10px;
        background: linear-gradient(to bottom, #D4AF37, #8B6E02);
        margin: -20px -20px 20px -20px;
        border-radius: 0 0 40px 40px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
    }
    
    /* Dizajn dugmića */
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
    div[data-baseweb="slider"] { margin-bottom: 20px; }
    
    /* Input polja */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKCIJE NAVIGACIJE ---
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
    
    if img_src:
        image_html = f'<img src="{img_src}" width="140" style="margin-bottom: 15px; filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.8)); transition: transform 0.3s;">'
    else:
        image_html = '<div style="font-size: 60px; margin-bottom: 10px; text-shadow: 2px 4px 6px rgba(0,0,0,0.4);">⚗️</div>'

    st.markdown(f"""
        <div class="header-box">
            {image_html}
            <h1 style='color: white; margin:0; font-size: 28px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>RAKIJA MASTER</h1>
            <p style='color: #eee; font-style: italic; font-size: 14px;'>Premium Distillery Tools</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-bottom:5px;'>🟢 UKOMLJAVANJE</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🍇 Šećer i Alk.", use_container_width=True): idi_na('secer')
    with c2:
        if st.button("🦠 Kvasci", use_container_width=True): idi_na('kvasci')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>🔥 DESTILACIJA</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button("✂️ Prvenac", use_container_width=True): idi_na('prvenac')
        if st.button("💧 Razblaživanje", use_container_width=True): idi_na('razblazivanje')
        if st.button("⚖️ Kupažiranje", use_container_width=True): idi_na('kupaza')
    with c4:
        if st.button("🏁 Patoka (Srce)", use_container_width=True): idi_na('patoka')
        if st.button("🌡️ Temperatura", use_container_width=True): idi_na('temperatura')

    st.markdown("<p style='color:#D4AF37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>🏺 ODLEŽAVANJE & EVIDENCIJA</p>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if st.button("🪵 Bure (Litri)", use_container_width=True): idi_na('bure')
    with c6:
        if st.button("📖 Dnevnik", use_container_width=True): idi_na('dnevnik')

# ==========================================
# --- STRANICE ALATA ---
# ==========================================
else:
    st.markdown("<div class='btn-nazad'>", unsafe_allow_html=True)
    if st.button("⬅ NAZAD NA MENI", use_container_width=True):
        idi_na('pocetna')
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")

    # 1. KONVERZIJA ŠEĆERA
    if st.session_state.stranica == 'secer':
        st.subheader("🍇 Konverter šećera")
        brix = st.slider("Izmeren šećer (% Brix):", min_value=0.0, max_value=30.0, value=12.0, step=0.5)
        
        babo = brix * 0.85
        oechsle = brix * 4.25
        pot_alkohol = brix * 0.55
        
        st.info(f"**Babo (KMW):** {babo:.1f}°\n\n**Oechsle:** {oechsle:.0f}°")
        st.success(f"**Potencijalni alkohol u komini:** oko {pot_alkohol:.1f} % vol")

    # 2. KVASCI I ENZIMI
    elif st.session_state.stranica == 'kvasci':
        st.subheader("🦠 Kvasci, Enzimi i Hrana")
        voca_kg = st.number_input("Količina voća (kg):", min_value=10, value=100, step=10)
        
        enzim = (voca_kg / 100) * 2
        kvasac = (voca_kg / 100) * 25
        hrana = (voca_kg / 100) * 25
        
        st.warning(f"**Receptura za {voca_kg} kg komine:**")
        st.write(f"- **Enzimi (pektolitika):** {enzim:.1f} g")
        st.write(f"- **Selekcionisani kvasac:** {kvasac:.1f} g")
        st.write(f"- **Hrana za kvasce:** {hrana:.1f} g")

    # 3. ODVAJANJE PRVENCA
    elif st.session_state.stranica == 'prvenac':
        st.subheader("✂️ Odvajanje prvenca")
        voce = st.selectbox("Vrsta voća:",["Šljiva", "Kajsija / Breskva", "Dunja", "Jabuka / Kruška", "Grožđe (Loza)", "Ostalo"])
        meka = st.number_input("Meka rakija u kazanu (L):", min_value=1.0, value=100.0, step=5.0)
        
        if voce in["Kajsija / Breskva", "Dunja"]: 
            proc = 0.015
        elif voce == "Šljiva": 
            proc = 0.008
        else: 
            proc = 0.010
        
        prvenac = meka * proc
        st.error(f"Preporučeno za odvajanje: **{prvenac:.2f} Litara** ({proc*100}%)")
        st.caption("Aplikacija daje procenu zasnovanu na prosečnoj količini pektina u voću. Konačan presek uvek radi na miris!")

    # 4. PATOKA
    elif st.session_state.stranica == 'patoka':
        st.subheader("🏁 Presek: Odvajanje Patoke")
        st.write("Trenutak kada prestaješ da hvataš srce rakije.")
        voce = st.selectbox("Vrsta voća u kazanu:",["Šljiva", "Kajsija / Breskva", "Dunja", "Jabuka / Kruška", "Grožđe (Loza)"])
        
        if voce in["Kajsija / Breskva", "Dunja"]:
            preporuka = "45% - 50%"
            opis = "Aromatično voće brzo gubi fine arome na luli i povlači kiselkaste patočne tonove. Reži ranije!"
        elif voce == "Šljiva":
            preporuka = "40% - 45%"
            opis = "Šljiva je stabilnija, ali ispod 40% na luli počinju da izlaze teški alkoholi (fuzeli) koji mute rakiju."
        elif voce == "Jabuka / Kruška":
            preporuka = "40% - 42%"
            opis = "Pazi na miris, čim osetiš tupi miris 'na vosak' ili 'travu', prekidaj hvatanje srca."
        else:
            preporuka = "35% - 40%"
            opis = "Loza podnosi malo dublje hvatanje, ali prati aromu."

        st.error(f"Kada jačina **NA LULI** padne na: **{preporuka} vol**")
        st.info(opis)
        st.caption("💡 *Pro savet:* Pravilo majstora je da se patoka odvaja kada prosečna jačina u sudu dostigne željenu (npr. 60-65%), a na luli padne na gore preporučenu granicu.")

    # 5. RAZBLAŽIVANJE
    elif st.session_state.stranica == 'razblazivanje':
        st.subheader("💧 Razblaživanje rakije")
        v_r = st.number_input("Količina rakije (L):", min_value=0.5, value=10.0, step=0.5)
        j1 = st.slider("Trenutna jačina (%):", min_value=20.0, max_value=80.0, value=65.0, step=0.5)
        j2 = st.slider("Željena jačina (%):", min_value=20.0, max_value=60.0, value=42.0, step=0.5)
        
        if j1 <= j2:
            st.error("Željena jačina mora biti manja od trenutne!")
        else:
            voda = v_r * (j1 / j2 - 1)
            st.success(f"Sipati destilovanu vodu: **{voda:.2f} L**")

    # 6. TEMPERATURA
    elif st.session_state.stranica == 'temperatura':
        st.subheader("🌡️ Korekcija temperature")
        izm = st.slider("Očitana jačina na alkoholmetru (%):", 10.0, 80.0, 45.0, 0.5)
        temp = st.slider("Temperatura destilata (°C):", 0.0, 40.0, 25.0, 1.0)
        
        stvarna = izm - ((temp - 20) * 0.3) if temp > 20 else izm + ((20 - temp) * 0.3)
        st.warning(f"Stvarna jačina (na 20°C): **{stvarna:.1f} % vol**")
        st.caption("Napomena: Prikazana je matematička aproksimacija (veoma tačna za kućne potrebe).")

    # 7. KUPAŽIRANJE
    elif st.session_state.stranica == 'kupaza':
        st.subheader("⚖️ Kupažiranje (Mešanje)")
        
        col1, col2 = st.columns(2)
        with col1:
            v1 = st.number_input("Rakija 1 (L):", value=10.0, step=1.0)
            j1 = st.number_input("Jačina 1 (%):", value=60.0, step=1.0)
        with col2:
            v2 = st.number_input("Rakija 2 (L):", value=5.0, step=1.0)
            j2 = st.number_input("Jačina 2 (%):", value=40.0, step=1.0)
            
        if (v1+v2) > 0:
            j_nova = ((v1 * j1) + (v2 * j2)) / (v1 + v2)
            st.success(f"Dobijaš **{v1+v2} L** rakije jačine **{j_nova:.1f} % vol**")

    # 8. ZAPREMINA BURETA
    elif st.session_state.stranica == 'bure':
        st.subheader("🪵 Zapremina Drvenog Bureta")
        
        h = st.slider("Visina bureta / Dužina duga (cm):", 20.0, 150.0, 70.0, 1.0)
        d_sredina = st.number_input("Prečnik na najširem delu (cm):", value=60.0, step=1.0)
        d_kraj = st.number_input("Prečnik na dnu/vrhu (cm):", value=50.0, step=1.0)
        
        if st.button("IZRAČUNAJ ZAPREMINU", use_container_width=True):
            v_litri = (math.pi * h / 12 * (2 * d_sredina**2 + d_kraj**2)) / 1000
            st.success(f"Zapremina bureta je približno: **{v_litri:.1f} Litara**")

    # 9. DNEVNIK
    elif st.session_state.stranica == 'dnevnik':
        st.subheader("📖 Digitalni Dnevnik")
        
        with st.expander("➕ Dodaj novi unos", expanded=True):
            ime = st.text_input("Naziv serije (npr. Kajsija 2026):")
            kg = st.number_input("Količina voća (kg):", value=500)
            dobijeno = st.number_input("Dobijeno litara:", value=45.0)
            jacina = st.number_input("Jačina (%):", value=42.0)
            
            if st.button("💾 SAČUVAJ U DNEVNIK", use_container_width=True):
                if ime:
                    unos = {
                        "datum": datetime.now().strftime("%d.%m.%Y"),
                        "ime": ime, "kg": kg, "litara": dobijeno, "jacina": jacina
                    }
                    st.session_state.dnevnik.append(unos)
                    st.success("Uspešno sačuvano!")
                else:
                    st.error("Unesi naziv serije.")

        st.write("### 🗄️ Arhiva")
        if len(st.session_state.dnevnik) == 0:
            st.caption("Dnevnik je prazan. Dodaj svoj prvi kazan!")
        else:
            for item in reversed(st.session_state.dnevnik):
                st.markdown(f"""
                <div style='background-color:#1e1e1e; padding:15px; border-radius:10px; margin-bottom:10px; border-left:5px solid #D4AF37;'>
                    <strong style='color:#D4AF37; font-size:18px;'>{item['ime']}</strong><br>
                    <small style='color:#888;'>Datum: {item['datum']}</small><br>
                    Voće: <b>{item['kg']} kg</b> | Dobijeno: <b>{item['litara']} L</b> | Jačina: <b>{item['jacina']}%</b>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #555; font-size:12px;'>Cloud015 © 2026</p>", unsafe_allow_html=True)
