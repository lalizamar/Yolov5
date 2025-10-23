}import streamlit as st
import random
import pandas as pd
import time # Añadimos time para simular el proceso de "rastreo"

# --- 1. Mapeo Creativo de Clases YOLO a Fantasmas Tiernos ---
# Usamos una lista de "fantasmas" que serán detectados aleatoriamente.
GHOST_LIST = [
    "Fantasma Vagabundo", 
    "Minino Espectral",
    "Can Espectral",
    "Poción Olvidada",
    "Grimorio Moderno",
    "Espectro Glotón",
    "Mochila Flotante",
    "Zapato Volador",
    "Calcetín Desaparecido",
    "Brujita Novata",
    "Momia Amigable"
]

# --- 2. Inyección de CSS para la Estética "Cute Halloween" ---
def inject_cute_halloween_css():
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Creepster&family=Julee&display=swap');
            
            /* Colores Base: Pastel Halloween */
            :root {{
                --color-primary: #FFB347; /* Naranja Calabaza Pastel */
                --color-secondary: #C3B1E1; /* Lavanda Pastel */
                --color-background: #F8F8FF; /* Blanco Fantasma */
                --color-text: #4B0082; /* Índigo Oscuro */
                --color-accent: #E1A9D4; /* Rosa Chicle */
            }}

            /* Fondo de la Aplicación */
            .stApp {{
                background: linear-gradient(135deg, var(--color-background) 0%, var(--color-secondary) 100%);
                color: var(--color-text);
                font-family: 'Julee', cursive; /* Fuente tierna */
            }}

            /* Títulos */
            h1, h2, h3, h4 {{
                font-family: 'Creepster', cursive; /* Fuente spooky/divertida para títulos */
                color: var(--color-text);
                text-shadow: 2px 2px var(--color-primary);
                text-align: center;
                margin-top: 0.5em;
            }}
            
            /* Botón de la Cámara (Estilo Fantasma) */
            .stCameraInput > label, .stButton > button {{
                background-color: var(--color-accent);
                color: white;
                border: 3px solid var(--color-text);
                border-radius: 12px;
                padding: 10px 20px;
                box-shadow: 5px 5px 0px var(--color-primary);
                transition: all 0.2s;
            }}
            .stCameraInput > label:hover, .stButton > button:hover {{
                background-color: var(--color-primary);
                box-shadow: 2px 2px 0px var(--color-text);
                transform: translateY(2px);
            }}

            /* Sidebar */
            /* Eliminamos los selectores específicos de Streamlit para la barra lateral 
               ya que no se usa en la versión simplificada */

            /* Dataframe y Cajas de Información */
            .stDataFrame, .stAlert, .stInfo, .stWarning, .stSuccess {{
                border-radius: 10px;
                border: 2px solid var(--color-text);
                box-shadow: 3px 3px 0px var(--color-primary);
            }}

        </style>
    """, unsafe_allow_html=True)

# --- 3. Configuración de página Streamlit y CSS ---
st.set_page_config(
    page_title="Ghostly Glimpse",
    page_icon="👻",
    layout="wide"
)

inject_cute_halloween_css()

# --- 4. Título y Narrativa (Parte Creativa) ---
st.title("👻 Caza Fantasmas 'Cute' (Ghostly Glimpse)")
st.markdown(f"""
<div style='text-align: center; background-color: var(--color-accent); padding: 10px; border-radius: 10px; border: 2px solid var(--color-text); margin-bottom: 20px;'>
    <h3 style='font-family: "Julee", cursive; text-shadow: none; color: white;'>
        ¡Bienvenido, Cazador de Espectros! 🍬
    </h3>
    <p style='font-family: "Julee", cursive; color: white; margin-bottom: 0;'>
        Esta interfaz transforma tu cámara en un **simulador de espectrómetro de visión artificial** para detectar 
        presencias espectrales (¡fantasmas tiernos!). Al tomar una foto, nuestro "algoritmo simplificado" 
        simulará la captura de los más adorables y traviesos fantasmas de tu casa.
    </p>
</div>
""", unsafe_allow_html=True)


# --- 5. Lógica Principal de Simulación de Detección ---
# No necesitamos cargar el modelo. La aplicación está lista inmediatamente.

# Contenedor principal para la cámara y resultados
main_container = st.container()

with main_container:
    # Capturar foto con la cámara
    picture = st.camera_input("📸 Busca un fantasma y presiona el botón para capturar la imagen", key="camera")
    
    if picture:
        # Simular el proceso de "detección"
        with st.spinner("Rastreando firmas espectrales..."):
            time.sleep(2) # Espera para simular el procesamiento
        
        # --- SIMULACIÓN DE RESULTADOS ---
        # Decidimos cuántos fantasmas "detectar" (entre 1 y 5)
        num_ghosts = random.randint(1, 5)
        
        # Elegimos esos fantasmas aleatoriamente de la lista
        simulated_detections = random.choices(GHOST_LIST, k=num_ghosts)
        
        # Procesar los resultados simulados para el DataFrame
        category_count = {}
        for ghost in simulated_detections:
            category_count[ghost] = category_count.get(ghost, 0) + 1
        
        ghosts_detected = len(simulated_detections)

        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🖼️ Escena Espectral Capturada")
            # En esta versión simplificada, solo mostramos la imagen capturada (sin cajas dibujadas)
            st.image(picture, caption="Foto capturada", use_container_width=True)
            st.markdown(f"""
                <div style='text-align: center; color: var(--color-text); border: 2px dashed var(--color-primary); border-radius: 5px; padding: 10px;'>
                    **Nota de Simulación:** El algoritmo simplificado ha analizado esta escena.
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if ghosts_detected > 0:
                st.subheader(f"✨ ¡ÉXITO! {ghosts_detected} Espectros Encontrados")
                st.balloons() # Animación de celebración
                st.success(f"¡Has capturado {ghosts_detected} presencias espectrales! ¡Están por todas partes!")
            else:
                st.subheader("🌫️ Zona Despejada")
                st.info("No se detectaron fantasmas con esta sensibilidad. ¡Intenta en un lugar más espeluznante o ajusta los umbrales!")

            # Tabla resumida de la simulación
            summary_data = [{"Categoría Espectral": name, "Cantidad": count} for name, count in category_count.items()]
            df_summary = pd.DataFrame(summary_data)
            
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
            
            # Gráfico de barras de fantasmas
            st.subheader("Gráfico de Apariciones")
            st.bar_chart(df_summary.set_index('Categoría Espectral')['Cantidad'])
            
            # Mensaje de Confianza simulada (para mantener la estructura del informe)
            st.caption(f"Confianza simulada del rastreo: {random.uniform(0.70, 0.99):.2f}")

else:
    st.info("Apunta tu cámara a tu entorno y presiona 'Tomar foto' para comenzar la caza de fantasmas.")


# Información adicional y pie de página
st.markdown("---")
st.caption("""
**Acerca de la aplicación (Versión Simplificada)**: 
Esta interfaz es un trabajo de Interfaces Multimodales. Utiliza Streamlit para la entrada de cámara y presenta una **simulación creativa de la detección de objetos (YOLO)** para ilustrar el concepto de Visión Artificial sin requerir librerías complejas como PyTorch o OpenCV.
""")
