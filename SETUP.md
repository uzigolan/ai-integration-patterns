# 🔧 Setup Guide

## Windows Users: Two Options

### Option 1: Use Python Launcher (Recommended for Quick Testing)

The `py` launcher comes with Python and handles Windows Python routing:

py pattern_1_library.py

**Pros:** No setup needed, works immediately
**Cons:** Requires `py` every time

---

### Option 2: Use Virtual Environment (Recommended for Development)

A virtual environment is already created at `.venv`:

.venv\Scripts\Activate.ps1; python pattern_1_library.py; python pattern_2_json_api.py; python pattern_3_config_file.py; deactivate

**Pros:** Clean environment, no `py` prefix needed, isolates dependencies
**Cons:** Need to activate each terminal session

---

## PowerShell Execution Policy Issues?

If you get an error about execution policies when activating:

.venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled on this system.

**Solution:** Run this once (in elevated PowerShell):

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Or use the batch file instead:

.venv\Scripts\activate.bat

---

## Linux/Mac Users

Just use `python` directly:

python pattern_1_library.py

Or activate the virtual environment:

source .venv/bin/activate; python pattern_1_library.py

---

## Virtual Environment Details

The `.venv` folder contains:
- **Scripts/** - Executable files (python.exe, pip.exe, etc.)
- **Lib/** - Python packages
- **Include/** - C header files
- **pyvenv.cfg** - Configuration

### What's Installed?

Currently: Just base Python 3.12.10

### Installing Packages

Once activated, you can install packages:

pip install flask
pip install pyyaml

### Recreating the Virtual Environment

If something breaks, recreate it:

```powershell
# Remove old one
Remove-Item .venv -Recurse -Force

# Create new one
py -m venv .venv

# Activate
.venv\Scripts\Activate.ps1
```

---

## Quick Command Reference

| Task | Windows (py) | Windows (venv) | Linux/Mac |
|------|---|---|---|
| Run pattern | `py pattern_1_library.py` | `.venv\Scripts\Activate.ps1` then `python pattern_1_library.py` | `python pattern_1_library.py` |
| Activate venv | N/A | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Deactivate venv | N/A | `deactivate` | `deactivate` |
| Install package | N/A | (after activate) `pip install <pkg>` | (after activate) `pip install <pkg>` |

---

## Why Virtual Environment?

**Without venv:** Packages install globally, can conflict with other projects
**With venv:** Each project has isolated environment

For this toolkit, venv is optional but recommended if you:
- Install additional packages (Flask, PyYAML)
- Use it alongside other Python projects
- Want clean dependency management

---

## Troubleshooting

### Error: "python was not found"
✅ **Fix:** Use `py` instead of `python`
```powershell
py pattern_1_library.py
```

### Error: "cannot load activate.ps1"
✅ **Fix 1:** Use batch file instead
```cmd
.venv\Scripts\activate.bat
```

✅ **Fix 2:** Update PowerShell execution policy (see above)

### "Module not found" when running patterns
✅ Make sure you're in the correct directory:
```powershell
cd c:\Users\uzi\Downloads\tools
py pattern_1_library.py
```

### Need OpenSSL installed?
The toolkit requires OpenSSL. Check:
```powershell
openssl version
```

If not found, install via:
- **Windows:** Use `choco install openssl` (if Chocolatey installed)
- **Or:** Download from https://slproweb.com/products/Win32OpenSSL.html

---

## Next Steps

1. ✅ Virtual environment is ready at `.venv`
2. ✅ Python 3.12.10 is working
3. ✅ Try running patterns with `py` or after venv activation
4. Read `README.md` for overview
5. Try each pattern file
6. Adapt for your own code

---

## Questions?

- Need more Python version info? Run: `py --version`
- Need to know where Python is installed? Run: `py -c "import sys; print(sys.executable)"`
- Need virtual environment info? Run: `pip list` (after activation)

Happy coding! 🚀
