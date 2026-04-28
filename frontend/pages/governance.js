import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Governance() {
  const [token, setToken] = useState("");
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState("");
  const [gates, setGates] = useState(null);
  const [compliance, setCompliance] = useState("");

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) loadProjects(t);
  }, []);

  async function loadProjects(tok) {
    const res = await fetch(apiBase + "/projects/", { headers: { Authorization: "Bearer " + tok } });
    setProjects(await res.json());
  }

  async function loadGates() {
    if (!selectedProject) return;
    const res = await fetch(apiBase + "/governance/gates/" + selectedProject, { 
      headers: { Authorization: "Bearer " + token } 
    });
    setGates(await res.json());
  }

  async function loadCompliance() {
    if (!selectedProject) return;
    const res = await fetch(apiBase + "/governance/compliance-report/" + selectedProject, { 
      headers: { Authorization: "Bearer " + token } 
    });
    const text = await res.text();
    setCompliance(text);
  }

  useEffect(() => {
    if (selectedProject) {
      loadGates();
      loadCompliance();
    }
  }, [selectedProject]);

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Governance & RSP Gates</h1>
      <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <label>Select Project: </label>
        <select value={selectedProject} onChange={e => setSelectedProject(e.target.value)} style={{ padding: 8, marginLeft: 10 }}>
          <option value="">-- Select --</option>
          {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
      </div>

      {gates && (
        <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
          <h3>Release Gates (RSP-style)</h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 15 }}>
            {Object.entries(gates.gates).map(([gate, info]) => (
              <div key={gate} style={{ 
                padding: 15, 
                border: "2px solid " + (info.status === "passed" ? "#28a745" : info.status === "pending" ? "#ffc107" : "#dc3545"),
                borderRadius: 8,
                textAlign: "center"
              }}>
                <h4>Gate {gate}</h4>
                <p>{info.name}</p>
                <span style={{ 
                  padding: "4px 8px", 
                  borderRadius: 3, 
                  background: info.status === "passed" ? "#d4edda" : info.status === "pending" ? "#fff3cd" : "#f8d7da",
                  fontSize: 12
                }}>{info.status}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 20, padding: 15, background: gates.ready_for_release ? "#d4edda" : "#fff3cd", borderRadius: 5 }}>
            <strong>Status: </strong> 
            {gates.ready_for_release ? "✅ READY FOR RELEASE" : "⚠️ NOT READY - Complete all gates"}
          </div>
        </div>
      )}

      {compliance && (
        <div style={{ background: "white", padding: 20, borderRadius: 8 }}>
          <h3>Compliance Report</h3>
          <pre style={{ background: "#f4f4f4", padding: 15, borderRadius: 5, overflow: "auto", whiteSpace: "pre-wrap" }}>
            {compliance}
          </pre>
        </div>
      )}
    </Layout>
  );
}
