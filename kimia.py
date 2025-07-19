import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image, ImageDraw
import io
import base64
import random

# Konfigurasi halaman
st.set_page_config(
    page_title="Lab Kimia Interaktif",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema warna
primary_color = "#FF6B6B"
secondary_color = "#4ECDC4"
accent_color = "#FFD166"
background_color = "#F7FFF7"
dark_color = "#1A535C"
text_color = "#333333"  # Warna teks baru untuk kontras

# CSS untuk styling
st.markdown(f"""
<style>
    /* Warna utama */
    .stApp {{
        background: linear-gradient(135deg, {background_color}, #E0F7E0);
        background-attachment: fixed;
    }}
    .css-1d391kg, .st-b7, .st-b8, .st-b9 {{
        background-color: transparent !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {dark_color} !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    p, div, span, li, td {{
        color: {text_color} !important;
    }}
    .stButton>button {{
        background: linear-gradient(to right, {primary_color}, {accent_color}) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
    }}
    .stSelectbox>div>div {{
        background-color: white !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }}
    .stSlider>div>div>div {{
        background: linear-gradient(to right, {accent_color}, {secondary_color}) !important;
    }}
    .stTabs>div>div>div>div {{
        background: linear-gradient(135deg, {secondary_color}, {primary_color}) !important;
        color: white !important;
        border-radius: 15px 15px 0 0 !important;
        padding: 12px 24px !important;
        font-weight: bold;
        margin: 0 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .stTabs>div>div>div>div[aria-selected="true"] {{
        background: linear-gradient(135deg, {primary_color}, {accent_color}) !important;
        transform: scale(1.05);
        z-index: 1;
    }}
    .stDataFrame {{
        border-radius: 15px !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
        overflow: hidden;
    }}
    .stAlert {{
        border-radius: 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }}
    .element-card {{
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        height: 100%;
        border: 2px solid {secondary_color};
    }}
    .element-card:hover {{
        transform: translateY(-10px) rotate(2deg);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        border: 2px solid {primary_color};
    }}
    .reaction-container {{
        background: white;
        border-radius: 25px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        border: 3px solid {accent_color};
        background-image: radial-gradient(circle at top right, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
    }}
    .color-box {{
        width: 100%;
        height: 180px;
        border-radius: 20px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 28px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2), 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 2px solid white;
    }}
    .color-box:hover {{
        transform: scale(1.03);
        box-shadow: inset 0 0 30px rgba(0,0,0,0.3), 0 6px 12px rgba(0,0,0,0.3);
    }}
    .warning-badge {{
        background: linear-gradient(135deg, #FFD166, #FF9E6D);
        color: {dark_color};
        border-radius: 50px;
        padding: 8px 20px;
        margin: 10px;
        display: inline-block;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    .apd-badge {{
        background: linear-gradient(135deg, {secondary_color}, #118AB2);
        color: white;
        border-radius: 50px;
        padding: 8px 20px;
        margin: 10px;
        display: inline-block;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    .periodic-header {{
        background: linear-gradient(135deg, {dark_color}, #073B4C);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}
    .chemical-equation {{
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px dashed {accent_color};
        color: {text_color};
    }}
    .bubble {{
        position: absolute;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        animation: float 15s infinite ease-in-out;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0) translateX(0) rotate(0); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-1000px) translateX(200px) rotate(360deg); opacity: 0; }}
    }}
    .compatibility-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }}
    .compatibility-table th, .compatibility-table td {{
        padding: 12px 15px;
        text-align: center;
        border: 1px solid #ddd;
    }}
    .compatibility-table th {{
        background-color: {dark_color};
        color: white;
        font-weight: bold;
    }}
    .compatibility-table tr:nth-child(even) {{
        background-color: #f8f9fa;
    }}
    .compatibility-table tr:hover {{
        background-color: #e9ecef;
    }}
    .compatibility-table .compatible {{
        background-color: #d4edda;
        color: #155724;
        font-weight: bold;
    }}
    .compatibility-table .incompatible {{
        background-color: #f8d7da;
        color: #721c24;
        font-weight: bold;
    }}
    .compatibility-table .conditional {{
        background-color: #fff3cd;
        color: #856404;
        font-weight: bold;
    }}
    .hazard-symbol {{
        font-size: 36px;
        margin-right: 15px;
        display: inline-block;
        width: 60px;
        text-align: center;
    }}
    .page-title {{
        background:linear-gradient(135deg, #1A535C, #073B4C);
        padding:30px; 
        border-radius:25px; 
        color:white; 
        margin-bottom:30px;
        text-align:center; 
        box-shadow:0 12px 24px rgba(0,0,0,0.3);
    }}
    .page-title h1 {{
        color: white !important;
        font-size:42px; 
        margin:0;
    }}
    .page-title p {{
        color: #FFD166 !important;
        font-size:20px; 
        margin:10px 0 0;
    }}
</style>
""", unsafe_allow_html=True)

# Animasi gelembung
st.markdown("""
<script>
function createBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    
    const size = Math.random() * 100 + 50;
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;
    
    const posX = Math.random() * window.innerWidth;
    bubble.style.left = `${posX}px`;
    bubble.style.bottom = `-100px`;
    
    const animationDuration = Math.random() * 20 + 10;
    bubble.style.animationDuration = `${animationDuration}s`;
    
    document.body.appendChild(bubble);
    
    setTimeout(() => {
        bubble.remove();
    }, animationDuration * 1000);
}

// Create bubbles every 1.5 seconds
setInterval(createBubble, 1500);
</script>
""", unsafe_allow_html=True)

# Database tabel periodik (disingkat untuk efisiensi)
PERIODIC_TABLE = [
    # Periode 1
    {"Symbol": "H", "Name": "Hidrogen", "AtomicNumber": 1, "AtomicMass": 1.008, 
     "Group": 1, "Period": 1, "Category": "Nonlogam", "Color": "#FF6B6B", "Electronegativity": 2.20, "Hazards": ["Mudah Terbakar"]},
    {"Symbol": "He", "Name": "Helium", "AtomicNumber": 2, "AtomicMass": 4.0026, 
     "Group": 18, "Period": 1, "Category": "Gas Mulia", "Color": "#4ECDC4", "Electronegativity": None, "Hazards": []},
    
    # Periode 2 (disingkat)
    {"Symbol": "Li", "Name": "Litium", "AtomicNumber": 3, "AtomicMass": 6.94, 
     "Group": 1, "Period": 2, "Category": "Logam Alkali", "Color": "#FFD166", "Electronegativity": 0.98, "Hazards": ["Mudah Terbakar", "Reaktif"]},
    {"Symbol": "Be", "Name": "Berilium", "AtomicNumber": 4, "AtomicMass": 9.0122, 
     "Group": 2, "Period": 2, "Category": "Logam Alkali Tanah", "Color": "#06D6A0", "Electronegativity": 1.57, "Hazards": ["Beracun"]},
    
    # ... (unsur lainnya disingkat untuk efisiensi)
    
    # Contoh unsur terakhir
    {"Symbol": "Og", "Name": "Oganesson", "AtomicNumber": 118, "AtomicMass": 294, 
     "Group": 18, "Period": 7, "Category": "Belum Diketahui", "Color": "#9D4EDD", "Electronegativity": None, "Hazards": ["Radioaktif"]}
]

# Database senyawa kimia (disingkat)
COMPOUNDS = {
    "Asam Klorida (HCl)": {"color": "#F0F0F0", "formula": "HCl", "type": "Asam Kuat", "hazards": ["Korosif"]},
    "Natrium Hidroksida (NaOH)": {"color": "#FFFFFF", "formula": "NaOH", "type": "Basa Kuat", "hazards": ["Korosif"]},
    "Tembaga Sulfat (CuSO₄)": {"color": "#00B4D8", "formula": "CuSO₄", "type": "Garam", "hazards": ["Beracun"]},
    "Besi (Fe)": {"color": "#B5651D", "formula": "Fe", "type": "Logam", "hazards": []},
    "Kalium Permanganat (KMnO₄)": {"color": "#9D00FF", "formula": "KMnO₄", "type": "Oksidator", "hazards": ["Pengoksidasi"]},
}

# Database reaksi kimia (disingkat)
REACTIONS = [
    {
        "reagents": ["Asam Klorida (HCl)", "Natrium Hidroksida (NaOH)"],
        "products": ["Natrium Klorida (NaCl)", "Air (H₂O)"],
        "equation": "HCl + NaOH → NaCl + H₂O",
        "type": "Netralisasi",
        "color_change": ["#F0F0F0 + #FFFFFF → #FFFFFF + #ADD8E6"],
        "energy": "Eksoterm",
        "hazards": ["Korosif", "Iritan"],
        "apd": ["Sarung Tangan", "Kacamata", "Jas Lab"],
        "description": "Reaksi netralisasi antara asam kuat dan basa kuat menghasilkan garam dan air. Reaksi ini melepaskan panas."
    },
    {
        "reagents": ["Tembaga Sulfat (CuSO₄)", "Besi (Fe)"],
        "products": ["Besi Sulfat (FeSO₄)", "Tembaga (Cu)"],
        "equation": "CuSO₄ + Fe → FeSO₄ + Cu",
        "type": "Reaksi Pendesakan",
        "color_change": ["#00B4D8 + #B5651D → #76D7EA + #D2691E"],
        "energy": "Eksoterm",
        "hazards": ["Iritan"],
        "apd": ["Sarung Tangan", "Kacamata"],
        "description": "Logam besi mendesak tembaga dari larutan tembaga sulfat, menghasilkan besi sulfat dan tembaga padat."
    }
]

# Fungsi untuk membuat kartu unsur
def create_element_card(element):
    hazards_html = ""
    if element["Hazards"]:
        hazards_html = "<div style='margin-top:10px;'><b>Bahaya:</b><br>"
        for hazard in element["Hazards"]:
            hazards_html += f"<span class='warning-badge'>{hazard}</span> "
        hazards_html += "</div>"
    
    card = f"""
    <div class="element-card">
        <div style="background:{element['Color']}; 
                    background:linear-gradient(135deg, {element['Color']}, #FFFFFF);
                    border-radius:50%; width:80px; height:80px; 
                    display:flex; align-items:center; justify-content:center; margin:0 auto 15px;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.2);">
            <h2 style="color:white; margin:0; text-shadow:2px 2px 4px rgba(0,0,0,0.5);">{element['Symbol']}</h2>
        </div>
        <h3 style="text-align:center; margin-bottom:10px; color:{dark_color};">{element['Name']}</h3>
        <div style="background:rgba(255,255,255,0.7); border-radius:15px; padding:10px;">
            <p style="text-align:center; margin:5px 0; font-size:1rem; color:{text_color};">
                <b>No Atom:</b> {element['AtomicNumber']}<br>
                <b>Massa:</b> {element['AtomicMass']}<br>
                <b>Golongan:</b> {element['Group']}<br>
                <b>Periode:</b> {element['Period']}<br>
                <b>Kategori:</b> {element['Category']}
            </p>
        </div>
        {hazards_html}
    </div>
    """
    return card

# Fungsi untuk menampilkan tabel periodik
def show_periodic_table():
    st.header("📊 Tabel Periodik Interaktif")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Tabel Periodik Unsur Kimia</h2>
        <p style="text-align:center; font-size:18px;">Klik pada kartu unsur untuk melihat detail lengkap</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kategori warna
    categories = {
        "Logam Alkali": "#FFD166",
        "Logam Alkali Tanah": "#06D6A0",
        "Logam Transisi": "#118AB2",
        "Logam Pascatransisi": "#073B4C",
        "Metaloid": "#6A4C93",
        "Nonlogam": "#FF6B6B",
        "Halogen": "#4ECDC4",
        "Gas Mulia": "#EF476F",
        "Belum Diketahui": "#9D4EDD"
    }
    
    # Filter kategori
    selected_category = st.selectbox("Filter Kategori", ["Semua"] + list(categories.keys()), key="category_filter")
    
    # Tampilkan legenda
    st.subheader("Legenda Kategori")
    cols = st.columns(5)
    for i, (cat, color) in enumerate(categories.items()):
        cols[i % 5].markdown(f"""
        <div style="background:{color}; 
                    background:linear-gradient(135deg, {color}, #FFFFFF);
                    border-radius:10px; padding:10px; text-align:center; 
                    color:white; margin-bottom:10px; font-weight:bold; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
            {cat}
        </div>
        """, unsafe_allow_html=True)
    
    # Tampilkan kartu unsur
    st.subheader("Daftar Unsur")
    if selected_category != "Semua":
        elements = [e for e in PERIODIC_TABLE if e["Category"] == selected_category]
    else:
        elements = PERIODIC_TABLE
        
    # Atur kartu dalam grid
    cols = st.columns(5)
    for i, element in enumerate(elements):
        with cols[i % 5]:
            st.markdown(create_element_card(element), unsafe_allow_html=True)
    
    # Grafik interaktif dengan Altair
    st.subheader("📈 Visualisasi Sifat Unsur")
    df = pd.DataFrame(PERIODIC_TABLE)
    
    # Hapus baris dengan nilai None di AtomicMass
    df = df.dropna(subset=['AtomicMass'])
    
    # Buat chart dengan Altair
    chart = alt.Chart(df).mark_circle(size=100).encode(
        x='AtomicNumber:Q',
        y='AtomicMass:Q',
        color=alt.Color('Category:N', legend=alt.Legend(title="Kategori")),
        tooltip=['Name:N', 'Symbol:N', 'AtomicNumber:Q', 'AtomicMass:Q', 'Category:N']
    ).properties(
        width=700,
        height=500,
        title='Massa Atom vs Nomor Atom'
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

# Fungsi untuk menampilkan simulasi reaksi
def show_reaction_simulator():
    st.header("🧪 Simulator Reaksi Kimia")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Simulasi Reaksi Kimia Interaktif</h2>
        <p style="text-align:center; font-size:18px;">Pilih dua senyawa untuk melihat reaksi yang terjadi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pilih senyawa
    col1, col2 = st.columns(2)
    with col1:
        compound1 = st.selectbox("Pilih Senyawa Pertama", list(COMPOUNDS.keys()), key="compound1")
        color1 = COMPOUNDS[compound1]["color"]
        st.markdown(f"<div style='background:{color1}; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
        st.caption(f"Rumus: {COMPOUNDS[compound1]['formula']}")
        
    with col2:
        compound2 = st.selectbox("Pilih Senyawa Kedua", list(COMPOUNDS.keys()), key="compound2")
        color2 = COMPOUNDS[compound2]["color"]
        st.markdown(f"<div style='background:{color2}; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
        st.caption(f"Rumus: {COMPOUNDS[compound2]['formula']}")
    
    # Tombol untuk melakukan reaksi
    if st.button("⚡ Lakukan Reaksi", use_container_width=True, key="react_button"):
        # Temukan reaksi yang sesuai
        reaction = None
        for r in REACTIONS:
            if (compound1 in r["reagents"] and compound2 in r["reagents"]) or \
               (compound2 in r["reagents"] and compound1 in r["reagents"]):
                reaction = r
                break
        
        # Tampilkan hasil reaksi
        if reaction:
            st.session_state.reaction = reaction
        else:
            st.session_state.reaction = None
    
    # Tampilkan hasil reaksi jika ada
    if "reaction" in st.session_state and st.session_state.reaction:
        reaction = st.session_state.reaction
        st.markdown(f"<div class='reaction-container'>", unsafe_allow_html=True)
        
        # Header reaksi
        st.subheader(f"Reaksi: {reaction['type']}")
        st.markdown(f"<div class='chemical-equation'>{reaction['equation']}</div>", unsafe_allow_html=True)
        
        # Visualisasi warna
        col1, col2, col3 = st.columns([1, 0.2, 1])
        with col1:
            st.markdown("### Pereaksi")
            for reagent in reaction["reagents"]:
                color = COMPOUNDS[reagent]["color"]
                st.markdown(f"<div class='color-box' style='background-color:{color}'>{reagent}</div>", 
                            unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h1 style='text-align:center; margin-top:80px; font-size:48px;'>→</h1>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("### Produk")
            for product in reaction["products"]:
                if product in COMPOUNDS:
                    color = COMPOUNDS[product]["color"]
                    st.markdown(f"<div class='color-box' style='background-color:{color}'>{product}</div>", 
                                unsafe_allow_html=True)
                else:
                    # Warna default untuk produk yang tidak terdaftar
                    st.markdown(f"<div class='color-box' style='background-color:#DDDDDD'>{product}</div>", 
                                unsafe_allow_html=True)
        
        # Informasi reaksi
        st.subheader("📝 Informasi Reaksi")
        st.markdown(f"**Jenis Reaksi:** {reaction['type']}")
        st.markdown(f"**Perubahan Energi:** {reaction['energy']}")
        st.markdown(f"**Deskripsi:** {reaction['description']}")
        
        # Bahaya dan APD
        col4, col5 = st.columns(2)
        with col4:
            st.subheader("⚠️ Simbol Bahaya")
            for hazard in reaction["hazards"]:
                st.markdown(f"<div class='warning-badge'>{hazard}</div>", unsafe_allow_html=True)
        
        with col5:
            st.subheader("🛡️ Alat Pelindung Diri (APD)")
            for apd in reaction["apd"]:
                st.markdown(f"<div class='apd-badge'>{apd}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    elif "reaction" in st.session_state and st.session_state.reaction is None:
        st.error("Tidak ada reaksi yang diketahui antara senyawa yang dipilih.")
        
    # Tampilkan daftar reaksi yang tersedia
    with st.expander("📚 Daftar Reaksi yang Tersedia", expanded=True):
        for i, r in enumerate(REACTIONS):
            st.markdown(f"#### Reaksi {i+1}: {r['type']}")
            st.markdown(f"**Persamaan:** {r['equation']}")
            st.markdown(f"**Pereaksi:** {', '.join(r['reagents'])}")
            st.markdown(f"**Produk:** {', '.join(r['products'])}")
            st.markdown("---")

# Fungsi untuk menampilkan informasi tambahan
def show_additional_info():
    st.header("📚 Ensiklopedia Kimia")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Panduan Lengkap Kimia Dasar</h2>
        <p style="text-align:center; font-size:18px;">Pelajari konsep-konsep dasar kimia dan eksperimen menarik</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Jenis-jenis reaksi kimia
    st.subheader("🧪 Jenis-Jenis Reaksi Kimia")
    reaction_types = [
        {"name": "Sintesis", "emoji": "⚗️", "desc": "Dua atau lebih zat bergabung membentuk zat baru. Contoh: 2H₂ + O₂ → 2H₂O"},
        {"name": "Dekomposisi", "emoji": "🧫", "desc": "Satu zat terurai menjadi dua atau lebih zat. Contoh: 2H₂O₂ → 2H₂O + O₂"},
        {"name": "Pembakaran", "emoji": "🔥", "desc": "Reaksi dengan oksigen yang menghasilkan panas dan cahaya. Contoh: CH₄ + 2O₂ → CO₂ + 2H₂O"},
        {"name": "Penggantian Tunggal", "emoji": "🔄", "desc": "Satu unsur menggantikan unsur lain dalam senyawa. Contoh: Zn + 2HCl → ZnCl₂ + H₂"},
        {"name": "Penggantian Ganda", "emoji": "🔀", "desc": "Ion-ion dari dua senyawa saling bertukar. Contoh: AgNO₃ + NaCl → AgCl + NaNO₃"},
        {"name": "Netralisasi", "emoji": "⚖️", "desc": "Asam dan basa bereaksi membentuk garam dan air. Contoh: HCl + NaOH → NaCl + H₂O"}
    ]
    
    cols = st.columns(3)
    for i, rtype in enumerate(reaction_types):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{rtype['emoji']}</span>
                    <h3 style="margin:0;">{rtype['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{rtype['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Simbol bahaya (9 simbol)
    st.subheader("⚠️ Simbol Bahaya Laboratorium (GHS)")
    hazard_symbols = [
        {"name": "Mudah Terbakar", "emoji": "🔥", "desc": "Bahan yang mudah menyala saat terkena api, panas, percikan api, atau sumber nyala lainnya"},
        {"name": "Mudah Teroksidasi", "emoji": "⚡", "desc": "Bahan yang dapat menyebabkan atau memperparah kebakaran, umumnya menghasilkan panas saat kontak dengan zat lain"},
        {"name": "Mudah Meledak", "emoji": "💥", "desc": "Bahan yang dapat meledak akibat reaksi kimia, menghasilkan gas panas dalam volume dan kecepatan tinggi"},
        {"name": "Beracun", "emoji": "☠️", "desc": "Bahan yang dapat menyebabkan keracunan akut atau kronis, bahkan kematian jika terhirup, tertelan, atau terserap kulit"},
        {"name": "Korosif", "emoji": "⚠️", "desc": "Bahan yang dapat merusak jaringan hidup dan material logam melalui reaksi kimia"},
        {"name": "Gas di Bawah Tekanan", "emoji": "💨", "desc": "Gas yang disimpan dalam wadah bertekanan dan dapat meledak jika dipanaskan"},
        {"name": "Toksik untuk Organ Target", "emoji": "🧬", "desc": "Bahan yang dapat menyebabkan kerusakan organ tertentu setelah paparan tunggal atau berulang"},
        {"name": "Bahaya Kronis", "emoji": "🔄", "desc": "Bahan yang dapat menyebabkan efek kesehatan jangka panjang seperti kanker, kerusakan reproduksi, atau mutasi genetik"},
        {"name": "Bahaya Lingkungan", "emoji": "🌍", "desc": "Bahan yang dapat menyebabkan efek merusak pada lingkungan perairan atau atmosfer"}
    ]
    
    cols = st.columns(3)
    for i, hazard in enumerate(hazard_symbols):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span class="hazard-symbol">{hazard['emoji']}</span>
                    <h3 style="margin:0;">{hazard['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{hazard['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Alat pelindung diri
    st.subheader("🛡️ Alat Pelindung Diri (APD)")
    apd_items = [
        {"name": "Kacamata Keselamatan", "emoji": "👓", "desc": "Melindungi mata dari percikan bahan kimia"},
        {"name": "Sarung Tangan", "emoji": "🧤", "desc": "Melindungi tangan dari kontak langsung bahan kimia"},
        {"name": "Jas Lab", "emoji": "🥼", "desc": "Melindungi tubuh dan pakaian dari percikan bahan kimia"},
        {"name": "Pelindung Wajah", "emoji": "🥽", "desc": "Melindungi seluruh wajah dari percikan berbahaya"},
        {"name": "Masker Respirator", "emoji": "😷", "desc": "Melindungi sistem pernapasan dari uap berbahaya"},
        {"name": "Sepatu Tertutup", "emoji": "👞", "desc": "Melindungi kaki dari tumpahan bahan kimia"}
    ]
    
    cols = st.columns(3)
    for i, apd in enumerate(apd_items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{apd['emoji']}</span>
                    <h3 style="margin:0;">{apd['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{apd['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tips keselamatan
    st.subheader("🔒 Tips Keselamatan Laboratorium")
    safety_tips = [
        "Selalu gunakan APD yang sesuai saat bekerja dengan bahan kimia",
        "Kenali sifat dan bahaya bahan kimia sebelum menggunakannya",
        "Jangan pernah mencicipi atau mencium bahan kimia secara langsung",
        "Bekerja di dalam lemari asam saat menangani bahan berbahaya",
        "Simpan bahan kimia sesuai dengan kelompok dan sifatnya",
        "Bersihkan tumpahan segera dengan prosedur yang benar",
        "Ketahui lokasi alat keselamatan (pemadam api, shower, eye wash)",
        "Jangan bekerja sendirian di laboratorium",
        "Baca dan pahami MSDS (Material Safety Data Sheet) sebelum menggunakan bahan kimia",
        "Cuci tangan setelah bekerja di laboratorium"
    ]
    
    for i, tip in enumerate(safety_tips):
        st.markdown(f"""
        <div class="element-card" style="padding:15px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:15px; color:{dark_color};">🔒</span>
                <p style="margin:0; font-size:16px; color:{text_color};">{i+1}. {tip}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan informasi PBK
def show_chemical_safety():
    st.header("🧪 Penanganan Bahan Kimia (PBK)")
    st.markdown("""
    <div class="periodic-header">
        <h2 style="color:white; text-align:center; font-size:32px;">Pedoman Penyimpanan dan Kompatibilitas Bahan Kimia</h2>
        <p style="text-align:center; font-size:18px;">Pelajari cara menyimpan bahan kimia dengan aman dan kelompok kompatibilitas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🏷️ Kelompok Penyimpanan Bahan Kimia")
    storage_groups = [
        {"name": "Asam Anorganik", "emoji": "🧪", "desc": "HCl, H₂SO₄, HNO₃, H₃PO₄. Simpan terpisah dari basa dan bahan organik."},
        {"name": "Basa", "emoji": "🧴", "desc": "NaOH, KOH, NH₄OH. Simpan terpisah dari asam dan logam."},
        {"name": "Pelarut Organik", "emoji": "💧", "desc": "Etanol, Aseton, Benzena. Simpan di lemari khusus bahan mudah terbakar."},
        {"name": "Oksidator", "emoji": "🔥", "desc": "KMnO₄, H₂O₂, KClO₃. Simpan terpisah dari bahan reduktor dan mudah terbakar."},
        {"name": "Logam Reaktif", "emoji": "⚙️", "desc": "Natrium, Kalium, Magnesium. Simpan dalam minyak mineral."},
        {"name": "Gas Bertekanan", "emoji": "💨", "desc": "O₂, H₂, CO₂. Ikat silinder dengan aman dan simpan di area berventilasi."}
    ]
    
    cols = st.columns(3)
    for i, group in enumerate(storage_groups):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="element-card">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:36px; margin-right:15px;">{group['emoji']}</span>
                    <h3 style="margin:0;">{group['name']}</h3>
                </div>
                <p style="font-size:16px; color:{text_color};">{group['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.subheader("🔄 Tabel Kompatibilitas Bahan Kimia")
    st.markdown("""
    <p style="font-size:16px; margin-bottom:20px;">Tabel berikut menunjukkan kelompok bahan kimia yang dapat disimpan bersama dan yang harus dipisahkan:</p>
    """, unsafe_allow_html=True)
    
    compatibility_data = {
        "Kelompok": ["Asam Anorganik", "Basa", "Pelarut Organik", "Oksidator", "Logam Reaktif", "Gas Bertekanan"],
        "Asam Anorganik": ["✅", "❌", "⚠️", "❌", "❌", "✅"],
        "Basa": ["❌", "✅", "⚠️", "❌", "❌", "✅"],
        "Pelarut Organik": ["⚠️", "⚠️", "✅", "❌", "❌", "⚠️"],
        "Oksidator": ["❌", "❌", "❌", "✅", "❌", "❌"],
        "Logam Reaktif": ["❌", "❌", "❌", "❌", "✅", "✅"],
        "Gas Bertekanan": ["✅", "✅", "⚠️", "❌", "✅", "✅"]
    }
    
    df = pd.DataFrame(compatibility_data)
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    st.subheader("📦 Prinsip Penyimpanan Aman")
    storage_principles = [
        "Simpan bahan kimia berdasarkan kelompok kompatibilitas, bukan berdasarkan abjad",
        "Gunakan wadah sekunder untuk bahan korosif dan beracun",
        "Beri label jelas dengan nama bahan, konsentrasi, tanggal pembuatan, dan simbol bahaya",
        "Batasi jumlah bahan kimia yang disimpan di meja kerja",
        "Simpan bahan mudah terbakar di lemari tahan api",
        "Periksa kondisi wadah penyimpanan secara berkala",
        "Simpan bahan yang tidak stabil di tempat gelap dan dingin",
        "Gunakan sistem inventaris FIFO (First In First Out)",
        "Sediakan material penyerap untuk penanganan tumpahan"
    ]
    
    for i, principle in enumerate(storage_principles):
        st.markdown(f"""
        <div class="element-card" style="padding:15px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:15px; color:{dark_color};">📦</span>
                <p style="margin:0; font-size:16px; color:{text_color};">{i+1}. {principle}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("🧯 Tanggap Darurat")
    emergency_measures = [
        "Tumpahan kecil: Gunakan material penyerap dan sarung tangan",
        "Tumpahan besar: Evakuasi area dan hubungi petugas tanggap darurat",
        "Kontak kulit: Bilas dengan air mengalir minimal 15 menit",
        "Kontak mata: Gunakan eye wash station selama 15 menit",
        "Tertelan: Jangan dimuntahkan kecuali diinstruksikan profesional",
        "Kebakaran kecil: Gunakan alat pemadam api yang sesuai",
        "Kebakaran besar: Aktifkan alarm dan evakuasi"
    ]
    
    for i, measure in enumerate(emergency_measures):
        st.markdown(f"""
        <div class="element-card" style="padding:15px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:15px; color:{dark_color};">🚨</span>
                <p style="margin:0; font-size:16px; color:{text_color};">{i+1}. {measure}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# UI Utama
st.markdown("""
<div class="page-title">
    <h1>🔬 Laboratorium Kimia Interaktif</h1>
    <p>Jelajahi tabel periodik, simulasikan reaksi kimia, dan pelajari konsep kimia dengan cara menyenangkan</p>
</div>
""", unsafe_allow_html=True)

# Tab navigasi
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tabel Periodik", "🧪 Simulator Reaksi", "📚 Ensiklopedia Kimia", "🛡️ Penanganan Bahan Kimia"])

with tab1:
    show_periodic_table()

with tab2:
    show_reaction_simulator()

with tab3:
    show_additional_info()

with tab4:
    show_chemical_safety()

# Footer
st.divider()
st.markdown("""
<div style="text-align:center; padding:30px; color:#1A535C;">
    <p style="font-size:18px; margin:0;">🔬 Laboratorium Kimia Interaktif © 2023</p>
    <p style="font-size:16px; margin:10px 0;">Dikembangkan dengan Streamlit | Untuk tujuan edukasi</p>
    <p style="font-size:14px; margin:0;">Versi 3.0 | Terakhir diperbarui: 18 Juli 2023</p>
</div>
""", unsafe_allow_html=True)
