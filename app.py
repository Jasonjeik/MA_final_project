import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import pickle

# Cargar datos y modelo
df = pd.read_csv("database.csv")  # Base de datos de cargas
with open("random_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Función para generar carga aleatoria
def generar_carga():
    carga = df.sample(1).iloc[0]
    return carga

# Página 1: Vista Cliente
def vista_cliente():
    st.title("Vista Cliente")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.subheader("Generar Carga")
        if st.button("Generar Carga"):
            carga = generar_carga()
            st.session_state["carga"] = carga

        if "carga" in st.session_state:
            st.image(f"images/{st.session_state['carga']['Equip']}.png", caption=st.session_state['carga']['Equip'])

    with col2:
        st.subheader("Mapa")
        if "carga" in st.session_state:
            mapa = folium.Map(location=[st.session_state['carga']['LatOrigin'], st.session_state['carga']['LngOrigin']], zoom_start=6)
            folium.Marker([st.session_state['carga']['LatOrigin'], st.session_state['carga']['LngOrigin']], tooltip="Origen").add_to(mapa)
            folium.Marker([st.session_state['carga']['LatDestination'], st.session_state['carga']['LngDestination']], tooltip="Destino").add_to(mapa)
            folium_static(mapa)

    with col3:
        st.subheader("Detalles")
        if "carga" in st.session_state:
            st.write(f"Weight: {st.session_state['carga']['Weight']} lbs")
            st.write(f"Size: {st.session_state['carga']['Size']} cu ft")
            distancia = np.random.randint(100, 500)  # Aquí podrías calcular la distancia real
            st.write(f"Distancia: {distancia} km")
            st.session_state["distancia"] = distancia

# Página 2: Vista Dueño del Vehículo
def vista_dueño():
    st.title("Vista Dueño del Vehículo")
    if "carga" in st.session_state:
        vista_cliente()
        st.subheader("Valor de la Carga")
        if "distancia" in st.session_state:
            features = [[st.session_state['carga']['Weight'], st.session_state['carga']['Size'], st.session_state['distancia']]]
            pred = model.predict(features)[0]
            min_value = pred * 0.9
            max_value = pred * 1.1
            st.write(f"Valor mínimo: ${min_value:.2f}")
            st.write(f"Valor máximo: ${max_value:.2f}")
    else:
        st.write("Por favor, genere una carga primero en la página de Cliente.")

# Menú de Navegación
pagina = st.sidebar.selectbox("Selecciona una página", ["Vista Cliente", "Vista Dueño del Vehículo"])

if pagina == "Vista Cliente":
    vista_cliente()
elif pagina == "Vista Dueño del Vehículo":
    vista_dueño()
