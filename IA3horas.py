import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Petroperú Strategic AI", layout="wide", page_icon="🛢️")

# --- URLS DE IMÁGENES (Para impacto visual) ---
IMG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png"
IMG_REFINERIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Refiner%C3%ADa_de_Talara.jpg/1024px-Refiner%C3%ADa_de_Talara.jpg"
IMG_OPERACIONES = "https://live.staticflickr.com/65535/52668693626_0780566618_b.jpg" # Imagen genérica de industria/oleoducto

# --- DATA HISTÓRICA REAL (2014-2024) ---
def get_historical_context():
    # Datos aproximados basados en reportes públicos y memoria anual
    data = {
        'Año': [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'Deuda_Total_B_USD': [1.2, 3.0, 4.1, 5.2, 5.5, 5.8, 6.2, 6.5, 7.8, 8.2, 8.5],
        'Utilidad_Neta_M_USD': [150, 480, 220, 180, -50, 120, -220, 100, -280, -800, -650], # Aprox
        'Hito': [
            'Inicio PMRT', 'Inversión', 'Emisión Bonos', 'Avance 60%', 'Costos Operativos', 
            'Pre-Pandemia', 'COVID-19', 'Rebote', 'Crisis Liquidez', 'Rescate MEF', 'Reestructuración'
        ]
    }
    return pd.DataFrame(data)

# --- DATA SIMULADA TIEMPO REAL (Lo que ya tenías) ---
def get_realtime_data():
    days = 30
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days)
    wti_price = np.random.normal(75, 3, days)
    cash_flow = (wti_price * 0.8) - 10 + np.random.normal(0, 2, days)
    df = pd.DataFrame({'Fecha': dates, 'WTI_Price': wti_price, 'Flujo_Caja_M_USD': cash_flow})
    df['Dia_Index'] = np.arange(len(df))
    return df

# --- SIDEBAR ---
with st.sidebar:
    st.image(IMG_LOGO, width=180)
    st.markdown("### 🏢 Centro de Comando")
    
    st.info("Estado: **ALERTA NARANJA**")
    st.markdown("**Focos de Atención:**")
    st.caption("🔴 Deuda Estructural PMRT")
    st.caption("🔴 Liquidez Corto Plazo")
    st.caption("🟡 Volatilidad Crudo WTI")
    
    st.image(IMG_OPERACIONES, caption="Operaciones Oleoducto", use_column_width=True)
    
    st.markdown("---")
    st.write("Sistema v5.0 - Retroalimentado con data histórica 2014-2024.")

# --- TÍTULO E IMAGEN PRINCIPAL ---
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("🛢️ Petroperú: Intelligence Monitor")
    st.markdown("### Análisis Histórico, Proyección y Chatbot Financiero")
with col_header2:
    # Mostramos la refinería para impacto visual
    st.image(IMG_REFINERIA, caption="Nueva Refinería Talara", use_column_width=True)

# --- PESTAÑAS DEL SISTEMA ---
tab_history, tab_realtime, tab_chat = st.tabs(["📜 Historia (2014-2024)", "⚡ Tiempo Real & IA", "🤖 Asesor Financiero"])

# ==========================================
# TAB 1: ANÁLISIS HISTÓRICO (LA RETROALIMENTACIÓN)
# ==========================================
with tab_history:
    st.header("Evolución Financiera: La Década Crítica")
    df_hist = get_historical_context()
    
    # Gráfico Mixto: Deuda (Línea) vs Utilidad (Barras)
    fig_hist = go.Figure()
    
    # Barras de Utilidad/Pérdida
    fig_hist.add_trace(go.Bar(
        x=df_hist['Año'], 
        y=df_hist['Utilidad_Neta_M_USD'],
        name='Utilidad Neta (Millones USD)',
        marker_color=['green' if x > 0 else 'red' for x in df_hist['Utilidad_Neta_M_USD']]
    ))
    
    # Línea de Deuda
    fig_hist.add_trace(go.Scatter(
        x=df_hist['Año'], 
        y=df_hist['Deuda_Total_B_USD'],
        name='Deuda Total Acumulada (Billones USD)',
        yaxis='y2',
        line=dict(color='black', width=4, dash='dot'),
        mode='lines+markers'
    ))
    
    fig_hist.update_layout(
        title="Impacto del PMRT: Escalada de Deuda vs Resultados Netos",
        yaxis=dict(title="Utilidad/Pérdida (Millones USD)"),
        yaxis2=dict(title="Deuda Total ($ Billones)", overlaying='y', side='right'),
        legend=dict(x=0, y=1.1, orientation='h')
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Tabla de Hitos
    st.subheader("Hitos Clave Identificados por la IA")
    st.dataframe(df_hist[['Año', 'Hito', 'Deuda_Total_B_USD']].set_index('Año'), use_container_width=True)

# ==========================================
# TAB 2: TIEMPO REAL (EL CEREBRO)
# ==========================================
with tab_realtime:
    st.subheader("Monitoreo de Liquidez (Simulación en Vivo)")
    
    if st.button('🔄 Sincronizar Datos de Mercado'):
        df_rt = get_realtime_data()
        st.session_state.rt_data = df_rt
        st.success("Conexión establecida.")
    
    if 'rt_data' in st.session_state:
        df = st.session_state.rt_data
        
        # Regresión rápida
        model = LinearRegression()
        model.fit(df[['Dia_Index']], df['Flujo_Caja_M_USD'])
        trend = model.coef_[0]
        
        col1, col2, col3 = st.columns(3)
        last_val = df['Flujo_Caja_M_USD'].iloc[-1]
        
        col1.metric("Caja Disponible", f"${last_val:.2f} M")
        col2.metric("Tendencia Corto Plazo", f"{trend:.2f}", delta_color="off")
        
        status_color = "green" if trend > 0 else "red"
        col3.markdown(f"### Estado: :{status_color}[{'Recuperación' if trend > 0 else 'Contracción'}]")
        
        # Gráfico simple
        st.line_chart(df.set_index('Fecha')['Flujo_Caja_M_USD'])
    else:
        st.info("Presiona Sincronizar para ver datos en tiempo real.")

# ==========================================
# TAB 3: CHATBOT CON MEMORIA HISTÓRICA
# ==========================================
with tab_chat:
    st.markdown("### 💬 Consulta a la Base de Conocimiento (2014-2025)")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Tengo acceso a la historia financiera desde 2014 y datos actuales. ¿Pregunta sobre la deuda histórica o la liquidez de hoy?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ej: ¿Por qué subió la deuda en 2017?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        prompt_lower = prompt.lower()
        response = ""
        
        # Lógica del Chatbot (Ahora sabe historia)
        with st.spinner('Consultando memoria histórica...'):
            time.sleep(1)
            
            if "2014" in prompt_lower:
                response = "En 2014 se marca el inicio fuerte del **PMRT (Proyecto Modernización Refinería Talara)**. La deuda era manejable ($1.2B), pero aquí comenzaron los compromisos de inversión masivos."
            elif "2017" in prompt_lower or "bonos" in prompt_lower:
                response = "El 2017 fue clave: Petroperú emitió **bonos corporativos por $2,000 millones** en el mercado internacional para financiar la refinería. Esto disparó la carga de deuda a $5.2 Billones."
            elif "2020" in prompt_lower or "pandemia" in prompt_lower:
                response = "El 2020 fue desastroso. La demanda de combustible cayó por el COVID-19, generando pérdidas netas de **$220 millones** y aumentando el estrés de liquidez."
            elif "2022" in prompt_lower or "crisis" in prompt_lower:
                response = "En 2022 explotó la **crisis de liquidez**. Hubo problemas con la auditoría de PwC, se rebajó la calificación crediticia y se solicitó el primer rescate fuerte al MEF."
            elif "deuda" in prompt_lower:
                response = "La deuda ha crecido exponencialmente: de **$1.2B en 2014** a más de **$8.5B en 2024**. La causa principal es el costo final de la Nueva Refinería de Talara y los intereses acumulados."
            else:
                response = "Esa información requiere un análisis más profundo. Basado en la tendencia 2014-2024, sugiero enfocarse en la reestructuración de pasivos de corto plazo. ¿Quieres saber sobre el año 2017 o 2022?"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
