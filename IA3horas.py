import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Petroperú GenAI | Financial Core", 
    layout="wide", 
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# --- 2. GESTIÓN DE NAVEGACIÓN Y ESTADO ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'
if 'moneda' not in st.session_state:
    st.session_state.moneda = "USD ($)"
if 'wti_simulado' not in st.session_state:
    st.session_state.wti_simulado = 76.50
if 'ml_mode' not in st.session_state:
    st.session_state.ml_mode = False  # Estado para activar modo predicción

# --- ESTADO INTELIGENCIA ARTIFICIAL (MEMORIA DE CONTEXTO) ---
if "contexto_chat" not in st.session_state:
    st.session_state.contexto_chat = {"tema_actual": None, "data_relevante": None}

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": (
            "**Sistema GenAI Financiero Iniciado.** Soy el modelo predictivo de Petroperú.\n\n"
            "He integrado módulos de **Machine Learning** para análisis económico:\n"
            "• 📈 **Forecasting:** Proyecciones de Flujo de Caja (Montecarlo).\n"
            "• 🧮 **Riesgo:** Análisis de sensibilidad WTI/EBITDA.\n"
            "• 🏭 **Activos:** Optimización operativa de Talara.\n\n"
            "Puede pedirme: *'Proyecta el flujo de caja para el Q4'*, *'Analiza la deuda'* o *'Simula un escenario de crisis'.*"
        )
    }]

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (TECH / DATA SCIENCE LOOK) ---
estilos_tech = """
<style>
    /* 1. FONDO GENERAL */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(10, 14, 23, 0.95), rgba(10, 14, 23, 0.98)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    /* 2. SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #050A14;
        border-right: 1px solid rgba(124, 58, 237, 0.3); /* Morado AI */
    }
    
    /* 3. TIPOGRAFÍA */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #E2E8F0 !important; font-family: 'Inter', sans-serif; 
    }
    
    /* 4. ELEMENTOS UI */
    .glass-card {
        background-color: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 12px; padding: 20px;
        backdrop-filter: blur(10px); margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%; background-color: #1E293B; color: #A78BFA !important; 
        border: 1px solid #7C3AED; border-radius: 6px; padding: 10px; 
        font-weight: 600; text-transform: uppercase; transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #7C3AED; color: white !important; box-shadow: 0 0 15px rgba(124, 58, 237, 0.6);
    }
    
    /* BOTONES DE DESCARGA */
    .stDownloadButton>button {
        background-color: #10B981 !important; /* Green Emerald */
        color: white !important;
        border: none;
    }

    /* 5. CHAT CARDS - AI STYLE */
    .bot-card {
        background-color: rgba(17, 24, 39, 0.9); 
        border: 1px solid #7C3AED; 
        border-left: 5px solid #7C3AED; 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.15);
    }
    .user-card {
        background-color: rgba(56, 189, 248, 0.15); 
        color: white; 
        padding: 12px 20px; 
        border-radius: 15px 15px 0 15px; 
        margin-bottom: 15px; 
        text-align: right;
        display: inline-block;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* 6. METRICAS */
    [data-testid="stMetricValue"] { color: #A78BFA !important; text-shadow: 0 0 10px rgba(124, 58, 237, 0.4); }
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

# --- 4. MOTOR DE IA GENERATIVA & MACHINE LEARNING (CORE) ---

class PetroGenAI:
    def __init__(self):
        # Base de Conocimiento Estructurada (RAG Context)
        self.vector_db = {
            "historia": {
                "tags": ["origen", "1969", "velasco", "ipc"],
                "content": "Petroperú fue fundada en 1969 (Gobierno de Velasco) tras la expropiación de la IPC. Su misión histórica es la seguridad energética. En los 90s sufrió fragmentación (venta de grifos, naviera, solgas), lo que redujo su margen integrado.",
                "ml_insight": "Correlación histórica: La fragmentación de activos en los 90 redujo el margen EBITDA en un 40% promedio durante la década siguiente."
            },
            "deuda": {
                "tags": ["bonos", "mef", "banco", "liquidez", "prestamo"],
                "content": "La deuda financiera asciende a $8.5 Billones. Estructura crítica: $3B en Bonos Soberanos (vencimientos 2032/2047) y $1.3B crédito sindicado CESCE. Se requiere soporte del MEF para capital de trabajo.",
                "ml_insight": "Análisis de Riesgo: El 'Spread' de los bonos Petroperú vs Tesoro Americano es >1100 pbs, indicando percepción de riesgo de impago (Default) sin garantía soberana."
            },
            "talara": {
                "tags": ["refineria", "nrt", "flexicoking", "operacion"],
                "content": "La NRT opera a 95 KBPD. La unidad crítica es el Flexicoking (conversión profunda). La rentabilidad depende del Crack Spread (diferencial crudo vs diésel).",
                "ml_insight": "Optimización: Modelos predictivos sugieren que con WTI > $80, el margen de refino debe superar los $12/bbl para cubrir servicio de deuda."
            }
        }

    # --- SIMULACIÓN ML: MONTECARLO ---
    def generar_proyeccion_ml(self, n_simulaciones=1000):
        """Simula proyecciones de EBITDA usando método Montecarlo"""
        np.random.seed(42)
        meses = np.array(range(1, 13))
        
        # Tendencia base + Ruido estocástico (Volatilidad del mercado)
        proyecciones = []
        for _ in range(n_simulaciones):
            volatilidad = np.random.normal(0, 15, 12) # Volatilidad de precios
            tendencia = np.linspace(100, 180, 12)     # Tendencia de recuperación
            proyeccion = tendencia + volatilidad
            proyecciones.append(proyeccion)
        
        datos = np.array(proyecciones)
        p10 = np.percentile(datos, 10, axis=0) # Escenario Pesimista
        p50 = np.percentile(datos, 50, axis=0) # Escenario Base
        p90 = np.percentile(datos, 90, axis=0) # Escenario Optimista
        
        return meses, p10, p50, p90

    # --- PROCESAMIENTO NLP SIMULADO ---
    def procesar_prompt(self, prompt):
        prompt = prompt.lower()
        response_payload = {"texto": "", "adjunto_tipo": None, "adjunto_data": None}
        
        # 1. INTENCIÓN: PREODICCIÓN / FORECAST (ML Trigger)
        if any(x in prompt for x in ["proyecta", "futuro", "prediccion", "simula", "forecast", "2025"]):
            meses, p10, p50, p90 = self.generar_proyeccion_ml()
            
            # Crear gráfico de abanico (Fan Chart)
            fig = go.Figure()
            # P90
            fig.add_trace(go.Scatter(x=list(range(1,13)), y=p90, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
            # P10 con relleno (Intervalo de Confianza)
            fig.add_trace(go.Scatter(x=list(range(1,13)), y=p10, mode='lines', fill='tonexty', 
                                     fillcolor='rgba(124, 58, 237, 0.2)', line=dict(width=0), 
                                     name='Intervalo Confianza (80%)'))
            # P50 (Línea central)
            fig.add_trace(go.Scatter(x=list(range(1,13)), y=p50, mode='lines', 
                                     line=dict(color='#00C851', width=3), name='Proyección Base (ML)'))
            
            fig.update_layout(title="Proyección Estocástica de EBITDA (Montecarlo)", template="plotly_dark", 
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Meses Futuros")
            
            response_payload["texto"] = (
                "🤖 **Ejecutando Modelo Predictivo...**\n\n"
                "He realizado 1,000 iteraciones de Montecarlo basadas en la volatilidad actual del WTI.\n"
                "• **Escenario Base (P50):** Recuperación sostenida del EBITDA operativa.\n"
                "• **Riesgo (P10):** Existe un 10% de probabilidad de flujo negativo en el Q3 si el WTI cae bajo $65.\n"
                "• **Oportunidad (P90):** Potencial de mejora significativa si la NRT mantiene carga plena."
            )
            response_payload["adjunto_tipo"] = "grafico"
            response_payload["adjunto_data"] = fig
            return response_payload

        # 2. INTENCIÓN: RETRIEVAL (RAG Trigger)
        found_key = None
        for key, data in self.vector_db.items():
            if any(tag in prompt for tag in data["tags"]):
                found_key = key
                break
        
        if found_key:
            info = self.vector_db[found_key]
            response_payload["texto"] = (
                f"### 💡 Análisis Generativo: {found_key.capitalize()}\n\n"
                f"{info['content']}\n\n"
                f"🧠 **Insight del Modelo:**\n{info['ml_insight']}"
            )
            # Agregar datos específicos si aplica
            if found_key == "deuda":
                 response_payload["adjunto_tipo"] = "dataframe"
                 response_payload["adjunto_data"] = generar_perfil_deuda()
            return response_payload

        # 3. FALLBACK GENERATIVO
        response_payload["texto"] = (
            "📉 **Fuera de Distribución.**\n\n"
            "Mi modelo no tiene confianza suficiente para responder esa consulta específica con los datos actuales.\n"
            "Puedo ayudarte analizando:\n"
            "1. **Predicciones:** 'Simula el flujo de caja 2025'.\n"
            "2. **Datos Estructurales:** 'Estructura de deuda actual'.\n"
            "3. **Operaciones:** 'Eficiencia de Talara'."
        )
        return response_payload

gen_ai = PetroGenAI()

# --- 5. FUNCIONES DE DATOS & VISUALIZACIÓN ---

def get_dashboard_data_ml(wti_price, use_prediction=False):
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    
    # Modelo Matemático Simplificado
    sensibilidad_wti = (wti_price - 70) * 2.5 # Impacto por cada dólar sobre 70
    
    base_ebitda = [80, 90, 85, 95, 100, 110]
    ebitda_real = [x + sensibilidad_wti for x in base_ebitda]
    
    if use_prediction:
        # Generar datos futuros (Jul-Dic)
        meses_futuros = ['Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        meses = meses + meses_futuros
        
        # Proyección lineal simple con ruido random (Simulación ML)
        tendencia = np.linspace(ebitda_real[-1], ebitda_real[-1]*1.2, 6)
        ruido = np.random.normal(0, 5, 6)
        ebitda_pred = list(tendencia + ruido)
        
        ebitda_total = ebitda_real + ebitda_pred
        tipo_dato = ['Real']*6 + ['Predicción']*6
        
        return pd.DataFrame({'Mes': meses, 'EBITDA': ebitda_total, 'Tipo': tipo_dato})
    else:
        return pd.DataFrame({'Mes': meses, 'EBITDA': ebitda_real, 'Tipo': ['Real']*6})

def generar_mapa_activos_inteligente():
    # Mapa con capas de datos geoespaciales
    data_points = [
        {"name": "Refinería Talara", "lat": -4.5772, "lon": -81.2719, "status": "Operativo", "color": [0, 255, 127, 180], "risk": 0.1},
        {"name": "ONP Estación 1", "lat": -4.9, "lon": -80.5, "status": "Mantenimiento", "color": [255, 165, 0, 180], "risk": 0.4},
        {"name": "ONP Estación 5", "lat": -5.5, "lon": -78.5, "status": "Alerta", "color": [255, 68, 68, 180], "risk": 0.8},
        {"name": "Terminal Callao", "lat": -12.05, "lon": -77.15, "status": "Operativo", "color": [0, 255, 127, 180], "risk": 0.2}
    ]
    df_map = pd.DataFrame(data_points)
    
    # Capa de puntos con radio variable según riesgo (Feature Engineering visual)
    layer = pdk.Layer(
        "ScatterplotLayer",
        df_map,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="risk * 50000 + 10000", # Radio dinámico basado en riesgo
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_min_pixels=5,
        radius_max_pixels=50,
    )
    
    # Capa de Arco (Flujo Logístico)
    arc_data = [{"source": [-81.27, -4.57], "target": [-77.15, -12.05], "value": 100}]
    layer_arc = pdk.Layer(
        "ArcLayer",
        arc_data,
        get_source_position="source",
        get_target_position="target",
        get_width=3,
        get_tilt=15,
        get_source_color=[0, 255, 127],
        get_target_color=[0, 200, 255],
    )

    view_state = pdk.ViewState(latitude=-9.0, longitude=-75.0, zoom=4.5, pitch=50)
    
    return pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[layer, layer_arc],
        tooltip={"text": "{name}\nEstado: {status}"}
    )

# Funciones auxiliares conservadas
def generar_perfil_deuda():
    return pd.DataFrame({
        'Acreedor': ['Bonos 2032', 'Bonos 2047', 'CESCE', 'Banca Local'],
        'Monto_MM': [1000, 2000, 1300, 500],
        'Tasa': ['4.75%', '5.63%', 'Variable', '8.50%']
    })

def layout_ml(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family="Inter"),
        xaxis=dict(gridcolor='rgba(124, 58, 237, 0.1)', color='#A78BFA'),
        yaxis=dict(gridcolor='rgba(124, 58, 237, 0.1)', color='#A78BFA'),
        legend=dict(font=dict(color='#E2E8F0')),
        hovermode="x unified"
    )
    return fig

# ==================================================
# SIDEBAR: PANEL DE CONTROL DE IA
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: #0F172A; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #7C3AED; margin-bottom: 20px;'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)

    st.markdown("### 🧠 Neural Core")
    c_prof1, c_prof2 = st.columns([1, 3])
    with c_prof1:
        st.markdown(f"<div style='position:relative;'><img src='{IMG_USER}' style='width: 50px; height: 50px; border-radius: 50%; border: 2px solid #7C3AED;'></div>", unsafe_allow_html=True)
    with c_prof2:
        st.markdown("""
        <div style='padding-left: 5px;'>
            <div style='color: white; font-weight: bold; font-size: 14px;'>Finanzas ML</div>
            <div style='color: #10B981; font-size: 11px; font-weight: bold;'>● Model Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    if st.button("🏠 HOME"): navegar_a('home')
    if st.button("🏭 TALARA OPS"): navegar_a('talara')
    if st.button("🔮 PREDICCIONES"): navegar_a('dashboard')
    if st.button("📂 DATA ROOM"): navegar_a('reportes')
    if st.button("🤖 GEN-AI CHAT"): navegar_a('chat')

    st.markdown("### ⚙️ Parámetros del Modelo")
    moneda = st.selectbox("Divisa Base", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    
    st.write("") 
    st.info("Algoritmo de optimización actualizado: v5.2.1")

# ==================================================
# VISTA 1: HOME (COMMAND CENTER)
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🧠 Petroperú AI Hub: Inteligencia Financiera")
    st.markdown("#### Plataforma de análisis predictivo y generativo.")
    st.write("") 

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image(IMG_CARD_TALARA, use_column_width=True)
        st.markdown("### 🏭 Ops & Activos")
        st.caption("Machine Learning aplicado a mantenimiento y costos.")
        if st.button("Analizar ➔", key="b1"): navegar_a('talara')

    with c2:
        st.image(IMG_CARD_FINANCE, use_column_width=True)
        st.markdown("### 🔮 Forecasting")
        st.caption("Modelos estocásticos de Flujo de Caja y EBITDA.")
        if st.button("Predecir ➔", key="b2"): navegar_a('dashboard')

    with c3:
        st.image(IMG_CARD_AI, use_column_width=True)
        st.markdown("### 🤖 GenAI Analyst")
        st.caption("Consultas en lenguaje natural sobre data financiera.")
        if st.button("Conversar ➔", key="b3"): navegar_a('chat')
    
    st.markdown("---")
    st.subheader("🌐 Visión Geo-Analítica en Tiempo Real")
    st.pydeck_chart(generar_mapa_activos_inteligente())

# ==================================================
# VISTA 2: TALARA (ANALYTICS)
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Talara: Deep Analytics")
    if st.button("⬅ Regresar al Hub"): navegar_a('home')
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### 📊 Desviación de Costos (Análisis de Varianza)")
        # Grafico Waterfall de Machine Learning
        fig_w = go.Figure(go.Waterfall(
            name = "Costo", orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "total"],
            x = ["Presupuesto Base", "Inflación", "Retrasos (Covid)", "Intereses", "Actual"],
            y = [1300, 500, 1200, 3500, 0],
            connector = {"line":{"color":"white"}},
            decreasing = {"marker":{"color":"#10B981"}},
            increasing = {"marker":{"color":"#EF4444"}},
            totals = {"marker":{"color":"#3B82F6"}}
        ))
        fig_w = layout_ml(fig_w)
        fig_w.update_layout(title="Drivers de Costo (Modelo de Atribución)")
        st.plotly_chart(fig_w, use_container_width=True)
        
    with col2:
        st.markdown("#### ⚡ KPIs Operativos")
        st.metric("Capacidad Utilizada", "96.5%", "+1.2%")
        st.metric("Margen Refino (USD)", "$11.4", "-0.3")
        st.metric("Disponibilidad Planta", "98.2%", "Óptimo")
        
        st.markdown("""
        <div class='glass-card'>
        <b>💡 Insight IA:</b>
        <small>El modelo detecta una correlación del 85% entre paradas no programadas en la Unidad de Flexicoking y caídas en el margen mensual.</small>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# VISTA 3: DASHBOARD PREDICTIVO (CORE ML)
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    st.title("🔮 Financial Forecasting & ML")
    
    # --- CONTROLES DE SIMULACIÓN ---
    c_ctrl, c_viz = st.columns([1, 3])
    
    with c_ctrl:
        st.markdown("<div class='bot-card'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Hiperparámetros")
        
        wti_val = st.slider("Precio WTI ($/bbl)", 40.0, 120.0, st.session_state.wti_simulado)
        st.session_state.wti_simulado = wti_val
        
        st.write("---")
        # SWITCH PARA ACTIVAR PREDICCIÓN
        modo_prediccion = st.toggle("Activar Forecasting (AI)", value=st.session_state.ml_mode)
        st.session_state.ml_mode = modo_prediccion
        
        if modo_prediccion:
            st.success("✨ Motor Predictivo: ON")
            st.caption("Algoritmo: Regresión con Ruido Gaussiano")
        else:
            st.warning("📊 Modo Histórico")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("⬅ Volver"): navegar_a('home')

    with c_viz:
        # Obtener Data
        df_ml = get_dashboard_data_ml(wti_val, use_prediction=modo_prediccion)
        
        # Métricas Dinámicas
        ebitda_total = df_ml['EBITDA'].sum()
        delta_vs_plan = ((ebitda_total - 600) / 600) * 100
        
        m1, m2, m3 = st.columns(3)
        m1.metric("EBITDA Proyectado", f"${ebitda_total:.1f} M", f"{delta_vs_plan:.1f}%")
        m2.metric("Sensibilidad WTI", "Alta", f"Corr: 0.92")
        m3.metric("Confianza Modelo", "89%", "R² Score")
        
        # Visualización
        st.markdown("#### 📈 Proyección de EBITDA (Escenarios Dinámicos)")
        
        if modo_prediccion:
            # Gráfico Avanzado ML
            fig = px.area(df_ml, x='Mes', y='EBITDA', color='Tipo', 
                          color_discrete_map={'Real': '#10B981', 'Predicción': '#7C3AED'})
            # Añadir línea de tendencia
            fig.add_scatter(x=df_ml['Mes'], y=df_ml['EBITDA'], mode='lines+markers', 
                            line=dict(color='white', width=1), name='Tendencia')
        else:
            # Gráfico Standard
            fig = px.bar(df_ml, x='Mes', y='EBITDA', color_discrete_sequence=['#3B82F6'])
            
        fig = layout_ml(fig)
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# VISTA 4: REPORTES (DATA ROOM)
# ==================================================
elif st.session_state.pagina_actual == 'reportes':
    st.title("📂 Data Room Inteligente")
    if st.button("⬅ Volver"): navegar_a('home')
    
    st.info("ℹ️ Los documentos han sido procesados por el motor OCR y están listos para análisis.")

    # Reutilizamos las funciones de generación de datos
    df_deuda = generar_perfil_deuda()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏦 Estructura de Capital")
        st.dataframe(df_deuda, use_container_width=True)
        st.caption("Probabilidad de Refinanciamiento: **Media (65%)** según condiciones de mercado.")
    
    with c2:
        st.markdown("### 📥 Exportar Dataset Procesado")
        csv = df_deuda.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar CSV (ML Ready)", csv, "data_ml_petroperu.csv", "text/csv")

# ==================================================
# VISTA 5: CHAT GEN-AI (SISTEMA RAG SIMULADO)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 GenAI Analyst Assistant")
    st.markdown("Modelo entrenado en finanzas corporativas, riesgo y operaciones.")
    if st.button("⬅ Cerrar Sesión"): navegar_a('home')

    chat_container = st.container()

    # Historial
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                # Bot UI Style
                st.markdown(f"""
                <div class="bot-card">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 20px; margin-right: 10px;">🧠</span>
                        <b style="color: #A78BFA;">PETRO-GENAI</b>
                    </div>
                    <div style="color: #E2E8F0; font-size: 15px; line-height: 1.6;">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
                
                # Adjuntos
                if "adjunto_tipo" in msg:
                    if msg["adjunto_tipo"] == "grafico":
                        st.plotly_chart(msg["adjunto_data"], use_container_width=True)
                    elif msg["adjunto_tipo"] == "dataframe":
                        st.dataframe(msg["adjunto_data"], hide_index=True)
            else:
                # User UI Style
                st.markdown(f"""<div style="text-align: right;"><div class="user-card">{msg["content"]}</div></div>""", unsafe_allow_html=True)

    # Input
    if prompt := st.chat_input("Pregunta al modelo (ej: 'Proyecta el EBITDA' o 'Riesgo de bonos')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(f"""<div style="text-align: right;"><div class="user-card">{prompt}</div></div>""", unsafe_allow_html=True)

        # Procesamiento
        with chat_container:
            placeholder = st.empty()
            placeholder.markdown("<span style='color:#7C3AED'>⚙️ Generando inferencia probabilística...</span>", unsafe_allow_html=True)
            time.sleep(1.2) # Latencia simulada
            
            respuesta = gen_ai.procesar_prompt(prompt)
            placeholder.empty()
            
            # Streaming effect fake
            msg_placeholder = st.empty()
            texto = ""
            for char in respuesta["texto"].split(" "):
                texto += char + " "
                msg_placeholder.markdown(f"""
                <div class="bot-card">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 20px; margin-right: 10px;">🧠</span>
                        <b style="color: #A78BFA;">PETRO-GENAI</b>
                    </div>
                    <div style="color: #E2E8F0;">{texto}▌</div>
                </div>""", unsafe_allow_html=True)
                time.sleep(0.04)
            
            # Final Render
            msg_placeholder.markdown(f"""
                <div class="bot-card">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 20px; margin-right: 10px;">🧠</span>
                        <b style="color: #A78BFA;">PETRO-GENAI</b>
                    </div>
                    <div style="color: #E2E8F0;">{respuesta["texto"]}</div>
                </div>""", unsafe_allow_html=True)

            if respuesta["adjunto_tipo"] == "grafico":
                st.plotly_chart(respuesta["adjunto_data"], use_container_width=True)
            elif respuesta["adjunto_tipo"] == "dataframe":
                st.dataframe(respuesta["adjunto_data"], use_container_width=True)

            # Guardar memoria
            st.session_state.messages.append({
                "role": "assistant", 
                "content": respuesta["texto"],
                "adjunto_tipo": respuesta["adjunto_tipo"],
                "adjunto_data": respuesta["adjunto_data"]
            })
