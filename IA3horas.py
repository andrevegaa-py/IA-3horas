import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import time

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO (MODO "APP NATIVA")
# ==============================================================================
st.set_page_config(
    page_title="Petroperú AI Hub | Enterprise",
    layout="wide",
    page_icon="🛢️",
    initial_sidebar_state="collapsed"
)

# CSS Avanzado para eliminar scroll de página y crear layout fijo
estilos_app = """
<style>
    /* Reset básico para aprovechar toda la pantalla */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }
    
    /* Fondo oscuro corporativo */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        background-image: radial-gradient(#232736 1px, transparent 1px);
        background-size: 25px 25px;
    }

    /* Ocultar elementos nativos de Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* ESTILO PESTAÑAS (TABS) - Panel Izquierdo */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #374151;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: #1F2937;
        border-radius: 6px 6px 0 0;
        color: #9CA3AF;
        font-size: 13px;
        font-weight: 600;
        padding: 0 15px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7C3AED !important; /* Morado AI */
        color: white !important;
    }

    /* TARJETAS DE CHAT (ESTILO GEMINI/GPT) */
    .chat-container-scroll {
        overflow-y: auto;
        padding-right: 10px;
    }
    
    .bot-card {
        background-color: #1E293B; /* Slate 800 */
        border-left: 4px solid #7C3AED;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .user-card {
        background-color: #334155; /* Slate 700 */
        border-radius: 8px;
        padding: 12px 15px;
        margin-bottom: 12px;
        text-align: right;
        margin-left: 20%;
        color: #F8FAFC;
    }
    
    /* PANELES DE DATOS */
    .kpi-card {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(5px);
        margin-bottom: 10px;
    }
    
    /* BOTONES */
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        background-color: #2D3748;
        color: white;
        border: 1px solid #4A5568;
    }
    .stButton>button:hover {
        border-color: #7C3AED;
        color: #7C3AED;
    }
</style>
"""
st.markdown(estilos_app, unsafe_allow_html=True)

# ==============================================================================
# 2. GESTIÓN DE ESTADO (SESSION STATE)
# ==============================================================================
if 'inicializado' not in st.session_state:
    st.session_state.inicializado = True
    st.session_state.mensajes = [{
        "role": "assistant",
        "content": (
            "👋 **Bienvenido al Sistema Neural de Petroperú.**\n\n"
            "Soy su analista virtual con capacidades de Machine Learning. "
            "Puedo realizar simulaciones financieras, analizar riesgos operativos y proyectar escenarios de flujo de caja.\n\n"
            "**¿En qué puedo asistirle hoy?**\n"
            "Ej: *'Simula EBITDA con WTI a $85'*, *'Muéstrame el mapa de Talara'* o *'Dame el reporte de deuda'.*"
        )
    }]
    st.session_state.wti_simulado = 75.0
    st.session_state.modo_ml = False

# ==============================================================================
# 3. LÓGICA DE NEGOCIO Y "CEREBRO" AI
# ==============================================================================

class PetroBrain:
    def __init__(self):
        # Base de Conocimiento Estática (RAG Context)
        self.knowledge_base = {
            "historia": "Petroperú fue creada en 1969. En los 90s sufrió un proceso de fragmentación (venta de grifos, flota y gas). Actualmente, con la Nueva Refinería Talara (NRT), busca recuperar la integración vertical y margen de refino.",
            "deuda": "La deuda total asciende a **$8.5 Billones**. Se compone principalmente de Bonos Soberanos ($3B) y crédito sindicado CESCE ($1.3B). La estrategia actual depende del apoyo del MEF para garantías de capital de trabajo.",
            "talara": "La NRT tiene una capacidad de 95,000 barriles/día. Su unidad clave es el Flexicoking. El margen objetivo es de $10-$12/bbl para garantizar el repago de la deuda."
        }

    def _simulacion_montecarlo(self, wti_base):
        """Genera proyección estocástica para EBITDA"""
        np.random.seed(int(time.time()))
        meses = ['Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        # Lógica financiera simple: WTI alto mejora margen (hipótesis)
        base_val = 100 + (wti_base - 70) * 2
        
        # Generar caminos aleatorios
        caminos = []
        for _ in range(500):
            ruido = np.random.normal(0, 5, 6)
            trend = np.linspace(base_val, base_val * 1.1, 6)
            caminos.append(trend + ruido)
            
        datos = np.array(caminos)
        p10 = np.percentile(datos, 10, axis=0) # Escenario Pesimista
        p50 = np.percentile(datos, 50, axis=0) # Escenario Base
        p90 = np.percentile(datos, 90, axis=0) # Escenario Optimista
        
        return meses, p10, p50, p90

    def procesar_consulta(self, prompt):
        prompt = prompt.lower()
        response = {"texto": "", "grafico": None, "tabla": None}

        # INTENCIÓN 1: PREDICCIÓN / SIMULACIÓN (ML)
        if any(x in prompt for x in ["prediccion", "simula", "futuro", "proyecta", "ebitda", "flujo"]):
            wti_actual = st.session_state.wti_simulado
            meses, p10, p50, p90 = self._simulacion_montecarlo(wti_actual)
            
            # Crear gráfico Fan Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=meses, y=p90, mode='lines', line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(x=meses, y=p10, mode='lines', fill='tonexty', 
                                     fillcolor='rgba(124, 58, 237, 0.2)', line=dict(width=0), name='Rango Confianza (80%)'))
            fig.add_trace(go.Scatter(x=meses, y=p50, mode='lines', 
                                     line=dict(color='#00C851', width=3), name='Escenario Base'))
            
            fig.update_layout(title="Proyección Montecarlo (EBITDA MM$)", template="plotly_dark", 
                              height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            
            response["texto"] = (
                f"🤖 **Ejecutando Modelo Predictivo (Montecarlo):**\n\n"
                f"Considerando un WTI base de **${wti_actual}**, he proyectado el desempeño para el H2.\n"
                f"• El escenario base sugiere una recuperación sostenida.\n"
                f"• Existe volatilidad implícita del 15% debido a factores externos."
            )
            response["grafico"] = fig
            return response

        # INTENCIÓN 2: DEUDA (TABLAS)
        if any(x in prompt for x in ["deuda", "bonos", "bancos", "pasivo"]):
            df_deuda = pd.DataFrame({
                "Instrumento": ["Bonos 2032", "Bonos 2047", "Sindicado CESCE", "Corto Plazo"],
                "Monto (MM$)": [1000, 2000, 1300, 2500],
                "Tasa": ["4.75%", "5.63%", "Libor+2.5%", "8.50%"]
            })
            response["texto"] = f"📉 **Análisis de Pasivos:**\n\n{self.knowledge_base['deuda']}\nAquí el desglose actual:"
            response["tabla"] = df_deuda
            return response

        # INTENCIÓN 3: CONOCIMIENTO GENERAL (RAG)
        for tema, info in self.knowledge_base.items():
            if tema in prompt:
                response["texto"] = f"📘 **Base de Conocimiento:**\n\n{info}"
                return response

        # FALLBACK
        response["texto"] = "No tengo datos específicos sobre eso en mi base actual. Puedo ayudarte con: **Simulaciones de EBITDA**, **Estructura de Deuda** o **Información de Talara**."
        return response

cerebro = PetroBrain()

# ==============================================================================
# 4. COMPONENTES VISUALES (PANTALLA IZQUIERDA)
# ==============================================================================

def render_simulador():
    st.markdown("#### 🎛️ Centro de Simulación")
    st.caption("Ajuste las variables macro para recalcular las proyecciones.")
    
    # Control Slider
    wti_input = st.slider("Precio Crudo WTI ($/bbl)", 40.0, 120.0, st.session_state.wti_simulado, step=1.0)
    st.session_state.wti_simulado = wti_input
    
    # Toggle ML
    ml_active = st.toggle("Activar Motor Neuronal", value=st.session_state.modo_ml)
    st.session_state.modo_ml = ml_active
    
    st.markdown("---")
    
    # KPI en Tiempo Real (Reactivo)
    ebitda_proy = 120 + (wti_input - 70) * 2.5
    delta = ((ebitda_proy - 120)/120)*100
    
    col_kpi1, col_kpi2 = st.columns(2)
    col_kpi1.metric("EBITDA Proyectado", f"${ebitda_proy:.1f} M", f"{delta:.1f}%")
    col_kpi2.metric("Caja Disponible", "$45.2 M", "-12%")
    
    # Gráfico Rápido
    df_chart = pd.DataFrame({
        'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'Real': [100, 110, 105, 115, 120, 125],
        'Proy': [100, 110, 105, 115, 120 + (wti_input-70), 125 + (wti_input-70)]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_chart['Mes'], y=df_chart['Proy'], name='Simulación', marker_color='#7C3AED'))
    fig.add_trace(go.Scatter(x=df_chart['Mes'], y=df_chart['Real'], name='Línea Base', line=dict(color='white', dash='dash')))
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=220, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

def render_mapa():
    st.markdown("#### 🗺️ Activos Geoespaciales")
    
    # Datos Geoespaciales Dummy
    data_talara = [{"name": "NRT Talara", "lat": -4.58, "lon": -81.27, "status": "Operativo"}]
    data_oleoducto = [{"name": "Estación 5", "lat": -5.5, "lon": -78.5, "status": "Alerta"}]
    
    layer_talara = pdk.Layer(
        "ScatterplotLayer", data=pd.DataFrame(data_talara),
        get_position=["lon", "lat"], get_color=[0, 200, 81, 200], get_radius=5000, pickable=True
    )
    layer_oleoducto = pdk.Layer(
        "ScatterplotLayer", data=pd.DataFrame(data_oleoducto),
        get_position=["lon", "lat"], get_color=[255, 68, 68, 200], get_radius=8000, pickable=True
    )
    
    view_state = pdk.ViewState(latitude=-5.0, longitude=-80.0, zoom=5.5, pitch=40)
    
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[layer_talara, layer_oleoducto],
        tooltip={"text": "{name}\nEstado: {status}"}
    )
    st.pydeck_chart(deck, use_container_width=True)
    
    st.info("ℹ️ **Alerta:** Mantenimiento preventivo en Tramo I del Oleoducto.")

def render_archivos():
    st.markdown("#### 📂 Data Room Financiero")
    
    data_files = pd.DataFrame({
        "Documento": ["EEFF Auditados 2023.pdf", "Presentación Inversionistas Q1.pptx", "Perfil Deuda Detallado.csv"],
        "Fecha": ["15/03/2024", "10/04/2024", "01/05/2024"],
        "Tipo": ["PDF", "PPTX", "CSV"]
    })
    st.dataframe(data_files, hide_index=True, use_container_width=True)
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.button("📥 Descargar Todo")
    with col_dl2:
        st.button("📧 Enviar por Correo")

# ==============================================================================
# 5. LAYOUT PRINCIPAL (DIVISIÓN DE PANTALLA)
# ==============================================================================

# Encabezado
c_logo, c_title = st.columns([0.5, 9])
with c_logo:
    st.markdown("## 🧠")
with c_title:
    st.markdown("### Petroperú GenAI | <span style='color:#7C3AED'>Financial Core v5.0</span>", unsafe_allow_html=True)

st.markdown("---")

# DIVISIÓN: 35% Panel Control | 65% Chat
col_izq, col_der = st.columns([0.35, 0.65], gap="medium")

# --- PANEL IZQUIERDO (HERRAMIENTAS) ---
with col_izq:
    # Contenedor con Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Simulador", "🗺️ Mapa", "📂 Archivos"])
    
    with tab1:
        render_simulador()
    with tab2:
        render_mapa()
    with tab3:
        render_archivos()

# --- PANEL DERECHO (CHAT) ---
with col_der:
    # Usamos st.container con altura definida para crear el efecto de scroll solo en el chat
    # Ajustamos altura según pantalla promedio (600px es un buen estándar para laptops)
    chat_container = st.container(height=600)
    
    with chat_container:
        # Renderizar historial
        for msg in st.session_state.mensajes:
            if msg["role"] == "assistant":
                # Mensaje Bot
                st.markdown(f"""
                <div class="bot-card">
                    <div style="display:flex; align-items:center; margin-bottom:5px;">
                        <span style="font-size:18px; margin-right:8px;">🤖</span>
                        <b style="color:#7C3AED;">PETRO-AI</b>
                    </div>
                    <div style="color:#E2E8F0; font-family:'Segoe UI';">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Renderizar Elementos Multimedia si existen en el historial
                if "grafico" in msg and msg["grafico"]:
                    st.plotly_chart(msg["grafico"], use_container_width=True)
                if "tabla" in msg and msg["tabla"] is not None:
                    st.dataframe(msg["tabla"], hide_index=True, use_container_width=True)
                    
            else:
                # Mensaje Usuario
                st.markdown(f"""
                <div class="user-card">
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)

    # Input Area (Fijo debajo del contenedor)
    prompt = st.chat_input("Escriba su consulta financiera estratégica aquí...")

    # Lógica de Respuesta
    if prompt:
        # 1. Agregar usuario al estado
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        
        # 2. Forzar actualización visual inmediata del mensaje usuario
        # (Esto hace que aparezca antes de procesar)
        st.rerun()

# --- PROCESAMIENTO POST-RERUN ---
# Esto se ejecuta al recargar la página tras el input del usuario
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with col_der:
        with chat_container:
            # Spinner de pensamiento dentro del chat
            with st.spinner("🔄 Analizando vectores financieros y ejecutando modelos..."):
                time.sleep(0.8) # Simular tiempo de cómputo
                
                # Obtener respuesta del Cerebro
                ultima_pregunta = st.session_state.mensajes[-1]["content"]
                respuesta_obj = cerebro.procesar_consulta(ultima_pregunta)
                
                # Guardar respuesta IA
                st.session_state.mensajes.append({
                    "role": "assistant",
                    "content": respuesta_obj["texto"],
                    "grafico": respuesta_obj["grafico"],
                    "tabla": respuesta_obj["tabla"]
                })
                
                # Recargar para mostrar la respuesta final
                st.rerun()
