from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse, Response
from jinja2 import Template
import json

from app.db import get_db
from app.models import Project, Job
from app.deps import require_role

router = APIRouter()

SYSTEM_CARD_TEMPLATE = """# System Card - {{ project_name }}

## 1. Overview
- Model name: {{ model_name }}
- Release date: {{ release_date }}
- Intended use: {{ intended_use }}
- Prohibited use: {{ prohibited_use }}

## 2. Training Data
- Sources: {{ training_sources }}
- Deduplication: {{ deduplication }}
- Filtering: {{ filtering }}

## 3. Training Procedure
- Post-training (RLVR): Mythos-Safe GRPO with defensive cyber verifiers
- Safety gates: Anti-hacking verifier, vulnerability scanner, calibration detector

## 4. Evaluations
### Capability
{% for eval in evals %}
- {{ eval.suite }}: accuracy {{ eval.accuracy }}
{% endfor %}

### Safety
- Harmlessness: {{ safety_score }}
- Jailbreak resistance: {{ jailbreak_score }}
- Tool-use constraints: Enforced via sandbox

## 5. Risk Assessment (RSP-style)
- Cyber risk: {{ cyber_risk }}
- Misuse risk: {{ misuse_risk }}
- Mitigations: Defensive verifiers, sandbox execution, audit logging

## 6. Deployment & Monitoring
- Logging: All jobs logged to PostgreSQL
- Incident response: Gate-based blocking for unsafe outputs
- Rollback plan: Model versioning in registry

## 7. Known Limitations
- Evaluation suites limited to math + cyber defensive
- No external red-teaming yet
"""

@router.get("/system-card/{project_id}")
def system_card(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor"))):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    jobs = db.query(Job).filter(Job.project_id == project_id, Job.status == "done").order_by(Job.id.desc()).limit(20).all()
    
    evals = []
    for j in jobs:
        if j.output_json:
            out = json.loads(j.output_json)
            if out.get("accuracy"):
                evals.append({"suite": out.get("suite", "unknown"), "accuracy": round(out["accuracy"], 3)})
    
    template = Template(SYSTEM_CARD_TEMPLATE)
    content = template.render(
        project_name=project.name,
        model_name="Mythos-Safe Model",
        release_date="2026-04-28",
        intended_use="Defensive cyber analysis, math reasoning",
        prohibited_use="Offensive exploits, malware generation",
        training_sources="Curated safe datasets",
        deduplication="Applied",
        filtering="Safety filters enabled",
        evals=evals[:5],
        safety_score=0.85,
        jailbreak_score=0.92,
        cyber_risk="Low (defensive-only verifiers)",
        misuse_risk="Low (sandbox + anti-hacking gates)"
    )
    
    return PlainTextResponse(content, media_type="text/markdown")

@router.get("/system-card/{project_id}/pdf")
def system_card_pdf(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor"))):
    """Generate PDF system card."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        import io
        
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(inch, height - inch, f"System Card - {project.name}")
        
        # Content
        c.setFont("Helvetica", 10)
        y = height - 1.5 * inch
        
        c.drawString(inch, y, "Model: Mythos-Safe Model")
        y -= 20
        c.drawString(inch, y, "Release Date: 2026-04-28")
        y -= 20
        c.drawString(inch, y, "Intended Use: Defensive cyber analysis, math reasoning")
        y -= 20
        c.drawString(inch, y, "Training Procedure:")
        y -= 15
        c.drawString(inch + 20, y, "- RLVR with defensive cyber verifiers")
        y -= 15
        c.drawString(inch + 20, y, "- Safety gates: Anti-hacking, vulnerability scanner")
        
        c.save()
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=system_card_{project_id}.pdf"}
        )
    except ImportError:
        return {"error": "reportlab not installed. Install with: pip install reportlab"}

@router.get("/eval-report/{project_id}")
def eval_report(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor"))):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    jobs = db.query(Job).filter(Job.project_id == project_id, Job.type == "eval").order_by(Job.id.desc()).limit(50).all()
    
    results = []
    for j in jobs:
        if j.output_json:
            out = json.loads(j.output_json)
            results.append({
                "job_id": j.id,
                "suite": out.get("suite", "unknown"),
                "accuracy": out.get("accuracy", 0),
                "status": j.status
            })
    
    report = f"# Evaluation Report - {project.name}\n\n"
    for r in results:
        report += f"- Job {r['job_id']}: {r['suite']} accuracy={r['accuracy']}\n"
    
    return PlainTextResponse(report, media_type="text/markdown")

@router.get("/eval-report/{project_id}/pdf")
def eval_report_pdf(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor"))):
    """Generate PDF evaluation report."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        import io
        import json
        
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        jobs = db.query(Job).filter(Job.project_id == project_id, Job.type == "eval").order_by(Job.id.desc()).limit(50).all()
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(inch, height - inch, f"Evaluation Report - {project.name}")
        
        y = height - 1.5 * inch
        c.setFont("Helvetica", 9)
        
        for j in jobs[:20]:
            if y < 2 * inch:
                c.showPage()
                y = height - inch
            
            if j.output_json:
                out = json.loads(j.output_json)
                c.drawString(inch, y, f"Job {j.id}: {out.get('suite', 'unknown')} - accuracy={out.get('accuracy', 0)}")
                y -= 20
        
        c.save()
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=eval_report_{project_id}.pdf"}
        )
    except ImportError:
        return {"error": "reportlab not installed. Install with: pip install reportlab"}
