import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Análisis Vehículos Eléctricos",
    layout="wide",
    menu_items={
        "Get Help": "https://tripleten.com/trainer/data-analyst/lesson/88d0605e-a452-4c37-a843-4a8c8f4d5c26/",
        "About": "Análisis interactivo de vehículos eléctricos en EE.UU. utilizando Streamlit y Plotly.",
    },
)

# Título de la aplicación
st.title("Análisis de Vehículos Eléctricos en EE.UU.")


# Cargar y limpiar los datos
def load_data():
    df = pd.read_csv("vehicles_us_clean.csv")
    df = df.dropna(subset=["odometer", "price", "model", "model_year"])
    df = df[df["odometer"] >= 0]
    df = df[df["price"] >= 0]
    df = df.rename(
        columns={
            "odometer": "Kilometraje",
            "model_year": "Año",
            "model": "Modelo",
            "condition": "Condición",
            "price": "Precio",
            "fuel": "Combustible",
            "cylinders": "Cilindrada",
            "transmission": "Transmisión",
            "type": "Tipo",
            "date_posted": "Fecha de publicación",
            "days_listed": "Días publicados",
            "paint_color": "Color",
            "is_4wd": "Tracción 4x4",
        }
    )
    return df


# Almacenar los datos en un DataFrame
car_data = load_data()

# Reemplazar valores nulos y formatear columnas
car_data["Color"] = car_data["Color"].fillna("-")
car_data["Tracción 4x4"] = car_data["Tracción 4x4"].replace(1, "Sí").fillna("No")

# Menú lateral con filtros
st.sidebar.header("Filtros")
selected_year = st.sidebar.slider(
    "Año del vehículo",
    int(car_data["Año"].min()),
    int(car_data["Año"].max()),
    (int(car_data["Año"].min()), int(car_data["Año"].max())),
)
min_odometer, max_odometer = st.sidebar.slider(
    "Rango de kilometraje (millas)",
    int(car_data["Kilometraje"].min()),
    int(car_data["Kilometraje"].max()),
    (int(car_data["Kilometraje"].min()), int(car_data["Kilometraje"].max())),
)
min_price, max_price = st.sidebar.slider(
    "Rango de precio (USD)",
    int(car_data["Precio"].min()),
    int(car_data["Precio"].max()),
    (int(car_data["Precio"].min()), int(car_data["Precio"].max())),
)
selected_models = st.sidebar.multiselect(
    "Selección de modelos",
    options=sorted(car_data["Modelo"].unique()),
    default=sorted(car_data["Modelo"].unique())[:10],
)

# Filtrar datos
filtered_data = car_data[
    (car_data["Año"].between(*selected_year))
    & (car_data["Kilometraje"].between(min_odometer, max_odometer))
    & (car_data["Precio"].between(min_price, max_price))
    & (car_data["Modelo"].isin(selected_models))
]

# Mostrar número de registros
st.markdown(f"**Vehículos mostrados:** {len(filtered_data)}")

# Opciones de visualización
st.sidebar.header("Visualizaciones")
show_hist = st.sidebar.checkbox("Histograma de Kilometraje", value=False)
show_scat = st.sidebar.checkbox("Dispersión Precio vs Kilometraje", value=False)
show_data = st.sidebar.checkbox("Ver datos filtrados", value=True)

# Histograma
if show_hist:
    st.subheader("Distribución del Kilometraje")
    fig = px.histogram(
        filtered_data,
        x="Kilometraje",
        nbins=80,
        color="Modelo",
        title="Distribución del Kilometraje por Modelo",
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersión
if show_scat:
    st.subheader("Relación entre Precio y Kilometraje")
    fig2 = px.scatter(
        filtered_data,
        x="Kilometraje",
        y="Precio",
        color="Modelo",
        hover_data=["Año", "Modelo"],
        title="Precio vs Kilometraje",
    )
    st.plotly_chart(fig2, use_container_width=True)

# Mostrar resumen de datos
if show_data:
    with st.expander("Mostrar datos filtrados", expanded=True):
        st.dataframe(filtered_data)

    with st.expander("Resumen de Datos Filtrados", expanded=True):
        st.write(
            filtered_data.describe()
            .T.rename(
                columns={
                    "count": "Cantidad",
                    "mean": "Promedio",
                    "std": "Desviación estándar",
                    "min": "Mínimo",
                    "25%": "Q1",
                    "50%": "Mediana",
                    "75%": "Q3",
                    "max": "Máximo",
                }
            )
            .round(2)
        )
