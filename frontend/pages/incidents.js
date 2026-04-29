import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Incidents() {
  const [token, setToken] = useState("");
  const [incidents, setIncidents] = useState([]);
  const [form, setForm] = useState({ project_id: "", severity: "medium", description: "" });

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) loadIncidents(t);
  }, []);

  async function loadIncidents(tok) {
    const res = await fetch(apiBase + "/incidents/", { headers: { Authorization: "Bearer " + tok } });
    setIncidents(await res.json());
  }

  async function createIncident() {
    await fetch(apiBase + "/incidents/", {
      method: "POST",
      headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    setForm({ project_id: "", severity: "medium", description: "" });
    loadIncidents(token);
  }

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Security Incidents</h1>
      <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>Report New Incident</h3>
        <input placeholder="Project ID" value={form.project_id} onChange={e => setForm({...form, project_id: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <select value={form.severity} onChange={e => setForm({...form, severity: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8 }}>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
        <textarea placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} style={{ width: "100%", padding: 8, marginBottom: 8, minHeight: 100 }} />
        <button onClick={createIncident} style={{ padding: "10px 20px", background: "#dc3545", color: "white", border: "none", borderRadius: 5 }}>Report Incident</button>
      </div>
      <div>
        <h3>Incident Log</h3>
        {incidents.map(inc => (
          <div key={inc.id} style={{ 
            background: "white", 
            padding: 15, 
            marginBottom: 10, 
            borderRadius: 8,
            borderLeft: "4px solid " + (inc.severity === "critical" ? "#dc3545" : inc.severity === "high" ? "#fd7e14" : inc.severity === "medium" ? "#ffc107" : "#28a745")
          }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong>Incident #{inc.id}</strong>
              <span style={{ 
                padding: "4px 8px", 
                borderRadius: 3, 
                background: inc.severity === "critical" ? "#f8d7da" : inc.severity === "high" ? "#fff3cd" : "#d4edda",
                fontSize: 12
              }}>{inc.severity}</span>
            </div>
            <p style={{ marginTop: 10 }}>{inc.description}</p>
            <small style={{ color: "#666" }}>Project: {inc.project_id} | Status: {inc.status} | Created: {inc.created_at}</small>
          </div>
        ))}
      </div>
    </Layout>
  );
}
