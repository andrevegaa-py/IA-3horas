import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🏭")

# --- 2. GESTIÓN DE NAVEGACIÓN ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'
if 'moneda' not in st.session_state:
    st.session_state.moneda = "USD ($)"

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL MASTERPIECE) ---
estilos_tech = """
<style>
    /* 1. FONDO GENERAL E INTEGRADO */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.94), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    /* 2. SIDEBAR (Fusión Perfecta) */
    [data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    /* 3. TIPOGRAFÍA BLANCA */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* 4. UI ELEMENTS */
    .glass-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px; padding: 20px;
        backdrop-filter: blur(8px); margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%; background-color: #1E293B; color: #38BDF8 !important; 
        border: 1px solid #38BDF8; border-radius: 6px; padding: 10px; 
        font-weight: 600; text-transform: uppercase; transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #38BDF8; color: #0F172A !important; box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
    }
    
    /* 5. IMAGENES Y MÉTRICAS */
    img { border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS Y RECURSOS ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_USER = "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg"
IMG_ROBOT = "https://img.freepik.com/free-photo/futuristic-robot-artificial-intelligence-concept_23-2151039287.jpg"

# Fallback por si no guardan la foto local
IMG_TALARA_WEB = "https://i0.wp.com/www.rumbominero.com/wp-content/uploads/2022/04/Refineria-de-Talara.jpg" 

# --- FUNCIONES DE DATOS ---
def get_talara_waterfall():
    return pd.DataFrame({
        'Concepto': ['Presupuesto Inicial', 'Actualización', 'Contrato EPC', 'Auxiliares', 'Intereses', 'Costo Final'],
        'Monto': [1300, 2000, 1000, 800, 3400, 0],
        'Medida': ["relative", "relative", "relative", "relative", "relative", "total"]
    })

def get_talara_funding():
    return pd.DataFrame({
        'Fuente': ['Bonos Corp.', 'Préstamos', 'Estado', 'Propios'],
        'Monto_B': [4.3, 1.3, 1.5, 1.4]
    })

def get_dashboard_data():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    return pd.DataFrame({
        'Mes': meses, 
        '2024': [120, 135, 110, 140, 155, 160], 
        '2023': [110, 125, 115, 130, 140, 145], 
        'EBITDA': [5, 5, -15, 5, 10, 10]
    })

def get_rankings():
    return pd.DataFrame({
        'Unidad': ['Refinería Talara', 'Oleoducto', 'Ventas Lima', 'Admin', 'Logística'],
        'Gasto_M': [850, 320, 150, 120, 80],
        'Cambio_Anual': ['+12%', '+5%', '-2%', '+1%', '+4%']
    })

# --- HELPER LAYOUT ---
def layout_blanco(fig, titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color='white', size=18)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
        legend=dict(font=dict(color='white')),
        uniformtext_minsize=10, uniformtext_mode='hide'
    )
    return fig

# ==================================================
# BARRA LATERAL (PERSONALIZADA)
# ==================================================
with st.sidebar:
    # 1. Logo + Refrán Corporativo
    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); margin-bottom: 10px;'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)
    
    # REFRÁN / SLOGAN
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <i style='color: #38BDF8; font-size: 14px; font-weight: bold;'>"Energía que mueve el desarrollo"</i>
    </div>
    """, unsafe_allow_html=True)

    # 2. Perfil de Usuario
    st.markdown("### 👤 Usuario")
    c_prof1, c_prof2 = st.columns([1, 3])
    with c_prof1:
        st.markdown(f"<img src='{IMG_USER}' style='width: 50px; height: 50px; border-radius: 50%; border: 2px solid #38BDF8;'>", unsafe_allow_html=True)
    with c_prof2:
        st.markdown("<div style='color: white; font-weight: bold;'>Gerencia Finanzas</div><div style='color: #00C851; font-size: 11px;'>● Activo</div>", unsafe_allow_html=True)
    
    st.divider()

    # 3. Navegación
    if st.button("🏠 DASHBOARD"): navegar_a('home')
    
    st.markdown("### 🛠️ Tools")
    moneda = st.selectbox("Divisa", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    
    st.divider()
    st.info("🔒 Conexión Segura")

# ==================================================
# VISTA 1: HOME
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú: Plataforma de Inteligencia Financiera")
    st.markdown("#### Seleccione un módulo estratégico:")
    st.write("") 

    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Intentamos mostrar la foto local si existe en el home también, si no, web
        if os.path.exists("talara_foto.jpg"):
            st.image("talara_foto.jpg", use_column_width=True)
        else:
            st.image(IMG_TALARA_WEB, use_column_width=True)
        st.markdown("### 🏭 Historia de Talara")
        if st.button("Acceder ➔", key="b1"): navegar_a('talara')

    with c2:
        st.image("https://img.freepik.com/free-photo/standard-quality-control-collage-concept_23-2149595831.jpg", use_column_width=True)
        st.markdown("### ⚡ Monitor Financiero")
        if st.button("Acceder ➔", key="b2"): navegar_a('dashboard')

    with c3:
        st.image("https://img.freepik.com/free-photo/rpa-concept-with-blurry-hand-touching-screen_23-2149311914.jpg", use_column_width=True)
        st.markdown("### 🤖 Petrolito AI")
        if st.button("Consultar ➔", key="b3"): navegar_a('chat')

# ==================================================
# VISTA 2: TALARA (CON TU FOTO)
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara")
    
    if st.button("⬅ Volver al Inicio"): navegar_a('home')
    
    # --- IMAGEN DEL USUARIO (TU FOTO) ---
    st.write("")
    # Verificamos si la imagen existe localmente, sino usamos fallback
    if os.path.exists("talara_foto.jpg"):
        st.image("talara_foto.jpg", caption="Vista Aérea Actualizada - NRT", use_column_width=True)
    else:
        st.warning("⚠️ No encontré el archivo 'talara_foto.jpg'. Mostrando imagen referencial.")
        st.image(IMG_TALARA_WEB, caption="Vista Referencial NRT", use_column_width=True)
    
    st.markdown("---")

    # Métricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📅 Inicio Obra", "2014", "5 años retraso")
    m2.metric("💰 Presupuesto Base", "$1.3 B", "2008")
    m3.metric("💸 Costo Final", "$8.5 B", "+553%", delta_color="inverse")
    m4.metric("📉 TIR", "2.8%", "Crítico")

    st.markdown("---")
    c_water, c_info = st.columns([2, 1])
    
    with c_water:
        st.markdown("**🔍 Anatomía del Sobrecosto**")
        df_w = get_talara_waterfall()
        fig_w = go.Figure(go.Waterfall(
            name = "Costo", orientation = "v", measure = df_w['Medida'], x = df_w['Concepto'], y = df_w['Monto'],
            text = ["+1.3", "+2.0", "+1.0", "+0.8", "+3.4", "8.5"], textposition = "outside",
            connector = {"line":{"color":"white"}}, decreasing = {"marker":{"color":"green"}},
            increasing = {"marker":{"color":"#ff4444"}}, totals = {"marker":{"color":"#33b5e5"}}
        ))
        fig_w = layout_blanco(fig_w, "")
        fig_w.update_traces(textfont_color='white')
        st.plotly_chart(fig_w, use_container_width=True)

    with c_info:
        st.markdown("#### 📖 Resumen Ejecutivo")
        st.markdown("""
        <div class="glass-card">
        El PMRT (Proyecto Modernización Refinería Talara) representa la mayor inversión industrial pública en la historia del Perú.
        <br><br>
        <b>Principales hitos:</b><br>
        • Emisión de bonos (2017)<br>
        • Crisis de liquidez (2022)<br>
        • Operación plena (2024)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c_pie, c_time = st.columns(2)
    with c_pie:
        st.markdown("**🏦 Financiamiento**")
        df_f = get_talara_funding()
        fig_p = px.pie(df_f, values='Monto_B', names='Fuente', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_p = layout_blanco(fig_p, "")
        fig_p.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(fig_p, use_container_width=True)

    with c_time:
        st.markdown("**⏳ Cronograma**")
        df_gantt = pd.DataFrame([
            dict(Task="Plan Original", Start='2014-01-01', Finish='2019-12-31', Color='Plan'),
            dict(Task="Ejecución Real", Start='2014-01-01', Finish='2023-12-31', Color='Real')
        ])
        fig_g = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Color", color_discrete_map={'Plan': '#00C851', 'Real': '#ff4444'})
        fig_g = layout_blanco(fig_g, "")
        st.plotly_chart(fig_g, use_container_width=True)

# ==================================================
# VISTA 3: DASHBOARD
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    moneda_sim = "$" if st.session_state.moneda == "USD ($)" else "S/."
    st.title(f"⚡ Monitor Financiero ({st.session_state.moneda})")
    if st.button("⬅ Volver"): navegar_a('home')

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💵 Caja", f"{moneda_sim} 15.4 M", "-12%", border=True)
    k2.metric("🛢️ WTI", "$76.50", "+4.5%", border=True)
    k3.metric("📉 Deuda", f"{moneda_sim} 8.5 B", "+3.6%", border=True)
    k4.metric("📊 EBITDA", f"{moneda_sim} 120 M", "+8.2%", border=True)

    st.markdown("---")
    df_fin = get_dashboard_data()
    df_rank = get_rankings()

    c_main, c_side = st.columns([2, 1])
    with c_main:
        st.markdown("**Ingresos vs Gastos**")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['2024'], name='2024', marker_color='#00C851'))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['2023'], name='2023', line=dict(color='white', dash='dash')))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['EBITDA'], name='EBITDA', fill='tozeroy', line=dict(color='#33b5e5', width=0), opacity=0.3))
        fig_bar = layout_blanco(fig_bar, "")
        fig_bar.update_layout(barmode='overlay', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_side:
        st.markdown("**🏆 Centros de Costo**")
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            y=df_rank['Unidad'], x=df_rank['Gasto_M'], orientation='h',
            marker_color=['#ff4444', '#ffbb33', '#00C851', '#33b5e5', '#aa66cc'],
            text=df_rank['Cambio_Anual'], textposition='auto', textfont_color='white'
        ))
        fig_rank = layout_blanco(fig_rank, "")
        fig_rank.update_layout(height=400)
        st.plotly_chart(fig_rank, use_container_width=True)

# ==================================================
# VISTA 4: CHAT PETROLITO (CON IMAGEN NUEVA)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    c_title, c_img = st.columns([3, 1])
    with c_title:
        st.title("🤖 Petrolito: Asesor IA")
    with c_img:
        st.image(IMG_ROBOT, width=100)
        
    if st.button("⬅ Volver"): navegar_a('home')

    chat_container = st.container()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hola, soy Petrolito. ¿En qué puedo ayudarte hoy?"}]

    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

    if prompt := st.chat_input("Escribe aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user", avatar="🧑‍💻").write(prompt)
        
        resp = "Procesando..."
        with st.spinner("Pensando..."):
            time.sleep(1)
            if "deuda" in prompt.lower(): resp = "La deuda es de $8.5B. Principalmente Bonos 2047."
            elif "talara" in prompt.lower(): resp = "Talara costó $8.5B total. Operativa pero con alta carga financiera."
            else: resp = "Interesante. Revisa el dashboard para más detalles."
        
        st.session_state.messages.append({"role": "assistant", "content": resp})
        with chat_container:
            st.chat_message("assistant", avatar="🤖").write(resp)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 💡 Sugerencias")
        st.markdown("<div class='glass-card'>🔹 <i>'¿Deuda actual?'</i><br>🔹 <i>'¿Sobrecosto Talara?'</i></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("#### 🚀 Beneficios")
        st.markdown("<div class='glass-card'>🧠 <b>Memoria 2014-2025</b><br>⚡ <b>Análisis en tiempo real</b></div>", unsafe_allow_html=True)
