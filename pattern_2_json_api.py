#!/usr/bin/env python3
"""
PATTERN 2: JSON STDIN/STDOUT INTERFACE
======================================
AI sends JSON to stdin, receives JSON from stdout
No knowledge of Python, CLI args, or internal implementation
AI sees: JSON schema for input and output
Perfect for LLMs and language-agnostic tools
"""

import json
import sys
from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput


def process_json_request(json_str: str) -> str:
    """
    Process certificate request from JSON input
    
    Input JSON Schema:
    {
        "cn": "example.com",
        "key_type": "rsa",                    # "rsa" or "ec"
        "key_strength": 2048,                 # 2048, 4096 for RSA; 256, 384, 521 for EC
        "validity_days": 365,                 # days certificate is valid
        "country": "US",                      # optional
        "state": "California",                # optional
        "locality": "San Francisco",          # optional
        "organization": "My Company",         # optional
        "output_dir": "./certs"               # optional, defaults to current dir
    }
    
    Output JSON Schema:
    {
        "success": true/false,
        "message": "Human readable message",
        "cert_path": "/path/to/cert.crt" or null,
        "key_path": "/path/to/cert.key" or null,
        "details": {...} or null,
        "error": "error message" or null
    }
    """
    try:
        request = json.loads(json_str)
    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "message": "Invalid JSON input",
            "error": str(e)
        })

    try:
        params = CertificateParams(
            cn=request.get("cn"),
            key_type=request.get("key_type", "rsa"),
            key_strength=request.get("key_strength", 2048),
            validity_days=request.get("validity_days", 365),
            country=request.get("country"),
            state=request.get("state"),
            locality=request.get("locality"),
            organization=request.get("organization"),
            output_dir=request.get("output_dir")
        )

        generator = CertificateGenerator()
        result: CertificateOutput = generator.generate(params)

        return json.dumps({
            "success": result.success,
            "message": result.message,
            "cert_path": result.cert_path,
            "key_path": result.key_path,
            "details": result.details,
            "error": result.error
        }, indent=2)

    except ValueError as e:
        return json.dumps({
            "success": False,
            "message": "Invalid parameters",
            "error": str(e)
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Unexpected error",
            "error": str(e)
        })


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # If JSON passed as argument
        json_input = sys.argv[1]
    elif not sys.stdin.isatty():
        # If stdin is piped (not a terminal)
        json_input = sys.stdin.read()
    else:
        # No input provided - show usage and example
        print("Usage: python pattern_2_json_api.py '<JSON>' or pipe JSON via stdin")
        print("\nExample (direct argument):")
        print('  python pattern_2_json_api.py \'{"cn":"example.com","key_type":"rsa"}\'')
        print("\nExample (pipe):")
        print('  echo \'{"cn":"example.com"}\' | python pattern_2_json_api.py')
        print("\nExample (PowerShell):")
        print('  $json = \'{"cn":"example.com"}\' | python pattern_2_json_api.py')
        sys.exit(0)

    result = process_json_request(json_input)
    print(result)
