import streamlit as st
import pandas as pd
import plotly.express as px
import sweetviz as sv
import os

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Análisis Descriptivo E-commerce",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# CARGA DE DATOS
# --------------------------------------------------

@st.cache_data
def cargar_datos():
    df = pd.read_excel(
        "amazon_ecommerce_1M.csv.xlsx",
        nrows=10000
    )
    return df

df = cargar_datos()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.image("logo.png", width=180)

st.sidebar.title("📊 Menú")

opcion = st.sidebar.radio(
    "Seleccione una sección",
    [
    "🏠 Inicio",
    "📁 Dataset",
    "🔍 Calidad de Datos",
    "📈 Estadísticas Descriptivas",
    "📊 Visualizaciones",
    "📑 Reporte Sweetviz",
    "📝 Conclusiones"
  ]
)

# --------------------------------------------------
# INICIO
# --------------------------------------------------

if opcion == "🏠 Inicio":

    st.image("logo.png", width=220)

    st.title("📊 Análisis Descriptivo de Datos E-commerce")

    st.markdown("""
    ### Instituto Superior Universitario Tecnológico del Azuay

    **Carrera:** Big Data

    **Estudiante:** Viviana Guambaña

    **Docente:** Ing. Verónica Chimbo
    """)

    st.markdown("---")

    st.subheader("📌 Indicadores Generales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Registros", f"{df.shape[0]:,}")
    col2.metric("Variables", df.shape[1])
    col3.metric("Valores Nulos", int(df.isnull().sum().sum()))
    col4.metric("Duplicados", int(df.duplicated().sum()))

    st.markdown("---")

    st.subheader("📈 Indicadores Clave")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Precio Promedio",
        f"${df['price'].mean():.2f}"
    )

    col2.metric(
        "⭐ Rating Promedio",
        round(df["rating"].mean(), 2)
    )

    col3.metric(
        "📦 Productos Devueltos",
        int(df["is_returned"].sum())
    )

    col4.metric(
    "🚚 Tiempo Promedio Entrega",
    f"{df['shipping_time_days'].mean():.2f} días"
)

    st.markdown("---")

    st.subheader("Descripción del Proyecto")

    st.write("""
    Esta aplicación permite adquirir, visualizar y analizar un conjunto de datos
    de comercio electrónico mediante técnicas de análisis descriptivo.
    La información proviene de un archivo Excel que contiene registros
    relacionados con productos, categorías, precios, descuentos,
    métodos de pago, calificaciones y estados de entrega.
    """)

# --------------------------------------------------
# DATASET
# --------------------------------------------------

elif opcion == "📁 Dataset":

    st.title("📁 Dataset")

    st.subheader("Vista previa")

    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Dimensiones")

    st.write(f"Filas: {df.shape[0]}")
    st.write(f"Columnas: {df.shape[1]}")

    st.subheader("Variables")

    st.write(df.columns.tolist())

# --------------------------------------------------
# CALIDAD DE DATOS
# --------------------------------------------------

elif opcion == "🔍 Calidad de Datos":

    st.title("🔍 Calidad de Datos")

    st.subheader("Tipos de Datos")

    tipos = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": df.dtypes.astype(str)
    })

    st.dataframe(tipos, use_container_width=True)

    st.subheader("Valores Nulos")

    nulos = pd.DataFrame({
        "Variable": df.columns,
        "Valores Nulos": df.isnull().sum()
    })

    st.dataframe(nulos, use_container_width=True)

    st.subheader("Duplicados")

    st.metric(
        "Registros duplicados",
        int(df.duplicated().sum())
    )

# --------------------------------------------------
# ESTADÍSTICAS
# --------------------------------------------------

elif opcion == "📈 Estadísticas Descriptivas":

    st.title("📈 Estadísticas Descriptivas")

    st.dataframe(
    df.describe().T,
    use_container_width=True
)

# --------------------------------------------------
# VISUALIZACIONES
# --------------------------------------------------

elif opcion == "📊 Visualizaciones":

    st.title("📊 Dashboard Visual de E-commerce")

    # -------------------------
    # Categorías
    # -------------------------

    st.subheader("🛍️ Productos por Categoría")

    categoria = df["category"].value_counts().reset_index()
    categoria.columns = ["category", "count"]

    fig1 = px.bar(
        categoria,
        x="category",
        y="count",
        color="category",
        title="Cantidad de Productos por Categoría",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -------------------------
    # Métodos de pago
    # -------------------------

    st.subheader("💳 Métodos de Pago")

    pagos = df["payment_method"].value_counts().reset_index()
    pagos.columns = ["payment_method", "count"]

    fig2 = px.bar(
        pagos,
        x="payment_method",
        y="count",
        color="payment_method",
        title="Métodos de Pago Utilizados",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------
    # Estado entrega
    # -------------------------

    st.subheader("🚚 Estado de Entrega")

    entrega = df["delivery_status"].value_counts().reset_index()
    entrega.columns = ["delivery_status", "count"]

    fig3 = px.bar(
        entrega,
        x="delivery_status",
        y="count",
        color="delivery_status",
        title="Estado de Entrega de los Pedidos",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -------------------------
    # Top marcas
    # -------------------------

    st.subheader("🏆 Top 10 Marcas")

    top_marcas = (
        df["brand"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_marcas.columns = ["brand", "count"]

    fig4 = px.bar(
        top_marcas,
        x="brand",
        y="count",
        color="brand",
        title="Top 10 Marcas con Más Productos",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    st.plotly_chart(fig4, use_container_width=True)

    # -------------------------
    # Precios
    # -------------------------

    st.subheader("💰 Distribución de Precios")

    fig5 = px.histogram(
        df,
        x="price",
        nbins=30,
        title="Distribución de Precios",
        color_discrete_sequence=["#2563EB"]
    )

    st.plotly_chart(fig5, use_container_width=True)

    # -------------------------
    # Ratings
    # -------------------------

    st.subheader("⭐ Distribución de Calificaciones")

    fig6 = px.histogram(
        df,
        x="rating",
        nbins=20,
        title="Distribución de Ratings",
        color_discrete_sequence=["#F59E0B"]
    )

    st.plotly_chart(fig6, use_container_width=True)

    # -------------------------
    # Devoluciones
    # -------------------------

    st.subheader("📦 Productos Devueltos")

    df_devoluciones = df.copy()

    df_devoluciones["Estado"] = df_devoluciones["is_returned"].map({
        True: "Devuelto",
        False: "Entregado"
    })

    fig7 = px.pie(
        df_devoluciones,
        names="Estado",
        title="Proporción de Devoluciones",
        color="Estado",
        color_discrete_map={
            "Devuelto": "#EF4444",
            "Entregado": "#10B981"
        }
    )

    fig7.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(fig7, use_container_width=True)

# --------------------------------------------------
# SWEETVIZ
# --------------------------------------------------

elif opcion == "📑 Reporte Sweetviz":

    st.title("📑 Reporte de Perfilado con Sweetviz")

    st.write("""
    Sweetviz es una herramienta de análisis exploratorio automático
    que permite estudiar distribuciones, correlaciones y características
    de las variables del conjunto de datos.
    """)

    if st.button("🚀 Generar Reporte Sweetviz"):

        with st.spinner("Generando reporte..."):

            reporte = sv.analyze(df)

            reporte.show_html(
                "reporte_sweetviz.html",
                open_browser=False
            )

        st.success("✅ Reporte generado correctamente.")

        st.info(
            "El archivo reporte_sweetviz.html fue creado en la carpeta del proyecto."
        )

        with open("reporte_sweetviz.html", "rb") as file:
            st.download_button(
                label="📥 Descargar Reporte HTML",
                data=file,
                file_name="reporte_sweetviz.html",
                mime="text/html"
            )
# --------------------------------------------------
# CONCLUSIONES
# --------------------------------------------------

elif opcion == "📝 Conclusiones":

    st.title("📝 Conclusiones")

    st.markdown(f"""
### Conclusiones del Análisis

**1. Calidad de los datos**

El conjunto de datos analizado contiene **{df.shape[0]:,} registros** y **{df.shape[1]} variables**, proporcionando información suficiente para realizar un análisis descriptivo del comercio electrónico. Además, no se identificaron valores nulos ni registros duplicados, lo que demuestra una adecuada calidad y consistencia de los datos.

**2. Comportamiento de las transacciones**

Se observó que el precio promedio de los productos es de **${df['price'].mean():.2f}**, mientras que la calificación promedio de los usuarios alcanza **{df['rating'].mean():.2f} sobre 5 puntos**, evidenciando una valoración generalmente favorable de los productos comercializados.

**3. Logística y devoluciones**

El tiempo promedio de entrega registrado es de **{df['shipping_time_days'].mean():.2f} días**, lo que refleja un proceso logístico relativamente eficiente. Asimismo, se identificaron **{int(df['is_returned'].sum())} devoluciones**, información relevante para futuros análisis de satisfacción del cliente y gestión de ventas.

**4. Utilidad del análisis descriptivo**

Las visualizaciones permitieron identificar patrones relacionados con categorías de productos, métodos de pago, marcas y estados de entrega, facilitando la comprensión del comportamiento general de las transacciones registradas.

**5. Desarrollo de la aplicación**

La aplicación desarrollada mediante Streamlit permitió adquirir, visualizar y analizar los datos de forma interactiva, constituyéndose en una herramienta útil para apoyar procesos de exploración y análisis de información empresarial.
""")
