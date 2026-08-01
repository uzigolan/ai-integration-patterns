"""
PATTERN 1: PYTHON LIBRARY INTERFACE
======================================
AI interacts through Python function calls (like using a library)
No knowledge of CLI args, subprocess calls, or OpenSSL directly
AI sees: Function signature with typed parameters and return values
"""

from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput


def ai_pattern_1_library():
    """AI uses the certificate generator as a Python library"""
    
    # AI only knows about these abstractions:
    # - CertificateParams (what inputs are needed)
    # - CertificateGenerator (how to generate)
    # - CertificateOutput (what it gets back)
    
    generator = CertificateGenerator()
    
    params = CertificateParams(
        cn="example.com",
        key_type="rsa",
        key_strength=2048,
        validity_days=365,
        organization="My Company",
        country="US"
    )
    
    result: CertificateOutput = generator.generate(params)
    
    # AI only knows:
    # - result.success: bool
    # - result.message: str
    # - result.cert_path: str or None
    # - result.key_path: str or None
    # - result.details: dict or None
    
    return result


if __name__ == "__main__":
    result = ai_pattern_1_library()
    print(f"Pattern 1 - Python Library: {result.message}")
