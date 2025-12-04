"""
Validators for JSON schemas and OpenAPI specifications.

This module provides utilities to validate schemas and OpenAPI specs
for consistency and correctness.
"""

from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import json
import yaml


class SchemaValidator:
    """Validate JSON schemas for consistency and best practices."""
    
    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize schema validator.
        
        Args:
            schema_path: Optional path to schema directory. If not provided,
                        uses the package's schema directory.
        """
        self.schema_path = schema_path
        if self.schema_path is None:
            from autogensocial_contracts import schemas
            self.schema_path = Path(schemas.__file__).parent
    
    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load a JSON schema by name.
        
        Args:
            schema_name: Name of the schema
            
        Returns:
            Dictionary containing the JSON schema
        """
        schema_file = self.schema_path / f"{schema_name}.json"
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_schema(self, schema_name: str) -> Tuple[bool, List[str]]:
        """
        Validate a JSON schema.
        
        Args:
            schema_name: Name of the schema to validate
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        
        try:
            schema = self.load_schema(schema_name)
        except FileNotFoundError:
            return False, [f"Schema file not found: {schema_name}"]
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        
        # Check for required top-level fields
        if '$schema' not in schema:
            issues.append("Missing '$schema' field")
        
        if 'title' not in schema:
            issues.append("Missing 'title' field")
        
        if 'type' not in schema:
            issues.append("Missing 'type' field")
        
        # Check for properties if type is object
        if schema.get('type') == 'object':
            if 'properties' not in schema:
                issues.append("Object schema missing 'properties' field")
            
            # Check for required fields
            required = schema.get('required', [])
            properties = schema.get('properties', {})
            
            for req_field in required:
                if req_field not in properties:
                    issues.append(f"Required field '{req_field}' not defined in properties")
            
            # Check for 'id' field in properties
            if 'id' not in properties:
                issues.append("Object schema should have an 'id' property")
        
        return len(issues) == 0, issues
    
    def validate_all_schemas(self) -> Dict[str, Tuple[bool, List[str]]]:
        """
        Validate all schemas in the schema directory.
        
        Returns:
            Dictionary mapping schema names to validation results
        """
        results = {}
        
        for schema_file in self.schema_path.glob("*.json"):
            schema_name = schema_file.stem
            is_valid, issues = self.validate_schema(schema_name)
            results[schema_name] = (is_valid, issues)
        
        return results
    
    def check_schema_consistency(
        self,
        schema1_name: str,
        schema2_name: str,
        shared_field: str
    ) -> Tuple[bool, List[str]]:
        """
        Check if a shared field has consistent definition across schemas.
        
        Args:
            schema1_name: Name of first schema
            schema2_name: Name of second schema
            shared_field: Name of the field to check
            
        Returns:
            Tuple of (is_consistent, list of differences)
        """
        schema1 = self.load_schema(schema1_name)
        schema2 = self.load_schema(schema2_name)
        
        props1 = schema1.get('properties', {})
        props2 = schema2.get('properties', {})
        
        if shared_field not in props1:
            return False, [f"Field '{shared_field}' not in {schema1_name}"]
        
        if shared_field not in props2:
            return False, [f"Field '{shared_field}' not in {schema2_name}"]
        
        field1 = props1[shared_field]
        field2 = props2[shared_field]
        
        differences = []
        
        # Check type consistency
        if field1.get('type') != field2.get('type'):
            differences.append(
                f"Type mismatch: {field1.get('type')} vs {field2.get('type')}"
            )
        
        # Check format consistency
        if field1.get('format') != field2.get('format'):
            differences.append(
                f"Format mismatch: {field1.get('format')} vs {field2.get('format')}"
            )
        
        return len(differences) == 0, differences


class OpenAPIValidator:
    """Validate OpenAPI specifications for consistency and best practices."""
    
    def __init__(self, openapi_path: Optional[Path] = None):
        """
        Initialize OpenAPI validator.
        
        Args:
            openapi_path: Optional path to OpenAPI directory. If not provided,
                         uses the package's openapi directory.
        """
        self.openapi_path = openapi_path
        if self.openapi_path is None:
            from autogensocial_contracts import openapi
            self.openapi_path = Path(openapi.__file__).parent
    
    def load_spec(self, spec_name: str) -> Dict[str, Any]:
        """
        Load an OpenAPI specification by name.
        
        Args:
            spec_name: Name of the spec
            
        Returns:
            Dictionary containing the OpenAPI specification
        """
        spec_file = self.openapi_path / f"{spec_name}.yaml"
        with open(spec_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def validate_spec(self, spec_name: str) -> Tuple[bool, List[str]]:
        """
        Validate an OpenAPI specification.
        
        Args:
            spec_name: Name of the spec to validate
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        
        try:
            spec = self.load_spec(spec_name)
        except FileNotFoundError:
            return False, [f"OpenAPI spec file not found: {spec_name}"]
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML: {e}"]
        
        # Check OpenAPI version
        if 'openapi' not in spec:
            issues.append("Missing 'openapi' version field")
        elif not spec['openapi'].startswith('3.'):
            issues.append(f"Unsupported OpenAPI version: {spec['openapi']}")
        
        # Check for required top-level fields
        if 'info' not in spec:
            issues.append("Missing 'info' section")
        else:
            info = spec['info']
            if 'title' not in info:
                issues.append("Missing 'info.title' field")
            if 'version' not in info:
                issues.append("Missing 'info.version' field")
        
        if 'paths' not in spec:
            issues.append("Missing 'paths' section")
        
        # Check paths
        paths = spec.get('paths', {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                    continue
                
                # Check for operationId
                if 'operationId' not in operation:
                    issues.append(f"Missing operationId for {method.upper()} {path}")
                
                # Check for responses
                if 'responses' not in operation:
                    issues.append(f"Missing responses for {method.upper()} {path}")
        
        return len(issues) == 0, issues
    
    def validate_all_specs(self) -> Dict[str, Tuple[bool, List[str]]]:
        """
        Validate all OpenAPI specs in the openapi directory.
        
        Returns:
            Dictionary mapping spec names to validation results
        """
        results = {}
        
        for spec_file in self.openapi_path.glob("*.yaml"):
            spec_name = spec_file.stem
            is_valid, issues = self.validate_spec(spec_name)
            results[spec_name] = (is_valid, issues)
        
        for spec_file in self.openapi_path.glob("*.yml"):
            spec_name = spec_file.stem
            is_valid, issues = self.validate_spec(spec_name)
            results[spec_name] = (is_valid, issues)
        
        return results
    
    def check_schema_refs(self, spec_name: str) -> Tuple[bool, List[str]]:
        """
        Check if all schema references in the spec are valid.
        
        Args:
            spec_name: Name of the spec to check
            
        Returns:
            Tuple of (all_valid, list of invalid references)
        """
        spec = self.load_spec(spec_name)
        schemas = spec.get('components', {}).get('schemas', {})
        invalid_refs = self._find_invalid_refs(spec, schemas)
        
        return len(invalid_refs) == 0, invalid_refs
    
    def _find_invalid_refs(
        self,
        obj: Any,
        schemas: Dict[str, Any],
        path: str = ""
    ) -> List[str]:
        """
        Recursively find invalid schema references.
        
        Args:
            obj: Object to check for references
            schemas: Valid schema definitions
            path: Current path in the object tree
            
        Returns:
            List of invalid reference paths
        """
        invalid_refs = []
        
        if isinstance(obj, dict):
            if '$ref' in obj:
                ref = obj['$ref']
                # Check if it's a component schema reference
                if ref.startswith('#/components/schemas/'):
                    schema_name = ref.split('/')[-1]
                    if schema_name not in schemas:
                        invalid_refs.append(f"{path}: {ref}")
            
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                invalid_refs.extend(self._find_invalid_refs(value, schemas, new_path))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                invalid_refs.extend(self._find_invalid_refs(item, schemas, new_path))
        
        return invalid_refs
