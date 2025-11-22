import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Petroperú AI Assistant", layout="wide", page_icon="🤖")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png", width=150)
    st.header("📉 Datos Maestros")
    st.info("Parámetros Financieros 2025")
    st.metric("Deuda LP", "$8.5 B", "Refinería Talara")
    st.markdown("---")
    st.write("Este sistema utiliza IA Generativa simulada para asistir en la toma de decisiones.")

# --- FUNCIONES MATEMÁTICAS (Backend) ---
def get_financial_data():
    days = 30
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days)
    wti_price = np.random.normal(75, 3, days)
    debt_obligations = np.random.normal(2, 0.1, days)
    cash_flow = (wti_price * 0.8) - (debt_obligations * 5) + np.random.normal(0, 2, days)
    df = pd.DataFrame({'Fecha': dates, 'WTI_Price': wti_price, 'Flujo_Caja_M_USD': cash_flow})
    df['Dia_Index'] = np.arange(len(df))
    return df

def train_model(df):
    model = LinearRegression()
    model.fit(df[['Dia_Index']], df['Flujo_Caja_M_USD'])
    return model

# --- ESTADO DE LA SESIÓN (MEMORIA DEL CHAT) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida por defecto
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hola. Soy el asistente financiero de Petroperú. Tengo acceso a los datos de tesorería y mercado en tiempo real. ¿En qué puedo ayudarte hoy?"
    })

if "data" not in st.session_state:
    st.session_state.data = get_financial_data()

# --- INTERFAZ PRINCIPAL ---
st.title("🛢️ Petroperú: Asistente Financiero Inteligente")

# Pestañas para separar Dashboard de Chat
tab1, tab2 = st.tabs(["📊 Dashboard de Control", "💬 Consultas a la IA (Modo Gemini)"])

# --- TAB 1: EL DASHBOARD (Lo que ya tenías) ---
with tab1:
    st.markdown("### Monitoreo en Tiempo Real")
    
    if st.button('🔄 Actualizar Datos de Mercado'):
        st.session_state.data = get_financial_data()
        st.success("Datos actualizados correctamente.")
    
    df = st.session_state.data
    model = train_model(df)
    
    # Gráfico rápido
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Flujo_Caja_M_USD'], fill='tozeroy', name='Flujo de Caja'))
    st.plotly_chart(fig, use_container_width=True)
    
    # KPIs rápidos
    col1, col2 = st.columns(2)
    col1.metric("Caja Actual", f"${df['Flujo_Caja_M_USD'].iloc[-1]:.2f}M")
    col2.metric("Tendencia", "Estable" if model.coef_[0] > 0 else "Bajista", delta_color="off")

# --- TAB 2: MODO GEMINI (EL CHATBOT) ---
with tab2:
    st.markdown("### 🤖 Chat con tus Finanzas")
    
    # 1. Mostrar historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 2. Input del usuario
    if prompt := st.chat_input("Escribe tu consulta aquí (Ej: ¿Cómo está la deuda?)..."):
        
        # Mostrar mensaje del usuario
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 3. LÓGICA DE RESPUESTA (Simulación de IA)
        # Aquí hacemos que parezca inteligente detectando palabras clave
        prompt_lower = prompt.lower()
        response = ""
        
        # Datos actuales para usar en la respuesta
        current_cash = st.session_state.data['Flujo_Caja_M_USD'].iloc[-1]
        
        with st.spinner('Analizando base de datos...'):
            time.sleep(1.5) # Simular que piensa
            
            if "hola" in prompt_lower or "buenos" in prompt_lower:
                response = "¡Hola! Estoy listo para analizar los estados financieros. Puedes preguntarme por la **deuda**, el **flujo de caja** o **proyecciones**."
                
            elif "deuda" in prompt_lower or "talara" in prompt_lower:
                response = f"Actualmente, la deuda estructural relacionada a la Nueva Refinería de Talara asciende a **$8,500 Millones**. Recomiendo vigilar el ratio de cobertura de intereses, ya que el flujo de caja actual de **${current_cash:.2f}M** podría estar presionado."
                
            elif "caja" in prompt_lower or "dinero" in prompt_lower or "liquidez" in prompt_lower:
                response = f"Al cierre de hoy, la liquidez disponible es de **${current_cash:.2f} Millones**. "
                if current_cash < 50:
                    response += "⚠️ **Alerta:** Este nivel es bajo. Sugiero activar líneas de crédito rotativas de inmediato."
                else:
                    response += "✅ **Estado:** El nivel es saludable para operaciones de corto plazo."
            
            elif "petróleo" in prompt_lower or "wti" in prompt_lower or "precio" in prompt_lower:
                response = "El precio del crudo muestra volatilidad. Recuerda que nuestra IA ha detectado que por cada dólar que baja el WTI, nuestro margen de refinación se reduce significativamente. ¿Deseas ver una simulación de impacto?"
            
            elif "riesgo" in prompt_lower or "peligro" in prompt_lower:
                response = "He calculado el **VaR (Value at Risk)**. Existe un 15% de probabilidad de que necesitemos inyección de capital del MEF si el petróleo cae por debajo de $70 esta semana."
                
            else:
                response = "Interesante pregunta. Basado en mis modelos de regresión lineal, sugiero mantener cautela en el gasto operativo (OPEX) hasta confirmar la tendencia de la próxima semana. ¿Quieres que genere un reporte detallado?"

        # Mostrar respuesta del asistente
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Guardar respuesta en historial
        st.session_state.messages.append({"role": "assistant", "content": response})
