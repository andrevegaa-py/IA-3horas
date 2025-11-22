import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🧬")

# --- 2. GESTIÓN DE NAVEGACIÓN (SESSION STATE) ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (FONDO TECNOLÓGICO FORMAL) ---
# Fondo azul oscuro profundo con partículas sutiles + Tarjetas estilo "Glassmorphism"
estilos_tech = """
<style>
    /* Fondo Tecnológico Formal */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.95)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    /* Estilo de Textos */
    h1, h2, h3, h4, p, li {
        color: #E2E8F0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Tarjetas Interactivas (Glassmorphism) */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* Botones Estilizados (Cyber-Formal) */
    .stButton>button {
        width: 100%;
        background-color: #0F172A;
        color: #38BDF8; /* Azul Neon Suave */
        border: 1px solid #38BDF8;
        border-radius: 8px;
        padding: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #38BDF8;
        color: #0F172A;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        text-shadow: 0 0 5px rgba(56, 189, 248, 0.3);
    }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS IMÁGENES ---
IMG_TALARA = "https://portal.andina.pe/EDPfotografia3/Thumbnail/2023/07/19/000969550W.jpg"
IMG_DASHBOARD = "https://img.freepik.com/free-photo/business-concept-with-graphic-holography_23-2149160929.jpg"
IMG_ROBOT = "https://img.freepik.com/free-photo/rendering-smart-home-device_23-2151039302.jpg"
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"

# --- FUNCIONES DE DATOS ---
def get_data_talara():
    data = {
        'Año': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'Deuda': [5.2, 5.5, 5.8, 6.2, 6.5, 7.8, 8.2, 8.5],
        'Inversion': [1400, 1100, 900, 600, 500, 350, 150, 50]
    }
    return pd.DataFrame(data)

# ==================================================
# BARRA LATERAL (SIEMPRE VISIBLE)
# ==================================================
with st.sidebar:
    # Logo con fondo blanco para que se vea bien
    st.markdown(f"<div style='background: white; padding: 10px; border-radius: 10px; text-align: center;'><img src='{IMG_LOGO}' width='150'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Centro de Control")
    
    if st.button("🏠 INICIO / MENÚ"):
        navegar_a('home')
    
    st.markdown("---")
    st.info("🔹 **Estado del Sistema:** En Línea")
    st.caption("v10.0 Tech-Enterprise")

# ==================================================
# VISTA 1: HOME (EL MENÚ INTERACTIVO VISUAL)
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú: Plataforma de Inteligencia Financiera")
    st.markdown("#### Seleccione un módulo para iniciar el análisis:")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # TARJETA 1: IMPACTO TALARA
    with col1:
        st.image(IMG_TALARA, use_column_width=True)
        st.markdown("### 🏭 Impacto Refinería")
        st.caption("Análisis histórico de la deuda, inversión (Capex) y sostenibilidad del proyecto Talara.")
        if st.button("Ver Análisis Talara ➔", key="btn_talara"):
            navegar_a('talara')

    # TARJETA 2: TIEMPO REAL
    with col2:
        st.image(IMG_DASHBOARD, use_column_width=True)
        st.markdown("### ⚡ Monitor en Vivo")
        st.caption("Dashboard de tesorería, flujo de caja diario y cotización del crudo WTI en tiempo real.")
        if st.button("Ver Dashboard ➔", key="btn_dash"):
            navegar_a('dashboard')

    # TARJETA 3: ASISTENTE IA
    with col3:
        st.image(IMG_ROBOT, use_column_width=True)
        st.markdown("### 🤖 Asesor IA")
        st.caption("Consultas financieras avanzadas con lenguaje natural. Pregunte sobre deuda, caja o riesgos.")
        if st.button("Iniciar Chat ➔", key="btn_chat"):
            navegar_a('chat')

# ==================================================
# VISTA 2: IMPACTO TALARA
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Análisis de Impacto: Nueva Refinería Talara")
    st.markdown("Evolución de la Deuda Estructural vs Inversión de Capital")
    
    if st.button("⬅ Volver al Menú Principal"):
        navegar_a('home')
    
    df = get_data_talara()
    
    # Gráfico Tech
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Año'], y=df['Inversion'], name='Inversión (Capex)', marker_color='#38BDF8')) # Azul Neon
    fig.add_trace(go.Scatter(x=df['Año'], y=df['Deuda'], name='Deuda Total ($B)', yaxis='y2', line=dict(color='#F472B6', width=3))) # Rosa Neon
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        yaxis=dict(title="Inversión (M USD)", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="Deuda Acumulada ($B)", overlaying='y', side='right'),
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    c1, c2 = st.columns(2)
    c1.info("La línea **Rosada** muestra cómo la deuda escaló hasta los $8.5B.")
    c2.info("Las barras **Azules** muestran el dinero inyectado en la construcción.")

# ==================================================
# VISTA 3: DASHBOARD TIEMPO REAL
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    st.title("⚡ Monitor de Tesorería en Tiempo Real")
    
    col_btn, col_space = st.columns([1, 5])
    with col_btn:
        if st.button("⬅ Volver"):
            navegar_a('home')

    # Simulador
    caja_val = 15.4 
    wti_val = 76.5
    
    # Métricas estilo Tech
    c1, c2, c3 = st.columns(3)
    c1.metric("💵 Caja Disponible", f"${caja_val} M", "-0.5%")
    c2.metric("🛢️ Precio WTI", f"${wti_val}", "+1.2%")
    c3.markdown("### Estado: :orange[ALERTA MEDIA]")

    # Gráfico de Linea Neon
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Caja", "WTI", "Deuda"])
    st.line_chart(chart_data)

# ==================================================
# VISTA 4: CHAT IA
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Asesor Financiero Inteligente")
    st.caption("Modo: Consultor Senior | Data: 2014-2025")
    
    if st.button("⬅ Volver al Menú"):
        navegar_a('home')

    # Chat UI
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Bienvenido al centro de inteligencia. Analizo datos de Petroperú en tiempo real. ¿Desea revisar la deuda de Talara o el flujo de caja?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Escriba su consulta financiera..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Lógica simple de respuesta
        resp = "Procesando consulta..."
        with st.spinner("Analizando nodos de datos..."):
            time.sleep(1)
            if "deuda" in prompt.lower():
                resp = "La deuda estructural asciende a **$8.5 Billones**. El apalancamiento es crítico debido al PMRT."
            elif "talara" in prompt.lower():
                resp = "La Refinería Talara ya está operativa, pero los costos financieros de su construcción siguen presionando la caja."
            else:
                resp = "Entendido. Basado en los indicadores actuales, sugiero cautela en el gasto operativo (OPEX)."
        
        st.session_state.messages.append({"role": "assistant", "content": resp})
        st.chat_message("assistant").write(resp)
