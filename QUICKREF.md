# Quick Reference: 8 AI Integration Patterns

## One-Page Summary

### Pattern 1: Python Library ⚡
**For:** Python code in same process
from cert_generator import CertificateGenerator, CertificateParams; gen = CertificateGenerator(); result = gen.generate(CertificateParams(cn="example.com"))
**Overhead:** None | **Complexity:** ⭐ | **Best For:** Rapid development

---

### Pattern 2: JSON stdin/stdout 📋
**For:** Language-agnostic CLI tools, LLMs
echo '{"cn":"example.com","key_type":"rsa"}' | python pattern_2_json_api.py
**Overhead:** Low | **Complexity:** ⭐⭐ | **Best For:** CLI integration, LLMs

---

### Pattern 3: Config File 📄
**For:** Batch operations, declarative approach
See config_example.json for format
python pattern_3_config_file.py config.yaml
**Overhead:** Low | **Complexity:** ⭐⭐ | **Best For:** Batch processing, audit trails

---

### Pattern 4: REST API 🌐
**For:** Distributed systems, cloud, multi-client

Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="example.com"; key_type="rsa"} | ConvertTo-Json) -ContentType "application/json"

**Overhead:** Medium | **Complexity:** ⭐⭐⭐ | **Best For:** Scalable services, multiple clients

---

### Pattern 5: Callable Service 🎯
**For:** Python with OOP, dependency injection
service = CertificateService(); result = service(cn="example.com", key_type="rsa"); results = service.batch([...]); corp = service.with_defaults(organization="Corp"); result = corp(cn="api.example.com")
**Overhead:** None | **Complexity:** ⭐ | **Best For:** Modern Python, testing

---

### Pattern 6: Abstract Interface 🏗️
**For:** Multiple implementations, testing, future-proof
provider = CertificateProviderFactory.create("openssl"); manager = CertificateManager(provider); result = manager.create_certificate(cn="example.com")
**Overhead:** None | **Complexity:** ⭐⭐⭐ | **Best For:** Pluggable architecture, testing with mocks

---

### Pattern 7: Event-Driven 📡
**For:** Complex workflows, audit logging, notifications
event_bus = CertificateEventBus(); generator = EventDrivenCertificateGenerator(event_bus); event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, on_done); result = generator.generate(params)
**Overhead:** Low | **Complexity:** ⭐⭐⭐⭐ | **Best For:** Observable systems, audit logging

---

### Pattern 8: MCP Server 🔧
**For:** Codex and other MCP clients that need discoverable, controlled tools
`codex mcp add certificate-generator -- "$PWD\.venv\Scripts\python.exe" "$PWD\pattern_8_mcp_server.py"`
**Overhead:** Medium | **Complexity:** ⭐⭐⭐ | **Best For:** Tool discovery, explicit schemas, safe agent actions

---

## Decision Tree

```
Will AI be in Python?
├─ YES → Use Pattern 1 or 5 (simplest, fastest)
└─ NO  → Continue...

Will Codex or another MCP client call this as a named tool?
├─ YES → Use Pattern 8 (MCP Server)
└─ NO  → Continue...

Do you need distributed/cloud?
├─ YES → Use Pattern 4 (REST API)
└─ NO  → Continue...

Do you need language-agnostic?
├─ YES → Use Pattern 2 (JSON) or Pattern 3 (Config)
└─ NO  → Continue...

Do you need multiple implementations/mocking?
├─ YES → Use Pattern 6 (Abstract Interface)
└─ NO  → Continue...

Do you need audit/logging/notifications?
├─ YES → Use Pattern 7 (Event-Driven)
└─ NO  → Use Pattern 1 or 5
```

---

## Setup on Windows

**Option 1: Use Python launcher (easiest)**
```powershell
py pattern_1_library.py
```

**Option 2: Activate virtual environment**
```powershell
.venv\Scripts\Activate.ps1
python pattern_1_library.py
```

## Pattern Input Types

**Non-interactive (run and exit):**
- Pattern 1, 3, 5, 6, 7

**Interactive/Blocking (with examples):**
- Pattern 2: Requires JSON input (see examples below)
- Pattern 4: REST server (runs indefinitely, press Ctrl+C to stop)

## File Quick Reference

| File | Pattern | Run With |
|------|---------|----------|
| `pattern_1_library.py` | 1 | `py pattern_1_library.py` |
| `pattern_2_json_api.py` | 2 | `echo '{}' \| py pattern_2_json_api.py` |
| `pattern_3_config_file.py` | 3 | `python pattern_3_config_file.py config.json` |
| `pattern_4_rest_api.py` | 4 | `python pattern_4_rest_api.py` + Invoke-RestMethod |
| `pattern_5_callable_service.py` | 5 | `python pattern_5_callable_service.py` |
| `pattern_6_abstract_interface.py` | 6 | `python pattern_6_abstract_interface.py` |
| `pattern_7_event_driven.py` | 7 | `python pattern_7_event_driven.py` |
| `pattern_8_mcp_server.py` | 8 | Register with `codex mcp add` |

---

## Speed Comparison

```
Performance (speed):
1. Library       ████████████████████ Fastest
5. Callable      ████████████████████ Fastest  
6. Abstract      ████████████████████ Fastest
2. JSON          ███████████████░░░░░ Fast
3. Config        ███████████████░░░░░ Fast
7. Event         ███████░░░░░░░░░░░░░ Medium
4. REST          ███████░░░░░░░░░░░░░ Medium (network overhead)
```

---

## Complexity Comparison

```
Easy to implement:
1. Library       ░░░░░░░░░░░░░░░░░░░░ Simplest
2. JSON          ░░░░░░░░░░░░░░░░░░░░ Simple
5. Callable      ░░░░░░░░░░░░░░░░░░░░ Simple
3. Config        ░░░░░░░░░░░░░░░░░░░░ Simple

Medium:
4. REST          ░░░░░░░░░░░░░░░░░░░░ Medium
6. Abstract      ░░░░░░░░░░░░░░░░░░░░ Medium

Hard to implement:
7. Event         ░░░░░░░░░░░░░░░░░░░░ Complex
```

---

## Use Case Matrix

| Use Case | Best Pattern | Why |
|----------|---|---|
| **Prototype** | 1 or 5 | Fast iteration |
| **Testing** | 6 | Mock support |
| **CLI Tool** | 2 | stdin/stdout |
| **LLM Integration** | 2 | JSON text-based |
| **Batch Job** | 3 | Config-driven |
| **Microservice** | 4 | REST standard |
| **Multi-tenant** | 4 | HTTP+scaling |
| **Audit Trail** | 7 | Events capture lifecycle |
| **Notifications** | 7 | Pub/sub pattern |
| **Future-proof** | 6 | Pluggable providers |
| **Performance Critical** | 1 | Lowest overhead |
| **Codex tool integration** | 8 | Native MCP discovery and schemas |

---

## Common Combinations

### Development + Testing
```
Pattern 1 (Library) for development
Pattern 6 (Abstract) with mock provider for testing
```

### Local + Cloud
```
Pattern 1 (Library) locally
Pattern 4 (REST) for cloud delegation
```

### Batch with Audit
```
Pattern 3 (Config) for batch definition
Pattern 7 (Events) for audit logging
```

### Full Stack
```
Pattern 3 (Config) defines batch
Pattern 7 (Events) fires lifecycle events
Events trigger Pattern 4 (REST) notifications
All use Pattern 6 (Abstract) provider
```

---

## Implementation Time

| Pattern | Setup Time | Test Time | Deploy Time |
|---------|-----------|----------|------------|
| 1 | 5 min | 5 min | 1 min |
| 2 | 10 min | 10 min | 2 min |
| 3 | 15 min | 10 min | 2 min |
| 4 | 30 min | 20 min | 10 min |
| 5 | 15 min | 10 min | 2 min |
| 6 | 30 min | 15 min | 5 min |
| 7 | 45 min | 30 min | 10 min |

---

## Error Handling

All patterns return `CertificateOutput`:
```python
@dataclass
class CertificateOutput:
    success: bool           # True/False
    message: str            # Human-readable
    cert_path: str | None   # Where cert is saved
    key_path: str | None    # Where key is saved
    details: dict | None    # Metadata
    error: str | None       # Error details if failed
```

Check `success` field, optionally log `error` field.

---

## JSON Schema Reference

### Input Parameters
```json
{
  "cn": "example.com",              // Required: Common Name
  "key_type": "rsa",                // "rsa" or "ec"
  "key_strength": 2048,             // RSA: 2048/4096, EC: 256/384/521
  "validity_days": 365,             // Certificate valid period
  "country": "US",                  // Optional: Country code
  "state": "California",            // Optional: State/Province
  "locality": "San Francisco",      // Optional: City
  "organization": "My Company",     // Optional
  "output_dir": "./certs"           // Optional: Output directory
}
```

### Output Format
```json
{
  "success": true,
  "message": "Certificate generated successfully",
  "cert_path": "/path/to/cert.crt",
  "key_path": "/path/to/cert.key",
  "details": {
    "cn": "example.com",
    "key_type": "rsa",
    "key_strength": 2048,
    "generated_at": "2024-01-01T12:00:00"
  },
  "error": null
}
```

---

## Common Mistakes

❌ **Don't:**
- Mix AI concerns with implementation details
- Hardcode paths or algorithms in AI code
- Skip error handling for Pattern 2-4 (remote calls)
- Use Pattern 4 for single-process applications
- Ignore scalability when choosing Pattern 1

✅ **Do:**
- Keep AI code focused on business logic
- Use abstraction layers
- Test with mock providers (Pattern 6)
- Version your JSON schemas
- Document interface contracts

---

## Related Documentation

- 📖 **PATTERNS.md** - Detailed guide (start here)
- 🏗️ **DIAGRAMS.md** - Visual architecture
- 📚 **ABSTRACTION_LEVELS.md** - Theory deep dive
- 💡 **README.md** - Overview

---

## Pro Tips

1. **Start simple (Pattern 1), evolve as needed**
   - Don't over-engineer from the start
   - Migrate to Pattern 4 when you need scaling

2. **Use Pattern 6 even for single implementation**
   - Makes testing trivial (mock provider)
   - Future-proof (easy to add providers)
   - Zero performance overhead

3. **Combine patterns strategically**
   - Pattern 3 + 7 = batch with audit
   - Pattern 4 + 6 = scalable with pluggable providers
   - Pattern 1 + 6 = local + testable

4. **Version your interfaces**
   - v1, v2 in REST endpoints
   - Backward compatibility matters

5. **Document error scenarios**
   - What happens if OpenSSL fails?
   - What does the error JSON contain?
   - How should AI handle it?

---

Print this page for quick reference! 🚀
