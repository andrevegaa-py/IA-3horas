import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO ENTERPRISE CHAT)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Master Core",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# CSS Avanzado para Interfaz de Chat Inmersiva
st.markdown("""
<style>
    /* Layout */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 7rem !important;
        max-width: 950px !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0B0F19; /* Azul Noche */
    }
    
    /* Burbujas */
    .chat-bubble {
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .user-bubble {
        background-color: #334155;
        border: 1px solid #475569;
        color: #F8FAFC;
        margin-left: 15%;
        text-align: right;
        border-bottom-right-radius: 4px;
    }
    .bot-bubble {
        background-color: #1E293B;
        border-left: 4px solid #00C851; /* Verde Petrolito */
        color: #E2E8F0;
        margin-right: 5%;
        border-bottom-left-radius: 4px;
    }

    /* Elementos Internos */
    .bot-bubble h3 { color: #38BDF8 !important; margin: 0 0 10px 0; font-size: 20px; }
    .bot-bubble strong { color: #00C851; font-weight: 600; }
    .bot-bubble ul { margin-bottom: 15px; }
    .bot-bubble li { margin-bottom: 8px; }
    
    /* Pregunta Estratégica */
    .strategic-q {
        display: block;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #334155;
        color: #38BDF8;
        font-weight: bold;
        font-style: italic;
    }

    /* Input Flotante */
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
# 2. CEREBRO INTEGRAL (CONOCIMIENTO + APRENDIZAJE + VISUALES)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 76.5,
        "produccion": 95.0,
        "tema_actual": "inicio"
    }

class PetrolitoBrain:
    def __init__(self):
        # --- BASE DE DATOS MASIVA (HISTORIA, FINANZAS, OPS) ---
        self.knowledge_base = {
            "historia": """
            **📜 Historia Corporativa:**
            * **Origen (1969):** Creada por Velasco Alvarado tras expropiar a la IPC en Talara. Misión: Soberanía energética.
            * **Crisis de los 90:** Privatización fragmentada. Se vendieron activos rentables: Flota (Transoceánica), Gas (Solgas) y Grifos, perdiendo la integración vertical.
            * **Actualidad:** Ley 30130 (2013) impulsó la Nueva Refinería Talara (NRT) para modernizar el desulfurizado.
            """,
            
            "deuda": """
            **💸 Estructura Financiera ($8.5 Billones):**
            * **Bonos Soberanos:** ~$3,000 MM (Vencimientos 2032 y 2047). Tasas fijas pero altas.
            * **Crédito CESCE:** ~$1,300 MM (Garantía española para la refinería).
            * **Corto Plazo:** El problema crítico. Compramos crudo al contado y vendemos a crédito (descalce de liquidez).
            * **Rating:** Calificación presionada (CCC+/B) que encarece el crédito.
            """,
            
            "operaciones": """
            **🏭 Nueva Refinería Talara (NRT):**
            * **Capacidad:** 95,000 Barriles/Día (KBPD).
            * **Unidad Clave:** Flexicoking (Convierte residuales baratos en productos caros).
            * **Margen Objetivo:** $10-$12/bbl (vs $4 de refinería antigua).
            
            **🛢️ Oleoducto Norperuano (ONP):**
            * Activo crítico para traer crudo de la selva, pero sufre constantes cortes por terceros y geodinámica.
            """
        }
        
        # Base de Archivos
        self.files_db = pd.DataFrame({
            "Documento": ["EEFF Auditados 2023", "Perfil Deuda Detallado", "Plan Operativo NRT"],
            "Tipo": ["PDF", "XLSX", "PDF"],
            "Fecha": ["2024-03", "2024-05", "2024-06"]
        })

    # --- APRENDIZAJE (NLP) ---
    def aprender(self, prompt):
        prompt = prompt.lower()
        msg = ""
        actualizo = False
        
        # Detectar WTI
        match_wti = re.search(r'(wti|precio|crudo).*?(\d{2,3}(\.\d+)?)', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memoria['wti'] = val
            msg = f"📝 *He recalibrado mis modelos: WTI ajustado a ${val}.*"
            actualizo = True
            
        # Detectar Producción
        match_prod = re.search(r'(producci|carga|refin).*?(\d{2,3})', prompt)
        if match_prod:
            val = float(match_prod.group(2))
            st.session_state.memoria['produccion'] = val
            msg = f"📝 *Registro operativo actualizado: Carga NRT a {val} KBPD.*"
            actualizo = True
            
        return actualizo, msg

    # --- VISUALES DINÁMICOS ---
    def generar_visual(self, tipo):
        wti = st.session_state.memoria['wti']
        prod = st.session_state.memoria['produccion']
        
        if tipo == "simulacion_ebitda":
            # Modelo: EBITDA mejora con WTI y Prod alta
            base = 100 + (wti - 70)*2 + (prod - 95)
            vals = [base*0.8, base, base*1.2]
            fig = go.Figure(go.Bar(
                x=["Escenario Pesimista", "Base (Tu Input)", "Optimista"],
                y=vals, marker_color=['#EF4444', '#00C851', '#38BDF8'],
                text=[f"${v:.0f}M" for v in vals], textposition='auto'
            ))
            fig.update_layout(title=f"Proyección EBITDA (WTI ${wti})", template="plotly_dark", 
                              paper_bgcolor='rgba(0,0,0,0)', height=300)
            return fig

        elif tipo == "mapa_activos":
            # Mapa Geoespacial con PyDeck
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=pd.DataFrame([
                    {"name": "Refinería Talara", "lat": -4.58, "lon": -81.27, "color": [0, 200, 81]},
                    {"name": "Estación 5 ONP", "lat": -5.5, "lon": -78.5, "color": [255, 68, 68]}
                ]),
                get_position=["lon", "lat"], get_color="color", get_radius=10000, pickable=True
            )
            view = pdk.ViewState(latitude=-5.0, longitude=-80.0, zoom=5, pitch=40)
            return pdk.Deck(layers=[layer], initial_view_state=view, map_style="mapbox://styles/mapbox/dark-v10", tooltip={"text": "{name}"})

        return None

    # --- LÓGICA CONVERSACIONAL (ENTREVISTADOR) ---
    def procesar(self, prompt):
        prompt_low = prompt.lower()
        actualizo, msg_learning = self.aprender(prompt)
        response = {"texto": "", "visual": None, "tipo_visual": None}
        
        prefix = msg_learning + "\n\n" if actualizo else ""
        
        # 1. TEMA: FINANZAS / DEUDA
        if any(x in prompt_low for x in ["deuda", "bonos", "financiera", "dinero", "caja"]):
            response["texto"] = (
                f"{prefix}### 📉 Análisis Financiero\n"
                f"{self.knowledge_base['deuda']}\n\n"
                f"Actualmente, con tu escenario de **WTI ${st.session_state.memoria['wti']}**, la presión de caja es significativa.\n"
                "<span class='strategic-q'>🤔 Pregunta estratégica: Dado que el servicio de deuda absorbe el flujo, ¿crees que la solución pasa por un nuevo aporte de capital del Estado o por reestructurar los bonos 2032?</span>"
            )
            response["visual"] = self.generar_visual("simulacion_ebitda")
            response["tipo_visual"] = "plotly"

        # 2. TEMA: OPERACIONES / TALARA
        elif any(x in prompt_low for x in ["talara", "operacion", "refineria", "flexicoking", "produccion"]):
            response["texto"] = (
                f"{prefix}### 🏭 Estado de la NRT\n"
                f"{self.knowledge_base['operaciones']}\n\n"
                f"Estamos operando a **{st.session_state.memoria['produccion']} KBPD**. La unidad de Flexicoking está optimizando residuales.\n"
                "<span class='strategic-q'>🔧 Consulta técnica: Para maximizar el margen, ¿deberíamos priorizar la producción de Turbo (aviones) o Diésel vehicular en este trimestre?</span>"
            )
            response["visual"] = self.generar_visual("mapa_activos")
            response["tipo_visual"] = "deck"

        # 3. TEMA: HISTORIA
        elif any(x in prompt_low for x in ["historia", "pasado", "origen", "1969"]):
            response["texto"] = (
                f"{prefix}{self.knowledge_base['historia']}\n\n"
                "<span class='strategic-q'>🧐 Reflexión: Muchos analistas dicen que perder los grifos y el gas en los 90 nos dejó vulnerables. ¿Coincides en que recuperar la integración vertical es la clave?</span>"
            )

        # 4. TEMA: ARCHIVOS / DATA ROOM
        elif any(x in prompt_low for x in ["archivo", "documento", "descargar"]):
            response["texto"] = (
                "### 📂 Data Room Corporativo\n"
                "He accedido al servidor seguro. Aquí están los reportes oficiales disponibles:"
            )
            response["visual"] = self.files_db
            response["tipo_visual"] = "dataframe"

        # 5. CONVERSACIÓN FLUIDA / SOLO APRENDIZAJE
        elif actualizo:
            response["texto"] = (
                f"{prefix}He actualizado mis tableros de control con tus nuevos datos.\n"
                "Ahora que hemos ajustado las variables macroeconómicas...\n"
                "<span class='strategic-q'>📊 ¿Quieres que proyecte el nuevo Flujo de Caja o prefieres revisar el impacto operativo en Talara?</span>"
            )
            response["visual"] = self.generar_visual("simulacion_ebitda")
            response["tipo_visual"] = "plotly"

        # 6. FALLBACK INTELIGENTE
        else:
            response["texto"] = (
                f"Hola. Soy **Petrolito AI**, tu socio estratégico.\n\n"
                f"Tengo en memoria un WTI de **${st.session_state.memoria['wti']}** y la refinería al **{int(st.session_state.memoria['produccion']/95*100)}%**.\n"
                "Puedo analizar:\n"
                "* La deuda de $8.5B y los Bonos.\n"
                "* La operación del Flexicoking en Talara.\n"
                "* La historia desde 1969.\n\n"
                "<span class='strategic-q'>👋 ¿Por dónde quieres empezar el análisis hoy?</span>"
            )

        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. GESTIÓN DE ESTADO
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Saludo inicial
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": {
            "texto": (
                "👋 **Bienvenido, Usuario.**\n\n"
                "Soy Petrolito AI. Tengo cargada toda la data histórica, financiera y operativa de la empresa. "
                "Además, aprendo de ti en tiempo real.\n\n"
                "<span class='strategic-q'>¿Quieres revisar la situación de la Deuda o el estado de Talara?</span>"
            ),
            "visual": None, "tipo_visual": None
        }
    })

# ==============================================================================
# 4. RENDERIZADO DEL CHAT
# ==============================================================================

st.markdown("<h2 style='text-align:center;'>🧠 Petroperú <span style='color:#00C851;'>AI Core</span></h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#64748B;'>Datos en Vivo: WTI <b>${st.session_state.memoria['wti']}</b> | Prod <b>{st.session_state.memoria['produccion']}k</b></p>", unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        # Render Texto Bot
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span style="font-size:24px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#00C851;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Render Visuales (Plotly / Mapas / Tablas)
        if pkg["visual"] is not None:
            with st.container():
                if pkg["tipo_visual"] == "plotly":
                    st.plotly_chart(pkg["visual"], use_container_width=True)
                elif pkg["tipo_visual"] == "deck":
                    st.pydeck_chart(pkg["visual"], use_container_width=True)
                elif pkg["tipo_visual"] == "dataframe":
                    st.dataframe(pkg["visual"], use_container_width=True, hide_index=True)

# ==============================================================================
# 5. INPUT Y PROCESAMIENTO
# ==============================================================================

if prompt := st.chat_input("Consulta a Petrolito... (Ej: 'Hablemos de deuda' o 'El WTI está en 90')"):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Petrolito está analizando escenarios..."):
        time.sleep(0.7) # Simular pensamiento
        
        ultima_entrada = st.session_state.mensajes[-1]["content"]
        respuesta_ia = brain.procesar(ultima_entrada)
        
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta_ia})
        st.rerun()
