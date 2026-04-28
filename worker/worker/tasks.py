import json
import os
import sys
from sqlalchemy import text
from worker.celery_app import celery
from worker.db import SessionLocal

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from worker.model_client import get_model_response

def append_log(db, job_id: int, msg: str):
    db.execute(text("UPDATE jobs SET logs = COALESCE(logs,'') || :m WHERE id=:id"), {"m": msg + "\n", "id": job_id})

@celery.task(name="worker.tasks.run_job")
def run_job(job_id: int):
    db = SessionLocal()
    try:
        db.execute(text("UPDATE jobs SET status='running' WHERE id=:id"), {"id": job_id})
        db.commit()
        
        row = db.execute(text("SELECT id, type, input_json FROM jobs WHERE id=:id"), {"id": job_id}).fetchone()
        payload = json.loads(row.input_json or "{}")
        
        append_log(db, job_id, f"Running job {job_id} type={row.type}")
        db.commit()
        
        if row.type == "eval":
            result = run_evaluation(payload)
        elif row.type == "math_eval":
            result = run_math_evaluation(payload)
        elif row.type == "cyber_eval":
            result = run_cyber_evaluation(payload)
        else:
            result = {"ok": True, "message": "Job completed", "result": "placeholder"}
        
        db.execute(text("UPDATE jobs SET status='done', output_json=:out WHERE id=:id"),
                   {"out": json.dumps(result), "id": job_id})
        append_log(db, job_id, f"Done. Result: {json.dumps(result)[:200]}")
        db.commit()
    except Exception as e:
        db.execute(text("UPDATE jobs SET status='failed' WHERE id=:id"), {"id": job_id})
        append_log(db, job_id, f"ERROR: {str(e)}")
        db.commit()
        raise
    finally:
        db.close()

def run_evaluation(payload: dict) -> dict:
    suite_type = payload.get("suite", "math_mini")
    
    if suite_type == "math_mini":
        return run_math_evaluation(payload)
    elif suite_type == "cyber_defensive":
        return run_cyber_evaluation(payload)
    else:
        return {"ok": False, "error": f"Unknown suite type: {suite_type}"}

def run_math_evaluation(payload: dict) -> dict:
    try:
        from worker.verifiers.math_exact_match import MathVerifier
        
        verifier = MathVerifier()
        
        model_endpoint = payload.get("model_endpoint", "")
        api_key = payload.get("api_key", "")
        model_name = payload.get("model_name", "")
        
        items = payload.get("items", [
            {"id": "q1", "prompt": "What is 2+2?", "expected": "4"},
            {"id": "q2", "prompt": "Compute 7*6", "expected": "42"}
        ])
        
        results = []
        for item in items:
            expected = item["expected"]
            
            if model_endpoint:
                try:
                    got = get_model_response(model_endpoint, item["prompt"], api_key, model_name)
                except Exception as e:
                    got = f"ERROR: {str(e)}"
            else:
                got = item.get("baseline_answer", "")
            
            result = verifier.verify(item["prompt"], got, expected=expected)
            results.append({
                "id": item["id"],
                "ok": result["reward"] > 0.5,
                "reward": result["reward"],
                "expected": expected,
                "got": got
            })
        
        acc = sum(1 for x in results if x["ok"]) / max(1, len(results))
        
        return {
            "ok": True,
            "accuracy": acc,
            "results": results,
            "suite": "math_mini"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def run_cyber_evaluation(payload: dict) -> dict:
    try:
        from worker.verifiers.cyber_defensive import VulnerabilityScannerVerifier
        
        verifier = VulnerabilityScannerVerifier()
        target_code = payload.get("target_code", "")
        
        model_endpoint = payload.get("model_endpoint", "")
        api_key = payload.get("api_key", "")
        model_name = payload.get("model_name", "")
        
        prompt = payload.get("prompt", f"Analyze this code for vulnerabilities:\n{target_code}")
        
        if model_endpoint:
            try:
                model_response = get_model_response(model_endpoint, prompt, api_key, model_name)
            except Exception as e:
                model_response = f"ERROR: {str(e)}"
        else:
            model_response = payload.get("model_response", "No response provided")
        
        result = verifier.verify(prompt, model_response, target_code=target_code)
        
        return {
            "ok": True,
            "reward": result["reward"],
            "details": result["details"],
            "suite": "cyber_defensive",
            "model_response": model_response[:500]
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
