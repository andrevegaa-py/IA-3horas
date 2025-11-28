import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (ESTILO ENTERPRISE DARK)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Financial Core",
    layout="wide",
    page_icon="📉",
    initial_sidebar_state="collapsed"
)

# CSS Avanzado
st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 8rem !important; max-width: 950px !important; }
    [data-testid="stAppViewContainer"] { background-color: #0B0F19; }
    
    .chat-bubble { padding: 25px; border-radius: 12px; margin-bottom: 25px; line-height: 1.7; font-family: 'Segoe UI', sans-serif; font-size: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .user-bubble { background-color: #1E293B; border: 1px solid #334155; color: #F8FAFC; margin-left: 20%; text-align: right; }
    .bot-bubble { background-color: #111827; border-left: 4px solid #E11D48; color: #CBD5E1; margin-right: 5%; }
    
    .bot-bubble h3 { color: #FB7185 !important; margin: 0 0 15px 0; font-size: 21px; font-weight: 700; letter-spacing: 0.5px; }
    .bot-bubble strong { color: #38BDF8; font-weight: 600; }
    .metric-badge { background: rgba(56, 189, 248, 0.1); color: #38BDF8; padding: 2px 8px; border-radius: 4px; font-weight: bold; border: 1px solid rgba(56, 189, 248, 0.2); }
    .warning-badge { background: rgba(244, 63, 94, 0.1); color: #F43F5E; padding: 2px 8px; border-radius: 4px; font-weight: bold; border: 1px solid rgba(244, 63, 94, 0.2); }

    .stChatInput { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 800px !important; z-index: 9999; }
    header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO FINANCIERO EXTENDIDO (DATA MACRO & PETROPERÚ)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 75.0,
        "tipo_cambio": 3.75, # PEN/USD
        "riesgo_pais": 160,  # Puntos básicos (Peru)
        "produccion": 95.0,
        "ebitda_meta": 667
    }

class PetrolitoBrain:
    def __init__(self):
        # Base de Datos Financiera Profunda
        self.knowledge = {
            "macro_peru": """
            **🌍 Contexto Macroeconómico Perú:**
            * **Riesgo Cambiario:** Petroperú tiene un descalce estructural. Compra crudo e insumos en Dólares (USD), pero el 70% de sus ingresos son en Soles (PEN) por ventas locales.
            * **Impacto FX:** Una devaluación del Sol incrementa automáticamente el servicio de la deuda y las pérdidas por diferencia de cambio.
            * **Riesgo País (EMBI+):** Actualmente el riesgo soberano de Perú afecta la tasa a la que Petroperú puede refinanciar. Al perder el Grado de Inversión (actualmente 'Junk' CCC+), el costo financiero se dispara por encima del 11-12%.
            """,
            
            "deuda_profunda": """
            **📉 Radiografía de la Crisis Financiera:**
            * **Patrimonio Neto:** Se ha reducido drásticamente debido a las pérdidas acumuladas (-$822M en 2023).
            * **Soporte Estatal (DU 013-2024):** El MEF ha tenido que intervenir con garantías para líneas de crédito ($800M) y capitalizaciones de deuda tributaria, ya que la banca privada cerró el grifo de liquidez (Líneas Revolventes).
            * **Bonos Soberanos:** Emitidos en 2017 y 2021. No tienen vencimientos inmediatos, pero sus cupones (intereses) absorben el poco flujo operativo disponible.
            """,
            
            "reestructuracion": """
            **🛠️ Plan de Reestructuración (PMO):**
            * Se ha contratado una Oficina de Gestión de Proyectos (PMO) privada para despolitizar la gestión.
            * **Venta de Activos:** Se evalúa la venta de inmuebles no operativos (Edificio Central) y unidades auxiliares.
            * **Austeridad:** Recorte de gastos administrativos en un 30% y optimización de la planilla.
            """
        }
        
        self.files_db = pd.DataFrame({
            "Reporte Técnico": [
                "EEFF Auditados 2023 (Dictamen Negativo)", 
                "Análisis de Sostenibilidad de Deuda (MEF)", 
                "Plan de Reestructuración (Arthur D. Little)",
                "Evaluación Crediticia Fitch/S&P 2024"
            ],
            "Fecha": ["Mayo 2024", "Junio 2024", "Julio 2024", "Agosto 2024"],
            "KPI Clave": [
                "Pérdida Neta -$822M",
                "Ratio Deuda/EBITDA > 15x",
                "Meta Ahorro $100M/año",
                "Downgrade a CCC+"
            ]
        })

    # --- MOTOR DE ACTUALIZACIÓN ---
    def actualizar(self, prompt):
        prompt = prompt.lower()
        msg = ""
        
        # WTI
        match_wti = re.search(r'(wti|precio).*?(\d{2,3})', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memoria['wti'] = val
            msg = f"🔄 *WTI ajustado a ${val}. Impacto en márgenes recalculado.*"

        # Tipo de Cambio
        match_tc = re.search(r'(cambio|dolar|sol).*?(\d{1}\.\d{2})', prompt)
        if match_tc:
            val = float(match_tc.group(2))
            st.session_state.memoria['tipo_cambio'] = val
            msg = f"🔄 *Tipo de Cambio ajustado a S/. {val}. Impacto FX recalculado.*"
            
        return msg

    # --- GENERADOR DE GRÁFICOS (LETRAS BLANCAS FORZADAS) ---
    def generar_grafico(self, tipo):
        mem = st.session_state.memoria
        
        # Configuración común para TODO gráfico: LETRAS BLANCAS
        layout_common = dict(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family="Segoe UI"), # FORZAR BLANCO
            title_font=dict(color='white', size=18),
            xaxis=dict(tickfont=dict(color='white'), title_font=dict(color='white'), gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(tickfont=dict(color='white'), title_font=dict(color='white'), gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(font=dict(color='white')),
            margin=dict(l=20, r=20, t=50, b=20),
            height=300
        )

        if tipo == "evolucion_patrimonio":
            years = ['2019', '2020', '2021', '2022', '2023', '2024 (Est)']
            # Datos aproximados reales (caída de patrimonio)
            patrimonio = [2800, 2600, 2400, 1900, 1100, 800] # Millones USD (Simulación basada en pérdidas)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years, y=patrimonio, mode='lines+markers', fill='tozeroy',
                line=dict(color='#F43F5E', width=3), marker=dict(size=8), name='Patrimonio Neto'
            ))
            fig.update_layout(title="📉 Destrucción de Patrimonio Neto (MM USD)", **layout_common)
            return fig

        elif tipo == "sensibilidad_fx":
            # Gráfico de impacto del Dólar en la Deuda
            tc_base = mem['tipo_cambio']
            tcs = [tc_base - 0.2, tc_base, tc_base + 0.2]
            deuda_soles = [8500 * tc for tc in tcs] # Deuda en soles equivalente
            
            fig = go.Figure(go.Bar(
                x=[f"S/. {tc:.2f}" for tc in tcs],
                y=deuda_soles,
                marker_color=['#10B981', '#3B82F6', '#EF4444'],
                text=[f"S/. {v:,.0f}M" for v in deuda_soles], textposition='auto'
            ))
            fig.update_layout(title=f"Impacto Tipo de Cambio en Deuda Total (Soles)", **layout_common)
            return fig

        elif tipo == "deuda_vencimientos":
            fig = go.Figure(go.Bar(
                x=['2024', '2025', '2026', '2027', '2032 (Bono)', '2047 (Bono)'],
                y=[2200, 800, 600, 500, 1000, 2000],
                marker_color='#38BDF8'
            ))
            fig.update_layout(title="Perfil de Vencimientos de Deuda (MM USD)", **layout_common)
            # Anotación para el corto plazo
            fig.add_annotation(x='2024', y=2200, text="Capital de Trabajo (Crítico)", showarrow=True, arrowhead=1, ax=0, ay=-40, font=dict(color='white'))
            return fig

        return None

    # --- RESPUESTA INTELIGENTE ---
    def generar_respuesta(self, prompt):
        prompt_low = prompt.lower()
        feedback = self.actualizar(prompt)
        header = f"{feedback}\n\n" if feedback else ""
        
        response = {"texto": "", "visual": None, "extra": None}

        # TEMA: SITUACIÓN FINANCIERA / PATRIMONIO
        if any(x in prompt_low for x in ["financiera", "patrimonio", "quiebra", "perdidas", "balance"]):
            response["texto"] = (
                f"{header}### 📉 Análisis de Solvencia y Patrimonio\n"
                f"{self.knowledge['deuda_profunda']}\n\n"
                f"La situación es crítica. El patrimonio de la empresa se ha erosionado debido a las pérdidas operativas y financieras consecutivas. "
                f"Actualmente, el ratio **Deuda/EBITDA supera las 15x**, muy por encima del límite saludable de 3x-4x.\n\n"
                f"El gráfico a continuación muestra cómo se ha contraído el valor patrimonial de la empresa en los últimos 5 años:"
            )
            response["visual"] = self.generar_grafico("evolucion_patrimonio")

        # TEMA: MACROECONOMÍA / TIPO DE CAMBIO
        elif any(x in prompt_low for x in ["macro", "dolar", "sol", "cambio", "riesgo pais", "mercado"]):
            response["texto"] = (
                f"{header}### 🌍 Exposición Macroeconómica\n"
                f"{self.knowledge['macro_peru']}\n\n"
                f"Con tu Tipo de Cambio actual de **S/. {st.session_state.memoria['tipo_cambio']}**, enfrentamos un riesgo severo.\n"
                f"Dado que la deuda ($8.5B) está en Dólares, pero gran parte de la venta de combustibles es en Soles, cualquier subida del dólar infla nuestra deuda en moneda local y genera pérdidas contables masivas."
            )
            response["visual"] = self.generar_grafico("sensibilidad_fx")

        # TEMA: REESTRUCTURACIÓN / FUTURO
        elif any(x in prompt_low for x in ["futuro", "plan", "solucion", "pmo", "reestructuracion"]):
            response["texto"] = (
                f"{header}### 🛠️ Plan de Rescate y Reestructuración\n"
                f"{self.knowledge['reestructuracion']}\n\n"
                f"El objetivo central es recuperar el **Grado de Inversión** a largo plazo. Sin embargo, en el corto plazo (2024-2025), la prioridad es:\n"
                f"1. Refinanciar las líneas de corto plazo (Capital de Trabajo).\n"
                f"2. Lograr que la NRT opere a plena carga sin paradas.\n"
                f"3. Vender activos no estratégicos para generar caja."
            )
            response["visual"] = self.generar_grafico("deuda_vencimientos")

        # TEMA: ARCHIVOS
        elif any(x in prompt_low for x in ["archivo", "reporte", "informe", "pdf"]):
            response["texto"] = "### 📂 Informes Oficiales (Finanzas & Riesgos)\nAcceso directo al repositorio de reportes auditados y de clasificación de riesgo:"
            response["extra"] = self.files_db

        # DEFAULT
        else:
            response["texto"] = (
                f"{header}Soy **Petrolito AI**, Analista Financiero Senior.\n\n"
                f"Tengo acceso a la data macroeconómica y a los reportes auditados de Petroperú. "
                f"Mis modelos detectan una alta sensibilidad al **Tipo de Cambio (S/. {st.session_state.memoria['tipo_cambio']})** y al **WTI (${st.session_state.memoria['wti']})**.\n\n"
                f"Puedo analizar:\n"
                f"🔹 **La erosión del Patrimonio Neto.**\n"
                f"🔹 **El riesgo por Tipo de Cambio.**\n"
                f"🔹 **El perfil de vencimientos de la deuda.**\n"
                f"¿Qué indicador te preocupa más?"
            )

        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. INTERFAZ DE CHAT
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": {
            "texto": (
                "👋 **Bienvenido al Financial Core.**\n\n"
                "He integrado la data de **Pérdidas Netas**, **Riesgo Cambiario** y los reportes de las **Calificadoras de Riesgo**.\n"
                "La situación financiera muestra un deterioro patrimonial importante y alta dependencia del soporte estatal.\n\n"
                "¿Deseas analizar la **Evolución del Patrimonio** o el **Impacto del Dólar** en la deuda?"
            ),
            "visual": None, "extra": None
        }
    })

# HEADER
st.markdown("<h2 style='text-align:center;'>📉 Petroperú <span style='color:#E11D48;'>Ultimate Financial AI</span></h2>", unsafe_allow_html=True)

# LOOP MENSAJES
for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:15px;">
                <span style="font-size:24px; margin-right:12px;">🤖</span>
                <span style="font-weight:700; color:#E11D48;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        if pkg["visual"]:
            st.plotly_chart(pkg["visual"], use_container_width=True)
        if pkg["extra"] is not None:
            st.dataframe(pkg["extra"], use_container_width=True, hide_index=True)

# INPUT
if prompt := st.chat_input("Consulta experta (Ej: 'Analiza el patrimonio', 'El dolar subió a 3.90')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Ejecutando modelos financieros..."):
        time.sleep(0.6)
        resp = brain.generar_respuesta(st.session_state.mensajes[-1]["content"])
        st.session_state.mensajes.append({"role": "assistant", "content": resp})
        st.rerun()
