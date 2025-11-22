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
    # Rastrea: Tema actual y Nivel de profundidad
    st.session_state.contexto_chat = {"tema_actual": None, "nivel_profundidad": 0}

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": (
            "Bienvenido al Hub de Inteligencia. Soy Petrolito 4.0.\n\n"
            "Estoy configurado con protocolos de **Rigor Financiero**. Puedo analizar data histórica, proyecciones de deuda y operaciones técnicas.\n"
            "• **Historia** (Evolución y Producción)\n"
            "• **Deuda** (Bonos y Estrategia)\n"
            "• **Talara** (Operaciones y Flexicoking)\n"
            "• **Macro** (Riesgo País y WTI)\n\n"
            "¿Cuál es su consulta estratégica?"
        )
    }]

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL IMPACT - MODO DARK PRO) ---
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
    
    /* BOTONES DE DESCARGA (NUEVO) */
    .stDownloadButton>button {
        background-color: #00C851 !important;
        color: white !important;
        border: none;
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

# --- 4. CEREBRO FINANCIERO 4.0 (MODO CONSULTOR + MULTIMEDIA) ---

class PetrolitoBrain:
    def __init__(self):
        self.USE_LIVE_API = False 
        
        # BASE DE CONOCIMIENTO COMPLETA
        self.knowledge_base = {
            "historia": [
                {"nivel": 0, "titulo": "📜 Historia: Origen y Misión", "texto": "Petroperú nació el **24 de julio de 1969** tras la nacionalización de la *International Petroleum Company* en Talara. Su mandato original fue garantizar la seguridad energética nacional, controlando toda la cadena.", "dato": "Origen: 1969 (Velasco) | Activo: Talara", "adjunto": "grafico_historia"},
                {"nivel": 1, "titulo": "📜 Historia: La Fragmentación (Años 90)", "texto": "En los 90 se privatizaron unidades rentables: la flota naviera, la planta de gas (Solgas) y refinerías satélites. La empresa perdió integración vertical, quedándose principalmente con el refino.", "dato": "Privatizado: Solgas, Naviera, Grifos"},
                {"nivel": 2, "titulo": "📜 Historia: Ley 30130 y Retorno", "texto": "La Ley 30130 (2013) blindó la construcción de la Nueva Refinería Talara pero restringió nuevas inversiones. Hoy, la estrategia es volver al *Upstream* (Lotes I, VI, Z-69) para producir crudo propio.", "dato": "Hito: Retorno al Upstream (Lotes I, VI)"}
            ],
            "deuda": [
                {"nivel": 0, "titulo": "📉 Deuda: Situación Crítica", "texto": "La deuda total es de **USD 8.5 Billones**. La estructura de capital es insostenible sin apoyo estatal. Actualmente, el MEF otorga garantías para evitar el impago de combustibles.", "dato": "Pasivo Total: $8.5B", "adjunto": "tabla_deuda"},
                {"nivel": 1, "titulo": "📉 Estructura de Pasivos", "texto": "El problema no es solo el monto, sino el plazo. Tenemos **$3,000 MM** en Bonos a largo plazo y **$1,300 MM** del crédito sindicado CESCE. Lo urgente es la deuda de corto plazo.", "dato": "Bonos: $3.0B | CESCE: $1.3B"},
                {"nivel": 2, "titulo": "📉 Riesgo de Liquidez y Yield", "texto": "Los bonos de Petroperú cotizan con un rendimiento (Yield) superior al 11%, reflejando alto riesgo de impago. Estamos en constante negociación ('Waivers') con la banca.", "dato": "Yield Mercado: >11%"}
            ],
            "talara": [
                {"nivel": 0, "titulo": "🏭 NRT: Operación Plena", "texto": "La Nueva Refinería Talara opera al 100% de capacidad (**95 KBPD**). Produce diésel y gasolinas Euro VI (menos de 50 ppm de azufre), cumpliendo la normativa ambiental.", "dato": "Capacidad: 95,000 BPD"},
                {"nivel": 1, "titulo": "🏭 Margen de Refino", "texto": "La rentabilidad depende del diferencial de precios (Crack Spread). Con la tecnología actual, buscamos un margen de **$10 a $12 por barril**, superior a los $4 de la refinería antigua.", "dato": "Target Margen: $10-12/bbl"},
                {"nivel": 2, "titulo": "🏭 Flexicoking: El Corazón Técnico", "texto": "La unidad de **Flexicoking** (licencia ExxonMobil) es la joya técnica. Convierte lo más barato (residuo de vacío) en productos caros y genera gas para autogeneración.", "dato": "Tecnología: Conversión Profunda"}
            ],
            "macro": [
                {"nivel": 0, "titulo": "🌍 Entorno: Volatilidad", "texto": "El negocio está expuesto al precio internacional del petróleo (WTI) y a la inestabilidad política. Las agencias de rating (S&P, Fitch) nos califican como bono basura ('Junk').", "dato": "Rating: CCC+ / BB+"},
                {"nivel": 1, "titulo": "🌍 Tipo de Cambio y Caja", "texto": "Existe un descalce estructural: Compramos crudo en Dólares y vendemos en Soles. Cuando el dólar sube (>3.80), necesitamos más soles para pagar la misma deuda.", "dato": "Riesgo FX: Crítico"},
                {"nivel": 2, "titulo": "🌍 Gobernanza Corporativa", "texto": "La reestructuración exige una auditoría externa (PwC) y la contratación de un gestor privado (PMO) para despolitizar la gestión, requisito clave de acreedores.", "dato": "Auditoría: PwC | Gestión: PMO"}
            ]
        }

    def _generar_grafico_produccion(self):
        years = [1980, 1990, 2000, 2010, 2020, 2024]
        prod = [180, 120, 40, 45, 35, 95]
        fig = go.Figure(data=go.Scatter(x=years, y=prod, mode='lines+markers', line=dict(color='#00C851', width=3)))
        fig.update_layout(title="Producción Histórica (Miles BPD)", template="plotly_dark", height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    def _generar_tabla_deuda(self):
        return pd.DataFrame({
            "Instrumento": ["Bonos 2032", "Bonos 2047", "CESCE (España)", "Banca Local"],
            "Monto_MM": [1000, 2000, 1300, 500],
            "Tasa": ["4.75%", "5.625%", "Variable+2%", "8.50%"]
        })

    def _detectar_intencion(self, prompt):
        prompt = prompt.lower()
        if any(x in prompt for x in ["historia", "velasco", "1969", "creacion", "pasado", "antigua", "ipc"]): return "historia"
        if any(x in prompt for x in ["deuda", "bono", "banco", "dinero", "mef", "prestamo", "caja", "liquidez"]): return "deuda"
        if any(x in prompt for x in ["talara", "refineria", "nrt", "flexicoking", "produccion", "operacion", "diesel"]): return "talara"
        if any(x in prompt for x in ["macro", "dolar", "wti", "precio", "riesgo", "mercado", "gobierno"]): return "macro"
        return None

    def procesar_consulta(self, prompt, estado_actual):
        tema = self._detectar_intencion(prompt)
        response_payload = {"texto": "", "adjunto_tipo": None, "adjunto_data": None}
        
        # Lógica de Continuidad
        continuidad = any(x in prompt for x in ["mas", "más", "detalle", "profundiza", "sigue", "continuar"])
        
        nuevo_nivel = 0
        tema_a_usar = None

        if continuidad and estado_actual["tema_actual"]:
            tema_a_usar = estado_actual["tema_actual"]
            nuevo_nivel = min(estado_actual["nivel_profundidad"] + 1, 2)
        elif tema:
            tema_a_usar = tema
            if estado_actual["tema_actual"] == tema:
                nuevo_nivel = min(estado_actual["nivel_profundidad"] + 1, 2)
            else:
                nuevo_nivel = 0

        # Lógica de Respuesta
        if tema_a_usar:
            # Actualizar memoria
            st.session_state.contexto_chat["tema_actual"] = tema_a_usar
            st.session_state.contexto_chat["nivel_profundidad"] = nuevo_nivel
            
            try:
                data = self.knowledge_base[tema_a_usar][nuevo_nivel]
                response_payload["texto"] = f"### {data['titulo']}\n\n{data['texto']}\n\n**Dato Clave:** {data['dato']}"
                if "adjunto" in data:
                    if data["adjunto"] == "grafico_historia":
                        response_payload["adjunto_tipo"] = "grafico"
                        response_payload["adjunto_data"] = self._generar_grafico_produccion()
                    elif data["adjunto"] == "tabla_deuda":
                        response_payload["adjunto_tipo"] = "dataframe"
                        response_payload["adjunto_data"] = self._generar_tabla_deuda()
            except:
                response_payload["texto"] = "⚠️ Error de acceso a datos internos. Por favor reinicie la consulta."
        
        else:
            # --- FALLBACK AVANZADO: RAZONAMIENTO & GUÍA (CONSULTOR DIRECTIVO) ---
            response_payload["texto"] = (
                f"🔎 **Análisis de Consulta:** He procesado su entrada *'{prompt}'*.\n\n"
                "Aunque detecto su intención de consulta, mis protocolos de **Rigor Financiero** me impiden "
                "especular sobre temas que no han sido auditados o que salen de mi base vectorial autorizada.\n\n"
                "**Como Asistente Estratégico, le sugiero redirigir el análisis a estos ejes críticos:**\n\n"
                "1.  💵 **Salud Financiera:** Pregunte por *'Deuda'*, *'Bonos'* o *'Liquidez'*.\n"
                "2.  🏭 **Operaciones:** Consulte sobre *'Talara'*, *'Producción'* o *'Flexicoking'*.\n"
                "3.  📜 **Contexto:** Explore la *'Historia'* de la empresa o el *'Riesgo País'*.\n\n"
                "👉 *Por favor, seleccione uno de estos vectores para desplegar la información oficial.*"
            )
            
        return response_payload

brain = PetrolitoBrain()

# --- 5. FUNCIONES DE DATOS (VISUALES & REPORTES) ---
# A. GENERADORES DE DASHBOARD Y TALARA
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

# B. GENERADORES DE REPORTES REALES (DATA ROOM)
def generar_eeff():
    df = pd.DataFrame({
        'Concepto': ['Ingresos por Ventas', 'Costo de Ventas', 'UTILIDAD BRUTA', 
                     'Gastos de Ventas', 'Gastos de Administración', 'Otros Ingresos/Gastos',
                     'EBITDA', 'Depreciación y Amortización', 'EBIT', 
                     'Gastos Financieros (Intereses)', 'Diferencia de Cambio', 'UTILIDAD NETA'],
        '2023 (Auditado MM USD)': [4500.0, -4100.0, 400.0, -150.0, -120.0, 50.0, 
                                   180.0, -300.0, -120.0, -450.0, -100.0, -670.0],
        '2024 (Preliminar MM USD)': [5200.0, -4400.0, 800.0, -160.0, -110.0, 40.0, 
                                     570.0, -320.0, 250.0, -480.0, -50.0, -280.0]
    })
    return df

def generar_flujo_caja():
    df = pd.DataFrame({
        'Rubro': ['SALDO INICIAL CAJA', '(+) Cobranzas Mercado Local', '(+) Exportaciones', 
                  '(-) Pago Proveedores Crudo', '(-) Servicio de Deuda', '(-) Planilla y Operaciones', 'SALDO FINAL CAJA'],
        'Semana 1 (Proy)': [50.0, 85.0, 20.0, -90.0, -10.0, -15.0, 40.0],
        'Semana 2 (Proy)': [40.0, 90.0, 15.0, -80.0, -25.0, -15.0, 25.0],
        'Semana 3 (Proy)': [25.0, 80.0, 30.0, -70.0, -10.0, -15.0, 40.0],
        'Semana 4 (Proy)': [40.0, 95.0, 10.0, -100.0, -5.0, -15.0, 25.0]
    })
    return df

def generar_perfil_deuda():
    df = pd.DataFrame({
        'Acreedor': ['Bonistas Int. 2032', 'Bonistas Int. 2047', 'CESCE (Sindicado)', 'Banco de la Nación', 'Facilidades Corto Plazo'],
        'Monto (MM USD)': [1000, 2000, 1300, 800, 2400],
        'Tasa Interés': ['4.750%', '5.625%', 'Libor + 2.5%', 'Tasa Preferencial', '8.50%'],
        'Vencimiento': ['2032', '2047', '2030', 'Revolving', '2024-2025'],
        'Estado': ['Vigente', 'Vigente', 'Periodo de Gracia', 'Vigente', 'Renovación Constante']
    })
    return df

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

    # Menú de Navegación Sidebar (CON REPORTES)
    if st.button("🏠 HOME"): navegar_a('home')
    if st.button("🏭 TALARA"): navegar_a('talara')
    if st.button("⚡ DASHBOARD"): navegar_a('dashboard')
    if st.button("📂 REPORTES"): navegar_a('reportes') # NUEVO
    if st.button("🤖 CHAT AI"): navegar_a('chat')

    st.markdown("### 🛠️ Ajustes")
    moneda = st.selectbox("Moneda", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    
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
# VISTA 4: REPORTES (DATA ROOM FINANCIERO)
# ==================================================
elif st.session_state.pagina_actual == 'reportes':
    st.title("📂 Data Room Financiero: Archivos Oficiales")
    st.markdown("Repositorio seguro de Estados Financieros, Flujos de Caja y Estructura de Deuda.")
    if st.button("⬅ Volver"): navegar_a('home')
    
    st.warning("⚠️ **CONFIDENCIAL:** La información contenida en estos archivos es para uso exclusivo de la Gerencia Financiera y Directorio.")

    # Generar DataFrames
    df_eeff = generar_eeff()
    df_cash = generar_flujo_caja()
    df_deuda = generar_perfil_deuda()

    col_rep1, col_rep2, col_rep3 = st.columns(3)

    # --- TARJETA 1: EEFF ---
    with col_rep1:
        st.markdown("""
        <div class="bot-card" style="height: 250px; text-align: center;">
            <h2 style="color: #00C851 !important;">📊</h2>
            <h4>Estados Financieros</h4>
            <p style="font-size: 13px;">Consolidado Auditado 2023 vs Preliminar 2024. Incluye EBITDA y Utilidad Neta.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Vista Previa:**")
        st.dataframe(df_eeff.head(3), hide_index=True, use_container_width=True)
        
        csv_eeff = df_eeff.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar EEFF_Consolidado.csv",
            data=csv_eeff,
            file_name="Petroperu_EEFF_Consolidado_2024.csv",
            mime="text/csv"
        )

    # --- TARJETA 2: CASH FLOW ---
    with col_rep2:
        st.markdown("""
        <div class="bot-card" style="height: 250px; text-align: center;">
            <h2 style="color: #33b5e5 !important;">💵</h2>
            <h4>Flujo de Caja (Weekly)</h4>
            <p style="font-size: 13px;">Proyección de Tesorería a 4 semanas. Detalle de cobranzas y servicio de deuda.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Vista Previa:**")
        st.dataframe(df_cash.head(3), hide_index=True, use_container_width=True)

        csv_cash = df_cash.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CashFlow_Proyectado.csv",
            data=csv_cash,
            file_name="Petroperu_FlujoCaja_Semanal.csv",
            mime="text/csv"
        )

    # --- TARJETA 3: DEUDA ---
    with col_rep3:
        st.markdown("""
        <div class="bot-card" style="height: 250px; text-align: center;">
            <h2 style="color: #ff4444 !important;">📉</h2>
            <h4>Perfil de Deuda</h4>
            <p style="font-size: 13px;">Desglose de acreedores (Bonistas, CESCE, Banca), tasas y vencimientos.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Vista Previa:**")
        st.dataframe(df_deuda.head(3), hide_index=True, use_container_width=True)

        csv_deuda = df_deuda.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Estructura_Deuda.csv",
            data=csv_deuda,
            file_name="Petroperu_Perfil_Deuda_2024.csv",
            mime="text/csv"
        )

# ==================================================
# VISTA 5: CHAT (CON SOPORTE MULTIMEDIA & FALLBACK)
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
