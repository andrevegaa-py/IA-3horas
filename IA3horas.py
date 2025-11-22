import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🏭")

# --- 2. GESTIÓN DE NAVEGACIÓN ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (MODO DARK - VISIBILIDAD TOTAL) ---
estilos_tech = """
<style>
    /* Fondo Tecnológico */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.98)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    /* --- FUERZA BRUTA: TODO TEXTO A BLANCO --- */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong { 
        color: #FFFFFF !important; 
        font-family: 'Segoe UI', sans-serif; 
    }
    
    /* Tarjetas Glassmorphism */
    .glass-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(8px);
        margin-bottom: 15px;
        color: #FFFFFF !important; /* Asegura texto blanco dentro */
    }

    /* Botones */
    .stButton>button {
        width: 100%; background-color: #0F172A; color: #38BDF8 !important; border: 1px solid #38BDF8;
        border-radius: 6px; padding: 10px; font-weight: 600; text-transform: uppercase; transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #38BDF8; color: #0F172A !important; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }
    .stButton>button p { color: inherit !important; }
    
    /* Métricas (Asegurar visibilidad) */
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-weight: bold; opacity: 0.9; }
    [data-testid="stMetricDelta"] { color: #E0E0E0 !important; background-color: rgba(0,0,0,0.3); padding: 2px 5px; border-radius: 4px;}
    
    /* Tablas */
    [data-testid="stDataFrame"] { background-color: rgba(0,0,0,0.2); }
    [data-testid="stDataFrame"] div { color: white !important; }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS (IMÁGENES ACTUALIZADAS AQUÍ) ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_DASHBOARD = "https://img.freepik.com/free-photo/business-concept-with-graphic-holography_23-2149160929.jpg"

# NUEVA IMAGEN TALARA (Vista nocturna impresionante)
IMG_TALARA = "https://i0.wp.com/www.rumbominero.com/wp-content/uploads/2022/04/Refineria-de-Talara.jpg" 

# NUEVA IMAGEN PETROLITO (Asesor Virtual Holográfico)
IMG_ROBOT = "https://img.freepik.com/free-photo/futuristic-robot-artificial-intelligence-concept_23-2151039287.jpg"

# --- FUNCIONES DE DATOS ---
def get_talara_waterfall():
    return pd.DataFrame({
        'Concepto': ['Presupuesto Inicial (2008)', 'Actualización (2012)', 'Contrato EPC (2014)', 'Unidades Auxiliares', 'Intereses Finan.', 'Costo Final'],
        'Monto': [1300, 2000, 1000, 800, 3400, 0],
        'Medida': ["relative", "relative", "relative", "relative", "relative", "total"]
    })

def get_talara_funding():
    return pd.DataFrame({
        'Fuente': ['Bonos Corporativos', 'Préstamos Sindicados', 'Aporte Estado', 'Recursos Propios'],
        'Monto_B': [4.3, 1.3, 1.5, 1.4]
    })

def get_dashboard_data():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ingresos_2024 = [120, 135, 110, 140, 155, 160]
    ingresos_2023 = [110, 125, 115, 130, 140, 145] 
    gastos = [115, 130, 125, 135, 145, 150] 
    ebitda = [x - y for x, y in zip(ingresos_2024, gastos)]
    return pd.DataFrame({'Mes': meses, '2024': ingresos_2024, '2023': ingresos_2023, 'Gastos': gastos, 'EBITDA': ebitda})

def get_rankings():
    costos = pd.DataFrame({
        'Unidad': ['Refinería Talara', 'Oleoducto Norperuano', 'Planta Ventas Lima', 'Administración Central', 'Logística Selva'],
        'Gasto_M': [850, 320, 150, 120, 80],
        'Cambio_Anual': ['+12%', '+5%', '-2%', '+1%', '+4%']
    })
    return costos

# --- HELPER PARA GRÁFICOS BLANCOS ---
def layout_blanco(fig, titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color='white', size=18)),
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'), # TEXTO GENERAL BLANCO
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', title_font=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', title_font=dict(color='white')),
        legend=dict(font=dict(color='white')),
        uniformtext_minsize=10, uniformtext_mode='hide'
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
    st.caption("v14.2 - Visual Upgrade")

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
        st.markdown("### 🏭 Historia de Talara")
        if st.button("Ver Auditoría ➔", key="b1"): navegar_a('talara')
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
# VISTA 2: IMPACTO TALARA (CORREGIDO VISIBILIDAD)
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara (PMRT)")
    col_head, _ = st.columns([1, 5])
    with col_head:
        if st.button("⬅ Volver"): navegar_a('home')
    
    # --- 1. METRICAS ---
    st.markdown("#### 1. El Salto Cuántico del Presupuesto")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📅 Inicio de Obra", "2014", "Retraso: 5 años")
    m2.metric("💰 Presupuesto Inicial", "$1.3 B", "Estimado 2008")
    m3.metric("💸 Costo Final + Intereses", "$8.5 B", "+553% vs Inicial", delta_color="inverse")
    m4.metric("📉 Rentabilidad (TIR)", "2.8%", "Baja Rentabilidad")

    st.markdown("---")

    # --- 2. CASCADA ---
    c_water, c_info = st.columns([2, 1])
    
    with c_water:
        st.markdown("**🔍 Anatomía del Sobrecosto (Billones USD)**")
        df_w = get_talara_waterfall()
        
        fig_w = go.Figure(go.Waterfall(
            name = "Costo", orientation = "v",
            measure = df_w['Medida'], x = df_w['Concepto'], y = df_w['Monto'],
            text = ["+1.3", "+2.0", "+1.0", "+0.8", "+3.4", "8.5"],
            textposition = "outside",
            connector = {"line":{"color":"white"}},
            decreasing = {"marker":{"color":"green"}},
            increasing = {"marker":{"color":"#ff4444"}}, 
            totals = {"marker":{"color":"#33b5e5"}}
        ))
        fig_w = layout_blanco(fig_w, "Evolución del Costo Acumulado")
        # Forzar texto de datos a blanco
        fig_w.update_traces(textfont_color='white', textfont_size=12)
        st.plotly_chart(fig_w, use_container_width=True)

    with c_info:
        st.markdown("#### 📖 Historia de los Retrasos")
        st.markdown("""
        <div class="glass-card">
        <b>2014:</b> Se firma contrato EPC con Técnicas Reunidas (España).<br><br>
        <b>2017:</b> Emisión de bonos por $2,000M. Se detectan unidades auxiliares no presupuestadas.<br><br>
        <b>2020:</b> Pandemia COVID-19 paraliza obras. Costos fijos siguen corriendo.<br><br>
        <b>2022:</b> Inicio de pruebas graduales. Crisis de liquidez por pago de deuda.<br><br>
        <b>2024:</b> Operación plena, pero con carga financiera crítica.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 3. PIE CHART Y GANTT ---
    c_pie, c_time = st.columns(2)
    
    with c_pie:
        st.markdown("**🏦 ¿Quién financió esto?**")
        df_f = get_talara_funding()
        fig_p = px.pie(df_f, values='Monto_B', names='Fuente', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_p = layout_blanco(fig_p, "")
        # Etiquetas Pie Chart blancas
        fig_p.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(fig_p, use_container_width=True)

    with c_time:
        st.markdown("**⏳ Cronograma: Planificado vs Real**")
        df_gantt = pd.DataFrame([
            dict(Task="Plan Original", Start='2014-01-01', Finish='2019-12-31', Color='Plan'),
            dict(Task="Ejecución Real", Start='2014-01-01', Finish='2023-12-31', Color='Real')
        ])
        fig_g = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Color", color_discrete_map={'Plan': '#00C851', 'Real': '#ff4444'})
        fig_g = layout_blanco(fig_g, "Desviación de Tiempo (4 años de retraso)")
        st.plotly_chart(fig_g, use_container_width=True)

# ==================================================
# VISTA 3: DASHBOARD
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    st.title("⚡ Monitor Financiero Integral")
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Volver"): navegar_a('home')

    st.markdown("#### 1. Indicadores Clave & Variación Anual")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💵 Caja Disponible", "$15.4 M", "-12% vs 2023", border=True)
    k2.metric("🛢️ Precio WTI", "$76.50", "+4.5% vs 2023", border=True)
    k3.metric("📉 Deuda Total", "$8.5 B", "+3.6% vs 2023", border=True)
    k4.metric("📊 EBITDA Ajustado", "$120 M", "+8.2% vs 2023", border=True)

    st.markdown("---")
    st.markdown("#### 2. Evolución Financiera (Ingresos YoY)")
    
    df_fin = get_dashboard_data()
    df_rank = get_rankings()

    c_main, c_side = st.columns([2, 1])
    with c_main:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['2024'], name='Ingresos 2024', marker_color='#00C851'))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['2023'], name='Ingresos 2023', line=dict(color='white', width=2, dash='dash')))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['EBITDA'], name='EBITDA Actual', fill='tozeroy', line=dict(color='#33b5e5', width=0), opacity=0.3))
        fig_bar = layout_blanco(fig_bar, "Comparativa Ingresos: 2023 vs 2024")
        fig_bar.update_layout(barmode='overlay', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_side:
        st.markdown("**🏆 Ranking: Centros de Costo**")
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            y=df_rank['Unidad'], x=df_rank['Gasto_M'], orientation='h',
            marker_color=['#ff4444', '#ffbb33', '#00C851', '#33b5e5', '#aa66cc'],
            text=df_rank['Cambio_Anual'], textposition='auto', textfont_color='white'
        ))
        fig_rank = layout_blanco(fig_rank, "Top 5 Gastos (Millones $)")
        fig_rank.update_layout(height=400, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_rank, use_container_width=True)

    st.markdown("---")
    c_risk, c_table = st.columns([1, 2])
    with c_risk:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = 35, 
            title = {'text': "Nivel de Estrés Financiero", 'font': {'color': 'white'}},
            number = {'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': 'white'}, 'bar': {'color': "#ff4444"},
                'steps': [{'range': [0, 50], 'color': "rgba(0, 255, 0, 0.2)"}, {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.2)"}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 85}
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with c_table:
        st.markdown("#### 📋 Detalle de Pasivos por Banco (Ranking)")
        df_bancos = pd.DataFrame({
            'Institución': ['Banco Nación', 'Bonos Internacionales', 'Banco Extranjero A', 'Banco Local B'],
            'Monto Deuda ($M)': [2500, 4000, 1200, 800],
            'Tasa Interés': ['4.5%', '7.2%', '6.1%', '5.8%'],
            'Vencimiento': ['2030', '2047', '2026', '2025']
        })
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
            if "deuda" in prompt.lower(): resp = "La deuda asciende a $8.5 Billones. Petrolito te informa que gran parte son Bonos emitidos en 2017 y 2021."
            elif "sobrecosto" in prompt.lower() or "costo" in prompt.lower(): resp = "El sobrecosto es significativo: de $1.3B iniciales a más de $8.5B. Esto se debe a intereses, retrasos por pandemia y unidades auxiliares no previstas."
            else: resp = "Interesante consulta. Basado en mis registros históricos, esa métrica requiere análisis. ¿Te gustaría ver el desglose de Talara?"
        
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
                <li style="margin-bottom: 10px;">🔹 <i>"¿Por qué costó tanto Talara?"</i></li>
                <li style="margin-bottom: 10px;">🔹 <i>"¿Cuándo se pagan los bonos?"</i></li>
                <li style="margin-bottom: 10px;">🔹 <i>"¿Cuánto retraso tuvo la obra?"</i></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_benef:
        st.markdown("#### 🚀 ¿Por qué consultar a Petrolito?")
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #38BDF8;">
            <b>🧠 Memoria Total:</b> Recuerda cada dólar gastado desde 2014.<br><br>
            <b>⚡ Auditoría Flash:</b> Explica sobrecostos en segundos.<br><br>
            <b>🤝 Visión 360:</b> Cruza datos de operación con deuda financiera.
        </div>
        """, unsafe_allow_html=True)
