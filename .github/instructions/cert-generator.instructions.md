---
description: "Use when: generate certificate, create cert, SSL certificate, TLS cert, self-signed cert, sign certificate, generate key pair, certificate for domain, pattern_2_json_api, use the MCP, via MCP, MCP server, pattern_8, pattern 8, cert via MCP, mcp cert, pki, PKI"
---
# Certificate Generator — How to Use

## MCP Server (Pattern 8) — preferred when MCP tools are available

When the user says "use the MCP", "via MCP", "MCP server", "pattern 8", or "pattern_8",
load and follow the skill at `.github/skills/cert-generator-mcp/SKILL.md`.

The MCP server exposes three tools:
- `get_generator_capabilities` — read-only, returns options
- `validate_certificate_request` — read-only, validates before writing
- `generate_certificate` — writes `certs/<cn>.crt` and `certs/<cn>.key`

Always call `validate_certificate_request` before `generate_certificate`.

To generate a certificate, run this command from `C:\Users\uzi\Downloads\tools` with the venv active:

echo '{"cn":"<domain>"}' | python pattern_2_json_api.py

## Activate venv first (once per terminal session)

.venv\Scripts\Activate.ps1

## Full example with all options

echo '{"cn":"example.com","key_type":"rsa","key_strength":2048,"validity_days":365}' | python pattern_2_json_api.py

## Input fields

| Field | Required | Options | Default |
|---|---|---|---|
| cn | YES | any domain name | — |
| key_type | no | rsa, ec | rsa |
| key_strength | no | RSA: 2048/4096, EC: 256/384/521 | 2048 |
| validity_days | no | any integer | 365 |
| organization | no | company name | — |
| country | no | 2-letter code | — |

## Output

```json
{
  "success": true,
  "cert_path": "example.com.crt",
  "key_path": "example.com.key"
}
```

## Rules

- Always activate `.venv\Scripts\Activate.ps1` before running
- Never edit `cert_generator.py` — use the pattern files only
- For batch certs use: `python pattern_3_config_file.py config.yaml`
- For REST API use: `Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="<domain>"} | ConvertTo-Json) -ContentType "application/json"`
