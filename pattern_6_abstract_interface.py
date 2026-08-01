#!/usr/bin/env python3
"""
PATTERN 6: ABSTRACT INTERFACE / STRATEGY PATTERN
================================================
AI uses abstract interface, multiple implementations possible
Perfect for pluggable architectures and future extensibility
Enables mocking and testing
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import asdict
from cert_generator import (
    CertificateGenerator, CertificateParams, CertificateOutput
)


class ICertificateProvider(ABC):
    """
    Abstract interface for certificate generation
    AI knows only this interface, not specific implementations
    """

    @abstractmethod
    def create(self, **kwargs) -> CertificateOutput:
        """Create a self-signed certificate"""
        pass

    @abstractmethod
    def validate(self, **kwargs) -> Dict[str, Any]:
        """Validate certificate parameters before creation"""
        pass

    @abstractmethod
    def get_supported_key_types(self) -> list:
        """Return list of supported key types"""
        pass

    @abstractmethod
    def get_supported_key_strengths(self, key_type: str) -> list:
        """Return list of supported key strengths for given type"""
        pass


class OpenSSLCertificateProvider(ICertificateProvider):
    """
    OpenSSL-based implementation
    AI doesn't know this exists, only uses ICertificateProvider interface
    """

    def __init__(self, openssl_path: str = "openssl"):
        self.generator = CertificateGenerator(openssl_path)

    def create(self, **kwargs) -> CertificateOutput:
        """Create certificate using OpenSSL"""
        params = CertificateParams(**kwargs)
        return self.generator.generate(params)

    def validate(self, **kwargs) -> Dict[str, Any]:
        """Validate parameters"""
        try:
            params = CertificateParams(**kwargs)
            return {
                "valid": True,
                "cn": params.cn,
                "key_type": params.key_type,
                "key_strength": params.key_strength,
                "validity_days": params.validity_days
            }
        except ValueError as e:
            return {
                "valid": False,
                "error": str(e)
            }

    def get_supported_key_types(self) -> list:
        """Supported key types"""
        return ["rsa", "ec"]

    def get_supported_key_strengths(self, key_type: str) -> list:
        """Supported strengths"""
        if key_type == "rsa":
            return [2048, 4096]
        elif key_type == "ec":
            return [256, 384, 521]
        return []


class MockCertificateProvider(ICertificateProvider):
    """
    Mock implementation for testing
    AI can use same interface with mock provider
    """

    def create(self, **kwargs) -> CertificateOutput:
        """Create mock certificate"""
        return CertificateOutput(
            success=True,
            message=f"Mock certificate for {kwargs.get('cn', 'unknown')}",
            cert_path=f"/mock/path/{kwargs.get('cn', 'unknown')}.crt",
            key_path=f"/mock/path/{kwargs.get('cn', 'unknown')}.key"
        )

    def validate(self, **kwargs) -> Dict[str, Any]:
        """Mock validation"""
        return {"valid": True}

    def get_supported_key_types(self) -> list:
        return ["rsa", "ec"]

    def get_supported_key_strengths(self, key_type: str) -> list:
        return [2048, 4096] if key_type == "rsa" else [256, 384, 521]


class CertificateProviderFactory:
    """
    Factory to create certificate providers
    AI can request providers without knowing implementations
    """

    _providers: Dict[str, type] = {
        "openssl": OpenSSLCertificateProvider,
        "mock": MockCertificateProvider
    }

    @classmethod
    def create(cls, provider_type: str = "openssl", **options) -> ICertificateProvider:
        """
        Create provider instance
        
        Args:
            provider_type: "openssl" or "mock"
            options: Provider-specific options
            
        Returns:
            ICertificateProvider implementation
        """
        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_type}")
        return provider_class(**options)

    @classmethod
    def register(cls, name: str, provider_class: type):
        """Register new provider implementation"""
        cls._providers[name] = provider_class


class CertificateManager:
    """
    Manager that uses certificate provider interface
    AI instantiates manager with a provider, uses only ICertificateProvider methods
    """

    def __init__(self, provider: ICertificateProvider):
        self.provider = provider

    def create_certificate(self, cn: str, **kwargs) -> CertificateOutput:
        """Create certificate with validation"""
        # AI doesn't know or care about implementation
        validation = self.provider.validate(cn=cn, **kwargs)
        if not validation.get("valid"):
            return CertificateOutput(
                success=False,
                message="Validation failed",
                error=validation.get("error", "Unknown error")
            )

        return self.provider.create(cn=cn, **kwargs)

    def get_capabilities(self) -> Dict[str, Any]:
        """Get provider capabilities"""
        key_types = self.provider.get_supported_key_types()
        capabilities = {}
        for kt in key_types:
            capabilities[kt] = self.provider.get_supported_key_strengths(kt)
        return capabilities


# AI usage pattern
def ai_pattern_6_interface():
    """Example: AI uses abstract interface through factory"""
    
    # AI requests a provider from factory
    provider = CertificateProviderFactory.create("openssl")
    
    # AI uses only the interface methods
    capabilities = provider.get_supported_key_types()
    strengths = provider.get_supported_key_strengths("rsa")
    
    # AI creates manager and works with it
    manager = CertificateManager(provider)
    
    result = manager.create_certificate(
        cn="example.com",
        key_type="rsa",
        key_strength=2048
    )
    
    return result


# Example: Easy testing with mock
def ai_with_mock_provider():
    """Example: Same code but using mock provider (for testing)"""
    
    # Only change: use different provider
    mock_provider = CertificateProviderFactory.create("mock")
    manager = CertificateManager(mock_provider)
    
    # AI code is identical to real usage
    result = manager.create_certificate(
        cn="test.example.com",
        key_type="rsa"
    )
    
    return result


if __name__ == "__main__":
    result = ai_pattern_6_interface()
    print(f"Pattern 6 - Abstract Interface: {result.message}")
    
    mock_result = ai_with_mock_provider()
    print(f"Mock Provider: {mock_result.message}")
