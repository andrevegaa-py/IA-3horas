import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🏭")

# --- 2. GESTIÓN DE ESTADO (SESSION STATE & MEMORIA) ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'
if 'moneda' not in st.session_state:
    st.session_state.moneda = "USD ($)"

# Memoria de Chat y Contexto de Profundidad
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": (
            "Bienvenido. Soy Petrolito, su sistema de inteligencia financiera.\n\n"
            "Mi nueva arquitectura de **Niveles de Profundidad** me permite detallar información progresivamente.\n"
            "Temas habilitados para Drill-Down:\n"
            "• **Deuda Estructural** (Bonos y CESCE)\n"
            "• **Operaciones Talara** (Flexicoking y Márgenes)\n"
            "• **Macroeconomía** (Riesgo País y WTI)\n\n"
            "¿Por dónde desea comenzar?"
        )
    }]

if "contexto_chat" not in st.session_state:
    # Rastrea de qué estamos hablando y en qué nivel de detalle (0=Resumen, 1=Detalle, 2=Técnico)
    st.session_state.contexto_chat = {"tema_actual": None, "nivel_profundidad": 0}

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL IMPACT) ---
estilos_tech = """
<style>
    /* FONDO GENERAL */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.94), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    [data-testid="stSidebar"] { background-color: #0B1120; border-right: 1px solid rgba(56, 189, 248, 0.2); }
    
    /* TEXTOS */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* COMPONENTS */
    .stButton>button {
        width: 100%; background-color: #1E293B; color: #38BDF8 !important; 
        border: 1px solid #38BDF8; border-radius: 6px; transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    
    /* CHAT CARDS */
    .bot-card {
        background-color: rgba(15, 23, 42, 0.9); 
        border: 1px solid #38BDF8; 
        border-left: 5px solid #38BDF8; 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);
    }
    .user-card {
        background-color: rgba(56, 189, 248, 0.2); 
        color: white; 
        padding: 12px 20px; 
        border-radius: 15px 15px 0 15px; 
        margin-bottom: 15px; 
        text-align: right;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .glass-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px; padding: 20px;
        backdrop-filter: blur(8px); margin-bottom: 15px;
    }
</style>
"""
st.markdown(estilos_tech, unsafe_allow_html=True)

# --- URLS IMÁGENES ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_USER = "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg"
IMG_SIDEBAR_BANNER = "https://img.freepik.com/free-photo/oil-refinery-twilight_1112-575.jpg"
IMG_CARD_TALARA = "https://portal.andina.pe/EDPfotografia3/Thumbnail/2022/04/12/000862854W.jpg"
IMG_CARD_FINANCE = "https://img.freepik.com/free-photo/standard-quality-control-collage-concept_23-2149595831.jpg"
IMG_CARD_AI = "https://img.freepik.com/free-photo/rpa-concept-with-blurry-hand-touching-screen_23-2149311914.jpg"

# --- 4. CEREBRO FINANCIERO AVANZADO (MULTINIVEL) ---
def cerebro_financiero_avanzado(prompt):
    prompt = prompt.lower()
    
    # BASE DE DATOS JERÁRQUICA (Lista de 3 niveles por tema)
    db_multinivel = {
        "deuda": [
            # NIVEL 0: Ejecutivo
            {
                "titulo": "📉 Deuda: Panorama Ejecutivo",
                "texto": "La deuda total consolidada es de **USD 8.5 Billones**. La estructura es pesada pero sostenible si se recupera el Grado de Inversión. Actualmente, el servicio de deuda compite con el OPEX.",
                "dato": "Total: $8.5B | Apalancamiento: Crítico"
            },
            # NIVEL 1: Analítico
            {
                "titulo": "📉 Deuda: Desglose por Instrumento",
                "texto": "Profundizando en la composición: El 45% son **Bonos Corporativos** internacionales y el 30% corresponde a la facilidad **CESCE (España)** para Talara. El resto es capital de trabajo a corto plazo que requiere 'rollover' constante.",
                "dato": "Bonos: $3.0B | CESCE: $1.3B"
            },
            # NIVEL 2: Técnico/Granular
            {
                "titulo": "📉 Deuda: Detalle de Covenants y Tasas",
                "texto": "A nivel granular: El **Bono 2047** tiene un cupón de 5.625%, pero su 'Yield' actual supera el 11% debido al descuento por riesgo país. Estamos negociando un 'Waiver' con la banca sindicada por incumplimiento de ratios de liquidez corriente.",
                "dato": "Cupón 2047: 5.625% | Waiver: En trámite"
            }
        ],
        "talara": [
            # NIVEL 0
            {
                "titulo": "🏭 PMRT: Situación General",
                "texto": "La Nueva Refinería Talara está operativa al 100%. Ya no es un proyecto en construcción. Procesa 95k barriles/día produciendo combustibles Euro VI.",
                "dato": "Estado: 100% Operativa"
            },
            # NIVEL 1
            {
                "titulo": "🏭 PMRT: Margen de Refinación",
                "texto": "La rentabilidad depende de la unidad de **Flexicoking**. A diferencia de la refinería antigua, esta tecnología convierte residuales baratos en productos valiosos, buscando elevar el margen de $4 a $10-12 por barril.",
                "dato": "Margen Objetivo: $10-12/bbl"
            },
            # NIVEL 2
            {
                "titulo": "🏭 PMRT: Especificaciones Técnicas",
                "texto": "Datos duros: La unidad de Flexicoking (FCK) tiene capacidad de 22,000 BPD de residuo de vacío. Las unidades de hidrotratamiento (HTD/HTG) operan a 85 bares de presión para eliminar azufre (<50ppm). El cuello de botella actual es logístico (evacuación en muelle).",
                "dato": "Capacidad FCK: 22k BPD | Azufre: <50ppm"
            }
        ],
        "macro": [
            # NIVEL 0
            {
                "titulo": "🌍 Contexto: Estabilidad y Sector",
                "texto": "El entorno es volátil. El precio del crudo y el soporte del Gobierno son las variables clave. A nivel nacional, mantenemos la garantía implícita del Estado Peruano.",
                "dato": "Soporte: Activo (Decretos Urgencia)"
            },
            # NIVEL 1
            {
                "titulo": "🌍 Contexto: Variables de Mercado",
                "texto": "El **WTI** oscila entre $75-$80, lo que afecta el costo de importación. El **Tipo de Cambio** (~3.75 PEN/USD) es crítico pues vendemos en Soles pero pagamos deuda en Dólares. El BCRP interviene para suavizar esta volatilidad.",
                "dato": "TC: 3.75 | WTI: ~$78"
            },
            # NIVEL 2
            {
                "titulo": "🌍 Contexto: Riesgo y Calificación",
                "texto": "Técnicamente, nuestra calificación crediticia ha bajado (Fitch/S&P nos ubican en terreno especulativo 'Junk'). El 'Spread' soberano de Perú es bajo (168 pbs), pero el spread corporativo de Petroperú es alto. La estrategia es recuperar el 'Investment Grade' vía auditorías.",
                "dato": "Rating: BB+ (Negativo) | Riesgo País: 168pbs"
            }
        ]
    }

    # 1. DETECTAR TEMA
    tema_detectado = None
    if any(x in prompt for x in ["deuda", "bono", "banco", "pagar", "dinero"]): tema_detectado = "deuda"
    elif any(x in prompt for x in ["talara", "refineria", "refinería", "produccion", "flexicoking"]): tema_detectado = "talara"
    elif any(x in prompt for x in ["mercado", "sector", "wti", "precio", "gobierno", "mef", "riesgo", "nacional"]): tema_detectado = "macro"

    # 2. MÁQUINA DE ESTADOS (Profundidad)
    if tema_detectado:
        estado = st.session_state.contexto_chat
        
        # Si es el mismo tema, aumentamos nivel. Si es nuevo, reset a 0.
        if estado["tema_actual"] == tema_detectado:
            nuevo_nivel = min(estado["nivel_profundidad"] + 1, 2)
        else:
            nuevo_nivel = 0
        
        # Actualizar memoria
        st.session_state.contexto_chat = {"tema_actual": tema_detectado, "nivel_profundidad": nuevo_nivel}
        
        # Obtener info
        info = db_multinivel[tema_detectado][nuevo_nivel]
        
        # Mensaje de ayuda visual
        footer = ""
        if nuevo_nivel < 2:
            footer = "\n\n🔽 *Para más detalles técnicos sobre esto, vuelva a preguntar o diga 'profundizar'.*"
        else:
            footer = "\n\n✅ *Ha llegado al nivel máximo de detalle técnico disponible.*"

        return f"### {info['titulo']}\n\n{info['texto']}\n\n**Dato Clave:** {info['dato']}{footer}"

    # 3. CONTINUIDAD GENÉRICA (Si el usuario dice "sigue" sin mencionar tema)
    if any(x in prompt for x in ["mas", "más", "detalle", "sigue", "profundiza"]):
        tema = st.session_state.contexto_chat["tema_actual"]
        if tema:
            nivel = min(st.session_state.contexto_chat["nivel_profundidad"] + 1, 2)
            st.session_state.contexto_chat["nivel_profundidad"] = nivel
            info = db_multinivel[tema][nivel]
            return f"### {info['titulo']} (Detalle)\n\n{info['texto']}\n\n**Dato Clave:** {info['dato']}"

    # 4. FALLBACK
    return (
        "Entendido. Para profundizar necesito saber qué vector analizar:\n"
        "1. **Finanzas:** Deuda y Bonos.\n"
        "2. **Técnico:** Talara y Producción.\n"
        "3. **Entorno:** Riesgo País y WTI.\n\n"
        "Pruebe preguntando: *'Hablemos del Riesgo País'*."
    )

# --- 5. FUNCIONES DE DATOS ---
def get_talara_waterfall():
    return pd.DataFrame({'Concepto': ['Inicial', 'Cambios', 'EPC', 'Aux', 'Intereses', 'Final'], 'Monto': [1300, 2000, 1000, 800, 3400, 0], 'Medida': ["relative", "relative", "relative", "relative", "relative", "total"]})
def get_talara_funding():
    return pd.DataFrame({'Fuente': ['Bonos Corp.', 'Préstamos', 'Estado', 'Propios'], 'Monto_B': [4.3, 1.3, 1.5, 1.4]})
def get_dashboard_data():
    return pd.DataFrame({'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May'], '2024': [120, 135, 110, 140, 155], '2023': [110, 125, 115, 130, 140], 'Gastos': [115, 130, 125, 135, 145], 'EBITDA': [5, 5, -15, 5, 10]})
def get_rankings():
    return pd.DataFrame({'Unidad': ['Refinería', 'Oleoducto', 'Ventas', 'Admin'], 'Gasto_M': [850, 320, 150, 120], 'Cambio_Anual': ['+12%', '+5%', '-2%', '+1%']})
def get_csv_download():
    return get_dashboard_data().to_csv(index=False).encode('utf-8')
def layout_blanco(fig, titulo):
    fig.update_layout(title=dict(text=titulo, font=dict(color='white')), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), font_color="white")
    return fig

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 0 15px rgba(56,189,248,0.3);'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)
    st.markdown("### 👤 Admin Finanzas")
    st.caption("Perfil: Gerencia General")
    st.divider()
    if st.button("🏠 HOME"): navegar_a('home')
    if st.button("📊 DASHBOARD"): navegar_a('dashboard')
    if st.button("🤖 CHAT AI"): navegar_a('chat')
    
    st.markdown("### ⚙️ Ajustes")
    st.session_state.moneda = st.selectbox("Moneda", ["USD ($)", "PEN (S/.)"])
    st.download_button("📥 Data Financiera", data=get_csv_download(), file_name='reporte_petroperu.csv')
    
    st.write("")
    st.image(IMG_SIDEBAR_BANNER, caption="Talara Live Feed", use_column_width=True)

# ==================================================
# VISTAS PRINCIPALES
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú AI Hub")
    st.markdown("#### Panel de Control Estratégico")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(IMG_CARD_TALARA, use_column_width=True)
        st.markdown("### 🏭 Talara")
        if st.button("Ver Auditoría ➔", key="b1"): navegar_a('talara')
    with c2:
        st.image(IMG_CARD_FINANCE, use_column_width=True)
        st.markdown("### ⚡ Finanzas")
        if st.button("Ver Dashboard ➔", key="b2"): navegar_a('dashboard')
    with c3:
        st.image(IMG_CARD_AI, use_column_width=True)
        st.markdown("### 🤖 Asesor AI")
        if st.button("Consultar ➔", key="b3"): navegar_a('chat')

elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Talara")
    if st.button("⬅ Volver"): navegar_a('home')
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Retraso", "5 Años", "Crítico")
    m2.metric("Presupuesto", "$1.3 B", "2008")
    m3.metric("Costo Final", "$8.5 B", "+553%", delta_color="inverse")
    m4.metric("Operatividad", "100%", "Normal")
    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        df_w = get_talara_waterfall()
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=df_w['Medida'], x=df_w['Concepto'], y=df_w['Monto'],
            text=["+1.3", "+2.0", "+1.0", "+0.8", "+3.4", "8.5"], textposition="outside",
            connector={"line":{"color":"white"}}, decreasing={"marker":{"color":"green"}}, increasing={"marker":{"color":"#ff4444"}}, totals={"marker":{"color":"#33b5e5"}}
        ))
        st.plotly_chart(layout_blanco(fig, "Análisis de Sobrecosto (Billones $)"), use_container_width=True)
    with c2:
        st.markdown("#### Hitos")
        st.markdown("<div class='glass-card'>• 2014: Inicio EPC<br>• 2017: Emisión Bonos<br>• 2020: COVID<br>• 2024: Full Operation</div>", unsafe_allow_html=True)

elif st.session_state.pagina_actual == 'dashboard':
    mon = "$" if st.session_state.moneda == "USD ($)" else "S/."
    st.title(f"⚡ Monitor Financiero ({st.session_state.moneda})")
    if st.button("⬅ Volver"): navegar_a('home')
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Caja Disponible", f"{mon} 15.4 M", "-12%")
    k2.metric("WTI Crudo", "$76.50", "+4.5%")
    k3.metric("Deuda Total", f"{mon} 8.5 B", "+3.6%", delta_color="inverse")
    k4.metric("EBITDA", f"{mon} 120 M", "+8.2%")
    
    st.markdown("---")
    c1, c2 = st.columns([2,1])
    with c1:
        df = get_dashboard_data()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Mes'], y=df['2024'], name='Ingresos', marker_color='#00C851'))
        fig.add_trace(go.Scatter(x=df['Mes'], y=df['Gastos'], name='Gastos', line=dict(color='#ff4444')))
        st.plotly_chart(layout_blanco(fig, "Flujo de Caja Operativo"), use_container_width=True)
    with c2:
        df_r = get_rankings()
        fig = px.bar(df_r, y='Unidad', x='Gasto_M', orientation='h', color='Gasto_M', color_continuous_scale='Reds')
        st.plotly_chart(layout_blanco(fig, "Centros de Costo"), use_container_width=True)

# ==================================================
# VISTA 4: CHAT PRO (DRILL-DOWN)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Petrolito AI: Drill-Down Analysis")
    st.markdown("*Capacidad: Análisis Progresivo (Ejecutivo > Analítico > Técnico)*")
    
    if st.button("⬅ Volver"): navegar_a('home')

    chat_container = st.container()

    # Renderizar historial con estilo
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div class="bot-card">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 20px; margin-right: 10px;">🤖</span>
                        <b style="color: #38BDF8;">PETROLITO AI</b>
                    </div>
                    <div style="color: #E2E8F0; font-family: 'Segoe UI'; font-size: 15px; line-height: 1.6;">
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="text-align: right;"><div class="user-card">{msg["content"]}</div></div>""", unsafe_allow_html=True)

    # Input del usuario
    if prompt := st.chat_input("Consulte sobre Deuda, Talara o Macroeconomía..."):
        # Guardar
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Renderizar mensaje usuario (Hack visual para instantaneidad)
        with chat_container:
            st.markdown(f"""<div style="text-align: right;"><div class="user-card">{prompt}</div></div>""", unsafe_allow_html=True)

        # Procesar respuesta IA
        with chat_container:
            placeholder = st.empty()
            
            # Indicador de estado visual
            tema_actual = st.session_state.contexto_chat.get('tema_actual', 'General') or 'General'
            nivel_futuro = min(st.session_state.contexto_chat.get('nivel_profundidad', 0) + 1, 2)
            
            placeholder.markdown(f"""
            <div class='bot-card' style='text-align:center; color:#38BDF8; border: 1px dashed #38BDF8; opacity: 0.7;'>
                <i>🔍 Analizando vector: {tema_actual.upper()} | Profundidad: Nivel {nivel_futuro + 1}/3...</i>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1.0) # Pausa para simular cómputo
            
            # Lógica del Cerebro
            respuesta_ia = cerebro_financiero_avanzado(prompt)
            
            # Renderizar respuesta final
            placeholder.markdown(f"""
            <div class="bot-card">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 20px; margin-right: 10px;">🤖</span>
                    <b style="color: #38BDF8;">PETROLITO AI</b>
                </div>
                <div style="color: #E2E8F0; font-family: 'Segoe UI'; font-size: 15px; line-height: 1.6;">
                    {respuesta_ia}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
