import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO NEURAL CHAT)
# ==============================================================================
st.set_page_config(
    page_title="Petroperú Neural AI | Self-Learning",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# CSS Profesional para experiencia tipo ChatGPT/Gemini
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important; /* Espacio para el input */
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
        border-left: 4px solid #8B5CF6; /* Violeta Neural */
        color: #E2E8F0;
        margin-right: 5%;
        border-radius: 12px 12px 12px 0;
    }

    /* ESTILOS DE TEXTO RICOS */
    .bot-bubble h3 { color: #A78BFA !important; margin: 0 0 10px 0; font-size: 18px; }
    .bot-bubble strong { color: #34D399; font-weight: 600; } /* Verde Esmeralda */
    .highlight { background-color: rgba(139, 92, 246, 0.2); padding: 2px 6px; border-radius: 4px; color: #D8B4FE; }

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
# 2. MOTOR DE APRENDIZAJE (MACHINE LEARNING CORE)
# ==============================================================================

if 'memory_state' not in st.session_state:
    # Estado inicial (Conocimiento Base)
    st.session_state.memory_state = {
        "wti": 76.5,          # Precio del barril
        "produccion": 95.0,   # Miles de barriles/dia
        "deuda_total": 8.5,   # Billones USD
        "tasa_interes": 8.5,  # Tasa base %
        "tema_actual": None,  # Contexto de conversación
        "usuario_nombre": "Gerente"
    }

class NeuralBrain:
    def __init__(self):
        # Base de Conocimiento Estática (Archivos y Datos Fijos)
        self.files_db = pd.DataFrame({
            "ID": ["DOC-001", "DOC-002", "DOC-003"],
            "Documento": ["Auditoría Costos NRT (PwC)", "Estructura Deuda Bonistas", "Plan Cierre Brechas"],
            "Formato": ["PDF", "XLSX", "PDF"]
        })

    # --- MÓDULO DE APRENDIZAJE (NLP PARSER) ---
    def aprender_del_usuario(self, prompt):
        """
        Analiza el texto del usuario para extraer nuevas variables y actualizar
        el modelo mental de la IA (Session State).
        """
        prompt = prompt.lower()
        aprendido_algo = False
        mensaje_aprendizaje = ""

        # 1. Detectar cambio de WTI
        # Ej: "El WTI ahora está en 90" o "Cambia el precio a 85.5"
        match_wti = re.search(r'(wti|precio|barril).*?(\d{2,3}(\.\d+)?)', prompt)
        if match_wti:
            nuevo_valor = float(match_wti.group(2))
            st.session_state.memory_state['wti'] = nuevo_valor
            aprendido_algo = True
            mensaje_aprendizaje += f"✅ He actualizado mi modelo: **WTI = ${nuevo_valor}**.\n"

        # 2. Detectar cambio de Producción
        # Ej: "La producción bajó a 80"
        match_prod = re.search(r'(producci.n|refineria).*?(\d{2,3})', prompt)
        if match_prod:
            nuevo_valor = float(match_prod.group(2))
            st.session_state.memory_state['produccion'] = nuevo_valor
            aprendido_algo = True
            mensaje_aprendizaje += f"✅ Registro operativo actualizado: **Carga NRT = {nuevo_valor} KBPD**.\n"

        # 3. Detectar contexto
        if "deuda" in prompt: st.session_state.memory_state['tema_actual'] = "deuda"
        elif "talara" in prompt: st.session_state.memory_state['tema_actual'] = "talara"
        elif "mapa" in prompt: st.session_state.memory_state['tema_actual'] = "geo"

        return aprendido_algo, mensaje_aprendizaje

    # --- GENERADORES VISUALES DINÁMICOS (Se adaptan a lo aprendido) ---
    def _generar_simulacion_ebitda(self):
        wti = st.session_state.memory_state['wti']
        prod = st.session_state.memory_state['produccion']
        
        # Lógica ML: El EBITDA depende de WTI y Producción
        factor_wti = (wti - 60) * 3  # Sensibilidad
        factor_prod = (prod / 95)    # Eficiencia
        base_ebitda = 100 * factor_prod + factor_wti
        
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul (Proy)']
        valores = [base_ebitda + np.random.randint(-10, 10) for _ in range(7)]
        valores[-1] = base_ebitda * 1.1 # Proyección optimista

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=valores, mode='lines+markers', 
                                 line=dict(color='#8B5CF6', width=4), name='EBITDA Dinámico'))
        fig.update_layout(title=f"Proyección EBITDA (Escenario: WTI ${wti} | Prod {prod}k)", 
                          template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        return fig

    def _generar_waterfall_talara(self):
        # Este gráfico es histórico, no cambia con WTI, pero se mantiene por solicitud de "no perder datos"
        fig = go.Figure(go.Waterfall(
            name = "Costo NRT", orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "total"],
            x = ["Base 2014", "EPC Adicional", "Financiero", "Retrasos", "Total"],
            y = [1300, 1500, 2400, 800, 0],
            connector = {"line":{"color":"white"}},
            decreasing = {"marker":{"color":"#34D399"}},
            increasing = {"marker":{"color":"#F87171"}},
            totals = {"marker":{"color":"#38BDF8"}}
        ))
        fig.update_layout(title="Auditoría de Costos NRT (MM USD)", template="plotly_dark", 
                          paper_bgcolor='rgba(0,0,0,0)', height=300)
        return fig

    # --- PROCESADOR PRINCIPAL ---
    def procesar_interaccion(self, prompt):
        response = {"texto": "", "visuales": []}
        
        # 1. FASE DE APRENDIZAJE
        aprendido, msg_aprendizaje = self.aprender_del_usuario(prompt)
        
        # 2. GENERACIÓN DE RESPUESTA
        prompt_low = prompt.lower()
        state = st.session_state.memory_state
        
        if aprendido:
            response["texto"] = f"{msg_aprendizaje}\nHe recalculado todas las proyecciones financieras basándome en los nuevos parámetros. ¿Qué indicador desea revisar ahora?"
            # Mostramos automáticamente el impacto del aprendizaje
            response["visuales"].append(("grafico", self._generar_simulacion_ebitda()))
            return response

        # Intención: TALARA
        if "talara" in prompt_low or state['tema_actual'] == "talara" and ("detalle" in prompt_low or "grafico" in prompt_low):
            response["texto"] = (
                f"### 🏭 Estado Situacional Talara (NRT)\n"
                f"Considerando su input actual de **Producción: {state['produccion']} KBPD**.\n\n"
                "La refinería opera bajo régimen de optimización de margen. "
                "A continuación presento la estructura de costos históricos y la proyección de flujo operativa ajustada a sus variables."
            )
            response["visuales"].append(("grafico", self._generar_waterfall_talara()))
            response["visuales"].append(("grafico", self._generar_simulacion_ebitda()))
            return response

        # Intención: FINANZAS / SIMULACIÓN
        if any(x in prompt_low for x in ["ebitda", "flujo", "caja", "finanza", "proyeccion"]):
            response["texto"] = (
                f"### 🔮 Simulación Financiera en Tiempo Real\n"
                f"Parámetros del modelo:\n"
                f"• **WTI:** ${state['wti']}/bbl\n"
                f"• **Producción:** {state['produccion']} KBPD\n"
                f"• **Deuda:** ${state['deuda_total']} B\n\n"
                "El algoritmo predice el siguiente comportamiento de EBITDA para el próximo trimestre:"
            )
            response["visuales"].append(("grafico", self._generar_simulacion_ebitda()))
            return response

        # Intención: ARCHIVOS
        if "archivo" in prompt_low or "documento" in prompt_low:
            response["texto"] = "### 📂 Data Room\nAccediendo al repositorio seguro. Estos son los archivos disponibles:"
            response["visuales"].append(("tabla", self.files_db))
            return response

        # Default / Conversación
        response["texto"] = (
            f"Entendido, {state['usuario_nombre']}. Mi modelo actual tiene un WTI de **${state['wti']}** y Producción de **{state['produccion']}k**.\n\n"
            "💡 **Puedes enseñarme nuevos datos.** Prueba diciéndome:\n"
            "- *'El WTI subió a 85 dólares'*\n"
            "- *'La producción cayó a 60'*\n"
            "- *'Dame el reporte de Talara'*"
        )
        return response

brain = NeuralBrain()

# ==============================================================================
# 3. GESTIÓN DEL CHAT (SESSION STATE & LOOP)
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Mensaje de bienvenida proactivo
    bienvenida = {
        "texto": (
            "👋 **Sistema Neural Iniciado.**\n\n"
            "Soy una IA con capacidad de **aprendizaje en sesión**. No uso datos fijos; aprendo de lo que me dices.\n"
            "Actualmente asumo un WTI de **$76.5** y Producción al **95%**.\n\n"
            "**¿Deseas actualizar estos parámetros o ver un reporte?**"
        ),
        "visuales": []
    }
    st.session_state.mensajes.append({"role": "assistant", "contenido": bienvenida})

# ==============================================================================
# 4. RENDERIZADO DEL CHAT
# ==============================================================================

# Encabezado Flotante
st.markdown("<h2 style='text-align:center;'>🧠 Petroperú <span style='color:#8B5CF6;'>Neural Core</span></h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#64748B;'>Parámetros Activos: WTI <b>${st.session_state.memory_state['wti']}</b> | Prod <b>{st.session_state.memory_state['produccion']}k</b></p>", unsafe_allow_html=True)

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
                <span style="font-weight:bold; color:#A78BFA;">AI LEARNING MODEL</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Render Visuales (Fuera de la burbuja para que sean interactivos)
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

if prompt := st.chat_input("Ej: 'El WTI está en 90' o 'Muestra Talara'"):
    # 1. Agregar usuario
    st.session_state.mensajes.append({"role": "user", "contenido": prompt})
    st.rerun()

# Respuesta Inmediata
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("🧠 Procesando nuevos datos y actualizando redes neuronales..."):
        time.sleep(0.8) # Latencia para realismo
        
        ultima_entrada = st.session_state.mensajes[-1]["contenido"]
        respuesta_ia = brain.procesar_interaccion(ultima_entrada)
        
        st.session_state.mensajes.append({"role": "assistant", "contenido": respuesta_ia})
        st.rerun()
