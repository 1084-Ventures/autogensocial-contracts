"""
Tests for the CRUD generator module.
"""

import pytest
from autogensocial_contracts.generators import CRUDGenerator


class TestCRUDGenerator:
    """Test CRUD operation generation."""
    
    def test_crud_generator_initialization(self):
        """Test CRUDGenerator can be initialized."""
        generator = CRUDGenerator()
        assert generator is not None
        assert generator.schema_path is not None
    
    def test_load_schema(self):
        """Test loading a JSON schema."""
        generator = CRUDGenerator()
        schema = generator.load_schema("brand")
        
        assert schema is not None
        assert "title" in schema
        assert schema["title"] == "Brand"
        assert "properties" in schema
    
    def test_get_model_name(self):
        """Test extracting model name from schema."""
        generator = CRUDGenerator()
        schema = generator.load_schema("brand")
        model_name = generator.get_model_name(schema)
        
        assert model_name == "Brand"
    
    def test_get_required_fields(self):
        """Test extracting required fields from schema."""
        generator = CRUDGenerator()
        schema = generator.load_schema("brand")
        required = generator.get_required_fields(schema)
        
        assert "id" in required
        assert "name" in required
    
    def test_get_properties(self):
        """Test extracting properties from schema."""
        generator = CRUDGenerator()
        schema = generator.load_schema("brand")
        properties = generator.get_properties(schema)
        
        assert "id" in properties
        assert "name" in properties
        assert "description" in properties
    
    def test_generate_python_create(self):
        """Test generating Python CREATE operation."""
        generator = CRUDGenerator()
        code = generator.generate_create_operation("brand", output_format="python")
        
        assert "async def create_brand" in code
        assert "brand: Brand" in code
        assert "db: AsyncSession" in code
        assert "return" in code
    
    def test_generate_python_read(self):
        """Test generating Python READ operation."""
        generator = CRUDGenerator()
        code = generator.generate_read_operation("brand", output_format="python")
        
        assert "async def get_brand" in code
        assert "async def list_brands" in code
        assert "brand_id: str" in code
    
    def test_generate_python_update(self):
        """Test generating Python UPDATE operation."""
        generator = CRUDGenerator()
        code = generator.generate_update_operation("brand", output_format="python")
        
        assert "async def update_brand" in code
        assert "brand_id: str" in code
        assert "BrandUpdate" in code
    
    def test_generate_python_delete(self):
        """Test generating Python DELETE operation."""
        generator = CRUDGenerator()
        code = generator.generate_delete_operation("brand", output_format="python")
        
        assert "async def delete_brand" in code
        assert "brand_id: str" in code
        assert "return" in code
    
    def test_generate_typescript_create(self):
        """Test generating TypeScript CREATE operation."""
        generator = CRUDGenerator()
        code = generator.generate_create_operation("post", output_format="typescript")
        
        assert "export async function createPost" in code
        assert "post: Post" in code
        assert "fetch" in code
    
    def test_generate_sql_create(self):
        """Test generating SQL CREATE TABLE statement."""
        generator = CRUDGenerator()
        code = generator.generate_create_operation("brand", output_format="sql")
        
        assert "CREATE TABLE brands" in code
        assert "id VARCHAR(255) NOT NULL PRIMARY KEY" in code
        assert "CREATE INDEX" in code
    
    def test_generate_all_operations(self):
        """Test generating all CRUD operations at once."""
        generator = CRUDGenerator()
        operations = generator.generate_all_operations("brand", output_format="python")
        
        assert "create" in operations
        assert "read" in operations
        assert "update" in operations
        assert "delete" in operations
        
        assert "async def create_brand" in operations["create"]
        assert "async def get_brand" in operations["read"]
        assert "async def update_brand" in operations["update"]
        assert "async def delete_brand" in operations["delete"]
    
    def test_invalid_output_format(self):
        """Test that invalid output format raises ValueError."""
        generator = CRUDGenerator()
        
        with pytest.raises(ValueError, match="Unsupported output format"):
            generator.generate_create_operation("brand", output_format="invalid")
