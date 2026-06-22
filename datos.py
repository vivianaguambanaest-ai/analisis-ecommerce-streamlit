import mysql.connector
import pandas as pd
import streamlit as st
# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
host="localhost",
user="root      ",
password="", 
database="bd_lavadora"
)              
df_clientes = pd.read_sql("SELECT * FROM cliente", con=conexion)
st.title("Unidad 2: Preparación de Datos")
st.dataframe(df_clientes)
st.header("Muestra las primeras filas del Dataframe")
st.dataframe(df_clientes)
st.header("Muestra las últimas filas del Dataframe")
st.dataframe(df_clientes.tail())
st.header("Muestra la información general del Dataframe")
st.write(df_clientes.info())
st.header("Muestra las estadísticas descriptivas del Dataframe")
st.dataframe(df_clientes.describe())
st.header("Muestra valores nulos por columna")
st.write(df_clientes.isnull().sum())
st.header("Muestra el número de filas y columnas del Dataframe")
st.write(df_clientes.shape)
st.header("Muestra el número de filas duplicadas en el Dataframe")
st.write(df_clientes.duplicated().sum())
st.header("Muestra los tipos de datos de cada columna")
st.dataframe(df_clientes.dtypes)
st.header("Muestra el número de valores únicos por columna")
st.dataframe(df_clientes.nunique())
st.title("Unidad 3: Limpieza de Datos")
st.header("1. identificar valores nulos")
st.write(df_clientes.isnull().sum())
st.header("Mostrar los registros con valores nulos")
st.dataframe(df_clientes[df_clientes.isnull().any(axis=1)])
st.header("2. Elimina filas con valores nulos")
df_clientes_limpio = df_clientes.dropna()
st.dataframe(df_clientes_limpio)
st.header("Reeplaza por un valor fijo")
df_clientes = df_clientes.fillna("Desconocido")
st.dataframe(df_clientes)
st.header("Reemplaza por la media de la columna")
df_clientes= df_clientes.fillna(df_clientes.mean(numeric_only=True))
st.dataframe(df_clientes)
st.header("3. Eliminar duplicados")
df_clientes = df_clientes.drop_duplicates()
st.dataframe(df_clientes)
st.header("4. Detectar Valores atipicos (Outliers)")
st.header("Agregar ventas con datos aleatoreos para mostrar outliers")
import numpy as np
np.random.seed(42)
df_clientes["ventas"] = np.random.randint(100, 1000, size=len
(df_clientes))
st.dataframe(df_clientes)
st.header("Mostrar el boxplot de ventas para detectar outliers")
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.boxplot(x=df_clientes["ventas"])
plt.title("Boxplot de Ventas")
plt.show()
st.pyplot(plt)
st.header("Eliminar outliers utilizando el método del rango intercuartílico (IQR)")
Q1 = df_clientes["ventas"].quantile(0.25)
Q3 = df_clientes["ventas"].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
df_clientes_sin_outliers = df_clientes[(df_clientes["ventas"] >= limite_inferior) & (df_clientes["ventas"] <= limite_superior)]
st.dataframe(df_clientes_sin_outliers)
st.header("5. Convertir tipos de datos")
df_clientes["ventas"] = df_clientes["ventas"].astype(float)
st.dataframe(df_clientes)
st.header("6. Renombrar columnas")
df_clientes_renombrado = df_clientes.rename(columns={"ventas": "Ventas"})
st.dataframe(df_clientes_renombrado)
st.header("7. Eliminar columnas innecesarias")
df_clientes_sin_columna = df_clientes.drop(columns=["ventas"])
st.dataframe(df_clientes_sin_columna)
st.title("Verificar Resultado final")
st.dataframe(df_clientes_sin_outliers.shape)
st.dataframe(df_clientes_sin_outliers.describe())
st.title("Guardar Datos Limpios ")
df_clientes_sin_outliers.to_csv("clientes_limpios.csv", index=False)
st.write("Datos limpios guardados en 'clientes_limpios.csv'")

