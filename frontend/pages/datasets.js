import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Datasets() {
  const [token, setToken] = useState("");
  const [datasets, setDatasets] = useState([]);
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ project_id: "", name: "", description: "", uri: "" });

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) { loadDatasets(t); loadProjects(t); }
  }, []);

  async function loadDatasets(tok) {
    const res = await fetch(apiBase + "/datasets/", { headers: { Authorization: "Bearer " + tok } });
    setDatasets(await res.json());
  }

  async function loadProjects(tok) {
    const res = await fetch(apiBase + "/projects/", { headers: { Authorization: "Bearer " + tok } });
    setProjects(await res.json());
  }

  async function createDataset() {
    await fetch(apiBase + "/datasets/", {
      method: "POST",
      headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    setForm({ project_id: "", name: "", description: "", uri: "" });
    loadDatasets(token);
  }

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Datasets</h1>
      <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>Register New Dataset</h3>
        <select value={form.project_id} onChange={e => setForm({...form, project_id: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }}>
          <option value="">Select Project</option>
          {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <input placeholder="Dataset name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="URI (file path or URL)" value={form.uri} onChange={e => setForm({...form, uri: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <button onClick={createDataset} style={{ padding: "10px 20px", background: "#0070f3", color: "white", border: "none", borderRadius: 5 }}>Register Dataset</button>
      </div>
      <div>
        <h3>Registered Datasets</h3>
        {datasets.map(d => (
          <div key={d.id} style={{ background: "white", padding: 15, marginBottom: 10, borderRadius: 8 }}>
            <h4>{d.name}</h4>
            <p style={{ color: "#666" }}>{d.description}</p>
            <p style={{ fontSize: 12, color: "#999" }}>URI: {d.uri || "Not specified"} | Project: {d.project_id}</p>
          </div>
        ))}
      </div>
    </Layout>
  );
}
