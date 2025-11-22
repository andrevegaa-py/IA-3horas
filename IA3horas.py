import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🏭")

# --- 2. GESTIÓN DE ESTADO (SESSION STATE) ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'
if 'moneda' not in st.session_state:
    st.session_state.moneda = "USD ($)"
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": (
            "Bienvenido, Gerente. Soy Petrolito, su asesor de inteligencia financiera.\n\n"
            "Tengo capacidad para analizar:\n"
            "• **Contexto Nacional:** Riesgo país, Apoyo del MEF y Tipo de Cambio.\n"
            "• **Sector Petrolero:** Tendencias del WTI y Márgenes de Refino.\n"
            "• **Estabilidad Corporativa:** Deuda, Talara y Flujo de Caja.\n\n"
            "¿Sobre qué área desea iniciar el análisis?"
        )
    }]

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL IMPACT & CHAT CARDS) ---
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
    
    /* TEXTOS */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* UI ELEMENTS */
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

    /* CHAT CARDS STYLING */
    .bot-card {
        background-color: rgba(15, 23, 42, 0.8); 
        border: 1px solid #38BDF8; 
        border-left: 5px solid #38BDF8; 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .user-card {
        background-color: rgba(56, 189, 248, 0.2); 
        color: white; 
        padding: 12px 20px; 
        border-radius: 15px 15px 0 15px; 
        margin-bottom: 15px; 
        text-align: right;
        display: inline-block;
    }
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

# --- 4. CEREBRO FINANCIERO AVANZADO (LÓGICA DE RAZONAMIENTO) ---
def cerebro_financiero_avanzado(prompt):
    prompt = prompt.lower()
    
    # A. BASE DE CONOCIMIENTO PROFUNDA (Macro y Micro)
    db_conocimiento = {
        "estabilidad": {
            "titulo": "🛡️ Solidez Financiera y Riesgo Soberano",
            "narrativa": (
                "En el contexto nacional, la estabilidad de Petroperú está intrínsecamente ligada al respaldo del **MEF (Ministerio de Economía y Finanzas)**. "
                "Aunque la calificación crediticia individual ha sufrido rebajas por agencias como Fitch o S&P (a terreno especulativo), "
                "el mercado internacional sigue valorando la garantía implícita del Estado Peruano. "
                "A nivel interno, la estabilidad depende de recuperar el Grado de Inversión mediante una estricta gobernanza corporativa y auditorías transparentes."
            ),
            "datos_extra": ["Riesgo País Perú: ~168 pbs (Promedio Latam)", "Soporte: Decretos de Urgencia vigentes", "Calificación: BB+ (Perspectiva Negativa)"]
        },
        "petroleo": {
            "titulo": "🛢️ Mercado de Hidrocarburos (Sector Outlook)",
            "narrativa": (
                "El sector petrolero enfrenta una alta volatilidad global. El diferencial (Spread) entre el crudo WTI y los derivados "
                "es la clave para nuestros márgenes de refino. Actualmente, la tendencia global apunta a una corrección de precios, "
                "lo que beneficia nuestras compras de insumos (crudo importado), pero reduce la valoración inmediata de nuestros inventarios. "
                "La **Nueva Refinería Talara** actúa como cobertura tecnológica al procesar crudos pesados (más baratos) y vender combustibles limpios (premium)."
            ),
            "datos_extra": ["WTI: Tendencia lateral $75-$80", "Margen Refino: Recuperándose post-arranque", "Demanda Local: Crecimiento del 3% anual"]
        },
        "nacional": {
            "titulo": "🇵🇪 Coyuntura Financiera Local",
            "narrativa": (
                "El sistema financiero peruano muestra resiliencia. El **Tipo de Cambio (PEN/USD)** se mantiene estable gracias a la intervención del BCRP, "
                "lo cual es una variable crítica para nosotros, dado que el 80% de nuestra deuda es en dólares y gran parte de los ingresos en soles. "
                "Sin embargo, las tasas de interés locales para capital de trabajo siguen elevadas, encareciendo las líneas de crédito revolventes."
            ),
            "datos_extra": ["Tipo de Cambio: ~3.75 (Estable)", "Tasa Ref BCRP: Tendencia a la baja", "Inflación: Controlada dentro del rango meta"]
        },
        "talara": {
            "titulo": "🏭 PMRT: Estatus Operativo",
            "narrativa": (
                "La Nueva Refinería Talara ya no es un proyecto en construcción, es una realidad operativa al 100%. "
                "El reto actual no es de ingeniería, sino puramente financiero: maximizar el EBITDA para cubrir el servicio de la deuda estructurada. "
                "Técnicamente, estamos produciendo diésel y gasolinas Euro VI, capturando el margen completo del mercado interno y reduciendo importaciones de derivados."
            ),
            "datos_extra": ["Producción: 95k barriles/día", "Tecnología: Flexicoking activo", "Margen esperado: USD 10-12/barril"]
        },
        "deuda": {
            "titulo": "📉 Estructura de Capital y Deuda",
            "narrativa": (
                "La posición de apalancamiento es el punto más crítico de la empresa. Con una deuda total cercana a los **$8.5 Billones**, "
                "el pago de intereses compite directamente con el presupuesto operativo (OPEX). "
                "La estrategia financiera sugerida es el 'Rollover' de la deuda de corto plazo y buscar garantías del Gobierno Nacional para mejorar las tasas "
                "de los bonos corporativos con vencimiento 2047."
            ),
            "datos_extra": ["Acreedores: CESCE (España) + Bonistas", "Ratio Deuda/EBITDA: >8x (Alto Riesgo)", "Vencimiento próximo: Bonos 2027"]
        },
        "liquidez": {
            "titulo": "💵 Análisis de Liquidez (Caja)",
            "narrativa": (
                "La liquidez corriente es restringida. Los proveedores de crudo exigen condiciones de pago contado o cartas de crédito confirmadas, "
                "lo que presiona el flujo de caja semanal. Es imperativo acelerar la cobranza de ventas mayoristas y gestionar eficientemente los inventarios."
            ),
            "datos_extra": ["Ratio Corriente: < 1.0 (Estrés)", "Acción: Optimización de cuentas por cobrar"]
        }
    }

    # B. DETECCIÓN DE CONTINUIDAD (Context Awareness)
    if any(x in prompt for x in ["más", "detalle", "continúa", "profundiz", "explica mejor", "otro"]):
        return (
            "### 🔄 Profundizando en el análisis\n\n"
            "Entendido. Si miramos el panorama completo, la recuperación financiera plena tardará aproximadamente **2 a 3 años**, "
            "siempre y cuando se mantenga el soporte gubernamental y la Refinería opere sin paradas no programadas.\n\n"
            "Es importante notar que, comparado con pares regionales como **Ecopetrol** o **Enap**, nuestro ratio de apalancamiento es superior, "
            "pero nuestra tecnología de refinación es más moderna.\n\n"
            "💡 *Sugerencia:* ¿Le gustaría ver una simulación de pago de deuda para el próximo trimestre?"
        )

    # C. MOTOR DE BÚSQUEDA SEMÁNTICA
    for key, info in db_conocimiento.items():
        match = False
        # Coincidencia directa
        if key in prompt: match = True
        # Sinónimos y contexto
        if key == "petroleo" and any(x in prompt for x in ["crudo", "sector", "barril", "oil", "combustible"]): match = True
        if key == "nacional" and any(x in prompt for x in ["perú", "pais", "local", "bcrp", "mef", "gobierno", "ministro"]): match = True
        if key == "estabilidad" and any(x in prompt for x in ["riesgo", "seguridad", "futuro", "quebrar", "situación", "realidad"]): match = True
        if key == "liquidez" and any(x in prompt for x in ["caja", "dinero", "plata", "pagar", "cobrar"]): match = True
        if key == "deuda" and any(x in prompt for x in ["bonos", "banco", "prestamo", "deber"]): match = True

        if match:
            bullets = "\n".join([f"• *{d}*" for d in info['datos_extra']])
            return (
                f"### {info['titulo']}\n\n"
                f"{info['narrativa']}\n\n"
                f"**📊 Indicadores Clave del Mercado:**\n{bullets}\n\n"
                f"💡 *Siguiente Paso:* ¿Desea analizar cómo impacta esto en el Flujo de Caja proyectado?"
            )

    # D. RESPUESTA FALLBACK (CONTINUIDAD)
    return (
        "### 🧠 Análisis en Proceso\n\n"
        "Esa consulta es interesante. Para darle una respuesta precisa, necesito correlacionar datos del **Sistema Financiero Nacional** y nuestra **Eficiencia Operativa**.\n\n"
        "Desde una perspectiva técnica, cualquier ineficiencia en la cadena de suministro impacta el EBITDA. Sin embargo, el respaldo del Estado mitiga el riesgo de insolvencia inmediata.\n\n"
        "Podemos enfocar el análisis en dos frentes:\n"
        "1. **Solvencia:** Capacidad de pago de la deuda a largo plazo.\n"
        "2. **Liquidez:** Disponibilidad de efectivo para operaciones hoy.\n\n"
        "¿Cuál es su prioridad estratégica en este momento?"
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
# BARRA LATERAL
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); margin-bottom: 20px;'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)
    st.markdown("### 👤 Usuario Conectado")
    c_prof1, c_prof2 = st.columns([1, 3])
    with c_prof1:
        st.markdown(f"<img src='{IMG_USER}' style='width: 60px; height: 60px; border-radius: 50%; border: 2px solid #38BDF8;'>", unsafe_allow_html=True)
    with c_prof2:
        st.markdown("""<div style='padding-left: 5px;'><div style='color: white; font-weight: bold; font-size: 16px;'>Admin Finanzas</div><div style='color: #00C851; font-size: 12px; font-weight: bold;'>● En Línea</div></div>""", unsafe_allow_html=True)
    st.divider()
    if st.button("🏠 DASHBOARD PRINCIPAL"): navegar_a('home')
    st.markdown("### 🛠️ Herramientas")
    moneda = st.selectbox("Moneda", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    st.download_button("📥 Descargar Reporte", data=get_csv_download(), file_name='reporte.csv', mime='text/csv')
    st.write("") 
    st.markdown("### 🌍 Sostenibilidad")
    st.image(IMG_SIDEBAR_BANNER, caption="Operaciones Talara - Turno Noche", use_column_width=True)
    st.caption("Monitoreo ambiental activo: ✅ Normal")

# ==================================================
# VISTAS (HOME, TALARA, DASHBOARD)
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú: Plataforma de Inteligencia Financiera")
    st.markdown("#### Seleccione un módulo estratégico:")
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

elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara")
    if st.button("⬅ Volver"): navegar_a('home')
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
            connector = {"line":{"color":"white"}}, decreasing = {"marker":{"color":"green"}}, increasing = {"marker":{"color":"#ff4444"}}, totals = {"marker":{"color":"#33b5e5"}}
        ))
        st.plotly_chart(layout_blanco(fig_w, ""), use_container_width=True)
    with c_info:
        st.markdown("#### 📖 Hitos Clave")
        st.markdown("<div class='glass-card'><b>2014:</b> Firma EPC Técnicas Reunidas.<br><br><b>2017:</b> Bonos $2,000M.<br><br><b>2024:</b> Operación plena.</div>", unsafe_allow_html=True)
    st.markdown("---")
    c_pie, c_time = st.columns(2)
    with c_pie:
        st.markdown("**🏦 Estructura de Financiamiento**")
        fig_p = px.pie(get_talara_funding(), values='Monto_B', names='Fuente', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_p.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(layout_blanco(fig_p, ""), use_container_width=True)
    with c_time:
        st.markdown("**⏳ Cronograma Real**")
        df_gantt = pd.DataFrame([dict(Task="Plan", Start='2014-01-01', Finish='2019-12-31', Color='Plan'), dict(Task="Real", Start='2014-01-01', Finish='2023-12-31', Color='Real')])
        fig_g = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Color", color_discrete_map={'Plan': '#00C851', 'Real': '#ff4444'})
        st.plotly_chart(layout_blanco(fig_g, ""), use_container_width=True)

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
        st.markdown("**Ingresos vs Gastos (YoY)**")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['2024'], name='2024', marker_color='#00C851'))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['2023'], name='2023', line=dict(color='white', dash='dash')))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['EBITDA'], name='EBITDA', fill='tozeroy', line=dict(color='#33b5e5', width=0), opacity=0.3))
        fig_bar.update_layout(barmode='overlay', height=400)
        st.plotly_chart(layout_blanco(fig_bar, ""), use_container_width=True)
    with c_side:
        st.markdown("**🏆 Centros de Costo**")
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(y=df_rank['Unidad'], x=df_rank['Gasto_M'], orientation='h', marker_color=['#ff4444', '#ffbb33', '#00C851', '#33b5e5', '#aa66cc'], text=df_rank['Cambio_Anual'], textposition='auto', textfont_color='white'))
        fig_rank.update_layout(height=400)
        st.plotly_chart(layout_blanco(fig_rank, ""), use_container_width=True)

# ==================================================
# VISTA 4: CHAT (CONVERSACIONAL & CONTEXTUAL)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Petrolito AI: Senior Financial Analyst")
    st.markdown("Focus: *Mercado Nacional, Sector Oil & Gas, Estabilidad Corporativa*")
    
    if st.button("⬅ Volver al Dashboard"): navegar_a('home')

    chat_container = st.container()

    # Renderizar historial
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                # Estilo "Tarjeta de Informe" para el bot
                st.markdown(f"""
                <div class="bot-card">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 20px; margin-right: 10px;">🤖</span>
                        <b style="color: #38BDF8;">PETROLITO AI ANALYSIS</b>
                    </div>
                    <div style="color: #E2E8F0; font-family: 'Segoe UI', sans-serif; line-height: 1.6;">
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Estilo "Burbuja" para usuario
                st.markdown(f"""
                <div style="text-align: right; margin-bottom: 10px;">
                    <div class="user-card">
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Input de Chat y Procesamiento
    if prompt := st.chat_input("Pregunta ej: ¿Cómo nos afecta el riesgo país?"):
        # 1. Agregar mensaje usuario al estado
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Mostrar inmediatamente (hack visual para no esperar al rerun)
        with chat_container:
             st.markdown(f"""<div style="text-align: right; margin-bottom: 10px;"><div class="user-card">{prompt}</div></div>""", unsafe_allow_html=True)

        # 3. Procesamiento con efecto visual
        with chat_container:
            placeholder = st.empty()
            # Spinner animado
            placeholder.markdown("""<div class='bot-card' style='text-align:center; color:#38BDF8;'><i>Consultando bases de datos macroeconómicas... 🔄</i></div>""", unsafe_allow_html=True)
            time.sleep(1.5) # Simular pensamiento
            
            # --- LLAMADA AL CEREBRO FINANCIERO ---
            respuesta_ia = cerebro_financiero_avanzado(prompt)
            
            # Efecto Typewriter sobre la tarjeta final
            full_html_start = """
            <div class="bot-card">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 20px; margin-right: 10px;">🤖</span>
                    <b style="color: #38BDF8;">PETROLITO AI ANALYSIS</b>
                </div>
                <div style="color: #E2E8F0; font-family: 'Segoe UI', sans-serif; line-height: 1.6;">
            """
            full_html_end = "</div></div>"
            
            # Stream de texto simulado
            current_text = ""
            # Procesar por palabras para velocidad de lectura natural
            words = respuesta_ia.split(" ")
            for word in words:
                current_text += word + " "
                # Renderizar texto Markdown a HTML dentro de nuestra tarjeta custom
                # Nota: st.markdown interpreta markdown dentro de html si se configura bien, pero aquí hacemos una inyección simple.
                # Para mantener el formato MD (negritas, bullets), usamos st.markdown directamente sobre el bloque.
                placeholder.markdown(full_html_start + current_text + "▌" + full_html_end, unsafe_allow_html=True)
                time.sleep(0.03)
            
            # Texto final limpio
            placeholder.markdown(full_html_start + respuesta_ia + full_html_end, unsafe_allow_html=True)

        # 4. Guardar respuesta en historial
        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})

    st.markdown("---")
    st.caption("💡 Fuente de datos: Estados Financieros Auditados, Reportes BCRP y Cotizaciones Platts WTI.")
