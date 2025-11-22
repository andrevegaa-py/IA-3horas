import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🧬")

# --- 2. GESTIÓN DE NAVEGACIÓN ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (MODO DARK TECH - LETRAS BLANCAS) ---
estilos_tech = """
<style>
    /* Fondo Tecnológico */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.98)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    /* FORZAR LETRAS BLANCAS EN TODA LA APP */
    h1, h2, h3, h4, h5, p, li, div, span, label { color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Tarjetas Glassmorphism */
    .glass-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(8px);
        margin-bottom: 15px;
    }

    /* Botones */
    .stButton>button {
        width: 100%; background-color: #0F172A; color: #38BDF8; border: 1px solid #38BDF8;
        border-radius: 6px; padding: 10px; font-weight: 600; text-transform: uppercase; transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #38BDF8; color: #0F172A; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }
    .stButton>button p { color: inherit !important; } /* Fix para texto de botones */
    
    /* Métricas */
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
    [data-testid="stMetricLabel"] { color: #E0E0E0 !important; }
    [data-testid="stMetricDelta"] { color: #E0E0E0 !important; }
    
    /* Tablas */
    [data-testid="stDataFrame"] { background-color: rgba(0,0,0,0.2); }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_TALARA = "https://portal.andina.pe/EDPfotografia3/Thumbnail/2023/07/19/000969550W.jpg" 
IMG_DASHBOARD = "https://img.freepik.com/free-photo/business-concept-with-graphic-holography_23-2149160929.jpg"
IMG_ROBOT = "https://img.freepik.com/free-photo/rendering-smart-home-device_23-2151039302.jpg"

# --- FUNCIONES DE DATOS AVANZADOS ---
def get_dashboard_data():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ingresos_2024 = [120, 135, 110, 140, 155, 160]
    ingresos_2023 = [110, 125, 115, 130, 140, 145] # Data año pasado
    gastos = [115, 130, 125, 135, 145, 150] 
    ebitda = [x - y for x, y in zip(ingresos_2024, gastos)]
    return pd.DataFrame({'Mes': meses, '2024': ingresos_2024, '2023': ingresos_2023, 'Gastos': gastos, 'EBITDA': ebitda})

def get_rankings():
    # Ranking de Centros de Costo (Donde se gasta más)
    costos = pd.DataFrame({
        'Unidad': ['Refinería Talara', 'Oleoducto Norperuano', 'Planta Ventas Lima', 'Administración Central', 'Logística Selva'],
        'Gasto_M': [850, 320, 150, 120, 80],
        'Cambio_Anual': ['+12%', '+5%', '-2%', '+1%', '+4%']
    })
    return costos

# --- HELPERS PARA GRÁFICOS BLANCOS ---
def layout_blanco(fig, titulo):
    fig.update_layout(
        title=titulo,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'), # <--- CLAVE: Letras blancas
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
        legend=dict(font=dict(color='white'))
    )
    return fig

# ==================================================
# BARRA LATERAL
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: white; padding: 10px; border-radius: 10px; text-align: center;'><img src='{IMG_LOGO}' width='140'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Centro de Control")
    if st.button("🏠 INICIO"): navegar_a('home')
    st.markdown("---")
    st.info("🔹 **Estado:** En Línea")
    st.caption("v13.0 - Dashboard Pro")

# ==================================================
# VISTA 1: HOME
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú: Plataforma de Inteligencia Financiera")
    st.markdown("#### Seleccione un módulo para iniciar el análisis:")
    st.write("") 

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(IMG_TALARA, use_column_width=True)
        st.markdown("### 🏭 Impacto Talara")
        if st.button("Ver Análisis ➔", key="b1"): navegar_a('talara')
    with col2:
        st.image(IMG_DASHBOARD, use_column_width=True)
        st.markdown("### ⚡ Monitor Financiero")
        if st.button("Ver Dashboard ➔", key="b2"): navegar_a('dashboard')
    with col3:
        st.image(IMG_ROBOT, use_column_width=True)
        st.markdown("### 🤖 Petrolito AI")
        st.caption("Tu nuevo compañero financiero inteligente.")
        if st.button("Hablar con Petrolito ➔", key="b3"): navegar_a('chat')

# ==================================================
# VISTA 2: IMPACTO TALARA
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Impacto: Nueva Refinería Talara")
    if st.button("⬅ Volver"): navegar_a('home')
    
    df_t = pd.DataFrame({
        'Año': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'Deuda': [5.5, 5.8, 6.2, 6.5, 7.8, 8.2, 8.5],
        'Inversion': [1100, 900, 600, 500, 350, 150, 50]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_t['Año'], y=df_t['Inversion'], name='Capex (Inversión)', marker_color='#38BDF8'))
    fig.add_trace(go.Scatter(x=df_t['Año'], y=df_t['Deuda'], name='Deuda Acumulada', yaxis='y2', line=dict(color='#F472B6', width=3)))
    fig = layout_blanco(fig, "Capex vs Deuda ($ Billones)")
    fig.update_layout(yaxis2=dict(overlaying='y', side='right', color='white'), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# VISTA 3: DASHBOARD (MEJORADO)
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    st.title("⚡ Monitor Financiero Integral")
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Volver"): navegar_a('home')

    # --- SECCIÓN 1: KPIs COMPARATIVOS (ANUALES) ---
    st.markdown("#### 1. Indicadores Clave & Variación Anual")
    k1, k2, k3, k4 = st.columns(4)
    # Usamos métricas con deltas para mostrar cambio anual
    k1.metric("💵 Caja Disponible", "$15.4 M", "-12% vs 2023", border=True)
    k2.metric("🛢️ Precio WTI", "$76.50", "+4.5% vs 2023", border=True)
    k3.metric("📉 Deuda Total", "$8.5 B", "+3.6% vs 2023", border=True) # Deuda subió (rojo automático)
    k4.metric("📊 EBITDA Ajustado", "$120 M", "+8.2% vs 2023", border=True)

    st.markdown("---")
    
    # --- SECCIÓN 2: ANÁLISIS GRÁFICO ---
    st.markdown("#### 2. Evolución Financiera (Ingresos YoY)")
    
    df_fin = get_dashboard_data()
    df_rank = get_rankings()

    c_main, c_side = st.columns([2, 1])

    with c_main:
        # GRÁFICO COMPARATIVO 2023 vs 2024
        fig_bar = go.Figure()
        # Barras 2024
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['2024'], name='Ingresos 2024', marker_color='#00C851'))
        # Línea 2023 (Comparativa)
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['2023'], name='Ingresos 2023', line=dict(color='white', width=2, dash='dash')))
        # Área de EBITDA
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['EBITDA'], name='EBITDA Actual', fill='tozeroy', line=dict(color='#33b5e5', width=0), opacity=0.3))
        
        fig_bar = layout_blanco(fig_bar, "Comparativa Ingresos: 2023 vs 2024")
        fig_bar.update_layout(barmode='overlay', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_side:
        # RANKING DE GASTOS (NUEVO)
        st.markdown("**🏆 Ranking: Centros de Costo**")
        # Usamos un gráfico de barras horizontales para el ranking
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            y=df_rank['Unidad'], 
            x=df_rank['Gasto_M'], 
            orientation='h',
            marker_color=['#ff4444', '#ffbb33', '#00C851', '#33b5e5', '#aa66cc'],
            text=df_rank['Cambio_Anual'],
            textposition='auto'
        ))
        fig_rank = layout_blanco(fig_rank, "Top 5 Gastos (Millones $)")
        fig_rank.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_rank, use_container_width=True)

    # --- SECCIÓN 3: MEDIDOR DE RIESGO Y RANKING DEUDA ---
    st.markdown("---")
    c_risk, c_table = st.columns([1, 2])
    
    with c_risk:
        # GAUGE CHART (Color Blanco en texto asegurado)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = 35, 
            title = {'text': "Nivel de Estrés Financiero", 'font': {'color': 'white'}}, # Título blanco
            number = {'font': {'color': 'white'}}, # Número blanco
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': 'white'}, 
                'bar': {'color': "#ff4444"},
                'steps': [{'range': [0, 50], 'color': "rgba(0, 255, 0, 0.2)"}, {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.2)"}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 85}
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with c_table:
        st.markdown("#### 📋 Detalle de Pasivos por Banco (Ranking)")
        # Tabla estilizada con Pandas
        df_bancos = pd.DataFrame({
            'Institución': ['Banco Nación', 'Bonos Internacionales', 'Banco Extranjero A', 'Banco Local B'],
            'Monto Deuda ($M)': [2500, 4000, 1200, 800],
            'Tasa Interés': ['4.5%', '7.2%', '6.1%', '5.8%'],
            'Vencimiento': ['2030', '2047', '2026', '2025']
        })
        # Mostramos la tabla ocupando el ancho
        st.dataframe(df_bancos, use_container_width=True, hide_index=True)

# ==================================================
# VISTA 4: CHAT PETROLITO
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Petrolito: Tu Asesor Financiero")
    if st.button("⬅ Volver"): navegar_a('home')

    chat_container = st.container()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy Petrolito. Conozco toda la historia financiera de la empresa. ¿En qué puedo ayudarte hoy?"}]

    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

    if prompt := st.chat_input("Pregúntale a Petrolito..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user", avatar="🧑‍💻").write(prompt)
        
        resp = "Procesando..."
        with st.spinner("Petrolito está pensando..."):
            time.sleep(1)
            if "deuda" in prompt.lower(): resp = "La deuda asciende a $8.5 Billones. Aunque es alta, Petrolito te informa que está estructurada a largo plazo gracias a los bonos emitidos."
            elif "gasto" in prompt.lower(): resp = "El Centro de Costo 'Refinería Talara' representa el mayor gasto operativo ($850M), con un incremento del 12% respecto al año anterior."
            else: resp = "Interesante consulta. Basado en mis registros históricos, esa métrica es estable. ¿Te gustaría ver una proyección a 3 meses?"
        
        st.session_state.messages.append({"role": "assistant", "content": resp})
        with chat_container:
            st.chat_message("assistant", avatar="🤖").write(resp)

    st.markdown("---")
    col_sugg, col_benef = st.columns(2)
    with col_sugg:
        st.markdown("#### 💡 Preguntas para Petrolito")
        st.markdown("""
        <div class="glass-card">
            <ul style="list-style-type: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 10px;">🔹 <i>"¿Cómo cerró la caja ayer?"</i></li>
                <li style="margin-bottom: 10px;">🔹 <i>"Explícame la deuda de Talara."</i></li>
                <li style="margin-bottom: 10px;">🔹 <i>"¿Qué centro de costo gasta más?"</i></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_benef:
        st.markdown("#### 🚀 ¿Por qué consultar a Petrolito?")
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #38BDF8;">
            <b>🧠 Memoria Total:</b> Recuerda datos desde el inicio del proyecto Talara.<br><br>
            <b>⚡ Alertas Rápidas:</b> Te avisa si los indicadores se ponen rojos.<br><br>
            <b>🤝 Socio Estratégico:</b> Te ayuda a entender los números difíciles.
        </div>
        """, unsafe_allow_html=True)
