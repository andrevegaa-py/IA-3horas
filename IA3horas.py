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

# --- ESTADO INTELIGENCIA ARTIFICIAL (MEMORIA) ---
if "contexto_chat" not in st.session_state:
    # Rastrea: Tema actual y Nivel de profundidad (0=Ejecutivo, 1=Analítico, 2=Técnico)
    st.session_state.contexto_chat = {"tema_actual": None, "nivel_profundidad": 0}

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": (
            "Bienvenido al Hub de Inteligencia. Soy Petrolito 3.0.\n\n"
            "He sido actualizado con capacidades de **Análisis Histórico** y **Generación de Gráficos**.\n"
            "Puedo asistirle en:\n"
            "• **Historia** (Evolución y Producción)\n"
            "• **Deuda** (Bonos y Estrategia)\n"
            "• **Talara** (Operaciones y Flexicoking)\n"
            "• **Macro** (Riesgo País y WTI)\n\n"
            "¿Por dónde desea comenzar?"
        )
    }]

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL IMPACT) ---
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
    
    /* 3. TIPOGRAFÍA */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* 4. ELEMENTOS UI */
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

    /* 5. CHAT CARDS */
    .bot-card {
        background-color: rgba(15, 23, 42, 0.9); 
        border: 1px solid #38BDF8; 
        border-left: 5px solid #38BDF8; 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);
    }
    .user-card {
        background-color: rgba(56, 189, 248, 0.2); 
        color: white; 
        padding: 12px 20px; 
        border-radius: 15px 15px 0 15px; 
        margin-bottom: 15px; 
        text-align: right;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* 6. AJUSTES MÉTRICAS */
    img { border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; opacity: 0.9; }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS IMÁGENES ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_USER = "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg"
IMG_SIDEBAR_BANNER = "https://img.freepik.com/free-photo/oil-refinery-twilight_1112-575.jpg"
IMG_CARD_TALARA = "https://portal.andina.pe/EDPfotografia3/Thumbnail/2022/04/12/000862854W.jpg"
IMG_CARD_FINANCE = "https://img.freepik.com/free-photo/standard-quality-control-collage-concept_23-2149595831.jpg"
IMG_CARD_AI = "https://img.freepik.com/free-photo/rpa-concept-with-blurry-hand-touching-screen_23-2149311914.jpg"

# --- 4. CEREBRO FINANCIERO 3.0 (CLASE COMPLETA) ---

class PetrolitoBrain:
    def __init__(self):
        self.USE_LIVE_API = False 
        
        # BASE DE CONOCIMIENTO AMPLIADA (Finanzas + Historia)
        self.knowledge_base = {
            "historia": [
                {
                    "nivel": 0,
                    "titulo": "📜 Historia: Origen y Misión",
                    "texto": "Petroperú fue creada el **24 de julio de 1969** (Ley 17753) tras la expropiación de los activos de la *International Petroleum Company* (IPC) en Talara. Su misión fundacional fue asegurar la soberanía energética del país, integrando verticalmente la exploración, refinación y distribución.",
                    "dato": "Fundación: 1969 (Gob. Velasco) | Activo Base: Talara",
                    "adjunto": "grafico_historia" # Trigger para gráfico
                },
                {
                    "nivel": 1,
                    "titulo": "📜 Historia: La Privatización (Años 90)",
                    "texto": "En los 90, bajo una política de libre mercado, Petroperú fue fragmentada. Se privatizaron activos clave: La Flota Petrolera (Transoceánica), la Planta de Gas (Solgas), grifos propios y refinerías menores (La Pampilla). La empresa perdió su integración vertical y se quedó solo con refinación y transporte (Oleoducto).",
                    "dato": "Pérdida: Grifos y Pozos | Enfoque: Solo Refino"
                },
                {
                    "nivel": 2,
                    "titulo": "📜 Historia: Retorno al Upstream y Ley 30130",
                    "texto": "En 2013 se promulga la **Ley 30130**, que declara de necesidad pública la Modernización de Talara, pero prohíbe inversiones en otros rubros si generan deuda. Recientemente, Petroperú ha retornado al 'Upstream' (Explotación) operando temporalmente los Lotes I, VI y Z-69 en Talara, buscando recuperar la integración vertical.",
                    "dato": "Ley 30130: Candado Financiero | Lotes actuales: I, VI, Z-69"
                }
            ],
            "deuda": [
                {"nivel": 0, "titulo": "📉 Deuda: Visión General", "texto": "La deuda financiera total es de **USD 8.5 Billones**. Dependemos de líneas garantizadas por el MEF. El flujo de caja operativo es insuficiente para el servicio de deuda corto plazo.", "dato": "Deuda: $8.5B", "adjunto": "tabla_deuda"},
                {"nivel": 1, "titulo": "📉 Composición de Pasivos", "texto": "45% Bonos Corporativos y 30% Facilidad CESCE (España). Presión crítica en capital de trabajo (Revolving).", "dato": "Bonos: $3.0B"},
                {"nivel": 2, "titulo": "📉 Covenants y Yield", "texto": "Yield de bonos 2047 supera el 11%. Se negocian 'Waivers' por incumplimiento de ratios de liquidez.", "dato": "Yield: >11%"}
            ],
            "talara": [
                {"nivel": 0, "titulo": "🏭 NRT: Status Operativo", "texto": "Refinería al 100%. Procesa 95k barriles/día. Ya no es proyecto, es activo productivo Euro VI.", "dato": "Capacidad: 95 KBPD"},
                {"nivel": 1, "titulo": "🏭 Márgenes y Flexicoking", "texto": "El margen objetivo es $10-12/bbl gracias a la unidad de Flexicoking que convierte residuales en destilados valiosos.", "dato": "Margen: $10-12"},
                {"nivel": 2, "titulo": "🏭 Tecnología ExxonMobil", "texto": "La licencia de Flexicoking permite procesar crudos pesados generando gas de síntesis para autogeneración eléctrica.", "dato": "Licencia: Exxon"}
            ],
            "macro": [
                {"nivel": 0, "titulo": "🌍 Riesgo y Entorno", "texto": "Entorno volátil. Variables clave: WTI y soporte del Estado. Calificación crediticia en terreno especulativo.", "dato": "Rating: Junk"},
                {"nivel": 1, "titulo": "🌍 Mismatch de Monedas", "texto": "Ingresos en Soles vs Deuda en Dólares. Tipo de cambio >3.80 afecta gravemente la caja.", "dato": "Riesgo FX: Alto"},
                {"nivel": 2, "titulo": "🌍 Gobernanza", "texto": "Exigencia de acreedores: Auditoría externa (PwC) y reestructuración con gestor privado (PMO).", "dato": "Auditor: PwC"}
            ]
        }

    def _generar_grafico_produccion(self):
        """Genera un gráfico histórico de producción para el chat"""
        years = [1980, 1990, 2000, 2010, 2020, 2024]
        prod = [180, 120, 40, 45, 35, 95] # Miles de barriles (aprox)
        fig = go.Figure(data=go.Scatter(x=years, y=prod, mode='lines+markers', line=dict(color='#00C851', width=3)))
        fig.update_layout(title="Producción Histórica (Miles BPD)", template="plotly_dark", height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    def _generar_tabla_deuda(self):
        """Genera dataframe para descarga"""
        return pd.DataFrame({
            "Instrumento": ["Bonos 2032", "Bonos 2047", "CESCE", "Banca Local"],
            "Monto_MM": [1000, 2000, 1300, 500],
            "Tasa": ["4.75%", "5.625%", "Variable", "8.00%"]
        })

    def _detectar_intencion(self, prompt):
        prompt = prompt.lower()
        if any(x in prompt for x in ["historia", "velasco", "1969", "creacion", "pasado", "privatiza", "ipc"]): return "historia"
        if any(x in prompt for x in ["deuda", "bono", "banco", "dinero", "mef"]): return "deuda"
        if any(x in prompt for x in ["talara", "refineria", "nrt", "flexicoking"]): return "talara"
        if any(x in prompt for x in ["macro", "dolar", "wti", "precio"]): return "macro"
        return None

    def procesar_consulta(self, prompt, estado_actual):
        tema = self._detectar_intencion(prompt)
        response_payload = {"texto": "", "adjunto_tipo": None, "adjunto_data": None}

        # Lógica de Profundidad
        nuevo_nivel = 0
        if any(x in prompt for x in ["mas", "más", "detalle", "profundiza"]):
            tema = estado_actual["tema_actual"]
            if tema: nuevo_nivel = min(estado_actual["nivel_profundidad"] + 1, 2)
        elif tema:
            if estado_actual["tema_actual"] == tema:
                nuevo_nivel = min(estado_actual["nivel_profundidad"] + 1, 2)
        else:
            response_payload["texto"] = "No entiendo el contexto. Pruebe: 'Historia de la empresa', 'Situación de Deuda' o 'Refinería Talara'."
            return response_payload

        # Actualizar Estado
        st.session_state.contexto_chat["tema_actual"] = tema
        st.session_state.contexto_chat["nivel_profundidad"] = nuevo_nivel

        # Construir Respuesta
        try:
            data = self.knowledge_base[tema][nuevo_nivel]
            response_payload["texto"] = f"### {data['titulo']}\n\n{data['texto']}\n\n**Dato Clave:** {data['dato']}"
            
            # GESTIÓN DE ADJUNTOS (INTELIGENCIA MULTIMEDIA)
            if "adjunto" in data:
                if data["adjunto"] == "grafico_historia":
                    response_payload["adjunto_tipo"] = "grafico"
                    response_payload["adjunto_data"] = self._generar_grafico_produccion()
                elif data["adjunto"] == "tabla_deuda":
                    response_payload["adjunto_tipo"] = "dataframe"
                    response_payload["adjunto_data"] = self._generar_tabla_deuda()
                    
        except:
            response_payload["texto"] = "Información no disponible para este nivel."

        return response_payload

# Instanciar cerebro
brain = PetrolitoBrain()

# --- 5. FUNCIONES AUXILIARES VISUALES ---
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
# BARRA LATERAL (COMPLETA)
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

    # Menú de Navegación Sidebar
    if st.button("🏠 HOME"): navegar_a('home')
    if st.button("🏭 TALARA"): navegar_a('talara')
    if st.button("⚡ DASHBOARD"): navegar_a('dashboard')
    if st.button("🤖 CHAT AI"): navegar_a('chat')

    st.markdown("### 🛠️ Ajustes")
    moneda = st.selectbox("Moneda", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    unidad = st.selectbox("Escala", ["Millones (MM)", "Miles (k)"])

    csv = get_csv_download()
    st.download_button("📥 Descargar Reporte", data=csv, file_name='reporte_petroperu.csv', mime='text/csv')
    
    st.write("") 
    st.markdown("### 🌍 Sostenibilidad")
    st.image(IMG_SIDEBAR_BANNER, caption="Talara - Feed en Vivo", use_column_width=True)
    st.caption("Monitoreo ambiental activo: ✅ Normal")

# ==================================================
# VISTA 1: HOME
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú AI Hub: Plataforma Estratégica")
    st.markdown("#### Seleccione un módulo de inteligencia:")
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
        st.info("Analista virtual: Historia & Finanzas.")
        if st.button("Consultar ➔", key="b3"): navegar_a('chat')

# ==================================================
# VISTA 2: TALARA
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara")
    col_head, _ = st.columns([1, 5])
    with col_head:
        if st.button("⬅ Volver"): navegar_a('home')
    
    # Métricas Superiores
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
# VISTA 4: CHAT (CON SOPORTE MULTIMEDIA)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Petrolito AI: Análisis & Historia")
    st.markdown("*Capacidad: Finanzas, Operaciones, Macro y Datos Históricos.*")
    
    if st.button("⬅ Volver"): navegar_a('home')

    chat_container = st.container()

    # --- RENDERIZADO DE HISTORIAL ---
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                # Renderizar Tarjeta del Bot
                st.markdown(f"""
                <div class="bot-card">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 20px; margin-right: 10px;">🤖</span>
                        <b style="color: #38BDF8;">PETROLITO AI</b>
                    </div>
                    <div style="color: #E2E8F0; font-family: 'Segoe UI'; font-size: 15px; line-height: 1.6;">
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Renderizar Adjuntos si existen en el historial
                if "adjunto_tipo" in msg:
                    if msg["adjunto_tipo"] == "grafico":
                        st.plotly_chart(msg["adjunto_data"], use_container_width=True)
                    elif msg["adjunto_tipo"] == "dataframe":
                        st.dataframe(msg["adjunto_data"], hide_index=True)

            else:
                # Renderizar Usuario
                st.markdown(f"""<div style="text-align: right;"><div class="user-card">{msg["content"]}</div></div>""", unsafe_allow_html=True)

    # --- INPUT DE USUARIO ---
    if prompt := st.chat_input("Ej: 'Cuéntame la historia de Petroperú' o 'Detalle de la deuda'"):
        # 1. Guardar mensaje usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(f"""<div style="text-align: right;"><div class="user-card">{prompt}</div></div>""", unsafe_allow_html=True)

        # 2. Procesamiento IA
        with chat_container:
            placeholder = st.empty()
            placeholder.markdown(f"<div style='color:#38BDF8; font-style:italic;'>🤖 Consultando base de datos...</div>", unsafe_allow_html=True)
            time.sleep(0.5)
            
            # Obtener respuesta compleja (Texto + Adjuntos)
            respuesta_obj = brain.procesar_consulta(prompt, st.session_state.contexto_chat)
            
            # Limpiar placeholder
            placeholder.empty()

            # 3. Mostrar Respuesta Texto
            st.markdown(f"""
            <div class="bot-card">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 20px; margin-right: 10px;">🤖</span>
                    <b style="color: #38BDF8;">PETROLITO AI</b>
                </div>
                <div style="color: #E2E8F0; font-family: 'Segoe UI'; font-size: 15px; line-height: 1.6;">
                    {respuesta_obj['texto']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 4. Mostrar Adjuntos Multimedia (Si existen)
            if respuesta_obj["adjunto_tipo"] == "grafico":
                st.caption("📊 Visualización Generada:")
                st.plotly_chart(respuesta_obj["adjunto_data"], use_container_width=True)
                
            elif respuesta_obj["adjunto_tipo"] == "dataframe":
                st.caption("📋 Datos Estructurados:")
                st.dataframe(respuesta_obj["adjunto_data"], use_container_width=True)

            # 5. Guardar en Historial (Incluyendo data de adjuntos)
            msg_data = {
                "role": "assistant", 
                "content": respuesta_obj["texto"],
                "adjunto_tipo": respuesta_obj["adjunto_tipo"],
                "adjunto_data": respuesta_obj["adjunto_data"]
            }
            st.session_state.messages.append(msg_data)
