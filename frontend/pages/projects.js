import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Projects() {
  const [token, setToken] = useState("");
  const [projects, setProjects] = useState([]);
  const [newName, setNewName] = useState("");
  const [newDesc, setNewDesc] = useState("");

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) loadProjects(t);
  }, []);

  async function loadProjects(tok) {
    const res = await fetch(apiBase + "/projects/", { headers: { Authorization: "Bearer " + tok } });
    setProjects(await res.json());
  }

  async function createProject() {
    await fetch(apiBase + "/projects/", {
      method: "POST",
      headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName, description: newDesc })
    });
    setNewName(""); setNewDesc("");
    loadProjects(token);
  }

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Projects</h1>
      <div style={{ background: "white", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>Create New Project</h3>
        <input placeholder="Project name" value={newName} onChange={e => setNewName(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="Description" value={newDesc} onChange={e => setNewDesc(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <button onClick={createProject} style={{ padding: "10px 20px", background: "#0070f3", color: "white", border: "none", borderRadius: 5 }}>Create</button>
      </div>
      <div>
        <h3>All Projects</h3>
        {projects.map(p => (
          <div key={p.id} style={{ background: "white", padding: 15, marginBottom: 10, borderRadius: 8, borderLeft: "4px solid #0070f3" }}>
            <h4>{p.name}</h4>
            <p style={{ color: "#666" }}>{p.description}</p>
            <small style={{ color: "#999" }}>Created: {p.created_at}</small>
          </div>
        ))}
      </div>
    </Layout>
  );
}
