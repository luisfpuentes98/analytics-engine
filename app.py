import streamlit as st
import pandas as pd
import time

# 1. Configuración General
st.set_page_config(page_title="AnalyticsEngine", layout="wide")
st.title("🏛️ AnalyticsEngine: Big Data Analytics")

# Inicialización de Familias de Columnas (Paso A)
if 'Datos_Usuario' not in st.session_state:
    st.session_state.Datos_Usuario = {'ID': [], 'Nombre': [], 'Email': []}
if 'Datos_Geograficos' not in st.session_state:
    st.session_state.Datos_Geograficos = {'ID': [], 'Ciudad': [], 'Pais': []}
if 'Datos_Metricas' not in st.session_state:
    st.session_state.Datos_Metricas = {'ID': [], 'Gasto_Publicitario': [], 'Clics': []}

# 2. Sidebar de Ingesta (Paso A)
with st.sidebar:
    st.header("📥 Ingesta de Datos")
    with st.form("registro_form", clear_on_submit=True):
        st.subheader("Datos de Registro")
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        ciudad = st.text_input("Ciudad")
        pais = st.text_input("País")
        gasto = st.number_input("Gasto Publicitario ($)", min_value=0.0)
        clics = st.number_input("Número de Clics", min_value=0)
        
        if st.form_submit_button("Insertar en Familias"):
            new_id = len(st.session_state.Datos_Usuario['ID']) + 1
            st.session_state.Datos_Usuario['ID'].append(new_id)
            st.session_state.Datos_Usuario['Nombre'].append(nombre)
            st.session_state.Datos_Usuario['Email'].append(email)
            st.session_state.Datos_Geograficos['ID'].append(new_id)
            st.session_state.Datos_Geograficos['Ciudad'].append(ciudad)
            st.session_state.Datos_Geograficos['Pais'].append(pais)
            st.session_state.Datos_Metricas['ID'].append(new_id)
            st.session_state.Datos_Metricas['Gasto_Publicitario'].append(gasto)
            st.session_state.Datos_Metricas['Clics'].append(clics)
            st.success(f"✅ Registro {new_id} guardado con éxito.")

# 3. SISTEMA DE PESTAÑAS
tab_query, tab_analytics = st.tabs(["🔍 Consulta Selectiva", "📊 Tablero Analítico"])

with tab_query:
    st.header("Simulación de Lectura de Columnas")
    columnas_disponibles = ['Nombre', 'Email', 'Ciudad', 'Pais', 'Gasto_Publicitario', 'Clics']
    seleccion = st.multiselect("Selecciona columnas para leer del disco:", columnas_disponibles)
    
    if st.button("Ejecutar Consulta"):
        if seleccion:
            start_time = time.perf_counter()
            query_results = pd.DataFrame({'ID': st.session_state.Datos_Usuario['ID']})
            for col in seleccion:
                if col in st.session_state.Datos_Usuario: query_results[col] = st.session_state.Datos_Usuario[col]
                elif col in st.session_state.Datos_Geograficos: query_results[col] = st.session_state.Datos_Geograficos[col]
                elif col in st.session_state.Datos_Metricas: query_results[col] = st.session_state.Datos_Metricas[col]
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            st.success(f"⚡ Consulta completada en {duration_ms:.4f} ms")
            st.info(f"💡 Ahorro de I/O: Se ignoraron {len(
