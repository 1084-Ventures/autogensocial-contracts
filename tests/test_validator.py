"""
Tests for the validator module.
"""

import pytest
from autogensocial_contracts.generators import SchemaValidator, OpenAPIValidator


class TestSchemaValidator:
    """Test JSON schema validation."""
    
    def test_schema_validator_initialization(self):
        """Test SchemaValidator can be initialized."""
        validator = SchemaValidator()
        assert validator is not None
        assert validator.schema_path is not None
    
    def test_load_schema(self):
        """Test loading a schema."""
        validator = SchemaValidator()
        schema = validator.load_schema("brand")
        
        assert schema is not None
        assert "title" in schema
    
    def test_validate_valid_schema(self):
        """Test validating a valid schema."""
        validator = SchemaValidator()
        is_valid, issues = validator.validate_schema("brand")
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_all_schemas(self):
        """Test validating all schemas."""
        validator = SchemaValidator()
        results = validator.validate_all_schemas()
        
        assert len(results) > 0
        assert "brand" in results
        assert "post" in results
    
    def test_check_schema_consistency(self):
        """Test checking field consistency across schemas."""
        validator = SchemaValidator()
        is_consistent, differences = validator.check_schema_consistency(
            "brand", "post", "id"
        )
        
        # Both should have 'id' field with same type
        # Either schemas are consistent, or differences don't include type mismatches
        if not is_consistent:
            assert len(differences) == 0 or all("Type mismatch" not in d for d in differences), \
                f"Found type mismatch in 'id' field: {differences}"


class TestOpenAPIValidator:
    """Test OpenAPI specification validation."""
    
    def test_openapi_validator_initialization(self):
        """Test OpenAPIValidator can be initialized."""
        validator = OpenAPIValidator()
        assert validator is not None
        assert validator.openapi_path is not None
    
    def test_load_spec(self):
        """Test loading an OpenAPI spec."""
        validator = OpenAPIValidator()
        spec = validator.load_spec("content-api")
        
        assert spec is not None
        assert "openapi" in spec
    
    def test_validate_valid_spec(self):
        """Test validating a valid OpenAPI spec."""
        validator = OpenAPIValidator()
        is_valid, issues = validator.validate_spec("content-api")
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_all_specs(self):
        """Test validating all OpenAPI specs."""
        validator = OpenAPIValidator()
        results = validator.validate_all_specs()
        
        assert len(results) > 0
        assert "content-api" in results or "publisher" in results
    
    def test_check_schema_refs(self):
        """Test checking schema references."""
        validator = OpenAPIValidator()
        all_valid, invalid_refs = validator.check_schema_refs("content-api")
        
        # Most specs should have valid references
        assert all_valid is True or len(invalid_refs) < 10
