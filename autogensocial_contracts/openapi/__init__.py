"""
OpenAPI specifications for AutoGenSocial platform services.
"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml

# Get the directory containing this file
_current_dir = Path(__file__).parent

def load_openapi_spec(service_name: str) -> Dict[str, Any]:
    """Load an OpenAPI specification by service name.
    
    Args:
        service_name: Name of the service (e.g., 'content-api', 'image-composer', 'publisher')
        
    Returns:
        Dictionary containing the OpenAPI specification
        
    Raises:
        FileNotFoundError: If the specification file doesn't exist
        yaml.YAMLError: If the YAML file is invalid
    """
    spec_file = _current_dir / f"{service_name}.yaml"
    if not spec_file.exists():
        raise FileNotFoundError(f"OpenAPI specification not found: {spec_file}")
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_available_specs() -> list[str]:
    """Get list of available OpenAPI specification files.
    
    Returns:
        List of service names that have OpenAPI specifications
    """
    yaml_files = _current_dir.glob("*.yaml")
    yml_files = _current_dir.glob("*.yml")
    
    specs = []
    for file_path in list(yaml_files) + list(yml_files):
        specs.append(file_path.stem)
    
    return sorted(specs)

# Pre-defined service names for easy access
CONTENT_API = "content-api"
IMAGE_COMPOSER = "image-composer" 
PUBLISHER = "publisher"

__all__ = [
    "load_openapi_spec",
    "get_available_specs",
    "CONTENT_API",
    "IMAGE_COMPOSER", 
    "PUBLISHER",
]
