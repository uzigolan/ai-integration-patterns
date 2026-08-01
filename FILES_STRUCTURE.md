# Complete File Structure & Contents

## 📦 What's Included

This toolkit contains a complete working example demonstrating how to expose your custom code to AI systems through different architectural patterns.

---

## 🎯 Core Implementation

### `cert_generator.py` (600+ lines)
**Purpose:** Self-signed certificate generator wrapping OpenSSL

**What it does:**
- Accepts parameters: CN, key type, key strength, validity period
- Validates all inputs (raises ValueError for invalid params)
- Executes OpenSSL via subprocess
- Returns structured output (CertificateOutput)

**Key Classes:**
- `CertificateParams` - Input dataclass with validation
- `CertificateGenerator` - Core implementation
- `CertificateOutput` - Output dataclass

**How to use it:**
```python
from cert_generator import CertificateGenerator, CertificateParams

gen = CertificateGenerator()
params = CertificateParams(cn="example.com", key_type="rsa", key_strength=2048)
result = gen.generate(params)
print(f"Success: {result.success}, Cert: {result.cert_path}")
```

**Run it:**
```bash
python cert_generator.py --cn example.com --key-type rsa --key-strength 2048
```

---

## 🏗️ 8 Integration Patterns

### `pattern_1_library.py` (30 lines)
**Pattern:** Python Library Interface
**Difficulty:** ⭐ Easy
**When to use:** Python code in same process, direct integration

**Example:**
```python
from cert_generator import CertificateGenerator, CertificateParams
gen = CertificateGenerator()
result = gen.generate(CertificateParams(cn="example.com"))
```

**Pros:** Fastest, simplest, direct access
**Cons:** Python-only, tight coupling

---

### `pattern_2_json_api.py` (120 lines)
**Pattern:** JSON stdin/stdout Interface
**Difficulty:** ⭐⭐ Medium
**When to use:** CLI tools, LLMs, language-agnostic solutions

**Example:**
```bash
echo '{"cn":"example.com","key_type":"rsa"}' | python pattern_2_json_api.py
```

**Input Format:**
```json
{
  "cn": "example.com",
  "key_type": "rsa",
  "key_strength": 2048,
  "validity_days": 365
}
```

**Output Format:**
```json
{
  "success": true,
  "message": "Certificate generated successfully",
  "cert_path": "/path/to/cert.crt",
  "key_path": "/path/to/cert.key"
}
```

**Pros:** Language-agnostic, works with LLMs, simple pipes
**Cons:** Serialization overhead, process per call

---

### `pattern_3_config_file.py` (140 lines)
**Pattern:** Configuration File Interface (YAML/JSON)
**Difficulty:** ⭐⭐ Medium
**When to use:** Batch operations, declarative approach, audit trails

**Example:**
```bash
python pattern_3_config_file.py config.yaml
```

**Config Format (YAML or JSON):**
```yaml
certificates:
  - cn: "api.example.com"
    key_type: "rsa"
    key_strength: 2048
    validity_days: 365
    organization: "My Company"
```

**Output:**
```json
{
  "success": true,
  "message": "Generated 3 certificates",
  "details": {
    "total": 3,
    "successful": 3,
    "results": [...]
  }
}
```

**Pros:** Batch processing, declarative, audit trail (config is documentation)
**Cons:** Less flexible (fixed structure), requires file I/O

---

### `pattern_4_rest_api.py` (200 lines)
**Pattern:** REST API Interface (Flask)
**Difficulty:** ⭐⭐⭐ Hard
**When to use:** Distributed systems, cloud, multiple clients

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/certificate` - Generate single certificate
- `POST /api/v1/certificate/batch` - Generate batch

**Example:**
# Start server
python pattern_4_rest_api.py

# In another terminal
Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="example.com"; key_type="rsa"} | ConvertTo-Json) -ContentType "application/json"
```

**Request:**
```json
{
  "cn": "example.com",
  "key_type": "rsa",
  "key_strength": 2048
}
```

**Response:**
```json
{
  "success": true,
  "message": "Certificate generated successfully",
  "cert_path": "/certs/example.com.crt",
  "key_path": "/certs/example.com.key"
}
```

**Pros:** Scalable, distributed, standard REST, language-agnostic
**Cons:** Most overhead (serialization + HTTP), network latency

---

### `pattern_5_callable_service.py` (100 lines)
**Pattern:** Callable Object Interface
**Difficulty:** ⭐ Easy
**When to use:** Python with OOP, dependency injection, testing

**Example:**
```python
from pattern_5_callable_service import CertificateService

service = CertificateService()

# Simple call
result = service(cn="example.com", key_type="rsa")

# Batch
results = service.batch([
    {"cn": "api.example.com"},
    {"cn": "web.example.com"}
])

# With defaults
company_certs = service.with_defaults(organization="Corp")
result = company_certs(cn="api.example.com")
```

**Pros:** Pythonic, intuitive, supports defaults, testable
**Cons:** Python-only, OOP knowledge required

---

### `pattern_6_abstract_interface.py` (200 lines)
**Pattern:** Abstract Interface / Strategy Pattern
**Difficulty:** ⭐⭐⭐ Hard
**When to use:** Multiple implementations, testing with mocks, future-proof code

**Key Classes:**
- `ICertificateProvider` - Abstract interface
- `OpenSSLCertificateProvider` - OpenSSL implementation
- `MockCertificateProvider` - Mock for testing
- `CertificateProviderFactory` - Factory pattern
- `CertificateManager` - Uses provider interface

**Example:**
```python
from pattern_6_abstract_interface import CertificateProviderFactory, CertificateManager

# Real implementation
provider = CertificateProviderFactory.create("openssl")
manager = CertificateManager(provider)
result = manager.create_certificate(cn="example.com")

# Mock for testing (AI code identical!)
mock_provider = CertificateProviderFactory.create("mock")
test_manager = CertificateManager(mock_provider)
result = test_manager.create_certificate(cn="test.com")
```

**Future Extension:**
```python
# Add AWS provider
class AwsAcmProvider(ICertificateProvider):
    def create(self, **kwargs): ...

# Register it
CertificateProviderFactory.register("aws", AwsAcmProvider)

# Use it (AI code unchanged!)
provider = CertificateProviderFactory.create("aws")
```

**Pros:** Pluggable, testable, future-proof, zero overhead
**Cons:** More boilerplate, pattern complexity

---

### `pattern_7_event_driven.py` (220 lines)
**Pattern:** Event-Driven / Observer Pattern
**Difficulty:** ⭐⭐⭐⭐ Very Hard
**When to use:** Complex workflows, audit logging, notifications

**Events:**
- `VALIDATION_START` - Validation starting
- `VALIDATION_COMPLETE` - Validation passed
- `VALIDATION_FAILED` - Validation failed
- `GENERATION_START` - Generation starting
- `GENERATION_COMPLETE` - Certificate created
- `GENERATION_FAILED` - Generation error

**Example:**
```python
from pattern_7_event_driven import (
    CertificateEventBus,
    EventDrivenCertificateGenerator,
    CertificateEventType
)

event_bus = CertificateEventBus()
generator = EventDrivenCertificateGenerator(event_bus)

# Subscribe to events
def on_complete(event):
    print(f"Certificate ready: {event.data['cert_path']}")

def on_error(event):
    print(f"Error: {event.error}")

event_bus.subscribe(CertificateEventType.GENERATION_COMPLETE, on_complete)
event_bus.subscribe(CertificateEventType.GENERATION_FAILED, on_error)

# Use generator
result = generator.generate(params)
# Events fire automatically → handlers execute
```

**Pros:** Observable, audit-logged, decoupled, handles side effects
**Cons:** Most complex, debugging harder, event ordering matters

---

### `pattern_8_mcp_server.py`
**Pattern:** Model Context Protocol (MCP) Server
**Difficulty:** ⭐⭐⭐ Medium
**When to use:** Codex or another MCP client needs discoverable, controlled tools

**Tools:**
- `get_generator_capabilities` (read-only)
- `validate_certificate_request` (read-only)
- `generate_certificate` (writes certificate and key files)

**Safety:** Requests are validated, common names cannot be file paths, and output is restricted to `certs/`.

**Install and register:**
```powershell
py -m pip install -r requirements-mcp.txt
codex mcp add certificate-generator -- "$PWD\.venv\Scripts\python.exe" "$PWD\pattern_8_mcp_server.py"
```

**Pros:** Native Codex tools, explicit schemas, controlled action boundary
**Cons:** Requires MCP dependency and client configuration

---

## 📚 Documentation

### `README.md` (400+ lines)
**What:** Complete overview and getting started guide

**Includes:**
- Toolkit overview
- What's included (file listing)
- Quick start for each pattern
- Comparison table
- How to use the toolkit
- Real-world examples
- FAQ
- Learning path

---

### `PATTERNS.md` (500+ lines)
**What:** Comprehensive guide to all 8 patterns

**Includes:**
- Detailed explanation of each pattern
- Pros/cons for every pattern
- What AI sees with each pattern
- Decision matrix
- Implementation checklist
- Testing instructions
- Complete workflow example

**Best for:** Understanding each pattern in depth

---

### `ABSTRACTION_LEVELS.md` (400+ lines)
**What:** Theory and architecture depth

**Includes:**
- The problem (why abstraction matters)
- Abstraction layers explanation
- Level 0-7 breakdown
- Knowledge comparison table
- Decision tree
- Stacking patterns
- Real-world phase migration
- Key principles

**Best for:** Understanding why abstraction matters

---

### `DIAGRAMS.md` (300+ lines)
**What:** ASCII diagrams for each pattern

**Includes:**
- Data flow diagrams
- Architecture stack visuals
- Process flow charts
- Real-world multi-pattern stack
- Comparison diagrams

**Best for:** Visual learners

---

### `QUICKREF.md` (250+ lines)
**What:** One-page quick reference

**Includes:**
- All 8 patterns summarized
- Decision tree
- File reference table
- Speed/complexity comparison
- Use case matrix
- Common combinations
- JSON schema reference
- Pro tips

**Best for:** Printing, quick lookup

---

## 📝 Configuration Examples

### `config_example.json` (30 lines)
**Purpose:** Example configuration file for Pattern 3

**Contains:**
- Multiple certificate definitions
- Different key types (RSA, EC)
- Various settings (key strength, validity)
- Shows proper JSON structure

**How to use:**
```bash
python pattern_3_config_file.py config_example.json
```

---

## 🎓 Learning Path

### Step 1: Understand the Problem
Read: `ABSTRACTION_LEVELS.md` (Level 0-1)

### Step 2: See Simple Example
Run: `python pattern_1_library.py`
Read: `PATTERNS.md` (Pattern 1)

### Step 3: Explore Each Pattern
For each pattern (1-7):
1. Read the section in `PATTERNS.md`
2. Review the code file
3. Try running it
4. Look at `DIAGRAMS.md`

### Step 4: Understand Theory
Read: Full `ABSTRACTION_LEVELS.md`
Review: `QUICKREF.md` comparison tables

### Step 5: Plan Your Implementation
Use: Decision tree in `QUICKREF.md`
Reference: Use case matrix
Plan: Combination of patterns

---

## 🔧 How to Adapt for Your Code

1. **Replace `cert_generator.py`** with your implementation
2. **Keep the same interface** (input/output structure)
3. **All patterns work with your code!**

Example:
```python
# Your code
class MyCodeGenerator:
    def process(self, params):
        # your logic
        return output

# Pattern 1 still works
from my_code import MyCodeGenerator
gen = MyCodeGenerator()
result = gen.process(params)

# Pattern 6 still works
provider = factory.create("mycode")
manager = Manager(provider)
result = manager.create(cn=...)

# All other patterns work too!
```

---

## 📊 File Statistics

| File | Lines | Purpose | Complexity |
|------|-------|---------|-----------|
| cert_generator.py | 600+ | Core implementation | ⭐⭐ |
| pattern_1_library.py | 30 | Python library | ⭐ |
| pattern_2_json_api.py | 120 | JSON interface | ⭐⭐ |
| pattern_3_config_file.py | 140 | Config file | ⭐⭐ |
| pattern_4_rest_api.py | 200 | REST API | ⭐⭐⭐ |
| pattern_5_callable_service.py | 100 | Callable object | ⭐ |
| pattern_6_abstract_interface.py | 200 | Abstract interface | ⭐⭐⭐ |
| pattern_7_event_driven.py | 220 | Event-driven | ⭐⭐⭐⭐ |
| pattern_8_mcp_server.py | 170 | MCP server | ⭐⭐⭐ |
| requirements-mcp.txt | 2 | Optional MCP dependency | - |
| README.md | 400+ | Overview & guide | - |
| PATTERNS.md | 500+ | Detailed patterns | - |
| ABSTRACTION_LEVELS.md | 400+ | Theory & architecture | - |
| DIAGRAMS.md | 300+ | Visual diagrams | - |
| QUICKREF.md | 250+ | Quick reference | - |
| config_example.json | 30 | Example config | - |

**Total:** 3500+ lines of code and documentation

---

## ✅ Quality Checklist

- [x] Core implementation (cert_generator.py) - Production ready
- [x] All 8 patterns - Working examples
- [x] Comprehensive documentation - 1500+ lines
- [x] Visual diagrams - Architecture explanations
- [x] Quick reference - For rapid lookup
- [x] Real-world examples - Phase migration, stacking
- [x] Config examples - Ready to use
- [x] Error handling - Graceful failures
- [x] Type hints - Type-safe Python
- [x] Comments - Code clarity

---

## 🚀 Next Steps

1. **Review the toolkit** - Read README.md and PATTERNS.md
2. **Try each pattern** - Run all 8 examples
3. **Study the theory** - Read ABSTRACTION_LEVELS.md
4. **Plan your implementation** - Use decision tree in QUICKREF.md
5. **Adapt for your code** - Replace cert_generator.py
6. **Choose patterns** - Pick 1-3 patterns for your needs
7. **Implement** - Use as template

---

## 📞 Quick Questions

**Q: Which pattern should I use?**
A: Check decision tree in QUICKREF.md

**Q: How do I adapt this for my code?**
A: Replace cert_generator.py, keep interface structure

**Q: Can I use multiple patterns?**
A: Yes! That's actually recommended for production systems

**Q: Where do I start?**
A: Read README.md, then PATTERNS.md

**Q: How do I understand the theory?**
A: Read ABSTRACTION_LEVELS.md

---

Print this file and use as a navigation guide! 🗺️
