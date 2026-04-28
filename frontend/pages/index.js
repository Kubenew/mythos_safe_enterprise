import { useEffect, useState } from "react";

export default function Home() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
  const [token, setToken] = useState("");
  const [email, setEmail] = useState("admin@local");
  const [password, setPassword] = useState("admin123");
  const [projects, setProjects] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  async function login() {
    setLoading(true);
    const res = await fetch(apiBase + "/auth/login", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({email, password})
    });
    const data = await res.json();
    setToken(data.access_token || "");
    setLoading(false);
  }

  async function loadData() {
    const p = await fetch(apiBase + "/projects/", {headers:{Authorization:"Bearer "+token}});
    setProjects(await p.json());

    const j = await fetch(apiBase + "/jobs/", {headers:{Authorization:"Bearer "+token}});
    setJobs(await j.json());
  }

  async function createJob(projectId, type) {
    await fetch(apiBase + "/jobs/", {
      method: "POST",
      headers:{Authorization:"Bearer "+token, "Content-Type":"application/json"},
      body: JSON.stringify({project_id: projectId, type: type, input: {suite: "math_mini"}})
    });
    loadData();
  }

  useEffect(()=>{ if(token) loadData(); }, [token]);

  return (
    <div style={{fontFamily:"Arial", padding:20, maxWidth:1200, margin:"0 auto"}}>
      <h1>Mythos-Safe Enterprise MVP</h1>
      {!token ? (
        <div style={{maxWidth:400, margin:"100px auto"}}>
          <h3>Login</h3>
          <input style={{width:"100%",padding:8,marginBottom:8}} value={email} onChange={e=>setEmail(e.target.value)} />
          <input style={{width:"100%",padding:8, marginBottom:8}} type="password" value={password} onChange={e=>setPassword(e.target.value)} />
          <button style={{padding:10, width:"100%", background:"#0070f3", color:"white", border:"none", borderRadius:5}} onClick={login} disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </div>
      ) : (
        <>
          <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:20}}>
            <div>
              <h2>Projects</h2>
              {projects.length === 0 ? <p>No projects yet</p> : (
                <ul style={{listStyle:"none", padding:0}}>
                  {projects.map(p => (
                    <li key={p.id} style={{padding:10, border:"1px solid #ddd", marginBottom:8, borderRadius:5}}>
                      <strong>{p.name}</strong> - {p.description}
                      <button onClick={() => createJob(p.id, "math_eval")} style={{marginLeft:10, padding:"5px 10px", fontSize:12}}>
                        Run Math Eval
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div>
              <h2>Jobs</h2>
              {jobs.length === 0 ? <p>No jobs yet</p> : (
                <table style={{width:"100%", borderCollapse:"collapse"}}>
                  <thead>
                    <tr style={{background:"#f4f4f4"}}>
                      <th style={{padding:8, textAlign:"left", borderBottom:"2px solid #ddd"}}>ID</th>
                      <th style={{padding:8, textAlign:"left", borderBottom:"2px solid #ddd"}}>Type</th>
                      <th style={{padding:8, textAlign:"left", borderBottom:"2px solid #ddd"}}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {jobs.slice(0, 10).map(j => (
                      <tr key={j.id}>
                        <td style={{padding:8, borderBottom:"1px solid #eee"}}>{j.id}</td>
                        <td style={{padding:8, borderBottom:"1px solid #eee"}}>{j.type}</td>
                        <td style={{padding:8, borderBottom:"1px solid #eee"}}>
                          <span style={{
                            padding:"4px 8px",
                            borderRadius:3,
                            background: j.status === "done" ? "#d4edda" : j.status === "failed" ? "#f8d7da" : "#fff3cd",
                            fontSize:12
                          }}>{j.status}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
          <p style={{marginTop:20}}>
            <a href={apiBase + "/docs"} target="_blank" style={{color:"#0070f3"}}>Backend API Docs</a> | 
            <a href={apiBase + "/reports/system-card/1"} target="_blank" style={{color:"#0070f3", marginLeft:10}}>System Card</a>
          </p>
        </>
      )}
    </div>
  );
}
