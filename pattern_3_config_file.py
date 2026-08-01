#!/usr/bin/env python3
"""
PATTERN 3: CONFIGURATION FILE INTERFACE
=======================================
AI creates a config file, invokes the program, reads results
No knowledge of internals, uses declarative config
Perfect for workflow orchestration and batch processing
"""

import json
import yaml
import sys
from pathlib import Path
from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput


def generate_from_config_file(config_file: str) -> CertificateOutput:
    """
    Generate certificate from configuration file
    
    Config file format: YAML or JSON
    
    Example YAML (config.yaml):
    ---
    certificates:
      - cn: "api.example.com"
        key_type: "rsa"
        key_strength: 2048
        validity_days: 365
        organization: "My Company"
        output_dir: "./certs"
        
      - cn: "*.example.com"
        key_type: "rsa"
        key_strength: 4096
        validity_days: 730
        organization: "My Company"
        output_dir: "./certs"
    
    Example JSON (config.json):
    {
      "certificates": [
        {
          "cn": "api.example.com",
          "key_type": "rsa",
          "key_strength": 2048,
          "validity_days": 365
        }
      ]
    }
    """
    config_path = Path(config_file)

    try:
        if config_path.suffix in [".yaml", ".yml"]:
            with open(config_path) as f:
                config = yaml.safe_load(f)
        elif config_path.suffix == ".json":
            with open(config_path) as f:
                config = json.load(f)
        else:
            return CertificateOutput(
                success=False,
                message="Unsupported config file format",
                error="Use .yaml, .yml, or .json"
            )

        generator = CertificateGenerator()
        results = []

        for cert_config in config.get("certificates", []):
            params = CertificateParams(
                cn=cert_config.get("cn"),
                key_type=cert_config.get("key_type", "rsa"),
                key_strength=cert_config.get("key_strength", 2048),
                validity_days=cert_config.get("validity_days", 365),
                country=cert_config.get("country"),
                state=cert_config.get("state"),
                locality=cert_config.get("locality"),
                organization=cert_config.get("organization"),
                output_dir=cert_config.get("output_dir")
            )
            result = generator.generate(params)
            results.append(result)

        # Return aggregated result
        all_success = all(r.success for r in results)
        return CertificateOutput(
            success=all_success,
            message=f"Generated {len(results)} certificates",
            details={
                "total": len(results),
                "successful": sum(1 for r in results if r.success),
                "failed": sum(1 for r in results if not r.success),
                "results": [
                    {
                        "cn": r.details.get("cn") if r.details else "unknown",
                        "success": r.success,
                        "cert_path": r.cert_path
                    }
                    for r in results
                ]
            }
        )

    except FileNotFoundError:
        return CertificateOutput(
            success=False,
            message="Configuration file not found",
            error=str(config_file)
        )
    except Exception as e:
        return CertificateOutput(
            success=False,
            message="Failed to process configuration",
            error=str(e)
        )


# AI generates config and uses this pattern:
def ai_pattern_3_config():
    """Example: AI creates config, generates certificates"""
    
    config = {
        "certificates": [
            {
                "cn": "myapp.com",
                "key_type": "rsa",
                "key_strength": 2048,
                "validity_days": 365,
                "organization": "My Company"
            },
            {
                "cn": "api.myapp.com",
                "key_type": "rsa",
                "key_strength": 4096,
                "validity_days": 730
            }
        ]
    }
    
    # AI writes config file
    config_path = Path("cert_config.json")
    config_path.write_text(json.dumps(config, indent=2))
    
    # AI invokes generation
    result = generate_from_config_file("cert_config.json")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pattern_3_config_file.py <config_file.yaml|json>")
        sys.exit(1)

    result = generate_from_config_file(sys.argv[1])
    print(json.dumps({
        "success": result.success,
        "message": result.message,
        "details": result.details,
        "error": result.error
    }, indent=2))
