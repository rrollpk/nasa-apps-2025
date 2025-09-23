import folium
from streamlit_folium import st_folium

    
# Crear mapa centrado en coordenadas
m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)

folium.GeoJson(
    geojson_data,
    name="Ciudades",
    style_function=lambda feature: {
        "fillColor": "green",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.4,
    },
    tooltip=folium.GeoJsonTooltip(fields=["city_name", "population"])
).add_to(m)
# Añadir marcador para ciudad
folium.CircleMarker(
    location=[48.8566, 2.3522],
    radius=10,
    popup="París: Índice ambiental 0.78",
    color='green',
    fill=True,
    fill_color='green'
).add_to(m)

# Mostrar en Streamlit
st_folium(m, width=700, height=500)



