import { useState } from "react";
import MapView from "./components/MapView";
import Dashboard from "./components/Dashboard";
import Filters from "./components/Filters";

export default function App() {
  const [data, setData] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [activeTab, setActiveTab] = useState("map"); // 👈 controla el tab activo

  // cargar datos (lo mismo que antes)
  useState(() => {
    fetch("/data/mock.json")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setFiltered(json);
      });
  }, []);

  const handleFilter = (municipio) => {
    if (!municipio) setFiltered(data);
    else setFiltered(data.filter((d) => d.municipio === municipio));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="container mx-auto p-4 max-w-4xl">
        {/* Botón de Sistema de Alertas encima */}
        <div className="flex justify-center mb-4">
          <button
            onClick={async () => {
              const email = prompt('Insert your email to receive alerts');
              if (!email) return;
              try {
                const res = await fetch('http://localhost:8000/subscribe', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ email })
                });
                if (!res.ok) {
                  const err = await res.json().catch(() => ({}));
                  alert('Failed to subscribe: ' + (err.detail || res.statusText));
                } else {
                  alert('Subscribed successfully — check your email for confirmation');
                }
              } catch (e) {
                alert('Could not reach alert server: ' + e.message);
              }
            }}
            className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-full shadow-md"
          >
            Sistema de Alertas
          </button>
        </div>
        <h1 className="text-3xl font-extrabold mb-6 text-blue-900 drop-shadow">NASA Space Apps Dashboard</h1>

      {/* Filtros arriba (opcional) */}
      {/* Obtener municipios únicos para el filtro */}
      {/* Solo capitales de comunidad autónoma */}
        <Filters
          onChange={handleFilter}
          municipios={Array.from(new Set(data
            .map((d) => d.municipio)
            .filter((m) => [
              "Madrid",
              "Barcelona",
              "Valencia",
              "Sevilla",
              "Zaragoza",
              "Valladolid",
              "Toledo",
              "Mérida",
              "Santiago de Compostela",
              "Oviedo",
              "Santander",
              "Logroño",
              "Pamplona",
              "Vitoria-Gasteiz",
              "Las Palmas de Gran Canaria",
              "Santa Cruz de Tenerife",
              "Palma"
            ].includes(m))
          )).sort()}
        />

      {/* Barra de tabs */}
      <div className="flex gap-2 mb-6">
        <button
          className={`flex-1 py-2 rounded-t-lg transition-all duration-200 shadow-sm text-lg font-semibold focus:outline-none 
            ${activeTab === "map" ? "bg-white text-blue-700 border-b-4 border-blue-500" : "bg-blue-100 text-blue-500 hover:bg-white"}`}
          onClick={() => setActiveTab("map")}
        >
          Mapa
        </button>
        <button
          className={`flex-1 py-2 rounded-t-lg transition-all duration-200 shadow-sm text-lg font-semibold focus:outline-none 
            ${activeTab === "dashboard" ? "bg-white text-blue-700 border-b-4 border-blue-500" : "bg-blue-100 text-blue-500 hover:bg-white"}`}
          onClick={() => setActiveTab("dashboard")}
        >
          Dashboard
        </button>
        <button
          className={`flex-1 py-2 rounded-t-lg transition-all duration-200 shadow-sm text-lg font-semibold focus:outline-none 
            ${activeTab === "ai" ? "bg-white text-blue-700 border-b-4 border-blue-500" : "bg-blue-100 text-blue-500 hover:bg-white"}`}
          onClick={() => setActiveTab("ai")}
        >
          AI Model
        </button>
      </div>
          

      {/* Contenido de cada tab */}
      <div className="bg-white rounded-b-lg shadow p-6 min-h-[350px]">
        {activeTab === "map" && <MapView data={filtered} />}
        {activeTab === "dashboard" && <Dashboard data={filtered} />}
        {activeTab === "ai" && (
          <div className="flex flex-col items-center justify-center h-full">
            <h2 className="text-2xl font-bold mb-2 text-blue-700">AI Model</h2>
            <p className="text-gray-600">Próximamente: aquí irá la integración con el modelo de IA.</p>
          </div>
        )}
      </div>
    </div>
    </div>
  );
}

