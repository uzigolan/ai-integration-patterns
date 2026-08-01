# Cert Generator MCP Skill

## When to use this skill

Load this skill when the user says any of:
- "use the MCP", "via MCP", "MCP server", "pattern 8", "pattern_8"
- "generate certificate using MCP", "cert via MCP"
- "pki", "PKI"

## MCP Server: `pattern_8_mcp_server.py`

The MCP server `certificate-generator` exposes **three tools**. Always follow this order:

### Step 1 — `get_generator_capabilities` (optional, read-only)
Returns supported key types, strengths, validity limits, and output directory.
Use this to confirm options before generating.

### Step 2 — `validate_certificate_request` (required before generation)
Validates the request without creating any files.

Parameters:
| Parameter | Required | Values | Default |
|---|---|---|---|
| cn | YES | letters, digits, `-`, `.`, `*` only | — |
| key_type | no | `rsa`, `ec` | `rsa` |
| key_strength | no | RSA: 2048/4096 · EC: 256/384/521 | 2048 |
| validity_days | no | 1–825 | 365 |
| country | no | 2-letter code | — |
| state | no | state/province | — |
| locality | no | city | — |
| organization | no | company name | — |

### Step 3 — `generate_certificate` (writes files)
Generates the self-signed certificate and private key.
Output files are written to the server-controlled `certs/` directory.

Returns:
```json
{
  "success": true,
  "cert_path": "certs/sivan.crt",
  "key_path": "certs/sivan.key"
}
```

## Workflow

1. Call `validate_certificate_request` with the user's parameters.
2. If `valid: true`, call `generate_certificate` with the same parameters.
3. Report `cert_path` and `key_path` to the user.

## Safety rules

- `cn` must NOT be a file path — the server enforces `SAFE_CN` regex.
- `validity_days` is capped at **825** by the server.
- Never call `generate_certificate` if validation returned `valid: false`.
- Output always goes to `certs/` — clients cannot override the output directory.

## Registering the MCP server

Install MCP dependency (once):

```
py -m pip install -r requirements-mcp.txt
```

Register with Codex CLI:

```
codex mcp add certificate-generator -- "$PWD\.venv\Scripts\python.exe" "$PWD\pattern_8_mcp_server.py"
```

Register with Copilot in VS Code (PowerShell CLI):

```
New-Item -ItemType Directory -Force .vscode | Out-Null
@'
{
  "servers": {
    "certificate-generator": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["${workspaceFolder}/pattern_8_mcp_server.py"]
    }
  }
}
'@ | Set-Content -Path .vscode/mcp.json
```

Manual Copilot registration option (`.vscode/mcp.json`):

```
.venv\Scripts\Activate.ps1
python pattern_8_mcp_server.py
```

Then register it in VS Code `.vscode/mcp.json`:

```json
{
  "servers": {
    "certificate-generator": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["${workspaceFolder}/pattern_8_mcp_server.py"]
    }
  }
}
```

Restart your MCP client (Codex or Copilot) after registration so tools are rediscovered.
