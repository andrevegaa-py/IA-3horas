import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO GPT-4 ENTERPRISE)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Senior Analyst",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para inmersión total y lectura profesional
st.markdown("""
<style>
    /* Layout Limpio */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 8rem !important;
        max-width: 900px !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0F172A; /* Dark Slate Blue */
    }
    
    /* Burbujas de Chat Profesionales */
    .chat-bubble {
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        line-height: 1.7;
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        font-size: 16px;
        color: #E2E8F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .user-bubble {
        background-color: #334155; /* Slate 700 */
        border: 1px solid #475569;
        margin-left: 20%;
        text-align: right;
    }
    
    .bot-bubble {
        background-color: #1E293B; /* Slate 800 */
        border-left: 4px solid #10B981; /* Verde GPT */
    }

    /* Formato de Texto Avanzado */
    .bot-bubble h3 { color: #34D399 !important; margin-top: 0; font-size: 20px; font-weight: 700; }
    .bot-bubble strong { color: #38BDF8; font-weight: 600; }
    .bot-bubble ul { margin-bottom: 15px; padding-left: 20px; }
    .bot-bubble li { margin-bottom: 8px; }
    .kpi-box { background: rgba(16, 185, 129, 0.1); padding: 2px 6px; border-radius: 4px; color: #34D399; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.2); }
    .alert-box { background: rgba(239, 68, 68, 0.1); padding: 2px 6px; border-radius: 4px; color: #F87171; font-weight: bold; border: 1px solid rgba(239, 68, 68, 0.2); }

    /* Input Flotante */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px !important;
        z-index: 9999;
    }
    
    /* Ocultar elementos innecesarios */
    header, footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO FINANCIERO AVANZADO (LÓGICA DIRECTA)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 76.5,          # Precio Barril Real
        "produccion": 95.0,   # Producción NRT
        "deuda_total": 8500,  # Millones USD
        "deficit_caja": 2200, # Capital de Trabajo Negativo
        "ebitda_meta": 667    # Proyección 2025
    }

class PetrolitoBrain:
    def __init__(self):
        # Base de Datos de Archivos Reales
        self.files_db = pd.DataFrame({
            "Documento": ["Estados Financieros Auditados 2023 (PwC)", "Clasificación de Riesgo (Fitch/Apoyo)", "Plan de Reestructuración 2025"],
            "Fecha": ["Mayo 2024", "Junio 2024", "Dic 2024"],
            "Hallazgo Clave": ["Pérdida Neta -$822M", "Rating 'CCC+' (Junk)", "Meta EBITDA +$667M"]
        })

    # --- 1. APRENDIZAJE SILENCIOSO (ACTUALIZA SIN MOLESTAR) ---
    def actualizar_memoria(self, prompt):
        prompt = prompt.lower()
        msg = ""
        
        # Detectar WTI
        match_wti = re.search(r'(wti|precio|barril).*?(\d{2,3})', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memoria['wti'] = val
            # Recalcular proyecciones automáticamente
            st.session_state.memoria['ebitda_meta'] = 667 + (val - 76.5) * 15 
            msg = f"🔄 *He recalibrado mis modelos financieros con un WTI de ${val}.*"

        # Detectar Producción
        match_prod = re.search(r'(producci|carga|refin).*?(\d{2,3})', prompt)
        if match_prod:
            val = float(match_prod.group(2))
            st.session_state.memoria['produccion'] = val
            msg = f"🔄 *Modelo operativo ajustado a {val} KBPD.*"
            
        return msg

    # --- 2. GENERACIÓN DE VISUALES (PLOTLY) ---
    def crear_grafico(self, tipo):
        mem = st.session_state.memoria
        
        if tipo == "deuda_breakdown":
            fig = go.Figure(go.Pie(
                labels=['Bonos (Largo Plazo)', 'Crédito España (CESCE)', 'Déficit Capital Trabajo', 'Otros'],
                values=[3000, 1300, 2200, 2000],
                hole=0.4,
                marker_colors=['#3B82F6', '#8B5CF6', '#EF4444', '#64748B']
            ))
            fig.update_layout(title="<b>Estructura de Deuda ($8.5B)</b>", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=40,b=20,l=20,r=20))
            return fig

        elif tipo == "waterfall_ebitda":
            # Proyección generativa
            base_2023 = -104
            recuperacion_ops = 400
            efecto_precio = (mem['wti'] - 70) * 10
            meta_final = base_2023 + recuperacion_ops + efecto_precio + 200 # Ajuste eficiencia
            
            fig = go.Figure(go.Waterfall(
                orientation="v", measure=["relative", "relative", "relative", "relative", "total"],
                x=["Real 2023", "Eficiencia Ops", "Impacto WTI", "Optimización", "Proyección 2025"],
                y=[base_2023, recuperacion_ops, efecto_precio, 200, 0],
                connector={"line":{"color":"white"}},
                decreasing={"marker":{"color":"#EF4444"}}, increasing={"marker":{"color":"#10B981"}}, totals={"marker":{"color":"#3B82F6"}}
            ))
            fig.update_layout(title=f"<b>Drivers EBITDA 2025 (WTI ${mem['wti']})</b>", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=40,b=20,l=20,r=20))
            return fig

        elif tipo == "eficiencia_nrt":
            val = (mem['produccion'] / 95) * 100
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = val, title = {'text': "Utilización NRT (%)"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#10B981" if val > 90 else "#F59E0B"}}
            ))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=30,b=20,l=20,r=20))
            return fig

        return None

    # --- 3. CEREBRO DE RESPUESTA DIRECTA (SENIOR ANALYST) ---
    def generar_respuesta(self, prompt):
        prompt_low = prompt.lower()
        mem = st.session_state.memoria
        
        # Actualización silenciosa
        feedback = self.actualizar_memoria(prompt)
        header = f"{feedback}\n\n" if feedback else ""
        
        response = {"texto": "", "visual": None, "extra_visual": None}

        # --- INTENCIÓN: FINANZAS / DEUDA / CAJA ---
        if any(x in prompt_low for x in ["deuda", "dinero", "caja", "bonos", "financiera", "situacion"]):
            liquidez_status = "CRÍTICO" if mem['deficit_caja'] > 1500 else "ESTABLE"
            
            response["texto"] = (
                f"{header}### 📉 Análisis de Posición Financiera\n"
                f"La situación es compleja pero estructurada. Al cierre auditado, enfrentamos una deuda total de **$8.5 Billones**.\n\n"
                f"El punto de dolor no son los Bonos (que vencen en 2032/2047), sino el **Capital de Trabajo**. "
                f"Actualmente tenemos un <span class='alert-box'>Déficit de Caja de ${mem['deficit_caja']} Millones</span>. "
                f"Esto significa que nuestras obligaciones a corto plazo (pagos a proveedores de crudo) superan nuestros activos líquidos inmediatos.\n\n"
                f"**Estrategia en curso:** El MEF está otorgando garantías para permitir líneas de crédito revolventes mientras la Refinería alcanza flujo positivo."
            )
            response["visual"] = self.crear_grafico("deuda_breakdown")
            return response

        # --- INTENCIÓN: PROYECCIONES / FUTURO / 2025 ---
        if any(x in prompt_low for x in ["proyeccion", "futuro", "2025", "ebitda", "ganancia", "meta"]):
            ebitda_calc = int(mem['ebitda_meta'])
            
            response["texto"] = (
                f"{header}### 🚀 Outlook 2025: Camino a la Rentabilidad\n"
                f"Basado en los fundamentales actuales y tu escenario de **WTI ${mem['wti']}**, proyectamos un cambio de tendencia radical.\n\n"
                f"La meta oficial es revertir las pérdidas de 2023 (-$822M) y alcanzar un <span class='kpi-box'>EBITDA Positivo de ${ebitda_calc} Millones</span> en 2025.\n"
                f"Este salto se sustenta en tres pilares:\n"
                f"1. Operación plena de la Unidad de Flexicoking (margen >$10/bbl).\n"
                f"2. Reducción de importación de combustibles refinados.\n"
                f"3. Estabilización del tipo de cambio."
            )
            response["visual"] = self.crear_grafico("waterfall_ebitda")
            return response

        # --- INTENCIÓN: OPERACIONES / TALARA ---
        if any(x in prompt_low for x in ["talara", "nrt", "refineria", "operacion", "produccion", "carga"]):
            utilizacion = int((mem['produccion'] / 95) * 100)
            
            response["texto"] = (
                f"{header}### 🏭 Nueva Refinería Talara (NRT)\n"
                f"El activo más importante de la empresa está operando con una carga de **{mem['produccion']} KBPD**.\n\n"
                f"Esto representa un factor de utilización del <span class='kpi-box'>{utilizacion}%</span>. "
                f"Técnicamente, la refinería ya completó su periodo de arranque. El reto ahora es **logístico**: "
                f"asegurar el suministro continuo de crudo pesado para alimentar la unidad de Flexicoking y maximizar el margen de refino."
            )
            response["visual"] = self.crear_grafico("eficiencia_nrt")
            return response

        # --- INTENCIÓN: ARCHIVOS / DATOS DUROS ---
        if any(x in prompt_low for x in ["archivo", "reporte", "excel", "pdf", "descargar"]):
            response["texto"] = "### 📂 Repositorio Oficial\nHe extraído los documentos clave directamente de la base de datos financiera:"
            response["extra_visual"] = self.files_db
            return response

        # --- DEFAULT: CAPACIDAD GENERATIVA ---
        # Si no encaja en nada específico, responde con inteligencia general usando las variables
        response["texto"] = (
            f"{header}Soy **Petrolito AI**. Mi análisis integral indica lo siguiente:\n\n"
            f"Con un precio de petróleo en **${mem['wti']}**, tenemos una oportunidad única para maximizar los ingresos de la Nueva Refinería Talara, "
            f"siempre que mantengamos la producción por encima de los **{mem['produccion']} KBPD**.\n\n"
            f"El riesgo principal sigue siendo la liquidez de corto plazo (-$2.2B). "
            f"¿Deseas que profundice en la **Estrategia de Deuda** o en las **Proyecciones de Flujo**?"
        )
        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. MOTOR DE CHAT (STREAMLIT)
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Mensaje inicial directo
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": {
            "texto": "👋 **Hola. Soy Petrolito AI.**\n\nEstoy conectado a la data auditada de Petroperú. Puedo analizar **Deuda**, **Operaciones** o **Proyecciones**.\nNo necesitas menús. Simplemente pregúntame lo que necesitas saber.",
            "visual": None, "extra_visual": None
        }
    })

# Renderizado del Chat
st.markdown("<h2 style='text-align:center;'>🧠 Petrolito <span style='color:#34D399;'>Direct Core</span></h2>", unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:15px;">
                <span style="font-size:24px; margin-right:12px;">🤖</span>
                <span style="font-weight:700; color:#34D399;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Renderizado de Gráficos Integrado en la respuesta (Directo, sin pedirlo)
        if pkg["visual"]:
            st.plotly_chart(pkg["visual"], use_container_width=True)
        if pkg["extra_visual"] is not None:
            st.dataframe(pkg["extra_visual"], use_container_width=True, hide_index=True)

# Input y Lógica
if prompt := st.chat_input("Pregunta directamente (Ej: 'Dame la proyección 2025' o 'Analiza la deuda')"):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Procesando análisis..."):
        time.sleep(0.5) # Velocidad GPT
        resp = brain.generar_respuesta(st.session_state.mensajes[-1]["content"])
        st.session_state.mensajes.append({"role": "assistant", "content": resp})
        st.rerun()
