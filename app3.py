import streamlit as st
import pandas as pd
import os

# Configuración inicial
st.set_page_config(page_title="Consulta Cliente Agrupado", layout="centered")
st.title("🔍 Consulta Cliente Agrupado / ID Negociación")

# Ruta del archivo persistente
RUTA_EXCEL = "archivo_guardado.xlsx"

# Columnas a mostrar
columnas_mostrar = [
    "ID NEGOCIACION",
    "ESTADO ID NEGOCIACION",
    "NIT CLIENTE",
    "CLIENTE AGRUPADO",
    "ID LINEA SERVICIO",
    "LINEA_UAI"
]

# Carga del archivo si el usuario sube uno nuevo
archivo_subido = st.file_uploader("📂 Sube el archivo Excel (hoja 'Maestro')", type=["xlsx", "xls"])

if archivo_subido:
    # Guardamos el archivo localmente
    with open(RUTA_EXCEL, "wb") as f:
        f.write(archivo_subido.getbuffer())
    st.success("✅ Archivo cargado y guardado exitosamente.")

# Verificar si hay un archivo disponible para leer
if os.path.exists(RUTA_EXCEL):
    try:
        df = pd.read_excel(RUTA_EXCEL, sheet_name="Maestro", dtype=str)
        st.info(f"📁 Usando archivo: {RUTA_EXCEL}")

        # Validar columnas
        columnas_faltantes = [col for col in columnas_mostrar if col not in df.columns]
        if columnas_faltantes:
            st.error(f"❌ Faltan las siguientes columnas en la hoja 'Maestro': {columnas_faltantes}")
        else:
            # Tipo de búsqueda
            opcion = st.radio("Selecciona tipo de búsqueda:", ["Por NIT CLIENTE", "Por ID NEGOCIACION"])

            if opcion == "Por NIT CLIENTE":
                nit = st.text_input("🔢 Ingresa el NIT del cliente:")
                if nit:
                    resultados = df[df["NIT CLIENTE"] == nit][columnas_mostrar]
                    if not resultados.empty:
                        st.write("✅ Resultados encontrados:")
                        st.dataframe(resultados)
                    else:
                        st.warning("⚠️ No se encontraron resultados para ese NIT.")

            elif opcion == "Por ID NEGOCIACION":
                id_neg = st.text_input("🆔 Ingresa el ID de negociación:")
                if id_neg:
                    resultados = df[df["ID NEGOCIACION"] == id_neg][columnas_mostrar]
                    if not resultados.empty:
                        st.write("✅ Resultados encontrados:")
                        st.dataframe(resultados)
                    else:
                        st.warning("⚠️ No se encontraron resultados para ese ID de negociación.")

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
else:
    st.warning("⚠️ No se ha cargado ningún archivo aún.")

