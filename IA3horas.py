import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO "FULL CHAT")
# ==============================================================================
st.set_page_config(
    page_title="Petroperú GenAI | Integrated Core",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para simular interfaz nativa de Chat (Tipo ChatGPT/Gemini)
st.markdown("""
<style>
    /* Reset de márgenes para pantalla completa */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 900px !important; /* Ancho de lectura ideal */
    }
    
    /* Fondo Oscuro */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
    }
    
    /* Ocultar elementos de UI de Streamlit */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Estilos de Burbujas de Chat */
    .chat-bubble {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .user-bubble {
        background-color: #2D3748;
        border: 1px solid #4A5568;
        color: #E2E8F0;
        text-align: right;
        margin-left: 20%;
    }
    
    .bot-bubble {
        background-color: #1E293B; /* Slate 800 */
        border-left: 4px solid #7C3AED; /* Morado AI */
        color: #F8FAFC;
        margin-right: 5%;
    }

    /* Títulos dentro del chat */
    .bot-bubble h3 { color: #A78BFA !important; margin-top: 0; }
    .bot-bubble h4 { color: #38BDF8 !important; margin-top: 15px; }
    .bot-bubble strong { color: #00C851; }

    /* Input Flotante Fijo */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px !important;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO INTELIGENTE (LOGICA DE NEGOCIO INTEGRADA)
# ==============================================================================

class PetroBrainIntegrated:
    def __init__(self):
        # Base de Datos de Archivos (Data Room)
        self.files_db = pd.DataFrame({
            "ID": ["DOC-001", "DOC-002", "DOC-003", "DOC-004"],
            "Documento": ["Auditoría Costos NRT (PwC)", "Diagrama Flujo Flexicoking", "Estructura Deuda Bonistas", "Plan de Cierre de Brechas"],
            "Formato": ["PDF", "DWG", "XLSX", "PDF"],
            "Peso": ["4.5 MB", "12.1 MB", "1.2 MB", "0.8 MB"]
        })

    def _generar_waterfall_talara(self):
        """Genera el gráfico de desviación presupuestal"""
        fig = go.Figure(go.Waterfall(
            name = "Costo NRT", orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "total"],
            x = ["Presupuesto 2014", "Adicionales EPC", "Gastos Financieros", "Retrasos/Covid", "Costo Final"],
            y = [1300, 1500, 2400, 800, 0],
            connector = {"line":{"color":"white"}},
            decreasing = {"marker":{"color":"#00C851"}},
            increasing = {"marker":{"color":"#FF4444"}},
            totals = {"marker":{"color":"#33B5E5"}}
        ))
        fig.update_layout(
            title="Analítica de Costos: Nueva Refinería Talara (MM USD)",
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=350, font=dict(color='white')
        )
        return fig

    def _generar_produccion_talara(self):
        """Genera gráfico de producción actual"""
        df = pd.DataFrame({
            'Producto': ['Diésel', 'Gasolinas', 'GLP', 'Turbo', 'Residuales'],
            'Barriles': [45000, 32000, 5000, 8000, 5000]
        })
        fig = px.pie(df, values='Barriles', names='Producto', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.Bluered_r)
        fig.update_layout(
            title="Mix de Producción Diario (95 KBPD)",
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)',
            height=350, font=dict(color='white')
        )
        return fig

    def procesar_prompt(self, prompt):
        prompt = prompt.lower()
        response_package = {
            "texto": "", 
            "elementos_visuales": [] # Lista de (tipo, objeto)
        }

        # --- INTENCIÓN: TALARA (SOLICITUD INTEGRAL) ---
        if any(x in prompt for x in ["talara", "refineria", "nrt", "costos"]):
            response_package["texto"] = (
                "### 🏭 Nueva Refinería Talara (NRT)\n\n"
                "He compilado el informe ejecutivo solicitado. La NRT opera actualmente al **100% de carga (95 MBD)**, "
                "procesando crudos pesados gracias a la unidad de **Flexicoking**.\n\n"
                "A continuación presento la **auditoría visual de costos** y el **mix de producción** actual, seguido de los archivos fuente."
            )
            # Agregar Gráfico 1
            response_package["elementos_visuales"].append(("grafico", self._generar_waterfall_talara()))
            # Agregar Gráfico 2
            response_package["elementos_visuales"].append(("grafico", self._generar_produccion_talara()))
            # Agregar Archivos
            response_package["elementos_visuales"].append(("texto_extra", "#### 📂 Archivos Fuente Detectados:"))
            response_package["elementos_visuales"].append(("dataframe", self.files_db[self.files_db['Documento'].str.contains("NRT|Flexicoking")]))
            
            return response_package

        # --- INTENCIÓN: ARCHIVOS / DATA ROOM ---
        if any(x in prompt for x in ["archivos", "documentos", "descargar", "data room"]):
            response_package["texto"] = (
                "### 📂 Data Room Corporativo\n\n"
                "Tengo acceso seguro al servidor de finanzas. Aquí están los documentos disponibles para su nivel de usuario:"
            )
            response_package["elementos_visuales"].append(("dataframe", self.files_db))
            return response_package

        # --- INTENCIÓN: SALUDO / DEFAULT ---
        response_package["texto"] = (
            "Hola. Soy la IA Central de Petroperú. \n\n"
            "Tengo todos los módulos integrados aquí mismo. Puedo mostrarte:\n"
            "1. **Análisis de Talara** (incluye gráficos de costos y producción).\n"
            "2. **Data Room** (acceso directo a archivos PDF/Excel).\n"
            "3. **Simulaciones Financieras**.\n\n"
            "¿Qué deseas visualizar?"
        )
        return response_package

brain = PetroBrainIntegrated()

# ==============================================================================
# 3. GESTIÓN DEL CHAT (STATE)
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Mensaje inicial proactivo
    start_pkg = brain.procesar_prompt("hola")
    st.session_state.mensajes.append({"role": "assistant", "contenido": start_pkg})

# ==============================================================================
# 4. RENDERIZADO DEL CHAT (LOOP PRINCIPAL)
# ==============================================================================

# Header simple
st.markdown("<h2 style='text-align: center; color: #E2E8F0;'>🧠 Petroperú AI <span style='color:#7C3AED'>Nexus</span></h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; margin-bottom: 30px;'>Inteligencia Financiera & Operativa Unificada</p>", unsafe_allow_html=True)

# Contenedor principal de mensajes
for msg in st.session_state.mensajes:
    
    if msg["role"] == "user":
        # Render Usuario
        st.markdown(f"""
        <div class="chat-bubble user-bubble">
            {msg["contenido"]}
        </div>
        """, unsafe_allow_html=True)
        
    elif msg["role"] == "assistant":
        # Render Bot (Complejo: Texto + Gráficos + Tablas mixtos)
        pkg = msg["contenido"]
        
        # 1. Texto Principal
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span style="font-size:24px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#E2E8F0;">AI ANALYST</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Elementos Visuales (Se renderizan FUERA de la burbuja HTML para mantener interactividad de Plotly/Pandas)
        if pkg["elementos_visuales"]:
            with st.container():
                for tipo, data in pkg["elementos_visuales"]:
                    if tipo == "grafico":
                        st.plotly_chart(data, use_container_width=True)
                    elif tipo == "dataframe":
                        st.dataframe(data, use_container_width=True, hide_index=True)
                    elif tipo == "texto_extra":
                        st.markdown(data)

# ==============================================================================
# 5. INPUT DE USUARIO & PROCESAMIENTO
# ==============================================================================

if prompt := st.chat_input("Ej: 'Dame el reporte completo de Talara con gráficos'"):
    
    # 1. Guardar y mostrar mensaje de usuario
    st.session_state.mensajes.append({"role": "user", "contenido": prompt})
    st.rerun()

# Lógica post-rerun (Se ejecuta inmediatamente después de que el usuario envía)
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    
    with st.spinner("🔄 Consultando base de datos, generando gráficos y recuperando archivos..."):
        time.sleep(1) # Simulación de pensamiento
        
        # Procesar
        respuesta_pkg = brain.procesar_prompt(st.session_state.mensajes[-1]["contenido"])
        
        # Guardar respuesta
        st.session_state.mensajes.append({"role": "assistant", "contenido": respuesta_pkg})
        st.rerun()
