#!/usr/bin/env python3
"""
PATTERN 5: CALLABLE OBJECT INTERFACE
====================================
AI creates an object and calls it like a function
Clean, object-oriented, easy to mock/test
Perfect for dependency injection and testing
"""

from cert_generator import CertificateGenerator, CertificateParams, CertificateOutput


class CertificateService:
    """
    Callable service for generating certificates
    
    Usage:
        cert_service = CertificateService()
        result = cert_service(
            cn="example.com",
            key_type="rsa",
            key_strength=2048,
            validity_days=365
        )
    """

    def __init__(self, openssl_path: str = "openssl"):
        """Initialize service with OpenSSL path"""
        self.generator = CertificateGenerator(openssl_path)

    def __call__(
        self,
        cn: str,
        key_type: str = "rsa",
        key_strength: int = 2048,
        validity_days: int = 365,
        country: str = None,
        state: str = None,
        locality: str = None,
        organization: str = None,
        output_dir: str = None
    ) -> CertificateOutput:
        """
        Generate certificate with named parameters
        
        Args:
            cn: Common Name
            key_type: "rsa" or "ec"
            key_strength: Key bits (RSA: 2048/4096, EC: 256/384/521)
            validity_days: Certificate validity period
            country: Country code
            state: State/Province
            locality: City
            organization: Organization name
            output_dir: Output directory
            
        Returns:
            CertificateOutput with success/failure information
        """
        params = CertificateParams(
            cn=cn,
            key_type=key_type,
            key_strength=key_strength,
            validity_days=validity_days,
            country=country,
            state=state,
            locality=locality,
            organization=organization,
            output_dir=output_dir
        )
        return self.generator.generate(params)

    def batch(self, requests: list) -> list:
        """
        Generate multiple certificates
        
        Args:
            requests: List of dictionaries with certificate parameters
            
        Returns:
            List of CertificateOutput objects
        """
        results = []
        for req in requests:
            result = self(**req)
            results.append(result)
        return results

    def with_defaults(self, **defaults):
        """
        Create a new service with default parameters
        
        Usage:
            company_certs = cert_service.with_defaults(
                organization="My Company",
                country="US",
                validity_days=730
            )
            result = company_certs(cn="api.example.com")
        """
        return BoundCertificateService(self, defaults)


class BoundCertificateService(CertificateService):
    """Service with bound default parameters"""

    def __init__(self, service: CertificateService, defaults: dict):
        self.generator = service.generator
        self.defaults = defaults

    def __call__(self, **kwargs) -> CertificateOutput:
        """Call with defaults merged in"""
        merged_params = {**self.defaults, **kwargs}
        return super().__call__(**merged_params)


# AI usage pattern
def ai_pattern_5_callable():
    """Example: AI uses callable service object"""
    
    # Create service instance
    cert_service = CertificateService()
    
    # AI can call it like a function
    result = cert_service(
        cn="example.com",
        key_type="rsa",
        key_strength=2048,
        validity_days=365,
        organization="My Company"
    )
    
    # AI can handle batch operations
    batch_results = cert_service.batch([
        {"cn": "api.example.com", "key_type": "rsa"},
        {"cn": "web.example.com", "key_type": "ec", "key_strength": 256}
    ])
    
    # AI can create specialized variants
    company_certs = cert_service.with_defaults(
        organization="My Company",
        country="US",
        validity_days=730
    )
    
    # Then use the specialized variant
    api_cert = company_certs(cn="api.example.com")
    web_cert = company_certs(cn="web.example.com")
    
    return result, batch_results, api_cert, web_cert


if __name__ == "__main__":
    result, batch, api, web = ai_pattern_5_callable()
    print(f"Pattern 5 - Callable Service: {result.message}")
    print(f"Batch results: {len(batch)} certificates")
