import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re
import io

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (FINTECH / ENTERPRISE GRADE)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI 1.0 | Enterprise Finance",
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="collapsed"
)

# --- CSS DE ALTA GAMA ---
st.markdown("""
<style>
    /* 1. FONDO Y TIPOGRAFÍA */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #1E293B 0%, #0F172A 100%);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 8rem !important;
        max-width: 1000px !important;
    }

    /* 2. HEADER TECNOLÓGICO */
    .tech-header {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        padding: 15px 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .status-dot {
        height: 10px; width: 10px; background-color: #10B981;
        border-radius: 50%; display: inline-block; margin-right: 8px;
        box-shadow: 0 0 8px #10B981;
    }
    
    /* 3. BURBUJAS DE CHAT (GLASSMORPHISM) */
    .chat-bubble {
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        line-height: 1.7;
        font-size: 15px;
        letter-spacing: 0.3px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    .bot-bubble {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-left: 4px solid #00D4FF; /* Cyan Futista */
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-right: 5%;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #334155 0%, #1E293B 100%);
        border: 1px solid rgba(255,255,255,0.1);
        color: #F8FAFC;
        margin-left: 20%;
        text-align: right;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* 4. ELEMENTOS INTERNOS DE LUJO */
    h3.bot-title {
        color: #00D4FF;
        font-weight: 700;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
    }
    
    .highlight-kpi {
        background: rgba(0, 212, 255, 0.1);
        color: #00D4FF;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .ml-badge {
        font-size: 11px;
        text-transform: uppercase;
        color: #10B981;
        border: 1px solid #10B981;
        padding: 2px 8px;
        border-radius: 12px;
        margin-left: 10px;
        letter-spacing: 0.5px;
    }

    /* 5. BOTÓN DE DESCARGA PREMIUM */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 13px !important;
        letter-spacing: 1px !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
    }

    /* 6. INPUT FLOTANTE */
    .stChatInput { 
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); 
        width: 800px !important; z-index: 9999; 
    }
    .stChatInput > div {
        background-color: #1E293B !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Ocultar elementos */
    header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO NEURONAL (MACHINE LEARNING CORE)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 75.0,        
        "produccion": 95.0, 
        "ebitda_base": 667, 
        "sensibilidad": 15.5 
    }

class PetrolitoBrain:
    def __init__(self):
        pass

    # --- MOTOR DE APRENDIZAJE (ML SIMULATOR) ---
    def procesar_aprendizaje(self, prompt):
        prompt = prompt.lower()
        mem = st.session_state.memoria
        cambios = []
        analisis_impacto = ""

        # WTI Learning
        match_wti = re.search(r'(wti|precio|crudo).*?(\d{2,3})', prompt)
        if match_wti:
            nuevo_wti = float(match_wti.group(2))
            delta_wti = nuevo_wti - mem['wti']
            impacto_ebitda = delta_wti * mem['sensibilidad']
            
            mem['wti'] = nuevo_wti
            cambios.append(f"WTI: ${nuevo_wti}")
            
            direccion = "Incremento" if delta_wti > 0 else "Contracción"
            analisis_impacto += f"• **Sensibilidad de Mercado:** El ajuste a ${nuevo_wti} genera un {direccion} proyectado en EBITDA de **${abs(impacto_ebitda):.1f} MM**."

        # Producción Learning
        match_prod = re.search(r'(producci|carga).*?(\d{2,3})', prompt)
        if match_prod:
            nuevo_prod = float(match_prod.group(2))
            mem['produccion'] = nuevo_prod
            cambios.append(f"Output: {nuevo_prod}k")
            analisis_impacto += f"\n• **Eficiencia Operativa:** Nueva tasa de carga al {int(nuevo_prod/95*100)}% optimiza la absorción de costos fijos."

        return cambios, analisis_impacto

    # --- DATA ENGINE (GENERACIÓN DE ARCHIVOS) ---
    def generar_reporte_descargable(self, tipo):
        mem = st.session_state.memoria
        wti = mem['wti']
        
        if tipo == "proyeccion_fin":
            # Modelo Financiero Simplificado
            ingresos = 4500 + (wti - 70) * 50
            costos = 4000 + (wti - 70) * 30 
            ebitda = ingresos - costos - 200
            
            df = pd.DataFrame({
                "RUBRO FINANCIERO": ["INGRESOS OPERATIVOS", "COSTO DE VENTAS", "GASTOS OPERATIVOS", "EBITDA PROYECTADO", "SERVICIO DEUDA", "FLUJO NETO"],
                "ESCENARIO BASE (MM $)": [4500, -4000, -200, 300, -450, -150],
                "ESCENARIO AJUSTADO (MM $)": [ingresos, -costos, -200, ebitda, -450, ebitda - 450],
                "VARIACIÓN": [f"WTI ${wti}", "Indexado Crudo", "Austeridad", "Resultado", "Bonos+Bancos", "Caja Final"]
            })
            return df.to_csv(index=False).encode('utf-8'), f"PetrolitoAI_Proyeccion_2025_WTI_{int(wti)}.csv"

        elif tipo == "deuda_detalle":
            df = pd.DataFrame({
                "INSTRUMENTO": ["BONOS GLOBALES 2032", "BONOS GLOBALES 2047", "SINDICADO CESCE", "CAPITAL DE TRABAJO"],
                "PRINCIPAL (MM $)": [1000, 2000, 1300, 2200],
                "CUPÓN / TASA": ["4.750%", "5.625%", "SOFR + 2.5%", "8.50%"],
                "ESTADO": ["VIGENTE", "VIGENTE", "PERIODO GRACIA", "REFINANCIAMIENTO"]
            })
            return df.to_csv(index=False).encode('utf-8'), "PetrolitoAI_Deuda_Corporativa.csv"
            
        return None, None

    # --- GRAPHICS ENGINE (PLOTLY DARK) ---
    def generar_grafico(self, tipo):
        mem = st.session_state.memoria
        # Configuración de Lujo
        layout_vip = dict(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8', family="Inter"), title_font=dict(color='white', size=16),
            margin=dict(l=20, r=20, t=50, b=20), height=300
        )

        if tipo == "ebitda_dinamico":
            base = mem['ebitda_base']
            impacto = (mem['wti'] - 75) * mem['sensibilidad']
            
            fig = go.Figure(go.Waterfall(
                orientation="v", measure=["relative", "relative", "total"],
                x=["Base Oficial", "Delta WTI", "Proyección AI"],
                y=[base, impacto, 0],
                connector={"line":{"color":"#64748B"}},
                decreasing={"marker":{"color":"#F43F5E"}}, increasing={"marker":{"color":"#10B981"}}, totals={"marker":{"color":"#00D4FF"}}
            ))
            fig.update_layout(title=f"PROYECCIÓN EBITDA 2025 (WTI ${mem['wti']})", **layout_vip)
            return fig

        elif tipo == "termometro_deuda":
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = 8.5, 
                title = {'text': "DEUDA TOTAL ($B)"}, number = {'suffix': " B"},
                gauge = {
                    'axis': {'range': [0, 10]}, 
                    'bar': {'color': "#F43F5E"}, 
                    'bgcolor': "#1E293B",
                    'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 8.5}
                }
            ))
            fig.update_layout(**layout_vip)
            return fig

        return None

    # --- CEREBRO CONVERSACIONAL ---
    def responder(self, prompt):
        prompt_low = prompt.lower()
        cambios, analisis_ml = self.procesar_aprendizaje(prompt)
        
        response = {"texto": "", "visual": None, "archivo": None}
        
        # Header de Aprendizaje
        header = ""
        if cambios:
            header = f"""
            <div style="background: rgba(16, 185, 129, 0.1); border-radius: 8px; padding: 10px; margin-bottom: 15px; border-left: 3px solid #10B981;">
                <div style="color: #10B981; font-weight: bold; font-size: 12px; margin-bottom: 4px;">NEURAL UPDATE DETECTED</div>
                <div style="color: #E2E8F0; font-size: 13px;">Parámetros actualizados: {', '.join(cambios)}</div>
                <div style="color: #94A3B8; font-size: 12px; margin-top: 5px;">{analisis_ml}</div>
            </div>
            """

        # INTENCIÓN: REPORTES / DESCARGAR
        if any(x in prompt_low for x in ["descargar", "reporte", "excel", "csv", "data room"]):
            response["texto"] = (
                f"{header}<h3 class='bot-title'>📁 GENERADOR DE REPORTES</h3>"
                f"He procesado el modelo financiero con los parámetros actuales. "
                f"A continuación, presento el **Estado de Resultados Proyectado** listo para auditoría o revisión ejecutiva."
            )
            csv_data, nombre_archivo = self.generar_reporte_descargable("proyeccion_fin")
            response["archivo"] = {"data": csv_data, "name": nombre_archivo, "label": "📥 DOWNLOAD EXECUTIVE REPORT (.CSV)"}

        # INTENCIÓN: PROYECCIONES / FUTURO
        elif any(x in prompt_low for x in ["proyeccion", "ebitda", "futuro", "2025"]):
            response["texto"] = (
                f"{header}<h3 class='bot-title'>🔮 PROYECCIÓN FINANCIERA 2025 <span class='ml-badge'>AI MODEL</span></h3>"
                f"Utilizando el precio WTI de <span class='highlight-kpi'>${st.session_state.memoria['wti']}</span>, el algoritmo predice una recuperación operativa.\n\n"
                f"El siguiente gráfico de cascada (Waterfall) desglosa cómo las variables de mercado impactan nuestra meta de EBITDA:"
            )
            response["visual"] = self.generar_grafico("ebitda_dinamico")

        # INTENCIÓN: DEUDA / FINANZAS
        elif any(x in prompt_low for x in ["deuda", "dinero", "caja", "bonos"]):
            response["texto"] = (
                f"{header}<h3 class='bot-title'>📉 ANÁLISIS DE SOLVENCIA</h3>"
                f"La exposición crediticia total asciende a <span class='highlight-kpi'>$8.5 Billones</span>. "
                f"Aunque el perfil de vencimientos de largo plazo está cubierto por las emisiones 2032/2047, el **Déficit de Capital de Trabajo** presiona la tesorería diaria.\n\n"
                f"Se recomienda descargar el detalle de acreedores para su revisión."
            )
            response["visual"] = self.generar_grafico("termometro_deuda")
            csv_data, nombre_archivo = self.generar_reporte_descargable("deuda_detalle")
            response["archivo"] = {"data": csv_data, "name": nombre_archivo, "label": "📥 DOWNLOAD DEBT SCHEDULE"}

        # DEFAULT
        else:
            response["texto"] = (
                f"{header}<h3 class='bot-title'>🤖 PETROLITO AI 1.0 <span class='ml-badge'>ONLINE</span></h3>"
                f"Sistema operativo y conectado a los mercados. Datos en tiempo real:\n"
                f"• **WTI CRUDE:** <span class='highlight-kpi'>${st.session_state.memoria['wti']}</span>\n"
                f"• **OUTPUT NRT:** <span class='highlight-kpi'>{st.session_state.memoria['produccion']} KBPD</span>\n\n"
                f"Escriba un comando para iniciar:\n"
                f"🔹 *'Generar reporte financiero'*\n"
                f"🔹 *'Análisis de deuda'*\n"
                f"🔹 *'WTI 85' (Para recalibrar)*"
            )

        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. INTERFAZ DE USUARIO (DASHBOARD)
# ==============================================================================

# --- HEADER TIPO DASHBOARD ---
st.markdown("""
<div class="tech-header">
    <div style="display:flex; align-items:center;">
        <span style="font-size: 24px; margin-right: 15px;">💠</span>
        <div>
            <div style="font-weight: 700; font-size: 20px; color: white;">PETROLITO AI 1.0</div>
            <div style="font-size: 11px; color: #00D4FF; letter-spacing: 1px;">ENTERPRISE FINANCIAL INTELLIGENCE</div>
        </div>
    </div>
    <div style="text-align: right;">
        <div style="font-size: 11px; color: #94A3B8;">SYSTEM STATUS</div>
        <div style="font-size: 13px; color: #10B981; font-weight: 600;"><span class="status-dot"></span>OPERATIONAL</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.mensajes.append({"role": "assistant", "content": {"texto": "<h3 class='bot-title'>👋 SYSTEM INITIALIZED</h3>Bienvenido al entorno financiero de Petroperú. Soy Petrolito AI 1.0.<br>Mis modelos predictivos están listos. ¿Desea descargar un <b>Reporte Financiero</b> o realizar una <b>Simulación de WTI</b>?", "visual": None, "archivo": None}})

# --- RENDERIZADO DEL CHAT ---
for i, msg in enumerate(st.session_state.mensajes):
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        st.markdown(f"""<div class="chat-bubble bot-bubble">{pkg['texto']}</div>""", unsafe_allow_html=True)
        
        if pkg["visual"]:
            st.plotly_chart(pkg["visual"], use_container_width=True)
            
        if pkg["archivo"]:
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                st.download_button(
                    label=pkg["archivo"]["label"],
                    data=pkg["archivo"]["data"],
                    file_name=pkg["archivo"]["name"],
                    mime="text/csv",
                    key=f"dl_{i}"
                )

# --- INPUT ---
if prompt := st.chat_input("Introduzca comando (Ej: 'Reporte', 'Deuda', 'WTI 90')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Processing Data Stream..."):
        time.sleep(0.6)
        resp = brain.responder(st.session_state.mensajes[-1]["content"])
        st.session_state.mensajes.append({"role": "assistant", "content": resp})
        st.rerun()
