import folium
from streamlit_folium import st_folium

tab1, tab2, tab3 = st.tabs(["Mapa", "Rankings", "Predicciones"])

with tab1:
    st.write("Mapa con Folium aquí")

with tab2:
    st.write("Rankings con métricas y tablas")

with tab3:
    st.write("Predicciones ambientales")
    
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

