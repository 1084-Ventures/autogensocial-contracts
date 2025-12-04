"""
Tests for the client generator module.
"""

import pytest
from autogensocial_contracts.generators import ClientGenerator


class TestClientGenerator:
    """Test API client generation."""
    
    def test_client_generator_initialization(self):
        """Test ClientGenerator can be initialized."""
        generator = ClientGenerator()
        assert generator is not None
        assert generator.openapi_path is not None
    
    def test_load_spec(self):
        """Test loading an OpenAPI specification."""
        generator = ClientGenerator()
        spec = generator.load_spec("content-api")
        
        assert spec is not None
        assert "openapi" in spec
        assert "info" in spec
        assert "paths" in spec
    
    def test_get_endpoints(self):
        """Test extracting endpoints from OpenAPI spec."""
        generator = ClientGenerator()
        spec = generator.load_spec("content-api")
        endpoints = generator.get_endpoints(spec)
        
        assert len(endpoints) > 0
        assert "/brands" in endpoints or any(path.startswith("/brands") for path in endpoints.keys())
    
    def test_get_base_url(self):
        """Test extracting base URL from OpenAPI spec."""
        generator = ClientGenerator()
        spec = generator.load_spec("content-api")
        base_url = generator.get_base_url(spec)
        
        assert base_url is not None
        assert len(base_url) > 0
    
    def test_generate_python_client(self):
        """Test generating Python API client."""
        generator = ClientGenerator()
        code = generator.generate_client("content-api", output_format="python")
        
        assert "class ContentAPIClient" in code
        assert "def __init__" in code
        assert "async def" in code
        assert "httpx" in code
    
    def test_generate_typescript_client(self):
        """Test generating TypeScript API client."""
        generator = ClientGenerator()
        code = generator.generate_client("publisher", output_format="typescript")
        
        assert "export class PublisherAPIClient" in code
        assert "constructor" in code
        assert "async" in code
        assert "fetch" in code
    
    def test_custom_class_name(self):
        """Test generating client with custom class name."""
        generator = ClientGenerator()
        code = generator.generate_client(
            "content-api",
            output_format="python",
            class_name="MyCustomClient"
        )
        
        assert "class MyCustomClient" in code
    
    def test_invalid_output_format(self):
        """Test that invalid output format raises ValueError."""
        generator = ClientGenerator()
        
        with pytest.raises(ValueError, match="Unsupported output format"):
            generator.generate_client("content-api", output_format="invalid")
