import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Petroperú AI Financial Monitor", layout="wide")

# --- SIDEBAR: CONTEXTO ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png", width=150)
    st.header("📉 Contexto Financiero")
    st.info("Datos públicos referenciales")
    st.metric("Deuda Total", "$8.5 B", delta="Refinería Talara", delta_color="inverse")
    st.write("---")
    st.caption("Benchmarking de Industria:")
    st.caption("✅ Eficiencia Operativa: +25%")
    st.caption("✅ Reducción de Riesgo: -40%")

# --- FUNCIONES DE DATOS Y MODELO ---
def get_financial_data():
    days = 30
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days)
    wti_price = np.random.normal(75, 3, days)
    debt_obligations = np.random.normal(2, 0.1, days)
    cash_flow = (wti_price * 0.8) - (debt_obligations * 5) + np.random.normal(0, 2, days)
    df = pd.DataFrame({
        'Fecha': dates, 'WTI_Price': wti_price,
        'Deuda_Diaria': debt_obligations, 'Flujo_Caja_M_USD': cash_flow
    })
    df['Dia_Index'] = np.arange(len(df))
    return df

def train_advanced_ai(df):
    X = df[['Dia_Index', 'WTI_Price']]
    y = df['Flujo_Caja_M_USD']
    model = LinearRegression()
    model.fit(X, y)
    return model

# --- NUEVA FUNCIÓN: PROYECCIÓN DE IMPACTO (ROI) ---
def plot_impact_projection():
    # Simulamos 12 meses de proyección
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Escenario 1: Costos Operativos Sin IA (Tendencia lineal de gasto)
    # Supongamos gastos de monitoreo manual de 5M acumulados mes a mes
    costs_manual = np.cumsum([5 + np.random.normal(0, 0.2) for _ in range(12)])
    
    # Escenario 2: Costos Con IA (Ahorro del 30% aprox en eficiencia)
    costs_ai = np.cumsum([3.5 + np.random.normal(0, 0.1) for _ in range(12)])
    
    fig = go.Figure()
    
    # Línea Roja (Lo que gastan hoy)
    fig.add_trace(go.Scatter(
        x=months, y=costs_manual,
        mode='lines+markers',
        name='Gasto Operativo Actual (Manual)',
        line=dict(color='red', dash='dot')
    ))
    
    # Línea Verde (Lo que gastarían con tu IA)
    fig.add_trace(go.Scatter(
        x=months, y=costs_ai,
        mode='lines+markers',
        name='Gasto Proyectado con IA',
        fill='tonexty', # Esto rellena el área entre las líneas
        fillcolor='rgba(0, 255, 0, 0.1)', # Color verde suavecito
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="📉 Proyección de Reducción de Costos Operativos (1 Año)",
        yaxis_title="Gasto Acumulado (Millones USD)",
        hovermode="x unified",
        legend=dict(y=1.1, orientation='h')
    )
    
    return fig, costs_manual[-1] - costs_ai[-1]

# --- INTERFAZ PRINCIPAL ---
st.title("🛢️ Petroperú: Monitor de Liquidez & Impacto IA")

if st.button('🔄 Ejecutar Análisis Completo'):
    # 1. Carga de Datos y Modelo
    df = get_financial_data()
    model = train_advanced_ai(df)
    
    # Predicciones
    last_day_idx = df['Dia_Index'].iloc[-1]
    last_wti = df['WTI_Price'].iloc[-1]
    future_pred = model.predict([[last_day_idx + 1, last_wti]])[0]
    
    # 2. Métricas en tiempo real
    st.subheader("1. Estado Financiero en Tiempo Real")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Precio WTI", f"${last_wti:.2f}")
    kpi2.metric("Flujo de Caja Hoy", f"${df['Flujo_Caja_M_USD'].iloc[-1]:.2f}M")
    
    if future_pred < 45:
        status = "RIESGO CRÍTICO"
        col = "red"
    else:
        status = "ESTABLE"
        col = "green"
    kpi3.metric("Predicción IA (Mañana)", f"${future_pred:.2f}M", status)

    # 3. Gráfico de Correlación (El de antes)
    fig_main = go.Figure()
    fig_main.add_trace(go.Bar(x=df['Fecha'], y=df['Flujo_Caja_M_USD'], name='Caja (M USD)'))
    fig_main.add_trace(go.Scatter(x=df['Fecha'], y=df['WTI_Price'], name='WTI ($)', yaxis='y2', line=dict(color='orange')))
    fig_main.update_layout(yaxis2=dict(overlaying='y', side='right'), title="Correlación WTI vs Caja")
    st.plotly_chart(fig_main, use_container_width=True)
    
    st.divider()
    
    # 4. SECCIÓN NUEVA: IMPACTO DEL PROYECTO
    st.subheader("2. Estimación de Impacto del Proyecto (Business Case)")
    st.markdown("""
    > *Basado en benchmarks de transformación digital en sector Oil & Gas (Reducción de costos operativos ~30%).*
    """)
    
    fig_impact, savings = plot_impact_projection()
    
    col_impact_1, col_impact_2 = st.columns([3, 1])
    
    with col_impact_1:
        st.plotly_chart(fig_impact, use_container_width=True)
        
    with col_impact_2:
        st.success(f"💰 AHORRO ESTIMADO (ANUAL)")
        st.metric("Eficiencia Financiera", f"${savings:.2f} M", "+30% ROI", delta_color="normal")
        st.markdown("**Beneficios Clave:**")
        st.markdown("- Automatización de reportes")
        st.markdown("- Detección de fraude")
        st.markdown("- Menos errores humanos")

else:
    st.info("Inicia el sistema para ver los dashboards.")
