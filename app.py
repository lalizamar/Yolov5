import cv2
import streamlit as st
import numpy as np
import pandas as pd
import torch
import os
import sys

# --- 1. Mapeo Creativo de Clases YOLO a Fantasmas Tiernos ---
# Usamos algunas clases comunes del conjunto COCO de YOLOv5 para simular fantasmas.
# COCO Classes (Index: Name): 0: person, 16: cat, 17: dog, 39: bottle, 64: mouse, 67: cell phone, etc.
GHOST_MAPPING = {
    0: "Fantasma Vagabundo (Persona)", # Person
    16: "Minino Espectral (Gato)",    # Cat
    17: "Can Espectral (Perro)",      # Dog
    39: "Poción Olvidada (Botella)",  # Bottle
    67: "Grimorio Moderno (Móvil)",   # Cell phone
    # Todas las demás se mapearán a Fantasma Genérico
}
DEFAULT_GHOST = "Espectro Desconocido"

def get_ghost_name(class_index):
    """Devuelve el nombre temático del 'fantasma' basado en el índice de la clase original."""
    return GHOST_MAPPING.get(class_index, DEFAULT_GHOST)

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
            .css-1d391kg {{ /* Selector genérico de sidebar */
                background-color: var(--color-secondary);
                border-right: 5px solid var(--color-primary);
            }}

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

# Función para cargar el modelo YOLOv5
@st.cache_resource
def load_yolov5_model(model_path='yolov5s.pt'):
    try:
        # Importar yolov5
        import yolov5
        
        # Intentar cargar el modelo YOLOv5 (generalmente carga el modelo COCO)
        model = yolov5.load(model_path, weights_only=False)
        return model
    
    except Exception as e:
        st.error(f"❌ Error al cargar el espectrómetro de visión (modelo YOLOv5): {str(e)}")
        st.info("""
        Recomendaciones:
        1. Asegúrate de tener las librerías PyTorch y YOLOv5 instaladas y compatibles.
           Por ejemplo: `pip install torch==1.12.0 torchvision==0.13.0 yolov5==7.0.9`
        2. El sistema intentará descargar 'yolov5s.pt' si no se encuentra localmente.
        """)
        return None

# --- 4. Título y Narrativa (Parte Creativa) ---
st.title("👻 Caza Fantasmas 'Cute' (Ghostly Glimpse)")
st.markdown(f"""
<div style='text-align: center; background-color: var(--color-accent); padding: 10px; border-radius: 10px; border: 2px solid var(--color-text); margin-bottom: 20px;'>
    <h3 style='font-family: "Julee", cursive; text-shadow: none; color: white;'>
        ¡Bienvenido, Cazador de Espectros! 🍬
    </h3>
    <p style='font-family: "Julee", cursive; color: white; margin-bottom: 0;'>
        Esta interfaz transforma tu cámara en un espectrómetro de visión artificial, utilizando el poderoso algoritmo YOLO (You Only Look Once) para detectar 
        presencias espectrales (¡es decir, objetos comunes de tu entorno!) y nombrarlas con nuestra estética de Halloween Tierno. 
        Prepárate para capturar los más adorables y traviesos fantasmas de tu casa.
    </p>
</div>
""", unsafe_allow_html=True)


# Cargar el modelo
with st.spinner("Activando el Espectrómetro de Visión (Cargando YOLOv5)..."):
    model = load_yolov5_model()

# Si el modelo se cargó correctamente, configuramos los parámetros
if model:
    # Sidebar para los parámetros de configuración
    st.sidebar.title("Ajustes Espectrales")
    
    # Ajustar parámetros del modelo
    with st.sidebar:
        st.subheader('Sensibilidad de Detección')
        model.conf = st.slider('Umbral de Confianza Espectral', 0.0, 1.0, 0.25, 0.01)
        model.iou = st.slider('Umbral de Solapamiento (IoU)', 0.0, 1.0, 0.45, 0.01)
        st.caption(f"Confianza: {model.conf:.2f} | IoU: {model.iou:.2f}")
        
        # Opciones adicionales
        st.subheader('Filtros Avanzados')
        try:
            model.agnostic = st.checkbox('Ignorar Clasificación (Agnostic NMS)', False)
            model.multi_label = st.checkbox('Permitir Múltiples Detecciones por Caja', False)
            model.max_det = st.number_input('Máximo de Espectros a Capturar', 10, 2000, 1000, 10)
        except:
            st.warning("Algunas opciones avanzadas no están disponibles con esta configuración")
    
    # Contenedor principal para la cámara y resultados
    main_container = st.container()
    
    with main_container:
        # Capturar foto con la cámara
        picture = st.camera_input("📸 Busca un fantasma y presiona el botón para capturar la imagen", key="camera")
        
        if picture:
            # Procesar la imagen capturada
            bytes_data = picture.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Realizar la detección
            with st.spinner("Rastreando firmas espectrales..."):
                try:
                    results = model(cv2_img)
                except Exception as e:
                    st.error(f"Error durante el rastreo espectral: {str(e)}")
                    st.stop()
            
            # Parsear resultados
            try:
                predictions = results.pred[0]
                boxes = predictions[:, :4]
                scores = predictions[:, 4]
                categories = predictions[:, 5]
                
                # --- LÓGICA DE DETECCIÓN DE FANTASMAS ---
                ghosts_detected = categories.shape[0] > 0
                
                # Mostrar resultados
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🖼️ Escena Espectral Capturada")
                    # Renderizar las detecciones
                    results.render()
                    # Mostrar imagen con las detecciones
                    st.image(cv2_img, channels='BGR', use_container_width=True)
                
                with col2:
                    if ghosts_detected:
                        st.subheader(f"✨ ¡ÉXITO! {ghosts_detected} Espectros Encontrados")
                        st.balloons() # Animación de celebración
                        st.success(f"¡Has capturado {ghosts_detected} presencias espectrales! ¡Están por todas partes!")
                    else:
                        st.subheader("🌫️ Zona Despejada")
                        st.info("No se detectaron fantasmas con esta sensibilidad. ¡Intenta en un lugar más espeluznante o ajusta los umbrales!")

                    # Obtener nombres de etiquetas y aplicar el mapeo temático
                    category_count = {}
                    detailed_data = []

                    for i, category_tensor in enumerate(categories):
                        category_idx = int(category_tensor.item()) if hasattr(category_tensor, 'item') else int(category_tensor)
                        
                        # Aplicar mapeo de fantasma
                        ghost_label = get_ghost_name(category_idx)
                        
                        # Contar por el nombre del fantasma
                        if ghost_label in category_count:
                            category_count[ghost_label] += 1
                        else:
                            category_count[ghost_label] = 1

                        # Preparar datos detallados
                        confidence = scores[i].item()
                        x_min, y_min, x_max, y_max = boxes[i][:4].cpu().numpy().astype(int)
                        
                        detailed_data.append({
                            "Fantasma Detectado": ghost_label,
                            "Confianza (%)": f"{confidence * 100:.1f}%",
                            "Clase Original (YOLO)": model.names[category_idx],
                            "Ubicación (Px)": f"({x_min},{y_min}) - ({x_max},{y_max})"
                        })
                    
                    if detailed_data:
                        df = pd.DataFrame(detailed_data)
                        
                        # Tabla resumida
                        summary_data = [{"Categoría Espectral": name, "Cantidad": count} for name, count in category_count.items()]
                        df_summary = pd.DataFrame(summary_data)
                        st.dataframe(df_summary, use_container_width=True, hide_index=True)
                        
                        # Gráfico de barras de fantasmas
                        st.subheader("Gráfico de Apariciones")
                        st.bar_chart(df_summary.set_index('Categoría Espectral')['Cantidad'])

                        # Mostrar tabla detallada bajo un expansor
                        with st.expander("Ver Detalles de Detección (Debug)"):
                            st.dataframe(df, use_container_width=True)
                        
                    
            except Exception as e:
                st.error(f"Error al procesar los resultados: {str(e)}")
                st.stop()
else:
    st.error("No se pudo iniciar el espectrómetro. Por favor verifica las dependencias e inténtalo nuevamente.")
    st.stop()

# Información adicional y pie de página
st.markdown("---")
st.caption("""
**Acerca de la aplicación**: Esta interfaz utiliza el algoritmo YOLOv5 (You Only Look Once) para la detección de objetos, 
simulando la captura de 'fantasmas tiernos' como parte de un proyecto de interfaces multimodales.
""")
