# 🎯 Quick Commands Reference

## Run All Patterns (Automated Test)

.venv\Scripts\Activate.ps1; python test_all_patterns.py

This runs patterns 1-3 and 5-7 automatically and shows results. Pattern 4 is skipped (it's a server).

---

## Run Individual Patterns

### Pattern 1: Python Library (Exit immediately)

python pattern_1_library.py

**Output:** Success message, exits

---

### Pattern 2: JSON API (Pass JSON input)

**Option A: Pipe JSON**
echo '{"cn":"example.com","key_type":"rsa"}' | python pattern_2_json_api.py

**Option B: JSON as argument**
python pattern_2_json_api.py '{"cn":"example.com"}'

**Option C: No input shows usage**
python pattern_2_json_api.py

**Output:** JSON response with certificate info

---

### Pattern 3: Config File (Exit after processing)

python pattern_3_config_file.py config_example.json

**Output:** Batch summary, exits

---

### Pattern 4: REST API Server (Runs forever - press Ctrl+C to stop)

**Terminal 1: Start server**
python pattern_4_rest_api.py

**Output:** Server runs on http://localhost:5000

**Terminal 2: Call the server**

Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="example.com"} | ConvertTo-Json) -ContentType "application/json"

**With more options:**

$body = @{cn="example.com"; key_type="rsa"; validity_days=730} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body $body -ContentType "application/json"

---

### Pattern 5: Callable Service (Exit immediately)

python pattern_5_callable_service.py

**Output:** Success messages, exits

---

### Pattern 6: Abstract Interface (Exit immediately)

python pattern_6_abstract_interface.py

**Output:** Success and mock examples, exits

---

### Pattern 7: Event-Driven (Exit immediately)

python pattern_7_event_driven.py

**Output:** Event messages, audit log, exits

---

### Pattern 8: MCP Server (Codex + Copilot)

Install MCP dependency:

py -m pip install -r requirements-mcp.txt

Register with Codex CLI:

codex mcp add certificate-generator -- "$PWD\.venv\Scripts\python.exe" "$PWD\pattern_8_mcp_server.py"

Or register with Copilot in VS Code by creating `.vscode/mcp.json`:

CLI option (PowerShell):

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

Restart your MCP client after registration.

**Output:** MCP tools become discoverable: `get_generator_capabilities`, `validate_certificate_request`, `generate_certificate`

---

## Summary: Which Patterns Need Input?

| Pattern | Needs Input? | How to Run |
|---------|---|---|
| 1 | ❌ No | python pattern_1_library.py |
| 2 | ✅ Yes* | Pipe JSON or pass as argument |
| 3 | ❌ No | python pattern_3_config_file.py config.json |
| 4 | 🌐 Server | python pattern_4_rest_api.py (runs forever) |
| 5 | ❌ No | python pattern_5_callable_service.py |
| 6 | ❌ No | python pattern_6_abstract_interface.py |
| 7 | ❌ No | python pattern_7_event_driven.py |
| 8 | 🔧 MCP client setup | Register MCP server, then call discovered tools |

*Pattern 2 now shows usage help if no input provided (doesn't hang!)

---

## Test Everything

python test_all_patterns.py

Should show: 6 passed, 0 failed, 1 skipped

---

## No More Hanging!

✅ Pattern 2 now shows usage instead of hanging
✅ Pattern 4 is clearly marked as a server (runs forever)
✅ All other patterns exit after running
✅ test_all_patterns.py runs everything safely

Note: Pattern 8 is not part of `test_all_patterns.py`; it is validated via MCP client discovery and tool calls.

**Run test_all_patterns.py to verify everything works!**
