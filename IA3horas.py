import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import re

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO AMIGABLE / DARK)
# ==============================================================================
st.set_page_config(
    page_title="Petrolito AI | Tu Asistente Fácil",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="collapsed"
)

# Estilos CSS: Alto contraste, letras grandes y colores guía
st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 8rem !important; max-width: 900px !important; }
    [data-testid="stAppViewContainer"] { background-color: #0F172A; } /* Fondo Azul Oscuro */
    
    /* Burbujas de Chat */
    .chat-bubble {
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        line-height: 1.8;
        font-family: 'Segoe UI', sans-serif;
        font-size: 17px; /* Letra más grande para lectura fácil */
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .user-bubble { background-color: #334155; color: #F8FAFC; margin-left: 15%; text-align: right; border-bottom-right-radius: 2px; }
    .bot-bubble { background-color: #1E293B; border-left: 6px solid #8B5CF6; color: #E2E8F0; margin-right: 5%; border-bottom-left-radius: 2px; }
    
    /* Elementos Educativos */
    .concept-box {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid #8B5CF6;
        color: #C4B5FD;
        padding: 10px;
        border-radius: 8px;
        font-size: 14px;
        margin-top: 10px;
        font-style: italic;
    }
    .highlight-good { color: #34D399; font-weight: bold; }
    .highlight-bad { color: #F87171; font-weight: bold; }
    
    /* Títulos */
    .bot-bubble h3 { color: #A78BFA !important; margin: 0 0 15px 0; font-size: 22px; font-weight: 700; }
    
    /* Input */
    .stChatInput { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 800px !important; z-index: 9999; }
    header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CEREBRO INTELIGENTE (DATA PROFUNDA + EXPLICACIÓN SIMPLE)
# ==============================================================================

if 'memoria' not in st.session_state:
    st.session_state.memoria = {
        "wti": 75.0,        # Precio del Petróleo
        "produccion": 95.0, # Miles de barriles al día
        "usuario_nivel": "principiante"
    }

class PetrolitoTeacher:
    def __init__(self):
        # DATOS REALES (NO SE PIERDE NADA)
        self.datos_duros = {
            "deuda_total": 8500, # Millones USD
            "deficit_caja": 2200, # El "hueco" de dinero
            "perdida_2023": 822,
            "ebitda_meta_2025": 667,
            "bonos_vencimiento": [2032, 2047]
        }
        
        # DICCIONARIO PARA PRINCIPIANTES
        self.explicaciones = {
            "ebitda": "💡 **¿Qué es EBITDA?**: Imagínalo como la ganancia bruta del negocio antes de pagar intereses, impuestos o deudas. Si es positivo, el negocio funciona; si es negativo, pierde dinero operando.",
            "capital_trabajo": "💡 **¿Qué es Capital de Trabajo?**: Es el dinero que necesitas en el bolsillo para operar hoy (comprar crudo, pagar luz). Si es negativo, significa que debes más a corto plazo de lo que tienes en la caja.",
            "flexicoking": "💡 **¿Qué es Flexicoking?**: Es como una 'olla a presión' gigante en la refinería que convierte lo que nadie quiere (brea/residuo) en productos caros (diésel/gasolina). Es la joya de la nueva fábrica."
        }

    # --- APRENDIZAJE: DETECTA CAMBIOS Y EXPLICA EL IMPACTO ---
    def procesar_cambio(self, prompt):
        prompt = prompt.lower()
        msg = ""
        
        # Detectar WTI
        match_wti = re.search(r'(wti|precio|petroleo|crudo).*?(\d{2,3})', prompt)
        if match_wti:
            val = float(match_wti.group(2))
            st.session_state.memoria['wti'] = val
            impacto = "positivo" if val > 70 else "negativo"
            explicacion = "suben nuestros ingresos porque vendemos más caro" if impacto == "positivo" else "bajan nuestros márgenes"
            msg = f"🔄 **Entendido. Ajusté el precio del petróleo a ${val}.**\nEsto significa que {explicacion}."

        # Detectar Producción
        match_prod = re.search(r'(producci|carga|fabrica).*?(\d{2,3})', prompt)
        if match_prod:
            val = float(match_prod.group(2))
            st.session_state.memoria['produccion'] = val
            msg = f"🔄 **Ajusté la producción de la fábrica a {val} mil barriles.**"
            
        return msg

    # --- GRÁFICOS EDUCATIVOS (LETRAS BLANCAS) ---
    def generar_grafico(self, tipo):
        mem = st.session_state.memoria
        
        # Configuración Visual Limpia
        layout_clean = dict(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family="Segoe UI", size=14), # BLANCO Y GRANDE
            margin=dict(l=20, r=20, t=50, b=20),
            height=300
        )

        if tipo == "termometro_caja":
            # Gráfico de Semáforo para la Deuda Corto Plazo
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = -self.datos_duros['deficit_caja'], # Valor negativo
                title = {'text': "Salud de Caja (Millones $)"},
                gauge = {
                    'axis': {'range': [-3000, 1000], 'tickfont': {'color': 'white'}},
                    'bar': {'color': "#F87171"}, # Rojo
                    'steps': [
                        {'range': [-3000, -1000], 'color': "rgba(239, 68, 68, 0.2)"}, # Zona Crítica
                        {'range': [-1000, 0], 'color': "rgba(251, 191, 36, 0.2)"},   # Zona Alerta
                        {'range': [0, 1000], 'color': "rgba(16, 185, 129, 0.2)"}     # Zona Verde
                    ],
                    'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 0}
                }
            ))
            fig.update_layout(**layout_clean)
            return fig

        elif tipo == "proyeccion_simple":
            # Bar chart simple: Pérdida vs Ganancia
            wti_effect = (mem['wti'] - 75) * 10
            ebitda_2025 = self.datos_duros['ebitda_meta_2025'] + wti_effect
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['2023 (Real)', '2025 (Tu Proyección)'],
                y=[-104, ebitda_2025],
                marker_color=['#F87171', '#34D399'], # Rojo vs Verde
                text=[f"-${104}M", f"+${int(ebitda_2025)}M"],
                textposition='auto'
            ))
            fig.update_layout(title="De Perder a Ganar (EBITDA)", **layout_common_axis(layout_clean))
            return fig
            
        elif tipo == "torta_deuda":
            # Pie chart simple
            fig = go.Figure(go.Pie(
                labels=['Lo que debemos a largo plazo (Bonos)', 'Lo que debemos pagar YA (Proveedores)'],
                values=[4300, 2200],
                marker_colors=['#3B82F6', '#EF4444'], # Azul vs Rojo
                textinfo='label+percent',
                textfont=dict(color='white')
            ))
            fig.update_layout(title="¿A quién le debemos?", **layout_clean)
            return fig

        return None

    # --- CEREBRO CONVERSACIONAL AMIGABLE ---
    def responder(self, prompt):
        prompt_low = prompt.lower()
        feedback = self.procesar_cambio(prompt)
        header = f"{feedback}\n\n" if feedback else ""
        
        response = {"texto": "", "visual": None}

        # CASO 1: DINERO / DEUDA (Explicación Sencilla)
        if any(x in prompt_low for x in ["dinero", "deuda", "plata", "quiebra", "caja", "situacion"]):
            response["texto"] = (
                f"{header}### 📉 ¿Cómo está la billetera de la empresa?\n"
                f"Te lo explico simple: Petroperú tiene activos valiosos (como la refinería), pero ahora mismo tiene un problema de liquidez.\n\n"
                f"Imagina que tienes una casa que vale mucho, pero no tienes efectivo en la billetera para pagar la luz hoy. Eso le pasa a la empresa:\n"
                f"* Tiene un **'Hueco de Caja' de ${self.datos_duros['deficit_caja']} Millones** (necesita pagar proveedores ya).\n"
                f"* En total, debe **$8,500 Millones**, pero la mayoría de eso se paga en muchos años (hasta el 2047).\n\n"
                f"Mira este 'termómetro' de salud financiera:"
            )
            response["texto"] += f"\n\n{self.explicaciones['capital_trabajo']}" # Añade explicación educativa
            response["visual"] = self.generar_grafico("termometro_caja")

        # CASO 2: FUTURO / PROYECCIONES (Optimismo vs Realidad)
        elif any(x in prompt_low for x in ["futuro", "ganar", "2025", "proyeccion", "ebitda"]):
            wti = st.session_state.memoria['wti']
            response["texto"] = (
                f"{header}### 🚀 ¿Vamos a ganar dinero pronto?\n"
                f"Sí, esa es la meta. Después de perder dinero en 2023 y 2024, el plan para 2025 es volver a los números azules (ganancias).\n\n"
                f"Con el precio del petróleo que tú me diste (**${wti}**), la refinería gana más por cada barril que procesa. "
                f"Se espera pasar de perder dinero a ganar unos **${int(667 + (wti-75)*10)} Millones** (EBITDA)."
            )
            response["texto"] += f"\n\n{self.explicaciones['ebitda']}"
            response["visual"] = self.generar_grafico("proyeccion_simple")

        # CASO 3: TALARA (Explicación Operativa)
        elif any(x in prompt_low for x in ["talara", "refineria", "fabrica", "operacion"]):
            response["texto"] = (
                f"{header}### 🏭 La Nueva Fábrica (Refinería Talara)\n"
                f"Ya no es la refinería vieja. Ahora es un complejo moderno que está funcionando casi al máximo de su capacidad (**{st.session_state.memoria['produccion']} mil barriles/día**).\n\n"
                f"Su secreto es la unidad de 'Flexicoking'. Antes, lo que sobraba del petróleo (brea) se vendía barato. Ahora, esa máquina lo convierte en gasolina cara. "
                f"Eso hace que ganemos **3 veces más** por barril que antes."
            )
            response["texto"] += f"\n\n{self.explicaciones['flexicoking']}"

        # CASO 4: ARCHIVOS (Transparencia)
        elif any(x in prompt_low for x in ["archivo", "papel", "reporte", "descargar"]):
            df_files = pd.DataFrame({"Nombre del Archivo": ["Reporte de Auditoría 2023", "Plan 2025", "Deuda Detallada"], "Formato": ["PDF", "Excel", "PDF"]})
            response["texto"] = "### 📂 Papeles Oficiales\nAquí tienes los documentos reales por si quieres ver los números al detalle:"
            response["visual"] = df_files # Streamlit maneja esto automático

        # DEFAULT (Guía Amigable)
        else:
            response["texto"] = (
                f"{header}Hola, soy **Petrolito**. Soy una IA que entiende de finanzas pero habla tu idioma.\n\n"
                f"Tengo toda la información de la empresa. Actualmente calculo todo con un petróleo a **${st.session_state.memoria['wti']}**.\n\n"
                f"**¿Qué quieres saber?** (Escribe como quieras):\n"
                f"🔹 *'¿Estamos quebrados?'* (Te explico la deuda)\n"
                f"🔹 *'¿Cuándo ganaremos dinero?'* (Te muestro el futuro)\n"
                f"🔹 *'El petróleo subió a 90'* (Para actualizar mis cálculos)"
            )

        return response

def layout_common_axis(base_layout):
    # Helper para asegurar ejes blancos
    base_layout['xaxis'] = dict(tickfont=dict(color='white'), showgrid=False)
    base_layout['yaxis'] = dict(tickfont=dict(color='white'), gridcolor='rgba(255,255,255,0.1)')
    return base_layout

brain = PetrolitoTeacher()

# ==============================================================================
# 3. INTERFAZ DE CHAT
# ==============================================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": {
            "texto": "👋 **¡Hola! Soy Petrolito.**\n\nSoy experto en finanzas de Petroperú, pero te lo voy a explicar fácil. \n¿Quieres saber sobre la **Deuda** (el dinero que debemos) o sobre la **Refinería** (cómo producimos)?",
            "visual": None
        }
    })

# RENDERIZADO
st.markdown("<h2 style='text-align:center;'>🎓 Petrolito <span style='color:#8B5CF6;'>Modo Educativo</span></h2>", unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"""<div class="chat-bubble user-bubble">{msg["content"]}</div>""", unsafe_allow_html=True)
    else:
        pkg = msg["content"]
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div style="display:flex; align-items:center; margin-bottom:15px;">
                <span style="font-size:24px; margin-right:12px;">🤖</span>
                <span style="font-weight:700; color:#A78BFA;">PETROLITO</span>
            </div>
            {pkg['texto']}
        </div>
        """, unsafe_allow_html=True)
        
        if pkg["visual"] is not None:
            if isinstance(pkg["visual"], go.Figure):
                st.plotly_chart(pkg["visual"], use_container_width=True)
            else:
                st.dataframe(pkg["visual"], use_container_width=True, hide_index=True)

# INPUT
if prompt := st.chat_input("Pregunta lo que quieras (Ej: '¿Hay dinero?', 'El crudo bajó a 60')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "user":
    with st.spinner("Buscando la mejor forma de explicarte..."):
        time.sleep(0.5)
        resp = brain.responder(st.session_state.mensajes[-1]["content"])
        st.session_state.mensajes.append({"role": "assistant", "content": resp})
        st.rerun()
