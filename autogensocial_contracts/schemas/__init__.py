"""
JSON schemas for AutoGenSocial platform data models.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# Get the directory containing this file
_current_dir = Path(__file__).parent

def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema by name.
    
    Args:
        schema_name: Name of the schema (e.g., 'brand', 'post', 'postPlan', 'socialAccount')
        
    Returns:
        Dictionary containing the JSON schema
        
    Raises:
        FileNotFoundError: If the schema file doesn't exist
        json.JSONDecodeError: If the JSON file is invalid
    """
    # Remove .json extension if provided
    if schema_name.endswith('.json'):
        schema_name = schema_name[:-5]
    
    schema_file = _current_dir / f"{schema_name}.json"
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema not found: {schema_file}")
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_available_schemas() -> list[str]:
    """Get list of available schema files.
    
    Returns:
        List of schema names that are available
    """
    json_files = _current_dir.glob("*.json")
    
    schemas = []
    for file_path in json_files:
        if file_path.name != "__init__.py":  # Exclude any __init__.py files
            schemas.append(file_path.stem)
    
    return sorted(schemas)

# Pre-defined schema names for easy access
BRAND = "brand"
POST = "post"
POST_PLAN = "postPlan"
SOCIAL_ACCOUNT = "socialAccount"

__all__ = [
    "load_schema",
    "get_available_schemas",
    "BRAND",
    "POST",
    "POST_PLAN",
    "SOCIAL_ACCOUNT",
]
