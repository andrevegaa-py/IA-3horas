import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re
import datetime

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (GEMINI-LIKE UI)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Enterprise Knowledge",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para replicar la elegancia de una IA avanzada
st.markdown("""
<style>
    /* Reset & Layout */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 8rem !important;
        max-width: 900px !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0F172A; /* Deep Space Blue */
    }
    
    /* Burbujas de Chat */
    .chat-bubble {
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        line-height: 1.7;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 16px;
        color: #E2E8F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .user-bubble {
        background-color: #334155;
        border: 1px solid #475569;
        margin-left: 20%;
        text-align: right;
    }
    
    .bot-bubble {
        background-color: #1E293B;
        border-left: 5px solid #38BDF8; /* Cyan Gemini */
    }

    /* Formato de Texto Rico */
    .bot-bubble h3 { color: #38BDF8 !important; margin-top: 0; font-size: 20px; font-weight: 700; }
    .bot-bubble h4 { color: #818CF8 !important; margin-top: 15px; font-size: 18px; font-weight: 600; }
    .bot-bubble strong { color: #34D399; font-weight: 600; }
    .bot-bubble code { background-color: #0F172A; color: #F472B6; padding: 2px 6px; border-radius: 4px; }
    .bot-bubble ul { margin-bottom: 15px; }
    .bot-bubble li { margin-bottom: 5px; }

    /* Botones Interactivos (Chips) */
    div.stButton > button {
        background-color: rgba(56, 189, 248, 0.05) !important;
        border: 1px solid #38BDF8 !important;
        color: #38BDF8 !important;
        border-radius: 24px !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        margin-right: 8px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        transform: translateY(-2px);
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
# 2. CEREBRO PROFUNDO (DEEP KNOWLEDGE ENGINE)
# ==============================================================================

# Variables de Estado Dinámicas (Memoria a Largo Plazo)
if 'contexto_ia' not in st.session_state:
    st.session_state.contexto_ia = {
        "wti_precio": 76.50,
        "produccion_nrt": 95.0, # Miles de barriles
        "deuda_total": 8500,    # Millones USD
        "tipo_cambio": 3.75,
        "usuario_nombre": "Colega"
    }

class PetrolitoBrain:
    def __init__(self):
        # 📚 BASE DE CONOCIMIENTO ENCICLOPÉDICA (SIMULADA)
        # Esto le da la capacidad de responder "Como Gemini" con datos duros.
        self.knowledge_base = {
            "historia": {
                "tags": ["historia", "origen", "creacion", "velasco", "ipc", "pasado", "privatizacion"],
                "titulo": "📜 Historia y Evolución Corporativa",
                "contenido": """
                **1. El Origen (1969):** Petroperú fue creada el 24 de julio de 1969, durante el gobierno de Juan Velasco Alvarado, tras la nacionalización de los activos de la *International Petroleum Company* (IPC) en Talara. Su misión fundacional fue garantizar la soberanía energética.
                
                **2. La Fragmentación (Años 90):** Durante el proceso de privatización, la empresa fue desmembrada. Perdió activos rentables como:
                * La Flota Petrolera (Transoceánica).
                * La planta de gas (Solgas).
                * Estaciones de servicio (Grifos).
                * Refinería La Pampilla (vendida a Repsol).
                
                **3. El Retorno (Actualidad):** Con la Ley 30130 (2013), se declaró de necesidad pública la modernización de la Refinería Talara. Actualmente, la estrategia busca la **Integración Vertical**: volver a explotar petróleo (Lotes I, VI, Z-69) para no depender de comprar crudo a precios internacionales.
                """
            },
            "financiera": {
                "tags": ["dinero", "deuda", "bonos", "caja", "ebitda", "liquidez", "mef", "prestamo", "dolar"],
                "titulo": "💸 Análisis de Situación Financiera",
                "contenido": """
                La situación financiera es compleja debido al apalancamiento por la construcción de la Nueva Refinería Talara (NRT).
                
                **📊 Estructura de la Deuda ($8.5 Billones):**
                * **Bonos Corporativos:** ~$3,000 MM (Vencimientos 2032 y 2047). Tienen garantía del propio activo, no soberana directa inicial.
                * **Crédito CESCE (España):** ~$1,300 MM sindicado con bancos internacionales.
                * **Capital de Trabajo:** Líneas revolventes de corto plazo que actualmente requieren garantías del MEF para mantener el suministro de combustibles.
                
                **⚠️ El Problema Central:** La 'Trampa de Liquidez'. La empresa compra crudo al contado (Cash) pero cobra combustibles a crédito (30-60 días). Si el WTI sube, se necesita más caja inmediata que la empresa no genera por el servicio de deuda.
                """
            },
            "operativa": {
                "tags": ["talara", "nrt", "refineria", "produccion", "flexicoking", "oleoducto", "onp", "selva"],
                "titulo": "🏭 Operaciones: Talara y Oleoducto",
                "contenido": """
                **1. Nueva Refinería Talara (NRT):**
                * **Capacidad:** 95,000 barriles por día (KBPD).
                * **Tecnología:** Cuenta con una unidad de *Flexicoking* (licencia ExxonMobil), única en la región, que convierte residuales (brea) en productos de alto valor y gas para autogeneración.
                * **Margen:** El objetivo es lograr un margen de refino de **$10-$12 por barril**, superior a los $3-$4 de la refinería antigua.
                
                **2. Oleoducto Norperuano (ONP):**
                Activo crítico que conecta la Selva con la Costa. Sufre constantes cortes por atentados (cortes intencionales) y geodinámica, lo que eleva los costos operativos y detiene el transporte de crudo de los lotes de la selva.
                """
            }
        }

    # --- MOTOR DE INFERENCIA Y APRENDIZAJE ---
    
    def razonar(self, prompt):
        """
        Analiza el prompt, actualiza variables si el usuario aporta datos nuevos,
        y selecciona la mejor respuesta de la base de conocimiento o genera una simulación.
        """
        prompt = prompt.lower()
        ctx = st.session_state.contexto_ia
        
        # 1. RETROALIMENTACIÓN ACTIVA (APRENDIZAJE)
        # Detecta si el usuario está corrigiendo o enseñando datos.
        aprendido = []
        
        # Regex para WTI
        match_wti = re.search(r'(wti|precio|barril).*?(\d{2,3}(\.\d+)?)', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            ctx['wti_precio'] = val
            aprendido.append(f"WTI actualizado a ${val}")

        # Regex para Producción
        match_prod = re.search(r'(producci|carga|refin).*?(\d{2,3})', prompt)
        if match_prod:
            val = float(match_prod.group(2))
            ctx['produccion_nrt'] = val
            aprendido.append(f"Producción ajustada a {val} KBPD")

        # 2. SELECCIÓN DE CONTENIDO (RAG SIMULADO)
        respuesta_base = None
        sugerencias = []
        visual = None
        
        # Buscar coincidencias en la base de conocimiento
        mejor_score = 0
        tema_detectado = None
        
        for llave, data in self.knowledge_base.items():
            score = sum(1 for tag in data["tags"] if tag in prompt)
            if score > mejor_score:
                mejor_score = score
                tema_detectado = llave
                respuesta_base = data
        
        # 3. GENERACIÓN DE RESPUESTA (NATURAL LANGUAGE GENERATION)
        response_text = ""
        
        # Encabezado de aprendizaje
        if aprendido:
            response_text += f"📝 *He actualizado mis modelos internos: {', '.join(aprendido)}.*\n\n"

        if tema_detectado == "financiera":
            response_text += f"### {respuesta_base['titulo']}\n{respuesta_base['contenido']}\n\n"
            response_text += f"💡 **Impacto en Tiempo Real:**\nCon el WTI actual de **${ctx['wti_precio']}**, la presión sobre la caja {( 'aumenta' if ctx['wti_precio'] > 80 else 'se estabiliza' )}. "
            response_text += "He generado una proyección de sensibilidad del EBITDA."
            visual = self._generar_grafico_ebitda()
            sugerencias = ["Ver Flujo de Caja", "Detalle de Bonos"]

        elif tema_detectado == "operativa":
            response_text += f"### {respuesta_base['titulo']}\n{respuesta_base['contenido']}\n\n"
            response_text += f"⚙️ **Estado Actual:**\nConsiderando tu input de **{ctx['produccion_nrt']} KBPD**, la refinería opera al **{min(100, int(ctx['produccion_nrt']/95*100))}%** de su capacidad nominal."
            visual = self._generar_grafico_waterfall()
            sugerencias = ["Ver Margen de Refino", "Mapa del Oleoducto"]

        elif tema_detectado == "historia":
            response_text += f"### {respuesta_base['titulo']}\n{respuesta_base['contenido']}"
            sugerencias = ["Ver Deuda Actual", "Situación Talara"]

        else:
            # FALLBACK INTELIGENTE (COMO GEMINI)
            response_text += f"Entiendo tu consulta. Basado en mi base de datos integral sobre Petroperú, puedo ofrecerte análisis en tres ejes clave:\n\n"
            response_text += "1.  **Financiero:** Deuda de $8.5B y problemas de liquidez.\n"
            response_text += "2.  **Operativo:** Nueva Refinería Talara y Oleoducto.\n"
            response_text += "3.  **Histórico:** Evolución desde 1969 hasta hoy.\n\n"
            response_text += f"*Actualmente estoy calculando escenarios con un WTI de ${ctx['wti_precio']}. ¿Sobre qué tema deseas profundizar?*"
            sugerencias = ["Situación Financiera", "Estado de Talara", "Historia"]

        return {
            "texto": response_text,
            "visual": visual,
            "sugerencias": sugerencias
        }

    # --- GENERADORES GRÁFICOS DINÁMICOS ---
    def _generar_grafico_ebitda(self):
        wti = st.session_state.contexto_ia['wti_precio']
        # Simulación: EBITDA mejora si WTI sube (margen teórico) pero caja sufre
        base = 100 + (wti - 70) * 1.5
        vals = [base * 0.9, base, base * 1.1]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Pesimista', 'Base', 'Optimista'],
            y=vals,
            marker_color=['#EF4444', '#3B82F6', '#10B981'],
            text=[f"${v:.0f}M" for v in vals],
            textposition='auto'
        ))
        fig.update_layout(title=f"Proyección EBITDA Trimestral (WTI ${wti})", template="plotly_dark", 
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        return fig

    def _generar_grafico_waterfall(self):
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Presupuesto 2014", "Adicionales EPC", "Gastos Financieros", "Costo Final"],
            y=[1300, 3800, 3400, 0],
            connector={"line": {"color": "white"}},
            decreasing={"marker": {"color": "green"}},
            increasing={"marker": {"color": "#F43F5E"}},
            totals={"marker": {"color": "#38BDF8"}}
        ))
        fig.update_layout(title="Desviación de Costos NRT (Millones USD)", template="plotly_dark", 
                          paper_bgcolor='rgba(0,0,0,0)', height=300)
        return fig

brain = PetrolitoBrain()

# ==============================================================================
# 3. GESTIÓN DEL CHAT E INTERACTIVIDAD
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Mensaje de Bienvenida "Gemini-Style"
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": {
            "texto": (
                "👋 **Hola. Soy Petrolito AI.**\n\n"
                "He cargado mi núcleo con toda la información histórica, financiera y técnica de Petroperú. "
                "Tengo capacidad de **razonamiento contextual**, lo que significa que puedo actualizar mis proyecciones si tú me das nuevos datos de mercado.\n\n"
                "💡 *Pruébame preguntando: 'Explícame el problema de la deuda' o 'El WTI subió a 90'.*"
            ),
            "visual": None,
            "sugerencias": ["Analizar Deuda", "Ver Historia", "Estatus Operativo"]
        }
    })

def procesar_clic(texto):
    st.session_state.mensajes.append({"role": "user", "content": texto})

# ==============================================================================
# 4. RENDERIZADO (UI/UX)
# ==============================================================================

# Título Flotante
st.markdown("<h1 style='text-align:center; color:#E2E8F0; margin-bottom:10px;'>🧠 Petroperú <span style='color:#38BDF8'>Intelligence</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#94A3B8; font-size:14px;'>Datos en Memoria: WTI <b>${st.session_state.contexto_ia['wti_precio']}</b> | NRT <b>{st.session_state.contexto_ia['produccion_nrt']} kbd</b></p>", unsafe_allow_html=True)

# Loop de Mensajes
for i, msg in enumerate(st.session_state.mensajes):
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        # Cuerpo del mensaje
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:15px;">
                <span style="font-size:24px; margin-right:12px;">🤖</span>
                <span style="font-weight:700; color:#38BDF8; font-size:18px;">PETROLITO AI</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Elementos Visuales
        if pkg["visual"]:
            st.plotly_chart(pkg["visual"], use_container_width=True)
            
        # Sugerencias Interactivas (Solo en el último mensaje)
        if pkg["sugerencias"] and i == len(st.session_state.mensajes) - 1:
            cols = st.columns(len(pkg["sugerencias"]) + 2)
            for idx, sug in enumerate(pkg["sugerencias"]):
                if cols[idx].button(sug, key=f"btn_{i}_{idx}"):
                    procesar_clic(sug)
                    st.rerun()

# ==============================================================================
# 5. INPUT Y PROCESAMIENTO
# ==============================================================================

if prompt := st.chat_input("Escribe tu consulta o actualiza un dato (ej: 'WTI a 85')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

# Lógica de Respuesta
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("🧠 Analizando vectores de información y recalculando modelos..."):
        time.sleep(0.7) # Latencia para sensación de procesamiento
        
        usuario_texto = st.session_state.mensajes[-1]["content"]
        respuesta_ia = brain.razonar(usuario_texto)
        
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta_ia})
        st.rerun()
