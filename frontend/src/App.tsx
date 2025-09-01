import { useState } from "react";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

type UploadResponse = {
  upload_id: string;
  filename: string;
  sheet_names: string[];
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [resp, setResp] = useState<UploadResponse | null>(null);
  const [uploads, setUploads] = useState<any[]>([]);

  const handleUpload = async () => {
    if (!file) return alert("Escolha um arquivo .xlsx");
    const form = new FormData();
    form.append("file", file);

    try {
      const { data } = await axios.post(`${API_BASE}/files/upload`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResp(data);
      await loadUploads();
    } catch (e: any) {
      alert(e?.response?.data?.detail || "Erro ao enviar arquivo");
    }
  };

  const loadUploads = async () => {
    const { data } = await axios.get(`${API_BASE}/uploads`);
    setUploads(data);
  };

  const exportCsv = async (uploadId: string) => {
    const url = `${API_BASE}/exports/csv?upload_id=${uploadId}`;
    window.open(url, "_blank");
  };

  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-3xl mx-auto space-y-6">
        <header className="space-y-1">
          <h1 className="text-2xl font-bold">Saúde MVP — Upload e Leitura de Planilhas</h1>
          <p className="text-gray-600">
            Faça upload de um .xlsx para ver as abas e salvar o registro no banco.
          </p>
        </header>

        <section className="bg-white rounded-xl shadow p-4 space-y-3">
          <div className="flex items-center gap-3">
            <input
              type="file"
              accept=".xlsx,.xlsm"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <button
              onClick={handleUpload}
              className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              Enviar
            </button>
            <button
              onClick={loadUploads}
              className="px-3 py-2 rounded-lg border hover:bg-gray-100"
            >
              Recarregar uploads
            </button>
          </div>

          {resp && (
            <div className="border rounded-lg p-3">
              <h2 className="font-semibold">Upload recente</h2>
              <p className="text-sm text-gray-600">{resp.filename}</p>
              <h3 className="mt-2 font-medium">Abas detectadas:</h3>
              <ul className="list-disc list-inside">
                {resp.sheet_names.map((n) => (
                  <li key={n}>{n}</li>
                ))}
              </ul>
              <div className="mt-2">
                <button
                  className="px-3 py-2 rounded-lg border hover:bg-gray-100"
                  onClick={() => exportCsv(resp.upload_id)}
                >
                  Exportar CSV (abas)
                </button>
              </div>
            </div>
          )}
        </section>

        <section className="bg-white rounded-xl shadow p-4">
          <h2 className="font-semibold mb-2">Uploads anteriores</h2>
          <div className="space-y-2">
            {uploads.map((u) => (
              <div key={u.id} className="flex items-center justify-between border rounded p-2">
                <div>
                  <div className="font-medium">{u.filename}</div>
                  <div className="text-sm text-gray-600">Enviado: {new Date(u.uploaded_at).toLocaleString()}</div>
                </div>
                <button
                  className="px-3 py-2 rounded-lg border hover:bg-gray-100"
                  onClick={() => exportCsv(u.id)}
                >
                  Exportar CSV
                </button>
              </div>
            ))}
            {uploads.length === 0 && <p className="text-sm text-gray-500">Nenhum upload ainda.</p>}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
