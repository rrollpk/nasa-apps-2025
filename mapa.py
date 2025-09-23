import folium
from streamlit_folium import st_folium

    
# Crear mapa centrado en coordenadas
m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)

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


