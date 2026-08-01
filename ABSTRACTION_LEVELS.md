# AI Code Execution: Abstraction Levels

## The Problem

AI systems need to execute your custom code, but:
- ❌ AI can't memorize implementation details
- ❌ AI can't reliably debug low-level operations
- ❌ Implementation changes break AI prompts
- ❌ You want AI to use code as "black box"

## The Solution: Abstraction Layers

Create clear boundaries where AI only knows **inputs** and **outputs**.

---

## Level 0: The Raw Problem

**What OpenSSL looks like to AI:**
```bash
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout server.key -out server.crt \
  -days 365 -subj "/C=US/ST=CA/L=SF/O=Corp/CN=example.com"
```

**AI's Challenge:**
- Too many flags and arguments
- Easy to make mistakes
- Implementation-dependent
- Hard to validate parameters
- Difficult to handle errors
- No way to control output location

---

## Level 1: Function Interface (Pattern 1)

```python
# AI sees this interface:
class CertificateGenerator:
    def generate(params: CertificateParams) -> CertificateOutput
```

**What AI knows:**
- ✅ Input: CertificateParams object with typed fields
- ✅ Output: CertificateOutput with success/failure info
- ❌ Implementation details (hidden)

**Example:**
```python
params = CertificateParams(
    cn="example.com",
    key_type="rsa",
    key_strength=2048
)
result = generator.generate(params)
```

**Abstraction Stack:**
```
AI Layer
   ↓ (calls)
CertificateGenerator.generate()
   ↓ (calls)
CertificateParams (validation)
   ↓ (calls)
subprocess.run(["openssl", ...])
   ↓ (executes)
OpenSSL (black box)
```

---

## Level 2: Data Format Interface (Pattern 2)

```json
{
  "cn": "example.com",
  "key_type": "rsa",
  "key_strength": 2048
}
    ↓
    (process boundary)
    ↓
{
  "success": true,
  "cert_path": "/path/to/cert.crt",
  "key_path": "/path/to/cert.key"
}
```

**What AI knows:**
- ✅ JSON input schema
- ✅ JSON output schema
- ✅ How to invoke (stdin/stdout)
- ❌ Language of implementation
- ❌ Internal logic

**Abstraction Stack:**
```
AI System
   ↓ (writes JSON to stdin)
Process: pattern_2_json_api.py
   ↓ (deserializes JSON)
Python code
   ↓ (calls)
CertificateGenerator
   ↓ (calls)
OpenSSL
```

---

## Level 3: Configuration Interface (Pattern 3)

```yaml
certificates:
  - cn: "api.example.com"
    key_type: "rsa"
    key_strength: 2048
```

**What AI knows:**
- ✅ Configuration format (YAML/JSON)
- ✅ Certificate schema
- ❌ How generator works
- ❌ File paths internals
- ❌ Batch processing details

**Abstraction Stack:**
```
AI System
   ↓ (generates)
YAML Config File
   ↓ (reads)
pattern_3_config_file.py
   ↓ (parses)
Certificate list
   ↓ (iterates)
CertificateGenerator for each
   ↓ (aggregates results)
Output summary
```

---

## Level 4: API Interface (Pattern 4)

```
AI System (Python, JavaScript, Go, etc.)
   ↓ (HTTP POST)
REST Server
   ↓ (route /api/v1/certificate)
Request Handler
   ↓ (validates)
CertificateGenerator
   ↓ (generates)
HTTP Response (JSON)
   ↓
AI System receives result
```

**What AI knows:**
- ✅ HTTP methods (POST, GET)
- ✅ Request/response format
- ✅ Endpoint paths
- ✅ Status codes
- ❌ Server implementation
- ❌ Threading/concurrency
- ❌ Database logic (if any)

**Multi-Language Capability:**
```
Python AI ──→ \
JavaScript AI ──→ REST Server ──→ Python Generator ──→ OpenSSL
Java AI ─────→ /
```

---

## Level 5: Object Interface (Pattern 5)

```python
# AI pattern
service = CertificateService()
result = service(cn="example.com", key_type="rsa")

# Creates specialized variants
company_service = service.with_defaults(organization="Corp")
result = company_service(cn="api.example.com")
```

**What AI knows:**
- ✅ Service is callable
- ✅ Parameter names (keyword args)
- ✅ Return type
- ✅ Can create variants
- ❌ Internal implementation
- ❌ How defaults work

---

## Level 6: Abstract Interface (Pattern 6)

```python
# AI only knows this interface
provider: ICertificateProvider = factory.create("openssl")
manager = CertificateManager(provider)
result = manager.create_certificate(cn="example.com")
```

**What AI knows:**
- ✅ Factory pattern
- ✅ ICertificateProvider contract
- ✅ Methods available
- ❌ Which implementation (could be OpenSSL, AWS ACM, Vault, etc.)
- ❌ Internal logic

**Future-Proof:**
```
# Today: OpenSSL
provider = factory.create("openssl")

# Tomorrow: AWS
provider = factory.create("aws")

# Day after: HashiCorp Vault
provider = factory.create("vault")

# AI code unchanged!
result = manager.create_certificate(cn="example.com")
```

---

## Level 7: Event Interface (Pattern 7)

```python
# AI subscribes to lifecycle
event_bus.subscribe(
    CertificateEventType.GENERATION_COMPLETE,
    on_certificate_ready
)

generator = EventDrivenCertificateGenerator(event_bus)
result = generator.generate(params)
# Events fire → handlers execute
# AI reacts to events, not imperative code
```

**What AI knows:**
- ✅ Event types
- ✅ Event data structure
- ✅ How to register handlers
- ❌ Generation algorithm
- ❌ When events fire
- ❌ Event ordering

**Abstraction Stack:**
```
AI: Define handlers
   ↓
Event Bus: Registry
   ↓
Generator: Publishes events
   ↓
Handlers: React to lifecycle
   ↓
Side effects (logging, notifications, etc.)
```

---

## Comparison: AI Knowledge Required

| Pattern | AI Must Know | AI Never Needs To Know |
|---------|-------------|------------------------|
| **1. Library** | Python, imports, function calls | OpenSSL, subprocess, file I/O |
| **2. JSON API** | JSON format, stdin/stdout | Python, implementation language |
| **3. Config** | YAML/JSON, config schema | Generator internals, algorithms |
| **4. REST** | HTTP, endpoints, status codes | Server details, backend language |
| **5. Callable** | Object methods, kwargs, defaults | Implementation, state management |
| **6. Abstract** | Factory, interface contracts | Algorithm choice, provider details |
| **7. Event** | Event types, handlers, callbacks | Generation logic, concurrency |

---

## Decision Tree: Which Pattern to Use?

```
Start: "I want AI to use my certificate generator"
│
├─ Is AI in Python? ──Y──→ [Library interface OK?]
│                          ├─ Yes → Use Pattern 1 (simplest)
│                          └─ No  → Continue
│
├─ Do you want language-agnostic? ──Y──→ Use Pattern 2 (JSON API)
│
├─ Do you need to scale to many users? ──Y──→ Use Pattern 4 (REST)
│
├─ Will you support multiple algorithms/providers? ──Y──→ Use Pattern 6 (Abstract)
│
├─ Do you need audit/logging/notifications? ──Y──→ Use Pattern 7 (Event-Driven)
│
├─ Batch processing? Simple config-driven? ──Y──→ Use Pattern 3 (Config)
│
└─ Need clean OOP with defaults? ──Y──→ Use Pattern 5 (Callable Service)
```

---

## Stacking Patterns

You don't have to pick just one! Common combinations:

### Stack 1: Development vs Production
```python
# Development: Use mock provider for fast testing
dev_manager = CertificateManager(CertificateProviderFactory.create("mock"))

# Production: Use real OpenSSL
prod_manager = CertificateManager(CertificateProviderFactory.create("openssl"))

# AI code is identical!
# (Pattern 6 abstraction makes this possible)
```

### Stack 2: Local + Remote
```
Local AI
  ├─ Pattern 5 (Callable) for quick operations
  └─ Pattern 4 (REST) for delegating to cloud service
    └─ Remote server uses Pattern 2 (JSON) internally
```

### Stack 3: Batch with Events
```
Config File (Pattern 3)
  ├─ Defines certificates to generate
  └─ Passed to Event-Driven Generator (Pattern 7)
    ├─ Publishes GENERATION_START events
    ├─ Publishes GENERATION_COMPLETE events
    └─ AI handlers log, notify, validate results
```

---

## Key Principle

> **AI should use your code through abstraction layers where it only knows**:
> - What type of inputs it can provide
> - What type of outputs it will receive
> - What to do if something fails
>
> **AI should NOT know**:
> - How inputs are processed
> - What algorithms run
> - How outputs are generated
> - Implementation language or technology

This keeps AI code stable even when you optimize, refactor, or completely replace internals.

---

## Real-World Example

### Scenario
You have an AI system that needs to generate SSL certificates, but you want flexibility.

### Phase 1: Development
```python
# Pattern 1: Direct library (fast iteration)
from cert_generator import CertificateGenerator
gen = CertificateGenerator()
result = gen.generate(params)
```

### Phase 2: Testing
```python
# Pattern 6: Abstract interface (testable)
mock_provider = factory.create("mock")
manager = CertificateManager(mock_provider)
result = manager.create_certificate(cn="test.com")  # No actual cert generation
```

### Phase 3: Multiple Clients
```python
# Pattern 4: REST API (scalable)
# AI code:
response = requests.post("https://cert-service.example.com/api/v1/certificate", ...)
result = response.json()
```

### Phase 4: Compliance/Audit
```python
# Pattern 7: Event-driven (observable)
# Add handlers for audit logging, compliance reporting
event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, audit_log)
```

### Phase 5: Batch Operations
```python
# Pattern 3: Config file (declarative)
# AI generates certificate.yaml, calls batch generator
result = generate_from_config_file("certificates.yaml")
```

**All phases use different patterns, but AI only needs to adapt its invocation - not its logic.**

---

## Summary

| Phase | Pattern | Reason |
|-------|---------|--------|
| Prototype | 1 | Fast |
| Test | 6 | Mockable |
| Scale | 4 | Distributed |
| Audit | 7 | Observable |
| Batch | 3 | Declarative |

This is the power of abstraction for AI integration.
