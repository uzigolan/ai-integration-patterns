#!/usr/bin/env python3
"""
PATTERN 4: REST API INTERFACE
=============================
AI makes HTTP requests to a server
No knowledge of implementation, only API endpoints and HTTP
Perfect for remote systems and cloud deployments
"""

import json
from flask import Flask, request, jsonify
from cert_generator import CertificateGenerator, CertificateParams

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "version": "1.0"})


@app.route('/api/v1/certificate', methods=['POST'])
def generate_certificate():
    """
    Generate a certificate via HTTP POST
    
    Request:
    POST /api/v1/certificate
    Content-Type: application/json
    
    {
        "cn": "example.com",
        "key_type": "rsa",
        "key_strength": 2048,
        "validity_days": 365,
        "country": "US",
        "state": "California",
        "locality": "San Francisco",
        "organization": "My Company"
    }
    
    Response (200 OK):
    {
        "success": true,
        "message": "Certificate generated successfully for example.com",
        "cert_path": "/certs/example.com.crt",
        "key_path": "/certs/example.com.key",
        "details": {...}
    }
    
    Response (400/500):
    {
        "success": false,
        "message": "Error description",
        "error": "Detailed error"
    }
    """
    try:
        # Parse JSON from request body with fallback
        data = None
        
        # Try Flask's built-in JSON parser first
        if request.is_json:
            data = request.json
        
        # Fallback: try parsing raw data if is_json check or json parsing failed
        if not data and request.data:
            try:
                data = json.loads(request.data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request",
                "error": "Request body must be valid JSON. Make sure Content-Type is 'application/json'"
            }), 400
        
        # Validate required field
        if not data.get("cn"):
            return jsonify({
                "success": False,
                "message": "Missing required parameter",
                "error": "Field 'cn' (Common Name) is required. Example: {\"cn\":\"example.com\"}"
            }), 400

        params = CertificateParams(
            cn=data.get("cn"),
            key_type=data.get("key_type", "rsa"),
            key_strength=int(data.get("key_strength", 2048)),
            validity_days=int(data.get("validity_days", 365)),
            country=data.get("country"),
            state=data.get("state"),
            locality=data.get("locality"),
            organization=data.get("organization"),
            output_dir=data.get("output_dir", "./certs")
        )

        generator = CertificateGenerator()
        result = generator.generate(params)

        return jsonify({
            "success": result.success,
            "message": result.message,
            "cert_path": result.cert_path,
            "key_path": result.key_path,
            "details": result.details,
            "error": result.error
        }), 200 if result.success else 400

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": "Invalid parameters",
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Internal error",
            "error": str(e)
        }), 500


@app.route('/api/v1/certificate/batch', methods=['POST'])
def generate_batch():
    """
    Generate multiple certificates in batch
    
    Request:
    POST /api/v1/certificate/batch
    Content-Type: application/json
    
    {
        "certificates": [
            {"cn": "api.example.com", "key_type": "rsa"},
            {"cn": "web.example.com", "key_type": "ec", "key_strength": 256}
        ]
    }
    
    Response:
    {
        "success": true,
        "message": "Generated 2 certificates",
        "results": [
            {"cn": "api.example.com", "success": true, "cert_path": "..."},
            {"cn": "web.example.com", "success": true, "cert_path": "..."}
        ]
    }
    """
    try:
        data = request.json or {}
        certificates = data.get("certificates", [])

        results = []
        generator = CertificateGenerator()

        for cert_data in certificates:
            params = CertificateParams(
                cn=cert_data.get("cn"),
                key_type=cert_data.get("key_type", "rsa"),
                key_strength=int(cert_data.get("key_strength", 2048)),
                validity_days=int(cert_data.get("validity_days", 365)),
                country=cert_data.get("country"),
                state=cert_data.get("state"),
                locality=cert_data.get("locality"),
                organization=cert_data.get("organization"),
                output_dir=cert_data.get("output_dir", "./certs")
            )

            result = generator.generate(params)
            results.append({
                "cn": params.cn,
                "success": result.success,
                "cert_path": result.cert_path,
                "key_path": result.key_path,
                "message": result.message
            })

        all_success = all(r["success"] for r in results)
        return jsonify({
            "success": all_success,
            "message": f"Processed {len(certificates)} certificate requests",
            "results": results
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Batch processing failed",
            "error": str(e)
        }), 500


# AI pattern: Make HTTP requests
def ai_pattern_4_rest_api():
    """Example: AI makes HTTP requests (this would use requests library in real code)"""
    
    import requests  # In real usage
    
    # AI sends HTTP request
    # response = requests.post(
    #     "http://localhost:5000/api/v1/certificate",
    #     json={
    #         "cn": "example.com",
    #         "key_type": "rsa",
    #         "key_strength": 2048,
    #         "validity_days": 365
    #     }
    # )
    # result = response.json()
    
    print("""
    AI Pattern 4 - REST API:
    - AI knows only HTTP endpoints
    - AI knows request/response JSON schemas
    - AI doesn't know implementation
    - Can call from any language/system
    """)


if __name__ == "__main__":
    print("Starting Certificate Generator REST API on port 5000...")
    print("Endpoints:")
    print("  GET  /health")
    print("  POST /api/v1/certificate")
    print("  POST /api/v1/certificate/batch")
    app.run(debug=False, port=5000, host="localhost")
