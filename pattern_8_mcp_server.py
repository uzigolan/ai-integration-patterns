#!/usr/bin/env python3
"""Pattern 8: Model Context Protocol (MCP) server for certificate generation.

This exposes focused, schema-derived tools to MCP clients such as Codex while
keeping certificate generation behind a controlled boundary. The pure helper
functions work without the optional ``fastmcp`` package for simple testing.
"""

from dataclasses import asdict
from pathlib import Path
import re
import sys
from typing import Any, Dict

from cert_generator import CertificateGenerator, CertificateParams


DEFAULT_OUTPUT_DIR = Path(__file__).with_name("certs")
SAFE_CN = re.compile(r"^[A-Za-z0-9*](?:[A-Za-z0-9*.-]{0,251}[A-Za-z0-9*])?$")


def get_generator_capabilities() -> Dict[str, Any]:
    """Return the stable contract an MCP client needs before a write."""
    return {
        "key_types": {"rsa": [2048, 4096], "ec": [256, 384, 521]},
        "validity_days": {"minimum": 1, "maximum": 825, "default": 365},
        "output_directory": str(DEFAULT_OUTPUT_DIR),
        "notes": [
            "Certificates are self-signed.",
            "Private keys are written only to the server's certs directory.",
            "Use validate_certificate_request before generate_certificate.",
        ],
    }


def _build_params(
    cn: str,
    key_type: str = "rsa",
    key_strength: int = 2048,
    validity_days: int = 365,
    country: str | None = None,
    state: str | None = None,
    locality: str | None = None,
    organization: str | None = None,
) -> CertificateParams:
    """Validate a request and lock MCP output to a controlled directory."""
    if not SAFE_CN.fullmatch(cn):
        raise ValueError(
            "cn must contain only letters, numbers, '*', '.', or '-', and cannot be a path"
        )
    if not 1 <= validity_days <= 825:
        raise ValueError("validity_days must be between 1 and 825")

    return CertificateParams(
        cn=cn, key_type=key_type, key_strength=key_strength,
        validity_days=validity_days, country=country, state=state,
        locality=locality, organization=organization,
        output_dir=str(DEFAULT_OUTPUT_DIR),
    )


def validate_certificate_request(**request: Any) -> Dict[str, Any]:
    """Validate a request without generating a certificate or private key."""
    try:
        params = _build_params(**request)
        validated = asdict(params)
        validated.pop("output_dir", None)
        return {"valid": True, "validated_request": validated, "errors": []}
    except (TypeError, ValueError) as error:
        return {"valid": False, "validated_request": None, "errors": [str(error)]}


def generate_certificate(**request: Any) -> Dict[str, Any]:
    """Generate a certificate after applying MCP-specific safety constraints."""
    validation = validate_certificate_request(**request)
    if not validation["valid"]:
        return {
            "success": False,
            "message": "Certificate request validation failed",
            "error": "; ".join(validation["errors"]),
        }

    result = CertificateGenerator().generate(_build_params(**request))
    return asdict(result)


def create_mcp_server() -> Any:
    """Create the server; importing FastMCP here keeps helpers dependency-free."""
    try:
        from fastmcp import FastMCP
    except ImportError as error:
        raise RuntimeError(
            "Pattern 8 needs the optional FastMCP dependency. Install it with: "
            "py -m pip install -r requirements-mcp.txt"
        ) from error

    mcp = FastMCP(
        "certificate-generator",
        instructions=(
            "Use get_generator_capabilities and validate_certificate_request before "
            "generate_certificate. Generation creates a self-signed certificate and "
            "private key in the server-controlled certs directory."
        ),
    )

    @mcp.tool(
        name="get_generator_capabilities",
        annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    )
    def get_generator_capabilities_tool() -> Dict[str, Any]:
        """Get supported key types, strengths, and safety limits. Read-only."""
        return get_generator_capabilities()

    @mcp.tool(
        name="validate_certificate_request",
        annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    )
    def validate_certificate_request_tool(
        cn: str, key_type: str = "rsa", key_strength: int = 2048,
        validity_days: int = 365, country: str | None = None,
        state: str | None = None, locality: str | None = None,
        organization: str | None = None,
    ) -> Dict[str, Any]:
        """Validate a request before generation. Read-only; creates no files."""
        return validate_certificate_request(
            cn=cn, key_type=key_type, key_strength=key_strength,
            validity_days=validity_days, country=country, state=state,
            locality=locality, organization=organization,
        )

    @mcp.tool(
        name="generate_certificate",
        annotations={"readOnlyHint": False, "destructiveHint": True, "openWorldHint": False},
    )
    def generate_certificate_tool(
        cn: str, key_type: str = "rsa", key_strength: int = 2048,
        validity_days: int = 365, country: str | None = None,
        state: str | None = None, locality: str | None = None,
        organization: str | None = None,
    ) -> Dict[str, Any]:
        """Generate a self-signed certificate and private key in certs/. Writes files."""
        return generate_certificate(
            cn=cn, key_type=key_type, key_strength=key_strength,
            validity_days=validity_days, country=country, state=state,
            locality=locality, organization=organization,
        )

    return mcp


def main() -> None:
    try:
        create_mcp_server().run(transport="stdio")
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
