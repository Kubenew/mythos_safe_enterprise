import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Evals() {
  const [token, setToken] = useState("");
  const [projects, setProjects] = useState([]);
  const [evals, setEvals] = useState([]);
  const [form, setForm] = useState({ project_id: "", suite: "math_mini", model_endpoint: "", api_key: "" });

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) { loadProjects(t); loadEvals(t); }
  }, []);

  async function loadProjects(tok) {
    const res = await fetch(apiBase + "/projects/", { headers: { Authorization: "Bearer " + tok } });
    setProjects(await res.json());
  }

  async function loadEvals(tok) {
    const res = await fetch(apiBase + "/jobs/", { headers: { Authorization: "Bearer " + tok } });
    const jobs = await res.json();
    setEvals(jobs.filter(j => j.type === "eval" || j.type === "math_eval" || j.type === "cyber_eval"));
  }

  async function runEval() {
    await fetch(apiBase + "/jobs/", {
      method: "POST",
      headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
      body: JSON.stringify({ 
        project_id: parseInt(form.project_id), 
        type: "eval", 
        input: { 
          suite: form.suite, 
          model_endpoint: form.model_endpoint,
          api_key: form.api_key 
        } 
      })
    });
    setForm({ project_id: "", suite: "math_mini", model_endpoint: "", api_key: "" });
    setTimeout(() => loadEvals(token), 1000);
  }

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Evaluations</h1>
      <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>Run New Evaluation</h3>
        <select value={form.project_id} onChange={e => setForm({...form, project_id: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }}>
          <option value="">Select Project</option>
          {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <select value={form.suite} onChange={e => setForm({...form, suite: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }}>
          <option value="math_mini">Math Mini</option>
          <option value="cyber_defensive">Cyber Defensive</option>
        </select>
        <input placeholder="Model Endpoint (optional)" value={form.model_endpoint} onChange={e => setForm({...form, model_endpoint: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="API Key (optional)" type="password" value={form.api_key} onChange={e => setForm({...form, api_key: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <button onClick={runEval} style={{ padding: "10px 20px", background: "#0070f3", color: "white", border: "none", borderRadius: 5 }}>Run Evaluation</button>
      </div>
      <div>
        <h3>Evaluation Results</h3>
        {evals.map(e => (
          <div key={e.id} style={{ background: "white", padding: 15, marginBottom: 10, borderRadius: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong>Job #{e.id}</strong>
              <span style={{ 
                padding: "4px 8px", 
                borderRadius: 3, 
                background: e.status === "done" ? "#d4edda" : e.status === "failed" ? "#f8d7da" : "#fff3cd",
                fontSize: 12 
              }}>{e.status}</span>
            </div>
            <p style={{ color: "#666", fontSize: 14 }}>Type: {e.type}</p>
            {e.output_json && (
              <pre style={{ background: "#f4f4f4", padding: 10, borderRadius: 5, fontSize: 12, overflow: "auto" }}>
                {JSON.stringify(JSON.parse(e.output_json), null, 2)}
              </pre>
            )}
          </div>
        ))}
      </div>
    </Layout>
  );
}
