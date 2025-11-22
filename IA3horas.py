import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# --- 1. CONFIGURACIÓN AMIGABLE ---
st.set_page_config(page_title="Portal Financiero Petroperú", layout="wide", page_icon="🇵🇪")

# --- 2. ESTILO CSS (CLEAN & CORPORATE) ---
# Usamos colores corporativos (Rojo Petroperú y Gris), bordes redondeados y sombras suaves.
custom_css = """
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #F5F7F9; /* Fondo gris muy suave */
    }

    /* Estilo de los contenedores (Tarjetas) */
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Botones personalizados */
    .stButton>button {
        background-color: #CE2029; /* Rojo Petroperú */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #A51920;
        transform: scale(1.02);
    }

    /* Títulos */
    h1, h2, h3 {
        color: #2C3E50;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #CE2029;
        font-weight: bold;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- DATOS (BACKEND) ---
def get_data():
    # Generamos datos simples para no complicar la demo
    fechas = pd.date_range(end=pd.Timestamp.now(), periods=30)
    caja = np.linspace(-50, 20, 30) + np.random.normal(0, 5, 30) # Simula recuperación leve
    return pd.DataFrame({'Fecha': fechas, 'Caja': caja})

# --- BARRA LATERAL (MENÚ SIMPLE) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Petroper%C3%fa_logo.svg/1200px-Petroper%C3%fa_logo.svg.png", width=180)
    st.markdown("### 📌 Menú Principal")
    
    # Navegación con Radio Button que parece menú
    opcion = st.radio(
        "Seleccione una opción:",
        ["🏠 Inicio", "📊 Ver Gráficos", "💬 Asistente Virtual"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.info("💡 **Ayuda:** Si tienes dudas sobre algún término, ve a la sección 'Asistente Virtual'.")

# --- LÓGICA DE PÁGINAS ---

# === PÁGINA 1: BIENVENIDA (HOME) ===
if "Inicio" in opcion:
    st.title("👋 ¡Bienvenido al Portal Financiero!")
    st.markdown("#### Información clara para tomar mejores decisiones.")
    
    st.markdown("""
    <div class="stCard">
        Este sistema te ayuda a visualizar el estado financiero de Petroperú de forma sencilla.
        No necesitas ser un experto para usarlo.
    </div>
    """, unsafe_allow_html=True)

    # Tarjetas de acceso rápido (Columnas)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830323.png", width=80) # Icono gráfico
        st.subheader("Estado Actual")
        st.caption("Revisa cómo va la caja y la deuda hoy.")
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80) # Icono robot
        st.subheader("Pregúntale a la IA")
        st.caption("¿Tienes dudas? Nuestro asistente te explica.")
        
    with col3:
        st.image("https://cdn-icons-png.flaticon.com/512/1584/1584892.png", width=80) # Icono alerta
        st.subheader("Alertas")
        st.caption("El sistema te avisará si hay riesgos.")

    st.success("✅ **Sistema Operativo:** Todos los servicios están funcionando correctamente.")

# === PÁGINA 2: GRÁFICOS (VISUAL) ===
elif "Gráficos" in opcion:
    st.title("📊 Tablero de Control")
    st.markdown("Aquí puedes ver la evolución del dinero disponible en la empresa.")
    
    # Botón grande y claro
    if st.button("🔄 Actualizar Datos Ahora"):
        st.toast("¡Datos actualizados con éxito!", icon="✅") # Notificación bonita
        time.sleep(1)

    df = get_data()
    ultimo_valor = df['Caja'].iloc[-1]

    # Métricas grandes con explicación (Tooltip)
    c1, c2 = st.columns(2)
    c1.metric(
        label="💰 Dinero en Caja (Millones USD)",
        value=f"${ultimo_valor:.2f} M",
        delta="1.5% vs ayer",
        help="Este es el dinero líquido disponible para pagar deudas hoy."
    )
    c2.metric(
        label="📉 Deuda Talara (Aprox)",
        value="$8,500 M",
        delta_color="off",
        help="Monto total adeudado por la construcción de la refinería."
    )

    # Gráfico limpio
    st.subheader("Evolución del último mes")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Caja'],
        mode='lines+markers',
        name='Flujo de Caja',
        line=dict(color='#CE2029', width=3), # Rojo corporativo
        fill='tozeroy',
        fillcolor='rgba(206, 32, 41, 0.1)' # Relleno suave
    ))
    fig.update_layout(
        plot_bgcolor='white',
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(gridcolor='#f0f0f0') # Rejilla muy suave
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Ver explicación del gráfico"):
        st.write("La línea roja muestra cuánto dinero tenemos. Si baja de 0, significa que estamos usando deuda para operar.")

# === PÁGINA 3: ASISTENTE (CHAT AMIGABLE) ===
elif "Asistente" in opcion:
    st.title("💬 Asistente Virtual")
    st.markdown("Hola, soy tu asistente financiero. No necesitas usar términos complicados, solo pregúntame.")

    # Chat container
    chat_container = st.container()

    # Historial
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy? Selecciona una opción abajo o escribe tu duda."}]

    with chat_container:
        for msg in st.session_state.messages:
            # Usamos avatares para que sea más visual
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

    # BOTONES DE PREGUNTAS RÁPIDAS (Para usuarios que no quieren escribir)
    st.markdown("###### Preguntas frecuentes (Haz clic para preguntar):")
    col_q1, col_q2, col_q3 = st.columns(3)
    
    pregunta_usuario = None
    
    if col_q1.button("¿Estamos en crisis?"):
        pregunta_usuario = "¿Estamos en crisis financiera?"
    if col_q2.button("Explícame la deuda"):
        pregunta_usuario = "Explícame la deuda de Talara de forma simple"
    if col_q3.button("¿Cuánto dinero hay?"):
        pregunta_usuario = "¿Cuál es el flujo de caja hoy?"

    # Input de texto (por si quieren escribir)
    input_texto = st.chat_input("O escribe tu pregunta aquí...")

    # Lógica unificada
    prompt = pregunta_usuario if pregunta_usuario else input_texto

    if prompt:
        # Mostrar lo que el usuario "dijo"
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user", avatar="🧑‍💻").write(prompt)

        # Respuesta amigable
        resp = ""
        with st.spinner('Consultando...'):
            time.sleep(1)
            p_low = prompt.lower()
            
            if "crisis" in p_low:
                resp = "Actualmente estamos en una situación delicada (Alerta Naranja). Tenemos mucha deuda por pagar, pero la refinería ya está produciendo. Es como tener una hipoteca grande: aprieta, pero tenemos casa nueva."
            elif "deuda" in p_low:
                resp = "Imagina que pedimos un préstamo muy grande para construir la nueva refinería. Debemos cerca de $8,500 millones. Ahora tenemos que vender mucho combustible para ir pagando esa tarjeta de crédito gigante."
            elif "dinero" in p_low or "caja" in p_low:
                resp = "Hoy tenemos el dinero justo para operar. Estamos vigilando cada gasto para no quedarnos sin efectivo para comprar crudo."
            else:
                resp = "Buena pregunta. Básicamente, estamos trabajando para estabilizar la economía de la empresa tras la construcción de Talara. ¿Quieres saber algo más?"

        st.session_state.messages.append({"role": "assistant", "content": resp})
        with chat_container:
            st.chat_message("assistant", avatar="🤖").write(resp)
