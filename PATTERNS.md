# AI Integration Patterns for Code Execution

A comprehensive guide showing 8 different methods for AI to use your code without knowing the implementation details.

---

## Overview

| Pattern | Method | Use Case | Complexity | Language | Perfect For |
|---------|--------|----------|-----------|----------|------------|
| **1** | Python Library | Direct code use | Low | Python | Native Python apps, same process |
| **2** | JSON API | stdin/stdout | Medium | Any | LLMs, CLI tools, shell scripts |
| **3** | Config File | YAML/JSON declaration | Medium | Any | Batch operations, workflows |
| **4** | REST API | HTTP requests | High | Any | Remote systems, cloud, microservices |
| **5** | Callable Service | Object interface | Low | Python | Dependency injection, testing |
| **6** | Abstract Interface | Strategy pattern | Medium | Python | Pluggable architectures, mocking |
| **7** | Event-Driven | Pub/Sub notifications | High | Python | Complex workflows, audit logging |
| **8** | MCP Server | Structured agent tools | Medium | Any MCP client | Codex, controlled actions |

---

## Table of Contents

- [Pattern 1: Python Library Interface](#pattern-1-python-library-interface)
- [Pattern 2: JSON stdin/stdout API](#pattern-2-json-stdinstdout-api)
- [Pattern 3: Configuration File Interface](#pattern-3-configuration-file-interface)
- [Pattern 4: REST API Interface](#pattern-4-rest-api-interface)
- [Pattern 5: Callable Service Object](#pattern-5-callable-service-object)
- [Pattern 6: Abstract Interface / Strategy Pattern](#pattern-6-abstract-interface--strategy-pattern)
- [Pattern 7: Event-Driven / Observer Pattern](#pattern-7-event-driven--observer-pattern)
- [Pattern 8: Model Context Protocol (MCP) Server](#pattern-8-model-context-protocol-mcp-server)
- [Quick Decision Matrix](#quick-decision-matrix)

---

## Pattern 1: Python Library Interface

**What AI Sees:**
```python
from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput

generator = CertificateGenerator()
params = CertificateParams(cn="example.com", key_type="rsa", key_strength=2048)
result: CertificateOutput = generator.generate(params)
```

**Pros:**
- Direct execution, no serialization overhead
- Type hints for IDE support
- Full Python ecosystem access
- Fast and simple

**Cons:**
- Python-only
- Tight coupling
- Must be in same process

**AI Knowledge Required:**
- Python imports
- Function signatures
- Return types

**File:** `pattern_1_library.py`

**AI Execute Command:**
```python
from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput

generator = CertificateGenerator()
params = CertificateParams(cn="example.com", key_type="rsa", key_strength=2048)
result: CertificateOutput = generator.generate(params)
print(result.cert_path, result.key_path)
```

---

## Pattern 2: JSON stdin/stdout API

**What AI Sees:**

**Input (stdin):**
```json
{
  "cn": "example.com",
  "key_type": "rsa",
  "key_strength": 2048,
  "validity_days": 365,
  "organization": "My Company"
}
```

**Output (stdout):**
```json
{
  "success": true,
  "message": "Certificate generated successfully",
  "cert_path": "/path/to/cert.crt",
  "key_path": "/path/to/cert.key",
  "details": {...}
}
```

**Pros:**
- Language-agnostic
- Works with LLMs and text-based tools
- Simple subprocess invocation
- Easy to chain in pipelines

**Cons:**
- Serialization/deserialization overhead
- Process spawn cost
- Separate process memory

**AI Knowledge Required:**
- Input/output JSON schema
- Command invocation
- JSON parsing

**File:** `pattern_2_json_api.py`

**AI Execute Command:**

echo '{"cn":"example.com","key_type":"rsa","validity_days":365}' | python pattern_2_json_api.py

---

## Pattern 3: Configuration File Interface

**What AI Sees:**

**YAML Configuration (config.yaml):**
```yaml
certificates:
  - cn: "api.example.com"
    key_type: "rsa"
    key_strength: 2048
    validity_days: 365
    organization: "My Company"
    
  - cn: "web.example.com"
    key_type: "ec"
    key_strength: 256
    validity_days: 730
```

**Output:**
```json
{
  "success": true,
  "message": "Generated 2 certificates",
  "results": [
    {"cn": "api.example.com", "success": true, "cert_path": "..."},
    {"cn": "web.example.com", "success": true, "cert_path": "..."}
  ]
}
```

**Pros:**
- Declarative (AI describes what, not how)
- Batch processing built-in
- Easy audit trail (config file is documentation)
- No code generation needed

**Cons:**
- Fixed structure (less flexible)
- Requires file I/O
- Schema validation needed

**AI Knowledge Required:**
- YAML/JSON syntax
- Certificate structure
- File paths

**File:** `pattern_3_config_file.py`

**AI Execute Command:**

python pattern_3_config_file.py config_example.json

---

## Pattern 4: REST API Interface

**What AI Sees:**

**HTTP POST:**
```
POST /api/v1/certificate
Content-Type: application/json

{
  "cn": "example.com",
  "key_type": "rsa",
  "key_strength": 2048,
  "validity_days": 365
}
```

**HTTP Response (200):**
```json
{
  "success": true,
  "message": "Certificate generated successfully for example.com",
  "cert_path": "/certs/example.com.crt",
  "key_path": "/certs/example.com.key"
}
```

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/certificate` - Generate single certificate
- `POST /api/v1/certificate/batch` - Generate multiple

**Pros:**
- Standard HTTP protocol
- Easy to scale (distribute load)
- Works across networks/clouds
- Language-agnostic
- Standard API documentation (OpenAPI/Swagger)

**Cons:**
- Most overhead (serialization + HTTP)
- Network latency
- Requires server running

**AI Knowledge Required:**
- HTTP methods and status codes
- REST API concepts
- JSON payloads
- Error handling

**File:** `pattern_4_rest_api.py`

**AI Execute Command:**

Step 1 — start the server (Terminal 1):

python pattern_4_rest_api.py

Step 2 — call it (Terminal 2):

Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="example.com"; key_type="rsa"} | ConvertTo-Json) -ContentType "application/json"

---

## Pattern 5: Callable Service Object

**What AI Sees:**

```python
from pattern_5_callable_service import CertificateService

# Create service
cert_service = CertificateService()

# Call like function
result = cert_service(
    cn="example.com",
    key_type="rsa",
    key_strength=2048
)

# Batch operations
results = cert_service.batch([
    {"cn": "api.example.com"},
    {"cn": "web.example.com"}
])

# Create specialized variants
company_certs = cert_service.with_defaults(
    organization="My Company",
    country="US"
)
result = company_certs(cn="api.example.com")
```

**Pros:**
- Pythonic and intuitive
- Support for defaults and specialization
- Works with dependency injection
- Easy to test and mock
- Clean OOP design

**Cons:**
- Python-only
- Requires understanding of objects
- State management

**AI Knowledge Required:**
- Python objects and methods
- Function call syntax
- Default parameters

**File:** `pattern_5_callable_service.py`

**AI Execute Command:**
```python
from pattern_5_callable_service import CertificateService

service = CertificateService()
result = service(cn="example.com", key_type="rsa")
print(result.cert_path, result.key_path)
```

---

## Pattern 6: Abstract Interface / Strategy Pattern

**What AI Sees:**

```python
from pattern_6_abstract_interface import (
    CertificateProviderFactory,
    ICertificateProvider,
    CertificateManager
)

# Get provider from factory
provider = CertificateProviderFactory.create("openssl")

# Create manager
manager = CertificateManager(provider)

# Use manager (implementation is hidden)
result = manager.create_certificate(
    cn="example.com",
    key_type="rsa"
)

# Get capabilities
capabilities = manager.get_capabilities()
# Returns: {"rsa": [2048, 4096], "ec": [256, 384, 521]}
```

**Pros:**
- Complete decoupling from implementation
- Easy to switch implementations (openssl → other)
- Perfect for mocking in tests
- Supports multiple algorithms/providers
- Future-proof (add new implementations without changing AI code)

**Cons:**
- More boilerplate code
- Extra indirection
- Requires understanding of patterns

**AI Knowledge Required:**
- Factory pattern
- Interface contracts
- Manager classes

**File:** `pattern_6_abstract_interface.py`

**AI Execute Command:**
```python
from pattern_6_abstract_interface import CertificateProviderFactory, CertificateManager

provider = CertificateProviderFactory.create("openssl")
manager = CertificateManager(provider)
result = manager.create_certificate(cn="example.com", key_type="rsa")
print(result.cert_path, result.key_path)
```

**Testing Example:**
```python
# Real implementation
real_provider = CertificateProviderFactory.create("openssl")
manager = CertificateManager(real_provider)

# Mock implementation (for testing)
mock_provider = CertificateProviderFactory.create("mock")
test_manager = CertificateManager(mock_provider)

# AI code is identical!
result = test_manager.create_certificate(cn="test.com")
```

---

## Pattern 7: Event-Driven / Observer Pattern

**What AI Sees:**

```python
from pattern_7_event_driven import (
    CertificateEventBus,
    EventDrivenCertificateGenerator,
    CertificateEventType
)

# Create event bus and generator
event_bus = CertificateEventBus()
generator = EventDrivenCertificateGenerator(event_bus)

# Define event handlers
def on_generation_start(event):
    print(f"Starting: {event.cn}")

def on_generation_complete(event):
    print(f"Done: {event.data['cert_path']}")

def on_error(event):
    print(f"Error: {event.error}")

# Subscribe to events
event_bus.subscribe(CertificateEventType.GENERATION_START, on_generation_start)
event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, on_generation_complete)
event_bus.subscribe(CertificateEventType.GENERATION_FAILED, on_error)

# Use generator - events fire automatically
result = generator.generate(params)
```

**Events Available:**
- `VALIDATION_START` - Validation starting
- `VALIDATION_COMPLETE` - Validation passed
- `VALIDATION_FAILED` - Validation failed
- `GENERATION_START` - Generation starting
- `GENERATION_COMPLETE` - Certificate created
- `GENERATION_FAILED` - Generation error

**Pros:**
- Decouples generation from side effects
- Multiple subscribers per event
- Easy audit logging
- Supports notifications (email, Slack, metrics)
- Complex workflows with dependencies

**Cons:**
- Most complex pattern
- Debugging can be harder (events are async)
- Requires understanding of pub/sub

**AI Knowledge Required:**
- Event-driven architecture
- Handler/callback functions
- Event types and lifecycle

**File:** `pattern_7_event_driven.py`

**AI Execute Command:**
```python
from pattern_7_event_driven import CertificateEventBus, EventDrivenCertificateGenerator, CertificateEventType
from cert_generator import CertificateParams

event_bus = CertificateEventBus()
generator = EventDrivenCertificateGenerator(event_bus)

event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, lambda e: print("Done:", e.data.get("cert_path")))
event_bus.subscribe(CertificateEventType.GENERATION_FAILED, lambda e: print("Error:", e.error))

params = CertificateParams(cn="example.com")
result = generator.generate(params)
```

**Example: Audit Logging**
```python
def audit_log(event):
    if event.event_type == CertificateEventType.GENERATION_COMPLETE:
        with open("audit.log", "a") as f:
            f.write(f"Certificate created: {event.cn}\n")

event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, audit_log)
```

---

## Pattern 8: Model Context Protocol (MCP) Server

**What Codex and Copilot see:** named tools with explicit input schemas instead of Python imports, shell commands, or REST details.

- `get_generator_capabilities` — read supported key types and safety limits
- `validate_certificate_request` — validate without creating files
- `generate_certificate` — create a self-signed certificate and private key

The MCP server exposes a controlled action boundary: it rejects path-like common names and writes output only under `certs/`.

**Install/enable the local skill (Pattern 8 assistant behavior):**

This repository includes a local skill and instruction wiring for Pattern 8:
- `.github/skills/cert-generator-mcp/SKILL.md`
- `.github/instructions/cert-generator.instructions.md`
- `.github/agents/cert-generator.agent.md`

No package install command is needed for the skill itself. To activate updates after cloning or editing these files:

1. Open the repository as your workspace root.
2. Restart the chat host so customizations reload (Reload Window in VS Code is the simplest path).
3. Use a trigger phrase in chat such as: `use the MCP`, `pattern 8`, `cert via MCP`, or `pki`.

The trigger words route certificate requests through the Pattern 8 MCP workflow (validate first, then generate).

**Install the optional dependency:**

```powershell
py -m pip install -r requirements-mcp.txt
```

**Register the stdio server with Codex CLI:**

```powershell
codex mcp add certificate-generator -- "$PWD\.venv\Scripts\python.exe" "$PWD\pattern_8_mcp_server.py"
```

**Register the stdio server with Copilot in VS Code:**

Create `.vscode/mcp.json` in the workspace:

Or run this CLI command in PowerShell to create it automatically:

```powershell
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

Restart your MCP client after registration. It can then discover the tools and use the sequence: capabilities -> validate -> generate.

**Pros:** native MCP tool discovery in Codex and Copilot, structured results, explicit read/write boundary, and a stable contract even if the implementation changes.

**Cons:** requires MCP client configuration; production remote deployment still needs authentication and authorization.

**File:** `pattern_8_mcp_server.py`

---

## Quick Decision Matrix

### Choose Pattern 1 if:
- ✅ AI code is Python
- ✅ Running in same process
- ✅ Speed is critical
- ✅ Simple integration

### Choose Pattern 2 if:
- ✅ AI is a shell script or CLI tool
- ✅ Need to pass data through pipes
- ✅ Language-agnostic solution
- ✅ Working with LLMs (text-based)

### Choose Pattern 3 if:
- ✅ Batch operations
- ✅ Configuration-driven approach
- ✅ Need audit trail (config file)
- ✅ Simple, declarative style

### Choose Pattern 4 if:
- ✅ Remote systems need to call code
- ✅ Running in cloud/microservices
- ✅ Multiple clients accessing service
- ✅ Need standard REST API docs

### Choose Pattern 5 if:
- ✅ Python with OOP patterns
- ✅ Need dependency injection
- ✅ Want clean Pythonic interface
- ✅ Testing/mocking needed

### Choose Pattern 6 if:
- ✅ Multiple implementations possible
- ✅ Future algorithm changes expected
- ✅ Need mock implementations for testing
- ✅ Pluggable architecture

### Choose Pattern 7 if:
- ✅ Complex workflows with side effects
- ✅ Need audit logging/notifications
- ✅ Multiple systems react to events
- ✅ Decoupled architecture required

### Choose Pattern 8 if:
- ✅ Codex or another MCP client should discover and call your capability as a tool
- ✅ You need explicit input schemas and read/write boundaries
- ✅ The implementation should remain behind a controlled server process

---

## Example: Complete AI Workflow

Here's how an AI system might use these patterns in sequence:

```python
# 1. Validate what we can do
from pattern_6_abstract_interface import CertificateProviderFactory

provider = CertificateProviderFactory.create("openssl")
capabilities = provider.get_supported_key_types()
# AI now knows: what key types are supported

# 2. Declare batch operations
from pattern_3_config_file import generate_from_config_file

config = {
    "certificates": [
        {"cn": "api.example.com", "key_type": "rsa"},
        {"cn": "web.example.com", "key_type": "rsa"}
    ]
}
# AI can generate configuration without implementation knowledge

# 3. Add observability
from pattern_7_event_driven import CertificateEventBus, EventDrivenCertificateGenerator

event_bus = CertificateEventBus()
generator = EventDrivenCertificateGenerator(event_bus)

def send_slack_notification(event):
    if event.event_type == CertificateEventType.GENERATION_COMPLETE:
        # send_slack(f"Certificate ready: {event.cn}")
        pass

event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, send_slack_notification)

# 4. Execute
results = generator.generate(params)
# Events fire, notifications sent, audit logged
```

---

## Implementation Checklist

- [x] **Pattern 1** - Direct Python library
- [x] **Pattern 2** - JSON stdin/stdout
- [x] **Pattern 3** - Config file (YAML/JSON)
- [x] **Pattern 4** - REST API (Flask)
- [x] **Pattern 5** - Callable service object
- [x] **Pattern 6** - Abstract interface/strategy
- [x] **Pattern 7** - Event-driven/observer
- [x] **Pattern 8** - MCP server for Codex and other MCP clients

---

## Files Reference

| File | Pattern | Purpose |
|------|---------|---------|
| `cert_generator.py` | Core | Base implementation |
| `pattern_1_library.py` | 1 | Python library usage |
| `pattern_2_json_api.py` | 2 | JSON stdin/stdout |
| `pattern_3_config_file.py` | 3 | Config file processing |
| `pattern_4_rest_api.py` | 4 | REST API server |
| `pattern_5_callable_service.py` | 5 | Callable objects |
| `pattern_6_abstract_interface.py` | 6 | Abstract interface |
| `pattern_7_event_driven.py` | 7 | Event-driven |
| `pattern_8_mcp_server.py` | 8 | MCP server |
| `requirements-mcp.txt` | 8 | Optional MCP dependency |
| `PATTERNS.md` | Guide | This file |

---

## Testing All Patterns

**Windows:** Use `py` launcher
```powershell
# Pattern 1: Python library
py pattern_1_library.py

# Pattern 2: JSON API
echo '{"cn":"test.com","key_type":"rsa"}' | python pattern_2_json_api.py

# Pattern 3: Config file
python pattern_3_config_file.py config.yaml

# Pattern 4: REST API (in terminal 1)
python pattern_4_rest_api.py

# Pattern 4: REST API (in terminal 2 - call it)
Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="example.com"} | ConvertTo-Json) -ContentType "application/json"

# Pattern 5: Callable service
python pattern_5_callable_service.py

# Pattern 6: Abstract interface
python pattern_6_abstract_interface.py

# Pattern 7: Event-driven
python pattern_7_event_driven.py

---

## Key Insight

**AI doesn't need to know the implementation.**

Each pattern shows a different **abstraction boundary** where:
- AI only knows what goes in and what comes out
- AI never needs to understand OpenSSL commands, subprocess handling, or file operations
- Implementations can change, algorithms can improve, but AI code remains unchanged

This is the power of proper abstraction for AI integration.
