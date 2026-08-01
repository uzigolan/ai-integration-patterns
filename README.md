# AI Code Execution Patterns - Complete Toolkit

This toolkit demonstrates **8 different methods** for AI systems to use your custom code without knowing implementation details.

## 📁 What You Have

### Core Implementation
- **`cert_generator.py`** - Self-signed certificate generator using OpenSSL
  - Wraps OpenSSL in clean Python interface
  - Handles RSA and EC key types
  - Parameter validation
  - Error handling

### 8 Integration Patterns

1. **`pattern_1_library.py`** - Python Library
   - Direct import and function calls
   - Fastest, tightest coupling
   - Perfect for: Python-only systems

2. **`pattern_2_json_api.py`** - JSON stdin/stdout
   - Text-based interface
   - Language-agnostic
   - Perfect for: LLMs, CLI tools, shell scripts

3. **`pattern_3_config_file.py`** - Configuration File
   - YAML/JSON config driven
   - Batch processing
   - Perfect for: Workflows, batch operations

4. **`pattern_4_rest_api.py`** - REST API
   - HTTP-based service
   - Scalable, distributed
   - Perfect for: Cloud, microservices, multiple clients

5. **`pattern_5_callable_service.py`** - Callable Object
   - Python object with `__call__`
   - Clean interface, testable
   - Perfect for: Dependency injection, modern Python

6. **`pattern_6_abstract_interface.py`** - Abstract Interface
   - Strategy pattern with factory
   - Pluggable implementations
   - Perfect for: Multiple algorithms, testing with mocks

7. **`pattern_7_event_driven.py`** - Event-Driven
   - Pub/Sub event bus
   - Observable, audit-logged
   - Perfect for: Complex workflows, notifications

8. **`pattern_8_mcp_server.py`** - MCP Server
   - Native tool interface for Codex and other MCP clients
   - Exposes capability discovery, validation, and certificate generation tools
   - Perfect for: Controlled agent actions and tool discovery

### Documentation

- **`PATTERNS.md`** - Comprehensive guide to all 8 patterns
  - Detailed explanation of each pattern
  - Pros/cons comparison table
  - Decision matrix
  - Implementation checklist

- **`ABSTRACTION_LEVELS.md`** - Theory and architecture
  - Why abstraction matters for AI
  - Abstraction stack diagrams
  - Knowledge required for each pattern
  - Real-world phase migration examples

- **`README.md`** - This file

### Examples

- **`config_example.json`** - Example configuration file for Pattern 3
  - Multiple certificates with different settings
  - Shows YAML/JSON structure

## 🚀 Quick Start

**Windows Users:** Activate the virtual environment first:

.venv\Scripts\Activate.ps1

Then use `python` for all commands below.

**Or activate the included virtual environment:**

.venv\Scripts\Activate.ps1
python pattern_1_library.py

### Pattern 1: Python Library (Simplest)

python pattern_1_library.py

### Pattern 2: JSON API

echo '{"cn":"example.com"}' | python pattern_2_json_api.py

### Pattern 3: Config File

python pattern_3_config_file.py config_example.json

### Pattern 4: REST API (Start Server)

python pattern_4_rest_api.py

Then in another terminal:

Invoke-RestMethod -Uri http://localhost:5000/api/v1/certificate -Method POST -Body (@{cn="example.com"} | ConvertTo-Json) -ContentType "application/json"

### Pattern 5: Callable Service

python pattern_5_callable_service.py

### Pattern 6: Abstract Interface

python pattern_6_abstract_interface.py

### Pattern 7: Event-Driven

python pattern_7_event_driven.py

### Pattern 8: MCP Server (Codex + Copilot)

```powershell
py -m pip install -r requirements-mcp.txt
codex mcp add certificate-generator -- "$PWD\.venv\Scripts\python.exe" "$PWD\pattern_8_mcp_server.py"
```

Or register for Copilot in VS Code with `.vscode/mcp.json`:

CLI option (PowerShell) to create it automatically:

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

Restart your MCP client after registration. The server validates requests before generation and writes keys only under `certs/`.

## 🎯 How to Use This Toolkit

### As an Educational Resource
Learn different architectural patterns for AI integration:
1. Read `ABSTRACTION_LEVELS.md` first (theory)
2. Review each pattern file (implementations)
3. Experiment with each pattern (practice)

### As a Template for Your Own Code
1. Start with your implementation (like `cert_generator.py`)
2. Pick the pattern(s) that match your use case
3. Adapt the example files to your code
4. Use the patterns to expose your code to AI

### To Show Different Approaches to AI
Demonstrate that AI doesn't need implementation details:
1. Start with Pattern 1 (direct access)
2. Show Pattern 2 (JSON abstraction)
3. Show Pattern 4 (REST abstraction)
4. Explain: AI never needs to know what changed
5. Apply to your own domain

## 📊 Comparison at a Glance

| Pattern | Coupling | Speed | Complexity | Best For |
|---------|----------|-------|-----------|----------|
| 1. Library | High | Fastest | Lowest | Simple Python |
| 2. JSON | Low | Fast | Low | CLI/LLM |
| 3. Config | Low | Medium | Low | Batch ops |
| 4. REST | Very Low | Medium | High | Distributed |
| 5. Callable | Medium | Fastest | Medium | OOP Python |
| 6. Abstract | Low | Fast | Medium | Testing |
| 7. Event | Very Low | Medium | Very High | Complex workflows |
| 8. MCP | Very Low | Medium | Medium | Codex, Copilot, and other MCP clients |

## 🔑 Key Insight

**The Goal:** AI uses your code through a clear interface without knowing how it works internally.

**The Benefit:** You can change implementation details (optimize, refactor, migrate) without breaking AI code.

**The Implementation:** Use abstraction layers at the boundary between AI and your code.

## 📝 Examples of Real-World Applications

### System Monitoring
```
AI: "Generate certificate for new server"
  → Uses Pattern 3 (Config) to batch create certs
  → Pattern 7 (Events) triggers monitoring setup
  → Events sent to Grafana/Prometheus
```

### DevOps Workflow
```
AI: "Create certs for staging environment"
  → Calls Pattern 4 (REST) to cert service
  → REST service uses Pattern 6 (Abstract) to switch providers
  → Development: Mock provider (Pattern 6)
  → Production: Real OpenSSL provider (Pattern 6)
```

### Cloud Infrastructure
```
AI: "Generate wildcard certificate"
  → Uses Pattern 2 (JSON) via subprocess
  → Piped through infrastructure automation
  → No language coupling, works with any CLI tool
```

### Compliance & Audit
```
AI: "Generate certificates with audit trail"
  → Uses Pattern 7 (Event-Driven)
  → Each certificate generation fires events
  → Events captured in immutable audit log
  → Compliance report generated from events
```

## 🔧 Extending This Toolkit

### Add a New Pattern
1. Create `pattern_8_yourpattern.py`
2. Implement the interface
3. Document in `PATTERNS.md`
4. Add to comparison table

### Use with Your Code
1. Replace `cert_generator.py` with your implementation
2. Keep the same interface (`CertificateParams`, `CertificateOutput`)
3. All patterns work with your code!

### Add New Providers (Pattern 6)
```python
class AwsAcmProvider(ICertificateProvider):
    """AWS ACM implementation"""
    def create(self, **kwargs) -> CertificateOutput:
        # AWS ACM logic here
        pass

# Register it
CertificateProviderFactory.register("aws", AwsAcmProvider)

# AI can now use it
provider = CertificateProviderFactory.create("aws")
# Same interface, different implementation!
```

## ❓ FAQ

**Q: Which pattern should I use?**
A: Start with Pattern 1 (library) for simplicity. If you need to scale, change to Pattern 4 (REST). If you need testing, add Pattern 6 (abstract). If you need audit, add Pattern 7 (events).

**Q: Can I use multiple patterns?**
A: Yes! Many real systems use combinations. Pattern 3 (config) feeds into Pattern 7 (events), which notifies Pattern 4 (REST) API.

**Q: How does this help AI?**
A: AI only needs to know the interface contract (input/output), not the implementation. This means you can change your code, add optimizations, or migrate to different technologies without AI code breaking.

**Q: Can I use this with non-Python code?**
A: Yes! Patterns 2 (JSON), 3 (Config), and 4 (REST) work with any language. Pattern 1, 5, 6, 7 are Python-specific.

**Q: What if I want to add a new parameter?**
A: With proper abstraction, you can add optional parameters without breaking existing code. AI learns about new parameters through interface documentation.

## 📚 Learning Path

1. **Beginner**: Start with Pattern 1, understand the problem
2. **Intermediate**: Read ABSTRACTION_LEVELS.md, try Pattern 2-3
3. **Advanced**: Study Pattern 6-7, understand strategy/observer patterns
4. **Expert**: Combine patterns, build complex workflows

## 🎓 Key Takeaways

1. **Abstraction is about contracts** - AI needs to know what goes in and comes out, not how
2. **Multiple patterns solve different problems** - No one pattern fits all cases
3. **Patterns can be stacked** - Real systems often use multiple patterns together
4. **Your code doesn't change** - Only the interface/API changes when switching patterns
5. **AI code stays stable** - Implementation can evolve without breaking AI integration

## 📞 Questions?

Review the specific pattern file + read PATTERNS.md + check ABSTRACTION_LEVELS.md

---

## 🤖 Meta-Layer: AI That Authors and Evaluates Its Own Instructions

Beyond the 7 code-integration patterns, the VS Code Copilot ecosystem includes a **meta-layer** where AI can author, manage, and evaluate the very customization files that govern its own behavior.

### What Are Customization Files?

Customization files tell Copilot *how to behave* in a given workspace:

| File type | Purpose |
|---|---|
| `.instructions.md` | Rules applied automatically to matching files |
| `.prompt.md` | Reusable prompt templates (`/my-prompt`) |
| `SKILL.md` | Packaged domain knowledge loaded on demand |
| `.agent.md` / `AGENTS.md` | Custom agent modes with scoped tools |
| `copilot-instructions.md` | Global workspace instructions |

### Skills That **Create** Customization Files

The **`agent-customization`** skill lets Copilot author, update, and debug all of the above file types:

```
User: "Save a rule that all Python files use double quotes"
  → Copilot uses agent-customization skill
  → Creates .github/copilot-instructions.md (or .instructions.md)
  → Adds applyTo: "**/*.py" frontmatter and the rule
```

```
User: "Create a skill for our REST API conventions"
  → Copilot scaffolds a SKILL.md with description + instructions
  → Adds it to the skills list so it auto-loads on relevant tasks
```

### Skills That **Analyze** Customization Files

The **`analyze-prompt`** skill runs the Chat Customizations Evaluations extension against any prompt/instruction file and reports diagnostics:

```
User: "Analyze this prompt file"
  → Runs chatCustomizationsEvaluations.analyzePrompt command
  → Reads Problems panel
  → Summarizes issues (empty responses, bad frontmatter, unreachable rules, etc.)
```

The **`fix-customization-evaluation-diagnostics`** skill takes those diagnostics and automatically applies fixes:

```
User: "Fix the diagnostics in my prompt"
  → Reads Problems panel for the active file
  → Applies targeted edits to resolve each reported issue
```

### The Feedback Loop

```
  Author (agent-customization)
       ↓
  .instructions.md / .prompt.md / SKILL.md
       ↓
  Analyze (analyze-prompt)
       ↓
  Diagnostics in Problems panel
       ↓
  Fix (fix-customization-evaluation-diagnostics)
       ↓
  Better customization files → Better AI behavior
```

### How This Relates to the 8 Patterns

The 8 patterns in this toolkit teach AI to use *your code* through clean interfaces.  
The meta-layer is the same principle applied one level up: AI uses *its own configuration* through clean, analyzable, fixable interfaces.

- Patterns 1–8 = abstract your **code** from the AI
- Meta-layer = abstract your **instructions** from the AI

Good luck! 🚀
