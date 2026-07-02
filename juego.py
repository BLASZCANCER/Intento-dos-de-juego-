import streamlit as st
import random
import math

# Configuración de página adaptativa (Debe ir al inicio)
st.set_page_config(
    page_title="TWD: AI Engine Mobile", 
    layout="centered",  # Centrado para mejor visualización en móviles
    initial_sidebar_state="collapsed"
)

# Estilos CSS inyectados para optimizar la visualización en pantallas táctiles
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 18px !important;
        border-radius: 10px;
    }
    .stTextInput>div>div>input {
        font-size: 16px !important; /* Evita que iOS haga zoom automático */
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# LÓGICA DEL MOTOR (Simulación e IA)
# =====================================================================
class MundoSimulado:
    def __init__(self, lat, lon, nombre_lugar, poblacion_pre_apocalipsis):
        self.lat = lat
        self.lon = lon
        self.nombre = nombre_lugar
        self.zombis_iniciales = math.floor(poblacion_pre_apocalipsis * 0.993)
        self.supervivientes_npc = math.floor(poblacion_pre_apocalipsis * 0.007)
        
    def obtener_estado_zona(self):
        return {
            "Zona": self.nombre,
            "Caminantes": f"{self.zombis_iniciales:,}",
            "NPCs detectados": f"{random.randint(1, max(1, self.supervivientes_npc // 100))}"
        }

class Personaje:
    def __init__(self, es_jugador=False):
        nombres = ["Rick", "Daryl", "Glenn", "Michonne", "Maggie", "Shane"] if es_jugador else ["Elena", "Carlos", "Javier", "Morgan"]
        roles = ["Ex-oficial", "Rastreador", "Médico", "Mecánico", "Civil"]
        psique = ["Líder pragmático", "Inestable por trauma", "Altruista", "Superviviente egoísta"]
        habilidades = ["Puntería", "Sigilo", "Medicina", "Combate"]
        
        self.nombre = random.choice(nombres) + (" (Tú)" if es_jugador else "")
        self.edad = random.randint(18, 60)
        self.rol_pre_virus = random.choice(roles)
        self.perfil_psicologico = random.choice(psique)
        self.habilidad_maestra = random.choice(habilidades)
        self.vida = 100
        self.cordura = random.randint(60, 100)

def lanzar_dado_narrativo():
    resultado_dado = random.randint(1, 20)
    if resultado_dado >= 12:
        return "CONSTRUCTIVO", resultado_dado, "Éxito. Logras adaptarte al entorno y avanzar."
    else:
        return "DESTRUCTIVO", resultado_dado, "Fallo. El entorno colapsa o aparecen caminantes."

# Inicialización de estado
if 'jugador' not in st.session_state:
    st.session_state.jugador = Personaje(es_jugador=True)
    st.session_state.mundo = MundoSimulado(33.7490, -84.3880, "Atlanta (Centro Urbano)", 500000)
    st.session_state.historial = ["Despiertas en un entorno desolado. El mundo cambió."]

# =====================================================================
# INTERFAZ GRÁFICA MÓVIL
# =====================================================================
st.title("☣️ TWD: AI WORLD ENGINE")

# Pestañas táctiles para separar la acción del estado del personaje
tab1, tab2, tab3 = st.tabs(["🎮 Juego", "👤 Personaje", "🌍 Mapa"])

with tab1:
    st.header("🖼️ Entorno Visual")
    modo_visual = st.segmented_control(
        "Modo Gráfico:", 
        ["Pixel Art RPG", "Panel de Cómic"], 
        default="Pixel Art RPG"
    )
    
    if modo_visual == "Pixel Art RPG":
        st.code(
            "=========================================\n"
            "[P] = Tú | [Z] = Zombi | [H] = Hospital\n"
            "=========================================\n"
            "[ ] [ ] [ ] [Z] [ ] [ ] [ ] [ ] [ ] [ ]\n"
            "[ ] [ ] [P] [ ] [ ] [ ] [Z] [ ] [ ] [ ]\n"
            "[ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [H] [ ]\n"
            "=========================================", 
            language="text"
        )
    else:
        st.markdown("> **[PANEL DE CÓMIC TEMPORAL]**\n> *Sombras marcadas estilo tinta. Un caminante golpea una reja.*")

    st.header("📖 Bitácora")
    # Mostrar las últimas 4 líneas del historial para no saturar la pantalla del celular
    for linea in st.session_state.historial[-4:]:
        st.write(linea)

    st.divider()
    
    # Control de entrada táctil
    accion_usuario = st.text_input("¿Qué haces?", placeholder="Ej: Registro el auto abandonado...")
    if st.button("Ejecutar Acción 🎲"):
        if accion_usuario:
            tipo, valor, desc = lanzar_dado_narrativo()
            resultado_accion = f"**Acción:** {accion_usuario} \n* Dado: {valor} ({tipo}) -> {desc}"
            st.session_state.historial.append(resultado_accion)
            st.rerun()

with tab2:
    st.header("👤 Tu Superviviente")
    st.write(f"**Nombre:** {st.session_state.jugador.nombre}")
    st.write(f"**Edad:** {st.session_state.jugador.edad} años")
    st.write(f"**Rol original:** {st.session_state.jugador.rol_pre_virus}")
    st.write(f"**Psique:** {st.session_state.jugador.perfil_psicologico}")
    st.write(f"**Especialidad:** {st.session_state.jugador.habilidad_maestra}")
    
    st.progress(st.session_state.jugador.vida / 100, text=f"Vida: {st.session_state.jugador.vida}%")
    st.progress(st.session_state.jugador.cordura / 100, text=f"Cordura: {st.session_state.jugador.cordura}%")

with tab3:
    st.header("🌍 Radar de Supervivencia")
    info_mundo = st.session_state.mundo.obtener_estado_zona()
    for k, v in info_mundo.items():
        st.write(f"**{k}:** {v}")
