# Architecture Diagrams: 7 Integration Patterns

Visual representations of how each pattern works.

## Pattern 1: Python Library

```
┌─────────────────────────────────────────────┐
│ AI System (Python)                          │
├─────────────────────────────────────────────┤
│ from cert_generator import ...              │
│ gen = CertificateGenerator()                │
│ result = gen.generate(params)   ◄── calls  │
└────────────────┬──────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│ cert_generator.py                           │
├─────────────────────────────────────────────┤
│ CertificateGenerator.generate()             │
│   └─ subprocess.run(["openssl", ...])       │
│         └─ OpenSSL process                  │
└─────────────────────────────────────────────┘

Data Flow:
  CertificateParams → generate() → CertificateOutput
                       (Python function call)
  
Overhead: Minimal (same process)
Coupling: Tight (direct dependency)
Performance: ★★★★★ Fastest
```

---

## Pattern 2: JSON stdin/stdout

```
┌──────────────────────────┐
│ AI System                │
├──────────────────────────┤
│ Prepare JSON input       │
│ Start subprocess         │
│ Send JSON to stdin  ─┐   │
│ Read JSON from stdout◄─┐ │
│ Parse result         │ │ │
└──────────────────────┼─┼─┘
                       │ │
          ┌────────────┘ │
          │              │
          ▼              │
    ┌──────────────────────────┐
    │ Process (Python)         │
    ├──────────────────────────┤
    │ pattern_2_json_api.py    │
    │                          │
    │ stdin: JSON  ───┐        │
    │ (deserialize)   │        │
    │ generate()      │        │
    │ (serialize)     │        │
    │ stdout: JSON ◄──┘        │
    └──────────────────────────┘

Data Flow:
  {"cn": "..."}  ──stdin──> Parser ──> generate() ──> Serializer ──stdout──> {"success": ...}
  
Overhead: Medium (serialization + process spawn)
Coupling: Very Low (process boundary)
Performance: ★★★☆☆ Medium
Works With: Any language that can read JSON
```

---

## Pattern 3: Config File

```
┌───────────────────────────────┐
│ AI System                     │
├───────────────────────────────┤
│ Generate config YAML/JSON  ──┐│
│ Write to file               ││
│ Call script with filename ◄─┘│
│                              │
│ Read result JSON             │
└───────────────────────────────┘
           │
           ▼
    ┌───────────────────────────┐
    │ cert_config.yaml          │
    ├───────────────────────────┤
    │ certificates:             │
    │   - cn: api.example.com   │
    │     key_type: rsa         │
    │   - cn: web.example.com   │
    │     key_type: ec          │
    └───────────────────────────┘
           │
           ▼
    ┌───────────────────────────────┐
    │ pattern_3_config_file.py      │
    ├───────────────────────────────┤
    │ for each cert in config:      │
    │   generate(params)            │
    │ aggregate results             │
    │ return summary                │
    └───────────────────────────────┘

Data Flow:
  AI writes → YAML File ← Script reads
  Iterates config ────> Generates certs ────> Returns aggregated result

Overhead: Low-Medium (file I/O)
Coupling: Low (declarative)
Performance: ★★★★☆ Good for batch
Perfect For: Batch operations, audit trails (config is documentation)
```

---

## Pattern 4: REST API

```
┌────────────────────────────────────────┐
│ AI System (Any Language)               │
├────────────────────────────────────────┤
│ POST /api/v1/certificate               │
│ Content-Type: application/json         │
│ {"cn": "example.com", ...}         ┐   │
│                                     │   │
│ ◄─ HTTP Response (200) ──────────┐ │   │
│ {"success": true, "cert_path": ...} │
└────────────────────────────────────────┘
              │                  ▲
              │ HTTP             │ HTTP
              ▼                  │
    ┌────────────────────────────────────┐
    │ REST Server (Flask)                │
    ├────────────────────────────────────┤
    │ @app.route('/api/v1/certificate')  │
    │   ├─ Parse JSON request            │
    │   ├─ Validate parameters           │
    │   ├─ Call CertificateGenerator     │
    │   └─ Return JSON response          │
    └────────────────────────────────────┘
             │
             ▼
    ┌────────────────────────────────────┐
    │ CertificateGenerator               │
    └────────────────────────────────────┘

Data Flow:
  JSON Request ──HTTP POST──> REST Handler ──Python──> Generator
     (HTTP)                      (Route)        (Function)
  
  Result ──JSON──> Response ──HTTP──> Client receives result

Overhead: High (serialization + HTTP)
Coupling: Very Low (process/network boundary)
Performance: ★★★☆☆ Medium (network latency)
Perfect For: Distributed systems, multiple clients, cloud
Language: Fully agnostic - client can be Python, JavaScript, Go, etc.
```

---

## Pattern 5: Callable Service

```
┌──────────────────────────────────────────┐
│ AI System (Python)                       │
├──────────────────────────────────────────┤
│ service = CertificateService()           │
│                                          │
│ # Basic call                             │
│ result = service(                        │
│   cn="example.com",                      │
│   key_type="rsa"                         │
│ )  ◄─── Callable interface              │
│                                          │
│ # Batch call                             │
│ results = service.batch([{...}, {...}])  │
│                                          │
│ # With defaults                          │
│ corp_service = service.with_defaults(    │
│   organization="Corp"                    │
│ )                                        │
│ result = corp_service(cn="api.corp.com") │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ CertificateService                       │
├──────────────────────────────────────────┤
│ def __call__(self, **kwargs)             │
│   └─ CertificateGenerator.generate()     │
│       └─ subprocess.run(openssl)         │
└──────────────────────────────────────────┘

Data Flow:
  kwargs ──call──> __call__ ──validate──> generate() ──return──> CertificateOutput

Overhead: Minimal
Coupling: Medium (Python objects)
Performance: ★★★★★ Fastest
Perfect For: Dependency injection, testing, modern Python
```

---

## Pattern 6: Abstract Interface

```
┌─────────────────────────────────────────────┐
│ AI System (Python)                          │
├─────────────────────────────────────────────┤
│ provider = factory.create("openssl")        │
│ manager = CertificateManager(provider)      │
│                                             │
│ result = manager.create_certificate(...)    │
│ capabilities = manager.get_capabilities()   │
│                                             │
│ (AI uses only ICertificateProvider methods) │
└─────────────────────────────────────────────┘
           │
           ▼
    ┌───────────────────────────────────┐
    │ CertificateProviderFactory        │
    ├───────────────────────────────────┤
    │ _providers = {                    │
    │   "openssl": OpenSSL...,          │
    │   "mock": MockProvider,           │
    │   "aws": AwsAcmProvider,          │
    │   ...                             │
    │ }                                 │
    │                                   │
    │ create(type) ──┬─────────────┐   │
    └────────────────┼─────────────┼───┘
                     │             │
         ┌───────────┘             └──────────┐
         │                                    │
         ▼                                    ▼
    ┌──────────────────┐          ┌──────────────────┐
    │ OpenSSLProvider  │          │ MockProvider     │
    ├──────────────────┤          ├──────────────────┤
    │ .create()        │          │ .create()        │
    │ .validate()      │          │ .validate()      │
    │ .get_...()       │          │ .get_...()       │
    └──────────────────┘          └──────────────────┘
         │                              │
         ▼                              ▼
    subprocess.run()              Return mock result
    (OpenSSL)                      (for testing)

Data Flow:
  AI calls interface method ──factory──> concrete provider ──executes logic──> result

Overhead: Low (factory creates once)
Coupling: Very Low (interface contract)
Performance: ★★★★★ Fastest
Perfect For: Multiple implementations, testing, future-proof
Future-Proof: Add AWS provider, Vault provider, etc. without changing AI code
```

---

## Pattern 7: Event-Driven

```
┌─────────────────────────────────────────────┐
│ AI System (Python)                          │
├─────────────────────────────────────────────┤
│ event_bus = CertificateEventBus()           │
│                                             │
│ # Subscribe to events                       │
│ event_bus.subscribe(                        │
│   GENERATION_START,                         │
│   on_start_handler                          │
│ )                                           │
│ event_bus.subscribe(                        │
│   GENERATION_COMPLETE,                      │
│   on_complete_handler                       │
│ )                                           │
│                                             │
│ generator = EventDrivenGenerator(event_bus) │
│ result = generator.generate(params)         │
│ # ──────────────────────────────────────┐   │
│ #   Events fire, handlers execute       │   │
│ # ◄──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
           │
           ▼
    ┌────────────────────────────┐
    │ EventDrivenGenerator       │
    ├────────────────────────────┤
    │ def generate(params):      │
    │   bus.publish(START)   ──┐ │
    │   validate()           │ │ │
    │   bus.publish(VALID)   │ │ │
    │   generate()           │ │ │
    │   bus.publish(DONE)    │ │ │
    │   return result        │ │ │
    │                        │ │ │
    │ ◄───────────────────────┘ │ │
    └────────────────────────────┘
           │
      ┌────┴────────────────┐
      │                     │
      ▼                     ▼
 ┌──────────────┐     ┌──────────────┐
 │ Event: START │     │ Event: DONE  │
 ├──────────────┤     ├──────────────┤
 │ timestamp    │     │ timestamp    │
 │ cn           │     │ cn           │
 │ data         │     │ data         │
 └──────────────┘     └──────────────┘
      │                     │
 ┌────┴────────────────────┴──────┐
 │  Event Bus Registry            │
 ├───────────────────────────────┤
 │ GENERATION_START: [handler1,  │
 │                    handler2]   │
 │ GENERATION_COMPLETE: [handler3] │
 └───────────────────────────────┘
      │        │          │
      ▼        ▼          ▼
  Handler1  Handler2  Handler3
  (logging) (audit)  (notification)

Data Flow:
  generate() ──publishes──> Event ──broadcasts──> All Handlers
                            ├── logging_handler()
                            ├── audit_handler()
                            └── notification_handler()

Overhead: Medium (event publishing)
Coupling: Very Low (event contract)
Performance: ★★★☆☆ Medium
Perfect For: Complex workflows, audit logging, notifications
Observable: Full lifecycle visibility
```

---

## Comparison: Architecture Stack Height

```
Pattern 1: Library        (Shortest Stack)
┌─────────────┐
│ AI          │ Direct call
└─────────────┘
│
└──> CertificateGenerator ──> OpenSSL

Pattern 2: JSON
┌─────────────┐
│ AI          │ Write JSON
└─────────────┘
│
└──> (Process Boundary)
│
└──> JSON Parser ──> CertificateGenerator ──> OpenSSL

Pattern 3: Config
┌─────────────┐
│ AI          │ Write config
└─────────────┘
│
└──> Config File
│
└──> (Process Boundary)
│
└──> YAML Parser ──> Config Handler ──> CertificateGenerator ──> OpenSSL

Pattern 4: REST            (Tallest Stack)
┌─────────────┐
│ AI          │ HTTP POST
└─────────────┘
│
└──> HTTP
│
└──> (Network Boundary)
│
└──> REST Handler ──> JSON Parser ──> CertificateGenerator ──> OpenSSL

Pattern 5: Callable
┌─────────────┐
│ AI          │ Call object
└─────────────┘
│
└──> Service Object ──> CertificateGenerator ──> OpenSSL

Pattern 6: Abstract
┌─────────────┐
│ AI          │ Use interface
└─────────────┘
│
└──> (Interface Contract)
│
└──> Factory ──> Concrete Provider ──> CertificateGenerator/Other/Etc ──> Various

Pattern 7: Event         (Most Complex)
┌─────────────┐
│ AI          │ Register handlers
└─────────────┘
│
└──> Event Bus
│
├──> Handler 1
├──> Handler 2
└──> Handler 3
     │
     └──> CertificateGenerator ──> OpenSSL
```

---

## Real-World Scenario: Multi-Pattern Stack

```
User Application (Web)
    │
    ├─ Pattern 4 (REST) ──> Cert Service (Backend)
    │                           │
    │                           ├─ Pattern 6 (Abstract)
    │                           │     ├─ OpenSSL Provider
    │                           │     └─ AWS Provider
    │                           │
    │                           └─ Pattern 7 (Events)
    │                               ├─ Audit Log Handler
    │                               └─ Notification Handler
    │
    ├─ Pattern 2 (JSON) ──> CLI Tool
    │                           │
    │                           └─ Certificate Generator
    │
    └─ Pattern 3 (Config) ──> Batch Job
                                 │
                                 └─ Generate N certificates

All patterns use the same underlying cert_generator.py
but expose it through different interfaces!
```

---

## Key Insight: Inversion of Knowledge

```
Traditional (Implementation-Heavy):
┌─────────────────────────────────────┐
│ AI needs to know:                   │
│ - OpenSSL flags                     │
│ - subprocess API                    │
│ - File paths                        │
│ - Error codes                       │
│ - Platform differences              │
│ ...                                 │
└─────────────────────────────────────┘

With Abstraction Patterns:
┌─────────────────────────────────────┐
│ AI knows:                           │
│ - Input parameters (cn, key_type)   │
│ - Output format (success/failure)   │
│ - Interface contract (methods)      │
│ - How to handle errors              │
│ ...                                 │
└─────────────────────────────────────┘

Result: AI code remains stable when:
✓ You optimize OpenSSL calls
✓ You switch providers
✓ You add new algorithms
✓ You change file locations
✓ You refactor internal logic
```

This is the power of abstraction for AI integration.
