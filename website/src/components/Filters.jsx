export default function Filters({ onChange, municipios = [] }) {
  return (
    <div className="flex gap-4 mb-6">
      <select
        onChange={e => onChange(e.target.value)}
        className="p-2 rounded border border-blue-200 shadow focus:ring-2 focus:ring-blue-400 focus:outline-none bg-white text-blue-900 font-medium"
      >
        <option value="">Todos los municipios</option>
        {municipios.map((m) => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>
    </div>
  );
}
