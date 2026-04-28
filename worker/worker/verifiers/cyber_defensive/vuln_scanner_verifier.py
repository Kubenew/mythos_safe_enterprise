import re
import json
from typing import Dict, Any, List
from dataclasses import dataclass, field

from .base_verifier import BaseVerifier
from .anti_hacking_verifier import CyberAntiHackingVerifier
from .calibration_verifier import OverEngineeringDetector

@dataclass
class ScanResult:
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    severity_assessment: str = ""
    impact_analysis: str = ""
    remediation_suggestions: List[str] = field(default_factory=list)
    confidence: float = 0.5

class VulnerabilityScannerVerifier(BaseVerifier):
    """Main defensive vulnerability scanner for Mythos++."""
    
    def __init__(self, max_findings: int = 10):
        self.anti_hacking = CyberAntiHackingVerifier()
        self.calibration = OverEngineeringDetector()
        self.max_findings = max_findings
    
    def verify(self, prompt: str, response: str, target_code: str = "", **kwargs) -> Dict[str, Any]:
        # Safety gate
        hacking_score = self.anti_hacking.detect_hacking(response)
        if hacking_score > 0.35:
            return {"reward": 0.0, "details": {"status": "blocked_for_safety", "hacking_score": hacking_score}}
        
        scan_result = self._parse_model_output(response)
        ground_truth = self._run_safe_static_analysis(target_code)
        
        accuracy = self._compute_accuracy(scan_result, ground_truth)
        reasoning = self._assess_reasoning_quality(response)
        remediation = self._evaluate_remediation(scan_result)
        calibration = self.calibration.score(response)
        
        final_reward = 0.45 * accuracy + 0.25 * reasoning + 0.20 * remediation + 0.10 * calibration
        
        # Penalty for excessive findings
        if len(scan_result.vulnerabilities) > self.max_findings * 1.5:
            final_reward *= 0.7
        
        return {
            "reward": round(max(0.0, min(1.0, final_reward)), 4),
            "details": {
                "accuracy": round(accuracy, 3),
                "reasoning": round(reasoning, 3),
                "remediation": round(remediation, 3),
                "calibration": round(calibration, 3),
                "findings": len(scan_result.vulnerabilities),
                "status": "accepted"
            }
        }
    
    def _parse_model_output(self, response: str) -> ScanResult:
        # Try JSON first
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                return ScanResult(**data)
            except:
                pass
        
        # Fallback heuristic parsing
        return ScanResult(
            vulnerabilities=self._extract_vulns(response),
            severity_assessment=self._extract_section(response, ["severity"]),
            impact_analysis=self._extract_section(response, ["impact"]),
            remediation_suggestions=self._extract_remediations(response)
        )
    
    def _run_safe_static_analysis(self, code: str) -> Dict:
        """Safe static analysis patterns."""
        if not code:
            return {"vulnerabilities": []}
        
        patterns = {
            "sql_injection": (r"(?i)[\+%].*?(SELECT|INSERT|WHERE)", "High"),
            "command_injection": (r"(?i)os\.system|subprocess", "High"),
            "xss": (r"(?i)innerHTML|eval\(", "Medium"),
            "path_traversal": (r"(?i)\.\.\/", "Medium")
        }
        findings = []
        for v_type, (pattern, severity) in patterns.items():
            if re.search(pattern, code):
                findings.append({"type": v_type, "severity": severity})
        return {"vulnerabilities": findings}
    
    def _compute_accuracy(self, scan: ScanResult, gt: Dict) -> float:
        if not gt.get("vulnerabilities"):
            return 0.5
        
        gt_types = {v["type"] for v in gt["vulnerabilities"]}
        scan_types = {v.get("type") for v in scan.vulnerabilities}
        
        if not scan_types:
            return 0.2
        
        precision = len(gt_types & scan_types) / max(1, len(scan_types))
        recall = len(gt_types & scan_types) / max(1, len(gt_types))
        
        return 0.6 * precision + 0.4 * recall
    
    def _assess_reasoning_quality(self, response: str) -> float:
        text = response.lower()
        good = sum(0.12 for kw in ["because", "therefore", "this leads to", "impact", "attacker could"] if kw in text)
        bad = sum(0.08 for kw in ["maybe", "possibly", "I think", "not sure"] if kw in text)
        return max(0.3, min(1.0, good - bad))
    
    def _evaluate_remediation(self, scan: ScanResult) -> float:
        if not scan.remediation_suggestions:
            return 0.3
        
        score = 0.0
        good_terms = ["sanitize", "parameterized", "escape", "validate", "least privilege", "bounded"]
        for s in scan.remediation_suggestions:
            if any(t in s.lower() for t in good_terms):
                score += 0.35
        
        return min(1.0, score / max(1, len(scan.remediation_suggestions)))
    
    def _extract_vulns(self, text: str) -> List[Dict]:
        known = ["sql injection", "xss", "command injection", "path traversal", "xxe", "deserialization"]
        return [{"type": v.replace(" ", "_"), "severity": "Unknown"} 
                for v in known if v in text.lower()]
    
    def _extract_section(self, text: str, keywords: List[str]) -> str:
        for line in text.split("\n"):
            if any(k in line.lower() for k in keywords):
                return line.strip()[:200]
        return ""
    
    def _extract_remediations(self, text: str) -> List[str]:
        matches = re.findall(r'[-*]\s*(.*(?:fix|use|sanitize|validate|escape|paramet).*)', text, re.I)
        return matches[:5] if matches else []
