import { useState, useEffect } from "react";
import Layout from "../components/Layout";

const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Jobs() {
  const [token, setToken] = useState("");
  const [jobs, setJobs] = useState([]);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t || "");
    if (t) loadJobs(t);
  }, []);

  async function loadJobs(tok) {
    const res = await fetch(apiBase + "/jobs/", { headers: { Authorization: "Bearer " + tok } });
    setJobs(await res.json());
  }

  const filteredJobs = filter === "all" ? jobs : jobs.filter(j => j.status === filter);

  if (!token) return <Layout><p>Please login first</p></Layout>;

  return (
    <Layout>
      <h1>Jobs</h1>
      <div style={{ marginBottom: 20 }}>
        <button onClick={() => setFilter("all")} style={{ marginRight: 10, padding: "8px 16px", background: filter === "all" ? "#0070f3" : "#ddd", color: filter === "all" ? "white" : "black", border: "none", borderRadius: 5 }}>All</button>
        <button onClick={() => setFilter("queued")} style={{ marginRight: 10, padding: "8px 16px", background: filter === "queued" ? "#0070f3" : "#ddd", color: filter === "queued" ? "white" : "black", border: "none", borderRadius: 5 }}>Queued</button>
        <button onClick={() => setFilter("running")} style={{ marginRight: 10, padding: "8px 16px", background: filter === "running" ? "#0070f3" : "#ddd", color: filter === "running" ? "white" : "black", border: "none", borderRadius: 5 }}>Running</button>
        <button onClick={() => setFilter("done")} style={{ marginRight: 10, padding: "8px 16px", background: filter === "done" ? "#0070f3" : "#ddd", color: filter === "done" ? "white" : "black", border: "none", borderRadius: 5 }}>Done</button>
        <button onClick={() => setFilter("failed")} style={{ padding: "8px 16px", background: filter === "failed" ? "#0070f3" : "#ddd", color: filter === "failed" ? "white" : "black", border: "none", borderRadius: 5 }}>Failed</button>
      </div>
      <table style={{ width: "100%", borderCollapse: "collapse", background: "white" }}>
        <thead>
          <tr style={{ background: "#f4f4f4" }}>
            <th style={{ padding: 12, textAlign: "left", borderBottom: "2px solid #ddd" }}>ID</th>
            <th style={{ padding: 12, textAlign: "left", borderBottom: "2px solid #ddd" }}>Project</th>
            <th style={{ padding: 12, textAlign: "left", borderBottom: "2px solid #ddd" }}>Type</th>
            <th style={{ padding: 12, textAlign: "left", borderBottom: "2px solid #ddd" }}>Status</th>
            <th style={{ padding: 12, textAlign: "left", borderBottom: "2px solid #ddd" }}>Created</th>
          </tr>
        </thead>
        <tbody>
          {filteredJobs.map(j => (
            <tr key={j.id}>
              <td style={{ padding: 12, borderBottom: "1px solid #eee" }}>{j.id}</td>
              <td style={{ padding: 12, borderBottom: "1px solid #eee" }}>{j.project_id}</td>
              <td style={{ padding: 12, borderBottom: "1px solid #eee" }}>{j.type}</td>
              <td style={{ padding: 12, borderBottom: "1px solid #eee" }}>
                <span style={{ 
                  padding: "4px 8px", 
                  borderRadius: 3, 
                  background: j.status === "done" ? "#d4edda" : j.status === "failed" ? "#f8d7da" : j.status === "running" ? "#cce5ff" : "#fff3cd",
                  fontSize: 12 
                }}>{j.status}</span>
              </td>
              <td style={{ padding: 12, borderBottom: "1px solid #eee", fontSize: 12, color: "#666" }}>{j.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Layout>
  );
}
