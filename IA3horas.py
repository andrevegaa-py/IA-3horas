import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO CONSULTOR EXPERTO)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Proyecciones Estratégicas",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para inmersión total
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 900px !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0F172A; /* Azul noche profundo */
    }
    
    /* BURBUJAS DE CHAT */
    .chat-bubble {
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 24px;
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .user-bubble {
        background-color: #334155;
        border: 1px solid #475569;
        color: #F8FAFC;
        margin-left: 15%;
        border-radius: 15px 15px 2px 15px;
        text-align: right;
    }
    
    .bot-bubble {
        background-color: #1E293B;
        border-left: 4px solid #00C851; /* Verde Petrolito */
        color: #CBD5E1;
        margin-right: 5%;
        border-radius: 15px 15px 15px 2px;
    }

    /* ESTILOS DE TEXTO RICOS */
    .bot-bubble h3 { color: #38BDF8 !important; margin: 0 0 12px 0; font-size: 19px; font-weight: 600; }
    .bot-bubble strong { color: #00C851; font-weight: 600; }
    .bot-bubble em { color: #94A3B8; font-style: italic; }
    
    /* SUGERENCIAS (BOTONES) */
    .suggestion-btn {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid #38BDF8;
        color: #38BDF8;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        margin-right: 8px;
        margin-top: 8px;
        cursor: default;
    }

    /* INPUT FLOTANTE */
    .stChatInput {
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px !important;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO DE PETROLITO (LÓGICA AVANZADA)
# ==============================================================================

if 'memory_state' not in st.session_state:
    st.session_state.memory_state = {
        "wti": 76.5,          # Precio barril actual
        "produccion": 95.0,   # Miles barriles/día
        "tema_anterior": None # Para entender contexto ("¿Y la deuda?")
    }

class PetrolitoBrain:
    def __init__(self):
        # Base de Datos Simulada
        self.db_files = pd.DataFrame({
            "Documento": ["Auditoría Costos NRT", "Perfil Deuda Sindicada", "Proyección Flujo Caja Q4"],
            "Fuente": ["PwC", "Gerencia Finanzas", "Petrolito AI"],
            "Fecha": ["2024-05", "2024-06", "Tiempo Real"]
        })

    # --- 1. MOTOR DE APRENDIZAJE Y CONTEXTO ---
    def analizar_input(self, prompt):
        """Detecta parámetros, intención y actualiza la memoria."""
        prompt_low = prompt.lower()
        state = st.session_state.memory_state
        learned_msg = ""
        intent = "general"

        # A. Actualización de Variables (Learning)
        # Regex flexible para captar "WTI a 80" o "Precio 80"
        match_wti = re.search(r'(wti|precio|barril).*?(\d{2,3}(\.\d+)?)', prompt_low)
        if match_wti:
            nuevo = float(match_wti.group(2))
            state['wti'] = nuevo
            learned_msg += f"📝 *He recalibrado mis modelos con un WTI de ${nuevo}.* "

        match_prod = re.search(r'(producci.n|refineria).*?(\d{2,3})', prompt_low)
        if match_prod:
            nuevo = float(match_prod.group(2))
            state['produccion'] = nuevo
            learned_msg += f"📝 *Ajusté la carga de refinería a {nuevo} KBPD.* "

        # B. Detección de Intención (Fuzzy Logic)
        if any(x in prompt_low for x in ["talara", "refineria", "nrt", "costos"]):
            intent = "talara"
        elif any(x in prompt_low for x in ["deuda", "bonos", "financiero", "dinero", "caja", "ebitda", "flujo"]):
            intent = "finanzas"
        elif any(x in prompt_low for x in ["archivo", "descargar", "documento"]):
            intent = "archivos"
        # Manejo de contexto implícito ("¿Y cómo afecta eso?", "¿Y la producción?")
        elif len(prompt.split()) < 4 and state['tema_anterior']:
             # Si la frase es corta, asumimos que sigue hablando del tema anterior
             intent = state['tema_anterior']
        
        # Guardar tema para la próxima (Memoria de Corto Plazo)
        state['tema_anterior'] = intent
        
        return intent, learned_msg

    # --- 2. GENERADORES DE PROYECCIONES (VISUALES) ---
    def _grafico_proyeccion(self):
        wti = st.session_state.memory_state['wti']
        prod = st.session_state.memory_state['produccion']
        
        # Modelo Matemático Simplificado de Petrolito
        # EBITDA = Base + (Delta WTI * Sensibilidad) + (Delta Prod * Eficiencia)
        ebitda_base = 100 
        impacto_wti = (wti - 70) * 2.5
        impacto_prod = (prod - 95) * 1.5
        ebitda_final = ebitda_base + impacto_wti + impacto_prod

        meses = ['Histórico', 'Mes Actual', '+1 Mes', '+2 Meses', '+3 Meses (Proy)']
        # Datos simulados con tendencia
        valores = [90, 95, ebitda_final*0.9, ebitda_final*0.95, ebitda_final]
        
        colores = ['#64748B']*2 + ['#00C851']*3 # Gris para pasado, Verde para futuro

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=meses, y=valores, marker_color=colores,
            text=[f"${v:.0f}M" for v in valores], textposition='auto'
        ))
        fig.add_trace(go.Scatter(
            x=meses, y=[v*1.05 for v in valores], mode='lines', 
            name='Escenario Optimista', line=dict(color='#38BDF8', dash='dash')
        ))
        
        fig.update_layout(
            title=f"Proyección EBITDA (Escenario: WTI ${wti})",
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, margin=dict(l=20, r=20, t=40, b=20),
            font=dict(family="Segoe UI")
        )
        return fig

    # --- 3. GENERADOR DE RESPUESTA HUMANIZADA ---
    def generar_respuesta(self, prompt):
        intent, learned_header = self.analizar_input(prompt)
        response = {"texto": "", "visuales": []}
        state = st.session_state.memory_state

        # INTENCIÓN: FINANZAS / PROYECCIÓN
        if intent == "finanzas":
            response["texto"] = (
                f"{learned_header}\n"
                f"### 📊 Análisis de Solvencia y Proyección\n"
                f"Analizando los fundamentales actuales (WTI **${state['wti']}**), preveo una recuperación progresiva del flujo de caja.\n\n"
                f"Si bien la deuda estructural sigue siendo un desafío, el EBITDA proyectado muestra una tendencia positiva gracias a los precios actuales. "
                f"Aquí le presento la simulación a 3 meses bajo las condiciones que me indicó:"
            )
            response["visuales"].append(("grafico", self._grafico_proyeccion()))
            
        # INTENCIÓN: TALARA / OPERACIONES
        elif intent == "talara":
            response["texto"] = (
                f"{learned_header}\n"
                f"### 🏭 Nueva Refinería Talara (NRT)\n"
                f"Entendido. Respecto a la operación técnica, estamos procesando **{state['produccion']} mil barriles diarios**.\n\n"
                f"La unidad de Flexicoking está estable. Sin embargo, para maximizar el margen de refino, "
                f"recomendaría vigilar el *Crack Spread* del diésel. Técnicamente, la refinería es rentable operativamente con estos volúmenes."
            )
            # Podríamos añadir gráfico de costos aquí si fuera necesario
            
        # INTENCIÓN: ARCHIVOS
        elif intent == "archivos":
            response["texto"] = (
                "### 📂 Data Room Corporativo\n"
                "He recuperado los documentos oficiales más recientes desde el servidor seguro. "
                "Puede descargarlos o visualizarlos directamente:"
            )
            response["visuales"].append(("tabla", self.db_files))

        # INTENCIÓN: AMBIGUA / GENERAL (GUÍA PROACTIVA)
        else:
            response["texto"] = (
                f"{learned_header}\n"
                f"### 🤖 Estoy listo, colega.\n"
                f"Actualmente mis proyecciones corren con un **WTI de ${state['wti']}** y una producción de **{state['produccion']}k**.\n\n"
                f"Si la consulta es vaga, puedo sugerirle profundizar en:\n"
                f"<span class='suggestion-btn'>📈 Proyectar Flujo de Caja</span> "
                f"<span class='suggestion-btn'>🏭 Ver Estado Talara</span> "
                f"<span class='suggestion-btn'>📉 Analizar Deuda</span>\n\n"
                f"*¿Sobre qué eje estratégico desea que profundice?*"
            )

        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. GESTIÓN DEL CHAT
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Saludo inicial empático
    st.session_state.mensajes.append({
        "role": "assistant", 
        "contenido": {
            "texto": (
                "👋 **Hola, soy Petrolito.**\n\n"
                "Estoy conectado a los datos de mercado en tiempo real (simulado). "
                "Puedo hacer proyecciones financieras, analizar Talara o recalibrar mis modelos si tú me das nuevos datos.\n\n"
                "*Prueba diciéndome: 'El WTI subió a 85' o simplemente pregúntame '¿Cómo está la refinería?'*"
            ),
            "visuales": []
        }
    })

# ==============================================================================
# 4. RENDERIZADO DEL CHAT
# ==============================================================================

# Header limpio
st.markdown("<h2 style='text-align:center; color:#E2E8F0;'>🤖 Petrolito <span style='color:#00C851;'>AI</span></h2>", unsafe_allow_html=True)

# Render Loop
for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["contenido"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["contenido"]
        # Render Bot
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span style="font-size:22px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#00C851; font-size:16px;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Render Visuales Interactivos
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

if prompt := st.chat_input("Consulta a Petrolito (Ej: 'Proyecta el EBITDA' o 'El WTI bajó a 70')"):
    # 1. Guardar mensaje usuario
    st.session_state.mensajes.append({"role": "user", "contenido": prompt})
    st.rerun()

# Respuesta Inmediata
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Petrolito está analizando escenarios..."):
        time.sleep(0.6) # Pequeña latencia para naturalidad
        
        ultima_entrada = st.session_state.mensajes[-1]["contenido"]
        
        # EL CEREBRO PROCESA LA RESPUESTA
        respuesta_ia = brain.generar_respuesta(ultima_entrada)
        
        st.session_state.mensajes.append({"role": "assistant", "contenido": respuesta_ia})
        st.rerun()
