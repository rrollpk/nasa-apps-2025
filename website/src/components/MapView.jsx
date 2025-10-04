import { MapContainer, TileLayer, Marker, Popup, LayersControl, LayerGroup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

// --- Componente MapView ---
export default function MapView({ data }) {
  const bounds = [[35.8, -9.5], [43.9, 3.5]]; // Península y Baleares
  const canariasBounds = [[27.5, -18.2], [29.5, -13.2]];
  // Filtrar solo municipios de Canarias
  const canariasData = data.filter(d => Number(d.lat) >= 27.5 && Number(d.lat) <= 29.5 && Number(d.lon) >= -18.2 && Number(d.lon) <= -13.2);

  return (
    <div className="relative rounded-lg overflow-hidden shadow mb-4">
      <MapContainer
        center={[40, -3]}
        zoom={6}
        style={{ height: '650px', width: '100%' }}
        className="z-0"
        bounds={bounds}
        maxBounds={bounds}
      >
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="Municipios">
            <LayerGroup>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
              {data.map((item, idx) => (
                <Marker
                  key={idx}
                  position={[
                    Number(item.lat) || 0,
                    Number(item.lon) || 0
                  ]}
                >
                  <Popup>
                    <div className="text-blue-900">
                      <div className="font-bold text-lg mb-1">{String(item.municipio)}</div>
                      <div className="text-sm">PM2.5: <span className="font-semibold">{String(item.pm25)}</span></div>
                      <div className="text-sm">Ozono: <span className="font-semibold">{String(item.ozono)}</span></div>
                      <div className="text-sm">Verde: <span className="font-semibold">{String(item.verde)}%</span></div>
                      <div className="text-xs text-gray-500 mt-1">{item.medidas}</div>
                    </div>
                  </Popup>
                </Marker>
              ))}
            </LayerGroup>
          </LayersControl.BaseLayer>
          <LayersControl.Overlay name="Partículas de aire (API)">
            <LayerGroup>
              {/* Aquí irá la visualización de partículas de aire en tiempo real */}
              <TileLayer
                url="https://tile.openweathermap.org/map/pm2_5/{z}/{x}/{y}.png?appid=YOUR_API_KEY"
                attribution="&copy; OpenWeatherMap contributors"
                opacity={0.6}
              />
            </LayerGroup>
          </LayersControl.Overlay>
        </LayersControl>
      </MapContainer>
    </div>
  );
}
