import streamlit as st
import pandas as pd
import time

# 1. Configuración General
st.set_page_config(page_title="AnalyticsEngine", layout="wide")
st.title("🏛️ AnalyticsEngine: Almacenamiento por Columnas")

# Inicialización de Familias (Si no existen)
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
            st.success(f"✅ Registro {new_id} guardado.")

# 3. SISTEMA DE PESTAÑAS (Paso B y C)
tab_query, tab_analytics = st.tabs(["🔍 Consulta Selectiva", "📊 Tablero Analítico"])

with tab_query:
    st.header("Simulación de I/O por Columna")
    
    # Definimos todas las columnas disponibles (excepto ID que es llave)
    columnas_disponibles = ['Nombre', 'Email', 'Ciudad', 'Pais', 'Gasto_Publicitario', 'Clics']
    
    # REQUERIMIENTO B: Multiselect para elegir columnas 
    seleccion = st.multiselect("Selecciona las columnas que deseas leer del disco:", columnas_disponibles)
    
    if st.button("Ejecutar Consulta de Columnas"):
        if seleccion:
            # Iniciamos cronómetro para medir eficiencia 
            start_time = time.perf_counter()
            
            # Simulamos el "escaneo" selectivo: solo tocamos los diccionarios necesarios
            query_results = pd.DataFrame({'ID': st.session_state.Datos_Usuario['ID']})
            
            for col in seleccion:
                # El sistema busca en qué "archivo" (familia) está la columna
                if col in st.session_state.Datos_Usuario:
                    query_results[col] = st.session_state.Datos_Usuario[col]
                elif col in st.session_state.Datos_Geograficos:
                    query_results[col] = st.session_state.Datos_Geograficos[col]
                elif col in st.session_state.Datos_Metricas:
                    query_results[col] = st.session_state.Datos_Metricas[col]
            
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            
            # REQUERIMIENTO B: Mostrar tiempo e información de ahorro 
            st.success(f"⚡ Consulta completada en {duration_ms:.4f} ms")
            
            columnas_ignoradas = len(columnas_disponibles) - len(seleccion)
            st.info(f"💡 Ahorro de I/O: Se han ignorado {columnas_ignoradas} columnas del almacenamiento.")
            
            st.dataframe(query_results, use_container_width=True)
        else:
            st.warning("Selecciona al menos una columna para simular la lectura.")

with tab_analytics:
    st.info("Pestaña disponible en el siguiente paso (Paso C).")
