import streamlit as st
import pandas as pd
import numpy as np
import time
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Petroperú AI Monitor", layout="wide")

st.title("🛢️ Petroperú: Monitor Financiero con IA")
st.markdown("### Sistema de Monitoreo y Predicción de Flujo de Caja en Tiempo Real")

# --- 1. SIMULACIÓN DE DATOS (EL "BACKEND") ---
# En la vida real, aquí conectarías a tu SQL/API
def get_realtime_data():
    # Simulamos datos de las últimas 24 horas (1 dato por hora)
    now = pd.Timestamp.now()
    timestamps = [now - pd.Timedelta(hours=i) for i in range(24)]
    timestamps.reverse()
    
    # Simulamos un flujo de caja (en millones USD) con cierta volatilidad
    # Base de 50M + variación aleatoria
    cash_flow = [50 + np.random.normal(0, 5) for _ in range(24)]
    
    df = pd.DataFrame({'Fecha': timestamps, 'Flujo_Caja_M_USD': cash_flow})
    df['Hora_Index'] = np.arange(len(df)) # Para que la IA entienda el tiempo como número
    return df

# --- 2. EL CEREBRO (LA IA) ---
def train_and_predict(df):
    # Entrenamos una regresión lineal simple con los datos actuales
    X = df[['Hora_Index']]
    y = df['Flujo_Caja_M_USD']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predecir la siguiente hora (Hora 25)
    next_hour = np.array([[24]]) 
    prediction = model.predict(next_hour)[0]
    
    # Calcular la tendencia (pendiente)
    trend = model.coef_[0]
    
    return prediction, trend, model

# --- 3. INTERFAZ DE STREAMLIT ---

# Botón para actualizar "Tiempo Real"
if st.button('🔄 Actualizar Datos (Simulación Tiempo Real)'):
    df = get_realtime_data()
    
    # Ejecutamos la IA
    prediction, trend, model = train_and_predict(df)
    
    # --- METRICAS KPI ---
    col1, col2, col3 = st.columns(3)
    
    # KPI 1: Último valor real
    last_val = df['Flujo_Caja_M_USD'].iloc[-1]
    col1.metric("💰 Flujo de Caja Actual", f"${last_val:.2f}M", delta_color="normal")
    
    # KPI 2: Predicción IA
    delta_pred = prediction - last_val
    col2.metric("🤖 Predicción IA (1h)", f"${prediction:.2f}M", f"{delta_pred:.2f}M", delta_color="inverse")
    
    # KPI 3: Estado del Sistema (Lógica de Alerta)
    if trend < -2:
        status = "🚨 CRÍTICO: Tendencia Negativa Fuerte"
        color_status = "red"
    elif trend < 0:
        status = "⚠️ PRECAUCIÓN: Tendencia a la baja"
        color_status = "orange"
    else:
        status = "✅ ESTABLE: Tendencia Positiva"
        color_status = "green"
        
    col3.markdown(f"**Estado IA:** :{color_status}[{status}]")

    # --- GRÁFICOS ---
    st.divider()
    
    # Crear gráfico interactivo con Plotly
    fig = go.Figure()
    
    # Línea de datos históricos
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Flujo_Caja_M_USD'], mode='lines+markers', name='Histórico Real'))
    
    # Línea de tendencia de la IA (Regresión)
    trend_line = model.predict(df[['Hora_Index']])
    fig.add_trace(go.Scatter(x=df['Fecha'], y=trend_line, mode='lines', name='Tendencia IA', line=dict(dash='dash')))
    
    # Punto futuro (Predicción)
    future_time = df['Fecha'].iloc[-1] + pd.Timedelta(hours=1)
    fig.add_trace(go.Scatter(x=[future_time], y=[prediction], mode='markers', marker=dict(color='red', size=12), name='Proyección Futura'))

    fig.update_layout(title="Análisis de Liquidez y Proyección", xaxis_title="Tiempo", yaxis_title="Millones USD")
    st.plotly_chart(fig, use_container_width=True)
    
    # --- DATA RAW ---
    with st.expander("Ver Datos Crudos"):
        st.dataframe(df)

else:
    st.info("Dale click a 'Actualizar Datos' para simular la entrada de información en vivo.")

# Footer chiquito
st.markdown("---")
st.caption("Desarrollado para Petroperú - Versión MVP 0.1")
