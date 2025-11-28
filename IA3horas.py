import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO PETROLITO)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Asistente Financiero",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

# CSS Profesional
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        max-width: 950px !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0B0F19;
    }
    header, footer, #MainMenu {visibility: hidden;}
    
    /* BURBUJAS DE CHAT */
    .chat-bubble {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        line-height: 1.6;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .user-bubble {
        background-color: #334155;
        border: 1px solid #475569;
        color: #F1F5F9;
        margin-left: 20%;
        border-radius: 12px 12px 0 12px;
    }
    
    .bot-bubble {
        background-color: #1E293B;
        border-left: 4px solid #00C851; /* Verde Petrolito */
        color: #E2E8F0;
        margin-right: 5%;
        border-radius: 12px 12px 12px 0;
    }

    /* ESTILOS DE TEXTO RICOS */
    .bot-bubble h3 { color: #38BDF8 !important; margin: 0 0 10px 0; font-size: 18px; }
    .bot-bubble strong { color: #00C851; font-weight: 600; }
    
    /* INPUT FLOTANTE */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px !important;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO DE PETROLITO (MACHINE LEARNING CORE)
# ==============================================================================

if 'memory_state' not in st.session_state:
    # Estado inicial (Conocimiento Base)
    st.session_state.memory_state = {
        "wti": 76.5,          # Precio del barril
        "produccion": 95.0,   # Miles de barriles/dia
        "deuda_total": 8.5,   # Billones USD
        "tasa_interes": 8.5,  # Tasa base %
        "tema_actual": None,  # Contexto de conversación
        "usuario_nombre": "Usuario" # Nombre genérico solicitado
    }

class PetrolitoBrain:
    def __init__(self):
        # Base de Conocimiento Estática
        self.files_db = pd.DataFrame({
            "ID": ["DOC-001", "DOC-002", "DOC-003"],
            "Documento": ["Auditoría Costos NRT (PwC)", "Estructura Deuda Bonistas", "Plan Cierre Brechas"],
            "Formato": ["PDF", "XLSX", "PDF"]
        })

    # --- MÓDULO DE APRENDIZAJE (NLP PARSER) ---
    def aprender_del_usuario(self, prompt):
        """Petrolito aprende nuevos datos de la conversación."""
        prompt = prompt.lower()
        aprendido_algo = False
        mensaje_aprendizaje = ""

        # 1. Detectar cambio de WTI
        match_wti = re.search(r'(wti|precio|barril).*?(\d{2,3}(\.\d+)?)', prompt)
        if match_wti:
            nuevo_valor = float(match_wti.group(2))
            st.session_state.memory_state['wti'] = nuevo_valor
            aprendido_algo = True
            mensaje_aprendizaje += f"📝 Entendido. He actualizado mi memoria: **WTI = ${nuevo_valor}**.\n"

        # 2. Detectar cambio de Producción
        match_prod = re.search(r'(producci.n|refineria).*?(\d{2,3})', prompt)
        if match_prod:
            nuevo_valor = float(match_prod.group(2))
            st.session_state.memory_state['produccion'] = nuevo_valor
            aprendido_algo = True
            mensaje_aprendizaje += f"📝 Registro operativo actualizado: **Producción = {nuevo_valor} KBPD**.\n"

        # 3. Detectar contexto
        if "deuda" in prompt: st.session_state.memory_state['tema_actual'] = "deuda"
        elif "talara" in prompt: st.session_state.memory_state['tema_actual'] = "talara"

        return aprendido_algo, mensaje_aprendizaje

    # --- GENERADORES VISUALES DINÁMICOS ---
    def _generar_simulacion_ebitda(self):
        wti = st.session_state.memory_state['wti']
        prod = st.session_state.memory_state['produccion']
        
        # Fórmula interna de Petrolito
        factor_wti = (wti - 60) * 3 
        factor_prod = (prod / 95)   
        base_ebitda = 100 * factor_prod + factor_wti
        
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul (Proy)']
        valores = [base_ebitda + np.random.randint(-10, 10) for _ in range(7)]
        valores[-1] = base_ebitda * 1.1 # Proyección optimista

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=valores, mode='lines+markers', 
                                 line=dict(color='#00C851', width=4), name='Flujo Petrolito'))
        fig.update_layout(title=f"Proyección Dinámica (WTI ${wti} | Prod {prod}k)", 
                          template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        return fig

    def _generar_waterfall_talara(self):
        fig = go.Figure(go.Waterfall(
            name = "Costo NRT", orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "total"],
            x = ["Base 2014", "EPC Adicional", "Financiero", "Retrasos", "Total"],
            y = [1300, 1500, 2400, 800, 0],
            connector = {"line":{"color":"white"}},
            decreasing = {"marker":{"color":"#00C851"}},
            increasing = {"marker":{"color":"#FF4444"}},
            totals = {"marker":{"color":"#33B5E5"}}
        ))
        fig.update_layout(title="Auditoría de Costos NRT (MM USD)", template="plotly_dark", 
                          paper_bgcolor='rgba(0,0,0,0)', height=300)
        return fig

    # --- PROCESADOR PRINCIPAL ---
    def procesar_interaccion(self, prompt):
        response = {"texto": "", "visuales": []}
        
        # 1. APRENDIZAJE
        aprendido, msg_aprendizaje = self.aprender_del_usuario(prompt)
        state = st.session_state.memory_state
        prompt_low = prompt.lower()
        
        if aprendido:
            response["texto"] = f"{msg_aprendizaje} He recalculado mis proyecciones con estos nuevos datos. ¿Qué más necesitas saber?"
            response["visuales"].append(("grafico", self._generar_simulacion_ebitda()))
            return response

        # 2. RESPUESTAS POR TEMA
        
        # Intención: TALARA
        if "talara" in prompt_low or (state['tema_actual'] == "talara" and any(x in prompt_low for x in ["ver", "grafico", "detalle"])):
            response["texto"] = (
                f"### 🏭 Nueva Refinería Talara (NRT)\n"
                f"Actualmente tengo registrada una producción de **{state['produccion']} miles de barriles por día**.\n\n"
                "Aquí tienes el desglose histórico de costos y mi proyección de flujo operativa actualizada:"
            )
            response["visuales"].append(("grafico", self._generar_waterfall_talara()))
            response["visuales"].append(("grafico", self._generar_simulacion_ebitda()))
            return response

        # Intención: FINANZAS / SIMULACIÓN
        if any(x in prompt_low for x in ["ebitda", "flujo", "caja", "finanza", "proyeccion", "dinero"]):
            response["texto"] = (
                f"### 🔮 Proyección Financiera (Motor Petrolito)\n"
                f"Estoy calculando el EBITDA basado en:\n"
                f"• **Precio WTI:** ${state['wti']}\n"
                f"• **Producción:** {state['produccion']} KBPD\n\n"
                "Según mi modelo de Machine Learning, este es el comportamiento esperado:"
            )
            response["visuales"].append(("grafico", self._generar_simulacion_ebitda()))
            return response

        # Intención: ARCHIVOS
        if any(x in prompt_low for x in ["archivo", "documento", "descargar", "excel", "pdf"]):
            response["texto"] = "### 📂 Acceso a Documentación\nClaro, aquí tienes los archivos oficiales disponibles en mi base de datos:"
            response["visuales"].append(("tabla", self.files_db))
            return response

        # Default / Conversación Abierta
        response["texto"] = (
            f"Hola, aquí **Petrolito** a tu servicio. 👋\n\n"
            f"Estoy monitoreando el WTI a **${state['wti']}** y la refinería al **{int(state['produccion']/95*100)}%** de capacidad.\n\n"
            "Puedes pedirme cualquier información, por ejemplo:\n"
            "🔹 *'Muéstrame los costos de Talara'*\n"
            "🔹 *'Calcula el EBITDA si el WTI sube a 85'*\n"
            "🔹 *'Dame los archivos de deuda'*\n"
            "¿En qué te ayudo hoy?"
        )
        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. GESTIÓN DEL CHAT (STATE)
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Saludo Inicial de Petrolito
    saludo = {
        "texto": (
            "🤖 **¡Hola! Soy Petrolito.**\n\n"
            "Soy tu asistente inteligente enfocado en finanzas y operaciones. "
            "Aprendo mientras conversamos. Ahora mismo asumo un WTI de **$76.5**.\n\n"
            "**¿Qué información necesitas consultar hoy?**"
        ),
        "visuales": []
    }
    st.session_state.mensajes.append({"role": "assistant", "contenido": saludo})

# ==============================================================================
# 4. RENDERIZADO DEL CHAT
# ==============================================================================

# Encabezado Petrolito
st.markdown("<h2 style='text-align:center;'>🤖 <span style='color:#00C851;'>Petrolito</span> AI Core</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#64748B;'>Memoria Activa: WTI <b>${st.session_state.memory_state['wti']}</b> | Prod <b>{st.session_state.memory_state['produccion']}k</b></p>", unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["contenido"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["contenido"]
        # Render Texto Bot
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:8px;">
                <span style="font-size:20px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#00C851;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Render Visuales (Fuera de HTML para interactividad)
        if pkg["visuales"]:
            with st.container():
                for tipo, data in pkg["visuales"]:
                    if tipo == "grafico":
                        st.plotly_chart(data, use_container_width=True)
                    elif tipo == "tabla":
                        st.dataframe(data, use_container_width=True, hide_index=True)

# ==============================================================================
# 5. INPUT Y PROCESAMIENTO
# ==============================================================================

if prompt := st.chat_input("Escribe aquí (Ej: 'El WTI subió a 90' o 'Ver archivos')"):
    # 1. Guardar mensaje usuario
    st.session_state.mensajes.append({"role": "user", "contenido": prompt})
    st.rerun()

# Respuesta Inmediata
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Petrolito está pensando..."):
        time.sleep(0.5) 
        
        ultima_entrada = st.session_state.mensajes[-1]["contenido"]
        respuesta_ia = brain.procesar_interaccion(ultima_entrada)
        
        st.session_state.mensajes.append({"role": "assistant", "contenido": respuesta_ia})
        st.rerun()
