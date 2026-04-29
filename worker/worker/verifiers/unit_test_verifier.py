import subprocess
import os
import sys
from dataclasses import dataclass

@dataclass
class UnitTestResult:
    ok: bool
    stdout: str
    stderr: str
    returncode: int

def run_pytest(repo_path: str, timeout_sec: int = 120) -> UnitTestResult:
    if not os.path.isdir(repo_path):
        raise ValueError(f"Repo path not found: {repo_path}")
    
    cmd = [sys.executable, "-m", "pytest", "-q"]
    try:
        p = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return UnitTestResult(
            ok=(p.returncode == 0),
            stdout=p.stdout,
            stderr=p.stderr,
            returncode=p.returncode,
        )
    except subprocess.TimeoutExpired as e:
        return UnitTestResult(ok=False, stdout=e.stdout or "", stderr="TIMEOUT", returncode=124)
