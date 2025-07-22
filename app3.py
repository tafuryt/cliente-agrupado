import streamlit as st
import pandas as pd
import os

# Configuración
st.set_page_config(page_title="Consulta Cliente Agrupado", layout="centered")
st.title("🔍 Consulta Cliente Agrupado / ID Negociación")

# Ruta donde guardar el archivo subido
RUTA_EXCEL = "archivo_actual.xlsx"

# Subir nuevo archivo
nuevo_archivo = st.file_uploader("📂 Sube el archivo Excel (hoja 'Maestro') si deseas reemplazar el actual", type=["xlsx", "xls"])

if nuevo_archivo:
    with open(RUTA_EXCEL, "wb") as f:
        f.write(nuevo_archivo.getbuffer())
    st.success("✅ Archivo actualizado exitosamente.")

# Cargar datos desde archivo persistente
if os.path.exists(RUTA_EXCEL):
    try:
        df = pd.read_excel(RUTA_EXCEL, sheet_name="Maestro", dtype=str)
        st.info(f"📁 Usando archivo guardado: {RUTA_EXCEL}")

        columnas_mostrar = [
            "ID NEGOCIACION",
            "ESTADO ID NEGOCIACION",
            "NIT CLIENTE",
            "CLIENTE AGRUPADO",
            "ID LINEA SERVICIO",
            "LINEA_UAI"
        ]

        # Validación
        columnas_faltantes = [col for col in columnas_mostrar if col not in df.columns]
        if columnas_faltantes:
            st.error(f"❌ Faltan columnas en el archivo: {columnas_faltantes}")
        else:
            # Búsqueda
            opcion = st.radio("Buscar por:", ["NIT CLIENTE", "ID NEGOCIACION"])

            if opcion == "NIT CLIENTE":
                nit = st.text_input("🔢 NIT del cliente:")
                if nit:
                    resultados = df[df["NIT CLIENTE"] == nit][columnas_mostrar]
                    st.dataframe(resultados if not resultados.empty else "⚠️ No se encontraron resultados.")
            else:
                id_neg = st.text_input("🆔 ID de negociación:")
                if id_neg:
                    resultados = df[df["ID NEGOCIACION"] == id_neg][columnas_mostrar]
                    st.dataframe(resultados if not resultados.empty else "⚠️ No se encontraron resultados.")
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
else:
    st.warning("⚠️ No se ha cargado ningún archivo aún.")
