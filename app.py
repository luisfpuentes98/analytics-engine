import streamlit as st
import pandas as pd
import time

# 1. Configuración de la Aplicación
st.set_page_config(page_title="AnalyticsEngine", layout="wide")
st.title("🏛️ AnalyticsEngine: Almacenamiento por Columnas")
st.markdown("### Simulación de Base de Datos Orientada a Columnas (Cassandra Style)")

# 2. Inicialización de Familias de Columnas (Paso A)
# En NoSQL orientado a columnas, cada familia se guarda de forma independiente
if 'Datos_Usuario' not in st.session_state:
    st.session_state.Datos_Usuario = {'ID': [], 'Nombre': [], 'Email': []}
if 'Datos_Geograficos' not in st.session_state:
    st.session_state.Datos_Geograficos = {'ID': [], 'Ciudad': [], 'Pais': []}
if 'Datos_Metricas' not in st.session_state:
    st.session_state.Datos_Metricas = {'ID': [], 'Gasto_Publicitario': [], 'Clics': []}

# 3. Formulario Lateral de Inserción (Paso A)
with st.sidebar:
    st.header("📥 Ingesta de Datos")
    with st.form("registro_form", clear_on_submit=True):
        st.subheader("Usuario")
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        
        st.subheader("Geografía")
        ciudad = st.text_input("Ciudad")
        pais = st.text_input("País")
        
        st.subheader("Métricas")
        gasto = st.number_input("Gasto Publicitario ($)", min_value=0.0)
        clics = st.number_input("Número de Clics", min_value=0)
        
        if st.form_submit_button("Insertar en Familias"):
            new_id = len(st.session_state.Datos_Usuario['ID']) + 1
            
            # Insertamos en cada familia de columnas simultáneamente
            st.session_state.Datos_Usuario['ID'].append(new_id)
            st.session_state.Datos_Usuario['Nombre'].append(nombre)
            st.session_state.Datos_Usuario['Email'].append(email)
            
            st.session_state.Datos_Geograficos['ID'].append(new_id)
            st.session_state.Datos_Geograficos['Ciudad'].append(ciudad)
            st.session_state.Datos_Geograficos['Pais'].append(pais)
            
            st.session_state.Datos_Metricas['ID'].append(new_id)
            st.session_state.Datos_Metricas['Gasto_Publicitario'].append(gasto)
            st.session_state.Datos_Metricas['Clics'].append(clics)
            
            st.success(f"✅ Registro {new_id} guardado en todas las familias.")

# Vista previa de las familias (para verificar el Paso A)
st.info("Estado actual de las 'Familias de Columnas' en memoria:")
c1, c2, c3 = st.columns(3)
with c1:
    st.write("**Datos_Usuario**", pd.DataFrame(st.session_state.Datos_Usuario))
with c2:
    st.write("**Datos_Geograficos**", pd.DataFrame(st.session_state.Datos_Geograficos))
with c3:
    st.write("**Datos_Metricas**", pd.DataFrame(st.session_state.Datos_Metricas))
