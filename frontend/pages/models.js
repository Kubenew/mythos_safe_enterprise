import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Models() {
  const [token, setToken] = useState("");
  const [models, setModels] = useState([]);
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ project_id: "", name: "", version: "1.0", endpoint: "" });

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) { loadModels(t); loadProjects(t); }
  }, []);

  async function loadModels(tok) {
    const res = await fetch(apiBase + "/models/", { headers: { Authorization: "Bearer " + tok } });
    setModels(await res.json());
  }

  async function loadProjects(tok) {
    const res = await fetch(apiBase + "/projects/", { headers: { Authorization: "Bearer " + tok } });
    setProjects(await res.json());
  }

  async function createModel() {
    await fetch(apiBase + "/models/", {
      method: "POST",
      headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    setForm({ project_id: "", name: "", version: "1.0", endpoint: "" });
    loadModels(token);
  }

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Model Registry</h1>
      <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>Register New Model</h3>
        <select value={form.project_id} onChange={e => setForm({...form, project_id: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }}>
          <option value="">Select Project</option>
          {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <input placeholder="Model name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="Version" value={form.version} onChange={e => setForm({...form, version: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="Endpoint (e.g., http://localhost:8000/v1)" value={form.endpoint} onChange={e => setForm({...form, endpoint: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <button onClick={createModel} style={{ padding: "10px 20px", background: "#0070f3", color: "white", border: "none", borderRadius: 5 }}>Register Model</button>
      </div>
      <div>
        <h3>Registered Models</h3>
        {models.map(m => (
          <div key={m.id} style={{ background: "white", padding: 15, marginBottom: 10, borderRadius: 8 }}>
            <h4>{m.name} v{m.version}</h4>
            <p style={{ color: "#666" }}>Endpoint: {m.endpoint || "Not set"}</p>
            <small style={{ color: "#999" }}>Project ID: {m.project_id}</small>
          </div>
        ))}
      </div>
    </Layout>
  );
}
