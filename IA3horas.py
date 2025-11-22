import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🏭")

# --- 2. GESTIÓN DE NAVEGACIÓN Y ESTADO ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'
if 'moneda' not in st.session_state:
    st.session_state.moneda = "USD ($)"
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hola. Soy Petrolito, tu socio estratégico. Analizo deuda, costos de refino y proyecciones de caja. ¿Qué escenario financiero revisamos hoy?"
    }]

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL IMPACT) ---
estilos_tech = """
<style>
    /* FONDO GENERAL */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.94), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    /* TIPOGRAFÍA */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* UI COMPONENTS */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1E293B !important; color: white !important; border: 1px solid #38BDF8;
    }
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

    /* IMÁGENES Y MÉTRICAS */
    img { border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; opacity: 0.9; }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS DE IMÁGENES ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_USER = "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg"
IMG_SIDEBAR_BANNER = "https://img.freepik.com/free-photo/oil-refinery-twilight_1112-575.jpg"
IMG_CARD_TALARA = "https://portal.andina.pe/EDPfotografia3/Thumbnail/2022/04/12/000862854W.jpg"
IMG_CARD_FINANCE = "https://img.freepik.com/free-photo/standard-quality-control-collage-concept_23-2149595831.jpg"
IMG_CARD_AI = "https://img.freepik.com/free-photo/rpa-concept-with-blurry-hand-touching-screen_23-2149311914.jpg"

# --- 4. LÓGICA AVANZADA (CEREBRO DE PETROLITO) ---
def cerebro_financiero_avanzado(prompt):
    prompt = prompt.lower()
    
    # 1. BASE DE CONOCIMIENTO (Contexto Estructurado)
    db_conocimiento = {
        "liquidez": {
            "dato": "Ratio corriente de 0.6x (Crítico)",
            "analisis": "Indica incapacidad temporal de cubrir pasivos a corto plazo sin inyección de capital o rollover.",
            "accion": "Sugerencia: Revisar la tabla de 'Pasivos Bancarios' para priorizar pagos."
        },
        "ebitda": {
            "dato": "USD 120 Millones (Proyectado 2024)",
            "analisis": "El margen operativo es positivo, pero insuficiente para cubrir el servicio de deuda anual (Intereses > EBITDA).",
            "accion": "Foco: Maximizar producción en Talara para diluir costos fijos."
        },
        "talara": {
            "dato": "Inversión total USD 8.5 Billones (100% Operativa)",
            "analisis": "La refinería ya genera margen, pero el costo hundido y los intereses capitalizados presionan el P&L.",
            "accion": "Ver gráfico Waterfall en la sección 'Historia de Talara'."
        },
        "bonos": {
            "dato": "Bono 2047 cotizando con descuento significativo",
            "analisis": "El mercado percibe un riesgo crediticio elevado (High Yield), esperando garantías del Estado.",
            "accion": "Estrategia: Evaluar opciones de recompra de deuda si mejora la caja."
        },
        "deuda": {
            "dato": "Deuda Total aprox. USD 8.5 Billones",
            "analisis": "Estructura pesada a largo plazo. Principal acreedor: Bonistas internacionales y CESCE.",
            "accion": "Monitorizar el riesgo cambiario si la deuda es en USD y los ingresos en Soles."
        }
    }

    # 2. MOTOR DE BÚSQUEDA (Keywords -> Respuesta Estructurada)
    for key, info in db_conocimiento.items():
        # Búsqueda directa o sinónimos comunes
        match_found = False
        if key in prompt: match_found = True
        if key == "liquidez" and "caja" in prompt: match_found = True
        if key == "talara" and ("refineria" in prompt or "refinería" in prompt): match_found = True

        if match_found:
            return (
                f"📊 **Dato Técnico:** {info['dato']}\n\n"
                f"🧠 **Análisis:** {info['analisis']}\n\n"
                f"🚀 **Recomendación:** {info['accion']}"
            )
    
    # 3. LÓGICA DIFUSA Y SUPOSICIONES (Fallback Inteligente)
    # Si no hay dato exacto, "piensa" y asume contexto para no cortar la charla.
    
    if any(x in prompt for x in ["futuro", "proyección", "2025", "visión", "largo plazo"]):
        return (
            "Aunque no tengo la proyección oficial cargada para esa variable específica, **basado en la tendencia histórica y precios del crudo**:\n\n"
            "1. Es probable que la presión de caja continúe los próximos 2 trimestres.\n"
            "2. Se asume que el WTI se mantendrá volátil entre $70-$80.\n\n"
            "¿Desea que simule un escenario de estrés financiero en el Dashboard?"
        )
    
    elif any(x in prompt for x in ["riesgo", "peligro", "alerta", "problema"]):
        return (
            "Detecto que le preocupa el perfil de riesgo. Aunque no especificó el indicador, **mi análisis general sugiere**:\n\n"
            "El riesgo principal hoy es la **liquidez inmediata**, más que la solvencia a largo plazo (ya que Talara es un activo productivo). "
            "El cuello de botella es el capital de trabajo.\n\n"
            "¿Revisamos los pasivos bancarios que vencen este mes?"
        )
    
    elif any(x in prompt for x in ["hola", "buenos", "saludo"]):
        return "¡Hola! Soy Petrolito. Estoy listo para analizar estados financieros, costos de Talara o ratios de liquidez. ¿Por dónde empezamos?"

    else:
        # Respuesta de Continuidad (Nunca "no sé")
        return (
            "Esa consulta es interesante y requiere correlacionar variables operativas que no están en mi vista rápida. "
            "Sin embargo, **la lógica financiera dicta que** cualquier ineficiencia operativa impactará directamente en el Flujo de Caja Libre.\n\n"
            "Podemos abordar esto desde dos ángulos:\n"
            "A) Analizar los Gastos Operativos.\n"
            "B) Ver el impacto en el EBITDA.\n\n"
            "¿Cuál prefiere profundizar?"
        )

# --- 5. FUNCIONES DE DATOS (DUMMY DATA) ---
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

def get_csv_download():
    df = get_dashboard_data()
    return df.to_csv(index=False).encode('utf-8')

def layout_blanco(fig, titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color='white', size=18)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', title_font=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', title_font=dict(color='white')),
        legend=dict(font=dict(color='white')),
        uniformtext_minsize=10, uniformtext_mode='hide'
    )
    return fig

# ==================================================
# BARRA LATERAL (VISUALMENTE RICA)
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); margin-bottom: 20px;'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)

    st.markdown("### 👤 Usuario Conectado")
    c_prof1, c_prof2 = st.columns([1, 3])
    with c_prof1:
        st.markdown(f"<img src='{IMG_USER}' style='width: 60px; height: 60px; border-radius: 50%; border: 2px solid #38BDF8;'>", unsafe_allow_html=True)
    with c_prof2:
        st.markdown("""
        <div style='padding-left: 5px;'>
            <div style='color: white; font-weight: bold; font-size: 16px;'>Admin Finanzas</div>
            <div style='color: #00C851; font-size: 12px; font-weight: bold;'>● En Línea</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    if st.button("🏠 DASHBOARD PRINCIPAL"): navegar_a('home')

    st.markdown("### 🛠️ Herramientas")
    moneda = st.selectbox("Moneda", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    unidad = st.selectbox("Escala", ["Millones (MM)", "Miles (k)"])

    csv = get_csv_download()
    st.download_button("📥 Descargar Reporte", data=csv, file_name='reporte.csv', mime='text/csv')
    
    st.write("") 
    st.markdown("### 🌍 Sostenibilidad")
    st.image(IMG_SIDEBAR_BANNER, caption="Operaciones Talara - Turno Noche", use_column_width=True)
    st.caption("Monitoreo ambiental activo: ✅ Normal")

# ==================================================
# VISTA 1: HOME
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú: Plataforma de Inteligencia Financiera")
    st.markdown("#### Seleccione un módulo estratégico:")
    st.write("") 

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image(IMG_CARD_TALARA, use_column_width=True)
        st.markdown("### 🏭 Historia de Talara")
        st.info("Auditoría de deuda y construcción.")
        if st.button("Acceder ➔", key="b1"): navegar_a('talara')

    with c2:
        st.image(IMG_CARD_FINANCE, use_column_width=True)
        st.markdown("### ⚡ Monitor Financiero")
        st.info("KPIs de liquidez y EBITDA en vivo.")
        if st.button("Acceder ➔", key="b2"): navegar_a('dashboard')

    with c3:
        st.image(IMG_CARD_AI, use_column_width=True)
        st.markdown("### 🤖 Petrolito AI")
        st.info("Tu analista virtual 24/7.")
        if st.button("Consultar ➔", key="b3"): navegar_a('chat')

# ==================================================
# VISTA 2: TALARA
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara")
    col_head, _ = st.columns([1, 5])
    with col_head:
        if st.button("⬅ Volver"): navegar_a('home')
    
    st.markdown("#### 1. El Salto Cuántico del Presupuesto")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📅 Inicio", "2014", "5 años retraso")
    m2.metric("💰 Presupuesto", "$1.3 B", "2008")
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
        st.markdown("#### 📖 Hitos Clave")
        st.markdown("""
        <div class="glass-card">
        <b>2014:</b> Firma EPC Técnicas Reunidas.<br><br>
        <b>2017:</b> Bonos $2,000M emitidos.<br><br>
        <b>2020:</b> Paralización COVID-19.<br><br>
        <b>2022:</b> Crisis de liquidez.<br><br>
        <b>2024:</b> Operación plena.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c_pie, c_time = st.columns(2)
    with c_pie:
        st.markdown("**🏦 Estructura de Financiamiento**")
        df_f = get_talara_funding()
        fig_p = px.pie(df_f, values='Monto_B', names='Fuente', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_p = layout_blanco(fig_p, "")
        fig_p.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(fig_p, use_container_width=True)

    with c_time:
        st.markdown("**⏳ Cronograma Real**")
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
    col_back, _ = st.columns([1, 6])
    with col_back:
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
        st.markdown("**Ingresos vs Gastos (YoY)**")
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

    st.markdown("---")
    c_risk, c_table = st.columns([1, 2])
    with c_risk:
        st.markdown("**Nivel de Riesgo**")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = 35, number = {'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': 'white'}, 'bar': {'color': "#ff4444"},
                'steps': [{'range': [0, 50], 'color': "rgba(0, 255, 0, 0.2)"}, {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.2)"}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 85}
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with c_table:
        st.markdown("#### 📋 Pasivos Bancarios")
        df_bancos = pd.DataFrame({
            'Banco': ['Nación', 'Bonos Int.', 'Extranjero A', 'Local B'],
            'Deuda': [2500, 4000, 1200, 800], 'Tasa': ['4.5%', '7.2%', '6.1%', '5.8%'], 'Vence': ['2030', '2047', '2026', '2025']
        })
        st.dataframe(df_bancos, use_container_width=True, hide_index=True)

# ==================================================
# VISTA 4: CHAT (OPTIMIZADO CON CEREBRO)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Petrolito AI: Socio Estratégico")
    st.markdown("Modo: *Análisis Financiero Continuo & Predictivo*")
    
    if st.button("⬅ Volver al Dashboard"): navegar_a('home')

    # Contenedor principal del chat
    chat_container = st.container()

    # Renderizar historial previo
    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            
            # Estilo diferenciado para usuario vs bot
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div style="background-color: rgba(30, 41, 59, 0.8); border-left: 4px solid #38BDF8; padding: 15px; border-radius: 4px; margin-bottom: 10px;">
                    <small style="color: #38BDF8;">PETROLITO AI</small><br>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.05); text-align: right; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)

    # Input del usuario
    if prompt := st.chat_input("Consulte sobre deuda, Talara, EBITDA o proyecciones..."):
        # 1. Guardar mensaje usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Mostrar mensaje usuario inmediatamente
        with chat_container:
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.05); text-align: right; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                {prompt}
            </div>
            """, unsafe_allow_html=True)
        
        # 3. Procesar respuesta con "Efecto Pensando"
        with chat_container:
            placeholder = st.empty()
            placeholder.markdown("Credits computing... 🟢")
            time.sleep(0.8) # Simula carga
            
            # --- LLAMADA AL CEREBRO ---
            respuesta_ia = cerebro_financiero_avanzado(prompt)
            
            # Simulación de escritura (Typewriter effect)
            full_res = ""
            header_html = '<div style="background-color: rgba(30, 41, 59, 0.8); border-left: 4px solid #38BDF8; padding: 15px; border-radius: 4px; margin-bottom: 10px;"><small style="color: #38BDF8;">PETROLITO AI</small><br>'
            
            for char in respuesta_ia.split(" "):
                full_res += char + " "
                placeholder.markdown(f"{header_html}{full_res}▌</div>", unsafe_allow_html=True)
                time.sleep(0.04)
            
            placeholder.markdown(f"{header_html}{full_res}</div>", unsafe_allow_html=True)
        
        # 4. Guardar respuesta en historial
        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})

    st.markdown("---")
    st.caption("💡 Petrolito utiliza lógica difusa para responder consultas sin datos exactos. Verifique siempre con el reporte oficial.")
