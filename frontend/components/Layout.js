import { useState, useEffect } from "react";
import Link from "next/link";

export default function Layout({ children }) {
  const [token, setToken] = useState("");

  useEffect(() => {
    setToken(localStorage.getItem("token") || "");
  }, []);

  if (!token) return <div>{children}</div>;

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <nav style={{ width: 250, background: "#1a1a1a", color: "white", padding: 20 }}>
        <h2 style={{ color: "#0070f3", marginBottom: 30 }}>Mythos-Safe</h2>
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li style={{ marginBottom: 10 }}>
            <Link href="/" style={{ color: "white", textDecoration: "none" }}>🏠 Dashboard</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/projects" style={{ color: "white", textDecoration: "none" }}>📁 Projects</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/models" style={{ color: "white", textDecoration: "none" }}>🤖 Models</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/datasets" style={{ color: "white", textDecoration: "none" }}>📊 Datasets</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/evals" style={{ color: "white", textDecoration: "none" }}>✅ Evaluations</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/jobs" style={{ color: "white", textDecoration: "none" }}>⚙️ Jobs</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/governance" style={{ color: "white", textDecoration: "none" }}>🛡️ Governance</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <Link href="/incidents" style={{ color: "white", textDecoration: "none" }}>⚠️ Incidents</Link>
          </li>
          <li style={{ marginBottom: 10 }}>
            <a href="http://localhost:8000/docs" target="_blank" style={{ color: "#0070f3", textDecoration: "none" }}>📖 API Docs</a>
          </li>
        </ul>
        <button 
          onClick={() => { localStorage.removeItem("token"); window.location.reload(); }}
          style={{ marginTop: 30, padding: "8px 16px", background: "#ff4444", color: "white", border: "none", borderRadius: 5, cursor: "pointer" }}
        >
          Logout
        </button>
      </nav>
      <main style={{ flex: 1, padding: 30, background: "#f5f5f5" }}>
        {children}
      </main>
    </div>
  );
}
