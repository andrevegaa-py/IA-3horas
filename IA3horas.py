import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO DASHBOARD CHAT)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Visual Intelligence",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Avanzados (Botones, Burbujas, Menús)
st.markdown("""
<style>
    /* Layout */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 9rem !important; max-width: 950px !important; }
    [data-testid="stAppViewContainer"] { background-color: #0B0F19; }
    
    /* Burbujas */
    .chat-bubble {
        padding: 20px 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .user-bubble {
        background: #334155;
        border: 1px solid #475569;
        color: #F8FAFC;
        margin-left: 20%;
        text-align: right;
    }
    .bot-bubble {
        background: #151B2B;
        border-left: 4px solid #F59E0B; /* Amber para Visuales */
        color: #E2E8F0;
        margin-right: 5%;
    }

    /* Títulos dentro del chat */
    .bot-bubble h3 { color: #FCD34D !important; margin: 0 0 10px 0; font-size: 20px; font-weight: 700; }
    .bot-bubble strong { color: #F59E0B; }
    
    /* MENÚ DE GRÁFICOS (Botones Estilizados) */
    .menu-header { color: #94A3B8; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-top: 10px; margin-bottom: 5px; }
    
    div.stButton > button {
        width: 100%;
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #334155 !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
        text-align: left !important;
        padding: 10px 15px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        border-color: #F59E0B !important;
        color: #F59E0B !important;
        background-color: rgba(245, 158, 11, 0.1) !important;
    }

    /* Input Flotante */
    .stChatInput {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 800px !important; z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO INTEGRAL (CONOCIMIENTO + CATÁLOGO VISUAL)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 76.5,
        "produccion": 95.0,
        "deuda": 8500
    }

class PetrolitoBrain:
    def __init__(self):
        # 1. Base de Conocimiento (Texto)
        self.knowledge = {
            "historia": "Desde 1969 hasta la privatización de los 90 (venta de Solgas/Transoceánica). Hoy buscamos recuperar la integración vertical.",
            "deuda": "Deuda total de **$8.5 Billones**. Déficit de capital de trabajo de -$2.2B. Bonos con vencimiento 2032/2047.",
            "talara": "Nueva Refinería Talara (NRT): 95 KBPD, tecnología Flexicoking, margen objetivo >$10/bbl."
        }
        
        # 2. Catálogo de Gráficos Disponibles (Menú Estructurado)
        self.visual_catalog = {
            "📉 Finanzas & Deuda": [
                {"label": "Composición de Deuda ($8.5B)", "id": "pie_deuda"},
                {"label": "Déficit de Capital de Trabajo", "id": "bar_deficit"},
                {"label": "Perfil de Vencimientos (Bonos)", "id": "line_vencimientos"}
            ],
            "🏭 Operaciones (NRT)": [
                {"label": "Waterfall de Costos NRT", "id": "waterfall_costos"},
                {"label": "Eficiencia Operativa vs Meta", "id": "gauge_eficiencia"},
                {"label": "Mapa de Activos Críticos", "id": "map_geo"}
            ],
            "🔮 Proyecciones Generativas": [
                {"label": "Simulación EBITDA 2025 (Dinámico)", "id": "bar_ebitda_sim"},
                {"label": "Sensibilidad Flujo de Caja", "id": "line_sensibilidad"}
            ]
        }

    # --- APRENDIZAJE ---
    def aprender(self, prompt):
        prompt = prompt.lower()
        msgs = []
        if re.search(r'(wti|precio).*?(\d{2,3})', prompt):
            val = float(re.search(r'(wti|precio).*?(\d{2,3})', prompt).group(2))
            st.session_state.memoria['wti'] = val
            msgs.append(f"WTI ${val}")
        if re.search(r'(producci|carga).*?(\d{2,3})', prompt):
            val = float(re.search(r'(producci|carga).*?(\d{2,3})', prompt).group(2))
            st.session_state.memoria['produccion'] = val
            msgs.append(f"Prod {val}k")
        return msgs

    # --- GENERADOR DE GRÁFICOS (BAJO DEMANDA) ---
    def renderizar_grafico(self, chart_id):
        mem = st.session_state.memoria
        
        if chart_id == "pie_deuda":
            fig = go.Figure(go.Pie(labels=['Bonos Lp', 'Crédito España', 'Corto Plazo (Déficit)'], values=[3000, 1300, 2200], hole=0.5, marker_colors=['#3B82F6', '#8B5CF6', '#EF4444']))
            fig.update_layout(title="Estructura Pasivos", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
            return fig
            
        elif chart_id == "bar_deficit":
            fig = go.Figure(go.Bar(x=['Caja Disponible', 'Obligaciones Corto Plazo'], y=[500, 2700], marker_color=['#10B981', '#EF4444']))
            fig.update_layout(title="Brecha de Liquidez (-$2.2B)", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
            return fig

        elif chart_id == "waterfall_costos":
            fig = go.Figure(go.Waterfall(orientation="v", measure=["relative", "relative", "relative", "total"], x=["Base", "EPC", "Intereses", "Total"], y=[1300, 3800, 3400, 0], connector={"line":{"color":"white"}}))
            fig.update_layout(title="Sobrecostos NRT", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
            return fig

        elif chart_id == "gauge_eficiencia":
            val = (mem['produccion'] / 95) * 100
            fig = go.Figure(go.Indicator(mode="gauge+number", value=val, title={'text': "Carga NRT (%)"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#F59E0B"}}))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=250)
            return fig
            
        elif chart_id == "bar_ebitda_sim":
            # Fórmula Generativa
            base = 150 + (mem['wti'] - 70)*10 + (mem['produccion'] - 80)*5
            fig = go.Figure(go.Bar(x=['Escenario Actual'], y=[base], marker_color='#F59E0B', text=[f"${base:.0f}M"], textposition='auto'))
            fig.update_layout(title=f"EBITDA Proyectado (WTI ${mem['wti']})", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
            return fig
            
        elif chart_id == "map_geo":
            layer = pdk.Layer("ScatterplotLayer", data=pd.DataFrame([{"lat": -4.58, "lon": -81.27}, {"lat": -5.5, "lon": -78.5}]), get_position=["lon", "lat"], get_color=[245, 158, 11], get_radius=10000, pickable=True)
            view = pdk.ViewState(latitude=-5.0, longitude=-80.0, zoom=5)
            return pdk.Deck(layers=[layer], initial_view_state=view, map_style="mapbox://styles/mapbox/dark-v10")
            
        return None

    # --- CEREBRO CONVERSACIONAL ---
    def procesar(self, prompt):
        prompt_low = prompt.lower()
        cambios = self.aprender(prompt)
        
        response = {"texto": "", "show_menu": False, "visual": None}
        header = f"📝 *Memoria Actualizada: {', '.join(cambios)}*\n\n" if cambios else ""

        # INTENCIÓN: SOLICITAR GRÁFICOS / MENÚ
        if any(x in prompt_low for x in ["grafico", "visual", "chart", "tabla", "ver datos", "opciones", "menu"]):
            response["texto"] = (
                f"{header}### 📊 Centro de Visualización\n"
                f"Tengo acceso a toda la data en tiempo real. He clasificado los gráficos disponibles por área estratégica.\n\n"
                f"**Selecciona qué visualización deseas generar ahora mismo:**"
            )
            response["show_menu"] = True
            return response

        # INTENCIÓN: DEUDA
        if "deuda" in prompt_low or "financiera" in prompt_low:
            response["texto"] = (
                f"{header}### 📉 Estado Financiero\n"
                f"{self.knowledge['deuda']}\n\n"
                f"Actualmente el déficit de caja es crítico. Con tu WTI de **${st.session_state.memoria['wti']}**, mejoramos márgenes, pero no liquidez inmediata."
            )
            response["visual"] = self.renderizar_grafico("pie_deuda")
            return response

        # INTENCIÓN: TALARA
        if "talara" in prompt_low or "nrt" in prompt_low:
            response["texto"] = (
                f"{header}### 🏭 Operaciones NRT\n"
                f"{self.knowledge['talara']}\n"
                f"Operando a **{st.session_state.memoria['produccion']} KBPD**. El factor de utilización es clave para diluir costos fijos."
            )
            response["visual"] = self.renderizar_grafico("gauge_eficiencia")
            return response

        # DEFAULT GEN-AI
        response["texto"] = (
            f"{header}Hola. Soy **Petrolito AI**.\n"
            f"Tengo toda la data histórica y financiera de Petroperú integrada. Aprendo de tus inputs (WTI/Producción).\n\n"
            f"💬 *Puedes preguntarme detalles o pedirme: **'Muéstrame los gráficos disponibles'** para ver el catálogo visual.*"
        )
        return response

brain = PetrolitoBrain()

# ==============================================================================
# 3. GESTIÓN DE CHAT Y CALLBACKS
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.mensajes.append({"role": "assistant", "content": {"texto": "👋 **Hola.** Soy tu analista integral.\nSi quieres ver datos duros, escribe: **'Ver gráficos'** y te mostraré mi catálogo.", "show_menu": False, "visual": None}})

def click_grafico(chart_id, label):
    # Simula que el usuario pidió ese gráfico específico
    st.session_state.mensajes.append({"role": "user", "content": f"Genera el gráfico: {label}"})
    # Genera la respuesta del bot con el gráfico
    visual = brain.renderizar_grafico(chart_id)
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": {
            "texto": f"### ✅ Visualización Generada: {label}\nAquí tienes el análisis solicitado basado en los parámetros actuales.",
            "visual": visual,
            "show_menu": False
        }
    })

# ==============================================================================
# 4. RENDERIZADO DEL CHAT
# ==============================================================================

st.markdown("<h2 style='text-align:center;'>🤖 Petroperú <span style='color:#F59E0B;'>Visual Core</span></h2>", unsafe_allow_html=True)

# Loop principal de mensajes
for i, msg in enumerate(st.session_state.mensajes):
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        # 1. Texto
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span style="font-size:24px; margin-right:10px;">🤖</span>
                <span style="font-weight:bold; color:#F59E0B;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Visuales (Si aplica)
        if pkg["visual"]:
            if isinstance(pkg["visual"], go.Figure):
                st.plotly_chart(pkg["visual"], use_container_width=True)
            elif isinstance(pkg["visual"], pdk.Deck):
                st.pydeck_chart(pkg["visual"], use_container_width=True)
        
        # 3. MENÚ DE GRÁFICOS (Solo si show_menu=True y es el último mensaje)
        if pkg.get("show_menu") and i == len(st.session_state.mensajes) - 1:
            st.markdown("---")
            catalog = brain.visual_catalog
            
            # Crear columnas para el layout del menú
            c1, c2, c3 = st.columns(3)
            cols = [c1, c2, c3]
            
            for idx, (categoria, items) in enumerate(catalog.items()):
                with cols[idx]:
                    st.markdown(f"<div class='menu-header'>{categoria}</div>", unsafe_allow_html=True)
                    for item in items:
                        # Botones que accionan el gráfico
                        if st.button(f"📊 {item['label']}", key=f"btn_{i}_{item['id']}"):
                            click_grafico(item['id'], item['label'])
                            st.rerun()

# ==============================================================================
# 5. INPUT USUARIO
# ==============================================================================

if prompt := st.chat_input("Pide 'Gráficos', 'Deuda' o actualiza datos (Ej: 'WTI 85')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Procesando..."):
        time.sleep(0.5)
        resp = brain.procesar(st.session_state.mensajes[-1]["content"])
        st.session_state.mensajes.append({"role": "assistant", "content": resp})
        st.rerun()
