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

# --- 3. ESTILOS CSS (TECH-FORMAL) ---
estilos_tech = """
<style>
    /* Fondo Tecnológico */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.94), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    /* Tipografía y Colores */
    h1, h2, h3, h4, p, li, div { color: #E2E8F0 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Tarjetas Glassmorphism */
    .glass-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
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
    
    /* Métricas */
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 5px rgba(56, 189, 248, 0.3); }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_TALARA = "https://portal.andina.pe/EDPfotografia3/Thumbnail/2023/07/19/000969550W.jpg" 
IMG_DASHBOARD = "https://img.freepik.com/free-photo/business-concept-with-graphic-holography_23-2149160929.jpg"
IMG_ROBOT = "https://img.freepik.com/free-photo/rendering-smart-home-device_23-2151039302.jpg"

# --- FUNCIONES DE DATOS ---
def get_dashboard_data():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ingresos = [120, 135, 110, 140, 155, 160]
    gastos = [115, 130, 125, 135, 145, 150] 
    ebitda = [x - y for x, y in zip(ingresos, gastos)]
    return pd.DataFrame({'Mes': meses, 'Ingresos': ingresos, 'Gastos': gastos, 'EBITDA': ebitda})

def get_expense_breakdown():
    return pd.DataFrame({
        'Categoría': ['Servicio Deuda (Talara)', 'Compra Crudo/Insumos', 'Operaciones (OPEX)', 'Personal', 'Otros'],
        'Monto': [45, 30, 15, 7, 3]
    })

# ==================================================
# BARRA LATERAL
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: white; padding: 10px; border-radius: 10px; text-align: center;'><img src='{IMG_LOGO}' width='140'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Centro de Control")
    if st.button("🏠 INICIO"): navegar_a('home')
    st.markdown("---")
    st.info("🔹 **Estado:** En Línea")
    st.caption("v12.1 - Powered by Petrolito AI")

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
    fig.update_layout(
        title="Capex vs Deuda ($ Billones)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(overlaying='y', side='right'), legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# VISTA 3: DASHBOARD
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    st.title("⚡ Monitor Financiero Integral")
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Volver"): navegar_a('home')

    st.markdown("#### 1. Indicadores de Liquidez y Mercado")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💵 Caja Disponible", "$15.4 M", "-2.1%", border=True)
    k2.metric("🛢️ Precio WTI", "$76.50", "+1.2%", border=True)
    k3.metric("📉 Deuda Total", "$8.5 B", "Estable", border=True)
    k4.metric("📊 Margen Refinación", "$11.2/bbl", "+0.5", border=True)

    st.markdown("---")
    st.markdown("#### 2. Análisis de Resultados y Gastos")
    
    df_fin = get_dashboard_data()
    df_exp = get_expense_breakdown()

    c_left, c_right = st.columns([2, 1])
    with c_left:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['Ingresos'], name='Ingresos', marker_color='#00C851'))
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['Gastos'], name='Gastos', marker_color='#ff4444'))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['EBITDA'], name='EBITDA', line=dict(color='yellow', width=3, dash='dot')))
        fig_bar.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='#E2E8F0'), height=350, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_right:
        fig_pie = px.pie(df_exp, values='Monto', names='Categoría', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='#E2E8F0'), height=350, showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    c_risk, c_info = st.columns([1, 2])
    with c_risk:
        # --- CORRECCIÓN DEL ERROR AQUÍ ---
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", 
            value = 35, 
            title = {'text': "Nivel de Estrés Financiero"},
            gauge = {
                'axis': {'range': [0, 100]}, 
                'bar': {'color': "#ff4444"},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(0, 255, 0, 0.1)"}, 
                    {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.1)"}
                ],
                'threshold': { # Ahora threshold está dentro de gauge
                    'line': {'color': "white", 'width': 4}, 
                    'thickness': 0.75, 
                    'value': 85
                }
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'), height=250, margin=dict(t=30, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with c_info:
        st.info("ℹ️ **Petrolito informa:** El nivel de estrés es moderado. Se recomienda vigilar la liquidez.")

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
            # Lógica de Petrolito
            if "deuda" in prompt.lower(): resp = "La deuda asciende a $8.5 Billones. Aunque es alta, Petrolito te informa que está estructurada a largo plazo gracias a los bonos emitidos."
            elif "gasto" in prompt.lower(): resp = "Detecto que el 45% de los gastos son financieros (pagos de Talara). Sugiero optimizar el OPEX para liberar caja."
            else: resp = "Interesante consulta. Basado en mis registros históricos, esa métrica es estable. ¿Te gustaría ver una proyección a 3 meses?"
        
        st.session_state.messages.append({"role": "assistant", "content": resp})
        with chat_container:
            st.chat_message("assistant", avatar="🤖").write(resp)

    # --- SECCIÓN DE AYUDA Y BENEFICIOS ---
    st.markdown("---")
    col_sugg, col_benef = st.columns(2)

    with col_sugg:
        st.markdown("#### 💡 Preguntas para Petrolito")
        st.markdown("""
        <div class="glass-card">
            <ul style="list-style-type: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 10px;">🔹 <i>"¿Cómo cerró la caja ayer?"</i></li>
                <li style="margin-bottom: 10px;">🔹 <i>"Explícame la deuda de Talara."</i></li>
                <li style="margin-bottom: 10px;">🔹 <i>"¿Qué pasa si sube el petróleo?"</i></li>
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
