import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú AI Hub", layout="wide", page_icon="🏭")

# --- 2. GESTIÓN DE NAVEGACIÓN Y ESTADO ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'
if 'moneda' not in st.session_state:
    st.session_state.moneda = "USD ($)"

# --- ESTADO INTELIGENCIA ARTIFICIAL (MEMORIA DE PROFUNDIDAD) ---
if "contexto_chat" not in st.session_state:
    # Rastrea: Tema actual y Nivel de profundidad (0=Ejecutivo, 1=Analítico, 2=Técnico)
    st.session_state.contexto_chat = {"tema_actual": None, "nivel_profundidad": 0}

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": (
            "Bienvenido. Soy Petrolito, su sistema de inteligencia financiera.\n\n"
            "He sido actualizado con una arquitectura de **Niveles de Profundidad** para evitar redundancias.\n"
            "Puedo detallar progresivamente información sobre:\n"
            "• **Deuda Estructural** (Bonos y CESCE)\n"
            "• **Operaciones Talara** (Flexicoking y Márgenes)\n"
            "• **Macroeconomía** (Riesgo País y WTI)\n\n"
            "¿Por dónde desea comenzar?"
        )
    }]

def navegar_a(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- 3. ESTILOS CSS (VISUAL IMPACT) ---
estilos_tech = """
<style>
    /* 1. FONDO GENERAL */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 23, 42, 0.94), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-technology-background-with-connecting-dots-lines_1048-12334.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    /* 2. SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    /* 3. TIPOGRAFÍA */
    h1, h2, h3, h4, h5, h6, p, li, div, span, label, b, i, strong, small { 
        color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* 4. ELEMENTOS UI */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1E293B !important; color: white !important; border: 1px solid #38BDF8;
    }
    .glass-card {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px; padding: 20px;
        backdrop-filter: blur(8px); margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%; background-color: #1E293B; color: #38BDF8 !important; 
        border: 1px solid #38BDF8; border-radius: 6px; padding: 10px; 
        font-weight: 600; text-transform: uppercase; transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #38BDF8; color: #0F172A !important; box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
    }

    /* 5. CHAT CARDS (NUEVO DISEÑO) */
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

    /* 6. AJUSTES MÉTRICAS */
    img { border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; opacity: 0.9; }
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

# --- 4. CEREBRO FINANCIERO AVANZADO (LÓGICA MULTINIVEL) ---
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

    # 1. DETECCIÓN DE TEMA
    tema_detectado = None
    if any(x in prompt for x in ["deuda", "bono", "banco", "pagar", "dinero"]): tema_detectado = "deuda"
    elif any(x in prompt for x in ["talara", "refineria", "refinería", "produccion", "flexicoking"]): tema_detectado = "talara"
    elif any(x in prompt for x in ["mercado", "sector", "wti", "precio", "gobierno", "mef", "riesgo", "nacional"]): tema_detectado = "macro"

    # 2. MÁQUINA DE ESTADOS (Profundidad Automática)
    if tema_detectado:
        estado = st.session_state.contexto_chat
        
        # Si el usuario sigue preguntando sobre lo mismo, profundizamos (Nivel 0 -> 1 -> 2)
        if estado["tema_actual"] == tema_detectado:
            nuevo_nivel = min(estado["nivel_profundidad"] + 1, 2)
        else:
            # Si cambia de tema, reseteamos al nivel ejecutivo (0)
            nuevo_nivel = 0
        
        # Actualizamos memoria
        st.session_state.contexto_chat = {"tema_actual": tema_detectado, "nivel_profundidad": nuevo_nivel}
        
        # Extraemos la info
        info = db_multinivel[tema_detectado][nuevo_nivel]
        
        # Mensaje guía
        footer = ""
        if nuevo_nivel < 2:
            footer = "\n\n🔽 *Para más detalles técnicos sobre esto, vuelva a preguntar o diga 'profundizar'.*"
        else:
            footer = "\n\n✅ *Ha llegado al nivel máximo de detalle técnico disponible en mi base.*"

        return f"### {info['titulo']}\n\n{info['texto']}\n\n**Dato Clave:** {info['dato']}{footer}"

    # 3. COMANDO DE CONTINUIDAD (Sin tema explícito)
    if any(x in prompt for x in ["mas", "más", "detalle", "sigue", "profundiza"]):
        tema = st.session_state.contexto_chat["tema_actual"]
        if tema:
            nivel = min(st.session_state.contexto_chat["nivel_profundidad"] + 1, 2)
            st.session_state.contexto_chat["nivel_profundidad"] = nivel
            info = db_multinivel[tema][nivel]
            return f"### {info['titulo']} (Detalle)\n\n{info['texto']}\n\n**Dato Clave:** {info['dato']}"

    # 4. FALLBACK INTELIGENTE
    return (
        "Entendido. Para utilizar mi capacidad de análisis multinivel, necesito que seleccione un vector:\n"
        "1. **Finanzas:** Deuda y Bonos.\n"
        "2. **Técnico:** Talara y Producción.\n"
        "3. **Entorno:** Riesgo País y WTI.\n\n"
        "Pruebe preguntando: *'Hablemos del Riesgo País'*."
    )

# --- 5. FUNCIONES DE DATOS COMPLETA ---
def get_talara_waterfall():
    return pd.DataFrame({
        'Concepto': ['Presupuesto Inicial', 'Actualización', 'Contrato EPC', 'Auxiliares', 'Intereses', 'Costo Final'],
        'Monto': [1300, 2000, 1000, 800, 3400, 0],
        'Medida': ["relative", "relative", "relative", "relative", "relative", "total"]
    })

def get_talara_funding():
    return pd.DataFrame({
        'Fuente': ['Bonos Corp.', 'Préstamos', 'Estado', 'Propios'],
        'Monto_B': [4.3, 1.3, 1.5, 1.4]
    })

def get_dashboard_data():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ingresos_2024 = [120, 135, 110, 140, 155, 160]
    ingresos_2023 = [110, 125, 115, 130, 140, 145] 
    gastos = [115, 130, 125, 135, 145, 150] 
    ebitda = [x - y for x, y in zip(ingresos_2024, gastos)]
    return pd.DataFrame({'Mes': meses, '2024': ingresos_2024, '2023': ingresos_2023, 'Gastos': gastos, 'EBITDA': ebitda})

def get_rankings():
    costos = pd.DataFrame({
        'Unidad': ['Refinería Talara', 'Oleoducto Norperuano', 'Planta Ventas Lima', 'Administración Central', 'Logística Selva'],
        'Gasto_M': [850, 320, 150, 120, 80],
        'Cambio_Anual': ['+12%', '+5%', '-2%', '+1%', '+4%']
    })
    return costos

def get_csv_download():
    df = get_dashboard_data()
    return df.to_csv(index=False).encode('utf-8')

def layout_blanco(fig, titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color='white', size=18)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', title_font=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', title_font=dict(color='white')),
        legend=dict(font=dict(color='white')),
        uniformtext_minsize=10, uniformtext_mode='hide'
    )
    return fig

# ==================================================
# BARRA LATERAL (COMPLETA)
# ==================================================
with st.sidebar:
    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); margin-bottom: 20px;'><img src='{IMG_LOGO}' width='100%'></div>", unsafe_allow_html=True)

    st.markdown("### 👤 Usuario Conectado")
    c_prof1, c_prof2 = st.columns([1, 3])
    with c_prof1:
        st.markdown(f"<img src='{IMG_USER}' style='width: 60px; height: 60px; border-radius: 50%; border: 2px solid #38BDF8;'>", unsafe_allow_html=True)
    with c_prof2:
        st.markdown("""
        <div style='padding-left: 5px;'>
            <div style='color: white; font-weight: bold; font-size: 16px;'>Admin Finanzas</div>
            <div style='color: #00C851; font-size: 12px; font-weight: bold;'>● En Línea</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    # Menú de Navegación Sidebar
    if st.button("🏠 HOME"): navegar_a('home')
    if st.button("🏭 TALARA"): navegar_a('talara')
    if st.button("⚡ DASHBOARD"): navegar_a('dashboard')
    if st.button("🤖 CHAT AI"): navegar_a('chat')

    st.markdown("### 🛠️ Ajustes")
    moneda = st.selectbox("Moneda", ["USD ($)", "PEN (S/.)"])
    st.session_state.moneda = moneda
    unidad = st.selectbox("Escala", ["Millones (MM)", "Miles (k)"])

    csv = get_csv_download()
    st.download_button("📥 Descargar Reporte", data=csv, file_name='reporte_petroperu.csv', mime='text/csv')
    
    st.write("") # Espacio
    st.markdown("### 🌍 Sostenibilidad")
    st.image(IMG_SIDEBAR_BANNER, caption="Talara - Feed en Vivo", use_column_width=True)
    st.caption("Monitoreo ambiental activo: ✅ Normal")

# ==================================================
# VISTA 1: HOME (TARJETAS VISUALES)
# ==================================================
if st.session_state.pagina_actual == 'home':
    st.title("🚀 Petroperú AI Hub: Plataforma Estratégica")
    st.markdown("#### Seleccione un módulo de inteligencia:")
    st.write("") 

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image(IMG_CARD_TALARA, use_column_width=True)
        st.markdown("### 🏭 Historia de Talara")
        st.info("Auditoría de deuda y construcción.")
        if st.button("Acceder ➔", key="b1"): navegar_a('talara')

    with c2:
        st.image(IMG_CARD_FINANCE, use_column_width=True)
        st.markdown("### ⚡ Monitor Financiero")
        st.info("KPIs de liquidez y EBITDA en vivo.")
        if st.button("Acceder ➔", key="b2"): navegar_a('dashboard')

    with c3:
        st.image(IMG_CARD_AI, use_column_width=True)
        st.markdown("### 🤖 Petrolito AI")
        st.info("Tu analista virtual con Deep Learning.")
        if st.button("Consultar ➔", key="b3"): navegar_a('chat')

# ==================================================
# VISTA 2: TALARA (DETALLE COMPLETO)
# ==================================================
elif st.session_state.pagina_actual == 'talara':
    st.title("🏭 Auditoría Visual: Nueva Refinería Talara")
    col_head, _ = st.columns([1, 5])
    with col_head:
        if st.button("⬅ Volver"): navegar_a('home')
    
    # Métricas Superiores
    st.markdown("#### 1. El Salto Cuántico del Presupuesto")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📅 Inicio", "2014", "5 años retraso")
    m2.metric("💰 Presupuesto", "$1.3 B", "2008")
    m3.metric("💸 Costo Final", "$8.5 B", "+553%", delta_color="inverse")
    m4.metric("📉 TIR", "2.8%", "Crítico")

    st.markdown("---")
    c_water, c_info = st.columns([2, 1])
    
    with c_water:
        st.markdown("**🔍 Anatomía del Sobrecosto**")
        df_w = get_talara_waterfall()
        fig_w = go.Figure(go.Waterfall(
            name = "Costo", orientation = "v", measure = df_w['Medida'], x = df_w['Concepto'], y = df_w['Monto'],
            text = ["+1.3", "+2.0", "+1.0", "+0.8", "+3.4", "8.5"], textposition = "outside",
            connector = {"line":{"color":"white"}}, decreasing = {"marker":{"color":"green"}},
            increasing = {"marker":{"color":"#ff4444"}}, totals = {"marker":{"color":"#33b5e5"}}
        ))
        fig_w = layout_blanco(fig_w, "")
        fig_w.update_traces(textfont_color='white')
        st.plotly_chart(fig_w, use_container_width=True)

    with c_info:
        st.markdown("#### 📖 Hitos Clave")
        st.markdown("""
        <div class="glass-card">
        <b>2014:</b> Firma EPC Técnicas Reunidas.<br><br>
        <b>2017:</b> Bonos $2,000M emitidos.<br><br>
        <b>2020:</b> Paralización COVID-19.<br><br>
        <b>2022:</b> Crisis de liquidez.<br><br>
        <b>2024:</b> Operación plena.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c_pie, c_time = st.columns(2)
    with c_pie:
        st.markdown("**🏦 Estructura de Financiamiento**")
        df_f = get_talara_funding()
        fig_p = px.pie(df_f, values='Monto_B', names='Fuente', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_p = layout_blanco(fig_p, "")
        fig_p.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(fig_p, use_container_width=True)

    with c_time:
        st.markdown("**⏳ Cronograma Real**")
        df_gantt = pd.DataFrame([
            dict(Task="Plan Original", Start='2014-01-01', Finish='2019-12-31', Color='Plan'),
            dict(Task="Ejecución Real", Start='2014-01-01', Finish='2023-12-31', Color='Real')
        ])
        fig_g = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Color", color_discrete_map={'Plan': '#00C851', 'Real': '#ff4444'})
        fig_g = layout_blanco(fig_g, "")
        st.plotly_chart(fig_g, use_container_width=True)

# ==================================================
# VISTA 3: DASHBOARD (DETALLE COMPLETO)
# ==================================================
elif st.session_state.pagina_actual == 'dashboard':
    moneda_sim = "$" if st.session_state.moneda == "USD ($)" else "S/."
    st.title(f"⚡ Monitor Financiero ({st.session_state.moneda})")
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅ Volver"): navegar_a('home')

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💵 Caja", f"{moneda_sim} 15.4 M", "-12%", border=True)
    k2.metric("🛢️ WTI", "$76.50", "+4.5%", border=True)
    k3.metric("📉 Deuda", f"{moneda_sim} 8.5 B", "+3.6%", border=True)
    k4.metric("📊 EBITDA", f"{moneda_sim} 120 M", "+8.2%", border=True)

    st.markdown("---")
    df_fin = get_dashboard_data()
    df_rank = get_rankings()

    c_main, c_side = st.columns([2, 1])
    with c_main:
        st.markdown("**Ingresos vs Gastos (YoY)**")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_fin['Mes'], y=df_fin['2024'], name='2024', marker_color='#00C851'))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['2023'], name='2023', line=dict(color='white', dash='dash')))
        fig_bar.add_trace(go.Scatter(x=df_fin['Mes'], y=df_fin['EBITDA'], name='EBITDA', fill='tozeroy', line=dict(color='#33b5e5', width=0), opacity=0.3))
        fig_bar = layout_blanco(fig_bar, "")
        fig_bar.update_layout(barmode='overlay', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_side:
        st.markdown("**🏆 Centros de Costo**")
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            y=df_rank['Unidad'], x=df_rank['Gasto_M'], orientation='h',
            marker_color=['#ff4444', '#ffbb33', '#00C851', '#33b5e5', '#aa66cc'],
            text=df_rank['Cambio_Anual'], textposition='auto', textfont_color='white'
        ))
        fig_rank = layout_blanco(fig_rank, "")
        fig_rank.update_layout(height=400)
        st.plotly_chart(fig_rank, use_container_width=True)

    st.markdown("---")
    c_risk, c_table = st.columns([1, 2])
    with c_risk:
        st.markdown("**Nivel de Riesgo**")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = 35, number = {'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': 'white'}, 'bar': {'color': "#ff4444"},
                'steps': [{'range': [0, 50], 'color': "rgba(0, 255, 0, 0.2)"}, {'range': [80, 100], 'color': "rgba(255, 0, 0, 0.2)"}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 85}
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with c_table:
        st.markdown("#### 📋 Pasivos Bancarios")
        df_bancos = pd.DataFrame({
            'Banco': ['Nación', 'Bonos Int.', 'Extranjero A', 'Local B'],
            'Deuda': [2500, 4000, 1200, 800], 'Tasa': ['4.5%', '7.2%', '6.1%', '5.8%'], 'Vence': ['2030', '2047', '2026', '2025']
        })
        st.dataframe(df_bancos, use_container_width=True, hide_index=True)

# ==================================================
# VISTA 4: CHAT (CON CEREBRO 4.0 & UI PRO)
# ==================================================
elif st.session_state.pagina_actual == 'chat':
    st.title("🤖 Petrolito AI: Drill-Down Analysis")
    st.markdown("*Capacidad: Análisis Progresivo (Ejecutivo > Analítico > Técnico)*")
    
    if st.button("⬅ Volver"): navegar_a('home')

    chat_container = st.container()

    # Historial Renderizado
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

    # Input Usuario
    if prompt := st.chat_input("Consulte sobre Deuda, Talara o Macroeconomía..."):
        # Guardar Msg Usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hack Visual: Mostrar inmediatamente el mensaje del usuario
        with chat_container:
            st.markdown(f"""<div style="text-align: right;"><div class="user-card">{prompt}</div></div>""", unsafe_allow_html=True)

        # Procesamiento IA
        with chat_container:
            placeholder = st.empty()
            
            # Indicador Visual de Profundidad (Status Bar)
            tema_actual = st.session_state.contexto_chat.get('tema_actual', 'General') or 'General'
            # Calculamos el nivel futuro solo para mostrarlo (la lógica real está en la función)
            nivel_futuro = min(st.session_state.contexto_chat.get('nivel_profundidad', 0) + 1, 2)
            
            placeholder.markdown(f"""
            <div class='bot-card' style='text-align:center; color:#38BDF8; border: 1px dashed #38BDF8; opacity: 0.7;'>
                <i>🔍 Analizando vector: {tema_actual.upper()} | Profundidad: Nivel {nivel_futuro + 1}/3...</i>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1.0) # Simulación de cómputo
            
            # Llamada al Cerebro Financiero Avanzado
            respuesta_ia = cerebro_financiero_avanzado(prompt)
            
            # Renderizar Respuesta Final
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
