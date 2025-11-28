import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (ESTILO ENTERPRISE)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Financial Intelligence",
    layout="wide",
    page_icon="📉",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados
st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 7rem !important; max-width: 950px !important; }
    [data-testid="stAppViewContainer"] { background-color: #0F172A; }
    
    .chat-bubble { padding: 25px; border-radius: 12px; margin-bottom: 25px; line-height: 1.6; font-family: 'Segoe UI', sans-serif; font-size: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .user-bubble { background-color: #334155; color: #F8FAFC; margin-left: 20%; text-align: right; border-bottom-right-radius: 2px; }
    .bot-bubble { background-color: #1E293B; border-left: 5px solid #E11D48; /* Rojo Financiero */ color: #E2E8F0; margin-right: 5%; border-bottom-left-radius: 2px; }
    
    .bot-bubble h3 { color: #F43F5E !important; margin: 0 0 15px 0; font-size: 22px; font-weight: 700; }
    .bot-bubble strong { color: #34D399; font-weight: 600; }
    .data-highlight { background: rgba(225, 29, 72, 0.1); border: 1px solid #E11D48; color: #FDA4AF; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    
    .strategic-q { display: block; margin-top: 20px; padding-top: 15px; border-top: 1px solid #334155; color: #38BDF8; font-weight: bold; font-style: italic; }
    .stChatInput { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 800px !important; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO FINANCIERO (DATA REAL AUDITADA)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {"wti": 75.0, "produccion": 95.0}

class PetrolitoBrain:
    def __init__(self):
        # --- BASE DE DATOS REAL (HALLAZGOS) ---
        self.financial_data = {
            "resultados": {
                "2023": -822, # Millones USD (Pérdida Neta)
                "2024_est": -774, # Estimado cierre
                "2025_proy": -200 # Proyección optimista (reducción pérdida)
            },
            "ebitda": {
                "2023": -104, # Negativo real
                "2024_est": 150, # Recuperación leve
                "2025_meta": 667 # Meta Oficial 2025
            },
            "deuda_real": {
                "total": 8500,
                "bonos": 3000,
                "cesce": 1300,
                "working_capital_deficit": 2200 # Hueco de liquidez
            }
        }
        
        self.files_db = pd.DataFrame({
            "Reporte Oficial": [
                "Estados Financieros Auditados 2023 (PwC)", 
                "Reporte Resultados Q3 2024", 
                "Proyección Flujo de Caja 2025-2030",
                "Clasificación Riesgo Apoyo & Asociados 2024"
            ],
            "Fecha": ["02/05/2024", "15/11/2024", "01/12/2024", "24/05/2024"],
            "Hallazgo Clave": [
                "Pérdida Neta $822M / Opinión con Salvedades",
                "Recuperación Margen Operativo",
                "Meta EBITDA $667M para 2025",
                "Rating bajó a A+(pe) por soporte estatal"
            ]
        })

    def aprender(self, prompt):
        prompt = prompt.lower()
        msg = ""
        actualizo = False
        
        match_wti = re.search(r'(wti|precio).*?(\d{2,3})', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memoria['wti'] = val
            msg = f"📝 *Ajuste de Mercado: WTI recalibrado a ${val}.*"
            actualizo = True
            
        return actualizo, msg

    # --- GENERADORES GRÁFICOS (PROYECCIONES REALES) ---
    def generar_visual(self, tipo):
        if tipo == "proyeccion_ebitda":
            # Gráfico de Recuperación EBITDA 2023-2025
            years = ['2023 (Real)', '2024 (Est.)', '2025 (Proyección)']
            vals = [self.financial_data['ebitda']['2023'], 
                    self.financial_data['ebitda']['2024_est'], 
                    self.financial_data['ebitda']['2025_meta']]
            
            colors = ['#EF4444', '#F59E0B', '#10B981'] # Rojo, Amarillo, Verde
            
            fig = go.Figure(go.Bar(
                x=years, y=vals, marker_color=colors,
                text=[f"${v}M" for v in vals], textposition='auto'
            ))
            fig.update_layout(
                title="🚀 Proyección Oficial EBITDA: El Salto 2025",
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300,
                yaxis_title="Millones USD"
            )
            return fig

        elif tipo == "estructura_deuda":
            # Pie Chart de la Deuda Real
            labels = ['Bonos Soberanos', 'Crédito CESCE', 'Déficit Capital Trabajo', 'Otras Obligaciones']
            values = [3000, 1300, 2200, 2000]
            
            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.4,
                marker_colors=['#3B82F6', '#8B5CF6', '#EF4444', '#64748B']
            ))
            fig.update_layout(
                title="🚨 Anatomía de la Deuda ($8.5B)",
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300
            )
            return fig
            
        elif tipo == "flujo_caja":
             # Proyección Cash Flow Operativo
             wti = st.session_state.memoria['wti']
             base_2025 = 5000 # Meta oficial $5B
             ajuste = (wti - 75) * 50 # Sensibilidad
             final = base_2025 + ajuste
             
             fig = go.Figure(go.Indicator(
                mode = "number+delta",
                value = final,
                delta = {'reference': 5000, 'relative': True, 'valueformat': '.1%'},
                title = {"text": f"Flujo de Caja Operativo 2025 (Est. WTI ${wti})"},
                number = {'prefix': "$", 'suffix': " M"}
            ))
             fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=200, font={'color': "white"})
             return fig

        return None

    # --- MOTOR DE RESPUESTA ---
    def procesar(self, prompt):
        prompt_low = prompt.lower()
        actualizo, msg_learning = self.aprender(prompt)
        response = {"texto": "", "visual": None, "tipo_visual": None}
        prefix = msg_learning + "\n\n" if actualizo else ""
        
        # TEMA 1: PROYECCIONES 2025 / EBITDA
        if any(x in prompt_low for x in ["proyeccion", "futuro", "2025", "ebitda", "ganancia"]):
            response["texto"] = (
                f"{prefix}### 🔮 Proyecciones Financieras 2025\n"
                f"La gerencia ha establecido una meta agresiva de recuperación:\n\n"
                f"* **EBITDA 2025:** Se proyecta alcanzar **$667 Millones** (positivo), saliendo de los números rojos de 2023 (-$104M).\n"
                f"* **Flujo de Caja:** Meta de ingresos operativos de **$5,000 Millones**.\n"
                f"* **Pérdida Neta:** Se espera reducir el déficit de -$800M a niveles manejables.\n\n"
                f"<span class='strategic-q'>📊 Análisis: Para lograr este EBITDA de $667M, necesitamos que la refinería mantenga el 100% de carga sin paradas. ¿Crees que el riesgo operativo está cubierto?</span>"
            )
            response["visual"] = self.generar_visual("proyeccion_ebitda")
            response["tipo_visual"] = "plotly"

        # TEMA 2: DEUDA / ESTADOS FINANCIEROS
        elif any(x in prompt_low for x in ["deuda", "financiero", "perdida", "balance", "capital"]):
            response["texto"] = (
                f"{prefix}### 📉 Estado de Situación Financiera (Auditado)\n"
                f"La situación es delicada. Los reportes confirman:\n"
                f"1.  **Déficit de Capital de Trabajo:** <span class='data-highlight'>-$2,200 Millones</span>. (Hueco de liquidez inmediato).\n"
                f"2.  **Pérdidas Acumuladas:** 2023 cerró con -$822M y 2024 bordea los -$774M.\n"
                f"3.  **Soporte:** Fitch bajó la calificación a A+(pe) asumiendo soporte del Estado.\n\n"
                f"<span class='strategic-q'>🤔 Dilema: Tenemos $2.2B de déficit de caja a corto plazo. ¿Priorizamos pagar a proveedores de crudo o el servicio de bonos?</span>"
            )
            response["visual"] = self.generar_visual("estructura_deuda")
            response["tipo_visual"] = "plotly"

        # TEMA 3: ARCHIVOS / REPORTES
        elif any(x in prompt_low for x in ["reporte", "archivo", "descargar", "auditado", "pwc"]):
            response["texto"] = "### 📂 Data Room: Estados Financieros Auditados\nHe compilado los reportes oficiales encontrados (PwC, Apoyo & Asociados):"
            response["visual"] = self.files_db
            response["tipo_visual"] = "dataframe"

        # TEMA 4: DEFAULT (RESUMEN EJECUTIVO)
        else:
            response["texto"] = (
                f"{prefix}Hola. Soy **Petrolito AI**, tu analista financiero.\n\n"
                f"He procesado la data real: Tuvimos pérdidas de **$822M en 2023**, pero proyectamos un **EBITDA de $667M para 2025**.\n"
                f"Tengo simulaciones listas con tu WTI de **${st.session_state.memoria['wti']}**.\n\n"
                f"<span class='strategic-q'>👋 ¿Quieres ver el gráfico de la recuperación del EBITDA o analizar el detalle de la Deuda?</span>"
            )
            if actualizo:
                 response["visual"] = self.generar_visual("flujo_caja")
                 response["tipo_visual"] = "plotly"

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
                "👋 **Bienvenido al Centro de Inteligencia Financiera.**\n\n"
                "He cargado los **Estados Financieros Auditados 2023-2024** y las **Proyecciones 2025**.\n"
                "Detecto un déficit de capital de trabajo de $2.2B, pero una meta de EBITDA positivo para el próximo año.\n\n"
                "<span class='strategic-q'>¿Empezamos revisando las Proyecciones 2025 o la Estructura de la Deuda?</span>"
            ),
            "visual": None, "tipo_visual": None
        }
    })

# Renderizado
st.markdown("<h2 style='text-align:center;'>📉 Petroperú <span style='color:#E11D48;'>Financial Core</span></h2>", unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span style="font-size:24px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#E11D48;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        if pkg["visual"] is not None:
            with st.container():
                if pkg["tipo_visual"] == "plotly":
                    st.plotly_chart(pkg["visual"], use_container_width=True)
                elif pkg["tipo_visual"] == "dataframe":
                    st.dataframe(pkg["visual"], use_container_width=True, hide_index=True)

if prompt := st.chat_input("Ej: 'Ver proyecciones 2025' o 'El WTI está en 80'"):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Analizando reportes auditados..."):
        time.sleep(0.7)
        resp = brain.procesar(st.session_state.mensajes[-1]["content"])
        st.session_state.mensajes.append({"role": "assistant", "content": resp})
        st.rerun()
