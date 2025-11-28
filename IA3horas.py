import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re
import random

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO CHATGPT FLUIDO)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito GenAI | Enterprise Core",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para interfaz de Chat Avanzada
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 8rem !important; max-width: 900px !important; }
    [data-testid="stAppViewContainer"] { background-color: #0B0F19; } /* Deep Night Blue */
    
    /* Burbujas de Chat Dinámicas */
    .chat-bubble {
        padding: 20px 24px;
        border-radius: 18px;
        margin-bottom: 20px;
        line-height: 1.65;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    .user-bubble {
        background: linear-gradient(135deg, #334155 0%, #1E293B 100%);
        border: 1px solid #475569;
        color: #F8FAFC;
        margin-left: 20%;
        text-align: right;
        border-bottom-right-radius: 4px;
    }
    
    .bot-bubble {
        background: #151B2B;
        border-left: 4px solid #10B981; /* Verde GenAI */
        color: #E2E8F0;
        margin-right: 5%;
        border-bottom-left-radius: 4px;
    }

    /* Tipografía y Elementos */
    .bot-bubble h3 { color: #34D399 !important; margin: 0 0 12px 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
    .bot-bubble strong { color: #38BDF8; font-weight: 600; }
    .bot-bubble .metric-highlight { background: rgba(16, 185, 129, 0.1); color: #34D399; padding: 2px 8px; border-radius: 6px; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.2); }
    .bot-bubble .alert-highlight { background: rgba(239, 68, 68, 0.1); color: #F87171; padding: 2px 8px; border-radius: 6px; font-weight: bold; border: 1px solid rgba(239, 68, 68, 0.2); }

    /* Input Flotante Moderno */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px !important;
        z-index: 9999;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO GENERATIVO (PETROLITO GEN-CORE)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 76.5,          # Precio Barril (Variable de Estado)
        "produccion": 95.0,   # Producción NRT
        "ebitda_proy": 667,   # Meta 2025
        "deuda_total": 8500,  # Deuda Real
        "contexto_previo": None # Memoria de Corto Plazo
    }

class PetrolitoGenAI:
    def __init__(self):
        # --- MAPA SEMÁNTICO (TRADUCTOR 1 PALABRA -> INTENCIÓN) ---
        self.intent_map = {
            "finanzas": ["deuda", "bonos", "dinero", "plata", "caja", "ebitda", "flujo", "financiero", "balance", "gastos", "pagos"],
            "operaciones": ["talara", "nrt", "refineria", "oleoducto", "produccion", "carga", "barriles", "planta", "flexicoking"],
            "proyecciones": ["futuro", "2025", "proyeccion", "meta", "objetivo", "ganancia", "estimado"],
            "archivos": ["archivo", "pdf", "excel", "descargar", "reporte", "documento", "data", "auditado"],
            "saludo": ["hola", "buenas", "inicio", "empezar", "hello", "hi"]
        }
        
        # Base de Conocimiento Real (Auditada)
        self.knowledge = {
            "finanzas": {
                "titulo": "Estado de Situación Financiera",
                "cuerpo_base": "La estructura de capital enfrenta un desafío de liquidez inmediato. El déficit de capital de trabajo es de -$2,200 Millones. Sin embargo, los Bonos Soberanos ($3,000 MM) tienen vencimientos a largo plazo (2032/2047), lo que nos da aire en el perfil de maduración.",
            },
            "operaciones": {
                "titulo": "Panorama Operativo (NRT)",
                "cuerpo_base": "La Nueva Refinería Talara es el activo principal. Con la unidad de Flexicoking operativa, maximizamos el margen procesando crudos pesados. El Oleoducto Norperuano sigue siendo el cuello de botella logístico debido a contingencias externas.",
            }
        }

    # --- 1. MOTOR DE APRENDIZAJE CONTINUO ---
    def procesar_aprendizaje(self, prompt):
        """Detecta cambios de variables en el flujo de la conversación."""
        prompt = prompt.lower()
        msg_learning = []
        
        # Detector WTI (ej: "WTI 80", "Precio 90")
        match_wti = re.search(r'(wti|precio|barril).*?(\d{2,3})', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memoria['wti'] = val
            st.session_state.memoria['ebitda_proy'] = 667 + (val - 76.5) * 15 # Recalcula EBITDA dinámicamente
            msg_learning.append(f"WTI a ${val}")

        # Detector Producción (ej: "Prod 90", "Carga 100")
        match_prod = re.search(r'(producci|carga).*?(\d{2,3})', prompt)
        if match_prod:
            val = float(match_prod.group(2))
            st.session_state.memoria['produccion'] = val
            msg_learning.append(f"Producción a {val}k")

        return msg_learning

    # --- 2. GENERADOR DE VISUALES (EN TIEMPO REAL) ---
    def generar_grafico(self, tipo):
        mem = st.session_state.memoria
        
        if tipo == "waterfall_ebitda":
            # Gráfico dinámico basado en WTI aprendido
            base = 150 # Est 2024
            impacto_wti = (mem['wti'] - 70) * 20
            impacto_ops = (mem['produccion'] - 80) * 10
            final = base + impacto_wti + impacto_ops
            
            fig = go.Figure(go.Waterfall(
                orientation="v", measure=["relative", "relative", "relative", "total"],
                x=["Base 2024", "Efecto WTI", "Eficiencia NRT", "Proyección 2025"],
                y=[base, impacto_wti, impacto_ops, 0],
                connector={"line":{"color":"white"}},
                decreasing={"marker":{"color":"#F43F5E"}}, increasing={"marker":{"color":"#10B981"}}, totals={"marker":{"color":"#3B82F6"}}
            ))
            fig.update_layout(title=f"Drivers del EBITDA (WTI ${mem['wti']})", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=280)
            return fig

        elif tipo == "deuda_pie":
            fig = go.Figure(go.Pie(
                labels=['Bonos (Largo Plazo)', 'Crédito España (CESCE)', 'Déficit Caja (Corto Plazo)'],
                values=[3000, 1300, 2200],
                hole=0.5, marker_colors=['#3B82F6', '#8B5CF6', '#EF4444']
            ))
            fig.update_layout(title="Composición Deuda $8.5B", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=280)
            return fig
            
        return None

    # --- 3. NÚCLEO DE RAZONAMIENTO (GENERATIVO) ---
    def generar_respuesta(self, prompt):
        prompt_low = prompt.lower()
        mem = st.session_state.memoria
        
        # A. Aprender primero
        cambios = self.procesar_aprendizaje(prompt)
        header_msg = ""
        if cambios:
            header_msg = f"📝 *He actualizado mi memoria: {', '.join(cambios)}. Recalculando escenarios...*\n\n"

        # B. Identificar Intención (Fuzzy Matching)
        intencion = "general"
        
        # Buscamos en el diccionario de sinónimos
        for key, keywords in self.intent_map.items():
            if any(word in prompt_low for word in keywords):
                intencion = key
                break
        
        # Contexto Persistente (Si el usuario dice solo "¿Y qué hacemos?", usa el tema anterior)
        if intencion == "general" and mem['contexto_previo']:
             # Si la frase es muy corta (< 4 palabras) y hay contexto, asumimos continuidad
             if len(prompt.split()) < 4:
                 intencion = mem['contexto_previo']

        # Guardar contexto para la siguiente vuelta
        st.session_state.memoria['contexto_previo'] = intencion

        # C. Construcción de Respuesta Generativa
        response = {"texto": "", "visual": None}

        # --- ESCENARIO: FINANZAS ---
        if intencion == "finanzas":
            estado_caja = "crítico" if mem['wti'] < 70 else "en recuperación"
            clase_alerta = "alert-highlight" if mem['wti'] < 70 else "metric-highlight"
            
            response["texto"] = (
                f"{header_msg}### 📉 Análisis Financiero Dinámico\n"
                f"Analizando tu escenario actual con **WTI a ${mem['wti']}**, la posición de caja se encuentra <span class='{clase_alerta}'>{estado_caja}</span>.\n\n"
                f"La deuda total se mantiene en **$8.5 Billones**, pero el déficit de capital de trabajo (-$2.2B) es la prioridad. "
                f"Con este precio de crudo, nuestro margen mejora, permitiendo cubrir mejor los intereses de los Bonos 2032.\n\n"
                f"**¿Te gustaría simular una reestructuración de deuda o ver el impacto en el EBITDA?**"
            )
            response["visual"] = self.generar_grafico("deuda_pie")

        # --- ESCENARIO: OPERACIONES (TALARA) ---
        elif intencion == "operaciones":
            eficiencia = int((mem['produccion'] / 95) * 100)
            status_nrt = "Óptima" if eficiencia > 90 else "Subutilizada"
            
            response["texto"] = (
                f"{header_msg}### 🏭 Estado Operativo: Nueva Refinería Talara\n"
                f"Con una carga de **{mem['produccion']} KBPD**, la refinería opera al <span class='metric-highlight'>{eficiencia}% de capacidad</span> ({status_nrt}).\n\n"
                f"El *Flexicoking* está procesando residuales a plena carga. Este nivel de producción es clave para diluir los costos fijos. "
                f"Si logramos mantener este ritmo, el costo unitario de refinación bajará a niveles competitivos de **$8/bbl**.\n\n"
                f"**¿Quieres ver el desglose de márgenes por barril?**"
            )
            # Aquí podríamos poner otro gráfico si quisiéramos
            
        # --- ESCENARIO: PROYECCIONES 2025 ---
        elif intencion == "proyecciones":
            ebitda_calc = int(mem['ebitda_proy'])
            delta = ebitda_calc - 667
            signo = "+" if delta >= 0 else ""
            
            response["texto"] = (
                f"{header_msg}### 🚀 Proyección Generativa 2025\n"
                f"Basado en tus inputs y la data oficial, he simulado el cierre del 2025:\n\n"
                f"* **EBITDA Proyectado:** <span class='metric-highlight'>${ebitda_calc} Millones</span> ({signo}{int(delta)} vs Meta Oficial).\n"
                f"* **Flujo de Caja:** Se estima superar los $5,000 Millones en ingresos operativos.\n"
                f"* **Pérdida Neta:** Reducción sustancial del déficit.\n\n"
                f"El gráfico a continuación muestra cómo el **Precio WTI (${mem['wti']})** y la **Eficiencia Operativa** construyen este resultado:"
            )
            response["visual"] = self.generar_grafico("waterfall_ebitda")

        # --- ESCENARIO: ARCHIVOS ---
        elif intencion == "archivos":
            df_files = pd.DataFrame({
                "Documento": ["EEFF Auditados 2023 (PwC)", "Proyecciones 2025 Oficiales", "Reporte Deuda"],
                "Enlace": ["Descargar PDF", "Descargar XLSX", "Descargar PDF"]
            })
            response["texto"] = "### 📂 Data Room Seguro\nAccediendo al repositorio. Aquí tienes los reportes oficiales listos para descarga:"
            # Pasamos el dataframe como visual especial
            response["visual"] = df_files 
            response["visual_type"] = "table"

        # --- ESCENARIO: SALUDO / DESCONOCIDO ---
        else:
            response["texto"] = (
                f"{header_msg}👋 **Hola. Soy Petrolito GenAI.**\n\n"
                f"Mi cerebro está conectado a la data financiera de Petroperú. "
                f"Actualmente mis simulaciones corren con **WTI ${mem['wti']}** y **Prod {mem['produccion']}k**.\n\n"
                f"**Pruébame con una sola palabra:**\n"
                f"🔹 Escribe **'Deuda'** para ver el análisis de pasivos.\n"
                f"🔹 Escribe **'Proyección'** para ver el futuro financiero.\n"
                f"🔹 O enséñame: **'El WTI subió a 90'**."
            )

        return response

brain = PetrolitoGenAI()

# ==============================================================================
# 3. INTERFAZ DE CHAT (LOOP PRINCIPAL)
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Mensaje Inicial
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": brain.generar_respuesta("saludo") # Generamos el saludo dinámicamente
    })

# RENDERIZADO
st.markdown("<h2 style='text-align:center; margin-bottom: 30px;'>🧠 Petroperú <span style='color:#10B981;'>Gen-Core</span></h2>", unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:15px;">
                <span style="font-size:24px; margin-right:12px;">🤖</span>
                <span style="font-weight:700; color:#10B981; font-size:18px;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # Renderizado Inteligente de Visuales
        if pkg["visual"] is not None:
            with st.container():
                if isinstance(pkg["visual"], go.Figure):
                    st.plotly_chart(pkg["visual"], use_container_width=True)
                elif isinstance(pkg["visual"], pd.DataFrame):
                    st.dataframe(pkg["visual"], use_container_width=True, hide_index=True)

# INPUT
if prompt := st.chat_input("Escribe 'Deuda', 'Talara' o actualiza datos (Ej: 'WTI 85')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

# RESPUESTA AUTOMÁTICA
if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Generando análisis..."):
        time.sleep(0.4) # Respuesta rápida tipo GPT
        
        user_text = st.session_state.mensajes[-1]["content"]
        respuesta_ia = brain.generar_respuesta(user_text)
        
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta_ia})
        st.rerun()
