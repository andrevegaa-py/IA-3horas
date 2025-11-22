import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
import random

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
    /* 1. FONDO GENERAL */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.94), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    /* 2. SIDEBAR */
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
IMG_TALARA_GENERADA = "http://googleusercontent.com/image_generation_content/0" # Tu imagen generada
IMG_FLAG_ICON = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Flag_of_Peru.svg/128px-Flag_of_Peru.svg.png"

# --- FUNCIONES DE DATOS (BASE DE CONOCIMIENTO) ---
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

# --- CEREBRO DE PETROLITO (NUEVO LOGIC) ---
def generar_respuesta_inteligente(prompt):
    prompt = prompt.lower()
    
    # Datos Dinámicos para usar en respuestas
    df_dash = get_dashboard_data()
    ultimo_ebitda = df_dash['EBITDA'].iloc[-1]
    ingreso_actual = df_dash['2024'].iloc[-1]
    tendencia = "positiva" if ingreso_actual > df_dash['2024'].iloc[-2] else "negativa"
    
    # 1. CATEGORÍA: DEUDA Y FINANZAS
    if any(x in prompt for in ['deuda', 'pasivo', 'bancos', 'bonos', 'debo']):
        base = "La deuda total estructural asciende a **$8.5 Billones**. "
        detalle = "Esta cifra se compone principalmente de los Bonos emitidos en 2017 ($2MM) y 2021, con vencimientos largos (2047). "
        analisis = "Aunque el monto asusta, es una deuda a largo plazo. El problema real son los intereses a corto plazo que nos quitan liquidez operativa. "
        consejo = "Recomendaría vigilar el ratio Deuda/EBITDA este trimestre."
        return base + detalle + analisis + consejo

    # 2. CATEGORÍA: TALARA / REFINERÍA
    elif any(x in prompt for in ['talara', 'refineria', 'pmrt', 'costo', 'retraso']):
        base = "La Nueva Refinería de Talara (NRT) tuvo un costo final aproximado de **$6,500 millones** (sin intereses), elevándose a $8.5B con gastos financieros. "
        contexto = "El proyecto sufrió retrasos por la pandemia y problemas con contratistas auxiliares. "
        suposicion = "Si la refinería opera al 100% de capacidad (95k barriles/día) durante todo el 2025, proyectamos que el margen de refinación podría cubrir el servicio de la deuda, pero apenas. "
        return base + contexto + suposicion

    # 3. CATEGORÍA: RESULTADOS / UTILIDAD / GANANCIA
    elif any(x in prompt for in ['ganancia', 'perdida', 'utilidad', 'ebitda', 'resultado', 'rentable']):
        base = f"Actualmente el EBITDA es de **${ultimo_ebitda} Millones** en el último mes reportado. "
        analisis = f"Estamos viendo una tendencia **{tendencia}** en los ingresos ({ingreso_actual}M). "
        explicacion = "Sin embargo, la utilidad neta sigue presionada. ¿Por qué? Porque aunque vendemos bien, pagamos muchos intereses y el tipo de cambio afecta nuestras compras de crudo. "
        return base + analisis + explicacion

    # 4. CATEGORÍA: MERCADO / WTI / PRECIOS
    elif any(x in prompt for in ['wti', 'precio', 'crudo', 'mercado', 'petroleo']):
        wti_actual = 76.50
        base = f"El WTI ronda los **${wti_actual}**. "
        escenario = "Supongamos que el WTI sube a $85: Nuestros ingresos subirían, pero también el costo de importar crudo. "
        impacto = "Para Petroperú, lo ideal es un WTI estable. La volatilidad alta nos obliga a usar coberturas (hedging) que cuestan dinero. "
        return base + escenario + impacto

    # 5. RESPUESTA DE RESPALDO (FALLBACK INTELIGENTE)
    else:
        # Si no entiende, genera una hipótesis educada
        return ("Esa es una pregunta compleja que requiere cruzar varias variables. "
                "Basado en la situación financiera general, mi análisis preliminar sugiere que deberíamos priorizar la liquidez de corto plazo. "
                "Si te refieres a un tema operativo específico, ten en cuenta que la eficiencia de Talara es el factor #1 para cualquier proyección de mejora. "
                "¿Te gustaría que analice cómo impactaría esto en el flujo de caja?")

# ==================================================
# BARRA LATERAL
# ==================================================
with st.sidebar:
    c_icon, c_space = st.columns([1, 4])
    with c_icon: st.image(IMG_FLAG_ICON, width=40)
    
    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); margin-top: 10px;'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 10px; margin-bottom: 20px;'><i style='color: #38BDF8; font-size: 14px; font-weight: 600;'>Energía que mueve el desarrollo</i></div>", unsafe_allow_html=True)

    st.markdown("### 👤 Usuario")
    c_prof1, c_prof2 = st.columns([1, 3])
    with c_prof1: st.markdown(f"<img src='{IMG_USER}' style='width: 50px; height: 50px; border-radius: 50%; border: 2px solid #38BDF8;'>", unsafe_allow_html=True)
    with c_prof2: st.markdown("<div style='color: white; font-weight: bold;'>Gerencia Finanzas</div><div style='color: #00C851; font-size: 11px;'>● Activo</div>", unsafe_allow_html=True)
    
    st.divider()
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
        st.image(IMG_TALARA_GENERADA, use_column_width=True)
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
# VISTA 2: TALARA
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara")
    if st.button("⬅ Volver al Inicio"): navegar_a('home')
    st.write("")
    st.image(IMG_TALARA_GENERADA, caption="Vista Aérea NRT - Generación AI", use_column_width=True)
    st.write("")
    st.markdown("---")
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
        st.markdown("""<div class="glass-card">El PMRT representa la mayor inversión industrial pública.<br><br><b>Hitos:</b><br>• Bonos (2017)<br>• Crisis (2022)<br>• Operación (2024)</div>""", unsafe_allow_html=True)
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
        df_gantt = pd.DataFrame([dict(Task="Plan Original", Start='2014-01-01', Finish='2019-12-31', Color='Plan'), dict(Task="Ejecución Real", Start='2014-01-01', Finish='2023-12-31', Color='Real')])
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
        fig_rank.add_trace(go.Bar(y=df_rank['Unidad'], x=df_rank['Gasto_M'], orientation='h', marker_color=['#ff4444', '#ffbb33', '#00C851', '#33b5e5', '#aa66cc'], text=df_rank['Cambio_Anual'], textposition='auto', textfont_color='white'))
        fig_rank = layout_blanco(fig_rank, "")
        fig_rank.update_layout(height=400)
        st.plotly_chart(fig_rank, use_container_width=True)
    st.markdown("---")
    c_risk, c_table = st.columns([1, 2])
    with c_risk:
        st.markdown("**Nivel de Riesgo**")
        fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = 35, number = {'font': {'color': 'white'}}, gauge = {'axis': {'range': [0, 100], 'tickcolor': 'white'}, 'bar': {'color': "#ff4444"}, 'steps': [{'range': [0, 50], 'color': "rgba(0, 255, 0, 0.2)"}, {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.2)"}], 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 85}}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
    with c_table:
        st.markdown("#### 📋 Pasivos Bancarios")
        df_bancos = pd.DataFrame({'Banco': ['Nación', 'Bonos Int.', 'Extranjero A', 'Local B'], 'Deuda': [2500, 4000, 1200, 800], 'Tasa': ['4.5%', '7.2%', '6.1%', '5.8%'], 'Vence': ['2030', '2047', '2026', '2025']})
        st.dataframe(df_bancos, use_container_width=True, hide_index=True)

# ==================================================
# VISTA 4: CHAT PETROLITO (RENOVADO)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    c_title, c_img = st.columns([3, 1])
    with c_title: st.title("🤖 Petrolito: Asesor IA")
    with c_img: st.image(IMG_ROBOT, width=100)
        
    if st.button("⬅ Volver"): navegar_a('home')

    chat_container = st.container()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy Petrolito. Tengo acceso completo a la data de Finanzas, Talara y Mercado. Hazme cualquier pregunta compleja, estoy listo."}]

    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

    if prompt := st.chat_input("Ej: ¿Qué pasa con el EBITDA si el WTI baja?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user", avatar="🧑‍💻").write(prompt)
        
        # --- LLAMADA A LA NUEVA INTELIGENCIA ---
        with st.spinner("Analizando bases de datos y proyectando escenarios..."):
            time.sleep(1.5) # Simula procesamiento
            respuesta_ia = generar_respuesta_inteligente(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
        with chat_container:
            st.chat_message("assistant", avatar="🤖").write(respuesta_ia)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 💡 Sugerencias")
        st.markdown("<div class='glass-card'>🔹 <i>'¿Cómo impacta el precio del WTI en mi EBITDA?'</i><br>🔹 <i>'¿La refinería es rentable actualmente?'</i><br>🔹 <i>'Analiza la estructura de la deuda.'</i></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("#### 🚀 Capacidades V2.0")
        st.markdown("<div class='glass-card'>🧠 <b>Inferencia Lógica:</b> Cruza variables para responder.<br>⚡ <b>Simulación:</b> Proyecta escenarios 'What-if'.</div>", unsafe_allow_html=True)
