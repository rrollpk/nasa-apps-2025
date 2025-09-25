import folium
from streamlit_folium import st_folium

    
# Crear mapa centrado en coordenadas
m = folium.Map(location=[40.4378373,-3.844348], zoom_start=5)

bounds = [[27.6, -18.2], [43.8, 4.3]]
m.fit_bounds(bounds)  # Ajusta vista inicial
m.options['maxBounds'] = bounds  # No deja salir de ahí

bordersStyle={
    'color': 'green',
    'weight': 2,
    'fillColor': 'blue',
    'fillOpacity': 0.2
}

folium.GeoJson("spain_Municipality_level_3.geojson", 
               name = 'Spain',
               style_function=lambda x:bordersStyle).add_to(m)


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

# 4. Control de capas (para activar/desactivar)
folium.LayerControl().add_to(m)

m.save("map.html")
