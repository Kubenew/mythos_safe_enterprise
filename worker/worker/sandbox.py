import subprocess
import tempfile
import os
from typing import Dict, Any

def run_in_sandbox(code: str, test_code: str = "", timeout: int = 30) -> Dict[str, Any]:
    """
    Run code in a sandboxed Docker container.
    In production, this would use gVisor (runsc) or Firecracker.
    """
    # Create temporary files
    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "solution.py")
        test_path = os.path.join(tmpdir, "test_solution.py")
        
        with open(code_path, "w") as f:
            f.write(code)
        
        if test_code:
            with open(test_path, "w") as f:
                f.write(test_code)
        else:
            # Default test
            with open(test_path, "w") as f:
                f.write("""
import subprocess
result = subprocess.run(["python", "solution.py"], capture_output=True, text=True, timeout=10)
print(result.stdout)
""")
        
        # Run in Docker with security constraints
        # In production with gVisor: --runtime=runsc
        cmd = [
            "docker", "run",
            "--rm",
            "--memory=128m",
            "--cpus=0.5",
            "--network=none",
            "--read-only",
            "-v", f"{tmpdir}:/sandbox:ro",
            "python:3.11-slim",
            "python", "/sandbox/test_solution.py"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir
            )
            
            return {
                "ok": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "stdout": "",
                "stderr": "TIMEOUT",
                "returncode": 124
            }
        except Exception as e:
            return {
                "ok": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }

def run_cyber_scan_sandbox(code: str) -> Dict[str, Any]:
    """
    Run cyber security scan in sandboxed environment.
    Uses semgrep in a container with gVisor (if available).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "target_code.py")
        
        with open(code_path, "w") as f:
            f.write(code)
        
        # Run semgrep in container
        cmd = [
            "docker", "run",
            "--rm",
            "--memory=256m",
            "--network=none",
            "-v", f"{tmpdir}:/code",
            "returntocorp/semgrep",
            "semgrep", "--config=auto", "/code/target_code.py"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "ok": True,
                "findings": result.stdout,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "ok": False,
                "findings": str(e),
                "returncode": -1
            }
