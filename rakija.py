import flet as st
import math
import json
import os
from datetime import datetime

# --- KONFIGURACIJA ---
GOLD_DARK = "#D4AF37"
GOLD_LIGHT = "#996515"
FILE_PATH = "dnevnik_podaci.json"

def main(page: ft.Page):
    page.title = "Rakija Master Pro"
    page.theme_mode = "dark"
    page.padding = 0
    page.window_width = 400
    page.window_height = 800
    
    # --- ČUVANJE PODATAKA ---
    def ucitaj_podatke():
        if os.path.exists(FILE_PATH):
            try:
                with open(FILE_PATH, "r", encoding="utf-8") as f: return json.load(f)
            except: return []
        return []

    def sacuvaj_podatke(lista):
        with open(FILE_PATH, "w", encoding="utf-8") as f: 
            json.dump(lista, f, indent=4, ensure_ascii=False)

    page.dnevnik = ucitaj_podatke()

    # --- POMOĆNE FUNKCIJE ZA STIL ---
    def get_gold(): return GOLD_DARK
    def get_txt(): return "white"
    def get_card(): return "#1e1e1e"

    def polje(label, value="", numeric=True, expand=False):
        return ft.TextField(
            label=label, value=str(value), height=50,
            border_color=get_gold(), focused_border_color=get_gold(),
            color=get_txt(), label_style=ft.TextStyle(color=get_gold(), size=11),
            border=ft.InputBorder.OUTLINE, border_radius=10, text_size=15,
            keyboard_type=ft.KeyboardType.NUMBER if numeric else ft.KeyboardType.TEXT,
            expand=expand
        )

    def akcija_dugme(tekst, funkcija):
        return ft.Container(
            content=ft.Text(tekst, weight="bold", color="black", size=15),
            bgcolor=get_gold(), padding=10, border_radius=10, 
            alignment=ft.Alignment(0, 0), on_click=funkcija, height=50
        )

    # --- NAVIGACIJA ---
    def idi_na(funkcija, ime):
        page.views.append(
            ft.View(
                route=f"/{ime}",
                controls=[funkcija()],
                bgcolor="#121212",
                padding=15,
                scroll="auto"
            )
        )
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = view_pop

    def dugme_nazad():
        return ft.Container(
            content=ft.TextButton(
                content=ft.Text("⬅ NAZAD NA MENI", color=get_gold(), weight="bold", size=14),
                on_click=view_pop
            ),
            padding=15, alignment=ft.Alignment(-1, 0)
        )

    # ==========================================
    # --- STRANICE ALATA ---
    # ==========================================

    def komina_strana():
        u = polje("Šećer u komini (% Brix)", "18")
        r = ft.Text(size=15, weight="bold", color=get_txt())
        def rac(e):
            try:
                b = float(u.value)
                r.value = f"Babo: {b*0.85:.1f}° | Oechsle: {b*4.25:.0f}°\nPotencijalni alkohol: {b*0.55:.1f}% vol"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("🍇 ANALIZA KOMINE", size=22, weight="bold", color=get_gold()),
            ft.Text("Brix meri šećer. Babo i Oechsle mere gustinu šire.", size=12, italic=True),
            u, akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def kvasci_strana():
        u = polje("Količina voća (kg)", "100")
        r = ft.Text(size=15, weight="bold", color=get_txt())
        def rac(e):
            try:
                k = float(u.value)
                r.value = f"Enzim: {(k/100)*2:.1f}g\nKvasac: {(k/100)*25:.1f}g\nHrana: {(k/100)*25:.1f}g"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("🦠 KVASCI I ENZIMI", size=22, weight="bold", color=get_gold()),
            ft.Text("Enzimi, kvasci i hrana osiguravaju čisto vrenje.", size=12, italic=True),
            u, akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def prvenac_strana():
        u = polje("Meka rakija (L)", "100")
        v = ft.Dropdown(label="Voće", border_color=get_gold(), color=get_txt(), 
                        options=[ft.dropdown.Option("Šljiva (1%)"), ft.dropdown.Option("Dunja (1.5%)"), ft.dropdown.Option("Ostalo (1.2%)")], 
                        value="Šljiva (1%)")
        r = ft.Text(size=16, color="red", weight="bold")
        def rac(e):
            try:
                p = 0.015 if "Dunja" in v.value else (0.012 if "Ostalo" in v.value else 0.01)
                r.value = f"ODVOJITI: {float(u.value)*p:.2f} L"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("✂️ PRVENAC", size=22, weight="bold", color=get_gold()),
            ft.Text("Odvajanje metila na početku prepeka.", size=12, italic=True),
            v, u, akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def razblazivanje_strana():
        v, j1, j2 = polje("Litraža (L)", "10"), polje("Trenutna %", "65"), polje("Željena %", "42")
        r = ft.Text(size=16, color="green", weight="bold")
        def rac(e):
            try:
                vd = float(v.value) * (float(j1.value)/float(j2.value) - 1)
                r.value = f"DODATI VODE: {vd:.2f} L"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("💧 RAZBLAŽIVANJE", size=22, weight="bold", color=get_gold()),
            ft.Text("Postepeno dodavanje destilovane vode u rakiju.", size=12, italic=True),
            v, j1, j2, akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def temperatura_strana():
        j, t = polje("Jačina %", "45"), polje("Temp °C", "15")
        r = ft.Text(size=16, color=get_gold(), weight="bold")
        def rac(e):
            try:
                s = float(j.value) + (20 - float(t.value)) * 0.3
                r.value = f"STVARNA JAČINA: {s:.1f}%"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("🌡️ TEMPERATURA", size=22, weight="bold", color=get_gold()),
            ft.Text("Korekcija očitane jačine na standardnih 20°C.", size=12, italic=True),
            j, t, akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def patoka_strana():
        v = ft.Dropdown(label="Voće", border_color=get_gold(), color=get_txt(), 
                        options=[ft.dropdown.Option("Šljiva"), ft.dropdown.Option("Dunja"), ft.dropdown.Option("Jabuka"), ft.dropdown.Option("Kajsija / Breskva"), ft.dropdown.Option("Grožđe")], 
                        value="Šljiva")
        r = ft.Text(size=15, color=get_txt())
        def rac(e):
            try:
                s = {
                    "Šljiva": "Prekidaj na 40-45% na luli. Ispod 40% izlaze teški alkoholi.",
                    "Dunja": "Prekidaj na 45-50% na luli. Aromatično voće brzo gubi fine arome.",
                    "Kajsija / Breskva": "Prekidaj na 45-50% na luli. Reži ranije!",
                    "Jabuka / Kruška": "Prekidaj na oko 40-42%. Pazi na miris 'na vosak'.",
                    "Grožđe": "Prekidaj na 35-40% na luli."
                }
                r.value = s.get(v.value, "Prati miris i jačinu."); page.update()
            except: r.value = "Greška!"
        return ft.Column([
            ft.Text("🏁 PATOKA", size=22, weight="bold", color=get_gold()),
            ft.Text("Trenutak kada se prekida hvatanje srca rakije.", size=12, italic=True),
            v, akcija_dugme("SAVET", rac), r, dugme_nazad()
        ])

    def kupaza_strana():
        v1, j1 = polje("L1 (Litri)", "10", expand=True), polje("Jačina 1 (%)", "60", expand=True)
        v2, j2 = polje("L2 (Litri)", "5", expand=True), polje("Jačina 2 (%)", "40", expand=True)
        r = ft.Text(size=15, color=get_txt())
        def rac(e):
            try:
                uk = float(v1.value) + float(v2.value)
                n = (float(v1.value)*float(j1.value) + float(v2.value)*float(j2.value)) / uk
                r.value = f"Ukupno: {uk}L | Jačina: {n:.1f}%"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("⚖️ KUPAŽA", size=22, weight="bold", color=get_gold()),
            ft.Text("Mešanje dve različite rakije radi ujednačavanja.", size=12, italic=True),
            ft.Row([v1, j1]), ft.Row([v2, j2]), akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def bure_strana():
        h, ds, dk = polje("Visina (cm)", "70"), polje("Sredina (cm)", "60"), polje("Dno (cm)", "50")
        r = ft.Text(size=15, color=get_txt())
        def rac(e):
            try:
                v = (math.pi * float(h.value) / 12 * (2 * float(ds.value)**2 + float(dk.value)**2)) / 1000
                r.value = f"Zapremina: oko {v:.1f} L"
            except: r.value = "Greška!"
            page.update()
        return ft.Column([
            ft.Text("🪵 BURE", size=22, weight="bold", color=get_gold()),
            ft.Text("Proračun zapremine drvenog bureta.", size=12, italic=True),
            h, ds, dk, akcija_dugme("IZRAČUNAJ", rac), r, dugme_nazad()
        ])

    def dnevnik_strana():
        lista_prikaz = ft.Column(spacing=10)
        def obrisi_unos(index):
            page.dnevnik.pop(index); sacuvaj_podatke(page.dnevnik); osvezi_listu()
        def osvezi_listu():
            lista_prikaz.controls.clear()
            for i, s in enumerate(reversed(page.dnevnik)):
                idx = len(page.dnevnik) - 1 - i
                lista_prikaz.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"{s.get('ime','-')} ({s.get('godina','-')})", weight="bold", size=14, color=get_gold()),
                                ft.Text(f"{s.get('kg','-')}kg | {s.get('datum','-')} | {s.get('litara','-')}L | {s.get('jacina','-')}%", size=12),
                            ], expand=True),
                            ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color="red", on_click=lambda _, x=idx: obrisi_unos(x))
                        ]),
                        bgcolor=get_card(), padding=10, border_radius=10, border=ft.Border.all(1, get_gold())
                    )
                )
            page.update()

        f_ime, f_god = polje("Voće", "Šljiva", False, expand=True), polje("Godina", "2024", expand=True)
        f_kg, f_dat = polje("Kg", "500", expand=True), polje("Datum", datetime.now().strftime("%d.%m"), False, expand=True)
        f_lit, f_jac = polje("Litri", "50", expand=True), polje("Jačina %", "42", expand=True)

        def dodaj(e):
            if f_ime.value:
                page.dnevnik.append({"ime": f_ime.value, "godina": f_god.value, "kg": f_kg.value, "datum": f_dat.value, "litara": f_lit.value, "jacina": f_jac.value})
                sacuvaj_podatke(page.dnevnik); osvezi_listu()

        osvezi_listu()
        return ft.Column([
            ft.Text("📖 DNEVNIK RADA", size=22, weight="bold", color=get_gold()), 
            ft.Row([f_ime, f_god]), ft.Row([f_kg, f_dat]), ft.Row([f_lit, f_jac]), 
            akcija_dugme("SAČUVAJ U ARHIVU", dodaj), 
            ft.Divider(color=get_gold()), lista_prikaz, dugme_nazad()
        ])

    def linkovi_strana():
        def link_dugme(tekst, ikona, url):
            return ft.Container(
                content=ft.Row([ft.Text(ikona, size=24), ft.Text(tekst, weight="bold", color="black")], alignment="center"),
                bgcolor=get_gold(), padding=15, border_radius=10, url=url
            )
        return ft.Column([
            ft.Text("🔗 LINKOVI I DOGAĐAJI", size=22, weight="bold", color=get_gold()),
            link_dugme("Knjiga: Rakijski kod", "📘", "https://www.facebook.com/rakijskikod/"),
            link_dugme("Rakija iz rakije", "🥂", "https://www.rakijaizrakije.com"),
            link_dugme("Savez proizvođača rakija", "🤝", "https://savezrakija.rs"),
            ft.Divider(color=get_gold()),
            ft.Text("📅 DOGAĐAJI", size=18, weight="bold", color=get_gold()),
            ft.Container(content=ft.Text("18.04.2024. Prvi Hajdučki festival rakije - Bogatić", color=get_gold(), weight="bold"), url="https://www.facebook.com/p/Хајдуčki-festival-rakije-Bogatić-61584019897579/"),
            dugme_nazad()
        ])

    # --- POČETNA STRANA ---
    def pocetna_strana():
        def stavka(t, i, funkcija, ime):
            return ft.Container(
                content=ft.Column([ft.Text(i, size=30), ft.Text(t, size=12, weight="bold", color=get_gold())], horizontal_alignment="center", alignment="center"),
                bgcolor=get_card(), expand=1, height=90, border_radius=15, border=ft.Border.all(1, get_gold()),
                on_click=lambda _: idi_na(funkcija, ime)
            )
        
        slika = ft.Image(src="kazan.png", width=150, height=150) if os.path.exists("kazan.png") else ft.Text("⚗️", size=70)

        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("RAKIJA MASTER PRO", size=24, weight="900", color="white"),
                    ft.Container(content=slika, alignment=ft.Alignment(0, 0), padding=10)
                ]), bgcolor=get_gold(), padding=20, border_radius=ft.BorderRadius(0,0,35,35), shadow=ft.BoxShadow(blur_radius=10, color="#66000000")
            ),
            ft.ListView([
                ft.Text(" 🟢 UKOMLJAVANJE", size=14, weight="bold", color=get_gold()),
                ft.Row([stavka("Komina", "🍇", komina_strana, "komina"), stavka("Kvasci", "🦠", kvasci_strana, "kvasci")]),
                ft.Text(" 🔥 DESTILACIJA", size=14, weight="bold", color=get_gold()),
                ft.Row([stavka("Prvenac", "✂️", prvenac_strana, "prvenac"), stavka("Patoka", "🏁", patoka_strana, "patoka")]),
                ft.Row([stavka("Razblaživanje", "💧", razblazivanje_strana, "razblazivanje"), stavka("Temperatura", "🌡️", temperatura_strana, "temp")]),
                ft.Text(" ⚖️ KUPAŽA I BURE", size=14, weight="bold", color=get_gold()),
                ft.Row([stavka("Kupaža", "⚖️", kupaza_strana, "kupaza"), stavka("Bure", "🪵", bure_strana, "bure")]),
                ft.Text(" 📖 ARHIVA", size=14, weight="bold", color=get_gold()),
                ft.Row([stavka("Dnevnik", "📖", dnevnik_strana, "dnevnik"), stavka("Linkovi", "🔗", linkovi_strana, "linkovi")]),
            ], expand=True, spacing=10, padding=15)
        ], expand=True)

    page.views.append(ft.View(route="/", controls=[pocetna_strana()], bgcolor="#121212", padding=0))
    page.update()

if __name__ == "__main__":
    ft.run(main)
