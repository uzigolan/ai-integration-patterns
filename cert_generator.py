#!/usr/bin/env python3
"""
Self-Signed Certificate Generator
Abstracts OpenSSL certificate generation with clean Python interface
"""

import subprocess
import os
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class CertificateParams:
    """Certificate generation parameters"""
    cn: str  # Common Name
    key_type: str = "rsa"  # rsa, ec
    key_strength: int = 2048  # For RSA: 2048, 4096; For EC: 256, 384, 521
    validity_days: int = 365
    country: Optional[str] = None
    state: Optional[str] = None
    locality: Optional[str] = None
    organization: Optional[str] = None
    output_dir: Optional[str] = None

    def __post_init__(self):
        if self.key_type.lower() not in ["rsa", "ec"]:
            raise ValueError(f"key_type must be 'rsa' or 'ec', got {self.key_type}")
        if self.key_type.lower() == "rsa" and self.key_strength not in [2048, 4096]:
            raise ValueError(f"RSA key_strength must be 2048 or 4096, got {self.key_strength}")
        if self.key_type.lower() == "ec" and self.key_strength not in [256, 384, 521]:
            raise ValueError(f"EC key_strength must be 256, 384, or 521, got {self.key_strength}")


@dataclass
class CertificateOutput:
    """Certificate generation output"""
    success: bool
    message: str
    cert_path: Optional[str] = None
    key_path: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CertificateGenerator:
    """Core certificate generation logic"""

    def __init__(self, openssl_path: str = "openssl"):
        self.openssl_path = openssl_path
        self._verify_openssl()

    def _verify_openssl(self):
        """Verify OpenSSL is installed and accessible"""
        try:
            subprocess.run(
                [self.openssl_path, "version"],
                capture_output=True,
                check=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            raise RuntimeError(f"OpenSSL not found or not accessible: {e}")

    def generate(self, params: CertificateParams) -> CertificateOutput:
        """Generate a self-signed certificate"""
        try:
            # Set output directory
            output_dir = Path(params.output_dir or ".")
            output_dir.mkdir(parents=True, exist_ok=True)

            cert_path = output_dir / f"{params.cn}.crt"
            key_path = output_dir / f"{params.cn}.key"

            # Build subject string
            subject = self._build_subject(params)

            # Build OpenSSL command
            cmd = self._build_command(
                params, subject, str(cert_path), str(key_path)
            )

            # Execute OpenSSL
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=30
            )

            if result.returncode != 0:
                return CertificateOutput(
                    success=False,
                    message="Certificate generation failed",
                    error=result.stderr
                )

            # Verify files exist
            if not cert_path.exists() or not key_path.exists():
                return CertificateOutput(
                    success=False,
                    message="Certificate files not created",
                    error="OpenSSL did not produce output files"
                )

            return CertificateOutput(
                success=True,
                message=f"Certificate generated successfully for {params.cn}",
                cert_path=str(cert_path),
                key_path=str(key_path),
                details=self._get_cert_details(str(cert_path), params)
            )

        except subprocess.TimeoutExpired:
            return CertificateOutput(
                success=False,
                message="Certificate generation timed out",
                error="OpenSSL operation exceeded 30 seconds"
            )
        except Exception as e:
            return CertificateOutput(
                success=False,
                message="Unexpected error during certificate generation",
                error=str(e)
            )

    def _build_subject(self, params: CertificateParams) -> str:
        """Build X.509 subject string"""
        parts = []
        if params.country:
            parts.append(f"C={params.country}")
        if params.state:
            parts.append(f"ST={params.state}")
        if params.locality:
            parts.append(f"L={params.locality}")
        if params.organization:
            parts.append(f"O={params.organization}")
        parts.append(f"CN={params.cn}")
        return "/".join(parts)

    def _build_command(
        self, params: CertificateParams, subject: str, cert_path: str, key_path: str
    ) -> list:
        """Build OpenSSL command"""
        cmd = [self.openssl_path, "req", "-x509", "-nodes"]

        # Add key type and strength
        if params.key_type.lower() == "rsa":
            cmd.extend(["-newkey", f"rsa:{params.key_strength}"])
        else:  # ec - use curve name directly (works on Windows without process substitution)
            curve_map = {256: "P-256", 384: "P-384", 521: "P-521"}
            curve = curve_map.get(params.key_strength, "P-256")
            cmd.extend(["-newkey", f"ec", "-pkeyopt", f"ec_paramgen_curve:{curve}"])

        # Add other parameters
        cmd.extend([
            "-keyout", key_path,
            "-out", cert_path,
            "-days", str(params.validity_days),
            "-subj", f"/{subject}"
        ])

        return cmd

    def _get_cert_details(self, cert_path: str, params: CertificateParams) -> Dict[str, Any]:
        """Extract certificate details"""
        try:
            result = subprocess.run(
                [self.openssl_path, "x509", "-in", cert_path, "-noout", "-text"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "cn": params.cn,
                "key_type": params.key_type,
                "key_strength": params.key_strength,
                "validity_days": params.validity_days,
                "generated_at": datetime.now().isoformat()
            }
        except Exception:
            return {}


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate self-signed certificates")
    parser.add_argument("cn", help="Common Name for certificate")
    parser.add_argument("--key-type", default="rsa", choices=["rsa", "ec"],
                        help="Key type (default: rsa)")
    parser.add_argument("--key-strength", type=int, default=2048,
                        help="Key strength in bits (RSA: 2048/4096, EC: 256/384/521)")
    parser.add_argument("--validity-days", type=int, default=365,
                        help="Certificate validity in days (default: 365)")
    parser.add_argument("--country", help="Country code (C)")
    parser.add_argument("--state", help="State/Province (ST)")
    parser.add_argument("--locality", help="Locality (L)")
    parser.add_argument("--organization", help="Organization (O)")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    try:
        params = CertificateParams(
            cn=args.cn,
            key_type=args.key_type,
            key_strength=args.key_strength,
            validity_days=args.validity_days,
            country=args.country,
            state=args.state,
            locality=args.locality,
            organization=args.organization,
            output_dir=args.output_dir
        )

        generator = CertificateGenerator()
        result = generator.generate(params)

        if args.json:
            print(json.dumps({
                "success": result.success,
                "message": result.message,
                "cert_path": result.cert_path,
                "key_path": result.key_path,
                "details": result.details,
                "error": result.error
            }, indent=2))
        else:
            print(result.message)
            if result.cert_path:
                print(f"Certificate: {result.cert_path}")
                print(f"Private Key: {result.key_path}")
            if result.error:
                print(f"Error: {result.error}", file=sys.stderr)
                sys.exit(1)

    except ValueError as e:
        print(f"Invalid argument: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
