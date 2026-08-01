#!/usr/bin/env python
"""
Test all 7 patterns without hanging or waiting for input.
Run with: py test_all_patterns.py
"""

import subprocess
import sys
import json
import time
from pathlib import Path

def run_pattern(pattern_num: int, description: str, command: list) -> bool:
    """Run a pattern and report success/failure"""
    print(f"\n{'='*60}")
    print(f"Pattern {pattern_num}: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS")
            if result.stdout:
                print("Output (first 200 chars):")
                print(result.stdout[:200])
            return True
        else:
            print(f"❌ FAILED (exit code: {result.returncode})")
            if result.stderr:
                print("Error:")
                print(result.stderr[:200])
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  TIMEOUT - Pattern took too long (skipped for safety)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🧪 TESTING ALL 7 PATTERNS")
    print("="*60)
    
    results = {}
    
    # Pattern 1: Library
    results[1] = run_pattern(
        1,
        "Python Library",
        ["python", "pattern_1_library.py"]
    )
    
    # Pattern 2: JSON API
    json_input = json.dumps({
        "cn": "test-pattern-2.com",
        "key_type": "rsa",
        "key_strength": 2048
    })
    results[2] = run_pattern(
        2,
        "JSON stdin/stdout",
        ["python", "pattern_2_json_api.py", json_input]
    )
    
    # Pattern 3: Config File
    results[3] = run_pattern(
        3,
        "Config File",
        ["python", "pattern_3_config_file.py", "config_example.json"]
    )
    
    # Pattern 4: REST API (skip with note - it runs forever)
    print(f"\n{'='*60}")
    print(f"Pattern 4: REST API")
    print(f"{'='*60}")
    print("⏭️  SKIPPED - REST server runs indefinitely")
    print("To test: python pattern_4_rest_api.py")
    print("Then in another terminal: curl -X POST http://localhost:5000/api/v1/certificate ...")
    print("Or use PowerShell: Invoke-WebRequest ...")
    results[4] = None  # N/A
    
    # Pattern 5: Callable Service
    results[5] = run_pattern(
        5,
        "Callable Service",
        ["python", "pattern_5_callable_service.py"]
    )
    
    # Pattern 6: Abstract Interface
    results[6] = run_pattern(
        6,
        "Abstract Interface",
        ["python", "pattern_6_abstract_interface.py"]
    )
    
    # Pattern 7: Event-Driven
    results[7] = run_pattern(
        7,
        "Event-Driven",
        ["python", "pattern_7_event_driven.py"]
    )
    
    # Summary
    print(f"\n\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    for pattern, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⏭️  SKIP"
        print(f"  Pattern {pattern}: {status}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    print(f"{'='*60}\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
