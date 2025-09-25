import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Crear mapa centrado en coordenadas
m = folium.Map(location=[40.4378373, -3.844348], zoom_start=5)

bounds = [[27.6, -18.2], [43.8, 4.3]]
m.fit_bounds(bounds)  # Ajusta vista inicial
m.options['maxBounds'] = bounds  # No deja salir de ahí

bordersStyle = {
    'color': 'green',
    'weight': 2,
    'fillColor': 'blue',
    'fillOpacity': 0.2
}

folium.GeoJson(
    "spain_Municipality_level_3.geojson",
    name='Spain',
    style_function=lambda x: bordersStyle
).add_to(m)

# Añadir marcador para ciudad
folium.CircleMarker(
    location=[40.4378373, -3.844348],
    radius=5,
    popup="Madrid: Índice ambiental 0.78",
    color='green',
    fill=True,
    fill_color='green'
).add_to(m)

# Heatmap
heat_data = [
    [40.4168, -3.7038, 0.8],  # Madrid
    [41.3879, 2.1699, 0.7],   # Barcelona
    [37.3891, -5.9845, 0.6],  # Sevilla
    [39.4699, -0.3763, 0.9],  # Valencia
]

HeatMap(
    heat_data,
    radius=25,
    blur=15,
    min_opacity=0.3,  # hace que sea medio translúcido
).add_to(m)

# Tabs
tab1, tab2 = st.tabs(['🗺️ Mapa', '📊 Otra cosa'])

with tab1:
    # Control de capas
    folium.LayerControl().add_to(m)

    # Mostrar en Streamlit
    st_folium(m, width=700, height=500)

with tab2:
    st.write("Aquí pondrás otra cosa (tabla, gráfico, etc.)")



m.save("map.html")
