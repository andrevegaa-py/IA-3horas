import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO NEURAL & INTERACTIVO)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Inteligencia Financiera",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados para Chat y Botones
st.markdown("""
<style>
    /* Layout General */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 8rem !important; /* Espacio extra para input */
        max-width: 900px !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0F172A; /* Dark Slate */
    }
    
    /* BURBUJAS DE CHAT */
    .chat-bubble {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    .user-bubble {
        background-color: #334155;
        border: 1px solid #475569;
        color: #F8FAFC;
        margin-left: 20%;
        text-align: right;
        border-radius: 15px 15px 2px 15px;
    }
    
    .bot-bubble {
        background-color: #1E293B;
        border-left: 4px solid #00C851; /* Verde Petrolito */
        color: #CBD5E1;
        margin-right: 5%;
        border-radius: 15px 15px 15px 2px;
    }
    
    /* BOTONES INTERACTIVOS DENTRO DEL CHAT */
    div.stButton > button {
        background-color: rgba(56, 189, 248, 0.1) !important;
        border: 1px solid #38BDF8 !important;
        color: #38BDF8 !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        padding: 5px 15px !important;
        margin-right: 5px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important;
        transform: scale(1.02);
    }

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
# 2. CEREBRO INTUITIVO (LOGICA DE NEGOCIO FLEXIBLE)
# ==============================================================================

if 'memory_state' not in st.session_state:
    st.session_state.memory_state = {
        "wti": 76.5,
        "produccion": 95.0,
        "ultimo_topico": None
    }

class PetrolitoBrain:
    def __init__(self):
        # Base de Datos Simulada (Data Lake)
        self.knowledge_base = {
            "finanzas": {
                "keywords": ["dinero", "caja", "ebitda", "flujo", "deuda", "bonos", "banco", "mef", "liquidez"],
                "text": "Financieramente, la prioridad es la gestión de liquidez de corto plazo. Con el WTI actual, proyectamos una recuperación del EBITDA, aunque el servicio de deuda ($8.5B) sigue presionando la caja. Se requiere rollover de líneas de crédito.",
                "actions": ["Proyectar Flujo de Caja", "Ver Estructura Deuda"]
            },
            "operaciones": {
                "keywords": ["talara", "refineria", "nrt", "produccion", "flexicoking", "carga", "barriles", "operativo"],
                "text": "La Nueva Refinería Talara (NRT) está operando en régimen de optimización. La unidad de Flexicoking es clave para procesar residuales. El margen de refino objetivo es >$10/bbl.",
                "actions": ["Ver Gráfico Producción", "Auditoría de Costos"]
            },
            "macro": {
                "keywords": ["wti", "precio", "mercado", "dolar", "tipo de cambio", "crudo", "brent"],
                "text": "El entorno macroeconómico es volátil. Nuestro modelo es sensible al precio del WTI y al Tipo de Cambio. Cada variación de $1 en el WTI impacta aproximadamente $20MM en el flujo anual.",
                "actions": ["Simular Impacto WTI", "Ver Tendencia Precio"]
            }
        }

    def _aprender_dato(self, prompt):
        """Extrae datos numéricos si el usuario los menciona"""
        prompt = prompt.lower()
        msg_extra = ""
        
        # Detectar WTI
        match_wti = re.search(r'(wti|precio).*?(\d{2,3})', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memory_state['wti'] = val
            msg_extra += f"📝 *Anotado: WTI ajustado a ${val}.* "
            
        # Detectar Producción
        match_prod = re.search(r'(producci|refin).*?(\d{2,3})', prompt)
        if match_prod:
            val = float(match_prod.group(2))
            st.session_state.memory_state['produccion'] = val
            msg_extra += f"📝 *Anotado: Producción ajustada a {val}k.* "
            
        return msg_extra

    def _generar_grafico(self, tipo):
        wti = st.session_state.memory_state['wti']
        
        if tipo == "flujo":
            # Gráfico de Proyección Financiera
            meses = ['Mes 1', 'Mes 2', 'Mes 3']
            base = 100 + (wti - 70) * 2
            vals = [base, base*1.05, base*1.1]
            fig = go.Figure(go.Bar(x=meses, y=vals, marker_color='#00C851', name='EBITDA'))
            fig.add_trace(go.Scatter(x=meses, y=[v+10 for v in vals], mode='lines', name='Optimista', line=dict(dash='dash', color='#38BDF8')))
            fig.update_layout(title=f"Proyección EBITDA (WTI ${wti})", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=20,r=20,t=40,b=20))
            return fig
            
        elif tipo == "costos":
            # Gráfico Waterfall Talara
            fig = go.Figure(go.Waterfall(
                orientation="v", measure=["relative", "relative", "total"],
                x=["Presupuesto", "Sobrecostos", "Final"], y=[1300, 7200, 0],
                connector={"line":{"color":"white"}}, decreasing={"marker":{"color":"green"}}, increasing={"marker":{"color":"red"}}, totals={"marker":{"color":"blue"}}
            ))
            fig.update_layout(title="Desviación Presupuestal NRT", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=20,r=20,t=40,b=20))
            return fig
        
        return None

    def pensar_respuesta(self, prompt):
        prompt_low = prompt.lower()
        response = {"texto": "", "visual": None, "opciones": []}
        
        # 1. Aprender (Learning Layer)
        learning_msg = self._aprender_dato(prompt)
        
        # 2. Inferencia de Tópico (Fuzzy Matching)
        topico_detectado = None
        score_max = 0
        
        for key, data in self.knowledge_base.items():
            matches = sum(1 for k in data["keywords"] if k in prompt_low)
            if matches > score_max:
                score_max = matches
                topico_detectado = key

        # 3. Construcción de Respuesta
        if topico_detectado:
            # Respuesta específica basada en conocimiento
            st.session_state.memory_state['ultimo_topico'] = topico_detectado
            data = self.knowledge_base[topico_detectado]
            
            response["texto"] = f"{learning_msg}\n{data['text']}"
            response["opciones"] = data['actions'] # Sugerencias interactivas
            
            # Generar gráfico automático si el usuario lo pidió explícitamente
            if "grafico" in prompt_low or "ver" in prompt_low or "proyectar" in prompt_low:
                if topico_detectado == "finanzas" or topico_detectado == "macro":
                    response["visual"] = self._generar_grafico("flujo")
                elif topico_detectado == "operaciones":
                    response["visual"] = self._generar_grafico("costos")

        elif learning_msg:
             # Solo aprendió un dato, pero no hay pregunta clara
             response["texto"] = f"{learning_msg}\nEntendido. He actualizado mis parámetros internos. ¿Qué análisis quieres que corra con estos nuevos datos?"
             response["opciones"] = ["Simular EBITDA", "Ver Impacto Operativo"]
             
        else:
            # Respuesta genérica / fallback inteligente
            response["texto"] = (
                "Entiendo tu consulta. Aunque no detecto un tema específico de mi base técnica, "
                "puedo analizar esto desde varias perspectivas. ¿Cómo prefieres enfocarlo?"
            )
            response["opciones"] = ["Enfoque Financiero", "Enfoque Operativo", "Ver Archivos"]
            
        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. GESTIÓN DE ESTADO Y CHAT
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Saludo inicial
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": {
            "texto": "👋 **Hola, soy Petrolito.**\nEstoy listo. Pregúntame lo que necesites sobre finanzas, operaciones o datos históricos, y te responderé intuitivamente.",
            "visual": None,
            "opciones": ["Ver Estado Financiero", "Estatus Talara"]
        }
    })

# Función para manejar clic en botones (Callback)
def clic_opcion(texto_opcion):
    # Simula que el usuario escribió la opción
    st.session_state.mensajes.append({"role": "user", "content": texto_opcion})

# ==============================================================================
# 4. RENDERIZADO DEL CHAT (CON BOTONES REALES)
# ==============================================================================

st.markdown("<h2 style='text-align:center;'>🤖 Petrolito <span style='color:#00C851;'>AI</span></h2>", unsafe_allow_html=True)

# Contenedor de mensajes
for i, msg in enumerate(st.session_state.mensajes):
    if msg["role"] == "user":
        # Mensaje Usuario
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    
    else:
        # Mensaje Bot
        pkg = msg["content"]
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span style="font-size:20px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#00C851;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Gráficos (si hay)
        if pkg["visual"]:
            st.plotly_chart(pkg["visual"], use_container_width=True)
            
        # BOTONES INTERACTIVOS (Solo en el último mensaje para no saturar)
        if pkg["opciones"] and i == len(st.session_state.mensajes) - 1:
            cols = st.columns(len(pkg["opciones"]) + 2) # Columnas dinámicas
            for idx, op in enumerate(pkg["opciones"]):
                # El botón llama a la función de clic
                if cols[idx].button(op, key=f"btn_{i}_{idx}"):
                    clic_opcion(op)
                    st.rerun()

# ==============================================================================
# 5. INPUT DE USUARIO
# ==============================================================================

if prompt := st.chat_input("Escribe aquí... (Ej: '¿Cómo está la caja?' o 'El WTI subió a 85')"):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

# Lógica de Respuesta Automática (se ejecuta tras un input o un clic en botón)
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Analizando..."):
        time.sleep(0.5) # Pequeña pausa para naturalidad
        
        ultima_pregunta = st.session_state.mensajes[-1]["content"]
        respuesta_ia = brain.pensar_respuesta(ultima_pregunta)
        
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta_ia})
        st.rerun()
